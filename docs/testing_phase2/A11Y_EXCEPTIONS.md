# Accessibility exception register

Named, owner-visible accessibility debt found while making the a11y suite honest
(Testing Strategy Phase 2, [`PLANNING.md`](PLANNING.md)).

Nothing here is a silent pass. There are two sections, and they record opposite things:

- **[Unasserted contracts](#unasserted-contracts)** (X1–X6) — something a test **could** assert but
  deliberately does not. A row exists because asserting it today would either force a production
  change that owner decision 4 does not authorize, or would assert behavior the app never shipped.
- **[Axe register](#axe-register)** (X7–X15; X11, X12 and X13 are resolved) — WCAG violations the shipped app produces today.
  These *are* asserted: `AXE_REGISTER` in [`e2e/accessibility.spec.ts`](../../e2e/accessibility.spec.ts)
  pins each surface's exact node count, so a violation can neither grow nor disappear unnoticed.
  What each row records is why the defect is not **fixed** here.

Rows keep their history after they are resolved and name the PR that closed them.

## Unasserted contracts

| # | Surface / selector | Rule | Finding | Why not asserted | Disposition |
|---|---|---|---|---|---|
| **X1** | `#routine-env`, `#routine-program`, `#routine-day`, `#exercise` (and the `.wpdd` dropdowns) | WCAG 4.1.2 Name, Role, Value | An invalid required field carried **no `aria-invalid`**; the attribute appeared **zero** times across `templates/`, `static/js/` and `static/css/`. Assistive tech was told *that* something was wrong — the toast is `role="alert" aria-live="assertive"` and focus moves to the control — but never *which* control. | Could not be asserted first: no honest test can demand an attribute that does not exist yet, and axe had nothing to evaluate. The owner granted a **named Decision-4 carve-out on 2026-08-14** — defect established by inspection, regression assertion written alongside the fix. | **RESOLVED — shipped in #364** (`ebfa716`, Packet E). Set and cleared at the sites that own `.is-invalid-required`. On `#exercise` it lands on the `.wpdd-button`, not the native select, which is `aria-hidden="true"`. Asserted by the existing `accessibility.spec.ts` "error states are not color-only" node — no test node added. Packet D cross-checks the fix from the other side: `state:validation-error` reports no new rule, so the attribute is valid everywhere it is now applied. |
| **X2** | `.is-invalid-required` vs `.is-invalid` | — | The app marks required-field errors with the custom class `.is-invalid-required` (`workout-plan-add-exercise.js`), while Bootstrap's `.is-invalid` is used only for scored-value validation on log inputs (`ui-handlers.js`). The old a11y test looked for `.is-invalid` and so could never have matched the required-field surface. | Not a rename but a **restyle**. Bootstrap's `.form-select.is-invalid` adds `--bs-form-select-bg-icon` **and `padding-right: 4.125rem`**, which would put a second icon beside the existing caret and shift layout on the three narrow side-by-side cascade selects. The two classes also mark genuinely different states, and WP4.4-d2 certified these exact selectors (C42–C49, [`CSS_PHASE4_WP4_4_D2_A11Y_EVIDENCE.md`](../CSS_PHASE4_WP4_4_D2_A11Y_EVIDENCE.md)). R1 never bit: no committed capture induces the invalid state, so the risk was live rendering, not baselines. | **DECLINED by owner 2026-08-14. Do not re-propose.** |
| **X3** | `.selection-field.has-validation-error label`, `.cascade-dropdown-wrapper.has-validation-error label` | WCAG 1.4.1 Use of Colour | The *field-level* error signal is colour + box-shadow + a shake animation only. The label turns red; nothing else about the field changes. | The **page-level** signal is not colour-only — a toast names the missing field and focus moves to it — so the shipped behavior satisfies the contract the test asserts. Strengthening the field-level signal is a design change. | Covered at page level by `accessibility.spec.ts` "error states are not color-only". |
| **X4** | `accessibility.spec.ts` "text remains readable when zoomed 200%" | WCAG 1.4.4 Resize Text | The test sets `body.style.zoom = '2'` and asserts a container is still visible. That is not real browser zoom and cannot detect reflow or clipping. | A genuine SC 1.4.4 check needs viewport-scaling work — a redesign, not an assertion repair. | Annotated in the spec. Left weak, deliberately. |
| **X5** | `accessibility.spec.ts` touch targets | WCAG 2.2 SC 2.5.8 / 2.5.5 | The floor asserted is **32 px**, not 44 px. | SC 2.5.8 (AA) requires 24×24; the 44×44 figure is SC 2.5.5, which is **AAA**. 32 px is this app's deliberate, declared floor in three route bundles. Raising it is a product decision and would red multiple bundles. | Intentional. AA-conformant. |
| **X6** | `static/js/darkMode.js` `.theme-animating` | — | **A regression with a named cause, not a mechanism the app never shipped.** The rule `html.theme-animating, html.theme-animating *, …::before, …::after { transition: none !important; animation: none !important; }` lived in `static/css/styles.css` and was deleted by **`ee82643`** ("chore(redesign): P10 remove legacy CSS sources", 2026-04-23) while `darkMode.js` was left intact. The class matched nothing for four months, so `theme-dark.css`'s unconditional `transition: all 0.3s` ran on every switch — measured at **`0.3s`** on `body`, against `0s` once restored. | The original entry blocked this on rule R1. **That was false.** Visual specs never click the toggle — `visual-helpers.ts` sets the theme in an init script, so `applyTheme` runs with `animate=false` and the class is never added — and `prepareForScreenshot()` already injects `transition-duration: 0s !important` before every capture. No capture could move. | **RESOLVED — shipped in #365** (`a49da8d`, Packet F). Restored into `motion.css`, which already owns global transition suppression; `theme-dark.css` is digest-pinned and `a11y.css` has a pinned `!important` count. Both halves of the CSS/JS pair are contract-pinned, since the failure mode was the two drifting apart. `setThemeAndSettle` is deliberately retained — it still guards the 0.2s `!important` dark form-control transition. |

## Axe register

Standards-based `@axe-core/playwright` 4.13.0 scan, WCAG conformance tags only (`wcag2a`,
`wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`); axe's `best-practice` tag is excluded because it
encodes axe's house style rather than a standard. Coverage is 11 routes × 2 themes plus three
deterministic states, all in `e2e/accessibility.spec.ts`, which runs in the **required** functional
gate.

Every row below is a real defect. **None was fixed by Packet D, by owner decision of 2026-08-14:**
Packet D takes the explicit-exception path — axe still executes every WCAG rule, and each existing
violation is pinned by surface, rule id and exact node count rather than suppressed. The
colour/token rewrite and the two-platform visual re-baseline are ruled out for that arc, and the
production corrections for X7–X13 and X15 were recorded as **owner-deferred**, not declined and not
blocking.

**Three of those deferrals have since been taken up.** X11, X12 and X13 shipped in **#393** as the
accessibility labelling packet: all three are WCAG 4.1.2 naming defects fixable by attribute alone,
which is what kept them clear of the colour/token and re-baseline exclusions. `select-name`,
`label` and `aria-prohibited-attr` no longer appear in `AXE_REGISTER` at all.

That is a scope decision, not a verdict on the defects. Owner decision 4 authorizes a production
change only as its own packet with migration notes, and the contrast rows are additionally bound by
standing rule **R1** — no required check measures visual output, so a token fix would stale 66 win32
+ 66 linux captures with CI green.

**Measurement note — dark counts require document-wide settlement.** The merge-time Packet D
reconciliation raised `volume_splitter:dark` from 2 to 3 and `fatigue:dark` from 4 to 6, attributing
the extra nodes to #365's restored transition suppression. That direction was wrong: the body-only
`setThemeAndSettle` helper could return while descendants were still transitioning, so 3 and 6 were
non-final paint. Two subsequent 114-test stress runs exposed the mistake. Waiting on
`document.getAnimations()` still returned too early (7/114 failures); holding a document-wide
computed-paint signature, including pseudo-elements, stable made the final readings reproduce as
**2** and **4** in every repeat. The required source contract pins that scope. Re-measuring with a
body-only or transition-list-only helper can disagree by design.

| # | Surface / selector | Rule | Finding | Registered as | Disposition |
|---|---|---|---|---|---|
| **X7** | Every route except `/progression` (both themes) and `/fatigue` light | WCAG 1.4.3 Contrast (Minimum) | Muted greys and the default link blue fall under 4.5:1 against both surfaces. Measured examples: `.stat-label` **2.56:1** (`#94a3b8` on `#ffffff`), `.step-link` **4.3:1** (`#0d6efd` on `#f8fafc`), and in dark `.tag` **2.78:1** (`#2563eb` on `#1b2948`). `/user_profile` is the worst surface in the app at **84** nodes light / **80** dark — one failing insights-tile label colour repeated across every tile. Dark is not uniformly worse: both summary pages score **better** dark (1 node) than light (4). | `color-contrast`, exact node count per route per theme | **OWNER-DEFERRED 2026-08-14.** Measured and pinned, not fixed: the owner ruled out the colour/token rewrite and the two-platform re-baseline for this arc. A future fix is one token/theme packet carrying that re-baseline, `EXPECTED_SNAPSHOT_COUNTS` and `snapshotManifest` per R1. |
| **X8** | `/fatigue` dark: `.fatigue-page__subtitle`, `label`, `p[data-testid="fatigue-empty-state"]` and its `a[href$="workout_plan"]` | WCAG 1.4.3 Contrast (Minimum) | **Four** nodes at final paint. Recorded separately from X7 because `templates/fatigue.html` links no page bundle at all, so this route is painted entirely by the shared global bundles — these four are a direct reading of shared CSS, not page-local overrides. `/fatigue` **light is clean**, which makes the pair the app's sharpest signal on whether a shared-token change helped or hurt. A merge-time draft raised this to six, but `h1` and `#fatigue-period` were transitional readings; the document-wide settlement proof is recorded above. | `color-contrast` ×4 on `fatigue:dark`; `fatigue:light` registered as an explicit empty list | **OWNER-DEFERRED 2026-08-14.** Belongs to the same future token packet as X7; keep the row distinct so the shared-bundle reading is not averaged away. |
| **X9** | `.wpdd-button` — `#primary_muscle_group_button`, `#secondary_muscle_group_button`, `#tertiary_muscle_group_button`, `#advanced_isolated_muscles_button`, `#exercise_button` | WCAG 4.1.2 Name, Role, Value | `workout-dropdowns.js:573` sets `aria-activedescendant` on a button that is given `aria-haspopup="listbox"` and `aria-controls` but never `role="combobox"`. On an implicit `button` role the attribute is not allowed, so the active option is announced to nobody. | `aria-allowed-attr` ×5 on `workout_plan:{light,dark}` and `state:modal-open`, `state:validation-error` | **OWNER-DEFERRED 2026-08-14.** Real defect, pinned, fix explicitly out of scope for this arc. The smallest correction is `role="combobox"`, which changes the announced role and is therefore its own decision. One component fix with X10. |
| **X10** | `.wpdd-native` — the native `<select>` behind each custom dropdown (**13 nodes**: `#primary_muscle_group`, `#secondary_muscle_group`, `#tertiary_muscle_group`, `#advanced_isolated_muscles`, `#force`, `#equipment`, `#mechanic`, `#utility`, `#grips`, `#stabilizers`, `#synergists`, `#difficulty`, `#exercise`) | WCAG 4.1.2 Name, Role, Value | `workout-dropdowns.js:92` sets `aria-hidden="true"` on the native select but leaves it tabbable — `opacity: 0` with no `tabindex="-1"`, measured `tabIndex: 0` and an explicit focus test returning focusable — so a keyboard user lands on a control assistive tech has been told does not exist. | 13 of the `aria-hidden-focus` ×14 on `workout_plan:{light,dark}` and `state:validation-error`; the 14th is **X15**, a different element | **OWNER-DEFERRED 2026-08-14.** Real defect, pinned, fix explicitly out of scope for this arc. Smallest correction would be `tabindex="-1"` beside the existing `aria-hidden`. Same component as X9. |
| **X11** | `/progression` `#exerciseSelect` | WCAG 4.1.2 Name, Role, Value | The control the entire page is driven by has no `<label>`, `aria-label` or `aria-labelledby`. Its visible heading ("Select Exercise to Progress") is an `<h4>` with no programmatic association. | was `select-name` ×1 on `progression:{light,dark}`; both keys are now `[]` | **RESOLVED — shipped in #393.** The `<h4>` took `id="exerciseSelectLabel"` and the select an `aria-labelledby` pointing at it, so the accessible name is the visible heading rather than a duplicated string. `/progression` is now clean in both themes — the first route besides `fatigue:light` to register an empty array. Attribute-only: all 6 win32 `progression-*` captures byte-matched with no re-baseline. `tests/test_css_cascade_contracts.py:406` pins `id="exerciseSelect"` as a literal substring, so the new attribute was appended after it rather than reordering the tag. |
| **X12** | `/volume_splitter` `.form-range.volume-slider[data-muscle]` (all 18) | WCAG 4.1.2 Name, Role, Value | Every muscle slider is unlabelled. The muscle name is rendered as adjacent text, never associated. The page is almost entirely a form, so this is the single largest functional loss in the app for a screen-reader user. | was `label` ×18 on `volume_splitter:{light,dark}`; both rows are now `color-contrast` only | **RESOLVED — shipped in #393.** `createSliderRow()` gives the `.muscle-name` span an id and points the range input's `aria-labelledby` at it. Deliberately **not** a `for=` on the wrapping `<label>`: that label also contains the live `.current-value` pill, so the association would name the slider "Neck 12" and mutate the name on every drag. Ids are keyed on the render index, which `renderSliders()` makes unique by construction. **Advanced mode was verified separately and is not covered by the register:** it renders 32 sliders, and an A/B measurement on the same code path took it from `label` ×32 to zero, with its pre-existing `color-contrast` ×4 unchanged. |
| **X13** | `/workout_log` `.btn-group` | WCAG 4.1.2 Name, Role, Value | A `div` carries `aria-label` with no `role` to hang it on, so the name is discarded. | was `aria-prohibited-attr` ×1 on `workout_log:{light,dark}`; both rows are now `color-contrast` only | **RESOLVED — shipped in #393, by `role="group"` rather than by deletion.** The element is empty (`childElementCount` 0, a `0×0` rect, referenced by no JS, CSS or test) and `GET /export_workout_log` has no UI control bound to it anywhere — already recorded in [`docs/product/APP_FLOW.md`](../product/APP_FLOW.md) §Known discrepancies — so deleting the placeholder was the preferred fix on review. **It was measured instead of assumed, and the measurement rejected it:** as `display: inline-flex` the empty box still generates a line box, so removing it shortened the page by 21px (`1440×1095` → `1440×1074`) and failed all six win32 `workout-log-*` captures on a size mismatch, which no pixel threshold can absorb. A 0×0 `getBoundingClientRect()` is **not** evidence that a node contributes no layout. Deletion is therefore a 12-capture two-platform re-baseline needing owner by-eye sign-off, and is left as its own packet; `role="group"` clears the same axe node with no pixel movement (18/18 win32 captures byte-matched across all three surfaces). |
| **X14** | The three deterministic states | — | `state:modal-open`, `state:validation-error` and `state:populated-table` are scanned in **light only** — the matrix the plan approved ("11 routes × 2 themes + 3 deterministic states"). Dark contrast for these same *surfaces* is covered by the route scans; what is not covered is dark contrast of the state-specific chrome (modal body, toast, injected rows). | Not registered — this row records the boundary itself | Intentional. Widening it doubles the state scans for the required gate; raise it with the runtime budget in [`PLANNING.md`](PLANNING.md) §6. |
| **X15** | `/workout_plan` `#vpDrawer` — the volume-progress drawer | WCAG 4.1.2 Name, Role, Value | The **fourteenth** `aria-hidden-focus` node, and **not** a `.wpdd-native` select. The collapsed drawer carries `aria-hidden="true"` while still containing focusable content, so the cause and the fix differ from X10's: this is a disclosure-widget state bug, not the progressive-enhancement wrapper. Split out because the original Packet D draft attributed all fourteen nodes to `.wpdd-native`, which was measurably wrong — the 14 axe targets are 13 selects plus this one. | The 14th of `aria-hidden-focus` ×14 on `workout_plan:{light,dark}` and `state:validation-error` | **OWNER-DEFERRED 2026-08-14.** Real defect, pinned, fix explicitly out of scope for this arc. Distinct owner from X9/X10 — do not fold it into that component fix. |

### Why `aria-hidden-focus` is absent from `state:modal-open`

It is not fixed there. axe's `focusable-modal-open` check returns `undefined` — not `false` — whenever
a modal is open, so all fourteen nodes (X10's thirteen `.wpdd-native` selects plus X15's `#vpDrawer`)
move from `violations` into `incomplete`, which the register does not read.
`state:validation-error` scans the same page with no modal open and still reports all fourteen,
which is what keeps the pair honest.

## Rules for this file

1. A row is not a licence to weaken an assertion. Assertions stay as strong as the shipped behavior
   allows; the register records what shipped behavior does *not* cover.
2. A row marked **Owner decision needed** must not be fixed as a side effect of another packet; it
   needs an explicit decision first. X1, X2 and X6 all carried that requirement and were decided on
   2026-08-14 — X1 granted a named Decision-4 carve-out and shipped, X6 restored and shipped, X2
   declined. X7–X13 and X15 were decided on the same day as **owner-deferred**: real defects,
   measured and pinned, whose production fixes were out of scope for that arc. X11, X12 and X13
   were later taken up and shipped in #393; X7–X10 and X15 remain deferred.
3. A resolved row stays, with its resolution recorded. Deleting one loses the reason the gap
   existed, which is what makes a repeat detectable — X6 is the worked example: the mechanism was
   deleted once already and nothing noticed for four months.
4. **Do not cite rule R1 without checking it — and check it by running the captures.** X6 sat
   unscheduled behind an R1 claim that was falsifiable and false. Before deferring a change as
   baseline-affecting, confirm a committed capture actually reaches the state in question. X13 is
   the mirror case and the sharper one: there the R1 risk was *real* and a DOM measurement said it
   was not. **A geometry read in `page.evaluate()` is not the oracle; `visual.spec.ts` is.** Run the
   affected captures before claiming a change is pixel-neutral.
5. X7–X10 and X15 are pinned at exact node counts. If a count moves, the fix is to find out *why* —
   a new violation is a defect, and a vanished one means this file is stale. Editing `AXE_REGISTER`
   to make a red go away is the one thing that turns it back into a suppression list.
6. Every rule id tolerated by `AXE_REGISTER` must appear here as a code span.
   `tests/test_axe_contracts.py` enforces that in the required pytest gate.
