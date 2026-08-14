# Accessibility exception register

Named, owner-visible accessibility debt found while making the a11y suite honest
(Testing Strategy Phase 2, [`PLANNING.md`](PLANNING.md)). Every row is something a test
**could** assert but deliberately does not, with the reason.

Nothing here is a silent pass. A row exists because asserting it today would either force a
production change that owner decision 4 does not authorize, or would assert behavior the app never
shipped.

## Register

| # | Surface / selector | Rule | Finding | Why not asserted | Disposition |
|---|---|---|---|---|---|
| **X1** | `#routine-env`, `#routine-program`, `#routine-day`, `#exercise` (and the `.wpdd` dropdowns) | WCAG 4.1.2 Name, Role, Value | An invalid required field carries **no `aria-invalid`**. `aria-invalid` appears **zero** times across `templates/`, `static/js/` and `static/css/`. Assistive tech is told *that* something is wrong (via the toast) but never *which control*. | Adding the attribute is a production change with no failing honest test behind it — writing a test that demands unbuilt behavior is designing a defect, not exposing one. Axe cannot flag it either: with no `aria-invalid` there is nothing for it to evaluate. | **Owner decision needed.** Not scheduled. |
| **X2** | `.is-invalid-required` vs `.is-invalid` | — | The app marks required-field errors with the custom class `.is-invalid-required` (`workout-plan-add-exercise.js`), while Bootstrap's `.is-invalid` is used only for scored-value validation on log inputs (`ui-handlers.js`). The old a11y test looked for `.is-invalid` and so could never have matched the required-field surface. | Unifying the two class names is a CSS/JS refactor across `a11y.css`, `pages-workout-plan.css` and two JS modules, with visual-baseline consequences (rule R1). | Recorded. Not scheduled. |
| **X3** | `.selection-field.has-validation-error label`, `.cascade-dropdown-wrapper.has-validation-error label` | WCAG 1.4.1 Use of Colour | The *field-level* error signal is colour + box-shadow + a shake animation only. The label turns red; nothing else about the field changes. | The **page-level** signal is not colour-only — a toast names the missing field and focus moves to it — so the shipped behavior satisfies the contract the test asserts. Strengthening the field-level signal is a design change. | Covered at page level by `accessibility.spec.ts` "error states are not color-only". |
| **X4** | `accessibility.spec.ts` "text remains readable when zoomed 200%" | WCAG 1.4.4 Resize Text | The test sets `body.style.zoom = '2'` and asserts a container is still visible. That is not real browser zoom and cannot detect reflow or clipping. | A genuine SC 1.4.4 check needs viewport-scaling work — a redesign, not an assertion repair. | Annotated in the spec. Left weak, deliberately. |
| **X5** | `accessibility.spec.ts` touch targets | WCAG 2.2 SC 2.5.8 / 2.5.5 | The floor asserted is **32 px**, not 44 px. | SC 2.5.8 (AA) requires 24×24; the 44×44 figure is SC 2.5.5, which is **AAA**. 32 px is this app's deliberate, declared floor in three route bundles. Raising it is a product decision and would red multiple bundles. | Intentional. AA-conformant. |
| **X6** | `static/js/darkMode.js` `.theme-animating` | — | The theme toggle adds and removes a `.theme-animating` class to "disable all transitions temporarily", but **no CSS rule anywhere in `static/css/` matches that class**. The suppression mechanism is dead, so `theme-dark.css`'s unconditional `transition: all 0.3s` on `body` runs on every theme switch. | This is a production defect, found by a test-only packet. Fixing it is a CSS/JS change with visual-baseline consequences (rule R1 in [`PLANNING.md`](PLANNING.md)) and no user-visible bug behind it — the transition is cosmetic. | **Owner decision needed.** It is the root cause of the settle wait in `setThemeAndSettle`. |

## Rules for this file

1. A row is not a licence to weaken an assertion. Assertions stay as strong as the shipped behavior
   allows; the register records what shipped behavior does *not* cover.
2. Rows X1 and X2 need an owner decision before any production change. Do not fix them as a side
   effect of another packet.
