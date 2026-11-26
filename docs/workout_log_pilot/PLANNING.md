# Plan Review — Workout Log pilot (#736 step 2)

**Status** — Gate 0 signed by the owner on 2026-11-20, with both corrections in Section 0
(check C10 and criteria 18 and 19). The council reviewed Astra's Plan v1 (`a0daa535`) on
2026-11-20. [Plan v2](#plan-v2) maps all 19 signed criteria to checks and incorporates
the 26 findings recorded at `28c8a151`. The council verified Plan v2 at `c3b3a767` on
2026-11-20 and found no blocker. TS-1 is resolved. See
[Council verification of Plan v2](#council-verification-of-plan-v2). The owner approved
Gate 1 on 2026-11-20, and Astra implements Plan v2. Gate 2 and the merge stay with the owner.

**Implementation and visual review, 2026-11-22.** The pilot is implemented on
`feat/736-workout-log-pilot` in `604663ad`. On the pinned control at `5dc83cef`, the
frame check reproduced C1–C4 and C10 failures. The 390 px Bench Press record measured
898.5 px high on the control and 241 px on the pilot. The 1360 px table's Exercise column
measured 299 px. Neither desktop width had a clipped heading. Both candidate runs
produced the same metrics across 22 combinations of size, scale, theme and content.

Local evidence lives under `artifacts/workout-log-frame/`. Compare
`control-ns2lb1yv/` with `candidate-9ilqky7_/` for the ordinary screenshots.
`candidate-wml_q6h5/` holds the independent repeat. Each directory includes the
fixture and measurements. Run `.venv/Scripts/python.exe e2e/scripts/run_workout_log_frame.py`
to reproduce the candidate, or append `--control-ref 5dc83cef` for the control.
The next owner decision is visual sign-off for baseline generation.

**Planning size:** Large under
[`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md#plan-stage-routing), because the work edits
shared CSS surfaces. Gate 0 and a council-reviewed Gate 1 both precede implementation.

**Sources.** [Issue #736](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/736): the
"Plan: Astra" comment (the adopted plan), "Review of Fable's plan: Astra" and the "Owner
decisions" comment. Step 1 merged as PR #740 (`main` at `5dc83cef`). The zero-RIR display fix
shipped earlier as PR #738.

**What was read.** The Log template, stylesheet, script and specs at `5dc83cef`. The checkout was
on `fix/733-mobile-menu-panel` (`dedee8bb`); `git diff origin/main HEAD` shows none of the files
cited below differ from `main`.

---

## Section 0 — Requirements Brief

**Raw request** (verbatim)

> Start step 2 of #736, the Workout Log pilot. Step 1 merged as PR #740 (main
> 5dc83cef). The adopted plan is the "Plan: Astra" comment and the "Owner
> decisions" comment on #736. This is Large under
> docs/ai_workflow/QUALITY_GATE.md (shared CSS surfaces): Gate 0, then Gate 1,
> before any application code.
>
> Run /requirements, write Section 0 of a new docs/<feature>/PLANNING.md, and
> stop for my Gate 0 approval. The brief must pin:
> - concrete values for radii, type sizes and weights, the page gutter per
>   width, and the surface rules;
> - the phone exercise card: which fields are in the main row (RIR visible; RPE
>   shown when it is what was logged) and which sit behind details;
> - desktop Planned/Logged column groups, with sorting bound to individual
>   field headers, not column position;
> - a reproducible acceptance check: fixture, selectors and counting method
>   (the audit script was not kept; only
>   artifacts/design-review-20261119/measurements.json remains);
> - which Log page overrides are deleted, and where the shared components live
>   (no new CSS bundle);
> - which test pins and visual baselines will move.
> Include a phone and a desktop mockup of the same workout for my by-eye
> review. No application code in this step.

**Problem**

The app has no shared page frame or component set, so each screen is styled separately. On the
Workout Log this shows in four ways.

- **The page has four left edges.** At 1440 px the audit measured the title text at x = 49, the
  import panel's heading at 75, the first button at 44 and the table at 17
  (`artifacts/design-review-20261119/measurements.json`).
- **A logged exercise is hard to use on a phone.** Step 1 gave each field the full card width, but
  one exercise is still a stack of 17 label and value rows, about 898 px tall at 390 px (PR #740).
- **The desktop table is hard to read.** It has 17 columns whose headings truncate at 1440 px, and
  each column has its own colour tint.
- **The page restyles shared components itself.** `pages-workout-log.css` holds 228 rules and 685
  declarations, 242 of them `!important`. A new shared rule loses to these unless they are
  deleted in the same change.

The pilot must give the Log one frame and one component set that later pages can adopt, and must
remove the page rules those components replace.

### Mockups

One static page renders the same seven-exercise workout as phone cards and as the desktop table.
It is a design reference, not application code, and sits in the gitignored `artifacts/` folder.

| File in `artifacts/workout-log-pilot/` | Shows |
|---|---|
| `mockup.html` | The live page. Resize the window to move between layouts. The corner control switches theme and the empty state. Sorting and Details work. |
| `phone-390-light.png`, `phone-390-dark.png` | Phone, 390 px |
| `phone-390-light-details-open.png` | Phone with the first card's Details open |
| `phone-390-light-empty.png`, `desktop-1440-light-empty.png` | Empty log |
| `tablet-768-light.png`, `laptop-1280-light.png`, `desktop-1200-light.png` | Two-column cards below 1360 px |
| `laptop-1366-light.png` | Table at the narrowest common width that gets it |
| `desktop-1440-light.png`, `desktop-1440-dark.png` | Desktop, 1440 px |

The workout is the six rows of `GYM - Full Body - Workout A` from the visual seed, with logged
values varied to show each rule (a logged RPE, an RIR of 0, a row that only matches the plan, two
unlogged rows), plus one 62-character catalog name. The mockup's navigation bar is a placeholder;
navigation is step 4.

### Pinned design values

Where a value is new it is marked ⚠️ and repeated under *Assumptions made*.

#### Radius

| Role | Value | Used by |
|---|---|---|
| Control | 8 px | Buttons, fields, thumbnails, sort controls |
| Panel | 12 px | Panels, cards, the table's panel |
| Modal | 16 px | Modals and drawers (not applied on the Log in this step, see A10) |
| Pill | 999 px | Status badges and chips |

Today the measured radius on almost every surface is already 8 px, and the page header is 20 px
(`layout.css:54`).

#### Type

Inter, weights 400, 500 and 600 only. Six sizes. ⚠️ Sizes are fixed and do not follow the
seven-band `--font-size-*` tokens (A2).

| Role | Size / line height | Weight |
|---|---|---|
| Page title | 24 / 32 px at 768 px and wider, 20 / 28 px below | 600 |
| Section and empty-state title | 18 / 24 px | 600 |
| Exercise name on a card, logged value on a card | 16 / 22 px and 16 / 24 px | 600 and 500 |
| Body, table cells, buttons, planned line | 14 / 20 px | 400 (500 for buttons and logged values, 600 for the exercise name in the table) |
| Labels, column headings, captions, badges, legend | 12 / 16 px | 500 for labels, headings and badges, 400 for captions |

Numeric cells and fields use tabular numerals and are right-aligned. For comparison, the audit
measured 19.2 px for today's title, 14.4 px for buttons and 13.6 px for table text at 1440 px.

#### Page gutter and frame

| Viewport width | Gutter | Top of the page header |
|---|---|---|
| Below 768 px | 16 px | 16 px below the navbar |
| 768 to 1359 px | 24 px | 24 px below the navbar |
| 1360 px and wider | 32 px | 24 px below the navbar |

- The page header, every panel and the log region share the gutter as their left and right edge.
- ⚠️ Content is capped at 1800 px wide and centred (the existing `--container-max-fhd`).
- The page header is plain text on the page background: the title on the left, the page's actions
  on the right. It has no panel, underline bar, gradient or centring. Below 768 px the actions
  drop under the title.
- Spacing uses the existing 4 px scale (`--s-1` to `--s-7`). Panels and cards have 16 px padding,
  cards are 12 px apart.

#### Surfaces

| Surface | Rule |
|---|---|
| Canvas | `--surface-0` (`#eef1f6` light, `#101419` dark) |
| Panel | Opaque `--surface-2` (`#ffffff` light, `#26313d` dark), 1 px hairline border, no shadow |
| Table header row, row hover | `--surface-1` |
| Field | `--surface-2` in light, `--surface-0` in dark, 1 px `--ink-3` border |
| Raised | Dropdowns, drawers, modals and toasts only: `--shadow-elev-2` |

- Inside the page content there is no `box-shadow`, `backdrop-filter`, gradient or inset shadow.
- ⚠️ The hairline is `#dfe3ec` light and `#3a4654` dark.
- Field borders use `--ink-3` because it clears 3:1 against the field surface (3.16:1 light,
  5.10:1 dark against the panel). `e2e/visual-field-separator.spec.ts` already requires 3:1 on
  this page.
- Secondary text uses `--ink-2`. `--ink-3` is for borders and icons only, because as text on
  white it is 3.16:1.
- Dark theme is a token swap. The new components carry no `[data-theme='dark']` rule of their own.
- ⚠️ The per-column colour tints (`metric-lane--*`) and the three-colour routine cell are dropped
  (A7).

#### Buttons and status

| Variant | Appearance |
|---|---|
| Primary | Filled indigo, white text. ⚠️ `#4263eb` in light (A6), `#5264ad` in dark (today's dark `--action-primary`) |
| Secondary | Panel surface, 1 px `--ink-3` border, `--ink-1` text |
| Ghost | No fill or border, `--ink-2` text |
| Danger | Secondary shape with danger text (⚠️ `#c0362c` light, `#f08a80` dark). A filled danger button appears only as a modal's confirm action |

- Two sizes: 40 px and 32 px tall, 14 / 20 px text at weight 500, 8 px radius. Below 768 px every
  button, field and disclosure is at least 44 px tall.
- A page shows at most one filled primary button. On an empty log it is
  **Import Current Workout Plan**. On a populated log there is none: Import becomes secondary and
  Clear Log is the danger variant.
- Status badge: a pill with a text label. ⚠️ Achieved is `#0b7a55` on `#e6f6ef` (light) and
  `#5fd3a6` (dark). Pending is `#8a5300` on `#fdf1d8` (light) and `#f3c56b` (dark).
- Comparison marks keep their arrows. ⚠️ Improved is the Achieved green, Below Target is the danger
  red, and Maintained is neutral `--ink-2` instead of today's yellow.

Contrast ratios in this section were computed with the WCAG formula in a script. They were not
measured with axe on a rendered page.

### Phone exercise card

Cards are used below 1360 px (A1): one column below 768 px, two columns from 768 px.

**Always visible**

| Element | Content |
|---|---|
| Thumbnail | 40 px, or a neutral placeholder when the exercise has none |
| Exercise name | In full. It wraps and is never truncated |
| Routine | One caption line, for example `Workout A · GYM · Full Body` |
| Status | Achieved or Pending badge |
| Planned line | For example `3 sets × 8–12 reps · 60 kg · RIR 2`. It shows RIR, RPE or both, whichever the plan holds |
| Logged fields | Min Reps, Max Reps, Weight, RIR, in that order, each a field-shaped target |
| Logged RPE | Joins the row as a fifth field when the record has a stored logged RPE (0 counts). ⚠️ It also joins when the plan prescribes RPE and no RIR (A5) |
| Details | A disclosure button |

**Behind Details**

- The planned values in full: Sets, Min Reps, Max Reps, RIR, RPE, Weight.
- Logged RPE, when it is not already in the main row.
- Last Progression date.
- Reference Video and Delete Entry.

Rules:

- RIR is always in the main row (owner decision 2). RPE never appears twice in one card.
- Each record has one editable representation. The card and the desktop row are the same record
  in the page, laid out differently by width.
- Activating a logged value opens the existing editor. Saving, cancelling, clearing and server
  rejection behave as shipped in #738.
- ⚠️ Details is closed on load and its state is not remembered. The row number is not shown on a
  card (A12).

In the mockup at 390 px a card with a one-line name is 226 px tall with four logged fields and
242 px with five. Step 1 measured about 898 px for the same row, and the audit 1,318 px.

### Desktop table

The table is used at 1360 px and wider, inside one panel.

- **Two header rows.** The first holds the group headings **Planned** (Sets, Min Reps, Max Reps,
  RIR, RPE, Weight) and **Logged** (Min Reps, Max Reps, RIR, RPE, Weight). The second holds the 17
  field headings in today's order: #, Routine, Exercise, the six planned fields, the five logged
  fields, Last Progression, Progressive Overload, Actions.
- **Headings.** A field heading may wrap to two lines and is never truncated. Each data cell is
  associated with both its group and its field, so a logged RIR cell is announced as
  "Logged RIR".
- **Sorting.** Each sortable field heading sorts by its own field, identified by the field and
  not by its position in the row. The group headings and Actions do not sort. The comparison
  itself does not change: numeric when both values parse as numbers, text otherwise. Today the
  sorter numbers every `th` and reads `row.cells` at that index
  (`static/js/modules/workout-log.js:246-291`), which is why a group row would shift every sort.
- ⚠️ A sort control is a keyboard-reachable button and the sorted heading exposes `aria-sort`
  (A11).
- **Cells.** Planned values are plain numbers in `--ink-2`. Logged values are field-shaped boxes
  32 px tall. Rows are 56 px tall with a 32 px thumbnail. Groups are separated by a hairline.
- **Routine.** Two lines in plain text: the workout, then environment and program.
- **Empty log.** ⚠️ A message panel replaces the log region. The table stays in the document (A9).

In the mockup the Exercise column is 306 px at 1440 px, 232 px at 1366 px and 226 px at 1360 px,
and no heading truncates at any of the three. At 1359 px the mockup shows two-column cards. All
four widths were measured with no vertical scrollbar.

### Acceptance check ("frame check")

The audit script was not kept, so the pilot commits its own check. Anyone must be able to rerun it
with one documented command.

**Fixture**

- The database built by `e2e/scripts/prepare_visual_db.py` (the `PW_VISUAL_SEED=1` path). It
  holds six log rows for `GYM - Full Body - Workout A`: Barbell Bench Press, Barbell Bent Over Row
  and Barbell Squat are logged; Barbell Deadlift, Barbell Curl and Barbell Seated Military Press
  are not.
- The check runs on its own throwaway copy and never shares a server run with `visual.spec.ts`.
- Before measuring it applies these scripted edits:

| Row | Edit | Case it provides |
|---|---|---|
| Barbell Deadlift | Logged min 5, max 5, weight 120, RIR 0 | A stored zero |
| Barbell Squat | Logged RPE 9 | RPE is what was logged |
| Barbell Curl | Logged weight 30 | Exercise order and Logged Weight order differ |
| Barbell Seated Military Press | Plan changed to RPE 8 with no RIR. Nothing logged | A blank row, and an exercise planned by RPE before its first entry (A5) |
| `Cable Standing Single Arm Internally Rotated Incline Chest Fly` | Added, unlogged | A long name (62 characters) |

Every seed row is planned by RIR and none has a planned RPE, so the Barbell Seated Military Press
edit is the only case that exercises A5 before anything is logged. The Barbell Squat edit does
not, because its RPE is already logged. The mockup has no such row; its Barbell Squat card shows
the five-field layout.

**Conditions**

- Chromium at 390 × 844, 768 × 1024 and 1440 × 900, light and dark, empty and populated.
- App scale level 6 (factor 1). One extra pass at level 8 (factor 1.2) at 390 and 1440 px, used
  for the overflow and readability checks only.
- Two extra passes at 1359 × 900 and 1360 × 900, light theme, populated, at scale level 6, used
  for the switch check (C10) only.
- Fonts loaded, transitions and animations disabled before any value is read.

**Selectors**

The population is every element inside `#main-content` that has a client rect. ⚠️ Component
selectors use the `ui-` prefix (A8); if Gate 1 renames the classes the check follows.

| Role | Selector |
|---|---|
| Page header block, title | `.ui-page-header`, `.ui-page-title` |
| Panel | `.ui-panel` |
| Button, by variant | `.ui-btn` |
| Field | `.ui-field` |
| Status badge | `.ui-badge` |
| Log region and records | `#workout-log-table`, `#workout-log-table tr[data-log-id]` |

**Counting method**

Values are read with `getComputedStyle` and `getBoundingClientRect`. "Distinct" means the set of
serialized values after rounding lengths to 0.5 px.

| # | What is counted | Pass |
|---|---|---|
| C1 | Left and right edges of the page header block, each panel and the log region | One left edge, equal to the gutter for that width. Right edge is the viewport width minus the gutter |
| C2 | `border-top-left-radius` of every element with a non-zero radius | Distinct values are within 8, 12 and 999 px |
| C3 | `font-size` and `font-weight` of every element that has its own text, excluding Font Awesome glyphs | Sizes within 12, 14, 16, 18, 20, 24 px. Weights within 400, 500, 600. The title is the largest text on the page |
| C4 | `box-shadow`, `backdrop-filter`, `background-image` of every element | All `none` |
| C5 | `document.documentElement.scrollWidth` | Not above the viewport width, at every width and in the scale 1.2 pass |
| C6 | At 390 px: name height, field boxes, card height | The six seed names take at most two lines. The long name shows in full with no ellipsis. Every logged field is at least 44 × 44 px. A closed card with a one-line name is at most 250 px tall |
| C7 | At 1440 px: heading overflow, Exercise column width | No heading has `scrollWidth` above `clientWidth`. The Exercise column is at least 220 px |
| C8 | Source: `[data-theme` selectors that name a `ui-` class, outside `tokens.css` | 0 |
| C9 | Source: rules in `pages-workout-log.css` that target a shared component (families below) | 0 for each deleted family. No `!important` is added, and the file's total falls below 242 |
| C10 | At 1359 px and at 1360 px: which layout renders. At 1360 px also heading overflow and Exercise column width | At 1359 px the records are two-column cards and no field heading is displayed. At 1360 px the table is displayed with its group and field headings, no heading has `scrollWidth` above `clientWidth`, and the Exercise column is at least 220 px. C5 passes at both widths |

C7 keeps its 1440 px checks. C10 repeats the heading and Exercise column checks at the narrowest
width that gets the table, where the mockup leaves 6 px over the 220 px limit.

**Control.** The check is evidence only if it also fails where it should. It must fail C1 to C4
on `main` at `5dc83cef`, and give identical output on two consecutive runs of the pilot branch.
It must also fail C10 there, because `main` still shows the table at 1359 px.
The raw output of all three runs goes under `artifacts/` and is summarized in the pull request.

### Log page overrides that are deleted, and where components live

**Where the shared components live.** No new bundle and no new `<link>`; the cap stays at 18.

| File | Receives |
|---|---|
| `static/css/tokens.css` | New tokens for the radius roles, hairline, status colours, primary fill, type roles and gutter. Additive: no existing token changes value |
| `static/css/layout.css` | The page frame: container gutter, page header, title, actions |
| `static/css/components.css` | Panel, button, field, status badge, data table, record card, empty state |
| `static/css/pages-workout-log.css` | Log-only layout: column widths keyed by field, the card's internal arrangement, editor positioning |
| `static/css/theme-dark.css` | Nothing for the Log |

The existing shared rules (`.page-header`, `.collapsible-frame`, `.btn-calm-*`, `.table-calm`,
`.tbl`, `.frame-calm-glass`) stay for the nine routes not yet migrated. The Log stops using them.

**What is deleted from `pages-workout-log.css`.** Counts are from a parse of the file at
`5dc83cef` with comments stripped. A rule is counted in every family its selector matches, so
the rows overlap.

| Family (selector contains) | Rules | Declarations | `!important` | After the pilot |
|---|---:|---:|---:|---|
| Table chrome (`.workout-log-table`, `.tbl`, `.table`): glass header and cells, zebra, hover filter, column tints, dark copies, `nth-child` widths | 130 | 379 | 182 | Chrome deleted. Only field-keyed column widths remain |
| Frame (`.workout-log-frame`, `.workout-log-controls-frame`, `.import-*`) | 46 | 182 | 52 | Deleted |
| Collapsible frame (`.collapsible-frame`, `.frame-header`, `.frame-title`, `.collapse-toggle`) | 20 | 77 | 16 | Deleted with the import panel (A3) |
| Legend (`.progression-legend`, `.legend-*`) | 18 | 59 | 6 | Reduced to layout |
| Form field (`.form-control`, `.editable-input`, `.number-input`, spinner) | 14 | 52 | 19 | Field chrome deleted. Editor positioning stays |
| Modal (`.modal`, `#clearLogModal`) | 12 | 19 | 10 | Kept in this step (A10) |
| Button (`.btn`, `.btn-*`) | 9 | 33 | 7 | Deleted |
| Container (`body`, `html`, `.container-fluid`) | 9 | 17 | 11 | Deleted. The shared frame owns the gutter |
| Badge (`.badge`) | 6 | 12 | 7 | Deleted |
| Page header (`.page-header`) | 5 | 11 | 0 | Deleted |

**Shared bundles that name the Log.** `components.css` has 65 lines that mention
`.workout-log-page`, `.workout-log-table`, `.workout-log-frame` or `.workout-log-controls-frame`;
`layout.css` has 2 and `theme-dark.css` has 1. Most are `:is(...)` groups shared with the Plan and
summary pages. The Log's branch is removed from each group that would restyle a new component.
The other branches are untouched.

**Template.** The empty `div.btn-group` placeholder at `templates/workout_log.html:281-283` is
removed. Its own comment defers that removal to the next change that moves these captures.

### Test pins and visual baselines that move

**Hooks that stay**, so that functional specs keep working unedited:
`#workout-log-table`, `data-testid="workout-log-table"`, `.workout-log-table`,
`.workout-log-frame`, `.workout-log-page`, `tr[data-log-id]`, every `data-field` value,
`.editable-text`, `.exercise-name`, `img.exercise-thumbnail`, `.log-play-video-btn`, `.badge`,
`td[data-label="Progressive Overload"]`, `#import-from-plan-btn` with the text
"Import Current Workout Plan", `#clear-log-btn`, `#clearLogModal`, `#confirm-clear-log-btn`,
`.progression-legend` with the words Improved, Maintained and Below Target, and the `h1` text
"Workout Log".

**Pins that move**

| Pin | Why it moves |
|---|---|
| `e2e/workout-log.spec.ts:54` and `:96-112` | Assert the import panel and its collapse toggle (A3) |
| `e2e/workout-log.spec.ts:81-94` and `:131-142` | Require a heading containing "scored" (A4) |
| `e2e/workout-log.spec.ts:203-221` | Requires every cell to be wider than 85% of the row at 375 and 390 px. That is step 1's stacked layout, which the card replaces |
| `e2e/empty-states.spec.ts:148-153` | Expects the empty table to be visible (A9). The test at `:352-362` only needs the table body attached and still holds |
| `e2e/accessibility.spec.ts:898` | `AXE_REGISTER` pins 2 `color-contrast` nodes for `workout_log:light`. The target is 0. `docs/testing_phase2/A11Y_EXCEPTIONS.md` row X7 changes with it. Which two nodes they are was not identified in this pass |
| `e2e/visual-field-separator.spec.ts:36` | Selects `table.tbl--responsive` on the Log. The 3:1 requirement stays; the selector moves if the class does |
| `e2e/visual-helpers.ts:256-257` and `tests/test_visual_capture_contracts.py:297` | Capture-time CSS aimed at the Log table's header cells and first column |
| `tests/test_css_cascade_contracts.py` | `test_workout_log_drops_inert_responsive_table_and_frame_families`, `test_workout_log_drops_cascade_dead_header_and_cell_glass` and `test_workout_log_hover_rules_own_only_their_live_filters` assert the text of rules that are deleted. Three more tests name a Log selector once or a few times |
| `tests/test_css_field_separator_contracts.py:36`, `tests/test_css_wp4_4_components_contracts.py:270`, `:275`, `:495`, `tests/test_css_wp4_4_i_is_repair_contracts.py`, `tests/test_css_wp4_4_layout_contracts.py:591` | Pin the `.workout-log-page` branch of shared `:is()` groups, or the shape of `pages-workout-log.css` |
| `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` with `tests/test_css_wp4_4_a_baseline_contracts.py` | Pins shared-surface line counts, `!important` totals, Stylelint counts, the `:is()` family records, pinned declarations and the snapshot manifest |
| `docs/test_inventory/` | Regenerated when any test is added, removed or renamed |

No Vitest file covers `workout-log.js` today, so the Vitest pins move only if the plan adds cases.
`tests/test_workout_log_routes.py` checks only for `id="workout-log-table"` and does not move.

**Visual baselines that move: 24 files**

| Spec | Captures | Per platform | Platforms |
|---|---|---:|---|
| `visual.spec.ts` | `workout-log-{mobile,tablet,desktop}-{light,dark}.png` | 6 | win32, linux |
| `visual-baseline-thumbnails.spec.ts` | `log-{mobile,tablet,desktop}-{light,dark}.png` | 6 | win32, linux |

- The suite's viewports are 375, 768 and 1440 px, so they capture one-column cards, two-column
  cards and the table.
- The four `snapshotManifest` digests in `CSS_PHASE4_WP4_4_A_BASELINE.json` change with them and
  are edited by hand for the affected directories only.
- win32 baselines are regenerated locally. The win32 thumbnail captures have no CI path at all.
  linux baselines come from the `Deep Gate Visual (Linux)` generate mode.
- No baseline is regenerated before the owner's by-eye sign-off, and never with a blanket
  `--update-snapshots`.
- Every other committed baseline must compare clean without regeneration.

**Documents updated in the same change:** `docs/product/DESIGN_BRIEF.md` (the rules that ship),
`docs/product/APP_FLOW.md` (the Log section), `docs/CSS_OWNERSHIP_MAP.md` if it lists a moved
selector, and `A11Y_EXCEPTIONS.md` if the axe count moves.

**Ordering.** PR #743 (#733, mobile menu) merged on 2026-11-19 as `44797998`. It edited
`DESIGN_BRIEF.md`, `APP_FLOW.md` and the test inventory, which the pilot also edits, so the pilot
branches from `main` at or after that commit. #743 changed none of the files this brief cites.

**Acceptance criteria**

"The fixture" means the frame check's fixture above. Widths are 390, 768 and 1440 px at app scale
1 unless stated.

1. **Gutter.** Given the Log at each width, in both themes, empty and populated, when the frame
   check reads the edges, then C1 passes: one left edge of 16, 24 or 32 px, and the page header
   starts 16 px below the navbar under 768 px and 24 px from 768 px.
2. **Radius, type and surfaces.** Given the same pages, when the frame check runs, then C2, C3 and
   C4 pass.
3. **One primary action.** Given an empty log, then the page content has exactly one filled
   primary button, Import Current Workout Plan. Given a populated log, then it has none, Import is
   secondary and Clear Log is the danger variant.
4. **Phone card content.** Given the fixture at 390 px, when the page loads, then each card shows
   the exercise name, routine, status, planned line and the logged Min Reps, Max Reps, Weight and
   RIR without opening Details and without sideways scrolling. The Barbell Squat card (RPE was
   logged) and the Barbell Seated Military Press card (planned by RPE, nothing logged) also show
   logged RPE in the main row. Every other card has logged RPE behind Details.
5. **Phone card size.** Given the fixture at 390 px, then C6 passes.
6. **Details.** Given a card, when Details is activated by touch or keyboard, then the planned
   values, Last Progression, Reference Video and Delete Entry appear, and the button reports its
   expanded state.
7. **Two-column cards.** Given the fixture at 768 px, then records are cards in two columns and C5
   passes.
8. **Desktop table.** Given the fixture at 1440 px, then the table shows the Planned and Logged
   group headings over their fields and C7 passes.
9. **Sorting follows the field.** Given the fixture at 1440 px with the group row present, when
   the Exercise heading is activated, then Barbell Bench Press is first and
   `Cable Standing Single Arm …` is last. When the Logged Weight heading is activated, then the
   rows that have a weight appear as Curl 30, Bench Press 60, Bent Over Row 70, Squat 100,
   Deadlift 120. Activating a heading with Enter from the keyboard gives the same result.
10. **Editing is unchanged.** Given a logged field on a card or in the table, then: Enter or
    leaving the editor saves a changed value once; Escape restores the saved value; clearing
    stores `null` and shows `--`; a rejected value shows the warning and leaves the row unchanged;
    and a reload shows the stored value.
11. **Zero and status.** Given the Barbell Deadlift record with planned RIR 2, when RIR 0 is
    saved and the page reloads, then the field shows `0` with its Improved mark and the badge
    reads Achieved, matching `GET /check_progression/<id>`.
12. **Phone end to end.** Given the fixture at 390 px, when the lifter finds a card by its
    exercise name, enters a value, leaves the Log and returns, then that same card shows the saved
    value and the correct status.
13. **Dark theme and contrast.** Given dark theme, then C8 passes. The axe `color-contrast` count
    for `/workout_log` does not rise in either theme, with a target of 0 in light.
14. **Overrides are gone.** Given the merged change, then C9 passes.
15. **Larger scale and long names.** Given app scale level 8 at 390 and 1440 px, then C5 passes
    and the long exercise name is readable in full.
16. **Other pages do not move.** Given the full visual matrix on both platforms, then every
    capture other than the 24 listed above compares clean without regeneration, and the runtime
    bundle count is still 18.
17. **Evidence.** Given the pull request, then it contains the frame check and its command, the
    three control runs, and ordinary (not capture-helper) screenshots of the Log at 390 and
    1440 px in both themes, empty and populated, plus one at scale level 8.
18. **The switch.** Given the fixture at 1359 px, then the records are two-column cards. Given
    the fixture at 1360 px, then the table is shown, no field heading is truncated and the
    Exercise column is at least 220 px wide, so C10 passes. Criterion 8 still holds at 1440 px.
19. **First RPE entry.** Given the Barbell Seated Military Press record at 390 px, planned by RPE
    with no RIR and with nothing logged, when the page loads and Details stays closed, then its
    logged RPE field and its logged RIR field are both visible in the main row. When the lifter
    activates that RPE field, enters a value and saves, then the value is stored, and a reload
    shows it in the main row.

**Calculation surface**

- `none`.
- The change is presentation only. It does not touch `utils/effective_sets.py`, the progression
  decision (`check_progression` on the server, `computeProgressionState` in
  `static/js/modules/workout-log.js`), any route, the schema, or an API response shape. Which
  card row shows RPE is a layout rule and feeds no calculation.

**In scope**

- The shared page frame, tokens and component set, added to `tokens.css`, `layout.css` and
  `components.css`.
- The Workout Log rebuilt on them: page header and actions, record cards below 1360 px, grouped
  table from 1360 px, empty state, legend, status badge.
- Field-bound sorting and header associations.
- Deleting the Log page overrides and Log branches listed above.
- The committed frame check, the moved test pins, the 24 baselines, and the four documents.

**Out of scope / non-goals**

- Any other route, the navbar, and navigation icons (steps 3 and 4).
- Motion polish (step 5).
- Changing how values sort, where blank values land, or adding a sort control to cards.
- New Log features: the unbound `GET /export_workout_log`, routine grouping, a "next exercise"
  marker, auto-advance.
- Restyling the Clear Log modal (A10).
- Changing the value of any existing token, or the existing shared rules other routes use.
- Adding the frame check to the required CI set. That is a separate contract change
  (`tests/test_playwright_shard_launcher_contracts.py` pins the set at 25).
- Calculation logic, database schema and API response shapes.

**Assumptions made**

Each is a default I chose where the request and the adopted plan do not decide. The mockup shows
every one of them, with one gap: it has no RPE-planned row without a logged value (A5), which the
fixture and criterion 19 now cover.

- ⚠️ **A1. Cards below 1360 px, table from 1360 px.** Today the switch is at 576 px. The 17 fields
  need about 1,280 px to show without truncation, and 1360 px is the navbar's existing compact
  breakpoint. Consequence: a 1280 px laptop gets two-column cards, and widths from 577 to 1359 px
  lose column sorting, which cards do not offer. Today's phone layout already hides the header
  row (`layout.css:1477` and `:1532`).
- ⚠️ **A2. Fixed type sizes.** The new components do not follow the seven-band density tokens.
  App scale and browser zoom remain the density controls. On a 4K display at scale 1, body text
  is 14 px where today's token gives 16 px.
- ⚠️ **A3. The import panel becomes page-header actions.** The collapsible "Import from Workout
  Plan" panel and its description are removed. The description's wording moves to the empty
  state.
- ⚠️ **A4. "Logged" replaces "Scored" in visible text.** Field names, `data-field` values and API
  fields keep `scored_*`. The legend drops "scored better than planned".
- ⚠️ **A5. RPE-only plans.** When the plan prescribes RPE and no RIR, logged RPE is in the main
  row before anything is logged. The owner's wording covers only "when it is what was logged";
  without this, a lifter who plans by RPE opens Details on every exercise.
- ⚠️ **A6. A darker indigo for the filled primary button.** White on `--accent` (`#4c6ef5`)
  computes to 4.32:1, under the 4.5:1 minimum. `#4263eb` computes to 4.98:1. `--accent` itself
  does not change.
- ⚠️ **A7. New colours, and less colour coding.** The hairline, status and danger-text values
  above are new and become tokens. Column tints and the coloured routine lines are dropped, and
  Maintained becomes neutral.
- ⚠️ **A8. The `ui-` class prefix.** No class in `static/css/` uses it today. Gate 1 may choose
  another name.
- ⚠️ **A9. Empty state.** A message panel replaces the log region; the table stays in the
  document so its hooks resolve.
- ⚠️ **A10. The Clear Log modal is not restyled.** Its 12 page rules stay as the one exception to
  C9 until the modal component is migrated.
- ⚠️ **A11. Sort controls** are buttons with `aria-sort`, a small addition to "bound to field
  headers".
- ⚠️ **A12. Card details.** Details is closed on load and not remembered. Delete Entry and
  Reference Video move behind Details on cards. The row number is not shown on cards.
- ⚠️ **A13. Content is capped at 1800 px.** Today the Log is full-bleed.
- ⚠️ **A14. New copy.** "No exercises logged yet", "Compared with the plan:", "Details",
  "Delete Entry", "Reference Video", "Set Date" and "Logged RPE".
- ⚠️ **A15. The frame check's thresholds** (250 px card, 220 px Exercise column) come from the
  mockup's measurements with a margin, not from the built page.

**Open questions for the user**

1. **Who implements, and who reviews?** Owner decision 4 names Astra as implementer of the pilot
   and Fable as reviewer of each pull request. This brief was written by Fable at the owner's
   request. If Fable also reviews the pilot's pull request, that review is not independent of
   these requirements. Please confirm the roles for Gate 1 and for the implementation.

No other question blocks Gate 0. Each ⚠️ above needs an accept or a correction.

### Section 0 sign-off — GATE 0

- [x] User confirms the acceptance criteria match intent. *(Confirmed 2026-11-20 with two
  corrections, quoted below.)*
- [x] User reviewed the assumptions and corrected or accepted each one.
- [x] Blocking questions are answered.

#### Owner answers, 2026-11-20

Given by the owner in the #736 run-preparation session, after `mockup.html` and the phone,
1280 px laptop and desktop screenshots were opened for review. Each answer below is the owner's
own selection or typed text, quoted as given.

| Assumption | Owner's answer |
|---|---|
| A1. Cards below 1360 px, table from 1360 px | "Accept 1360 px (Recommended)" |
| A3. The import panel becomes page-header actions | "Accept (Recommended)" |
| A4. "Logged" replaces "Scored" in visible text | "Accept 'Logged' (Recommended)" |
| A5. RPE-only plans show logged RPE in the main row | "Accept (Recommended)" |
| A12. Card details | "Accept (Recommended)" |
| A13. Content is capped at 1800 px | "Accept the cap (Recommended)" |
| A2, A6, A7, A8, A9, A10, A11, A14, A15 (asked as one question) | "Accept all nine (Recommended)" |

**Acceptance criteria.** Asked whether the 17 criteria match intent, the owner did not confirm
them as drafted and gave two corrections instead:

> Test the 1360 px switch. Verify cards at 1359 px and the table at 1360 px. Check heading fit
> and the 220 px Exercise column at 1360 px. The current table check runs at 1440 px.
>
> Test the first RPE entry. Include an exercise planned with RPE and no RIR, with nothing logged
> yet. On a phone, verify that RPE is visible and editable without opening Details and that RIR
> is still visible. The current Squat fixture starts with RPE already logged, so it can pass even
> if the A5 behavior is missing.

Asked again whether the criteria match intent with those two added, the owner answered:
"Yes, with those two added (Recommended)".

Both corrections were folded into Section 0 on 2026-11-20 at the owner's request. The switch is
check C10 and criterion 18, with the 1440 px checks kept. The first RPE entry is the Barbell
Seated Military Press fixture edit and criterion 19. Checked the same day against a scratch copy
of `e2e/fixtures/database.visual.seed.db`: all six seed rows are planned by RIR and none has a
planned RPE, which is why the second correction is a scripted fixture edit. Which row carries the
edit, and the value RPE 8, were chosen when folding it in and are not the owner's words.

**Open question 1 (roles).**

| Asked | Owner's answer |
|---|---|
| Who implements the pilot, and who reviews it | "Keep decision 4 for the pilot" (the option read: Astra implements the Log pilot and Fable reviews it) |
| Who drafts the pilot's implementation plan for Gate 1 | "Astra drafts, Claude's council reviews (Recommended)" |
| Which gates the owner keeps | "I keep Gate 0 for every step of #736 and Gates 1 and 2 for the Workout Log pilot (step 2). For steps 3–5 only, I delegate Gate 1 after the required council review and Gate 2 after the required checks and reviews pass. Record each delegated approval in the step’s PLANNING.md." |

Gate 0 for the pilot is signed off by the owner. Gate 1 and Gate 2 for the pilot stay with the
owner, as does the merge of the pilot's pull request.

---

## Plan v1

**Goal** — A lifter can read the prescription and log a result on the same exercise card on a
phone, and compare and sort Planned and Logged fields in the desktop table.

**Scope**

- **In** — The shared frame and components opt into use on Workout Log. Deliver the card and
  grouped table, preserve the editor and actions, and implement the acceptance checks for all
  19 criteria in Section 0.
- **Out** — Workout Plan and other route migrations, navigation and motion, a new CSS bundle,
  card sorting, and Clear Log modal restyling. The calculation surface is empty. Routes,
  persistence behavior, database schema and API contracts stay as specified in Section 0.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `templates/workout_log.html` | Modify | One record row and editor per field, controlled card Details, grouped headers, header actions and empty panel. |
| `static/css/tokens.css`, `static/css/layout.css`, `static/css/components.css` | Modify | Add opt-in tokens, frame and components, and remove superseded Log branches from legacy selectors. |
| `static/css/pages-workout-log.css`, `static/css/theme-dark.css` | Modify | Retain Log geometry and the modal exception in the page bundle. Remove the superseded Log branch of the existing dark selector. Define the new components' dark values in tokens. |
| `static/js/modules/workout-log.js`, `static/js/modules/ui-handlers.js` | Modify | Field sort, disclosure and responsive placement. Keep the current save lifecycle and spinner behavior while giving the Log's field and date triggers keyboard access and styling the Log spinners through the shared component. |
| `e2e/scripts/run_workout_log_frame.py`, `e2e/playwright.workout-log-frame.config.ts`, `e2e/workout-log-frame.check.ts` | Add | Opt-in, serial Playwright check, independent scratch app and fixture, stable report. |
| `e2e/workout-log.spec.ts`, `e2e/empty-states.spec.ts`, `e2e/accessibility.spec.ts`, `e2e/visual-field-separator.spec.ts` | Modify | Update retired layout expectations, exercise real editing and keyboard paths, and update the verified axe and separator pins. |
| `e2e/visual-helpers.ts`, `tests/test_visual_capture_contracts.py`, CSS contract tests named in Section 0 | Modify as affected | Retarget only the Log-specific capture and CSS assertions. Preserve the contracts for remaining consumers. |
| `docs/CSS_PHASE4_WP4_4_A_BASELINE.json`, `docs/test_inventory/`, `docs/product/DESIGN_BRIEF.md`, `docs/product/APP_FLOW.md`, `docs/testing_phase2/A11Y_EXCEPTIONS.md`, `docs/CSS_OWNERSHIP_MAP.md` | Modify as affected | Document the shipped rules, ownership and proven pin changes. Use the inventory generator. |
| `e2e/__screenshots__/{win32,linux}/` | Update after owner sign-off | Only the six full-page and six thumbnail Log captures per platform named in Section 0. |

**Effort** — L · **Owner** — Astra · **Depends on** — #738, #740 and #743, present on
`44797998`. Gate 0 is signed. Claude's three-person council reviews this plan before the owner's
Gate 1. Fable reviews the PR, and the owner decides Gate 2 and merge.
See [the adopted plan](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/736#issuecomment-6995069056)
and [the owner's decisions](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/736#issuecomment-6995960502).

**Sequence**

1. After Gate 1, write the failing acceptance checks and prepare the seeded runner. Run the
   old-UI control before implementation and capture ordinary before screenshots. Keep local
   Playwright runs serial.
2. Wire the shared frame, tokens and page states. Move the Log markup and behavior to the
   existing save and action entry points. Remove the superseded overrides in the same change.
3. Finish the layout and behavior checks. Re-measure the axe and field-separator targets and
   update the affected contracts and docs. Compare the ordinary after screenshots against the
   approved mockups, including the actual app navbar and a populated table at 1360 px.
4. Get the owner's by-eye sign-off before any baseline generation. Use the pushed candidate
   branch for the Linux workflow, update the approved Log captures and their four manifest
   digests, then run the full platform comparison and other implementation gates. Open the
   PR for Fable's review and PR checks. Present the final diff and evidence for owner Gate 2
   and leave the merge to the owner.

### Frame, components and layout

- Accept A8's `ui-` prefix. `layout.css` owns `.ui-page-frame`, `.ui-page-header`,
  `.ui-page-title` and `.ui-page-actions`. `components.css` owns `.ui-panel`,
  `.ui-btn` with `--primary`, `--secondary`, `--ghost`, `--danger` and `--small`
  modifiers, `.ui-field`, `.ui-badge` with `--achieved` and `--pending` modifiers,
  `.ui-data-table`, `.ui-record-card` and `.ui-empty-state`. Use additive, role-named
  `--ui-*` values in `tokens.css`, aliasing existing surfaces, ink and spacing where they
  already match the brief. Scope state and geometry to the adopted classes. The old classes
  listed as hooks in Section 0 stay on their existing semantic elements where applicable.
- Put the page title and action buttons in the shared frame. Use the empty panel and description
  for an empty log, with the table present but hidden and its body empty. Hide the legend there.
  Keep Clear Log as the outline danger action and keep its modal. The populated state uses the
  secondary Import button. Preserve the existing request, toast and refresh behavior.
- Render one server-generated `tr[data-log-id]` per entry and keep all five scored fields and
  the date as single editor instances in their existing canonical cells. Use explicit, stable
  field keys on the 17 table columns and on their cells. At desktop widths keep native table
  layout with a `colgroup` for each metric group, `scope="colgroup"` on Planned and Logged,
  `scope="col"` on field headings and explicit `headers` IDs on grouped data cells. Keep the
  accessible Actions heading. Sort buttons carry the field key and the active `th` carries
  `aria-sort`. Decorative icons stay out of accessible names.
- Below 1360 px, the same table body becomes a card grid, with two columns from 768 px. Each
  record row lays out its cells in the card order. The existing row-number cell hosts a
  mobile-only Details button in place of its number. Planned sets hosts the mobile planned
  summary alongside a separately addressable detail value. The native button controls the IDs
  of that row's detail values and actions and updates `aria-expanded`. A single Reference Video
  button moves from the Exercise slot to the card Actions slot. Keep the date and Delete Entry
  controls in their canonical cells. Hide closed detail controls from both tab order and the
  accessibility tree. Verify the accessible field names and traversal order when the grid is
  active as well as the desktop group associations.
- Use one `matchMedia('(min-width: 1360px)')` listener to put the same cells in card or table DOM
  order. On a viewport change keep the focused field cell in place while moving its siblings
  around it. If the change hides the focused target, use the existing commit-on-leave behavior
  once and move focus to the associated disclosure or visible field. Preserve stable record IDs
  and the current row order when switching layouts. Details begins closed on a new page load.
- Start the 1360 px column budget with the Exercise column taking the remainder and the other
  columns totaling at most 1048 px including their padding. Use compact widths for # and Actions
  and wrapping headings for label pairs. The mockup leaves 6 px of spare Exercise width without
  a scrollbar. With 32 px gutters, a 17 px classic scrollbar and two 1 px panel borders leave
  1277 px, or 229 px for Exercise at that budget. Confirm the real CSS with both Chromium's
  normal scrollbar and a pass that reserves a classic gutter. Verify heading text, sort icon
  and focus outline fit together. Use the table panel as a named horizontal scroll region at
  larger app scales if needed. At scale 1 on both desktop acceptance widths the entire table
  fits. At scale 1.2 keep the exercise name fully readable and scrolling contained within the
  region. On cards allow the editor to span the card width while active so the 44 px controls,
  input and existing plus/minus buttons fit even with five resting fields.

### Sorting and editing

- Bind each sort button to the matching stable cell key, including non-metric fields. Use the
  current comparator and its ascending-first toggle, with the original value text separated
  from added mobile labels, spinner glyphs, action text and icons. Read confirmed scores from
  `.editable-text` on every sort so edits take effect without a reload. Preserve the existing
  blank and date comparison inputs, and leave group headers and Actions out of the sort.
  Use `data-sort-field` on the Log's buttons so the global `th[data-sort]` handler never
  binds to them. Drop the Log's legacy responsive-table opt-in so its other controller
  cannot hide the new keyed columns.
- Use native button triggers with names for the logged fields and date. Use the existing
  `initializeUIHandlers` editor, pending-write guard and `updateScoredValue` path. Keep the
  single Escape, Enter and focusout lifecycle, plus the arrow and badge outcomes of #738.
  Update presentation variants without replacing the badge's base class or making the
  comparison depend on visually hidden text. Use the existing raw planned and confirmed
  logged values. Derive the RPE placement from presence, treating `0` as a value and null,
  empty or legacy `'None'` as missing. The row gets the fifth field when logged RPE is present
  or planned RPE is present with planned RIR absent. Refresh placement after a confirmed RPE
  save or clear. Leave the RIR field visible for both branches. Preserve video, date, delete,
  Clear Log and Import handlers and remove the obsolete import-collapse handler. Apply A4's
  Logged wording to validation feedback and accessible names alongside the visible labels.
- Keep the score and date cell hooks used by the existing browser specs. Add or adjust browser
  coverage for touch and keyboard Details, field names, Enter/blur once, Escape, validation
  and server rejection, zero, clearing, and reload. Include an RPE edit starting behind Details
  and a viewport transition while editing to catch duplicate initialization or writes.
  **Add no Vitest cases.** The risk is the live DOM, focus lifecycle and network persistence.
  Cover those through Playwright and regenerate the inventory for the E2E changes. No change
  to the Vitest case list.

### Frame check and isolated fixture

Run from the repository root after the check is implemented:

```powershell
.venv/Scripts/python.exe e2e/scripts/run_workout_log_frame.py
```

The runner uses the active Python on other platforms (`python e2e/scripts/run_workout_log_frame.py`).
It creates a unique directory under `artifacts/workout-log-frame/`, prepares the committed
visual seed with `prepare_visual_db.py --source <committed seed> --output <scratch DB>`, and
binds all later DB and runtime paths to that directory. In a transaction through
`DatabaseHandler` with the explicit scratch path, locate the six rows by routine and exercise.
Assert the expected counts and seed values before updating. Apply the Section 0 edits to
Deadlift, Squat and Curl. Set Military Press to `planned_rpe = 8`, `planned_rir = NULL` with
all five scored values null. Add one unlinked record for the confirmed catalog name
`Cable Standing Single Arm Internally Rotated Incline Chest Fly` with 3 sets, 12–15 reps,
12.5 kg, planned RIR 2, empty results and a fixed timestamp. Assert the seven resulting rows
and the first-RPE precondition. The only persisted test data is in the scratch copy.

Launch the installed Playwright CLI with the dedicated config, Chromium, one worker, zero
retries and its own Playwright-managed server. The config uses the repo browser settings, a
loopback port outside the normal visual lane, an explicit server working directory and
`reuseExistingServer: false`. The launcher supplies DB path, isolated runtime root, output
path and port to the child. Server startup consumes the already prepared DB. The default
Playwright test glob and current CI shard ignore the `.check.ts` suffix. The dedicated
config selects only that file. The same command accepts an optional
`--control-ref 5dc83cef` for the old-UI control. In that mode, export the pinned tracked
source with `git archive` into the scratch directory and point the server and CSS source checks
at the export, using the current environment and test harness. No Git checkout is created.

Use the strict Playwright fixture and the real route. At base scale run the full
390/768/1440 × light/dark × populated/empty matrix. Set theme and scale before navigation
through the app's persisted settings, assert their applied values, wait for fonts and
disable only animations and transitions for measurements. Run the two larger-scale
readability passes and the 1359/1360 populated passes defined in Section 0. Measure headings
and inner sort labels, the Exercise cell width and horizontal overflow at both table widths.
Count card columns from visible record rectangles. Read source checks C8 and C9 from parsed
CSS with comments excluded, using the installed PostCSS parser. Account for only the
explicit Log geometry and Clear Log modal exceptions. Use the legacy selectors on the control
to measure real elements. Assert the old page fails C1–C4 and C10 for the named reasons.

Run populated geometry before editing. For criterion 19, target the Military Press row by
name, prove Details remains closed, RIR and RPE have visible triggers, and the confirmed
RPE is empty. Enter 9, wait for the successful update, verify the read endpoint and reload
the same record. Verify the Deadlift zero against the progression endpoint and exercise the
field-bound sort oracles from criterion 9. Then clear the scratch log through its existing
endpoint, prove it is empty and run the empty measurements. Capture the pre-edit normal
screenshots for evidence separately from measurements, alongside empty-state and scale-8
screenshots, with no visual-capture helper. Write stable ordered metrics to JSON with the
brief's 0.5 px rounding. Keep timing, paths and console logs outside this file. Save the
control and two independent candidate reports and require identical candidate metrics.

### Contrast and test pins

On unmodified `44797998`, a scratch copy of the existing axe test used the functional seed,
the 1440 × 900 Chromium viewport, the registered WCAG tags and the existing theme-settle
helper. Axe 4.14.0 reported 26 passing rules in each theme and zero log rows. The two
`workout_log:light` nodes were `#import-from-plan-btn` (**4.32:1**, white on `#4c6ef5`)
and `#clear-log-btn` (**4.11:1**, white on `#e44040`). Dark reported zero violations.
The raw probe is in `artifacts/736-plan-probe-496d95c4/axe-output.txt`.

The new approved primary fill and outlined danger action address those targets on this page.
Re-run the existing route scan and record the new target-level results before changing
`AXE_REGISTER` and X7. Also check populated cards, open Details, the table and the
active field in both themes. Keep the existing 3:1 field-separator contract, retarget it to
the shared field border and keep its negative control. Use the existing retained table ID
for the capture hooks, scoping first-column/card styles if necessary. Leave comparison
thresholds and other routes' scopes in place. Update only affected parts of the CSS baseline
ledger from the existing tool, including affected `:is()` records and pins with a measured
replacement where applicable. Keep unrelated entries and historical guarantees intact.

**Expected gates** — Astra's proposed union for the council's test strategist to verify.

- **pytest** — Full suite via `.venv/Scripts/python.exe -m pytest tests/ -q`, including
  the cascade, visual-selector, axe, console and snapshot-manifest contracts.
- **Chromium** — `workout-log`, `empty-states`, `accessibility`, `visual-field-separator`,
  `validation-boundary`, `error-handling`, `smoke-navigation`, `nav-dropdown`, `dark-mode`,
  `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening`
  and the dedicated frame check. Manually smoke real numeric and date editors, video
  actions, import and clear on the seeded app. Run `npm run test:js` for the shared
  UI handler touch and regenerate and check the inventory with its Python generator.
- **CSS and visual** — Seven-surface `node scripts/css_audit/stylelint_surfaces.mjs` with
  no increase by category, plus Stylelint on `pages-workout-log.css`. Use
  `PW_VISUAL_SEED=1` for the full `visual.spec.ts` matrix on both platforms and
  the thumbnail suites. After owner by-eye sign-off, Windows generation filters to
  `workout-log (mobile|tablet|desktop) (light|dark)$` and
  `log-(mobile|tablet|desktop)-(light|dark)$` in the respective specs. Verify that
  `--list` returns six cases per filter. Use Linux deep gate generate mode and import only the
  named Log captures, then run its compare mode on the final head. Require a clean
  first attempt. Review all expected PR checks, including Windows visuals, and confirm
  that only the 24 agreed snapshot files moved. Use `/verify-and-polish` and retain the
  results and screenshot paths for Gate 2 and Fable.

---

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| Plan v1 author | not applicable | Astra (Codex), assigned directly by the owner for step 2. No Claude `product-manager` wrote Section 0 or Plan v1. |
| Response matrix | not applicable | Proposed dispositions written by the main Claude session that ran the council, not by a `product-manager`. See the evidence gap below. |
| Plan v2 author | not applicable | Astra (Codex) revised the plan after the owner relayed the council findings on 2026-11-20. |
| `architecture-reviewer` | `aa1e122e4107e5b7f` | Fresh context, briefed with the file path and the owner's constraints only. |
| `test-strategist` | `ad8ed0a59bfb2dee4` | Same brief, plus the repository's known hidden CI gates to check. |
| `product-risk-reviewer` | `a5d5874a5d192824d` | Same brief, plus the RIR/RPE, #738 and database-isolation focus areas. |

**Same product-manager resumed for the matrix + Plan v2?** No. No `product-manager` took
part. Astra wrote Plan v1 outside the Claude agent system, and the owner's run prompt assigns
the revision to Astra.

**Evidence gap** — No `product-manager` continuity exists to record, because the owner's role
split puts the plan with Astra. The main Claude session wrote the response matrix below
because the run prompt asks only that the findings be recorded in this file. It did not
revise Plan v1. The three reviewers ran once each on `a0daa535`. No ID was invented and no
review was rerun.

---

## Council review of Plan v1

**Reviewed** — Plan v1 at `a0daa535` (branch `feat/736-workout-log-pilot`, based on
`origin/main` at `44797998`), on 2026-11-20. All three reviewers read the file cold and
checked its claims against the code. Each received the owner's constraints and the
proportionality rule: a finding blocks only if it names a concrete loss, a wrong result or a
blocked operation.

**Verdicts**

- `architecture-reviewer` — sound with non-blocking findings (8).
- `test-strategist` — blocking (2 blocking, 8 non-blocking).
- `product-risk-reviewer` — sound with non-blocking findings (8).

**Outcome** — One blocking finding is open, TS-1. The main session downgrades TS-2 to
non-blocking (reason in the matrix). The owner relays the findings to Astra, and Astra
revises Plan v1. The council then verifies the fixes before the plan goes to the owner for
Gate 1.

### Response matrix (proposed dispositions)

These are proposals for the owner and Astra. Gate 1 is the owner's decision. IDs refer to
the reviewer sections below: AR is `architecture-reviewer`, TS is `test-strategist` and PR
is `product-risk-reviewer`.

| ID | Finding | Severity | Proposed disposition | Action for Astra's revision |
|---|---|---|---|---|
| TS-1 | Criteria 3 (one primary), 4 (per-card RPE placement, including the Barbell Squat main-row case) and 12 (leave the Log and return) have no named check | **Blocking** (upheld) | Accept | Add a criterion-to-check table covering all 19 criteria. Suggested homes: criterion 3 counts visible `.ui-btn--primary` in the empty and populated frame-check passes; criterion 4 asserts RPE placement per record name; criterion 12 is a 390 px `workout-log.spec.ts` case that navigates away and back. Verified: Plan v1 names only a reload for persistence and names no primary-button or Squat check. |
| TS-2 | The Chromium list misses specs that load the shared `ui-handlers.js` editor | Downgraded to non-blocking | Accept | The described failure does not occur as written: Plan v1's gate list ends with `/verify-and-polish`, whose first step is the full `/verify-suite` (full pytest and full Chromium). State plainly that the full Chromium suite is the gate for the shared handler edit, so the targeted list is not read as the whole gate. |
| TS-3 | `tsc` and pyright are missing from the gates | Non-blocking | Accept | Add `npx tsc --noEmit` and `scripts/pyright_baseline_diff.py`. Type the new runner, because `main` has no pyright headroom. |
| TS-4 | A literal loopback origin or a hard wait in the new `.ts` files reds a pytest pin or the inventory | Non-blocking | Accept | Build URLs only from the passed port or `baseURL`. Use no `waitForTimeout`. |
| TS-5 | `.check.ts` sits outside the default glob and the CI shard | Non-blocking (claim verified) | Accept | Set an explicit `testMatch` in the dedicated config. No other change. |
| TS-6 | Criteria 18 and 19 have no regression pin after merge | Non-blocking | Accept | Add lighter assertions of both to `e2e/workout-log.spec.ts` and regenerate the inventory. |
| TS-7 | The "existing tool" wording for the CSS baseline ledger conflicts with `e2e/CLAUDE.md` | Non-blocking | Accept | Hand-edit the four manifest digests with the test's own algorithm. Hand-edit the other affected entries, or review an `emit_baseline.py` diff entry by entry. |
| TS-8 | Retargeted cascade tests must keep their negative assertions. The axe register and `A11Y_EXCEPTIONS.md` move together | Non-blocking | Accept | Say what each retargeted test asserts. Cite `tests/test_axe_contracts.py` among the pins. |
| TS-9 | Name the visual-baseline failure modes | Non-blocking | Accept | Record that `visual-windows` stays red until the win32 captures are pushed, and that `log-desktop-light` is a known flipper under its tolerance. |
| TS-10 | `visual-field-separator.spec.ts` covers 375 and 768 px, where the Log becomes cards | Non-blocking | Accept | Retarget the card fields as well as the 1440 px table. |
| AR-1 | The "legacy responsive-table opt-in" the plan drops is probably the `tbl--responsive` CSS class, not a controller opt-in | Non-blocking | Accept | Name the exact class or attribute. Verified: `templates/workout_log.html:66` has `tbl--responsive` and no `data-table-responsive`. |
| AR-2 | The positional `th` sorting must go, or group headers and Actions stay clickable | Non-blocking | Accept | State that `initializeSimpleTableSorting` and `sortTableByColumn` are removed, not wrapped. |
| AR-3 | Plan v1 edits `theme-dark.css`, which Section 0 says gets "Nothing for the Log" | Non-blocking | Accept | Say the edit is a removal only, name the selector, and record it in the ownership map and the baseline ledger. |
| AR-4 | Bootstrap classes kept on the same elements (`.table-striped`, `.btn`, `.badge`) can break C2 to C4 or force `!important` | Non-blocking | Accept | List which Bootstrap classes are dropped and which hook classes stay. |
| AR-5 | The `--control-ref` export needs `.venv` and `node_modules` to start | Non-blocking | Accept | Say the export reuses the working tree's `.venv` and `node_modules`. Keep the control at `5dc83cef`, because the owner-signed Section 0 names that commit. |
| AR-6 / PR-1 | The runner's database isolation is implicit. `HT_RUNTIME_DIR` alone copies the real database | Non-blocking | Accept | Set `DB_FILE` and `HT_RUNTIME_DIR` explicitly for every child process. Before launch, assert that the resolved path is under the run's scratch directory and is not the live path. Assert the server's path again after start. Add a refusal test. |
| AR-7 | A new file under `e2e/` could trip the inventory or spec-list pins | Non-blocking | Accept | Covered by TS-5 and the inventory regeneration already planned. |
| AR-8 | No coordination note for the shared-surface edits | Non-blocking | Accept | Add one line saying the shared CSS and `ui-handlers.js` edits are coordinated under #736. |
| PR-2 | A sort right after an edit orders rows by the old value | Non-blocking | Accept | Await the pending write before sorting, or re-sort after the save settles. Add an "edit, then click a header" case. |
| PR-3 | The `'--'` cleared sentinel is missing from the missing-value set. The display of a missing planned value is unspecified | Non-blocking | Accept | Add `'--'` for logged values. Specify the card and Details wording for a missing planned value. Keep the sort text unchanged. |
| PR-4 | The criterion 9 Exercise-sort oracle cannot fail, because the server already returns that order | Non-blocking (test honesty) | Accept | Assert the order after a second activation (descending), or after sorting by another field first. Criterion 9's wording stays as signed. |
| PR-5 | The criterion 11 oracle may save nothing, because the fixture already stores Deadlift RIR 0 and the editor skips an unchanged value | Non-blocking (test honesty) | Accept | Drive the zero through a real change (2, then 0). Judge it on a row where RIR is the only improving field. |
| PR-6 | Label text inside the value nodes, or the load-time `className` rewrite, can flip badges or cause spurious writes | Non-blocking | Accept | Assert that `.editable-text` holds only the bare value and that each row has one `data-field="planned_*"`. Assert that the load-time badge matches `GET /check_progression/<id>` for all seven rows. Name the load-time badge call as a site to change. |
| PR-7 | Focus handling after commit, Escape and re-placement is unspecified | Non-blocking | Accept | Return focus to the field's trigger. Focus the Details button when the field has moved behind closed Details. |
| PR-8 | The added Cable record's routine is not stated | Non-blocking | Accept | Pin it to `GYM - Full Body - Workout A` with `workout_plan_id` NULL. |

No finding is rejected or deferred.

### architecture-reviewer (agent `aa1e122e4107e5b7f`)

*Verbatim. Numbering is the reviewer's own; the matrix prefixes it with AR.*

I read the Plan v1 section against Section 0 and spot-checked its claims against the code. I found no blocking findings. The verdict is **sound with non-blocking findings**. I did not read the entire plan or every file it names: the Section 0 test-pin table (lines 372 to 560) is unread. In the CSS I only matched `tbl--responsive` rules. I did not run `gh issue view 736`.

1. **Non-blocking. Plan: "Drop the Log's legacy responsive-table opt-in so its other controller cannot hide the new keyed columns."**
   - Evidence:
     - `static/js/table-responsiveness.js:425` binds only `[data-table-responsive]` tables.
     - `templates/workout_log.html:64-66` has no such attribute. The table carries the class `tbl--responsive` and `data-visual-surface`.
     - My grep of `workout-log.js` and `table-responsiveness.js` found no `tbl--responsive` consumer, apart from the Log's own CSS (`pages-workout-log.css:261` and others).
   - Failure: the "opt-in" the plan removes is probably the `tbl--responsive` class, which is a CSS hook and not a controller opt-in. An implementer may delete a class that other CSS or tests still use, or miss a real opt-in that is set elsewhere.
   - Fix: name the exact attribute or class to drop. Confirm with `Grep "tableResponsive|data-table-responsive"` across `templates/` and `static/js/`. Drop the claim if nothing sets it for the Log.

2. **Non-blocking. Plan: "Use `data-sort-field` … so the global `th[data-sort]` handler never binds."**
   - Evidence: `ui-handlers.js:298` binds `th[data-sort]` on `th` elements only. The Log's current sorting is positional (`workout-log.js:246-291`, `columnIndex` and `a.cells[columnIndex]`), and it binds a click to every `th`, with a "Click to sort" title and a pointer cursor (lines 247-254).
   - Failure: the plan's field-keyed buttons would avoid the global handler. But if `initializeSimpleTableSorting` is not replaced, the group headers and Actions `th` stay clickable. Group headers would then sort by position. That contradicts "leave group headers and Actions out of the sort".
   - Fix: state explicitly that `initializeSimpleTableSorting` and `sortTableByColumn` are deleted and not wrapped.

3. **Non-blocking. Plan, Artifacts and the `components.css` and `layout.css` edits.**
   - Evidence: Section 0 says `theme-dark.css` receives "Nothing for the Log". Plan v1 says to "Remove the superseded Log branch of the existing dark selector" in `theme-dark.css`. Section 0 also notes 1 Log mention in `theme-dark.css`.
   - Failure: this is an edit to a shared dark bundle that Section 0 does not scope as a removal. Section 0 only says nothing is added.
   - Fix: say that the edit is a removal only. Name the selector, and record it in `CSS_OWNERSHIP_MAP.md` and the CSS baseline ledger, which the plan already lists.

4. **Non-blocking. Plan: "legacy hooks stay", for example `.badge`, `.workout-log-frame` and `.workout-log-table`, while the new classes carry the styling.**
   - Evidence: the template keeps these as hook classes on elements such as `workout-log-frame` at `workout_log.html:61` and `.table` at line 66.
   - Failure: Bootstrap's `.table` and `.table-striped` (also `.badge` and `.btn`) on the same elements bring Bootstrap styling into the check. This can break C2 to C4, which require no shadow, one radius set and no background image, and it can force `!important`.
   - Fix: drop `table-striped`, `table-calm` and `tbl` from the Log's table, and the Bootstrap `.btn` and `.badge` visual classes from the new components. Keep only the hook classes that specs read. List which classes are dropped, so the C9 count is predictable.

5. **Non-blocking. Plan: the `--control-ref 5dc83cef` control, with the pinned export pointing the server and CSS checks at it.**
   - Evidence: the plan's base is `44797998`. It includes #743 (navbar), which postdates `5dc83cef`.
   - Failure: the control runs on a different navbar from the candidate. C1 to C4 are scoped to `#main-content`, so the result is probably unaffected. But the export also needs the venv and `node_modules`. If the control is not wired to them, it cannot start.
   - Fix: say the export reuses the working tree's `.venv` and `node_modules`. Alternatively pin the control to `44797998`, which is what the code now does.

6. **Non-blocking. Plan: the scratch fixture, "In a transaction through `DatabaseHandler` with the explicit scratch path".**
   - Evidence: `utils/database.py:292-294` is `__init__(database_path=None)`, so it accepts a path. That matches the plan. This does follow the module rule on DB access.
   - Failure: none. Still, the plan relies on `HT_RUNTIME_DIR` alone not being enough, because `HT_RUNTIME_DIR` alone copies the real DB into the scratch runtime. The plan says "binds all later DB and runtime paths" but does not name `DB_FILE`.
   - Fix: name both `DB_FILE` and `HT_RUNTIME_DIR` as set by the launcher, and add an assertion that the server's DB path is the scratch path. This protects the "never the real database" constraint.

7. **Non-blocking. Plan: the `.check.ts` suffix and the dedicated config.**
   - Evidence: `playwright.config.ts:109` uses `testDir: './e2e'` with no `testMatch` override, so Playwright's default glob applies. It does not match `.check.ts`, which holds up the plan's claim. I found no `.check.ts` or `testMatch` references under `.github`.
   - Failure: none for CI collection. But `tests/` pins on the e2e inventory and `ci.yml` spec lists may glob `e2e/*.ts`. A new file under `e2e/` could trip the inventory-drift check or a spec-list pin (`== 25`).
   - Fix: confirm by running the inventory generator and `pytest` on the test-inventory pins before Gate 1 closes. The plan already says to regenerate the inventory.

8. **Non-blocking. Scope and shared surfaces.**
   - The plan edits shared files:
     - `components.css`, `layout.css`, `tokens.css`, `ui-handlers.js` and the dark bundle.
     - `docs/product/DESIGN_BRIEF.md` is listed, which meets the owner constraint.
   - It does not touch `app.py`, blueprints, schema or routes. The module-boundary, blueprint, schema, DB, response-contract, logger and normalization checks are all not applicable.
   - It does not declare a coordination note for the shared CSS and `ui-handlers.js` edits, per `WORKSTREAM_OWNERSHIP.md`. The owner's #736 decisions and the Gate 0 sign-off probably cover it.
   - Fix: add one line saying shared-surface edits are coordinated under #736.

**Verdict: sound with non-blocking findings.**

### test-strategist (agent `ad8ed0a59bfb2dee4`)

*Verbatim, except that the reviewer's own headings are demoted one level to fit this section.
Numbering is the reviewer's own; the matrix prefixes it with TS.*

**Review of Plan v1 (Workout Log pilot, #736 step 2): required gates, coverage gaps and hidden CI gates**

Evidence is read from the repo at the checked-out `feat/736-workout-log-pilot`. I edited nothing.

#### Findings

**1. BLOCKING — Criteria 3, 4 and 12 have no named check.**
- Plan text: "implement the acceptance checks for all 19 criteria" (Plan v1 Scope, line 625). The frame-check section (lines 743-795) and the Sorting and editing section (lines 735-741) name checks only for the following.
  - Criteria 1, 2, 5, 7, 8 and 15 and checks C1–C10, via the frame check.
  - Criteria 9, 11 and 19, via the frame check.
  - Criteria 6, 10 and part of 18, via the `workout-log.spec.ts` additions.
- Not named anywhere:
  - Criterion 3: exactly one filled primary when empty and none when populated. It is not in the C1–C10 table (lines 298-309) and not in the plan's counting steps.
  - Criterion 4, as a per-card rule: five cards must show logged RPE behind Details. The Barbell Squat main-row case is also not named.
  - Criterion 12: "leaves the Log and returns". The plan names reload only (line 738), not a navigate-away-and-back.
- Failure: three signed Gate 0 criteria can merge with no test, which is the "criterion with no check" case.
- Fix: add a criterion-to-check table to Plan v1. Suggested homes:
  - Criterion 3: the frame check, counting visible `.ui-btn--primary` in the empty and populated passes.
  - Criterion 4: assert RPE placement per record name.
  - Criterion 12: a phone-viewport `workout-log.spec.ts` case that navigates away and back.

**2. BLOCKING — The "Expected gates" Chromium list is too small for the `static/js/modules/ui-handlers.js` edit.**
- Plan text: Artifacts row for `static/js/modules/workout-log.js` and `ui-handlers.js`, and the Chromium list at lines 819-822.
- Evidence:
  - `static/js/app.js:6` and `:220` import and call `initializeUIHandlers()` on every page.
  - The QUALITY_GATE feature map has no `ui-handlers` row.
  - The Targeted-test derivation says to run the union, and `/verify-suite` when no meaningful coverage can be derived.
  - The plan's list omits `workout-plan`, `exercise-interactions`, `superset-edge-cases`, `progression`, `user-profile`, `volume-splitter`, `api-integration`, `browser-navigation-state`, `program-backup` and `fatigue-context`. These pages also load the changed global handler.
  - `workout-plan.spec.ts` and `exercise-interactions.spec.ts` also cover the shared components.css/layout.css Log-branch removals.
- Failure: a regression in the shared editor, tooltip or dropdown code on another page passes the plan's own gate set. The same specs are in the CI `e2e-functional-shard` list (ci.yml:487-511) and would first fail on the PR.
- Fix: name the full `/verify-suite` (full pytest plus the full Chromium suite). `/verify-and-polish` already runs it, so the plan is half-way there. Alternatively confine the ui-handlers.js edit to a Log-only module and keep the targeted list.

**3. NON-BLOCKING (add to the gate list) — `tsc` and pyright are missing from the gates.**
- `tsconfig.json:13` includes `e2e/**/*.ts` and `playwright.config.ts`. The new `e2e/workout-log-frame.check.ts` and `e2e/playwright.workout-log-frame.config.ts` are therefore checked by the required `Type Check (tsc blocking + pyright measure-only)` job. The new `e2e/scripts/run_workout_log_frame.py` falls under the repo-wide pyright baseline diff. `pyrightconfig.json` excludes only `artifacts`, `docs/archive` and similar, not `e2e/scripts`. Main has zero pyright headroom.
- Fix: add `npx tsc --noEmit` and `scripts/pyright_baseline_diff.py` to the gates, and write the runner with explicit types.

**4. NON-BLOCKING — A literal loopback origin or a hard wait in the new `.ts` files reds a pytest pin.**
- `tests/test_playwright_url_contracts.py:129-144` scans every `e2e/**/*.ts` with `https?://(127.0.0.1|localhost):\d+`. That includes the new config and check files. A literal origin with a port number, such as `http://127.0.0.1:5077` in the dedicated config, reds that test. Build the URL only from the passed port or from `baseURL`.
- `scripts/generate_test_inventory.py:509` counts `waitForTimeout` lines across `e2e` `*.ts` files. A hard wait in the check file creates inventory drift. Use no hard waits.

**5. NON-BLOCKING — Claim verified: `.check.ts` is outside the default glob and the CI shard.**
- The root config (`playwright.config.ts:109`) sets `testDir: './e2e'` and no `testMatch`, so Playwright's default `*.spec|test` pattern applies and `workout-log-frame.check.ts` is not matched.
- CI passes explicit `e2e/*.spec.ts` paths (ci.yml:486-511). The pytest contracts enumerate `*.spec.ts` only (`test_playwright_runner_contracts.py:170`, `test_playwright_shard_launcher_contracts.py:89`, `test_static_replay_contracts.py:44`).
- The dedicated config must set an explicit `testMatch`. The default pattern would not select the file either.
- Consequence: the frame check is never run by CI and not counted by the inventory (the generator's per-spec counts are `*.spec.ts` only). The plan itself keeps it out of CI (Section 0, lines 503-504).

**6. NON-BLOCKING — The two owner corrections have no regression pin after merge.**
- Criteria 18 (1359/1360 switch) and 19 (first RPE entry on a plan with RPE and no RIR) are asserted only in the opt-in `.check.ts`.
- The `workout-log.spec.ts` additions (lines 735-738) list Details, names, Enter/blur, Escape, validation, zero, clearing, reload, an RPE edit starting behind Details, and a viewport transition. They do not list the A5 RPE-only row or the 1359/1360 boundary.
- Fix: put a lighter assertion of each in `e2e/workout-log.spec.ts`, which runs in the required shard, injecting rows as `accessibility.spec.ts` does. These count as test additions, so regenerate the inventory.

**7. NON-BLOCKING — The CSS baseline "existing tool" instruction conflicts with repo guidance.**
- Plan text: "Update only affected parts of the CSS baseline ledger from the existing tool" (line 811).
- `e2e/CLAUDE.md` says to hand-edit only the affected `snapshotManifest` digest and never run `scripts/css_audit/emit_baseline.py`, which rewrites the whole file. QUALITY_GATE also routes a change to `emit_baseline.py` to `/verify-suite`.
- Verified: `tests/test_css_wp4_4_a_baseline_contracts.py:641-645` computes each manifest digest as `sha256` over file names plus byte sizes. The four digests (win32 and linux, `visual.spec.ts` and `visual-baseline-thumbnails.spec.ts`; JSON lines 831, 903, 924, 996) therefore move once the PNG bytes change, while the counts stay 66 and 15. The 24 files exist on disk (12 per platform: six `workout-log-*` and six `log-*`).
- Fix: state "hand-edit the four digests, compute them with the test's own algorithm". Hand-edit the `sharedSurfaceLines`, `:is()` and pinned-declaration entries too, or review the `emit_baseline.py` diff entry by entry.

**8. NON-BLOCKING — The retargeted cascade tests must keep their negative assertions.**
- The three `tests/test_css_cascade_contracts.py` tests named in Section 0 assert deleted rule text.
- The owner constraint is "never weaken or delete a test". Retarget each to assert the family is still absent from the Log bundle, not remove the case. The plan says "Retarget only" but does not say what replaces them.
- `tests/test_axe_contracts.py` binds `A11Y_EXCEPTIONS.md` rows to `AXE_REGISTER`. The plan's X7 and `AXE_REGISTER` edit must change both (`e2e/accessibility.spec.ts:898`, `workout_log:light` node count 2). Cite `tests/test_axe_contracts.py` among the pins.

**9. NON-BLOCKING — Visual-baseline plumbing is accurate but the failure modes should be named.**
- The `--list` filters match the real titles: `workout-log mobile light` in `visual.spec.ts:42`, and `log-${viewport}-${theme}` in the thumbnails spec at line 121.
- The thumbnails spec asserts at lines 131-137 that `#workout-log-table tbody tr` rows number at least 4 and that at least one `img.exercise-thumbnail` has a `/static/vendor/free-exercise-db/` src. Cards must keep real `tbody tr` and `img` nodes at 375 px, which the plan's "same row" design does.
- `e2e/CLAUDE.md` says `log-desktop-light` is a known-flipping capture under the 800 px tolerance. The plan's "clean first attempt" requirement is correct.
- `visual-windows` runs on every PR and compares only the win32 `visual.spec.ts` set. It is non-required, so merge is not blocked. It will be red until the win32 PNGs are pushed. Win32 thumbnails are compared only by the local run. Linux thumbnails are compared only by the weekly or dispatched Linux gate.

**10. NON-BLOCKING — Frame-check thresholds and the visual-field-separator spec.**
- `e2e/visual-field-separator.spec.ts` runs in the required shard against 3 viewports. At 375 px and 768 px the Log is now cards, so retarget the selector for card fields as well as the 1440 px table. The plan names only a selector rename.

#### Corrected gate list

- **pytest:** full `.venv/Scripts/python.exe -m pytest tests/ -q`. It covers the cascade, `test_visual_selector_contracts`, `test_css_wp4_4_*`, `test_axe_contracts`, `test_console_guard_contracts`, `test_playwright_url_contracts`, `test_playwright_*_contracts`, `test_visual_capture_contracts`, `test_css_wp4_4_a_baseline_contracts` (snapshot manifest) and `test_vitest_inventory_contracts` (unaffected, since no Vitest case is added).
- **Chromium:** `/verify-suite`. It should include at least the plan's list plus `workout-plan`, `exercise-interactions`, `superset-edge-cases`, `progression`, `user-profile`, `volume-splitter`, `api-integration` and `browser-navigation-state`. Also run `program-backup` isolated, and `fatigue-context`.
- **Visual:**
  - The full `visual.spec.ts` matrix with `PW_VISUAL_SEED=1`.
  - The thumbnails spec, win32 local.
  - `Deep Gate Visual (Linux)` in generate mode for the 12 Linux Log captures, then compare mode on the final head.
  - `visual-windows` on the PR.
- **Stylelint:** `node scripts/css_audit/stylelint_surfaces.mjs` with no category rise, plus Stylelint on `pages-workout-log.css`.
- **Type and static:** `npx tsc --noEmit` and `scripts/pyright_baseline_diff.py` (finding 3).
- **JS:** `npm run test:js`.
- **Inventory:** `python scripts/generate_test_inventory.py` then `--check`. Do it with no untracked `.md` in a globbed surface directory.
- **New:**
  - The frame check, `python e2e/scripts/run_workout_log_frame.py`, with its control run.
  - The `workout-log.spec.ts` tests for criteria 3, 4, 12, 18 and 19.
  - Manual smoke of editors, video, import and clear on the seeded app.
- **Known red:** `e2e/program-backup.spec.ts:79`, an isolated-pass flake.
- **Fixture work:** none. No `tests/conftest.py`, blueprint or table change.

#### Verdict

**Blocking.** Findings 1 and 2 must be resolved in Plan v1 before Gate 1.
- Finding 1: three signed acceptance criteria lack a named check.
- Finding 2: the global `ui-handlers.js` edit is gated by a targeted Chromium list. The canonical rule requires the union or `/verify-suite`, and a regression on another page would be caught first by the PR checks.
- The remaining findings are non-blocking.
- The plan's claims were verified against the repo: the `.check.ts` glob exclusion, the 24 baseline files, the four manifest digests, and the visual spec titles and filters.
- The Section 0 content itself matches the repo evidence I checked.

### product-risk-reviewer (agent `a5d5874a5d192824d`)

*Verbatim, except that two angle-bracket placeholders the transport had escaped are restored.
Numbering is the reviewer's own; the matrix prefixes it with PR.*

Verdict: sound with non-blocking findings. I found nothing that, as written, loses an edit, writes a wrong value or touches the real database. Nothing in the plan touches calculation logic, Effective sets, local-first stance or the schema. I made no edits.

**Verified against the code**
- **Database isolation holds.** `prepare_visual_db.py:84-93` assigns `utils.config.DB_FILE` before any initializer runs. `DatabaseHandler`, `catalog_seed.py:44` and `auto_backup.py:48,20` all read `utils.config.DB_FILE` at call time, and the auto-backup folder sits beside the DB. So the seed, the catalog upgrade and the startup backup all land in the scratch directory. `assert_safe_output` (`:41-53`) refuses the live path.
- **Zero and legacy values are handled correctly today.** The template uses `not in (none,'','None')` (`workout_log.html:133,153,173,194`), so 0 counts as logged. The server's `check_progression` (`utils/workout_log.py:129-152`) uses `is not None`, and the client's `computeProgressionState` (`workout-log.js:28-39`) uses `Number.isFinite(parseFloat(...))`. All three treat 0 as a value.
- **The save lifecycle guard holds.** `finish()` clears `activeScoreEditor` first (`ui-handlers.js:110-113`), so a second blur or an explicit commit during a layout switch cannot write twice.
- **Wording.** "Scored" becomes "Logged" in visible copy under owner-accepted A4. The only visible "Scored" strings are the table headings, `data-label`, the legend, and the toast at `ui-handlers.js:127` with its pin at `e2e/workout-log.spec.ts:343`. That spec is already in the plan's modify list. Server messages never say "scored".

**Findings**

1. **Non-blocking. Plan, Frame check section: the isolation guards are implicit.**
   - Evidence: `utils/config.py:22` falls back to the real `data/database.db` when `DB_FILE` is unset. The memory note says `HT_RUNTIME_DIR` alone copies the real DB into the scratch runtime. `init_runtime()` (`runtime_init.py:89-100`) runs migration when `DB_FILE` is unset. The plan says the launcher "supplies DB path, isolated runtime root", but not that the runner fails closed.
   - Failure: a stray `DatabaseHandler()` call without a path, or the `--control-ref` export server launched without `DB_FILE`, would use or copy the developer's real DB.
   - Fix: have the runner set `DB_FILE` and `HT_RUNTIME_DIR` explicitly for every child, including the prepare step, the control-export server and the scratch-edit process. Before launch it should assert the resolved DB path sits under `artifacts/workout-log-frame/<unique>/` and differs from `legacy_database_path()`. It should assert the same for the server's DB through a post-start probe. Add a test showing the runner refuses when the DB path resolves to the live DB.

2. **Non-blocking. Plan, Sorting and editing: a sort right after an edit orders by the old value.**
   - Evidence: focusing a header button fires `focusout`, which calls `finish(true)` and starts an async save (`ui-handlers.js:149-151`, `:133-134`). The sort click then reads `.editable-text`, which `updateScoredValue` only updates after the response (`workout-log.js:369-376`).
   - Failure: no stored value is wrong, but the rows end up ordered by the pre-edit value and stay out of order until the next sort.
   - Fix: await the pending write before sorting, or re-run the active sort after the save settles. Add a browser case for "edit then click a header".

3. **Non-blocking. Plan, Sorting and editing: the plan misses the `'--'` sentinel and leaves the "None" display unspecified.**
   - Evidence:
     - The plan's missing-value list is null, empty and `'None'`. Confirmed logged values reach JS as `.editable-text` text, where a cleared value is `'--'` (`ui-handlers.js:99-102`; `workout-log.js:375`).
     - Planned cells print `{{ log.planned_rir }}`, so a NULL becomes the literal "None" (`workout_log.html:130-131`). The new planned line and the Details planned values are not told how to show missing values.
     - Changing "None" to "--" would move blank planned values in sort, because `'None'.localeCompare` sorts after digits and `'--'` before them. Section 0 puts "where blank values land" out of scope.
   - Failure: after clearing logged RPE, a placement helper that doesn't treat `'--'` as missing leaves RPE in the main row. The cards could show "RIR None".
   - Fix: add `'--'` to the missing set for logged values, specify the card and Details wording for a missing planned value, and keep the sort text unchanged.

4. **Non-blocking, test-honesty. Plan, Frame check section: the criterion 9 Exercise-sort oracle cannot fail.**
   - Evidence: `get_workout_logs()` already orders by `routine, exercise` (`utils/workout_log.py:114`), and `sortTableByColumn` has no `sort-asc` class on first click, so it sorts ascending. "Barbell Bench Press first, Cable last" is therefore the initial order before any sort.
   - Failure: a broken Exercise sort still passes.
   - Fix: assert the order after a second click (descending), or after first sorting by another field.

5. **Non-blocking, test-honesty. Plan, Frame check section: the criterion 11 oracle is weak and may not save anything.**
   - Evidence: the fixture already stores Deadlift RIR 0 and weight 120. The submit guard `value !== confirmedScore(cell)` (`ui-handlers.js:117`) skips a save of an unchanged 0. If planned weight is below 120, the badge is Achieved from weight alone, whatever RIR does. I could not read the seed's planned values from the binary seed.
   - Failure: "save RIR 0 and reload" is a no-op, and a regression that treats 0 as missing could still pass.
   - Fix: drive 0 through a real change (set RIR to 2, then to 0), and judge the zero on a row where RIR is the only improving field.

6. **Non-blocking. Plan, Frame, components and layout / Sorting and editing: badge and progression-state hazards when the markup changes.**
   - Evidence: `updateProgressionBadge` rewrites `badge.className` wholesale (`workout-log.js:46`), and `initializeProgressionChecks` runs it for every row on load (`:293-298`). `computeProgressionState` takes the first `[data-field="planned_*"]` and `[data-field="scored_*"] .editable-text` by `textContent`.
   - Failure: any label text added inside those nodes (for example a mobile label or a button name) makes `parseFloat` return NaN. `confirmedScore` would also return label text, so every unchanged edit would count as changed and be written. The load-time badge can silently flip, and the `ui-badge` class would be wiped on load.
   - Fix: add an acceptance assertion that `.editable-text` text equals the bare value, that no second `data-field="planned_*"` exists per row, and that the load-time badge matches `GET /check_progression/<id>` for all seven fixture rows. Name the load-time call as one of the badge sites to change.

7. **Non-blocking. Plan, Layout switching: focus handling is unspecified after save, Escape and re-placement.**
   - Evidence: `finish()` hides the input and shows the text with no focus restore (`ui-handlers.js:121-123`). Placement refresh after an RPE save or clear moves a field between the main row and Details.
   - Failure: a keyboard user loses their place, and may be left on a field that just moved behind a closed Details.
   - Fix: return focus to the field's trigger after commit or cancel. If the field has moved into closed Details, focus the Details button.

8. **Non-blocking. Plan, Frame check fixture: the new record's routine is not stated.**
   - Evidence: Plan v1 gives the name, sets, reps, weight and RIR for the added Cable row but no routine.
   - Failure: with a different routine, `ORDER BY routine, exercise` places the row differently and the sort expectations shift.
   - Fix: pin the routine to `GYM - Full Body - Workout A`, and state that `workout_plan_id` stays NULL. The backfill at `db_initializer.py:279-326` only links on an exact unique match, so a unique name is safe.

## Plan v2

Astra, 2026-11-20. This revision adopts the goal, scope, artifacts and four implementation
steps of Plan v1. The following checks, implementation details and gates supersede the
corresponding v1 instructions. Section 0 remains the signed requirements. All 26 proposed
dispositions are accepted for this revision.

### Acceptance criteria and their checks (TS-1, TS-6)

**Frame** below means the serial, opt-in `e2e/workout-log-frame.check.ts` run against the
seven-record Section 0 fixture. **Log spec** means `e2e/workout-log.spec.ts` in the required
Chromium shard. The frame check owns the full matrix. The Log spec sets up its required
records in the functional lane's scratch DB before opening the page. Follow the existing
#738 case's plan/import and read-back pattern, assert fixture preconditions and identify
records by exercise, routine and ID. A missing record fails the check.

| Criterion | Named check and pass condition |
|---|---|
| 1. Gutter | Frame, **page edges and header offset**. Run C1 at all three base widths, both themes, empty and populated. Also measure navbar bottom to header top, 16 px at 390 and 24 px at 768 and 1440. |
| 2. Radius, type and surfaces | Frame, **component styles**. Run C2–C4 over the full base matrix with Section 0's selectors, computed-style populations and rounding. |
| 3. One primary action | Frame, **Import variant by log state**. In `#main-content` count visible `.ui-btn--primary` and independently count actions with the computed primary fill. Both sets contain only “Import Current Workout Plan” when empty and are empty when populated. Check populated Import's secondary and Clear Log's outline-danger styles in both themes. Pin the state change in the functional empty/import flow too. |
| 4. Phone card content | Frame, **RPE placement by exercise**, at 390 px before any edits. For each of the seven closed cards assert its name, routine, status, planned line and visible Min Reps, Max Reps, Weight and RIR, in order and within the viewport. Squat shows RPE 9 and Seated Military Press shows blank RPE in the main row. For Bench Press, Bent Over Row, Curl, Deadlift and the long Cable row, RPE is hidden on load and appears on opening that card's Details. Count one RPE editor per record across both states. Pin the logged, planned-only and ordinary cases in the Log spec. |
| 5. Phone card size | Frame, **closed card measurements**, C6 at 390 px. Measure the six seed names, full Cable name, field targets and height of every one-line-name card. |
| 6. Details | Log spec, **Details by touch and keyboard**. Check initially collapsed, tap to open, close and reopen by keyboard. Assert the row's six planned values, date, Reference Video, Delete Entry and `aria-expanded`. Verify closed controls leave the tab order. |
| 7. Two-column cards | Frame, **tablet grid**. At 768 px measure two distinct record columns and assert C5. |
| 8. Desktop table | Frame, **desktop column groups**. At 1440 px check Planned and Logged over their six and five fields, cell-to-header IDs, and C7 including each heading's fit and the 220 px Exercise minimum. |
| 9. Sorting follows the field | Frame, **weight then exercise**, at 1440 px with the group row visible. Activate Logged Weight first and assert the five weighted records in order (Curl 30, Bench Press 60, Bent Over Row 70, Squat 100, Deadlift 120). Activate Exercise and assert the complete ascending name list, Bench first and Cable last. Activate it again and require the reverse list. Repeat from a fresh page with keyboard Enter and check `aria-sort` on the active heading. |
| 10. Editing | Log spec, **commit, cancel, clear and reject**, in both layouts. Count POSTs by record and field for changed Enter and blur (one each), Escape and unchanged input (zero). Assert stored null and displayed `--` on clear, the warning and unchanged value on validation or server rejection, and the confirmed value after reload. Exercise a breakpoint crossing with an active editor and an edit followed immediately by sort. |
| 11. Zero and status | Frame, **Deadlift RIR 2 → 0**, after the geometry and sort passes. The committed seed plans 5–8 reps, 120 kg and RIR 2. The frame fixture logs 5/5 reps, 120 kg and blank RPE. Save RIR 2 and verify Pending, then enter 0 and require exactly one successful zero POST for that ID. Read numeric 0 via `/get_workout_logs`, reload and assert visible 0, its Improved mark and Achieved equal to `/check_progression/<id>`. Only RIR can improve in this transition. Retain the #738 Log spec. |
| 12. Phone end to end | Log spec, **leave and reopen the edited exercise**, at 390 px. Find the target by its displayed name among other records and remember its ID. Enter a changed value that moves Pending to Achieved, wait for its successful POST, navigate to Workout Plan and assert that destination loaded. Reopen Workout Log through navigation, find the same name and ID, and compare its displayed value and badge to the stored value and progression response. Run this journey on the seven-record frame fixture as well. |
| 13. Dark theme and contrast | Frame, **shared dark selectors** (C8). The `/workout_log` axe scan in `accessibility.spec.ts` measures both themes against their registered counts, targeting zero in light and retaining zero in dark. Inspect the populated, open-Details and editing states. |
| 14. Overrides | Frame, **retired Log selectors** (C9). Count each Section 0 family after its stated exceptions. Check the total falls below 242 and inspect the CSS diff for any added `!important`. Retain the cascade contracts below. |
| 15. Scale and long names | Frame, **scale-8 readability**, at 390 and 1440 px. Assert scale factor 1.2, C5 and the entire Cable name visible without clipping or ellipsis, including within the desktop scroll region. |
| 16. Other pages | **Platform visual comparisons and bundle inventory**. Compare the complete full-page and thumbnail sets on win32 and Linux. Inspect the changed-file list against the 24 authorized Log PNGs and count the runtime CSS bundles against the signed total of 18. |
| 17. Evidence | **PR evidence review**. Reproduce the documented runner command. Attach or identify the failing pinned control and two independent candidate reports with identical metrics, plus ordinary screenshots at 390 and 1440 px, light/dark, empty/populated, and at scale 8. Include the populated 1360 px table for the owner's by-eye review. |
| 18. The switch | Frame, **C10 at 1359 and 1360**. Assert two card columns and hidden headings at 1359, then visible group/field headings, no heading overflow and Exercise ≥220 px at 1360. Assert C5 at both. Pin both sides of the breakpoint on populated records in the Log spec. |
| 19. First RPE entry | Frame and Log spec, **first RPE without opening Details**. At 390 px require Military Press planned RPE 8, planned RIR null and all five scores null. Check visible RIR and RPE triggers with Details closed, enter 9 once, read that record's stored 9 and reload. RPE 9 and the RIR trigger remain visible with Details closed. |

Run the populated measurements, per-card placement and sort sequence before the first write.
Give each editing scenario its starting values independently. For criterion 12 the unlogged
Cable record can change from Pending to Achieved by entering RIR 1 against planned RIR 2.
After all populated checks, clear only the scratch log and measure the empty state.

### Fixture and control (AR-5–7, PR-1, PR-8, TS-4–5)

- A typed Python launcher creates a fresh directory under `artifacts/workout-log-frame/`.
  Before importing app modules or starting any child, it resolves the expected DB and
  runtime paths, requires both inside that specific run, and refuses the checkout's
  `legacy_database_path()` and paths escaping the run. It explicitly supplies `DB_FILE`
  and `HT_RUNTIME_DIR` to seed preparation, scratch edits, Playwright and both candidate
  and control Flask processes. The seed source is the committed visual fixture. Use the
  explicit scratch path for `DatabaseHandler`, with the existing seeder guard enabled.
- In the test server process, compare effective `utils.config.DB_FILE` and runtime root
  with the launcher's expected paths before `init_runtime()`. Emit the resolved pair to
  the runner and verify it again at readiness before browser writes. Also read the seven
  expected IDs and values over the existing read API. A focused runner pytest passes a
  live-path destination and a path outside the run, and asserts refusal before any
  seeding, DB open or child launch. It can use a stand-in live path in a temporary tree.
- Set the long Cable record's routine to `GYM - Full Body - Workout A` and
  `workout_plan_id` to SQL NULL. Assert the seven names and effort values before measuring.
  For `--control-ref 5dc83cef`, run the archived app and inspect its CSS from the export,
  using the working checkout's absolute venv interpreter and Playwright installation in
  `node_modules`. Check the loaded app originates in the export. The old-UI C1–C4/C10
  failures come from measurements on legacy elements. A failed setup is an error.
- Set explicit `testMatch` for `workout-log-frame.check.ts` in the dedicated config.
  Verify discovery with both configs' `--list`. Use the passed port and `baseURL` for
  origins, and wait for responses or observable DOM state throughout the new TS code.
  Run the inventory generator, its `--check` mode and inventory/runner/URL pytest pins
  after adding the dedicated files and required-shard cases.

### Shared components, sort and focus (AR-1–4, AR-8, PR-2–7)

- Coordinate `layout.css`, `components.css`, `theme-dark.css` and the shared editor in
  `ui-handlers.js` under #736. Remove `table`, `table-striped`, `table-calm`, `tbl` and
  `tbl--responsive` from the Log table. The last is a CSS class. The JS controller binds
  `[data-table-responsive]`, which this table already omits. Replace Bootstrap button,
  field and badge colour classes on migrated controls (`btn`, `btn-*`, `form-control`,
  `bg-success`, `bg-warning`) with their shared components. Keep the Section 0 selector
  hooks, including `.badge.ui-badge`, `.log-play-video-btn`, the input/spinner hooks,
  table ID/classes named under **Hooks that stay**, and the modal's action hooks.
  In `theme-dark.css` remove only the `:where([data-theme="dark"] .workout-log-frame)`
  branch of the grouped glass rule. Record the removal in the ownership map and ledger.
- Replace `initializeSimpleTableSorting` and `sortTableByColumn` with the keyed sorter.
  The group and Actions headers have no sort handler. Before reading confirmed scores,
  await any write started by focus leaving the editor. On rejection sort the restored
  values. In the Log spec hold the update response, activate Logged Weight during the
  pending save, release it and assert the final order reflects the new value and only
  one write occurred. Choose a value that crosses another weighted row.
- Give each planned metric one keyed value per record, and each numeric `.editable-text`
  only its confirmed number or `--`. Keep labels, icons and the mobile summary outside
  the nodes read by the existing progression comparison. Treat null, empty, legacy
  `'None'` and displayed `'--'` as absent for placement, and keep zero present. Omit
  missing effort terms in the planned summary and use `--` for a missing planned value
  in Details. Keep the legacy raw inputs to the sort comparator for missing values.
- Update badge variants at initialization (through `checkProgressiveOverload` and
  `updateProgressionBadge`), after score writes and in the server-response badge updater,
  preserving both base classes. On first load
  check all seven rows' bare values, unique planned keys and badge text against their
  own progression endpoint. After a confirmed RPE save or clear, re-evaluate placement.
  Test Return and Escape restoring focus to the field trigger. If the field moves
  behind closed Details, focus its disclosure. On deliberate Tab, blur or header
  activation, respect the user's new visible focus target. Keep the single-write guard.

### Verification gates (TS-2–3, TS-7–10)

- The shared `ui-handlers.js` edit requires **full pytest and full Chromium** through
  `/verify-suite` within `/verify-and-polish`. Plan v1's targeted list is for quick
  feedback. Include the isolated backup and fatigue-context coverage, the separate
  frame runner, the seeded manual checks, Stylelint, Vitest and inventory checks.
  Run `npx tsc --noEmit` and CI's pyright JSON measurement followed by
  `scripts/pyright_baseline_diff.py` against `docs/ci_cd_phase3/pyright-baseline.json`.
- Retarget the three named cascade tests in their existing slots. The responsive/frame
  test asserts absence of the retired frame padding and responsive table chrome. The
  header/cell glass test asserts absence of header/cell glass, zebra and metric tints.
  The hover test asserts absence of the retired row-hover filters. Keep coverage for
  shared selectors' surviving consumers. In `visual-field-separator.spec.ts` measure
  visible card fields at 375 and 768 px and table fields at 1440 px, preserving 3:1
  and the negative control. Change measured axe counts and X7 together and run
  `tests/test_axe_contracts.py`.
- Hand-edit only the measured changes in `CSS_PHASE4_WP4_4_A_BASELINE.json`, including
  shared-surface line counts, selector groups and pinned declarations. After by-eye
  approval and capture generation, compute the four affected `snapshotManifest` digests
  with the sorted filename/byte-size algorithm in `test_css_wp4_4_a_baseline_contracts.py`.
  Use that contract to verify the ledger. Skip the whole-ledger emitter.
- Keep real `tbody tr` and thumbnail images in both layouts. Check the PR's
  `visual-windows` comparison after the approved Windows PNGs are pushed. Until then
  it compares the new UI to the previous full-page images. Compare Windows thumbnails
  locally and both Linux sets in the final deep-gate compare. Require a clean first
  attempt for `log-desktop-light`, including its existing 800-pixel tolerance.

At plan revision, the existing inventory generator's `--check` passed and all 48 cases
in `tests/test_vitest_inventory_contracts.py` passed. The Deadlift prescription above
was checked directly in the committed read-only visual seed. The acceptance checks
in the table are implementation deliverables after owner Gate 1.

### Gate 1 sign-off

- [x] Gate 0 complete (owner, 2026-11-20).
- [x] Every finding has a proposed disposition.
- [x] Agent provenance complete, with the evidence gap stated.
- [x] Astra recorded Plan v2 for TS-1 and all accepted non-blocking findings.
- [x] The council verifies the fixes (2026-11-20, `c3b3a767`: no blocker; see below).
- [x] Owner approves the plan (Gate 1). Approved by the owner on 2026-11-20, in their words:
  "I approve Gate 1 for the Workout Log pilot on Plan v2 at 05797c95. Astra may begin
  implementation."

---

## Council verification of Plan v2

**Verified** — Plan v2 at `c3b3a767`, on 2026-11-20. The three reviewers ran again in fresh
contexts. Each received the file, the Plan v1 findings at `28c8a151` and
`git diff 28c8a151 c3b3a767`. Each checked whether its own findings were resolved and looked
for new problems. Each received the same owner constraints and blocking rule as the first
round.

| Reviewer | Agent ID | Findings resolved | New findings | Verdict |
|---|---|---|---|---|
| `architecture-reviewer` | `a692721d78418f2d4` | AR-1 to AR-7 resolved, AR-8 partly | 3 non-blocking | Fixes verified, no blocker |
| `test-strategist` | `a89919484d0277285` | TS-1 to TS-10 resolved, with all 19 criteria mapped to checks that can fail | 4 low | Fixes verified, no blocker |
| `product-risk-reviewer` | `a162679b51fd43398` | PR-1 to PR-8 resolved, and the Deadlift 2 → 0 claim confirmed against `build_visual_seed.py:56` | 1 low, 1 info | Fixes verified, no blocker |

These are new agents. The first-round IDs are in the Agent provenance table above. No
first-round agent was resumed, and every verifier read the file cold. The reviewers took no
part in writing the plan.

**Outcome** — No blocking finding is open. Plan v2 is ready for the owner's Gate 1. The new
findings below are all non-blocking. Under the proportionality rule they do not need another
plan round. Astra carries them into the implementation, and the PR review checks them.

### New findings and proposed dispositions

| ID | Finding | Severity | Proposed disposition | Action during implementation |
|---|---|---|---|---|
| V-AR-1 | The server-side check of the database path before `init_runtime()` has no named home | Non-blocking | Accept | Put the check in a runner-owned entry script. Leave `app.py`, `utils/runtime_init.py` and `create_app()` untouched. If `app.py` must change, declare it as a shared-state edit under #736. |
| V-AR-2 | The coordination line names the CSS files and `ui-handlers.js`, but not the other shared files the change edits | Non-blocking (closes AR-8) | Accept | Add the baseline ledger, the visual PNGs, `DESIGN_BRIEF.md` and the test inventory to the coordination line. `ci.yml` does not change, because `e2e/workout-log.spec.ts` is already in its E2E list (`ci.yml:510`). |
| V-AR-3 | "Keep the single-write guard" does not say where the sort's await on a pending save lives. Workout Plan also uses the shared editor | Non-blocking | Accept | Add the await in `workout-log.js` and leave the shared editor's Plan behaviour unchanged. Full Chromium already covers Workout Plan editing. |
| V-TS-1 | After merge, CI does not cover criteria 1, 2, 5, 7–9, 11 and 13–15, because the frame check is opt-in | Low | Accept as a stated limit | Section 0, which the owner signed, keeps the frame check out of CI. Name the limit in the PR. |
| V-TS-2 | Criterion 6's check lists "date" where Section 0 says "Last Progression" | Low (wording) | Accept | They are the same field: `templates/workout_log.html:232` labels the date cell Last Progression. Use the Section 0 name in the spec. |
| V-TS-3 | The new runner pytest and Log spec cases move the test inventory | Low | Accept | Already planned. Commit the regenerated inventory in the same PR. |
| V-TS-4 | The origin pin scans the new config under `e2e/` | Low | Accept | Already planned: take the port and `baseURL` from the environment. |
| V-PR-1 | The Deadlift fixture sentence in criterion 11 does not restate the stored RIR 0 | Low (wording) | Accept | Seed RIR 0 as Section 0 states, so the first-load measurement sees the stored zero. |
| V-PR-2 | The isolation guard names only the checkout's `legacy_database_path()` | Info | No action | The explicit `DB_FILE` and `HT_RUNTIME_DIR` override the archived app's own legacy path. |

### architecture-reviewer, verification (agent `a692721d78418f2d4`)

*Verbatim, except that the reviewer's own headings are demoted to fit this section.*

#### AR-1 to AR-8

| ID | Verdict | Evidence |
|---|---|---|
| AR-1 | Resolved | Plan v2 line 1209-1211 names `tbl--responsive` as a CSS class. It also states that the controller binds `[data-table-responsive]`, which this table omits. Verified: `templates/workout_log.html:66` has `class="table table-striped workout-log-table table-calm tbl tbl--responsive"` and no data attribute. The only controller binding is `static/js/table-responsiveness.js:425`, `qsa('[data-table-responsive]')`. |
| AR-2 | Resolved | Plan v2 line 1218 says to replace `initializeSimpleTableSorting` and `sortTableByColumn`. It also says the group and Actions headers get no handler. Verified: both functions exist only in `static/js/modules/workout-log.js:246` and `:257`, and are called at `:76`. Replacing them there touches no shared surface. |
| AR-3 | Resolved | Plan v2 line 1216-1217 limits the edit to removing `:where([data-theme="dark"] .workout-log-frame)` from the grouped glass rule. It also records the removal in the ownership map and the ledger. Verified: the selector sits in the grouped rule at `static/css/theme-dark.css:85-88`, so removing one list item is a pure removal. |
| AR-4 | Resolved | Plan v2 line 1210-1215 lists the dropped classes: `table`, `table-striped`, `table-calm`, `tbl`, `tbl--responsive`, `btn`, `btn-*`, `form-control`, `bg-success`, `bg-warning`. It also lists the hooks that stay: `.badge.ui-badge`, `.log-play-video-btn` and others. The exact hook list is deferred to "Hooks that stay" in Plan v1 and Section 0. |
| AR-5 | Resolved | Plan v2 line 1196-1199 has the control run from an export, using the working checkout's absolute venv interpreter and `node_modules` Playwright. The control stays at `5dc83cef`, matching Section 0. It also checks that the loaded app originates in the export. |
| AR-6 / PR-1 | Resolved | Plan v2 line 1181-1193 sets `DB_FILE` and `HT_RUNTIME_DIR` explicitly for every child process. The launcher asserts the paths are inside the run and refuses `legacy_database_path()`, which exists at `utils/runtime_paths.py:99`. The server re-checks its effective paths before `init_runtime()`, and there is a refusal pytest. |
| AR-7 | Resolved | Plan v2 line 1200-1204 sets an explicit `testMatch`, checks discovery with `--list` on both configs, and regenerates the inventory with `--check`. It also runs the inventory, runner and URL pytest pins. |
| AR-8 | Partly | Plan v2 line 1208 declares coordination under #736 for `layout.css`, `components.css`, `theme-dark.css` and the shared editor in `ui-handlers.js`. It does not cover the other shared surfaces Plan v2 edits. See finding 1. |

#### New findings

1. **Non-blocking: the test-server path check has no named home.**
   - Plan text: line 1188-1190, "In the test server process, compare effective `utils.config.DB_FILE` and runtime root with the launcher's expected paths before `init_runtime()`."
   - Evidence: `init_runtime()` is called only from entry points, and `app.py` is a declared shared-state file. The check also needs a place to emit the resolved pair to the runner. Plan v2 does not say where this code lives.
   - Failure: the implementer may put it in `app.py` or `utils/runtime_init.py` without the shared-surface declaration. That would add test-only code to a production entry point.
   - Fix: say the check lives in a runner-owned entry script under `scripts/`, and that `app.py`, `utils/runtime_init.py` and `create_app()` are untouched. If `app.py` must change, declare it as a shared-state edit under #736.

2. **Non-blocking: the other shared-state files are not covered.**
   - Plan text: line 1208 lists CSS and `ui-handlers.js` only.
   - Evidence: Plan v2 also edits `CSS_PHASE4_WP4_4_A_BASELINE.json` and the visual PNGs. It also edits the DESIGN_BRIEF (an owner constraint), the inventory files and `ci.yml`'s E2E list via the new required-shard cases. The ci.yml list is pinned `== 25` in a pytest, per memory.
   - Failure: a pinned test goes red late, or a peer session collides on the ledger.
   - Fix: add one line naming these files and stating that the DESIGN_BRIEF update ships in the same change. Also state whether the new Log spec case changes the ci.yml spec-list pin.

3. **Non-blocking: "keep the single-write guard" is ambiguous.**
   - Plan text: line 1237, and the pending-save sort at line 1218-1223.
   - Evidence: the shared editor lives in `ui-handlers.js`, which `workout-plan-table.js` also uses. `workout-log.js` is not the only consumer.
   - Failure: a change that makes the sorter await the editor's write could add Log-specific behaviour to a shared module, and Workout Plan could regress. Full pytest and Chromium are required (line 1241), which mitigates this.
   - Fix: say the await hook is added in `workout-log.js` and the shared editor keeps its Plan behaviour unchanged. Add a Plan-page editing case to the retained coverage.

I found no contradictions with Section 0 beyond what the response matrix already settled. The plan does not touch the schema, `routes/` or API shapes, so the blueprint, schema-registry and response-contract checks do not apply.

**Verdict: fixes verified, no blocker.** AR-1 to AR-7 are resolved. AR-8 is partly resolved and is non-blocking, as is each of the three new findings.

### test-strategist, verification (agent `a89919484d0277285`)

*Verbatim, except that the reviewer's own headings are demoted and one escaped angle-bracket
placeholder is restored.*

#### Verdict

Plan v2 resolves TS-1, the open blocker. No blocking finding, and the fixes are verified. I read the plan and the repo code but did not re-run the inventory `--check` or the 48 contract tests. The author's "passed" claim is unverified by me. I also did not open `tsconfig.json` or `ci.yml`. For tsc coverage I relied on the council's quote of `tsconfig.json:13`.

#### TS-1 to TS-10

| ID | Status | Evidence |
|---|---|---|
| TS-1 | Resolved | All 19 criteria map to a named check (table at lines 1152-1172). Details below. |
| TS-2 | Resolved | Lines 1241-1244 make full pytest plus full Chromium, via `/verify-suite` inside `/verify-and-polish`, the gate for the shared `ui-handlers.js` edit. |
| TS-3 | Resolved | Lines 1245-1246 add `npx tsc --noEmit`, the pyright JSON measurement and `scripts/pyright_baseline_diff.py`. The runner is typed. `tsconfig.json` coverage rests on the council's quote of `tsconfig.json:13`, which I did not open. |
| TS-4 | Resolved | Lines 1201-1204 build URLs from the passed port or `baseURL` and use no `waitForTimeout`. `tests/test_playwright_url_contracts.py:129-144` scans every `.ts` under `e2e/` for a hard-coded origin. `scripts/generate_test_inventory.py:509` scans the same tree for `waitForTimeout`. Both would catch a violation. |
| TS-5 | Resolved | `playwright.config.ts:109` has `testDir: './e2e'` and no `testMatch`, so the default pattern skips `.check.ts`. No `.check.ts` exists yet. Line 1200 adds an explicit `testMatch` and `--list` checks on both configs. The inventory runs `playwright test --list --project=chromium` from the root config (`generate_test_inventory.py:123`), so the frame spec never enters the counts. |
| TS-6 | Resolved | Criteria 18 and 19 each have a Log spec pin (lines 1171-1172). I did not check the Log spec for existing 1359/1360 or first-RPE cases. |
| TS-7 | Resolved | Lines 1255-1259 hand-edit the four digests and skip the emitter. The algorithm (sorted filenames plus byte sizes, sha256) matches `tests/test_css_wp4_4_a_baseline_contracts.py:641-645`. |
| TS-8 | Resolved | Lines 1247-1254 say what each retargeted cascade test asserts. They keep negative assertions, move the axe counts and X7 together, and run `tests/test_axe_contracts.py`. |
| TS-9 | Resolved | Lines 1260-1264 record that `visual-windows` stays red until the win32 PNGs are pushed, and that `log-desktop-light` is a known flipper under its 800-pixel tolerance. |
| TS-10 | Resolved | Line 1252 measures card fields at 375 and 768 px and table fields at 1440 px, and keeps the 3:1 check and the negative control. |

##### TS-1 per criterion

Each of these can fail when the criterion breaks.

- **Criterion 3:** counts `.ui-btn--primary` and, independently, the computed primary fill. A class-only fix would fail the second count.
- **Criterion 4:** asserts per-card content and RPE placement for the seven named records. The Log spec covers the logged, planned-only and ordinary cases.
- **Criterion 12:** the journey leaves the page and compares the reopened card's value and badge against the stored value and `/check_progression/<id>`. It asserts that the Workout Plan page loaded, so it cannot pass by never navigating. It runs on both the Log spec's scratch records and the seven-record frame fixture.
- **Criteria 1, 2, 5, 7-9, 11, 13-15, 18, 19:** each has a Frame check with explicit numeric or order assertions. Criteria 10 and 6 have Log spec checks.
- **Criteria 16 and 17:** these are comparison and review gates, not assertions. The Section 0 wording makes them evidence reviews, so I accept that.

#### New findings

All are non-blocking.

1. **Low. The frame matrix lives only in an opt-in check.**
   - Criteria 1, 2, 5, 7-9, 11 and 13-15 are covered only by `workout-log-frame.check.ts`.
   - Plan text: "serial, opt-in", with the Log spec limited to the criteria it names.
   - Failure: after merge nothing in CI protects them, since CI skips `.check.ts`. The PR's evidence run is the only protection.
   - Fix: none needed if the owner accepts this. Optionally name this limit in the plan.

2. **Low. Criterion 6 text drifted.**
   - Section 0 says the expanded Details show "Last Progression". Plan v2's check (line 1159) lists the six planned values, date, Reference Video and Delete Entry. It never mentions Last Progression.
   - Failure: a Log spec that passes without checking Last Progression.
   - Fix: add Last Progression to the Details assertion, or note that "date" is that field.

3. **Low. New pytest file plus new Log spec cases move the inventory.**
   - Plan text: the "focused runner pytest" (line 1191) and the new Log spec cases.
   - Evidence: the inventory drift check is required and fails on any test add or remove. Line 1203 does say to regenerate the inventory after adding the dedicated files and cases.
   - Failure: only if the regeneration is skipped, which reds `Test Inventory Drift`.
   - Fix: regenerate and commit `TEST_INVENTORY.md` and `TEST_INVENTORY.json` in the same PR. If the sorter or editor gets new Vitest cases, the four pins in `tests/test_vitest_inventory_contracts.py` also need moving.

4. **Low. The new config under `e2e/` is scanned by the origin pin.**
   - Plan text: `e2e/playwright.workout-log-frame.config.ts`.
   - Evidence: `test_no_playwright_source_hardcodes_an_origin` uses `E2E.rglob("*.ts")`, so the config and `.check.ts` are both scanned.
   - Failure: a literal `localhost` or `127.0.0.1` in the config reds that pin.
   - Fix: take `baseURL` and the port from the environment, as line 1202 already says.

#### Files read

- `docs/workout_log_pilot/PLANNING.md`
- `playwright.config.ts`
- `scripts/generate_test_inventory.py`
- `tests/test_playwright_url_contracts.py`
- `tests/test_css_wp4_4_a_baseline_contracts.py`
- `e2e/workout-log.spec.ts`

### product-risk-reviewer, verification (agent `a162679b51fd43398`)

*Verbatim, except that the reviewer's own headings are demoted and escaped angle brackets
are restored.*

I read Plan v2 with Plan v1 and Section 0. I checked its claims against `e2e/scripts/build_visual_seed.py`, `utils/workout_log.py`, `static/js/modules/workout-log.js`, `utils/config.py`, `utils/runtime_paths.py`, `utils/runtime_init.py` and `utils/runtime_migration.py`. I could not read the binary `database.visual.seed.db`. The seed builder script is the authority for its plan rows. No files were edited.

#### PR-1 to PR-8

| # | Verdict | Evidence |
|---|---|---|
| PR-1 (explicit DB isolation) | Resolved | v2 (line 1181) resolves the expected DB and runtime paths before any app import and requires both inside the run. It refuses `legacy_database_path()` and escaping paths, and passes `DB_FILE` and `HT_RUNTIME_DIR` to every child. It rechecks in the server before `init_runtime()` and again at readiness. A runner pytest asserts refusal before any seed, DB open or child launch. In the code, `runtime_migration.py:240-242` makes an env `DB_FILE` win outright and never migrates into it. `runtime_init.py:51-55` takes `DB_FILE` from the env too, so setting both variables avoids the copy-the-real-DB hazard. In a checkout `runtime_database_path()` equals the legacy path, so refusing the legacy path also covers the live DB. |
| PR-2 (sort right after an edit) | Resolved | v2 (line 1219-1223) awaits any write started by focus leaving the editor before reading confirmed scores. On rejection it sorts the restored values. It adds a held-response case that crosses another weighted row and asserts one write. Criterion 10 adds "edit followed immediately by sort". |
| PR-3 (`'--'` sentinel and missing planned value) | Resolved | v2 (line 1226) treats null, empty, legacy `'None'` and displayed `'--'` as absent for placement, and keeps 0 present. It omits missing effort terms in the planned summary and uses `--` in Details. It keeps the legacy raw inputs for the sort comparator. This is consistent with `computeProgressionState` (`workout-log.js:28-39`): `parseFloat('--')` is NaN, so it is not finite and returns false. |
| PR-4 (criterion 9 oracle cannot fail) | Resolved | The check now sorts by Weight first, so Exercise ascending is no longer the server's default order. The server returns `ORDER BY routine, exercise` (`workout_log.py:114`). It also requires the descending list on a second activation, and repeats from a fresh page by keyboard with an `aria-sort` check. Criterion 9's signed wording is unchanged. |
| PR-5 (criterion 11 may save nothing) | Resolved | Section 0's fixture stores Deadlift RIR 0 (line 261). v2 saves RIR 2 first, then 0, and requires exactly one successful zero POST. It reads numeric 0 through `/get_workout_logs` and compares the post-reload badge to `/check_progression/<id>`. See the seed check below. |
| PR-6 (label text in value nodes, badge rewrite sites) | Resolved | v2 (line 1224-1236) keeps `.editable-text` to the bare value or `--`. It gives each record one keyed planned value and checks all seven rows' badge against the progression endpoint on first load. It names the three `className` rewrite sites, which match `workout-log.js:46` (`updateProgressionBadge`), `:349` (server-response updater) and `:599` (`checkProgressiveOverload`). It preserves both base classes. No e2e, pytest or Vitest pin asserts `bg-success` or `bg-warning` on the Log badge. The only hits are toast and goal-badge pins. |
| PR-7 (focus handling) | Resolved | Return and Escape restore focus to the field trigger. If the field has moved behind closed Details, focus goes to the disclosure. A deliberate Tab, blur or header activation keeps the user's new target. The single-write guard is retained. |
| PR-8 (Cable record's routine) | Resolved | v2 pins `GYM - Full Body - Workout A` with `workout_plan_id` NULL. `get_workout_logs()` reads only `workout_log` with a LEFT JOIN to exercises, so a NULL plan id still lists. The order Bench, Row, Curl, Deadlift, Military Press, Squat, Cable matches "Bench first, Cable last". |

**Deadlift seed check.** `build_visual_seed.py:56` plans Barbell Deadlift as 3 sets, 5 to 8 reps, RIR 2, 120 kg. Only the first three plan rows are logged, so the Deadlift log row is unlogged in the base seed. Section 0 edits it to logged 5/5, 120, RIR 0.

With 5/5/120 and RIR 2:
- RIR is not below the plan (2 < 2 is false).
- Min reps 5 is not above 5, and max reps 5 is not above 8.
- Weight 120 is not above 120.
- RPE is blank.

The server-side check returns false, so the badge reads Pending. It matches `computeProgressionState`. With RIR 0, `0 < 2` is true on the server and `parseFloat('0')` is finite in the JS, so both give Achieved. Only RIR can improve, as v2 states. The v2 claim holds.

#### New findings

1. **Low (wording only): the frame fixture's Deadlift RIR is not restated.**
   - Plan text: criterion 11 says "The frame fixture logs 5/5 reps, 120 kg and blank RPE" and then "Save RIR 2".
   - Evidence: Section 0 (line 261) and Plan v1 (line 759) specify stored RIR 0 for the Deadlift fixture. This is not a contradiction.
   - Failure: an implementer could seed RIR as NULL. The 2 → 0 sequence still works. But the first-load Improved mark and Achieved badge at the pre-edit measurement would differ from the other plan text that assumes a stored zero.
   - Fix: add "stored RIR 0" to the criterion 11 fixture sentence.

2. **Info, no action: the isolation guard names only the checkout's `legacy_database_path()`.**
   - Evidence: in the `--control-ref` archived app, `installation_root()` is the export directory, so that app's legacy path differs.
   - Failure: none. The explicit `DB_FILE` and `HT_RUNTIME_DIR` override it, and the 5dc83cef export contains `runtime_paths.py` (runtime-paths work predates it).

I found no new calculation, local-first, terminology or workflow-migration risk:
- The plan changes no calculation. It reads the existing progression comparison and the `/check_progression` endpoint only.
- There is no auth, cloud or telemetry.
- Copy ("Import Current Workout Plan", Achieved/Pending, Details) matches Section 0.
- There is no schema or API-shape change. The only seed edits are in the scratch copy.
- Zero RIR is preserved, matching #738.
- Effective sets are not touched.

#### Verdict

**Fixes verified, no blocker.** PR-1 to PR-8 are all resolved. Finding 1 is a wording tidy, not a blocker.

---

## Evidence — fix round, 2026-11-25

Implementer's record for the round after the pilot review at `19f3302e`. The edits were
uncommitted when these commands ran. Gate 2 is not approved here.

**Changed paths**

- `templates/workout_log.html` — `.workout-log-frame` now wraps the empty-state panel and the
  table's scroll region, so the frame is visible in both states and only the region is hidden on
  an empty log. The legend gains "Compared with the plan:". An unset Last Progression shows
  "Set Date".
- `static/js/modules/workout-log.js` — the card order is name, routine, status. The sort waits
  with `Promise.allSettled`. Deleting the last record hides the region, not the frame.
- `static/css/pages-workout-log.css` — the routine caption and status sit under the name beside
  the thumbnail. Both span the card's second row, and the caption keeps 80 px clear on the right
  for the badge, so a long caption wraps beside it. Every 12 px role has a 16 px line, with 4 px
  under each field label. Logged RPE takes its full label behind Details. Spinner chrome left
  this file.
- `static/css/components.css`, `static/css/tokens.css` — `--ui-field-surface` (`--surface-2`
  light, `--surface-0` dark) for `.ui-field` and `.ui-field-input`, the empty-state title's
  24 px line height, and the spinner chrome.
- `docs/product/APP_FLOW.md`, `docs/product/DESIGN_BRIEF.md`,
  `docs/CSS_PHASE4_WP4_4_A_BASELINE.json`, `scripts/css_audit/j_known_live_mutation.mjs`.

**Commands and results**

| Command | Result |
|---|---|
| `npx playwright test e2e/workout-log.spec.ts e2e/visual-field-separator.spec.ts e2e/accessibility.spec.ts --project=chromium --reporter=line` | 110 passed |
| `npx playwright test e2e/smoke-navigation.spec.ts e2e/empty-states.spec.ts --project=chromium --reporter=line` | 35 passed |
| `.venv/Scripts/python.exe e2e/scripts/run_workout_log_frame.py`, twice | Both passed. The two `metrics.json` files are byte-identical (`candidate-6qmna1y4`, `candidate-z9xx9yjq`) |
| The same with `--control-ref 5dc83cef` | Passed (`control-0wohnl_h`) |
| `pytest tests/ -q -n 8 --dist loadfile -k "css or visual or axe or landmark or workout_log or template or inventory or playwright or console"` | 757 passed, 1 skipped, 1 failed |
| `npx stylelint static/css/pages-workout-log.css` | 0 errors, 18 warnings, the same count as before the round |
| `node scripts/css_audit/stylelint_surfaces.mjs <out.json>` | 2652 warnings, identical by rule and by file to the `25b009ba` output |
| `npx tsc --noEmit`, `npx vitest run` | No errors; 271 passed |

Every row is from the final state of the edits. At 390 px a closed card with a one-line name
measures 239 px (limit 250). The Exercise column is 255 px at 1360 px and 335 px at 1440 px
(limit 220).

**Long routine caption.** Measured on a throwaway frame-run database
(`artifacts/workout-log-frame/routine-probe-gn_rswls`, seeded and guarded by the frame runner)
with three records renamed to `GYM - Upper Lower Hypertrophy Split - Workout B Heavy`. The
browser had a 15 px scrollbar, so the layouts were 375 and 753 px wide. On four-field and
five-field cards, in one column and in two, the caption took two lines beside the badge. The
gap to the badge was at least 10 px and the page did not scroll sideways. The badge is 69.5 px
wide for Achieved and 63 px for Pending. The routine names were restored afterwards.

**Baseline ledger.** `workoutLogPilot.surfaces` in `docs/CSS_PHASE4_WP4_4_A_BASELINE.json`,
re-measured by hand as newline count and LF-normalized bytes: `pages-workout-log.css` 176 lines
and 7673 bytes, `tokens.css` 509 and 15081, `components.css` 5091 and 164622.

**Known red.** `tests/test_css_theme_dark_p3_audit_contracts.py::test_this_packet_wrote_no_production_css`
asserts that `git status --porcelain -- static/css` is empty, so it fails while the CSS edits
are uncommitted. It was not rerun on a committed tree in this round.

**Migration notes.** Presentation only: no calculation, route, schema or response shape
changed. Markup that other code may select on moved in three places.

- `role="region"`, its `aria-label` and `tabindex="0"` moved from `.workout-log-frame` to a
  child `div`. `.workout-log-frame` is no longer hidden on an empty log.
- The Last Progression cell carries `data-sort-value` with the displayed date, or an empty
  string. The sorter read the same two strings from the button's text before, so the order
  is unchanged.
- The unset date button's accessible name now ends with ", Set Date". Its visible text must
  appear in the name (axe `label-content-name-mismatch`).

**Coverage not added.** Tests were outside this round's edit scope. No test asserts the
"Compared with the plan:", "Set Date" or behind-Details "Logged RPE" text.

### Second round, 2026-11-25

Implementer's record for the by-eye findings B1, B2 and B5 and the frame assertions added at
`1b712de0`. The edits were uncommitted when these commands ran. The ledger numbers here
replace the ones above.

**Changed paths**

- `static/css/pages-workout-log.css` — field labels wrap, and each field shares a label row
  and a field row with its neighbours through `subgrid`, so the field boxes stay on one line.
  A field column is never narrower than its value with its mark. Labels are weight 500. A
  comparison mark is `--ink-2` unless it is Improved or Below Target. The date input fills its
  cell: the date column is 122 px and the status column 86 px. A cell with an open numeric
  editor drops its block padding, so a table row stays 56 px.
- `static/css/components.css` — a field below 1360 px is 16 / 24 px.
- `static/css/tokens.css`, `static/css/layout.css` — `--ui-title-line` (28 px, 32 px from
  768 px) sets the page title's line height.
- `templates/workout_log.html` — the date input carries `ui-field-input`.
- `static/js/modules/workout-log.js` — after a date saves, focus returns to the date button
  unless the user has already moved it.
- `docs/CSS_PHASE4_WP4_4_A_BASELINE.json`.

**Commands and results**

| Command | Result |
|---|---|
| `.venv/Scripts/python.exe e2e/scripts/run_workout_log_frame.py`, twice | Both passed. The two `metrics.json` files are byte-identical (`candidate-9wu2g5u_`, `candidate-u3gswng7`) |
| The same with `--control-ref 5dc83cef` | Passed (`control-5nsd25em`) |
| `npx playwright test e2e/workout-log.spec.ts e2e/empty-states.spec.ts e2e/smoke-navigation.spec.ts e2e/visual-field-separator.spec.ts e2e/accessibility.spec.ts --project=chromium --reporter=line` | 145 passed |
| `pytest tests/ -q -n 8 --dist loadfile -k "css or visual or axe or landmark or workout_log or template or inventory or playwright or console"` | 757 passed, 1 skipped, 1 failed (the uncommitted-CSS test named above) |
| `npx stylelint static/css/pages-workout-log.css` | 0 errors, 18 warnings, the same count as before the round |
| `npx tsc --noEmit`, `npx vitest run` | No errors; 271 passed |

**Measurements**, in CSS px, on a throwaway frame-run database
(`artifacts/workout-log-frame/layout-probe-qjznf225`). The Squat card has five fields and the
widest value, `100.0`.

| Layout | Squat label lines | Smallest label gap on any card | Squat field widths | Squat card height |
|---|---|---|---|---|
| 390 px, scale 6 | all one line | 8.2 | 60.4, 60.4, 78.5, 54.4, 54.4 | 239 |
| 390 px, scale 8 (325 px) | Min Reps and Max Reps on two | 9.8 | 45.6, 45.6, 64.2, 44, 44 | 265.5 |
| 360 px, scale 6 | Max Reps on two | 5.6 | 54.5, 54.5, 70.9, 49.1, 49 | 255 |
| 320 px, scale 6 | Min Reps and Max Reps on two | 8.5 | 44, 44, 64.5, 44, 44 | 266 |

- Every field is 44 px tall and the fields of a card sit on one row in all four layouts.
- At scale 8 the Squat weight field holds its mark, a 2 px gap and `100.0` with nothing to
  spare. At 320 px its field row runs 2.5 px into the card's 16 px right padding.
- The page title is 20 / 28 px below 768 px and 24 / 32 px from 768 px.
- At 1440 and 1360 px the open date input is 114 px in a 122 px cell, 4 px inside it on the
  left and right and 8 px clear of the status badge. A row is 56 px with the date editor or a
  numeric editor open. The Exercise column is 245.8 px at 1360 px and 325.8 px at 1440 px,
  and no heading is clipped.

**Baseline ledger.** `workoutLogPilot.surfaces`, re-measured by hand: `pages-workout-log.css`
194 lines and 8774 bytes, `tokens.css` 510 and 15129, `components.css` 5091 and 164658,
`layout.css` 1862 and 50119.

**Migration notes.** Presentation only. The date input gains the `ui-field-input` class, and
the card's field layout now needs `subgrid` (Chromium 117, Firefox 71, Safari 16).

### Third round — narrow five-field cards, 2026-11-26

Implementer's record for the owner's finding on `54e6ab2c`: a card with five logged fields did
not fit a 320 or 360 px phone at scale 8. The edits were uncommitted when these commands ran.
The `pages-workout-log.css` ledger numbers here replace the ones above.

**Changed paths**

- `static/css/pages-workout-log.css` — a card marked `data-field-rows="2"` wraps its logged
  fields onto two rows. Five fields wrap three and two: Min Reps, Max Reps and Weight, then RIR
  and RPE. Four fields wrap two and two. Each row keeps the shared label row and field row, so
  the open editor still sits under the row it belongs to. Below 1360 px a logged field's
  minimum width is 44 px as rendered: above scale 6 the layout minimum is 44 px divided by the
  scale factor plus 0.5 px (37.2 px at scale 8). It is unchanged at scale 6 and below.
- `static/js/modules/workout-log.js` — `fitRecordFields` measures every card on one row and
  sets or clears `data-field-rows`. It runs at load, when the fonts are ready, when the card
  list changes width, when the layout crosses 1360 px and after a logged value saves.
- `docs/product/APP_FLOW.md`, `docs/CSS_PHASE4_WP4_4_A_BASELINE.json`.

**Why a script decides.** Whether five fields fit depends on their values. At 390 px at
scale 8 the owner's values fit one row and `100`, `100`, `1000.0`, `10`, `10.0` do not. A grid
takes its column count from the template, never from its content. `flex-wrap` does wrap by
content, but its lines share neither columns nor the label and field rows that the open
editor relies on. The card already takes its cell order from the same script.

**Measurements**, in px as rendered, on a throwaway frame-run database
(`artifacts/workout-log-frame/narrow-probe-rndxmnho`). The owner's Barbell Squat record: planned
RIR 2 and RPE 8 at 100 kg, logged `10`, `10`, `100.0`, `1`, `10.0`, a mark in every field.

| Viewport, scale | Rows | Field widths | Field height | Rightmost field to the content edge, to the card edge | Card height | Page `scrollWidth` / `clientWidth` |
|---|---|---|---|---|---|---|
| 320 px, scale 8 | 2 | 67.3, 67.3, 87.5, then 67.3, 67.3 | 52.8 | 0, 20.2 | 455.4 | 320 / 320 |
| 360 px, scale 8 | 2 | 79.4, 79.4, 103.3, then 79.4, 79.4 | 52.8 | 0, 20.2 | 417 | 360 / 360 |
| 390 px, scale 8 | 1 | 51.9, 51.9, 77, 46.7, 64.6 | 52.8 | 0, 20.2 | 342.6 | 390 / 390 |
| 320 px, scale 6 | 2 | 72.1, 72.1, 93.8, then 72.1, 72.1 | 44 | 0, 17 | 348 | 320 / 320 |
| 360 px, scale 6 | 1 | 53.3, 53.3, 69.3, 48, 54.2 | 44 | 0, 17 | 275 | 360 / 360 |
| 390 px, scale 6 | 1 | 60.4, 60.4, 78.5, 54.4, 54.4 | 44 | 0, 17 | 239 | 390 / 390 |

- On this head the same record left its card by 57.7 px at 320 px and 17.7 px at 360 px at
  scale 8, the page was 359 px wide in a 320 px viewport, and at 390 px the row ran 7.9 px
  into the card's right padding.
- With `100`, `100`, `1000.0`, `10`, `10.0` the card has two rows at 320, 360, 390 and 768 px
  at scale 8 and at 320 px at scale 6, and one row at 360, 390 and 768 px at scale 6.
- An all-blank five-field card has two rows at 320 px at scale 8 and one row everywhere else.
- A four-field card stays on one row with the fixture's values at every width. With `100`,
  `100`, `1000.0`, `10` it wraps two and two at 320 and 360 px at scale 8.
- The probe read 112 cards: both value sets at 320, 360, 390 and 768 px at scales 6 and 8. No
  field left its card or its padding, no value was clipped, no mark touched its value, every
  field was at least 44 × 44 and no page scrolled sideways.
- At scale 6, at 360, 375, 390, 768, 1024, 1359, 1360 and 1440 px, with Details closed, with
  Details open and with an editor open, every box inside `#main-content` is where it was on
  this head: 0 differences to 0.01 px over 22 states. A closed one-line card at 390 px is
  239 px with four fields and with five.
- The frame check's `metrics.json` differs from the one measured on this head in 2 of 22
  entries, both 390 px at scale 8: two five-field cards have RIR and RPE fields 51 to 51.5 px
  wide where they were 53.

**Commands and results**

| Command | Result |
|---|---|
| `npx playwright test e2e/workout-log.spec.ts e2e/empty-states.spec.ts e2e/smoke-navigation.spec.ts e2e/visual-field-separator.spec.ts e2e/accessibility.spec.ts --project=chromium --reporter=line` | 146 passed |
| `.venv/Scripts/python.exe e2e/scripts/run_workout_log_frame.py`, ten runs on the final edits | 2 passed (`candidate-dp_up5ng`, `candidate-jocfc6a_`). 8 failed on one assertion, described below. All ten `metrics.json` files are byte-identical |
| The same with `--control-ref 5dc83cef` | Passed (`control-eux75vgm`) |
| `pytest tests/ -q -n 8 --dist loadfile -k "css or visual or axe or landmark or workout_log or template or inventory or playwright or console"` | 757 passed, 1 skipped, 1 failed (the uncommitted-CSS test named in the first round) |
| `npx stylelint static/css/pages-workout-log.css` | 0 errors, 18 warnings, the same count as before the round |
| `npx tsc --noEmit`, `npx vitest run` | No errors; 271 passed |
| `PW_VISUAL_SEED=1 npx playwright test e2e/visual.spec.ts e2e/visual-baseline-thumbnails.spec.ts -g "workout-log\|workout_log thumbnails"` | 7 failed, 5 did not run. The committed win32 Log baselines date from `5dc83cef`, before the pilot: `workout-log-mobile-light` expects 375 × 6159 and the page is 375 × 1770 |

**A race in the frame check, fixed in `dbe81bb6`.** The eight failing runs fail only
`logged RPE and RIR share one row` (`e2e/workout-log-frame.check.ts:295`, reached from `:703`
straight after `page.reload()` at `:700`). The helper reads the RPE box and the RIR box in two
calls while the reloaded page is still scrolling to its restored position. The check was run
three times against the application source at `54e6ab2c` with no edits
(`head-z15446qz`, `head-0svxic9h`, `head-irzyjkjx`) and failed the same assertion in two of
them. A replay of the helper's own steps over 40 reloads read the two boxes at different
heights 13 times on these edits and 18 times on the committed assets. In the twelve
mismatches printed, both boxes had settled at the same height 400 ms later. The implementer
did not edit the check. The test author then confirmed the cause over 44 probed reloads: the
two tops were equal in every animation frame, and the old read mismatched only while the page
was scrolling back to its saved position. `dbe81bb6` reads both tops in one pass, in the frame
check and in `e2e/workout-log.spec.ts`, with the 1 px tolerance unchanged. Five consecutive
frame-check runs then passed with byte-identical `metrics.json`, and the `5dc83cef` control
still passed.

**Baseline ledger.** `workoutLogPilot.surfaces`, re-measured by hand: `pages-workout-log.css`
205 lines and 9510 bytes. The other surfaces are unchanged.

**Migration notes.** Presentation only: no calculation, route, schema or response shape
changed. `tr.ui-record-card` gains the attribute `data-field-rows="2"` while its fields are
wrapped, and loses it when they fit one row or the table is shown. The script holds the card
list's height with an inline `min-height` while it measures, then clears it.

**Coverage.** `e2e/workout-log.spec.ts` (`phone card fits five logged fields at 320, 360 and
390 px at scale 8`) and the frame check's `expectNarrowPhoneCardsFit` cover the fit at scale 8.
`dbe81bb6` adds four checks to the same spec, all at scale 8: the refit after a saved value
(360 px), the refit after a resize from 390 to 320 px and back without a reload, the editor
inside a wrapped card (320 px) and a wrapped four-field card (320 px). No automated check
covers the refit after a live scale change. The implementer exercised it with a probe script
on the throwaway database and found it working.

**Left as it is**

- After a live resize or scale change the cards are refitted on the next frame, so one frame
  can show the previous wrapping. The test author sampled it: two frames at 320 px showed the
  old one-row layout before the refit.
- On every load the page script reorders and fits the cards just after first paint (first
  paint at 40 to 76 ms, the script at 71 to 118 ms). The reorder dates from `604663ad`. At
  320 px at scale 8 the test author's card with the owner's values shows two or three frames
  on one row, 9 to 24 px past the card, before it wraps and grows from 388 to 513 px.
- For about 150 ms after an inline editor opens it sits over the Details button below it (up
  to 50 px at scale 8, 42 px at scale 6), because `.editable` in `components.css` animates the
  row it reserves. This predates the round and also happens on one-row cards. The settled
  state is clean.
- At 320 px at scale 8 a five-field card logged `1000`, `1000`, `1000.0` wraps, and its first
  row runs 11.1 px into the right padding, 9.1 px inside the card's box. Nothing is clipped
  and the page does not scroll. It fits at 360 px and wider.
- Below scale 6 a logged field renders under 44 px: 33 px tall at level 1. This round did
  not change it.
