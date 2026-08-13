# App Flow

*What each screen is for, what the user can do on it, and what actually happens — including
when it fails.*

**Derived from:** the source tree at revision `542df07` — every rendered template and its loaded
JavaScript dependency graph, every frontend network call site, every route handler, and a live
HTTP probe of the running application. **On conflict, the code wins.**

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

1. **`app.js` is a shared bundle, but the JS cost is not identical per page.** Five templates load
   an additional page module on top of it, and 17 of the 50 files in `static/js/modules/` are not
   reachable from `app.js` at all:

   | Page | Extra module | Files it adds |
   |---|---|---|
   | `/user_profile` | `user-profile.js` | 8 |
   | `/session_summary` | `session-summary.js` | 3 |
   | `/weekly_summary` | `weekly-summary.js` | 2 |
   | `/workout_plan` | `workout-plan-page.js` + `muscle-selector.js` | 2 |
   | `/body_composition` | `body-composition.js` | 1 |
   | `/` | `welcome.js` | 1 |

   `base.html` separately loads `filter-view-mode.js` and `modal-focus-trap.js` as classic
   scripts — outside the module graph, so they add one file each on every page.

2. **Membership in `pageInitializers` is not the same as having page JavaScript.** `/weekly_summary`,
   `/session_summary`, and `/workout_plan` appear in the map *and* load their own module; the
   live render path for the two summaries is the page module, not `app.js`. Conversely
   `/user_profile` and `/body_composition` are absent from the map and load a module anyway.
   `/fatigue` is the only page with neither — it is entirely server-rendered.

`app.js` also assigns 20 functions onto `window` so inline `onclick=` attributes in templates can
reach them. That is why several controls below have no listener registration you can grep for —
the binding is the `onclick` attribute itself.

## Third-party assets the browser fetches

The server makes no outbound calls. The **browser** does, on every page load:

| Asset | Host | Loaded by |
|---|---|---|
| Inter web font stylesheet + font files | `fonts.googleapis.com`, `fonts.gstatic.com` | `templates/base.html` — every page |
| Bootstrap 5.3.8 JavaScript bundle | `cdn.jsdelivr.net` | `templates/base.html` — every page |
| Sortable 1.14.0 | `cdnjs.cloudflare.com` | `templates/workout_plan.html` |
| flatpickr (CSS + JS) | `cdn.jsdelivr.net` | `templates/progression_plan.html` |
| Popper 2 and Tippy 6 | `unpkg.com` | `templates/volume_splitter.html` |

The Bootstrap **CSS** is served locally from `static/css/bootstrap.custom.min.css`; the CDN
appears only as an `onerror` fallback on that `<link>`, so it is fetched only if the local file
fails to load. Everything in the table above is fetched unconditionally.

Offline, the application still runs and all data operations work, but the Inter font falls back
to the next stack entry and any page depending on a CDN script loses that behavior — drag-and-drop
reordering on the plan, the date picker on progression, tooltips on the splitter.

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
| Author link | Navigation | External, `target="_blank" rel="noopener noreferrer"` |
| Scale − / + | Local state | Writes the `ui-scale-level` **cookie** (1–8). Read server-side by `inject_scale_level()` in `app.py`, which maps it to a zoom factor; out-of-range or non-numeric falls back to `6` (zoom `1`) |
| Muscle naming toggle (`#muscleModeToggle`) | Local state | Writes `hypertrophy_filter_view_mode` to `localStorage` and dispatches a `filterViewModeChanged` event. **No request.** Button label reads **Simple** or **Scientific**; the stored values are `'simple'` and `'advanced'` |
| Dark mode toggle (`#darkModeToggle`) | Local state | Writes `darkMode` (`'true'`/`'false'`) to `localStorage` and sets `data-theme` on `<html>`. With nothing stored it follows `prefers-color-scheme` and keeps following it until the user chooses |
| Skip to main content | Presentation | Focuses `#main-content` |

> The muscle-naming control is a **navbar** button and affects every page. A currently-shipped
> document, `docs/FILTER_VIEW_MODE.md`, tells the reader to find it in the Workout Plan "Filter
> Exercises" header and calls the modes "Simple / Advanced". Both are stale. Flagged here rather
> than corrected — editing that document was outside this packet's scope.

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
the first two entries in the drop list. `docs/program_backups.md` currently states the opposite
("Backups survive normal erase/reset flows because they are not stored in `user_selection`") —
that claim is contradicted by the code. See
[`BACKEND_SCHEMA.md`](BACKEND_SCHEMA.md#what-an-erase-actually-destroys).

The pre-erase snapshot is a raw SQLite file copy. There is **no in-application path to restore
it** — recovery means replacing the database file by hand. Home's own copy, "Auto-backup before
data reset ensures you never lose progress," is optimistic about that.

The exercise catalog is not dropped and is not lost.

---

## Plan — `/workout_plan`

**Purpose.** Build routines. Filter the catalog, choose an exercise, set sets/reps/weight/RIR,
and arrange the result. The densest screen in the application — roughly 59 declared controls plus
per-row controls rendered by JavaScript.

**Initialization.** `initializeWorkoutPlan()` wires filters, the routine cascade, plan handlers,
the volume panel, and the controls animation. It deliberately does **not** call
`handleRoutineSelection()` separately; doing so once left two live listeners on the hidden
`#routine` field and produced a duplicate `/get_all_exercises` fetch per navigation.

### Selecting what to add

| Control | Action type | Endpoint / behavior |
|---|---|---|
| Filter form (muscle, equipment, difficulty, …) | API | `POST /filter_exercises` → filtered names. Column names are whitelist-validated server-side; an unknown column is `VALIDATION_ERROR` 400 |
| Search field | Presentation | Narrows already-loaded options client-side |
| Clear filters | Presentation → API | Resets the form, then `GET /get_all_exercises` |
| Routine cascade — environment → program → day | Presentation → API | Three dependent `<select>`s compose the hidden `#routine` value; selecting a day issues `GET /get_routine_exercises/<routine>`. **That endpoint ignores the routine and returns the full catalog** — deliberately: the dropdown it feeds is an *add* control, so every exercise must stay offered no matter which routine already uses it |
| Exercise `<select>` | API | On change, `GET /get_exercise_info/<name>` for metadata; `GET /api/user_profile/estimate?exercise=…` for the suggested numbers |
| Weight / sets / RIR / RPE / min-rep / max-rep | Presentation | Local inputs. Bounds are enforced on submit by the server, not by the browser attributes |
| Estimate trace toggle | Presentation | Expands the derivation behind the suggested numbers |
| **Add Exercise** | API | `POST /add_exercise` → row appended, table refreshed |

`GET /get_exercise_info/<name>` for an unknown exercise returns HTTP 404 `NOT_FOUND` — verified
live.

### Working with the plan table

| Control | Action type | Endpoint / behavior |
|---|---|---|
| Table load / refresh | API | `GET /get_workout_plan` returns every plan row with its exercise metadata. Called on load and after any mutation |
| Inline field edit | API | `POST /update_exercise` with `{id, updates}`. Server-side bounds: weight 0–1000 kg, RIR 0–10, min ≤ max; violations are `VALIDATION_ERROR` 400 |
| Drag to reorder | API | `POST /update_exercise_order` (Sortable). CDN-dependent |
| Remove row | API | `POST /remove_exercise`. A non-numeric id is `VALIDATION_ERROR` 400 — verified live |
| Replace exercise | API | `POST /replace_exercise` — **see the three-outcome table above** |
| Link superset | API | `POST /api/superset/link` with exactly two ids; one id is `VALIDATION_ERROR` 400 — verified live |
| Unlink superset | API | `POST /api/superset/unlink` |
| Execution style | API | `GET /api/execution_style_options`, then `POST /api/execution_style` |
| Video / image preview | Presentation | Opens a modal. The plan table is built client-side, so its media path is validated in JavaScript by `resolveExerciseMediaSrc()` — a mirror of the server-side shape rules in `utils/media_path.py` |
| Routine tabs | Presentation | Filters displayed rows |
| Volume panel toggle | Presentation → API | Expands the panel, which reads `GET /api/volume_progress` |

### Plan-level actions

| Control | Action type | Endpoint / behavior |
|---|---|---|
| **Generate Starter Plan** | Presentation → API | Modal collects days, environment, experience, goal, volume scale, movement restrictions, equipment whitelist, and up to two priority muscles; submits `POST /generate_starter_plan`. Every dropdown's options are **hardcoded in the template** — `GET /get_generator_options` exists but nothing calls it. Selecting zero equipment is blocked client-side with a warning toast before any request; more than two priority muscles is trimmed to two with a warning |
| Export to Workout Log | API → Navigation | `POST /export_to_workout_log`, then redirects to `/workout_log` after ~1.5 s |
| Export to Excel | Download | `GET /export_to_excel?view_mode=…`, response read as a blob and saved via a temporary `<a download>`. The `view_mode` value is read from `localStorage` |
| Load Program | Navigation | → `/backup?intent=browse` |
| Clear Plan | Presentation → API | Modal, then `POST /clear_workout_plan` |

---

## Log — `/workout_log`

**Purpose.** Record what was actually performed against what was planned. Each row carries both
the `planned_*` snapshot and the `scored_*` values.

| Control | Action type | Endpoint / behavior |
|---|---|---|
| Import from Plan | API | `POST /export_to_workout_log`, same endpoint the Plan page uses |
| Scored weight / min reps / max reps / RIR / RPE | API | `POST /update_workout_log` with `{id, updates: {field: value}}` per field. **An empty string is sent as `null`**, which is how a scored value is cleared — the nullable columns are the contract that makes partial logging work |
| Progression date | API | `POST /update_progression_date` |
| Progression status check | API | `GET /check_progression/<log_id>` |
| Delete row | API | `POST /delete_workout_log` |
| Clear Log | Presentation → API | Modal, then `POST /clear_workout_log` |
| Reference video / thumbnail | Presentation | Opens the shared video modal. This page is server-rendered, so its media path is revalidated at render by the `safe_media_path` Jinja filter — the only template in the application that uses it |

Neither `GET /export_workout_log` nor `GET /get_workout_logs` has any control bound to it in the
current templates — the page's rows are server-rendered, so the log page never needs to fetch
them. Both are listed in *Known discrepancies* below.

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
| Muscle Contribution Mode `<select>` | API | Re-requests `GET /weekly_summary?contribution_mode=total\|direct` with JSON headers. `TOTAL` credits primary 100%, secondary 50%, tertiary 25%; `DIRECT_ONLY` credits primary only |
| Export to Excel | Download | `GET /export_to_excel` — the **workout plan** export, not a summary export |
| Pattern coverage panel | API | `GET /api/pattern_coverage` |
| **Projected fatigue badge** | Presentation + Navigation | Server-rendered on every request. Shows a band label and an info tooltip; its "View per-muscle breakdown" link navigates to `/fatigue` |
| Collapsible explanation | Presentation | `<details>` block |

**`counting_mode` has no UI control.** It is a query parameter (`raw` / `effective`, default
`effective`); the page renders both counts side by side instead of switching between them.
Unrecognized values for either mode fall back to the default rather than erroring.

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
saying "≤10 OK"; and the rep-range factor keys off the *average* of min and max, so an average
landing between buckets matches none of them and falls through to 1.0.

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
| Muscle Contribution Mode | API | Same endpoint, `contribution_mode` |
| **Projected fatigue badge** | Presentation + Navigation | Same always-on server-rendered badge as Weekly Summary; links to `/fatigue` |
| Export to Excel | Download | `GET /export_to_excel` |

**What the date window actually filters.** Volume comes from `user_selection` — the plan. Session
counts come from `workout_log`. The date range filters **only the log side**. So narrowing the
range changes the per-session denominator and the warning level; it never changes the volume
totals. With nothing logged in the window, `sets_per_session` is `null` and the warning level is
`no_data` rather than zero.

The same two-stage effective-set arithmetic and the same informational-only rule apply.

---

## Fatigue — `/fatigue`

**Purpose.** A per-muscle fatigue readout over a selectable period. Entirely server-rendered —
no page-specific JavaScript, and the only control is a form that reloads the page.

| Control | Action type | Behavior |
|---|---|---|
| Period `<select>` | Navigation | Auto-submits its form on change — `GET /fatigue?period=…`, a real navigation and full page reload. There is no Apply button; a submit button exists only inside `<noscript>`, labelled "Update" |
| Link to Plan | Navigation | → `/workout_plan` |

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
| Date field | Presentation | flatpickr picker — CDN-dependent |
| Complete goal | API | `POST /complete_progression_goal/<id>` |
| Delete goal | Presentation → API | Modal, then `DELETE /delete_progression_goal/<id>` |

### What the suggestion is, and is not

- **The page returns a list, not a decision.** A technique note and three manual options are
  appended on every call regardless of status. The double-progression verdict is one card among
  them.
- **There are three reachable statuses**: `increase_weight`, `increase_reps`, `maintain`. The
  function's own docstring advertises a fourth, `reduce_weight`, that the body cannot return —
  reduce-weight appears as a *suggestion* inside the `increase_reps` branch when the lifter has
  been below the minimum twice consecutively and the weight exceeds 5. Read the body, not the
  docstring.
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
| Export volume | Download | `POST /api/export_volume_excel`, saved as a blob |
| Export to Excel | Download | `GET /export_to_excel` — the plan export |
| Active-plan summary | Presentation | Expands the current active plan |
| Tooltips | Presentation | Popper/Tippy — CDN-dependent |

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
| Name + note, Save | API | `POST /api/backups`. A blank name is blocked client-side with a warning toast, and independently by the route as `VALIDATION_ERROR` 400. Saving with an empty plan warns once before proceeding |
| Backup list | API | `GET /api/backups` |
| Search / sort | Presentation | Filters and orders the loaded list client-side |
| Open a backup | API | `GET /api/backups/<id>` → `NOT_FOUND` 404 for an unknown id — verified live |
| Rename / edit note | API | `PATCH /api/backups/<id>` |
| **Restore** | Presentation → API | Confirmation, then `POST /api/backups/<id>/restore`. The confirmation text states plainly that the current plan and all logged sessions will be cleared |
| Save current plan first | API | Offered inside the restore confirmation only; snapshots the present state before restoring |
| Delete | Presentation → API | Confirmation, then `DELETE /api/backups/<id>` |

`/workout_plan`'s "Load Program" button arrives here as `/backup?intent=browse`.

### What restore actually does

Restore is **replace, not merge, and its blast radius is the whole program**:

1. `DELETE FROM workout_log` — **every logged session is deleted**, not just those for the
   restored routines;
2. `DELETE FROM user_selection` — the entire plan, across all routines;
3. re-insert the snapshot's rows.

A snapshot contains **plan rows only** — routine, exercise, sets, rep range, RIR, RPE, weight,
order, and superset group. It carries no logged history, no profile, no goals, no body
composition, no volume plans, and no settings. Restoring therefore loses all training history
permanently, and does not restore anything outside the program.

Rows naming an exercise no longer in the catalog are skipped and reported rather than failing the
restore.

An automatic snapshot is also taken at application startup, and one is taken before an erase.

---

## Known discrepancies

Recorded because a reader will otherwise assume the obvious reading. None is fixed here — this is
a documentation packet.

| Where | What |
|---|---|
| `static/js/modules/exports.js` — `exportSummary()` | Builds `/export_weekly_summary` or `/export_session_summary`. **Neither route exists**; the real route is `POST /export_summary`. The function is exported and assigned to `window.exportSummary`, but no template or spec invokes it, so nothing currently calls the broken URL. Its unit test mocks `fetch`, so it passes without ever proving the route exists |
| `static/js/app.js` — `initializeModules()` | Defined, contains a single case, and is never called |
| `docs/program_backups.md` | States backups survive an erase. The code drops both backup tables |
| `docs/FILTER_VIEW_MODE.md` | Documents the naming toggle as living in the Plan page's filter header and calls the modes "Simple / Advanced". It is a navbar control, and the UI label is "Scientific" |
| `utils/progression_plan.py` — `_get_progression_status` docstring | Advertises a `reduce_weight` return the body cannot produce |
| `templates/volume_splitter.html` | Heading reads "AI Suggestions" for a rule-based local heuristic |
| Registered but unbound | **Six of the 78 routes have no caller anywhere** in `templates/` or `static/js/`: `GET /api/superset/suggest`, `GET /get_generator_options`, `GET /get_workout_logs`, `GET /export_workout_log`, `POST /export_summary`, `POST /export_large_dataset`. Established by censusing every registered rule against the whole frontend, matching each rule's static prefix so dynamically assembled URLs still count. They work when called directly; nothing in the UI calls them. Note the causal link: `/export_summary` is unreachable **because** its only intended caller, `exportSummary()`, builds a different URL — see the row above |

---

## Verifying this document

Route claims come from the live `url_map`. Behavior claims come from handler bodies, never from
docstrings — that rule is what caught the progression-status discrepancy above. Outcome claims for
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
