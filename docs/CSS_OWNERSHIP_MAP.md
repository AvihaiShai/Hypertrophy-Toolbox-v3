# CSS Ownership Map

Last updated: 2026-08-27, line citations re-measured against `templates/base.html` after the dark-theme packet inserted a parser-blocking `js/theme-init.js` tag in the head. Every line number below moved by +3; the link **order**, the bundle inventory and the ownership assignments are unchanged. The 2026-08-25 revision re-measured against the route templates at `5ca4191`, corrected item 2 and recorded the load-order drift in item 6; both still stand.

This document reflects the active CSS loading model after the Calm Glass redesign cleanup, the Backup Center page, the Profile page, and the Body Composition page.

## Current Loading Architecture

1. `templates/base.html` loads 8 global application bundles directly.
2. Ten route templates add exactly one route bundle each through `{% block page_css %}`. Two others add none: `templates/error.html` declares the block and deliberately leaves it empty, and `templates/fatigue.html` (`GET /fatigue`) declares no `page_css` block at all. Both render on the global bundles alone.
3. The steady-state app surface is 18 application CSS files: 8 global bundles plus 10 page bundles, excluding Bootstrap.
4. Legacy aggregate and per-feature source files from the redesign migration are no longer part of the runtime loading graph.
5. **Load order is cascade-significant and two globals load *after* the page bundle.** Measured in `templates/base.html`: `tokens.css` (:15), `bootstrap.custom.min.css` (:16), `base.css` (:20), `layout.css` (:21), `components.css` (:22), `navbar.css` (:23), `a11y.css` (:24), **the page bundle (:27)**, then `motion.css` (:28) and `theme-dark.css` (:29) — so those two are the only globals that can beat a route bundle at equal specificity. Nothing paints before `tokens.css`: the only tag above it is the parser-blocking `js/theme-init.js` (:11), which sets `data-theme` on `<html>` so the first stylesheet already resolves against the correct theme.
6. **This is drift since the 2026-05-23 revision.** Read at `d5b80bf` (2026-05-23 23:40 +03), the last commit on or before that date, `tokens.css` loaded at `:26`, after `{% block page_css %}` at `:25`; it now loads first, so it went from overriding route bundles to being overridden by them. A route bundle that relies on beating a token declaration must be re-measured rather than assumed.

## Always-Loaded Core CSS

These styles are linked directly from `templates/base.html` and should be treated as shared app-wide CSS:

Listed in measured link order. Line numbers skip `:14` and `:17`, which are the two `static/vendor/` links (Inter, Font Awesome), and `:11`, the `js/theme-init.js` script; every **global** row below is a `static/css/` link. The italicised row is the page bundle's injection point, not a global file, and can itself carry a `static/vendor/` sheet — see `progression_plan.html` under Page-Specific CSS Loading.

| Load | File | Ownership / purpose |
|---|------|----------------------|
| `base.html:15` | `tokens.css` | Design tokens, spacing, and responsive scale variables |
| `base.html:16` | `bootstrap.custom.min.css` | Bootstrap build artifact |
| `base.html:20` | `base.css` | Element defaults, app background, and baseline typography |
| `base.html:21` | `layout.css` | Shared layout structure and responsive shell behavior |
| `base.html:22` | `components.css` | Buttons, forms, tables, cards, modals, tooltips, toasts, and calm overlay primitives |
| `base.html:23` | `navbar.css` | Global navbar layout and calm glass navbar presentation |
| `base.html:24` | `a11y.css` | Accessibility controls, scale system, focus fixes, and Firefox fallbacks |
| *`base.html:27`* | *`{% block page_css %}`* | *Route bundle injection point — see Page-Specific CSS Loading below* |
| `base.html:28` | `motion.css` | Shared animations and reduced-motion behavior |
| `base.html:29` | `theme-dark.css` | Dark-theme tokens and shared dark overrides |

## Page-Specific CSS Loading

The per-page loading strategy is implemented in the templates below.

| Template | Page-specific CSS |
|----------|-------------------|
| `welcome.html` | `pages-welcome.css` |
| `workout_plan.html` | `pages-workout-plan.css` |
| `workout_log.html` | `pages-workout-log.css` |
| `weekly_summary.html` | `pages-weekly-summary.css` |
| `session_summary.html` | `pages-session-summary.css` |
| `progression_plan.html` | `pages-progression.css` (+ `flatpickr.min.css` at `:7`) |
| `user_profile.html` | `pages-user-profile.css` |
| `body_composition.html` | `pages-body-composition.css` |
| `volume_splitter.html` | `pages-volume-splitter.css` |
| `backup.html` | `pages-backup.css` |

## Active Bundle Responsibilities

The runtime CSS surface is organized around the target bundles below.

| File | Primary ownership |
|------|-------------------|
| `tokens.css` | Responsive tokens, spacing scale, input/button/table sizes, and calm color tokens |
| `motion.css` | Transitions, skeleton states, and motion preferences |
| `base.css` | Body backdrop, shared text defaults, and fluid baseline typography |
| `layout.css` | Containers, shell spacing, responsive tables, and grid/layout utilities |
| `components.css` | Reusable interactive surfaces and component-level UI patterns |
| `navbar.css` | Navigation layout, pills, dropdown presentation, and mobile navbar behavior |
| `theme-dark.css` | Shared dark theme token overrides and dark component styling |
| `a11y.css` | UI scaling, focus states, and browser-specific accessibility fallbacks |
| `pages-welcome.css` | Welcome route presentation |
| `pages-workout-plan.css` | Workout plan route-specific controls and views |
| `pages-workout-log.css` | Workout log route-specific layouts and table behavior |
| `pages-weekly-summary.css` | Weekly summary route visuals |
| `pages-session-summary.css` | Session summary route visuals |
| `pages-progression.css` | Progression route visuals |
| `pages-user-profile.css` | Profile route visuals (reference lifts, insights, coverage bodymap) |
| `pages-body-composition.css` | Body Composition calculator, ACE band, trend SVG, history table |
| `pages-volume-splitter.css` | Volume splitter route visuals |
| `pages-backup.css` | Backup Center route visuals |

## Maintenance Rules

1. Update this map when template CSS loading changes, **including a change of order** — re-read `templates/base.html` rather than editing the table from memory.
2. Add shared rules to an existing global bundle unless the behavior is route-specific.
3. Keep route-specific CSS inside the route bundle; do not reintroduce feature-level runtime files or aggregate `@import` chains.
4. Keep the runtime target at 18 app CSS files plus Bootstrap unless a reviewer explicitly approves a structural change.
