# Plan Review — Workout Log pilot (#736 step 2)

**Status** — Gate 0 signed by the owner on 2026-11-20, with both corrections in Section 0
(check C10 and criteria 18 and 19). Astra's Plan v1 is ready for council review. The owner
decides Gate 1 after that review.

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

Plan v1 author is Astra (Codex), assigned directly by the owner for step 2. A Claude
`product-manager` agent ID does not apply to this draft. The council records its three
reviewer IDs and actual author continuity when it reviews the plan. Review and Gate 1
are pending.
