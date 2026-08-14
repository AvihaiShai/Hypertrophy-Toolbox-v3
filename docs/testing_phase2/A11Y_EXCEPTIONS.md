# Accessibility exception register

Named, owner-visible accessibility debt found while making the a11y suite honest
(Testing Strategy Phase 2, [`PLANNING.md`](PLANNING.md)). Every row is something a test
**could** assert but deliberately does not, with the reason.

Nothing here is a silent pass. A row exists because asserting it today would either force a
production change that owner decision 4 does not authorize, or would assert behavior the app never
shipped. Rows keep their history after they are resolved and name the PR that closed them.

## Register

| # | Surface / selector | Rule | Finding | Why not asserted | Disposition |
|---|---|---|---|---|---|
| **X1** | `#routine-env`, `#routine-program`, `#routine-day`, `#exercise` (and the `.wpdd` dropdowns) | WCAG 4.1.2 Name, Role, Value | An invalid required field carried **no `aria-invalid`**; the attribute appeared **zero** times across `templates/`, `static/js/` and `static/css/`. Assistive tech was told *that* something was wrong — the toast is `role="alert" aria-live="assertive"` and focus moves to the control — but never *which* control. | Could not be asserted first: no honest test can demand an attribute that does not exist yet, and axe had nothing to evaluate. The owner granted a **named Decision-4 carve-out on 2026-08-14** — defect established by inspection, regression assertion written alongside the fix. | **RESOLVED — shipped in #364** (`ebfa716`, Packet E). Set and cleared at the sites that own `.is-invalid-required`. On `#exercise` it lands on the `.wpdd-button`, not the native select, which is `aria-hidden="true"`. Asserted by the existing `accessibility.spec.ts` "error states are not color-only" node — no test node added. |
| **X2** | `.is-invalid-required` vs `.is-invalid` | — | The app marks required-field errors with the custom class `.is-invalid-required` (`workout-plan-add-exercise.js`), while Bootstrap's `.is-invalid` is used only for scored-value validation on log inputs (`ui-handlers.js`). The old a11y test looked for `.is-invalid` and so could never have matched the required-field surface. | Not a rename but a **restyle**. Bootstrap's `.form-select.is-invalid` adds `--bs-form-select-bg-icon` **and `padding-right: 4.125rem`**, which would put a second icon beside the existing caret and shift layout on the three narrow side-by-side cascade selects. The two classes also mark genuinely different states, and WP4.4-d2 certified these exact selectors (C42–C49, [`CSS_PHASE4_WP4_4_D2_A11Y_EVIDENCE.md`](../CSS_PHASE4_WP4_4_D2_A11Y_EVIDENCE.md)). R1 never bit: no committed capture induces the invalid state, so the risk was live rendering, not baselines. | **DECLINED by owner 2026-08-14. Do not re-propose.** |
| **X3** | `.selection-field.has-validation-error label`, `.cascade-dropdown-wrapper.has-validation-error label` | WCAG 1.4.1 Use of Colour | The *field-level* error signal is colour + box-shadow + a shake animation only. The label turns red; nothing else about the field changes. | The **page-level** signal is not colour-only — a toast names the missing field and focus moves to it — so the shipped behavior satisfies the contract the test asserts. Strengthening the field-level signal is a design change. | Covered at page level by `accessibility.spec.ts` "error states are not color-only". |
| **X4** | `accessibility.spec.ts` "text remains readable when zoomed 200%" | WCAG 1.4.4 Resize Text | The test sets `body.style.zoom = '2'` and asserts a container is still visible. That is not real browser zoom and cannot detect reflow or clipping. | A genuine SC 1.4.4 check needs viewport-scaling work — a redesign, not an assertion repair. | Annotated in the spec. Left weak, deliberately. |
| **X5** | `accessibility.spec.ts` touch targets | WCAG 2.2 SC 2.5.8 / 2.5.5 | The floor asserted is **32 px**, not 44 px. | SC 2.5.8 (AA) requires 24×24; the 44×44 figure is SC 2.5.5, which is **AAA**. 32 px is this app's deliberate, declared floor in three route bundles. Raising it is a product decision and would red multiple bundles. | Intentional. AA-conformant. |
| **X6** | `static/js/darkMode.js` `.theme-animating` | — | **A regression with a named cause, not a mechanism the app never shipped.** The rule `html.theme-animating, html.theme-animating *, …::before, …::after { transition: none !important; animation: none !important; }` lived in `static/css/styles.css` and was deleted by **`ee82643`** ("chore(redesign): P10 remove legacy CSS sources", 2026-04-23) while `darkMode.js` was left intact. The class matched nothing for four months, so `theme-dark.css`'s unconditional `transition: all 0.3s` ran on every switch — measured at **`0.3s`** on `body`, against `0s` once restored. | The original entry blocked this on rule R1. **That was false.** Visual specs never click the toggle — `visual-helpers.ts` sets the theme in an init script, so `applyTheme` runs with `animate=false` and the class is never added — and `prepareForScreenshot()` already injects `transition-duration: 0s !important` before every capture. No capture could move. | **RESOLVED — shipped in #365** (`a49da8d`, Packet F). Restored into `motion.css`, which already owns global transition suppression; `theme-dark.css` is digest-pinned and `a11y.css` has a pinned `!important` count. Both halves of the CSS/JS pair are contract-pinned, since the failure mode was the two drifting apart. `setThemeAndSettle` is deliberately retained — it still guards the 0.2s `!important` dark form-control transition. |

## Rules for this file

1. A row is not a licence to weaken an assertion. Assertions stay as strong as the shipped behavior
   allows; the register records what shipped behavior does *not* cover.
2. A row marked **Owner decision needed** must not be fixed as a side effect of another packet; it
   needs an explicit decision first. X1, X2 and X6 all carried that requirement and were decided on
   2026-08-14 — X1 granted a named Decision-4 carve-out and shipped, X6 restored and shipped, X2
   declined.
3. A resolved row stays, with its resolution recorded. Deleting one loses the reason the gap
   existed, which is what makes a repeat detectable — X6 is the worked example: the mechanism was
   deleted once already and nothing noticed for four months.
4. **Do not cite rule R1 without checking it.** X6 sat unscheduled behind an R1 claim that was
   falsifiable and false. Before deferring a change as baseline-affecting, confirm a committed
   capture actually reaches the state in question.
