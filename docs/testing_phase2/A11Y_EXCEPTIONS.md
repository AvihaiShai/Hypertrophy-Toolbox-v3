# Accessibility exception register

Named, owner-visible accessibility debt found while making the a11y suite honest
(Testing Strategy Phase 2, [`PLANNING.md`](PLANNING.md)).

Nothing here is a silent pass. There are two sections, and they record opposite things:

- **[Unasserted contracts](#unasserted-contracts)** (X1–X6) — something a test **could** assert but
  deliberately does not. A row exists because asserting it today would either force a production
  change that owner decision 4 does not authorize, or would assert behavior the app never shipped.
- **[Axe register](#axe-register)** (X7–X14) — WCAG violations the shipped app produces today.
  These *are* asserted: `AXE_REGISTER` in [`e2e/accessibility.spec.ts`](../../e2e/accessibility.spec.ts)
  pins each surface's exact node count, so a violation can neither grow nor disappear unnoticed.
  What each row records is why the defect is not **fixed** here.

## Unasserted contracts

| # | Surface / selector | Rule | Finding | Why not asserted | Disposition |
|---|---|---|---|---|---|
| **X1** | `#routine-env`, `#routine-program`, `#routine-day`, `#exercise` (and the `.wpdd` dropdowns) | WCAG 4.1.2 Name, Role, Value | An invalid required field carries **no `aria-invalid`**. `aria-invalid` appears **zero** times across `templates/`, `static/js/` and `static/css/`. Assistive tech is told *that* something is wrong (via the toast) but never *which control*. | Adding the attribute is a production change with no failing honest test behind it — writing a test that demands unbuilt behavior is designing a defect, not exposing one. Axe cannot flag it either: with no `aria-invalid` there is nothing for it to evaluate. | **RESOLVED by #364**, which exposes `aria-invalid` on the focused invalid control and clears it on correction, with both halves asserted in `accessibility.spec.ts`. The Packet D scan cross-checks the fix from the other side: `state:validation-error` reports no new rule, so the attribute is valid everywhere it is now applied. |
| **X2** | `.is-invalid-required` vs `.is-invalid` | — | The app marks required-field errors with the custom class `.is-invalid-required` (`workout-plan-add-exercise.js`), while Bootstrap's `.is-invalid` is used only for scored-value validation on log inputs (`ui-handlers.js`). The old a11y test looked for `.is-invalid` and so could never have matched the required-field surface. | Unifying the two class names is a CSS/JS refactor across `a11y.css`, `pages-workout-plan.css` and two JS modules, with visual-baseline consequences (rule R1). | Recorded. Not scheduled. |
| **X3** | `.selection-field.has-validation-error label`, `.cascade-dropdown-wrapper.has-validation-error label` | WCAG 1.4.1 Use of Colour | The *field-level* error signal is colour + box-shadow + a shake animation only. The label turns red; nothing else about the field changes. | The **page-level** signal is not colour-only — a toast names the missing field and focus moves to it — so the shipped behavior satisfies the contract the test asserts. Strengthening the field-level signal is a design change. | Covered at page level by `accessibility.spec.ts` "error states are not color-only". |
| **X4** | `accessibility.spec.ts` "text remains readable when zoomed 200%" | WCAG 1.4.4 Resize Text | The test sets `body.style.zoom = '2'` and asserts a container is still visible. That is not real browser zoom and cannot detect reflow or clipping. | A genuine SC 1.4.4 check needs viewport-scaling work — a redesign, not an assertion repair. | Annotated in the spec. Left weak, deliberately. |
| **X5** | `accessibility.spec.ts` touch targets | WCAG 2.2 SC 2.5.8 / 2.5.5 | The floor asserted is **32 px**, not 44 px. | SC 2.5.8 (AA) requires 24×24; the 44×44 figure is SC 2.5.5, which is **AAA**. 32 px is this app's deliberate, declared floor in three route bundles. Raising it is a product decision and would red multiple bundles. | Intentional. AA-conformant. |
| **X6** | `static/js/darkMode.js` `.theme-animating` | — | The theme toggle adds and removes a `.theme-animating` class to "disable all transitions temporarily", but **no CSS rule anywhere in `static/css/` matches that class**. The suppression mechanism is dead, so `theme-dark.css`'s unconditional `transition: all 0.3s` on `body` runs on every theme switch. | This is a production defect, found by a test-only packet. Fixing it is a CSS/JS change with visual-baseline consequences (rule R1 in [`PLANNING.md`](PLANNING.md)) and no user-visible bug behind it — the transition is cosmetic. | **Owner decision needed.** It is the root cause of the settle wait in `setThemeAndSettle`. |

## Axe register

Standards-based `@axe-core/playwright` 4.13.0 scan, WCAG conformance tags only (`wcag2a`,
`wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`); axe's `best-practice` tag is excluded because it
encodes axe's house style rather than a standard. Coverage is 11 routes × 2 themes plus three
deterministic states, all in `e2e/accessibility.spec.ts`, which runs in the **required** functional
gate.

Every row below is a real defect. None is fixed here: owner decision 4 authorizes a production
change only as its own packet with migration notes, and the contrast rows are additionally bound by
standing rule **R1** — no required check measures visual output, so a token fix would stale 66 win32
+ 66 linux captures with CI green.

| # | Surface / selector | Rule | Finding | Registered as | Disposition |
|---|---|---|---|---|---|
| **X7** | Every route except `/fatigue` light, both themes | WCAG 1.4.3 Contrast (Minimum) | Muted greys and the default link blue fall under 4.5:1 against both surfaces. Measured examples: `.stat-label` **2.56:1** (`#94a3b8` on `#ffffff`), `.step-link` **4.3:1** (`#0d6efd` on `#f8fafc`), and in dark `.tag` **2.78:1** (`#2563eb` on `#1b2948`). `/user_profile` is the worst surface in the app at **84** nodes light / **80** dark — one failing insights-tile label colour repeated across every tile. Dark is not uniformly worse: both summary pages score **better** dark (1 node) than light (4). | `color-contrast`, exact node count per route per theme | **Owner decision needed.** One token/theme packet, carrying the two-platform re-baseline, `EXPECTED_SNAPSHOT_COUNTS` and `snapshotManifest` per R1. Not scheduled. |
| **X8** | `/fatigue` dark: `.fatigue-page__subtitle`, `label`, `p[data-testid="fatigue-empty-state"]` and its `a[href$="workout_plan"]` | WCAG 1.4.3 Contrast (Minimum) | Four nodes, **3.97:1**, **2.49:1**, **3.97:1** and **4.13:1**. Recorded separately from X7 because `templates/fatigue.html` links no page bundle at all, so this route is painted entirely by the shared global bundles — these four are a direct reading of shared CSS, not of page-local overrides. `/fatigue` **light is clean**, which makes the pair the app's sharpest signal on whether a shared-token change helped or hurt. | `color-contrast` ×4 on `fatigue:dark`; `fatigue:light` registered as an explicit empty list | **Owner decision needed.** Belongs to the same token packet as X7; keep the row distinct so the shared-bundle reading is not averaged away. |
| **X9** | `.wpdd-button` — `#primary_muscle_group_button`, `#secondary_muscle_group_button`, `#tertiary_muscle_group_button`, `#advanced_isolated_muscles_button`, `#exercise_button` | WCAG 4.1.2 Name, Role, Value | `workout-dropdowns.js:573` sets `aria-activedescendant` on a button that is given `aria-haspopup="listbox"` and `aria-controls` but never `role="combobox"`. On an implicit `button` role the attribute is not allowed, so the active option is announced to nobody. | `aria-allowed-attr` ×5 on `workout_plan:{light,dark}` and `state:modal-open`, `state:validation-error` | **Owner decision needed.** One component fix with X10. Not scheduled. |
| **X10** | `.wpdd-native` — the native `<select>` behind each custom dropdown | WCAG 4.1.2 Name, Role, Value | `workout-dropdowns.js:92` sets `aria-hidden="true"` on the native select but leaves it tabbable, so a keyboard user lands on a control assistive tech has been told does not exist. Fourteen nodes on `/workout_plan`. | `aria-hidden-focus` ×14 on `workout_plan:{light,dark}` and `state:validation-error` | **Owner decision needed.** Same component as X9. Not scheduled. |
| **X11** | `/progression` `#exerciseSelect` | WCAG 4.1.2 Name, Role, Value | The control the entire page is driven by has no `<label>`, `aria-label` or `aria-labelledby`. Its visible heading ("Select Exercise to Progress") is an `<h4>` with no programmatic association. | `select-name` ×1 on `progression:{light,dark}` | **Owner decision needed.** Smallest fix of the set — one `aria-labelledby` — but still a production change. Not scheduled. |
| **X12** | `/volume_splitter` `.form-range.volume-slider[data-muscle]` (all 18) | WCAG 4.1.2 Name, Role, Value | Every muscle slider is unlabelled. The muscle name is rendered as adjacent text, never associated. The page is almost entirely a form, so this is the single largest functional loss in the app for a screen-reader user. | `label` ×18 on `volume_splitter:{light,dark}` | **Owner decision needed.** Not scheduled. |
| **X13** | `/workout_log` `.btn-group` | WCAG 4.1.2 Name, Role, Value | A `div` carries `aria-label` with no `role` to hang it on, so the name is discarded. | `aria-prohibited-attr` ×1 on `workout_log:{light,dark}` | **Owner decision needed.** Not scheduled. |
| **X14** | The three deterministic states | — | `state:modal-open`, `state:validation-error` and `state:populated-table` are scanned in **light only** — the matrix the plan approved ("11 routes × 2 themes + 3 deterministic states"). Dark contrast for these same *surfaces* is covered by the route scans; what is not covered is dark contrast of the state-specific chrome (modal body, toast, injected rows). | Not registered — this row records the boundary itself | Intentional. Widening it doubles the state scans for the required gate; raise it with the runtime budget in [`PLANNING.md`](PLANNING.md) §6. |

### Why `aria-hidden-focus` is absent from `state:modal-open`

It is not fixed there. axe's `focusable-modal-open` check returns `undefined` — not `false` — whenever
a modal is open, so the fourteen X10 nodes move from `violations` into `incomplete`, which the
register does not read. `state:validation-error` scans the same page with no modal open and still
reports all fourteen, which is what keeps the pair honest.

## Rules for this file

1. A row is not a licence to weaken an assertion. Assertions stay as strong as the shipped behavior
   allows; the register records what shipped behavior does *not* cover.
2. Row X2 needs an owner decision before any production change. Do not fix it as a side effect of
   another packet. (X1 carried the same restriction until #364 resolved it deliberately.)
3. X7–X13 are pinned at exact node counts. If a count moves, the fix is to find out *why* — a new
   violation is a defect, and a vanished one means this file is stale. Editing `AXE_REGISTER` to
   make a red go away is the one thing that turns it back into a suppression list.
4. Every rule id tolerated by `AXE_REGISTER` must appear here as a code span.
   `tests/test_axe_contracts.py` enforces that in the required pytest gate.
