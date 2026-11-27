# App Flow

*What each screen is for, what the user can do on it, and what actually happens — including
when it fails.*

**Derived from:** the source tree at revision `d1efc93` — every rendered template and its loaded
JavaScript dependency graph, every frontend network call site, every route handler, and a live
HTTP probe of the running application. Plan routine-cascade behavior was re-verified at revision
`538919a`. **On conflict, the code wins.**

Two rules governed how this document was written, and they are worth stating because they
changed several conclusions:

- **Behavior comes from the handler, never from the markup.** Template copy is marketing; a
  docstring is a comment. Where a docstring and a function body disagreed, the body won, and the
  disagreement is recorded.
- **Tests are gap-detection evidence, not the oracle.** The E2E suite was used to check that
  documented flows exist, never to define what the product is.

---

## The page-load model

Every page extends `templates/base.html`, which loads eight global CSS bundles and a fixed set of
scripts. The central one is `static/js/app.js`: an ES module that statically imports a **34-file
graph** on every page — not code-split, not lazy — and then dispatches by path:

```js
const pageInitializers = {
  '/workout_plan': …, '/workout_log': …, '/weekly_summary': …,
  '/session_summary': …, '/progression': …, '/volume_splitter': …, '/backup': …
};
```

Three consequences that shape everything below:

1. **`app.js` is a shared bundle, but the JS cost is not identical per page.** Six templates load
   an additional page module on top of it, and 18 of the 51 files in `static/js/modules/` are not
   reachable from `app.js` at all:

   | Page | Extra module | Files it adds |
   |---|---|---|
   | `/user_profile` | `user-profile.js` | 8 |
   | `/session_summary` | `session-summary.js` | 3 |
   | `/weekly_summary` | `weekly-summary.js` | 2 |
   | `/workout_plan` | `workout-plan-page.js` + `muscle-selector.js` | 2 |
   | `/fatigue` | `fatigue-heatmap.js` | 2 |
   | `/body_composition` | `body-composition.js` | 1 |
   | `/` | `welcome.js` | 1 |

   `base.html` separately loads `filter-view-mode.js` and `modal-focus-trap.js` as classic
   scripts — outside the module graph, so they add one file each on every page.

2. **Membership in `pageInitializers` is not the same as having page JavaScript.** `/weekly_summary`,
   `/session_summary`, and `/workout_plan` appear in the map *and* load their own module; the
   live render path for the two summaries is the page module, not `app.js`. Conversely
   `/user_profile`, `/body_composition`, and `/fatigue` are absent from the map and load a module
   anyway. Only four pages run on `app.js` alone — `/workout_log`, `/progression`,
   `/volume_splitter`, and `/backup` — and all four reach it through the map.

`app.js` also assigns 20 functions onto `window` so inline `onclick=` attributes in templates can
reach them. That is why several controls below have no listener registration you can grep for —
the binding is the `onclick` attribute itself.

## Third-party assets — all served locally

**The application loads every asset from its own origin.** The server has no outbound calls, and
nothing is loaded from a CDN, a font service, or any other third party. The one network use is the
optional, click-initiated exercise reference video described at the end of this section.

Third-party code is vendored under `static/vendor/`, each directory carrying its upstream license,
a `NOTICE.md`, and a `VERSION` file recording the exact source it was taken from:

| Asset | Version | Vendored at | Loaded by |
|---|---|---|---|
| Inter web font + `@font-face` CSS | Google Fonts v20 | `static/vendor/inter/` | `templates/base.html` — every page |
| Bootstrap JavaScript bundle | 5.3.9 | `static/vendor/bootstrap/` | `templates/base.html` — every page |
| Font Awesome | 5.15.4 | `static/vendor/fontawesome/` | `templates/base.html` — every page |
| Sortable | 1.14.0 | `static/vendor/sortable/` | `templates/workout_plan.html` |
| flatpickr | 4.6.13 | `static/vendor/flatpickr/` | `templates/progression_plan.html` |
| Popper | 2.11.8 | `static/vendor/popperjs/` | `templates/volume_splitter.html` |
| Tippy | 6.3.7 | `static/vendor/tippy/` | `templates/volume_splitter.html` |

The Inter stylesheet references `woff2` files by relative path under the same vendor directory, so
the font resolves offline too.

**Offline, every page renders exactly as it does online**, with its typography and every
interaction intact — drag-to-reorder on the plan, the date picker on progression, tooltips on the
splitter. The only feature that degrades is the reference video below.

The only external URLs written into the templates are two author links to LinkedIn, in the navbar
and on Home. Both are ordinary links the user must click; neither is fetched on page load.

**Exercise reference videos need the network.** `static/js/modules/exercise-video-modal.js`
builds YouTube URLs when the user clicks an exercise's video control on the Plan or Log page. A
curated video ID sets the shared modal's iframe to `https://www.youtube.com/embed/<id>` and its
external link to `https://www.youtube.com/watch?v=<id>`; an exercise without a valid ID opens
`https://www.youtube.com/results?search_query=…` in a new tab. Nothing is requested before the
click. Offline, the embedded player or search tab cannot load; the rest of the page is unaffected.

## Route surface

79 rules are registered. Removing Flask's `static` endpoint leaves **78 application rules** over
74 distinct URL paths — some paths carry several methods — which split into **11 page routes**
that render HTML and **67 routes** that return JSON or a file.

Exactly one of those 78 is registered **directly on the app rather than on a blueprint**:
`POST /erase-data` in `app.py`. That matters when enumerating the surface, because the test
harness builds a blueprint-only application, so a taxonomy derived from it would silently omit
the one route that destroys all data.

### Blueprint classification

Every registered blueprint, classified as a product surface or as supporting infrastructure,
with the reason.

| Blueprint | Classification | Reason |
|---|---|---|
| `main` | **Product surface** — Home | Renders `/`, the landing and orientation screen |
| `workout_plan` | **Product surface** — Plan | Renders `/workout_plan`; owns plan CRUD, supersets, generation, replacement, estimates |
| `workout_log` | **Product surface** — Log | Renders `/workout_log`; owns logging and progression checks |
| `weekly_summary` | **Product surface** — Analyze | Renders `/weekly_summary`; owns pattern coverage |
| `session_summary` | **Product surface** — Analyze | Renders `/session_summary` |
| `fatigue` | **Product surface** — Fatigue | Renders `/fatigue`, a first-class navbar destination |
| `progression_plan` | **Product surface** — Progress | Renders `/progression`; owns goals and suggestions |
| `volume_splitter` | **Product surface** — Distribute | Renders `/volume_splitter`; owns volume plans |
| `user_profile` | **Product surface** — Profile | Renders `/user_profile`; owns profile, lifts, preferences, calibration, fatigue settings |
| `body_composition` | **Product surface** — Body Composition | Renders `/body_composition`, a first-class navbar destination |
| `program_backup` | **Product surface** — Backup | Renders `/backup`, the Backup Center |
| `filters` | **Supporting infrastructure** | Renders no page. Two endpoints serving the Plan page's exercise filtering |
| `exports` | **Supporting infrastructure** | Renders no page. Four file-producing endpoints called from Plan and the summaries |

Eleven blueprints are product surfaces; two are infrastructure. Every one of the eleven is
reachable from the navbar.

## Response contract

Every JSON route returns the same envelope, verified live against the running application for
14 GET endpoints and 9 deliberate failure paths — including the 404 handler.

```jsonc
// success — HTTP 200
{ "ok": true,  "status": "success", "data": …, "message": "…", "requestId": "…" }
// failure
{ "ok": false, "status": "error",   "message": "…",
  "error": { "code": "…", "message": "…", "requestId": "…" } }
```

Codes observed in practice: `VALIDATION_ERROR` (400), `NOT_FOUND` (404), `INTERNAL_ERROR` (500),
`EXPORT_FAILED` (500), `PLAN_NOT_FOUND` (404), plus the three replace-exercise codes below. The
contract itself is owned by [`../../.claude/rules/routes.md`](../../.claude/rules/routes.md).

### Three outcomes, not two

A control has **three** possible ends, and collapsing them to success/failure gets this
application wrong:

| Outcome | Shape | Presented as |
|---|---|---|
| Success | HTTP 200, `ok: true` | Result applied, success toast |
| **No result** | **HTTP 200, `ok: false`, with `error.reason`** | **Warning** — the request was understood and processed; there was simply nothing to do |
| Failure | HTTP 4xx/5xx, `ok: false` | Error toast |

The middle row is real and deliberate. `POST /replace_exercise` returns `NO_CANDIDATES`,
`SELECTION_FAILED`, and `DUPLICATE` with `status_code=200` (`utils/exercise_replacement.py`), and
`static/js/modules/workout-plan-replacement.js` branches on `error.reason` — **not on the HTTP
status and not on `error.code`**. Anything keyed on status alone would report those three as
successes.

**Severity does not track HTTP status here, in either direction.** The reason-to-toast map in
`workout-plan-helpers.js` is what actually decides:

| `error.reason` | HTTP | Toast |
|---|---|---|
| `no_candidates` | 200 | warning |
| `duplicate` | 200 | warning |
| `selection_failed` | 200 | **error** — it has no case and falls through to the default |
| `missing_metadata` | **400** | **warning** |
| `not_found` | 404 | error |

So one 200 outcome is presented as an error and one 400 is presented as a warning. Do not infer
either direction from the status code.

## Action types

Not every control calls the server. Each control below is classified as one of:

- **API** — issues an HTTP request
- **Navigation** — changes location
- **Local state** — writes `localStorage` or a cookie; no request
- **Download** — produces a file the browser saves
- **Presentation** — pure client-side display: modal, tab, sort, collapse, filter of already-loaded data

---

## Global navigation — `templates/base.html`

Present on every page.

| Control | Action type | Behavior |
|---|---|---|
| Brand / logo | Navigation | → `/` |
| **Plan**, **Log** | Navigation | → `/workout_plan`, `/workout_log` |
| **Analyze** ▾ | Presentation | Bootstrap dropdown containing **Weekly**, **Session**, **Fatigue** |
| **Progress** | Navigation | → `/progression` |
| **Profile**, **Body Composition** | Navigation | → `/user_profile`, `/body_composition` |
| **Distribute** | Navigation | → `/volume_splitter` |
| **Backup** | Navigation | → `/backup` |
| Menu toggle (hamburger, up to 1359.98px) | Presentation | Opens a full-height panel below the header holding **Plan**, **Log**, **Analyze**, **Progress**, **Profile**, **Body Composition**, **Distribute**, **Backup** and the right-hand controls. Closes on the toggle, Escape or a click on empty panel space, and focus returns to the toggle. Widening to 1360px or wider closes it and releases scroll lock and focus trap |
| Author link | Navigation | External, `target="_blank" rel="noopener noreferrer"` |
| Scale − / + | Local state | Changes application scale and writes `ui-scale-level` to **localStorage and a cookie** (1–8). On the server, `inject_scale_level()` in `app.py` maps the value to a zoom factor. Out-of-range and non-numeric values fall back to level `6` (zoom `1`). Ctrl/Cmd `+`, `-` and `0` still control browser zoom. The application-scale control is available in browsers that support CSS `zoom`, subject to the existing responsive visibility. Browsers without CSS `zoom` support hide the control and its trailing divider. Firefox validation covers version 160.0.1, tested on 2026-11-18 |
| Muscle naming toggle (`#muscleModeToggle`) | Local state | Writes `hypertrophy_filter_view_mode` to `localStorage` and dispatches a `filterViewModeChanged` event. The toggle itself sends **no request**. Button label reads **Simple** or **Scientific**; the stored values are `'simple'` and `'advanced'`. What it changes: [Muscle naming mode](#muscle-naming-mode) |
| Dark mode toggle (`#darkModeToggle`) | Local state | Writes `darkMode` (`'true'`/`'false'`) to `localStorage` and sets `data-theme` on `<html>`. With nothing stored it follows `prefers-color-scheme` and keeps following it until the user chooses |
| Skip to main content | Presentation | Focuses `#main-content` |

### Muscle naming mode

The navbar muscle-naming button is the control for one browser-wide setting. It is stored only as
`hypertrophy_filter_view_mode` in `localStorage` (`'simple'` when unset), so it survives reloads and
applies on every page; the server stores nothing. Below the `lg` breakpoint the button shows only
its icon. **Simple** uses everyday groupings (Biceps, Glutes, Quads); **Scientific** uses anatomical
names (Long Head Bicep, Gluteus Maximus, Rectus Femoris). Changing it updates every surface
below in place. The toggle itself sends no request, but two surfaces react with one — the Plan
filter when a selected value is translated, and the two summary pages — as their rows say:

| Surface | What changes |
|---|---|
| Plan filter dropdowns — Primary, Secondary, Tertiary, Advanced Isolated Muscles | Options are rebuilt in the new naming. A current selection is translated where a counterpart exists; a simple group with no one-to-one scientific option is kept as a temporary "… (Group)" option; otherwise the dropdown resets to All. When the translation changes the filter value, the filter re-runs |
| Plan table muscle columns | Cell text is re-derived from each cell's stored raw value, with no refetch. In Scientific mode a Primary cell shows the matching isolated muscles when the row has any |
| Plan table **Simple / Advanced** button | A second control for the same setting, created in the table's own controls row. It flips the same stored value, so the two buttons stay in step. In Simple mode the Tertiary Muscle, Utility, Movement Pattern, Movement Subpattern, Stabilizers and Synergists columns are hidden by CSS; Scientific shows them |
| Weekly Summary and Session Summary | The page refetches its summary (`GET /weekly_summary` or `GET /session_summary`) and re-renders the muscle-group rows in the new naming. The server-rendered isolated-muscle cells are relabelled in place from their stored raw value |
| Excel export | The value is sent as `view_mode` on `GET /export_to_excel`. `advanced` renames the Workout Plan columns (for example `Primary Muscle` becomes `Primary Muscle Group`) and swaps muscle names for the scientific ones; any other value is treated as `simple`. Both modes append `Time Cap (sec)`, `EMOM Interval (sec)` and `EMOM Rounds` after `Exercise Order` (columns V–X), preserving columns A–U. Timing values are exported as stored, with empty cells for missing values |

**Server-side filter expansion.** `POST /filter_exercises` accepts either naming and expands it in
`routes/filters.py`. A simple key becomes every database value it covers, matched with OR —
`glutes` covers `Gluteus Maximus` and `Hip-Adductors` for the primary filter, and `biceps` covers
`long-head-bicep` and `short-head-bicep` for the isolated filter. A scientific key on a
primary/secondary/tertiary filter resolves through its simple parent. A simple key with no
scientific breakdown (`traps-middle`, `lower-back`, `lats`, `upper-back`) is **ignored** on the
isolated filter — it does not narrow the result, and it does not return nothing.

---

## Home — `/`

**Purpose.** Landing and orientation. Explains the workflow and links into it. Almost entirely
navigation — and one destructive control that exists nowhere else.

| Control | Action type | Behavior |
|---|---|---|
| 15 workflow links | Navigation | → Plan, Log, Weekly Summary, Progression, Volume Splitter, Backup |
| **Erase All Data** (`#eraseDataBtn`) | Presentation → API | Opens a confirmation modal; confirming issues `POST /erase-data` |

`app.js` defensively removes any `#eraseDataBtn` or `.erase-data-btn` found on a page without
`.welcome-container`, so this control cannot leak onto another screen.

### The erase contract

`POST /erase-data` requires `{"confirm": "ERASE_ALL_DATA"}` in the body. Without it, HTTP 400
`VALIDATION_ERROR` — verified live. With it, the handler:

1. writes a pre-erase snapshot to `data/auto_backup/`;
2. drops the 16 tables in `OWNED_TABLES_DROP_ORDER`;
3. reinitializes the schema.

**This destroys the Backup Center library.** `program_backups` and `program_backup_items` are
the first two entries in the drop list. See
[`BACKEND_SCHEMA.md`](BACKEND_SCHEMA.md#what-an-erase-actually-destroys).

The pre-erase snapshot is a raw SQLite file copy. There is **no in-application path to restore
it** — recovery means replacing the database file by hand. Home's own copy, "Auto-backup before
data reset ensures you never lose progress," is optimistic about that. The success response carries
`data.auto_backup` — `{"filename": "database_<timestamp>.db"}`, or `null` when no snapshot was
taken (see [Startup snapshot](#startup-snapshot)) — and the Home page shows it as an informational
banner naming the file.

The exercise catalog is not dropped and is not lost.

---

## Plan — `/workout_plan`

**Purpose.** Build and edit routines. The workout plan list sits above the Add exercise panel.
On the first load of a populated plan, the first routine in environment, program and workout
order is selected. Choose All to see every exercise, or choose a routine tab to see its rows.
Each tab shows its exercise count. An empty plan offers Generate Starter Plan and Add first
exercise, which moves focus to the environment field.

**Initialization.** `initializeWorkoutPlan()` wires filters, the routine cascade, plan handlers,
the volume panel, and the controls animation. It deliberately does **not** call
`handleRoutineSelection()` separately; doing so once left two live listeners on the hidden
`#routine` field and produced a duplicate `/get_all_exercises` fetch per navigation.

### Selecting what to add

| Control | Action type | Endpoint / behavior |
|---|---|---|
| Filters (muscle, equipment, difficulty, …) | Presentation → API | The filter section starts collapsed. Changes apply through `POST /filter_exercises` and update the exercise match count. Active filters are shown as removable chips even while the section is closed. Removing a chip clears that filter and refreshes the options. The server validates filter column names and returns `VALIDATION_ERROR` 400 for an unknown column |
| Exercise search | Presentation | The search field inside the exercise picker narrows already-loaded options client-side |
| Clear filters | Presentation → API | Clears the filters and chips, resets the routine cascade and reloads the catalog via `GET /get_all_exercises` |
| Routine cascade — environment → program → day | Presentation → API | Three dependent `<select>`s compose the hidden `#routine` value. Completing the cascade with a real day synchronously clears transient superset checkbox, row-highlight, and action-bar state, then — **only when no filter dropdown holds a value** — issues `GET /get_routine_exercises/<routine>`; with active filters it re-applies them via `POST /filter_exercises` instead. Empty intermediate values — including Clear Filters and the stateless page reset — do not clear that selection. The reset never unlinks a persisted superset or changes the plan rows on display. **The endpoint ignores the routine and returns the full catalog** — deliberately: the dropdown it feeds is an *add* control, so every exercise must stay offered no matter which routine already uses it |
| Exercise `<select>` | API | On change, `GET /get_exercise_info/<name>` for metadata; `GET /api/user_profile/estimate?exercise=…` for the suggested numbers |
| Weight / sets / RIR / RPE / min-rep / max-rep | Presentation | Local inputs. Sets and both rep fields retain their typed values through submission so validation can catch invalid counts |
| Estimate trace toggle | Presentation | Expands the derivation behind the suggested numbers |
| **Add Exercise** | API | `POST /add_exercise`. Valid values append a row and refresh the table. If the active routine tab hides the new row, the success toast names the routine it was added to. A rejected submission shows the validation message and leaves the plan unchanged |

`GET /get_exercise_info/<name>` for an unknown exercise returns HTTP 404 `NOT_FOUND` — verified
live.

### Working with the plan list

Exercise cards appear in one column below 768 px and two columns from 768 px. Each card shows
the routine, exercise and prescription. Swap and video are available on the card and Details
reveals the editable numbers, execution style, superset selection and Remove action. From
1360 px the same rows appear in a table that scrolls horizontally inside the list panel.

| Control | Action type | Endpoint / behavior |
|---|---|---|
| Table load / refresh | API | `GET /get_workout_plan` returns every plan row with its exercise metadata. Called on load and after any mutation |
| Inline field edit | API | `POST /update_exercise` with `{id, updates}`. Weight is limited to 0–1000 kg and RIR to 0–10. A validation failure returns HTTP 400 `VALIDATION_ERROR`, keeps the last saved value visible and leaves all submitted fields unchanged |
| Drag to reorder | API | Drag by the handle in either layout. A linked partner moves alongside the dragged exercise. `POST /update_exercise_order` saves the order as an atomic batch. Invalid entries return `VALIDATION_ERROR` 400. The list reloads the saved order after validation or write failures |
| Remove row | API | `POST /remove_exercise`. A non-numeric id is `VALIDATION_ERROR` 400 — verified live |
| Replace exercise | API | `POST /replace_exercise` — **see the three-outcome table above** |
| Link superset | API | Select two exercises in the list, then choose Link as Superset. `POST /api/superset/link` requires exactly two ids. The linked exercises each show the same neutral Superset badge and side rail |
| Unlink superset | API | `POST /api/superset/unlink` |
| Execution style | API | `GET /api/execution_style_options`, then `POST /api/execution_style` |
| Video / image preview | Presentation | Curated videos open in a modal. The video button opens a YouTube search in a new tab when the exercise lacks a valid video ID. Thumbnails show a preview on hover or focus. The plan table is built client-side, so its media path is validated in JavaScript by `resolveExerciseMediaSrc()` — a mirror of the server-side shape rules in `utils/media_path.py`. The video itself loads from YouTube and needs internet ([third-party assets](#third-party-assets--all-served-locally)) |
| Routine tabs | Presentation | Filters displayed rows |
| Volume targets | Presentation → API | Opens the right-hand drawer. The page loads `GET /api/volume_progress` on initialization and refreshes after changes that affect volume. Use the close button, Escape or the backdrop to dismiss it. The open state is stored locally |

Plan sets and rep bounds must be whole numbers of at least 1, within SQLite's integer range.
Inline edits apply these bounds to the submitted count fields. Minimum reps must be at most
maximum reps when both are usable. An inline edit can repair either field when the stored
companion is invalid. The two rep bounds can also be repaired together in one request.
A blank inline count edit reverts to the saved value without sending a write. After a
successful save the cell shows the stored number, so `08` displays as `8`.

### Plan-level actions

Export to Workout Log is in the page header. More opens the menu for Export All Tables,
Backup Center, Generate Starter Plan and Clear Plan.

| Control | Action type | Endpoint / behavior |
|---|---|---|
| **Generate Starter Plan** | Presentation → API | Modal collects days, environment, experience, goal, volume scale, movement restrictions, equipment whitelist, and up to two priority muscles; submits `POST /generate_starter_plan`. Every dropdown's options are **hardcoded in the template** — `GET /get_generator_options` exists but nothing calls it. Selecting zero equipment is blocked client-side with a warning toast before any request; more than two priority muscles is trimmed to two with a warning |
| Export to Workout Log | API → Navigation | `POST /export_to_workout_log` validates the full plan before adding log rows or skipping duplicates. Invalid sets or reps return HTTP 400 `VALIDATION_ERROR` with the affected routine, exercise and reason, and no row is imported until that plan row is corrected inline. After a successful import, the browser navigates to `/workout_log` after ~1.5 s |
| Export All Tables | Download | `GET /export_to_excel?view_mode=…`, response read as a blob and saved via a temporary `<a download>`. The `view_mode` value is read from `localStorage`. If the isolated-muscle statistics read fails, full export returns HTTP 500 with `EXPORT_FAILED`. The Workout Plan shows an error toast and the download does not start. A successful read with no mappings permits a workbook without the Isolated Muscles sheet |
| Backup Center | Navigation | → `/backup?intent=browse` |
| Clear Plan | Presentation → API | Modal, then `POST /clear_workout_plan` |

Unexpected Add Exercise storage failures return HTTP 500 / `INTERNAL_ERROR` with
`Failed to add exercise`; expected input problems retain their specific validation
messages. If starter-plan storage fails, generation still returns HTTP 200 and its
generated data with `persisted: false` and `persist_error: "Failed to save generated plan"`.

---

## Log — `/workout_log`

**Purpose.** Record what was actually performed against what was planned. Each row carries both
the `planned_*` snapshot and the `scored_*` values.

Below 1360 px each exercise appears as a card. Two cards fit per row from 768 px.
Each card shows its planned prescription and editable logged reps, weight and RIR.
A logged RPE or an RPE-only prescription adds RPE to the main row. A card too narrow
for its logged fields on one row wraps them onto two. Details opens the
remaining values, Last Progression, Reference Video and Delete Entry. On desktop,
the Planned and Logged groups have individually sortable field headings. Number
columns sort as numbers, so zero and decimals take their numeric place, and Last
Progression sorts by its saved date, including a date just saved in the row. An
empty date and a missing or cleared number sort last in both directions.

| Control | Action type | Endpoint / behavior |
|---|---|---|
| Import from Plan | API | `POST /export_to_workout_log`, same endpoint the Plan page uses |
| Logged weight / min reps / max reps / RIR / RPE | API | `POST /update_workout_log` with `{id, updates: {field: value}}` per field. Enter or leaving the editor saves a changed value once. Escape discards the draft, including spinner changes. Clearing a saved score sends `null` |
| Progression date | API | `POST /update_progression_date` |
| Progression status check | API | `GET /check_progression/<log_id>` |
| Delete row | API | `POST /delete_workout_log` |
| Clear Log | Presentation → API | Modal, then `POST /clear_workout_log` |
| Reference video / thumbnail | Presentation | A curated video opens the shared video modal. The video button opens a YouTube search in a new tab when the exercise lacks a valid video ID. This page is server-rendered, so its media path is revalidated at render by the `safe_media_path` Jinja filter — the only template in the application that uses it. The video itself loads from YouTube and needs internet ([third-party assets](#third-party-assets--all-served-locally)) |

Logged reps accept whole numbers of at least 0 within SQLite's integer range. The minimum cannot
exceed a usable maximum. A saved value displays as the stored number, so a zero displays as `0`,
including after reload, and its progression indicator is shown. A clear displays as `--`. Invalid drafts show a warning and keep the last saved value visible. If the server
rejects a scored edit, it returns HTTP 400 `VALIDATION_ERROR` and leaves the row unchanged.

Neither `GET /export_workout_log` nor `GET /get_workout_logs` has any control bound to it in the
current templates — the page's rows are server-rendered, so the log page never needs to fetch
them. Both are listed in *Known discrepancies* below.

| Read | Healthy result | Read failure |
|---|---|---|
| `GET /workout_log` | HTTP 200 with the normal table, including zero rows when the log is empty | HTTP 500 with “Unable to load workout log.” Browser navigation shows the shared error page. JSON and XHR requests receive `INTERNAL_ERROR`. This describes the current page load, including when navigation follows a successful import. |
| `GET /export_workout_log` | An XLSX attachment when rows exist, or HTTP 404 with JSON `NOT_FOUND` when the log is empty | HTTP 500 with JSON `INTERNAL_ERROR` and no attachment |
| `GET /get_workout_logs` | HTTP 200 with the log list in the JSON success envelope's `data` field, including `[]` when empty | HTTP 500 with JSON `INTERNAL_ERROR` |

---

## Weekly Summary — `/weekly_summary`

**Purpose.** Volume per muscle across the whole program, with effective and raw counts side by
side, a per-muscle volume classification, and movement-pattern coverage.

**This page describes the plan, not the log — and there is no date window.** The query joins
`user_selection` to `exercises` and never touches `workout_log`. `calculate_weekly_summary()`
takes no date argument. The page's own `<title>` says **"Plan Volume Summary"**, which is the
accurate name.

Three specifics that are easy to state wrong:

- **"Frequency" is not sessions performed.** It counts how many distinct routines give that
  muscle at least 1.0 effective sets.
- **The `method` query parameter is accepted and ignored.** It is retained so older callers do
  not raise; it changes nothing.
- **The volume-class badge always derives from effective sets**, even when the displayed number
  is raw. A second legacy classifier computed from the displayed number is emitted alongside it
  under a different key.

### Modes

| Control | Action type | Behavior |
|---|---|---|
| Muscle Contribution Mode `<select>` | API | Re-requests `GET /weekly_summary?contribution_mode=total\|direct` with JSON headers. `TOTAL` credits primary 100%, secondary 50%, tertiary 25%; `DIRECT_ONLY` credits primary only. A failed isolated-muscle read returns HTTP 500 with `INTERNAL_ERROR` and the table shows “Failed to load data.” |
| Export to Excel | Download | `GET /export_to_excel` — the **workout plan** export, not a summary export |
| Pattern coverage panel | API | `GET /api/pattern_coverage` |
| **Projected fatigue badge** | Presentation + Navigation | Server-rendered on every request. Shows a band label and an info tooltip; its "View per-muscle breakdown" link navigates to `/fatigue` |
| Collapsible explanation | Presentation | `<details>` block |

**`counting_mode` has no UI control.** It is a query parameter (`raw` / `effective`, default
`effective`); the page renders both counts side by side instead of switching between them.
Unrecognized values for either mode fall back to the default rather than erroring.

If the isolated-muscle statistics read fails on initial navigation, the page returns HTTP 500
and shows the shared error page. A successful read with no matches leaves the page available
and hides the isolated-muscle panel.

### How the two numbers relate

Effective sets are computed in **two stages**, and collapsing them into one formula is the most
common way to get this wrong:

1. **Per row**: `effective = raw_sets × effort_factor × rep_range_factor`. No muscle weighting yet.
2. **Per muscle**: that value `× the muscle's contribution weight` (1.0 / 0.5 / 0.25).

`CountingMode.RAW` sets the effort and rep-range factors to 1.0 — **and nothing else.** The
muscle-contribution weighting still applies. So in `TOTAL` mode a 3-set bench press contributes
**1.5 raw sets** to Triceps. That is correct behavior, not a rounding bug.

Two threshold details worth knowing before reading a boundary: the session-volume bands are
lower-inclusive and upper-exclusive, so exactly 10.0 classifies as borderline despite a docstring
saying "≤10 OK"; and the rep-range factor keys off the *average* of min and max, so a 5–8 range is
read as 6.5 rather than as two endpoints.

Those rep-range bands are **total** — every positive average lands in one, with no gap
(`DECISIONS.md` ADR-009 ruling 2): under 6 → 85%, 6–20 → 100%, over 20 up to 30 → 85%, over 30 →
70%. A rep range that is not set, or whose average is zero or negative, stays neutral at 100%.
*(Superseded wording, kept because it described real behavior until 2026-08-30: "an average landing
between buckets matches none of them and falls through to 1.0." That fall-through was the defect
ADR-009 removed — an average of 30.5 scored 1.0, above both its neighbours.)*

> Effective sets, the volume class, and the coverage warnings are **informational**. Nothing here
> adjusts a plan value, blocks an input, or gates a control.

---

## Session Summary — `/session_summary`

**Purpose.** The same volume picture, grouped by routine, with an optional date window and
per-session averages.

| Control | Action type | Behavior |
|---|---|---|
| Routine filter | API | `GET /session_summary?routine=…` with JSON headers |
| Start / end date | API | Same endpoint, `start_date` / `end_date` |
| Muscle Contribution Mode | API | Same endpoint, `contribution_mode`. A failed isolated-muscle read during this refresh returns HTTP 500 with `INTERNAL_ERROR` and the table shows “Failed to load data.” |
| **Projected fatigue badge** | Presentation + Navigation | Same always-on server-rendered badge as Weekly Summary; links to `/fatigue` |
| Export to Excel | Download | `GET /export_to_excel` |

If the isolated-muscle statistics read fails on initial navigation, the page returns HTTP 500
and shows the shared error page. A successful read with no matches leaves the page available
and hides the isolated-muscle panel.

**What the date window actually filters.** Volume comes from `user_selection` — the plan. Session
counts come from `workout_log`. The date range filters **only the log side**. So narrowing the
range changes the per-session denominator and the warning level; it never changes the volume
totals. With nothing logged in the window, `sets_per_session` is `null` and the warning level is
`no_data` rather than zero.

The same two-stage effective-set arithmetic and the same informational-only rule apply.

---

## Fatigue — `/fatigue`

**Purpose.** A per-muscle fatigue readout over a selectable period — a body heatmap above a
detailed bar list. **This page makes no API calls at all.** Everything is server-rendered, and the
one module it loads reads its data from a `<script type="application/json">` block the server
embeds rather than fetching anything.

| Control | Action type | Behavior |
|---|---|---|
| Period `<select>` | Navigation | Auto-submits its form on change — `GET /fatigue?period=…`, a real navigation and full page reload. There is no Apply button; a submit button exists only inside `<noscript>`, labelled "Update" |
| Body map panel | Presentation | A `<details>` element, open by default. Collapsing it is browser-native; no state is persisted |
| Planned / Logged channel buttons | Presentation | Recolor the figures from the already-rendered data. Each button renders `hidden` and is revealed only if that channel actually has data — measured on a planned-only page, `Planned` is visible and pressed while `Logged` stays hidden, so no dead toggle is ever shown |
| Body map figures | Presentation | Two SVGs, front and back, colored by each muscle's existing fatigue band. Regions with no reading stay gray |
| Legend | Presentation | Band swatches with text labels |
| Link to Plan | Navigation | → `/workout_plan` |

### The body map is a second view of the same numbers

It introduces no metric. The colors come from the same `muscle_rows` the bar list below renders,
so the map and the list can never disagree.

Three details that would otherwise read as bugs, all stated in the page's own copy:

- **Three muscles have no region of their own.** Front-Shoulder and Rear-Shoulder are represented
  by the Middle-Shoulder region; Middle-Traps is represented by the upper-back region, which the
  taxonomy routes to Traps. All three still get their own bar in the list below.
- **Unread regions stay gray**, and the caveat explaining that sits *above* the figures, because
  the per-region detail is hover-only and a touch user never sees it.
- **The panel is progressive enhancement.** With JavaScript off the figures never mount and a note
  stands in for them; the bar list is the primary view and is unaffected. On a page with no
  planned or logged data the panel is not rendered at all.

### What the numbers are, and are not

- **Fatigue uses raw sets.** `CountingMode` is deliberately not consulted, so the fatigue figure
  never changes when a summary page's mode changes. Fatigue and effective sets are **separate
  pipelines** that happen to share the muscle-contribution weights.
- **The headline percentage column is an index, not a volume percentage.** It is
  `100 × fatigue_score / MRV_landmark` (`percent_of_mrv` internally; the page labels it
  "% of typical recoverable range" and never says MRV to the user). The score accumulates
  `per-set fatigue × sets × role weight`; the landmark is a weekly **set count**. Those are not
  the same unit — read the column as "score relative to this muscle's recoverable-volume
  landmark", never as "percentage of your weekly volume".
- **Twelve muscles have landmarks.** Front-Shoulder, Rear-Shoulder, Lower Back, Hip-Adductors,
  Middle-Traps, Neck, and the `Unassigned` sentinel have none, and render `—` with a neutral band.
- **There is no decay.** Phase 1 "weekly" means *the set of routines passed in*, not a rolling
  time-decayed window — the plan source has no date column, so date bucketing is the caller's job
  and the aggregate is a plain sum.
- **A logged row whose `scored_*` fields are all NULL contributes zero.** With `this_session`
  selected and nothing logged, the window is empty rather than an error.
- **Stimulus-to-fatigue ratio renders `—` when fatigue is zero**, rather than infinity.
- **The bands are literature-anchored defaults.** They were reviewed once against felt labels and
  no threshold was changed. They are not calibrated to this user, and they are not a target.

### Two different fatigue surfaces — do not conflate them

| Surface | Where | Gated? |
|---|---|---|
| **Projected fatigue badge** | Weekly Summary and Session Summary | **No.** Always rendered; the route computes the score and band on every request with no settings check |
| **Fatigue context block** | Progression estimates and suggestions | **Yes.** Controlled from Profile by `fatigue_context_settings.enabled`, which is **off by default** |

Only the second is the opt-in one. Both are independent of `CountingMode` and `ContributionMode`.

The badge's own tooltip states the constraints plainly: it reads planned routines rather than
logged sets, and it ignores the Counting Mode toggle.

> Everything on this page is descriptive. It does not gate, warn-and-block, or adjust anything.

---

## Progression — `/progression`

**Purpose.** Double-progression guidance per exercise, and user-created goals.

| Control | Action type | Endpoint / behavior |
|---|---|---|
| Exercise `<select>` | API | `POST /get_exercise_suggestions` |
| Current value lookup | API | `POST /get_current_value` with `{exercise, goal_type}` |
| Goal form (type, current, target, date) | API | `POST /save_progression_goal`. An empty body is `VALIDATION_ERROR` 400 — verified live |
| Date field | Presentation | flatpickr picker, vendored locally |
| Complete goal | API | `POST /complete_progression_goal/<id>` |
| Delete goal | Presentation → API | Modal, then `DELETE /delete_progression_goal/<id>` |
| Current Goals table | Presentation | Cards at 576px and below; above that, all seven columns with their headers. From 576.02px to 1200px the table scrolls inside its focusable, labelled region, and the "Scroll sideways" hint is shown and announced only while the region actually overflows (#716) |

### What the suggestion is, and is not

- **The page returns a list, not a decision.** A technique note and three manual options are
  appended on every call regardless of status. The double-progression verdict is one card among
  them.
- **There are three statuses**: `increase_weight`, `increase_reps`, `maintain`. `reduce_weight`
  is not a status — it appears as a *suggestion* inside the `increase_reps` branch when the
  lifter has been below the minimum twice consecutively and the weight exceeds 5.
- **Missing effort data counts as acceptable effort.** With both RIR and RPE absent, the effort
  check returns true, so a weight increase can be suggested from rep data alone.
- **The increment is flat.** +2.5 kg for novices, +5.0 kg otherwise, at every load — the current
  weight is passed in and not used. The unit "kg" is hardcoded in the copy.
- **Nothing is written back to the plan.** Every write on this page lands in `progression_goals` —
  insert on save, update on complete, delete on delete — and all three are explicit user actions.
  `user_selection` is never touched, so acting on a suggestion means editing the plan yourself.

---

## Volume Splitter — `/volume_splitter`

**Purpose.** Distribute weekly sets per muscle across a chosen number of training days, then save
and optionally activate the result.

| Control | Action type | Endpoint / behavior |
|---|---|---|
| Training days `<select>` | Presentation | Local input |
| Basic / advanced grouping radio | Presentation | Selects the muscle grouping used by the calculation |
| Calculate | API | `POST /api/calculate_volume` with `{mode, training_days, volumes, ranges}` |
| Reset | Presentation | Clears the local form |
| Save & Activate | API | `POST /api/save_volume_plan` |
| Saved-plan list | API | `GET /api/volume_history`; `GET /api/volume_plan/<id>` to load one |
| Activate / deactivate | API | `POST /api/volume_plan/<id>/activate` or `/deactivate`. A missing plan is `PLAN_NOT_FOUND` 404 |
| Delete plan | Presentation → API | Modal, then `DELETE /api/volume_plan/<id>` |
| Export volume | Download | `POST /api/export_volume_excel`, saved as a blob on success. Malformed root/volume shapes and nonfinite or boolean volume values return HTTP 400 `VALIDATION_ERROR`. Parsed falsy roots retain header-only exports; malformed or empty JSON bodies remain 400 `BAD_REQUEST`, and unsupported content types remain 415. On an HTTP failure the UI shows one generic error toast and creates no download; unexpected builder failures are logged and return a safe 500 |
| Export to Excel | Download | `GET /export_to_excel` — the plan export |
| Active-plan summary | Presentation | Expands the current active plan |
| Tooltips | Presentation | Popper and Tippy, vendored locally |

Only one plan can be active at a time, and that is enforced by the **database**: a partial unique
index over `is_active WHERE is_active = 1`.

### The "AI Suggestions" panel

The page renders a heading reading **AI Suggestions**. There is no AI involved. The panel is a
local rule-based heuristic in `utils/volume_ai.py` with hardcoded thresholds — it warns when
total volume exceeds `training_days × 30`, warns when a muscle exceeds 10 sets per session, and
suggests consolidating below 3. There is no model, no inference, and no network call of any kind.

The heading is documented here as it ships. Renaming it would be a code change and is not
proposed by this document.

> These suggestions are informational. They do not change the split or block saving.

---

## Profile — `/user_profile`

**Purpose.** Reference lifts, demographics, and rep preferences that feed the Plan page's
suggested numbers; plus the learned-calibration and fatigue-context settings. The most
form-dense screen — around 38 declared controls across five forms.

| Form / control | Action type | Endpoint / behavior |
|---|---|---|
| Demographics (gender, age, height, weight, experience) | API | `POST /api/user_profile`, autosaved. An unrecognized gender is `VALIDATION_ERROR` 400 with the message `gender must be one of M, F` — verified live |
| Reference lifts | API | `POST /api/user_profile/lifts` with a `lifts` array. Weight and reps are individually nullable, so a lift can be listed but unfilled |
| Rep-range preferences | API | `POST /api/user_profile/preferences`. Tier ∈ complex / accessory / isolated; range ∈ heavy / moderate / light — enforced by a database `CHECK` as well as by the route |
| Calibration mode | API | `GET`/`POST /api/user_profile/calibration_settings`. Mode is `off` or `suggest` — there is no "apply" mode |
| Calibration dashboard | API | `GET /api/user_profile/calibration/dashboard` |
| Promote a learned calibration | API | `POST /api/user_profile/calibration/promote` → `NOT_PROMOTABLE` or `REFERENCE_LIFT_EXISTS` (both 400) when it cannot be applied |
| Reset one exercise | API | `POST /api/user_profile/calibration/reset` |
| Reset all learned calibration | API | `POST /api/user_profile/calibration/reset_all` |
| Ignore a transfer | API | `POST /api/user_profile/calibration/ignore_transfer` |
| Un-ignore a transfer | API | `POST /api/user_profile/calibration/unignore_transfer` |
| Clear all ignored transfers | API | `POST /api/user_profile/calibration/clear_ignored_transfers` |
| Fatigue context settings | API | `GET`/`POST /api/user_profile/fatigue_context_settings`. Source ∈ planned / logged / both; period ∈ this_session / this_week / last_4_weeks. **Disabled by default** |
| Coverage body map | Presentation | SVG rendered from a `<script type="application/json" data-bodymap-state>` block the server embeds; the SVG asset itself is fetched by JavaScript at runtime |
| Link to Plan | Navigation | → `/workout_plan` |

Learned calibration is **opt-in and advisory**. Its own on-page copy states it "never changes
your suggested weight, reps, or sets"; the only way a learned value becomes a reference lift is
the explicit Promote action.

---

## Body Composition — `/body_composition`

**Purpose.** Record measurements and track body-fat estimates over time.

| Control | Action type | Endpoint / behavior |
|---|---|---|
| Neck / waist / hip / notes | Presentation | Local inputs. Height, weight, age, and gender come from Profile |
| Save snapshot | API | `POST /api/body_composition/snapshot` → `VALIDATION_ERROR` 400 on invalid input |
| History list | API | `GET /api/body_composition/snapshots` |
| Delete snapshot | API | `DELETE /api/body_composition/snapshots/<id>` → `NOT_FOUND` 404 for an unknown id |
| Method explainer | Presentation | `<details>` block |
| Link to Profile | Navigation | → `/user_profile` |

Two estimates are stored per snapshot. The BMI-based figure is always present; the Navy-formula
figure requires the circumference measurements and is null without them — which is exactly what
the column nullability encodes.

---

## Backup Center — `/backup`

**Purpose.** Snapshot and restore the workout program.

| Control | Action type | Endpoint / behavior |
|---|---|---|
| Name + note, Save | API | `POST /api/backups`. A blank name is blocked client-side with a warning toast, and independently by the route as `VALIDATION_ERROR` 400. Saving with an empty plan warns once before proceeding. The name is trimmed, required and at most 100 characters; the note is optional, trimmed and at most 500 (a blank note is stored as `NULL`); either limit exceeded is `VALIDATION_ERROR` 400. Duplicate names are allowed. Every backup this route creates is `backup_type` `manual` |
| Backup list | API | `GET /api/backups` |
| Search / type filter / sort | Presentation | Filters (All / Manual / Auto) and orders the loaded list client-side. The page header counts the current program's rows and the saved, manual and auto snapshots. No route or startup path creates an `auto` backup, so the Auto filter and count show only rows already marked `auto` in the database |
| Open a backup | API | `GET /api/backups/<id>` → `NOT_FOUND` 404 for an unknown id — verified live |
| Detail pane "Schema" stat | Presentation | Displays `schema_version` from the detail payload, defaulting to `1` when absent. Informational only — nothing branches on it and restore ignores it ([ADR-008](../DECISIONS.md)). Reads `2` for a backup saved since the execution fields were added to backups and `1` for an earlier one |
| Rename / edit note | API | `PATCH /api/backups/<id>`. At least one of `name` / `note` is required (`VALIDATION_ERROR` 400 otherwise); the same limits as Save apply; an unknown id is `NOT_FOUND` 404 |
| **Restore** | Presentation → API | Confirmation, then `POST /api/backups/<id>/restore`. The confirmation text states plainly that the current plan and all logged sessions will be cleared. A backup holding an execution style or timing value restore cannot interpret is refused as `VALIDATION_ERROR` 400 with `error.reason` `RESTORE_REFUSED`, and nothing is changed: an error toast carries the server's message for 30 seconds, no result panel is shown, and the confirmation stays open |
| Save current plan first | API | Offered inside the restore confirmation only; snapshots the present state before restoring, as an ordinary manual backup named `Pre-restore snapshot (<timestamp>)` |
| Delete | Presentation → API | Confirmation, then `DELETE /api/backups/<id>` |

On `/workout_plan`, More → Backup Center opens `/backup?intent=browse`.

### What restore actually does

Restore is **replace, not merge, and its blast radius is the whole program**:

1. `DELETE FROM workout_log` — **every logged session is deleted**, not just those for the
   restored routines;
2. `DELETE FROM user_selection` — the entire plan, across all routines;
3. re-insert the snapshot's rows.

A snapshot contains **plan rows only** — routine, exercise, sets, rep range, RIR, RPE, weight,
order, superset group, and the execution style with its time cap, EMOM interval and EMOM
rounds. It carries no logged history, no profile, no goals, no body composition, no volume
plans, and no settings. Restoring therefore loses all training history permanently, and does
not restore anything outside the program.

Restore classifies rows before writing. `skipped` lists unique exercise names missing from
the catalog. `invalid` reports each row whose sets, rep bounds, weight or RIR fails validation,
with its routine, exercise and reason. The three steps run in one transaction and roll back
on a database error. The response data is `backup_id`, `backup_name`, `restored_count`, `skipped`
and `invalid`. An unknown id returns HTTP 404 `NOT_FOUND`.

When rows are skipped, the API message, Backup Center panel and toast state the total skipped
rows and the counts by reason. A missing exercise used in two routines counts as two skipped
rows and appears once in the details list. The panel lists invalid rows with their reasons.
When zero rows are restored, the panel uses warning styling and the toast reports the outcome
as a warning. Restore still replaces the active program in that case. When rows were skipped
and none restored, the message ends with "Your current plan and workout log were cleared."
Restored sets and rep bounds are stored as the whole numbers validation parsed.

#### Execution settings, and when a restore is refused

Each restored row gets back the execution style and timing values it had when the backup was
taken. A value the backup does not hold is *missing* — the row was saved before backups carried
these fields, or the backup row holds no value for it (SQL `NULL`). An empty string is a stored
value, not a missing one. A missing style is restored as `standard`; a missing time cap,
interval or rounds value is restored empty, never as a default. So every row of a backup
saved before this change restores as `standard` with no timing values.

A value that is present but cannot be interpreted **refuses the whole restore**, unlike the
per-row skips above. Only rows that would otherwise be restored are checked; a row already
skipped for its catalog entry or its bounds cannot cause a refusal. The cases:

| Case | Example |
|---|---|
| A style that is not exactly `standard`, `amrap` or `emom` — no case folding, no trimming | `tabata`, `EMOM`, ` emom`, an empty string |
| A timing value that is not a whole number | `abc`, `12.5`, an empty string |
| A timing value outside its range: time cap 10–600 s, EMOM interval 15–180 s, EMOM rounds 1–20 | time cap `601` |
| A timing value stored against a style that does not use it | `standard` with a time cap; `emom` with a time cap |

The application cannot write any of these. They reach a backup only when the database was
edited outside it.

A refusal is `VALIDATION_ERROR` 400 with `error.reason` `RESTORE_REFUSED` and `error.rows`,
one `{routine, exercise, field, value, problem}` entry per problem. It is decided before the
first `DELETE`, so the plan, every logged session and the backup itself are exactly as they
were. The message says so and names every offending row; a stored value longer than 40
characters is shown as its first 40 and `…`, and a binary value as `<binary, N bytes>`. The
Backup Center shows that message in an error toast that stays for 30 seconds instead of the
usual 3. Nothing in the application repairs such a row, so the backup cannot be restored until
the value is corrected in the database. The accepted styles and ranges are restore's own
(`utils/backup_execution_contract.py`), pinned so that a later change to the plan page's limits
cannot silently make an existing backup unrestorable ([ADR-015](../DECISIONS.md)).

### Startup snapshot

Separate from the Backup Center library, the application copies the whole SQLite file to
`data/auto_backup/database_<timestamp>.db` (under the runtime root) at startup and immediately
before an erase, using SQLite's online-backup API, and keeps the newest 7. No snapshot is taken —
and the erase response's `auto_backup` is `null` — when the database file is missing, holds fewer
than 100 exercises, or `TESTING=1`; startup also skips it on the first run that has just copied
the catalog seed. These files are outside the Backup Center and have no in-application restore.

---

## Known discrepancies

Recorded because a reader will otherwise assume the obvious reading. None is fixed here — this is
a documentation packet.

| Where | What |
|---|---|
| `static/js/modules/exports.js` — `exportSummary()` | Builds `/export_weekly_summary` or `/export_session_summary`. **Neither route exists**; the real route is `POST /export_summary`. The function is exported and assigned to `window.exportSummary`, but no template or spec invokes it, so nothing currently calls the broken URL. Its unit test mocks `fetch`, so it passes without ever proving the route exists |
| `static/js/app.js` — `initializeModules()` | Defined, contains a single case, and is never called |
| `templates/volume_splitter.html` | Heading reads "AI Suggestions" for a rule-based local heuristic |
| Registered but unbound | **Six of the 78 routes have no caller anywhere** in `templates/` or `static/js/`: `GET /api/superset/suggest`, `GET /get_generator_options`, `GET /get_workout_logs`, `GET /export_workout_log`, `POST /export_summary`, `POST /export_large_dataset`. Established by censusing every registered rule against the whole frontend, matching each rule's static prefix so dynamically assembled URLs still count. They work when called directly; nothing in the UI calls them. Note the causal link: `/export_summary` is unreachable **because** its only intended caller, `exportSummary()`, builds a different URL — see the row above |

---

## Verifying this document

Route claims come from the live `url_map`. Behavior claims come from handler bodies, never from
docstrings — that rule is what caught the progression-status docstring error, since corrected. Outcome claims for
14 GET endpoints and 9 deliberate failure paths were probed against a running application.

The check that matters most here is the **reverse** one, and it is the easy one to skip. Proving
that every route this document names exists is weak — it cannot catch a control described as wired
when nothing calls it. So every registered rule was censused against the whole frontend in the
other direction, matching each rule's static prefix so a dynamically assembled URL still counts.
That pass found the six unbound routes above, and it corrected three claims in an earlier draft of
this document that described unreachable endpoints as live controls.

**Provenance of the "verified live" annotations.** Those come from a one-shot HTTP probe against
a locally running instance, and **the raw capture is not committed** — it would be a stale
snapshot within a release, which is exactly what this suite's anti-drift rule forbids. So they are
not reproducible from the repository alone; re-running the probe is the way to confirm them.
Everything else in this document *is* statically checkable from source, and was checked that way.

Commands to regenerate the ground truth are in
[`README.md`](README.md#re-verifying-this-suite).
