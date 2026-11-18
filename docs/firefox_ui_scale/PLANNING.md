# Plan Review — Firefox application scale (#607, AUD-1291)

**Status:** The owner approved Gate 0 and Plan v2 (Gate 1) on 2026-11-18.

**Planning size:** Large under
[QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md#plan-stage-routing). The change
edits `static/css/a11y.css`, a shared CSS surface. If the modal counter-zoom changes,
it also edits `static/css/components.css`, another shared surface. The change-type
table classifies a shared-surface change as **Large**. This work therefore needs
Gate 0 (this section) and then Gate 1 (council-reviewed Plan v2) before code.

## Section 0 — Requirements Brief

**Raw request** (owner, 2026-11-18, verbatim)
> #607 — choose A′. Proceed with requirements, then the council-reviewed plan for approval before implementation. Fix Firefox scaling and navbar/modal counter-scaling. Include real pointer checks, persistence after reload, and native browser zoom combined with app scale. Record which Firefox version was tested. I approve the Linux visual deep-gate compare dispatch against the eventual implementation commit, with no baseline regeneration included in this approval. Keep the existing browser-support scope; do not add a Firefox Playwright project.

**Owner Gate 0 decision** (owner, 2026-11-18, verbatim)
> #607 correction — approved with revised wording: “Correction: Firefox currently hides the scale control and its divider. When activated programmatically, scaling is also blocked by the Firefox exclusions in JS and CSS. The decided fix makes the control visible and functional in Firefox with CSS zoom support.” Correct the requirements document’s inaccurate wording too, while retaining the historical measurements and their synthetic-input limitation.
>
> #607 — Gate 0 approved with these decisions incorporated:
> - Q1: Use CSS zoom capability detection, without a Firefox version or UA check. Hide the scale control and its associated divider when zoom is unsupported. Firefox 126 introduced CSS zoom support, but that does not establish that our counter-scaling works in every subsequent release. Record the exact tested build and limit validation claims accordingly. No historical browser matrix or additional CI browser is required.
> - Q2: Compare against Firefox’s own level-6 reference, at the same viewport, native zoom, route and UI state. Allow ±1 CSS px for measured dimensions and centering. Require no horizontal overflow, clipping or misplaced pointer targets. Pixel identity with Chromium is unnecessary.
> - A1: Yes, exposing the control in capable Firefox is intended.
> - A2: Replace the unverified version assumption with the verified support boundary and capability fallback above.
> - A3: Safari work is outside scope; do not claim its behavior was verified.
> - A4: Levels 1, 4, 6 and 8 are sufficient for geometry checks. Keep the specified endpoint and native-zoom combination checks.
> - A5/A6: Treat navbar and modal behavior as separate unknowns. Measure both; do not assume a shared failure or cause.
> - A7: Human input or browser/OS automation is acceptable. Use a headed browser and actual pointer targeting of visible elements; synthetic activation does not count.
> - A8: Reset and verify native zoom at 100% before each independent case, then set and record the case’s required native zoom.
>
> Deliberately replace the contract that preserves the Firefox exclusion, while retaining unrelated guarantees. Keep the existing Chromium checks and the approved Linux compare dispatch; no baseline regeneration.

**Wording correction (2026-11-18).** An earlier draft of this brief said that the
control "changes nothing visible in Firefox". That wording implied the control was
visible but inert, which is wrong. On current main the Firefox-only `@-moz-document`
block hides the control. The 2026-11-17 measurements below were taken by activating
the hidden control programmatically with synthetic `.click()`. They are kept as
history with that limitation.

**What A′ refers to** (option text as given to the owner, restated here, not quoted)
Remove the Firefox user-agent exclusion in `applyScale`
(`static/js/accessibility.js`). Remove the Firefox-only `@-moz-document url-prefix()`
block in `static/css/a11y.css`. Make the navbar counter-zoom and the modal
counter-zoom, which both consume `--ui-scale-inverse`, hold their normal size in
Firefox. The Gate 0 decision adds the capability fallback (Q1).

**Prior decision this request continues**
On 25 October 2026 the AI consulting team recorded a delegated decision in
[the #607 comment](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/607#issuecomment-6400201151).
That decision was product direction only and not a Gate 0/1 sign-off. It selected
browser-native Ctrl/Cmd zoom shortcuts, kept application scale on separate controls,
and said to "decide Firefox application-scale behavior separately". It also listed
"Firefox application-scale contract, independently of native shortcut ownership" as
a remaining sub-decision, and it set the constraint "No browser-support expansion
or baseline change". PR #710 (`b5a67581`) shipped the shortcut half. This brief
covers only the Firefox application-scale sub-decision.

### Facts

Facts marked *source* were rechecked in code at `ad6f739b` on 2026-11-18. Facts
marked *measured 2026-11-17* are historical runtime measurements reported for this
brief. They are not re-run here and are cited as measurements, with the input
limitation stated. Facts marked *owner-stated* come from the Gate 0 decision.

- *Source.* `applyScale` sets `data-scale` on `<html>` in every browser. When the
  user agent contains `firefox`, it removes the inline `zoom` instead of setting it
  and writes only `--ui-scale` (`static/js/accessibility.js`, `applyScale`).
- *Source.* `templates/base.html` renders `<html data-scale="…" style="zoom: …">` on
  the server from the `ui-scale-level` cookie. The mapping is in
  `inject_scale_level()` in `app.py`: levels 1–8 map to 0.75, 0.8, 0.85, 0.9, 0.95,
  1, 1.1 and 1.2, and an invalid value maps to level 6.
- *Source.* The `@-moz-document url-prefix()` block in `a11y.css` holds **8**
  `!important` declarations, and it does more than reset zoom:
  - it forces `zoom: 1` on `html` and `html[data-scale]`;
  - it forces `zoom: 1`, `transform: none`, `width: 100%` and `max-width: 100vw` on
    `#navbar`;
  - it declares `display: none` for `.scale-control-compact`, for the nav item that
    contains it, and for the dividers on either side of it.

  **Firefox users therefore have no visible scale control today.** Removing the block
  makes the control visible in Firefox.
- *Source reading, not measured.* The nav-item and divider rules in that block
  probably lose the cascade. `navbar.css` declares
  `#navbar .nav-item { display: flex !important; }` outside any layer. Its
  specificity is (1,1,0), which beats the block's `:has()` selectors at (0,2,0) and
  (0,4,0). `a11y.css` declares no layer, so both rules are unlayered `!important`
  author declarations, and specificity decides. Only the control's own hide
  (`.scale-control-compact`, which has no competitor) is predicted to take effect.
  The empty nav item and both dividers would still render. This is unverified; Plan v1
  measures it (case C0).
- *Source.* `navbar.css` hides the scale nav item and every `.nav-divider` in **all**
  browsers at viewport widths of 1360–1500px
  (`@media (min-width: 1360px) and (max-width: 1500px)`, `!important`, with specificity
  that outranks the rule above). A 1366px viewport falls inside that band.
- *Source.* Only `--ui-scale-inverse` has CSS consumers. There are two:
  - `#navbar { zoom: var(--ui-scale-inverse, 1) }` inside `@supports (zoom: 1)` in
    `a11y.css`;
  - `.modal { zoom: var(--ui-scale-inverse, 1) }` inside `@supports (zoom: 1)` in
    `components.css`.

  `--ui-scale` is declared but no rule reads it. `components.css` also hides
  `.modal-backdrop` unconditionally. Its comment gives the reason: fixed-position
  backdrops render incorrectly under zoom.
- *Source.* Chromium never parses `@-moz-document`, so removing that block cannot
  change the Chromium cascade. That claim comes from the d2 evidence and the
  docstring of `test_chromium_invisible_annotations_were_not_removed`.
- *Source.* `tests/test_css_wp4_4_a11y_contracts.py::test_chromium_invisible_annotations_were_not_removed`
  asserts that the `@-moz-document` block exists and carries exactly 8 `!important`
  declarations. Removing the block makes this test fail by design. In the same file,
  the total `!important` count (50) and the `.scale-control-compact` occurrence
  count (5, of which 4 are inside the block) also move.
- *Source.* `e2e/accessibility.spec.ts` › "Native zoom and application scale" runs on
  Chromium only. It asserts that `html.style.zoom` is `1.2` and `0.75` at the limits,
  and it checks localStorage, the cookie, keyboard activation and reload persistence.
  The Firefox project in `playwright.config.ts` is commented out. No Vitest unit test
  covers `accessibility.js`.
- *Source.* `docs/product/APP_FLOW.md` says the scale buttons "retain their existing
  responsive visibility and Firefox behavior". `docs/product/DESIGN_BRIEF.md`
  describes the user-controlled zoom.
- *Owner-stated.* Firefox 126 introduced CSS `zoom` support. That alone does not
  establish that this app's counter-scaling works in later releases.
- *Measured 2026-11-17 (history; synthetic input).* The environment was Firefox 160.0
  (system install, because this host's Playwright has no Firefox) and Chromium 149, at
  viewport 1366×768 on `/workout_plan`. In Firefox the control was hidden. The
  measurements activated it programmatically with synthetic `.click()`. Under that
  activation, the JS skipped zoom. After a reload, the CSS rule cancelled both the JS
  zoom and the server-rendered inline zoom. (At 1366px the `navbar.css` band above
  also hides the control in every browser.)
- *Measured 2026-11-17 (history; synthetic input).* CSS `zoom` works in Firefox 160.
  Setting it directly scaled the layout at 1.2 and at 0.75. A fixed element, a
  Bootstrap dropdown and a modal stayed hit-testable. Only synthetic `.click()` was
  used.
- *Measured 2026-11-17 (history; synthetic input).* A simulation removed the rule and
  bypassed the JS skip. The record does not say whether the whole `@-moz-document`
  block was removed or only its `html` zoom rule. Page scaling then worked, but the
  navbar counter-zoom failed in Firefox:
  - at scale 1.2, `#navbar` was 76.8px high;
  - at scale 0.75, it was 988px wide and 46.3px high;
  - Chromium holds 1366×64 at both scales.

  The cause is unexplained. *Derived from those numbers:* the level-8 height ratio is
  exactly 1.2 (76.8 / 64). The level-1 ratios are about 0.723 (46.3 / 64 and
  988 / 1366), not 0.75. One mechanism may therefore not explain both levels.
- *Not checked as of 2026-11-17:*
  - real (trusted) pointer input;
  - a headed browser;
  - native Ctrl/Cmd +/− combined with application scale;
  - Firefox versions earlier than 160 (the owner requires no historical matrix);
  - scrolling (the result was inconclusive).

**Problem**
The application-scale control is advertised as an accessibility feature, but it is
unavailable to Firefox users. A Firefox-only rule hides the control. When the hidden
control is activated programmatically, scaling is also blocked by the Firefox
exclusions in JS and CSS, including the scale the server renders after a reload.
Current Firefox supports CSS `zoom`, so the original premise ("zoom is not supported
in Firefox") no longer holds there. Simply removing the exclusion, however, may leave
the navbar scaling with the page, which the counter-zoom design exists to prevent,
and the modal is unverified. A Firefox user with CSS zoom support needs the same
outcome a Chromium user gets: a working scale control, a navbar and modals that keep
their normal size, a choice that survives reload, and correct composition with the
browser's own zoom. A browser without CSS zoom support must not show a control that
does nothing. Chromium and Edge behavior must not change.

**Acceptance criteria**

The Firefox criteria (1–9) are verified manually or by browser/OS automation outside
the committed suite. "Tested Firefox" means the exact build recorded under
criterion 9. "Level-6 reference" means the same element measured at application
level 6 in tested Firefox, at the same viewport, native zoom, route and UI state.
"Within tolerance" means within ±1 CSS px for each measured dimension and for
centering (Q2, resolved). "Geometry levels" means application levels 1, 4 and 8, each
compared with the level-6 reference (A4, resolved).

1. **Control is available.** In tested Firefox, at the viewport widths where Chromium
   shows the scale control, the user loads any page. The `−`/indicator/`+` control
   and its dividers are then visible and operable, with the same responsive
   visibility as Chromium. (A1, resolved.)
2. **Page content scales.** In tested Firefox, the user changes the level with real
   pointer input (see 6). At each geometry level, the page then renders at that
   level's mapped factor (0.75–1.2). A reference element in the main content measures
   within tolerance of level-6 reference × factor. The indicator and the disabled
   state at levels 1 and 8 update as they do in Chromium.
3. **Navbar holds its size.** In tested Firefox, at each geometry level, the `#navbar`
   width and height equal the level-6 reference within tolerance. The navbar spans
   the viewport width, and the page shows no horizontal overflow or clipping. The
   2026-11-17 failure (76.8px at 1.2; 988×46.3 at 0.75) must not reproduce.
4. **Modals hold their size and stay usable.** In tested Firefox, at each geometry
   level, a Bootstrap modal is opened on a page that has one. The modal dialog then:
   - is centered in the viewport within tolerance;
   - is fully visible, or scrollable to its full content, with no clipping;
   - has its controls (close, primary action, form fields) operable with real
     pointer input;
   - matches the level-6 reference size within tolerance.

   Closing the modal returns the page to a usable state.
5. **Persistence after reload.** In tested Firefox, the user sets level 8 and reloads.
   The page then:
   - renders scaled from first paint through the server-rendered zoom, with no
     visible reset to 100%;
   - shows indicator `8`;
   - keeps localStorage and the cookie `ui-scale-level` at `8`.

   The same holds for level 1, and for navigating to a second route.
6. **Real pointer input.** In tested Firefox, at levels 1 and 8, the checks run in a
   headed browser with real pointer input: a human with a physical pointer, or
   browser/OS automation that moves the pointer to visible elements and clicks them.
   Synthetic activation (`.click()`, `dispatchEvent`) does not count. (A7, resolved.)
   Under that input, these land on the intended target:
   - the scale buttons;
   - a navbar link;
   - a navbar dropdown and one of its items;
   - the dark-mode toggle;
   - a fixed-position element;
   - a modal's controls;
   - one table/form control in the main content.

   The page scrolls to its last content at both levels. No pointer target is
   misplaced.
7. **Native zoom combined with application scale.** In tested Firefox, before each
   independent case, native zoom is reset and verified at 100%. The case's required
   native zoom is then set and recorded (A8, resolved). The cases cover native zoom at
   least one step above and one below 100% (for example 110% and 90%), each with
   application levels 1 and 8. The two effects then compose:
   - the page is scaled by both;
   - the navbar holds its size relative to the level-6 reference at the same native
     zoom, within tolerance;
   - modals stay usable as in 4;
   - pointer targets stay correct as in 6.

   Native zoom changes never write `ui-scale-level`. Ctrl/Cmd+0 resets only native
   zoom and leaves the application level unchanged.
8. **Browsers without CSS zoom support.** Capability, not identity, decides
   (Q1, resolved):
   - Neither the JS nor the CSS contains a Firefox version check or a user-agent check
     for application scale.
   - Where CSS `zoom` is unsupported, the scale control and its associated divider are
     hidden.
   - Where CSS `zoom` is supported, the control is shown, subject to the responsive
     visibility in criterion 1.
9. **Build recorded and claims limited.** The implementation evidence records:
   - the exact Firefox version and build ID;
   - the OS;
   - the viewport;
   - that the run was headed;
   - the input method used for 1–8;
   - the native zoom of each case.

   The owner-facing docs (`docs/product/APP_FLOW.md`, `docs/product/DESIGN_BRIEF.md`)
   state the capability-based behavior and the tested build. They replace the current
   "existing … Firefox behavior" wording. They claim validation only for the tested
   build, and they make no claim about Safari.
10. **Chromium/Edge unchanged.** The existing Chromium assertions in
    `e2e/accessibility.spec.ts` › "Native zoom and application scale" pass without
    modification. The full `visual.spec.ts` matrix (`PW_VISUAL_SEED=1`) and the
    approved Linux visual deep-gate compare dispatch, run against the implementation
    commit, show no new difference attributable to this change. No baseline is
    regenerated.
11. **Committed contracts stay honest.**
    - The contract that preserves the Firefox exclusion is replaced deliberately, in
      this change, with a recorded justification.
    - Its replacement guards against reintroducing a Firefox-only or user-agent
      exclusion of application scale.
    - The unrelated guarantees in that contract file, and every other existing a11y or
      cascade contract guarantee, are retained.
    - No Firefox Playwright project is added, and no browser is added to CI.
12. **No unrelated behavior moves.**
    - The scale mapping, the 1–8 limits, the storage key, the cookie, the
      server-side fallback and the native-shortcut contract from #710 are unchanged.
    - No schema, API, route or calculation change is made.

**Calculation surface**
- `none`. No effective-sets, volume, progression, fatigue or other calculation
  function is touched. The 1–8 → zoom-factor mapping in `app.py` and
  `accessibility.js` is a presentation constant, and it stays unchanged
  (criterion 12).

**In scope**
- The application-scale path in `static/js/accessibility.js` (`applyScale`): removing
  the user-agent exclusion.
- Removing the Firefox-only block in `static/css/a11y.css`.
- A CSS-zoom capability fallback that hides the scale control and its associated
  divider where zoom is unsupported, with no version or user-agent check.
- Navbar counter-scaling in Firefox and modal counter-scaling in Firefox, diagnosed
  separately (`a11y.css`, and `components.css` if needed), without changing Chromium.
- Replacing the a11y contract that preserves the Firefox exclusion, plus any committed
  coverage the plan selects. The council decides whether to add Vitest coverage of
  `applyScale`.
- A manual or browser/OS-automated Firefox verification, outside the committed suite,
  that covers criteria 1–9 with the build recorded.
- Product-doc updates: `APP_FLOW.md` (Scale row) and `DESIGN_BRIEF.md` (user-controlled
  zoom).
- Required gates for this change, as the union from QUALITY_GATE:
  - full `pytest`;
  - Chromium `smoke-navigation`, `nav-dropdown`, `accessibility`, `dark-mode`,
    `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes` and
    `ui-hardening`;
  - the full `visual.spec.ts` matrix with `PW_VISUAL_SEED=1`;
  - seven-surface Stylelint (`node scripts/css_audit/stylelint_surfaces.mjs`), with
    no category rising;
  - the Linux visual deep gate (`Deep Gate Visual (Linux)`) in **compare** mode
    against the implementation commit. The owner approved that dispatch and approved
    no baseline regeneration;
  - a manual smoke for the interactive JS change;
  - `docs/test_inventory/` regenerated if any test is added, removed or renamed.

**Out of scope / non-goals**
- Adding a Firefox (or WebKit) Playwright project or any CI browser, which would
  expand browser support.
- A historical browser matrix: testing Firefox builds other than the recorded one.
- Regenerating visual baselines on either platform.
- Changing native-zoom shortcut handling (shipped by #710).
- Changing the scale levels, mapping, limits, persistence keys or server rendering.
- Restoring `.modal-backdrop`, or other modal and backdrop redesign beyond holding
  modal size and usability in Firefox.
- Giving `--ui-scale` a consumer, or tidying the unused token, unless the plan shows
  it is needed for the fix.
- Safari work, and any claim that Safari behavior was verified (A3).

**Assumptions made**

The owner reviewed A1–A8 at Gate 0 on 2026-11-18. Each one is resolved below.

- **A1 (resolved).** Exposing the scale control in capable Firefox is intended
  (owner: "Yes").
- **A2 (resolved).** The earlier, unverified version assumption is replaced. Firefox
  126 introduced CSS `zoom` support (owner-stated). Behavior is decided by CSS-zoom
  capability detection with no version or user-agent check. Where zoom is
  unsupported, the control and its associated divider are hidden. Validation is
  claimed only for the tested build.
- **A3 (resolved).** Safari and WebKit work is out of scope. No claim is made that
  their behavior was verified. By source reading, WebKit has no `@-moz-document` and
  no UA match, so it already takes the Chromium path. That reading is not a
  verification.
- **A4 (resolved).** Levels 1, 4, 6 and 8 suffice for geometry checks (6 is the
  reference). The endpoint checks (levels 1 and 8) and the native-zoom combination
  checks remain as specified.
- **A5 (resolved).** The navbar counter-zoom failure in Firefox is an unknown and is
  measured on its own. No cause is assumed. The plan must show the mechanism before
  it relies on a fix.
- **A6 (resolved).** The modal is a separate unknown and is measured on its own. No
  shared failure or cause with the navbar is assumed.
- **A7 (resolved).** Real pointer input means human input or browser/OS automation in
  a headed browser, with the pointer targeting visible elements. Synthetic activation
  does not count. The evidence names the method used.
- **A8 (resolved).** Before each independent case, native zoom is reset and verified
  at 100%. The case's required native zoom is then set and recorded.
- **A9 (resolved).** The raw request quoted above is the owner's message of
  2026-11-18, quoted verbatim by the coordinating session. The 2026-11-18 comment on
  #607 records the same decision in paraphrase.

**Open questions for the user**
- **Q1 (answered 2026-11-18).** Capability detection decides, with no version or
  user-agent check. Where zoom is unsupported, the control and its associated divider
  are hidden. The tested build is recorded and claims are limited to it. No historical
  browser matrix and no additional CI browser are required. Folded into criteria 8–9.
- **Q2 (answered 2026-11-18).** Compare against Firefox's own level-6 reference at the
  same viewport, native zoom, route and UI state. Allow ±1 CSS px for measured
  dimensions and centering. Require no horizontal overflow, clipping or misplaced
  pointer targets. Pixel identity with Chromium is unnecessary. Folded into
  criteria 2–7.

Two non-blocking notes were raised after Gate 0. Plan v1 raised them as owner
questions OQ1 and OQ2, and Plan v2 carries them, with recommendations, to Gate 1:
- The source reading above predicts that today's block hides only the control, not
  the nav item or the dividers. If case C0 confirms that, the approved #607 correction
  ("hides the scale control and its divider") overstates today's Firefox rendering.
- The decision says "its associated divider", in the singular. Today's block declares
  hides for both flanking dividers.

### Section 0 sign-off — GATE 0
- [x] User confirms the acceptance criteria match intent. — owner, 2026-11-18
- [x] User reviewed the assumptions (A1–A8) and corrected or accepted each one. — owner, 2026-11-18
- [x] Blocking questions Q1 and Q2 are answered. — owner, 2026-11-18

---

## Plan v1

**Goal**: Firefox builds that support CSS `zoom` get a working application-scale
control. With that control, the navbar and modals hold their normal size, the choice
persists across reload, and the control composes with native zoom. Browsers without
CSS `zoom` support hide the control and its divider. Chromium and Edge behavior stays
unchanged.

**Scope**
- **In**:
  - removing the user-agent branch in `applyScale`, so the inline zoom is always
    written;
  - deleting the `@-moz-document url-prefix()` block in `a11y.css`;
  - adding a CSS capability fallback (`@supports not (zoom: 1)`) that hides the scale
    nav item and its associated divider;
  - two markup hooks in `templates/base.html` for that fallback;
  - a separate diagnosis of the Firefox navbar counter-zoom and of the Firefox modal
    counter-zoom, then a fix for each only where the diagnosis shows one is needed,
    chosen under the decision rule below;
  - replacing the contract that preserves the Firefox exclusion, plus a small new
    capability contract;
  - updating stale comments in `a11y.css` and `accessibility.js`;
  - product-doc updates; inventory regeneration;
  - the manual Firefox verification protocol; the Chromium gates; the approved Linux
    compare dispatch.
- **Out**:
  - a Firefox, WebKit or any other new Playwright project or CI browser;
  - any baseline regeneration;
  - Safari work or claims;
  - a historical Firefox matrix;
  - changes to `app.py`, the scale mapping, the storage key, the cookie, the
    server-side fallback, or the #710 shortcut contract;
  - `.modal-backdrop` or other modal redesign;
  - giving `--ui-scale` a consumer;
  - edits to `navbar.css` (any need for one stops the work for owner approval);
  - edits to historical evidence docs that mention `@-moz-document`
    (`docs/CSS_PHASE4_WP4_4_D2_A11Y_EVIDENCE.md` and `docs/css_scale_btn_cleanup/*`),
    which stay as history;
  - the shared files `app.py`, every `CLAUDE.md`, `.claude/settings.json`,
    `docs/MASTER_HANDOVER.md` and `.gitignore`;
  - `utils/workout_log.py`, `routes/workout_log.py`, `routes/workout_plan.py` and the
    summary modules, which another session owns.

### Key decisions

**D1. Capability detection runs in CSS, not JS.** The fallback is
`@supports not (zoom: 1) { … }` in `a11y.css`. The JS route was considered and
rejected for four reasons:
- *First paint.* `accessibility.js` loads at the end of `<body>`, so a JS check would
  show the control and then hide it. `@supports` applies before first paint.
- *Same test as the existing counter-zoom.* Both counter-zoom rules are already gated
  by `@supports (zoom: 1)`. The fallback is its exact complement, so the control and
  the counter-zoom can never disagree about support.
- *The cascade.* `#navbar .nav-item { display: flex !important; }` in `navbar.css`
  defeats the `hidden` attribute and any low-specificity class. A JS route would
  still need a CSS rule to win, so it adds code without removing the CSS.
- *No new DOM work in `accessibility.js`.* `test_accessibility_js_still_constructs_no_dom`
  pins that module's DOM-free premise. The CSS route leaves it untouched.

JS then needs no capability check at all. `applyScale` always writes
`document.documentElement.style.zoom`, exactly as the server already does for every
browser. A browser without zoom support ignores the property, and the control is
hidden in that browser anyway. The `--ui-scale` inline write in the Firefox branch is
deleted with that branch. That variable has no consumer, and the `data-scale` blocks
in `a11y.css` declare it regardless.

**D2. The fallback targets markup hooks, not `:has()`.** `base.html` gains
`data-scale-control-item` on the `<li>` that contains `.scale-control-compact`, and
`data-scale-control-divider` on its associated divider. The fallback rule is:

```css
@supports not (zoom: 1) {
    #navbar .nav-item[data-scale-control-item],
    #navbar .nav-item[data-scale-control-divider] {
        display: none !important;
    }
}
```

The reasons:
- *Firefox's `:has()` support starts at 121.* A `:has()` selector list is
  non-forgiving, so Firefox ≤120 would drop the whole rule and show an inert control.
  Attribute selectors work wherever `@supports not` works.
- *Specificity is (1,2,0) with `!important`.* That beats `navbar.css`'s (1,1,0)
  `!important`, the rule that source reading says defeats today's block.
- *Chromium never applies the block.* The attributes match nothing in Chromium, so
  Chromium rendering cannot change.

**D3. "Its associated divider" means the trailing divider.** The divider after the
control is at `base.html` line 209, between the control and the muscle-mode toggle.
Hiding it, together with the control's item, leaves exactly one separator between the
signature and the muscle-mode toggle. That matches the owner's singular wording.
Hiding both dividers would leave no separator. **Owner confirmation requested
(OQ1).**

**D4. Diagnose the navbar and the modal separately before choosing any fix**
(A5/A6). See the diagnosis protocol below. A counter-zoom change is made only when the
diagnosis names a mechanism and the decision rule accepts the fix.

**D5. Replace the contract deliberately and keep its unrelated guarantees.** See the
contract changes below. The WP4.4 packet file changes only where the deleted block
moved a pinned number. The new #607 guarantees go in a new file, so the WP4.4 file
keeps its historical scope.

**D6. Chromium invariance is shown by construction, plus measurement.** By
construction:
- `@-moz-document` is never parsed by Chromium;
- `@supports not (zoom: 1)` is false in Chromium;
- the new attributes match no Chromium-applied rule;
- the JS path Chromium takes is unchanged.

Any counter-zoom fix additionally needs a Chromium computed-style and geometry
differential (step 6).

### Diagnosis protocol — navbar and modal, separately (Phase A)

The diagnosis runs in tested Firefox, headed, on the Phase B build (exclusions
removed, no counter-zoom change). It uses the scratch runtime and the disposable
profile from the verification protocol. The viewport is chosen as in V-2. Native zoom
is 100%, reset and verified first. Levels 1, 4, 6 and 8 are tested.

**Validate the oracle first** (`.claude/rules/verification.md`). Run the measurement
script in Chromium on the same build, before any Firefox result is trusted:
- a known-scaled element (the main-content reference element) must read
  factor × level-6 at each level;
- the known-counter-zoomed `#navbar` must read its level-6 size at every level;
- two runs with identical CSS must give identical records.

If any control fails, the script's coordinate space is wrong. Fix the script before
reading Firefox numbers. The engines may report `getBoundingClientRect` in different
spaces under CSS zoom, so the decisive geometry is the on-screen box: screenshot pixels
÷ `devicePixelRatio`. The DOM reads are diagnostic.

Measurement reads through the DevTools console are allowed, because A7 restricts
activation, not reads. Level changes during diagnosis may use the control with real
pointer input, or a cookie or localStorage write followed by reload. The method is
recorded. Acceptance (Phase C) uses real pointer input only.

**Navbar.** At each level, record:
- for `html`, `body` and `#navbar`: `getComputedStyle(el).zoom` and
  `el.currentCSSZoom`;
- for `#navbar`: the computed `width`, `max-width`, `height` and `position`,
  `getBoundingClientRect()`, `offsetWidth` and `offsetHeight`;
- `documentElement.scrollWidth` versus `clientWidth`;
- the on-screen navbar box from a screenshot.

**Modal.** The modal is `#generatePlanModal` on `/workout_plan`, which has a close
button, a primary action and form fields. At each level, with the modal open, record:
- the same zoom reads for `.modal`, `.modal-dialog` and `.modal-content`;
- their bounding rectangles;
- the dialog's center offset from the viewport center;
- whether the content scrolls to its end;
- the on-screen dialog box from a screenshot;
- with real pointer input, whether a click on the visible close button and on a form
  field lands on that element.

**Hypotheses.** Each is tested on its own, for the navbar and the modal separately.

| ID | Hypothesis | What would show it |
|---|---|---|
| H0 | The 2026-11-17 failure came from the simulation leaving part of the `@-moz-document` block in force. For example, `#navbar { zoom: 1 !important; max-width: 100vw !important }` would defeat the counter-zoom. | With the whole block deleted, the navbar and modal hold their size within tolerance. |
| H1 | The counter-zoom declaration does not apply in Firefox. | The computed `zoom` on the element is `1`, not the inverse, and `currentCSSZoom` equals the page factor. |
| H2 | The counter-zoom applies, but sizing resolves differently under nested zoom. Candidates: `width: 100%` or `max-width: 100vw` with `position: sticky` (navbar); `position: fixed` and its viewport containing block (modal). | `currentCSSZoom` is about 1, but the box differs from the reference. Overriding the suspect declaration in DevTools restores it. |
| H3 | (Modal only) Firefox already centers fixed elements correctly under root zoom, and the counter-zoom moves the dialog off center. | Disabling the counter-zoom in DevTools restores centering in Firefox. |
| H4 | The measurement is wrong, not the rendering: the DOM coordinate space differs. | The DOM reads disagree with the screenshot box while the screenshot box is within tolerance. |

The level-1 ratio of about 0.723 versus the level-8 ratio of exactly 1.2 (Section 0)
is checked explicitly. If they differ, the levels may need different explanations.

**Candidate fixes.** These apply per element.
- **None needed** (H0 or H4 confirmed). Record the measurements and make no change.
- **Re-express the counter-zoom engine-neutrally** (H1). For example, use literal
  per-level values (`html[data-scale="1"] #navbar { zoom: 1.333 }`) inside the same
  `@supports (zoom: 1)` gate, in the file that owns the rule today.
- **Adjust only the diverging sizing declaration** (H2), inside the owning file's
  `@supports (zoom: 1)` block. Change it in a form that leaves Chromium's geometry
  identical.
- **Escalate** (H3, or no candidate passes). Firefox and Chromium would need opposite
  treatment, and capability detection cannot tell them apart. A user-agent or
  `-moz-` gate is forbidden by Q1.

**Decision rule.** A fix is adopted only if all of the following hold:
1. the diagnosis names the mechanism with a measurement that the fix demonstrably
   changes;
2. the fix uses no user-agent check, version check, `@-moz-document` or `-moz-`
   gate;
3. it edits only `a11y.css` (navbar) or `components.css` (modal);
4. with it applied in tested Firefox, the element meets criteria 3 or 4 at levels 1,
   4 and 8;
5. the Chromium differential (step 6) shows identical geometry for `#navbar`,
   `.modal` and `.modal-dialog` at levels 1, 4, 6 and 8 and at the three visual
   viewports, with the same-CSS control at zero differences. Any computed-value change
   is listed and shown geometry-neutral.

If several candidates qualify, take the one with the fewest changed declarations. If
none qualifies, implementation **stops**. The diagnosis goes to the owner as a plan
amendment, and nothing ships partially. The navbar and the modal are decided
independently: a navbar fix is never assumed to fix the modal, or the reverse.

### Firefox verification protocol (Phase C — acceptance)

**V-1. Environment**
- *Scratch runtime.* Both variables sit under `artifacts/`:
  - `HT_RUNTIME_DIR` = `artifacts/firefox_ui_scale/runtime/`;
  - `DB_FILE` = `artifacts/firefox_ui_scale/runtime/database.db`, a seeded copy made
    by `e2e/scripts/prepare_e2e_db.py --output <that path>`.

  Setting `HT_RUNTIME_DIR` alone copies the real database, so `DB_FILE` is mandatory.
  The startup log must show the scratch database path before any case runs. Launch
  with debug and the reloader off, per the `run-hypertrophy-toolbox` skill's rules,
  and record the port.
- *Browser.* Tested Firefox runs headed with a disposable profile at
  `artifacts/firefox_ui_scale/firefox-profile/` (`-no-remote -profile`). Per-site
  zoom, cookies and storage then start clean, and the owner's own profile is not
  touched.
- *Recorded once.* From `about:support`: version, build ID and update channel. Also
  the OS build, `devicePixelRatio` at 100%, the window's `innerWidth` and
  `innerHeight`, the input method (human pointer, or the named OS/browser automation),
  and the implementation commit SHA.

**V-2. Viewport.** The control must be visible in every case. `navbar.css` hides it
below 992px and from 1360 to 1500px. Native zoom also changes the CSS viewport width.
The window is therefore sized so that `innerWidth` stays at or above 1501 at 110%
native zoom: 1920 is the target, which gives about 1745 at 110% and about 2133 at
90%. `innerWidth` is recorded for every case. A visibility-only check also runs at
1280 (visible) and 1440 (hidden, in both browsers) for criterion 1.

**V-3. Case reset (A8).** Before every independent case:
1. press Ctrl+0;
2. verify native zoom is 100%: no zoom badge in the URL bar, and `devicePixelRatio`
   equals the recorded 100% value;
3. set the case's native zoom with Ctrl +/− and record it;
4. set the application level with real pointer clicks on `−`/`+`.

**V-4. Cases**

| Case | Native zoom | Levels | Route | Checks | Criteria |
|---|---|---|---|---|---|
| C0 | 100% | 6 | `/workout_plan` (on **main**, before the change) | Do the scale item and the two dividers render in Firefox today? Records history; answers OQ2. | — |
| C1 | 100% | 6 | `/workout_plan` | Level-6 reference: navbar box, main-content reference element, `#generatePlanModal` dialog box and center | 2–4 baseline |
| C2 | 100% | 1, 4, 8 | `/workout_plan` | Content factor, navbar box, modal box, center and scroll versus C1; no horizontal overflow or clipping | 2, 3, 4 |
| C3 | 100% | 1, 8 | `/workout_plan` | The criterion 6 target list under real pointer input; scroll to the last content | 6 |
| C4 | 100% | 8, then 1 | `/workout_plan` → reload → `/weekly_summary` | First paint already scaled, indicator, localStorage, cookie | 5 |
| C5 | 110% and 90% (separate cases) | 6 reference, then 1 and 8 | `/workout_plan` | Navbar and modal versus level 6 at the same native zoom; pointer targets; no `ui-scale-level` write on native zoom change; Ctrl+0 leaves the level unchanged | 7 |
| C6 | 100% | 6 | `/` | Control and dividers visible at 1280 and 1920, hidden at 1440 (also in Chromium) | 1 |
| C7 | 100% | — | `/` | Unsupported fallback: a second disposable profile with `layout.css.zoom.enabled` = `false`, if the tested build still has that preference. Expected: `CSS.supports('zoom', '1')` is false, and the control item and trailing divider are hidden. If the preference is absent, record "not runtime-verifiable on the tested build" and rely on the contract test. | 8 |

Every geometry comparison applies the ±1 CSS px tolerance to on-screen boxes
(screenshot pixels ÷ `devicePixelRatio`). Each comparison is against the level-6
reference at the same viewport, native zoom, route and UI state.

**V-5. Evidence location.** Under `artifacts/firefox_ui_scale/evidence/<YYYY-MM-DD>/`:
- `environment.md`: everything listed in V-1, plus the port;
- `diagnosis.md`: navbar and modal in separate sections, with oracle control output,
  measurements, the hypothesis confirmed, the fix chosen or "none needed", and the
  Chromium differential result;
- `cases.csv`: case, native zoom, level, route, element, measured box, reference box,
  delta, pass/fail;
- screenshots named by case.

`artifacts/` is gitignored and local. The durable record is a summary table in the
PR description and in the #607 closing comment. Whether to commit an evidence summary
is OQ3.

### Contract changes

**`tests/test_css_wp4_4_a11y_contracts.py`.** Deliberate edits only. Every other test
and constant stays as is.
- **`test_chromium_invisible_annotations_were_not_removed`**
  - Drop the `@-moz-document` half: the block exists, with 8 `!important`.
  - Keep the four annotated `-moz-box-shadow` declarations unchanged. That guarantee
    is unrelated to #607.
  - Update the docstring from 12 to 4 annotations, recording that #607 deleted the 8
    by owner decision at Gate 0 on 2026-11-18. They were deleted, not de-weighted.
  - The name stays. The four survivors are still invisible to Chromium.
- **`test_important_count_is_exactly_the_d2_certified_result`**: 50 → **43**. The
  ledger is 50 − 8 (the deleted block) + 1 (the fallback's `display: none !important`).
  The docstring records the ledger. The assertion stays exact in both directions.
- **`LIVE_GENERATION["scale-control-compact"]`**: 5 → **1**. All four removed
  occurrences were selectors inside the deleted block. The live rule
  `.scale-control-compact { display: flex; … }` is the one that remains. A comment
  records why. `scale-btn-compact` (6) and `scale-indicator` (2) do not change.

**New file `tests/test_ui_scale_capability_contracts.py`.** The name is tentative.
- No runtime `static/css/*.css` file contains `@-moz-document`.
- `accessibility.js` contains no `userAgent`, no `firefox` (case-insensitive) and no
  `removeProperty('zoom')`, and `applyScale` assigns
  `document.documentElement.style.zoom`.
- `a11y.css` contains exactly one `@supports not (zoom: 1)` block. Its only rule
  hides the two hooks with `display: none !important`. Neither hook appears anywhere
  else in `static/css/`, so no Chromium-applied rule can match it.
- In `base.html`, `data-scale-control-item` sits on the `<li>` that contains
  `.scale-control-compact`. `data-scale-control-divider` sits on exactly one divider,
  the one immediately after that `<li>`.
- The counter-zoom remains gated by `@supports (zoom: 1)` for both `#navbar` and
  `.modal`, in whatever form Phase A selects.

Every new or changed assertion gets a red-path proof, and each mutation is run in
both directions.

No edit to `tests/test_css_cascade_contracts.py` or
`tests/test_visual_selector_contracts.py` is planned. `scripts/css_audit/measure.py`
derives the WP4.4 baseline's contract anchors and pins only from those two files.
`test_wp4_4_baseline_is_pinned_and_matches_its_source_commit` measures the surfaces at
the baseline's own commit. Both are expected to stay green, and the full pytest run
confirms it.

**Artifacts**
| Path | Change | Notes |
|---|---|---|
| `static/js/accessibility.js` | modify | Remove the UA branch so the inline zoom is always written; fix the stale "Firefox doesn't support zoom" comments |
| `static/css/a11y.css` | modify | Delete the `@-moz-document` block; add the `@supports not (zoom: 1)` fallback (D2); fix the stale counter-zoom comment; navbar counter-zoom fix only if Phase A selects one |
| `static/css/components.css` | modify (conditional) | Modal counter-zoom fix only if Phase A selects one; otherwise untouched |
| `templates/base.html` | modify | Add `data-scale-control-item` to the scale `<li>` and `data-scale-control-divider` to the trailing divider; no other markup change |
| `tests/test_css_wp4_4_a11y_contracts.py` | modify | The three deliberate edits under Contract changes |
| `tests/test_ui_scale_capability_contracts.py` | new | The #607 capability and anti-exclusion contract |
| `docs/product/APP_FLOW.md` | modify | Scale row: capability-based behavior, tested Firefox build, no Safari claim |
| `docs/product/DESIGN_BRIEF.md` | modify | User-controlled-zoom paragraph: the same facts |
| `docs/test_inventory/TEST_INVENTORY.md`, `TEST_INVENTORY.json` | regenerate | Per-file pytest counts change (new file); regenerate with `scripts/generate_test_inventory.py`, never by hand |
| `docs/firefox_ui_scale/PLANNING.md` | this file | Plan of record; Plan v2 and the evidence summary pointer are added later |
| `artifacts/firefox_ui_scale/**` | uncommitted | Scratch runtime, disposable Firefox profiles, probe scripts, evidence (V-5) |

**Effort**: L · **Owner**: implementing agent under the coordinating session. The
Firefox acceptance phase needs a human operator (the owner) or approved OS/browser
automation that drives a real pointer in a headed browser. · **Depends on**: Gate 1
approval of Plan v2. The file set does not overlap the other session's files.

**Sequence**
1. **Branch.** Start from freshly fetched `origin/main` in the existing checkout,
   following the one-checkout rule (no worktree). Another session shares this
   checkout, so stage only this plan's paths and never use `git add -A`.
2. **Phase A0 — pre-change records.**
   - Run case C0 in Firefox on main.
   - Capture the Chromium "before" record for the invariance differential, with the
     same-CSS control: computed `zoom`, `width`, `height` and `max-width`, plus
     on-screen boxes, for `#navbar`, `.modal` and `.modal-dialog`, at levels 1, 4, 6
     and 8 and at the three visual viewports.
3. **Phase B — base change.**
   - In JS: remove the UA branch.
   - In CSS: delete the `@-moz-document` block, add the fallback, and fix the comments.
   - In `base.html`: add the two hooks.
   - Run `tests/test_css_wp4_4_a11y_contracts.py` and confirm it reds in exactly the
     three predicted places.
   - Make the three deliberate edits and add the new contract file, with red-path
     proofs.
4. **Phase A — diagnosis.** Run the diagnosis protocol on the Phase B build, for the
   navbar and then, separately, for the modal. Write `diagnosis.md`.
5. **Phase B2 — fixes.** For each element, apply the fix the decision rule selects,
   or none. If the rule selects nothing for an element that fails, **stop** and report
   to the owner.
6. **Chromium invariance differential.** Compare against the step 2 record, with the
   same-CSS control at zero differences. This is required whenever step 5 changed CSS.
   If step 5 changed nothing, it still runs once as a cheap confirmation.
7. **Phase C — Firefox acceptance.** Run cases C1–C7 per the protocol.
8. **Docs.** Update `APP_FLOW.md` and `DESIGN_BRIEF.md`, naming the exact tested
   build.
9. **Inventory.** Run `scripts/generate_test_inventory.py`, then `--check`. First
   confirm that no untracked `.md` sits in a globbed surface directory.
10. **Gates.** Run the gates listed below, then `/verify-and-polish`
    (`code-reviewer`, then `unslop-reviewer`).
11. **PR and dispatch.** Commit, open the PR, mark it ready, and **stop**. Do not
    merge. Merging needs the owner's explicit confirmation naming the PR.
    - Dispatch the approved Linux compare against the implementation commit:
      `gh workflow run deep-gate-visual.yml --ref <branch> -f visual_mode=compare`.
    - Confirm that the run's head SHA equals the implementation commit, and record the
      run ID.
    - Read the result under ADR-011: a green reached through retries is not a pass.
12. **Report.** Report to the owner with the PR, the evidence summary and the Linux
    run. The coordinator posts the owner-approved #607 correction wording.

**Expected gates** (to be confirmed by `test-strategist`)
- **pytest:** the full suite (shared-surface row), which includes
  `tests/test_css_wp4_4_a11y_contracts.py`, the new contract file,
  `tests/test_css_cascade_contracts.py`, `tests/test_visual_selector_contracts.py` and
  `tests/test_css_wp4_4_a_baseline_contracts.py`. The pyright baseline diff runs
  because a `.py` file is added; the new test file must add no net-new diagnostics.
- **e2e (Chromium):**
  - `smoke-navigation`, `nav-dropdown`, `accessibility`, `dark-mode`, `summary-pages`,
    `volume-progress`, `fatigue`, `fatigue-stage4-smokes` and `ui-hardening` (the
    shared-surface row). This set also covers the template row's `base` specs and the
    JS row's `accessibility` spec.
  - `e2e/accessibility.spec.ts` › "Native zoom and application scale" must pass
    **unmodified**.
- **Visual:**
  - the full `visual.spec.ts` matrix with `PW_VISUAL_SEED=1` on Windows. Any red must
    be shown to be pre-existing on a base rebased onto main, not attributed to this
    change;
  - the Linux `Deep Gate Visual (Linux)` compare dispatch against the implementation
    commit (owner-approved). No `generate` mode and no `--update-snapshots`.
- **Other:**
  - seven-surface Stylelint (`node scripts/css_audit/stylelint_surfaces.mjs`): no
    category may rise. If the ID-scoped fallback selector raises one, choose another
    selector shape before considering an owner exception;
  - `docs/test_inventory/` regenerated and `--check` green;
  - manual smoke: Firefox Phase C (above) plus a brief headed Chromium check of the
    control;
  - `/verify-and-polish` for the diff-time reviewers.
- **No Vitest by default.** `test-strategist` decides (RQ1). If Vitest is added, the
  inventory regeneration also covers it.

### Risks

| Risk | Mitigation |
|---|---|
| No engine-neutral counter-zoom fix exists for one element | The decision rule stops implementation and goes back to the owner; no partial ship, and no UA or `-moz-` gate |
| Exposing scale in Firefox surfaces other Firefox-only layout problems on routes not measured (popovers appended to `body`, toasts, charts) | Criterion 6 covers a fixed element, a dropdown and a form control; RQ3 proposes a cheap overflow sweep of all 11 routes at levels 1 and 8 |
| DOM geometry reads use different coordinate spaces in the two engines under zoom | Validate the oracle in Chromium first; decide on screenshot boxes (H4) |
| Native zoom pushes the viewport into the 1360–1500px band, hiding the control in every browser | V-2 window sizing; record `innerWidth` per case |
| Windows visual matrix carries seed-dependent or pre-existing reds | Run with `PW_VISUAL_SEED=1`; compare against a rebased main base; never regenerate |
| The fallback cannot be exercised at runtime on the tested build | C7 uses the `layout.css.zoom.enabled` preference if present; otherwise the claim is limited to the contract test and recorded as such |
| The owner-approved correction wording overstates today's divider hiding | C0 measures it; OQ2 lets the owner decide whether to amend the #607 comment |

### Open questions

**For the owner** (none blocks Plan v1 review):
- **OQ1.** Hide the control's item and only the **trailing** divider, leaving one
  separator between the signature and the muscle toggle (D3, proposed)? Or hide
  **both** flanking dividers, which is what today's block declares?
- **OQ2.** If C0 confirms that today's Firefox still renders the empty item and both
  dividers, the approved correction ("hides the scale control and its divider")
  overstates current behavior. Should the #607 comment be adjusted?
- **OQ3.** Should a short committed evidence summary
  (`docs/firefox_ui_scale/EVIDENCE.md`) accompany the PR? The alternative is the PR
  description and the #607 comment alone, with raw evidence under the gitignored
  `artifacts/`.

**For the reviewers:**
- **RQ1 (`test-strategist`).** Is a Vitest case for `applyScale`, which writes the
  inline zoom under a Firefox user-agent string, worth its cost over the source-shape
  pytest contract?
- **RQ2 (`architecture-reviewer`).** Are template data-attribute hooks (D2) acceptable,
  versus `:has()` selectors that would avoid the template edit but fail on Firefox
  ≤120?
- **RQ3 (`test-strategist`).** Keep or cut a light 11-route sweep at levels 1 and 8 in
  Firefox, reading horizontal overflow and checking by eye?
- **RQ4 (`architecture-reviewer`).** Should the #607 guarantees go in a new contract
  file, rather than extending the WP4.4 packet-owned file?
- **RQ5 (`product-risk-reviewer`).** Is a disabled `layout.css.zoom.enabled` preference
  acceptable evidence for criterion 8? And is the product-doc claim wording sound if
  that preference is absent?

---

## Agent provenance

*Required for every council run. The manager records each agent ID returned by its `Agent(...)` call and supplies the `product-manager` its own ID back, because an agent cannot know its own ID. The `product-manager` stamps the IDs the manager supplies — **never invent an ID**, never rerun completed council work to manufacture continuity, and record an unrecoverable ID as an evidence gap.*

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `a7864a1bd081b1065` | Author of Section 0 and Plan v1. |
| `product-manager` — response matrix + Plan v2 | `a7864a1bd081b1065` | Author of the matrix and Plan v2. |
| `architecture-reviewer` | `a76b409dff6120e6e` | Step 2 reviewer. |
| `test-strategist` | `a6057e78a14615c3d` | Step 2 reviewer. |
| `product-risk-reviewer` | `a89b499cb37a409f2` | Step 2 reviewer. |

**Same product-manager resumed for the matrix + Plan v2?** `yes` (resumed via `SendMessage` to the Plan v1 agent ID).

**Evidence gap** — `none` for agent IDs and continuity. The three reviewers' full
reports were not relayed to this `product-manager`. They live in the coordinating
session's transcript. The response matrix below condenses them as the coordinator
synthesized them.

---

## Reviewer findings

*Deviation from the template, recorded on purpose. The reviewers' outputs are not
pasted verbatim here. Their full reports live in the coordinating session's
transcript, and this `product-manager` received only the coordinator's synthesis.
Each section below records the verdict as the coordinator reported it, and the
individual findings appear in the response matrix. Nothing here is quoted from a
reviewer.*

### architecture-reviewer (agent `a76b409dff6120e6e`)
Verdict as reported: **needs revision**. Three should-fix findings (A-S1 to A-S3) and
notes (A-N4 to A-N7). No blockers.

### test-strategist (agent `a6057e78a14615c3d`)
Verdict as reported: **full gate; approve once S1–S4 are folded in**. Four should-fix
findings (T-S1 to T-S4), notes (T-N1 to T-N6), and answers to RQ1 and RQ3.

### product-risk-reviewer (agent `a89b499cb37a409f2`)
Verdict as reported: **respects invariants**. Two should-fix findings (P-S1, P-S2),
four notes (P-N1 to P-N4), and an answer to RQ5.

---

## Response matrix

*The coordinator proposed these dispositions (council Step 3), and they await the
owner at Gate 1. None is rejected or deferred, so no `MASTER_HANDOVER.local.md` note
is needed. "Noted" marks a finding that confirms the plan and needs no change.*

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| **A-S1.** Use one hook, not two: keep `data-scale-control-item` on the control's `<li>` (`base.html:190`); drop `data-scale-control-divider`; hide the trailing divider with `#navbar .nav-item[data-scale-control-item] + .nav-divider`, specificity (1,3,0). Two attributes can drift apart if the markup is reordered. | architecture-reviewer | accept | D2 v2: a two-selector fallback with one hook. The contract becomes "one hook, on the `<li>` that contains `.scale-control-compact`, followed by the divider". This settles the mechanics of OQ1 in favor of the trailing divider. |
| **A-S2.** List and update every docstring, comment and assertion message in `tests/test_css_wp4_4_a11y_contracts.py` that cites 50, 12, 8 or the block: the module docstring at lines 8–11, the comment at line 78, the `test_chromium_invisible_annotations…` docstring at line 339, and the `test_important_count…` docstring and assertion message at lines 246–249. Record that the #607 ledger replaces d2's. | architecture-reviewer | accept | Contract changes v2 lists each place, and all are edited together. |
| **A-S3.** The final `!important` pin comes after B2. The step-3 pin is provisional and is recomputed and re-proved after step 5. A B2 fix adds no `!important` unless the ledger is re-justified, and the step-5 evidence records any it introduces. | architecture-reviewer | accept (merged with T-S4) | Sequence v2, steps 3 and 5; Contract changes v2. |
| **A-N4.** The anti-exclusion contract is weakly shaped. Strip comments and assert on code: no `navigator.*` read in `applyScale`, and no conditional around the zoom assignment. | architecture-reviewer | accept (merged with T-S2) | Contract changes v2, assertion (b). |
| **A-N5.** Update the stale `a11y.css` comments (lines 80, 83, 90–91). Add `docs/CSS_OWNERSHIP_MAP.md:30` ("Firefox fallbacks") to the artifacts, reworded to describe a capability fallback. | architecture-reviewer | accept (with T-N3) | Artifacts v2; Sequence v2, steps 3 and 8. |
| **A-N6.** The fallback and the HTML inline zoom are complements, and the `--ui-scale` write is safe to delete. | architecture-reviewer | noted | No change; confirms D1. |
| **A-N6b.** `.modal-backdrop` is hidden under zoom (`components.css:2394-2403`). Check page interaction behind an open modal in Firefox. | architecture-reviewer | accept | Case C2 v2 records, with real pointer input, whether page content behind an open modal is reachable, compared with Chromium, and flags any difference. The backdrop behavior is not changed. |
| **A-N7.** `APP_FLOW.md:210` is the only product-doc Firefox statement; the other docs stay as history. | architecture-reviewer | noted | No change. |
| **T-S1.** The Chromium spec list misses the `QUALITY_GATE.md:150` row. Add `validation-boundary`, `error-handling` and `empty-states`, and correct the "also covers" sentence. Add `workout-plan.spec.ts` if `components.css` (`#generatePlanModal`) changes. | test-strategist | accept | Expected gates v2. |
| **T-S2.** Assert on the body of `applyScale`: no `navigator`, `CSS.supports` or `removeProperty`; exactly one `document.documentElement.style.zoom = zoomValue`; no `if`, ternary or `&&` guards it. Run the `firefox` and `userAgent` scans on comment-stripped source, reusing the existing stripper. | test-strategist | accept | Contract changes v2, assertion (b). |
| **T-S3.** Anchor the hook assertions with `(?![\w-])` and run mutations in both directions. | test-strategist | accept (adapted to the single hook from A-S1) | Contract changes v2 mutation list: rename the hook in the CSS only; rename it in the template only; move the hook to the wrong `<li>`; move the divider so it is no longer the immediate next sibling. |
| **T-S4.** The counter-zoom assertion and the `!important` ledger depend on the diagnosis. Write the counter-zoom assertion in step 5; the ledger is "50 − 8 + 1, plus any B2 delta". | test-strategist | accept (merged with A-S3) | Sequence v2, step 5; Contract changes v2. |
| **T-N1, T-N2.** The cascade claim and the "exactly three reds" prediction check out. A fourth red is new information. | test-strategist | noted | Prediction kept. Sequence v2, step 3: a fourth red stops the step for investigation. |
| **T-N3.** The `CSS_OWNERSHIP_MAP` row. | test-strategist | accept | See A-N5. |
| **T-N4.** Regenerate the inventory only on the clean #607 branch from `origin/main`, never on the #715 tree. | test-strategist | accept | Sequence v2, steps 1 and 9 state it explicitly. |
| **T-N5.** Tests stay Chromium-only by design. The e2e at `accessibility.spec.ts:741-773` becomes the committed proof of the single path. | test-strategist | noted | No change; cited in D7 v2. |
| **T-N6.** The known red at `program-backup.spec.ts:79` is outside this gate set. If a full run includes it, record whether it passes in isolation. | test-strategist | accept (note) | Expected gates v2. |
| **RQ1.** No Vitest. | test-strategist | accept | D7 v2. |
| **RQ3.** Keep the 11-route sweep as a diagnostic, differential case C8 (detail in Plan v2), outside the committed suite. | test-strategist | accept | Case C8 v2. |
| **P-S1.** C7 can pass for the wrong reason, because the item is also hidden below 992px and from 1360 to 1500px. Fix C7's viewport at 1920. Add a control run in the same profile: with the hook removed in DevTools, the control reappears with zoom off; with the hook present, it stays hidden. Confirm `CSS.supports('zoom','1')` is false. | product-risk-reviewer | accept (single hook, per A-S1) | Case C7 v2. |
| **P-S2.** Write migration notes in the PR, as the refactor invariant requires: in Firefox the control becomes visible; stored `ui-scale-level` values (cookie or localStorage, including old ones) now take effect; the reset is the existing −/+ buttons; nothing migrates server-side. Add a Phase C check on a fresh profile with a seeded level-8 cookie: the page scales at first paint. | product-risk-reviewer | accept | Migration notes v2; case C9 v2. |
| **P-N1.** Product docs say "validated on Firefox <version> on <date>; other releases not verified". The exact build ID and the evidence table go in the PR and the #607 comment, not in the docs. | product-risk-reviewer | accept (implementation guidance only) | Doc wording rules v2. Criterion 9's approved text is not edited. |
| **P-N2.** The docs say the control is "subject to the existing responsive visibility". | product-risk-reviewer | accept | Doc wording rules v2. |
| **P-N3.** "UI scale", "text size" and "application scale" are used inconsistently. Pick one name for the new doc text and note the inconsistency in the PR; do not fix it here. | product-risk-reviewer | accept | Doc wording rules v2 use "application scale". Migration notes v2 record the inconsistency. |
| **P-N4.** D3 and the single remaining divider hold up. | product-risk-reviewer | noted | No change. |
| **RQ5.** The disabled preference is evidence of the fallback wiring only, not of real browsers without zoom. If the preference is absent, the docs say the fallback "is guarded by a source-shape test and was not exercised at runtime". | product-risk-reviewer | accept | Case C7 v2; doc wording rules v2. |

RQ2 (hooks versus `:has()`) is settled by A-S1: one attribute hook plus a sibling
combinator, still with no `:has()`. The coordinator's synthesis recorded no finding
on RQ4, so the v1 choice (a new contract file) stands.

---

## Plan v2

*Plan v2 restates Plan v1 with the accepted findings applied. Wherever a part is
marked "unchanged from v1", the Plan v1 text above is adopted by reference, word for
word. Everything else here replaces the corresponding v1 part.*

**Goal**: unchanged from v1.

**Scope**
- **In**: as v1, with three changes:
  - the fallback uses **one** markup hook (`data-scale-control-item`) instead of two;
  - `docs/CSS_OWNERSHIP_MAP.md` gets a wording update (A-N5);
  - the PR carries migration notes (P-S2).
- **Out**: unchanged from v1. Also out: changing `.modal-backdrop` behavior, even if
  the C2 reachability check finds a difference between the engines (A-N6b). A
  difference is reported, not fixed.

### Key decisions (v2)

**D1. Capability detection runs in CSS, not JS.** Unchanged from v1.

**D2 (revised, A-S1). One hook, plus a sibling combinator.** `base.html` gains
`data-scale-control-item` on the `<li>` that contains `.scale-control-compact`
(line 190), and nothing else. The fallback in `a11y.css` is:

```css
@supports not (zoom: 1) {
    #navbar .nav-item[data-scale-control-item],
    #navbar .nav-item[data-scale-control-item] + .nav-divider {
        display: none !important;
    }
}
```

The two selectors have specificity (1,2,0) and (1,3,0). Both beat `navbar.css`'s
(1,1,0) `#navbar .nav-item { display: flex !important; }`. The leading divider stays
visible, so one separator remains between the signature and the muscle-mode toggle.
One attribute cannot drift apart from a second one when the markup is reordered. The
rule still uses no `:has()`, so it works wherever `@supports not` does. Chromium never
applies it.

**D3. "Its associated divider" means the trailing divider.** Unchanged from v1. A-S1
supplies the mechanics; the owner confirms at Gate 1 (OQ1).

**D4. Diagnose the navbar and the modal separately before any fix.** Unchanged from
v1.

**D5. Replace the contract deliberately and keep its unrelated guarantees.** Unchanged
in intent. The details are revised under Contract changes v2.

**D6. Chromium invariance by construction, plus measurement.** Unchanged from v1. The
single hook matches no Chromium-applied rule.

**D7 (new, RQ1 and T-N5). No Vitest.** After the change, `applyScale` has one
unconditional path. The body-shape contract (assertion (b) below) pins that shape. The
existing Chromium e2e at `e2e/accessibility.spec.ts:741-773` executes that single path
and is its committed runtime proof. A jsdom case driven by a user-agent string would
test an input that no longer influences the code.

### Diagnosis protocol (Phase A)

Unchanged from v1: the oracle validation, the navbar and modal measurement lists, the
hypotheses H0–H4, the candidate fixes, and the decision rule, including the stop.
Accepted findings add two constraints:
- an adopted fix adds no `!important` unless the ledger is re-justified in the step-5
  evidence (A-S3);
- if a modal fix changes `components.css`, `workout-plan.spec.ts` joins the gates
  (T-S1).

### Firefox verification protocol (Phase C)

V-1 (environment), V-2 (viewport), V-3 (case reset) and V-5 (evidence location) are
unchanged from v1. In V-4, cases C0, C1 and C3–C6 are unchanged. C2 and C7 are revised,
and C8 and C9 are new:

| Case | Native zoom | Levels | Route | Checks | Criteria |
|---|---|---|---|---|---|
| C2 (revised) | 100% | 1, 4, 8 | `/workout_plan` | As v1. **Add (A-N6b):** with `#generatePlanModal` open at levels 1 and 8, click a visible main-content control outside the dialog with real pointer input. Record whether it reacts and whether the modal stays open. Do the same in Chromium, and flag any difference. Do not change the backdrop. | 2, 3, 4 |
| C7 (revised, P-S1 and RQ5) | 100% | — | `/` | The window is **fixed at 1920**, with `innerWidth` recorded, so neither `navbar.css` band can hide the item. Use a second disposable profile with `layout.css.zoom.enabled` = `false`. (1) Confirm `CSS.supports('zoom', '1')` is `false`. (2) With the hook present, the control's item and the trailing divider are hidden and the leading divider is visible. (3) Control run in the same profile: remove `data-scale-control-item` in the DevTools Inspector; the control and the trailing divider reappear. (4) Restore the hook; both are hidden again. This is evidence of the fallback's wiring only, not of real browsers without zoom. If the tested build lacks the preference, record that, and the docs use the RQ5 wording. | 8 |
| C8 (new, RQ3; diagnostic, not acceptance) | 100% | 6, 1, 8 | The 11 pages in `e2e/visual.spec.ts`'s page list, through `ROUTES`: welcome, workout-plan, workout-log, weekly-summary, session-summary, progression, body-composition, volume-splitter, user-profile, backup, fatigue | Validate the oracle in Chromium first. At window widths 1920 and 1280, read `documentElement.scrollWidth − clientWidth` in Firefox and in Chromium. Compare Firefox with its own level 6 and with Chromium at the same level. Levels may be set by cookie and localStorage plus reload, recorded as such. Take a screenshot of any route that flags. **Stopping rule:** a Firefox delta more than 1 CSS px above Chromium's is reported, attributed to an element through the screenshot and DevTools. It blocks only if the element is in the navbar or a modal. The sweep stays outside the committed suite. | — |
| C9 (new, P-S2) | 100% | 8 | `/workout_plan` | Fresh disposable profile. Seed `ui-scale-level` = `8` in localStorage and the cookie through the DevTools storage panel; this seeds state, not activation. Reload. Expected: first paint is already scaled (inline zoom `1.2`, `data-scale="8"`) and the indicator shows `8`. **Cookie-only variant, observation only:** seed the cookie alone, and record the rendered zoom, the indicator and the cookie after load, in Firefox and in Chromium (see the PM note under Risks). | 5 |

### Contract changes v2

**`tests/test_css_wp4_4_a11y_contracts.py`.** The assertion edits are as v1, with
revised numbers:
- **`test_chromium_invisible_annotations_were_not_removed`.** Drop the
  `@-moz-document` half and keep the four annotated `-moz-box-shadow` declarations.
  The name stays.
- **`test_important_count_is_exactly_the_d2_certified_result`.**
  - In step 3 the pin is **provisional**: 50 − 8 + 1 = **43**.
  - In step 5 the final pin is recomputed as **50 − 8 + 1 + any B2 delta** and its red
    paths are proved again (A-S3, T-S4).
  - A B2 fix adds no `!important` unless the ledger is re-justified in the step-5
    evidence.
- **`LIVE_GENERATION["scale-control-compact"]`**: 5 → **1**, as v1.

**Every text that cites the old numbers or the block is updated in the same edit**
(A-S2):
- the module docstring, lines 8–11 ("RETAINED the other 50");
- the comment above `LIVE_GENERATION`, line 78;
- the `test_chromium_invisible_annotations_were_not_removed` docstring, from line 339;
- the `test_important_count_is_exactly_the_d2_certified_result` docstring and its
  assertion message, lines 246–249.

Each records that the #607 ledger replaces d2's: d2 certified 50, and #607 deleted the
8 annotations in the `@-moz-document` block and added the fallback's annotation, by
owner decision at Gate 0 on 2026-11-18. Every other test and constant in the file is
unchanged.

**New file `tests/test_ui_scale_capability_contracts.py`.** The name is tentative.
- **(a)** No runtime `static/css/*.css` file contains `@-moz-document`.
- **(b) (T-S2 and A-N4).**
  - All scans of `accessibility.js` run on comment-stripped source. Reuse the
    existing length-preserving stripper, extended to blank `//` line comments.
  - The whole file contains no `firefox` (case-insensitive) and no `userAgent`.
  - Extract the `applyScale` function body. It contains no `navigator`, no
    `CSS.supports` and no `removeProperty`. It holds exactly one
    `document.documentElement.style.zoom = zoomValue`, and no `if`, ternary,
    `&&` or `||` guards that assignment.
- **(c)** `a11y.css` contains exactly one `@supports not (zoom: 1)` block. Its only
  rule is the two-selector list from D2 v2, with `display: none !important`. Outside
  that block, `data-scale-control-item` appears nowhere in `static/css/`. All hook
  matches are anchored with `(?![\w-])`.
- **(d)** `base.html` contains exactly one `data-scale-control-item` (anchored),
  located on the `<li>` that contains `.scale-control-compact`. That `<li>`'s
  immediate next sibling `<li>` carries `nav-divider`.
- **(e)** The counter-zoom remains gated by `@supports (zoom: 1)` for `#navbar` and
  `.modal`. This assertion is **written in step 5**, so it matches the form the
  diagnosis selects (T-S4).

**Mutations.** Each is run in both directions: the mutation must turn the test red,
and reverting it must turn the test green.
- Rename the hook in the CSS only.
- Rename the hook in the template only.
- Move the hook to the wrong `<li>`.
- Move the divider so it is no longer the immediate next sibling.
- Wrap the zoom assignment in an `if`.
- Add a `navigator.userAgent` read inside `applyScale`.
- Add the word `firefox` in a comment. This must stay **green**, which proves the
  comment stripping.
- For every changed count in the WP4.4 file: one more and one fewer.

The shared files `tests/test_css_cascade_contracts.py` and
`tests/test_visual_selector_contracts.py` are still not edited, for the reason given
in v1.

**Artifacts**
| Path | Change | Notes |
|---|---|---|
| `static/js/accessibility.js` | modify | Remove the UA branch; the inline zoom is always written; fix the stale comments |
| `static/css/a11y.css` | modify | Delete the `@-moz-document` block (its comment at lines 90–91 goes with it); add the D2 v2 fallback; reword the stale counter-zoom comments at lines 80 and 83; navbar fix only if Phase A selects one |
| `static/css/components.css` | modify (conditional) | Modal fix only if Phase A selects one |
| `templates/base.html` | modify | Add `data-scale-control-item` to the scale `<li>` only |
| `tests/test_css_wp4_4_a11y_contracts.py` | modify | Contract changes v2, including every A-S2 text |
| `tests/test_ui_scale_capability_contracts.py` | new | Assertions (a)–(e) |
| `docs/product/APP_FLOW.md` | modify | Scale row (doc wording rules below) |
| `docs/product/DESIGN_BRIEF.md` | modify | User-controlled-zoom paragraph (doc wording rules below) |
| `docs/CSS_OWNERSHIP_MAP.md` | modify | Line 30: "Firefox fallbacks" becomes a capability-fallback description (A-N5) |
| `docs/test_inventory/TEST_INVENTORY.md`, `TEST_INVENTORY.json` | regenerate | On the clean #607 branch only (T-N4) |
| `docs/firefox_ui_scale/PLANNING.md` | this file | Plan of record |
| `artifacts/firefox_ui_scale/**` | uncommitted | Scratch runtime, disposable profiles, probes, evidence |

**Effort**: L, unchanged. **Owner**: unchanged. **Depends on**: owner approval of this
Plan v2 (Gate 1).

**Sequence**
1. **Branch.** As v1: fetched `origin/main`, the existing checkout, path-scoped staging.
   The #607 branch is clean, started from `origin/main`. Nothing from the #715 tree is
   present on it (T-N4).
2. **Phase A0.** Unchanged from v1 (case C0; the Chromium "before" record with the
   same-CSS control).
3. **Phase B — base change.**
   - Make the JS change. Make the CSS change: delete the block, add the D2 v2
     fallback, and reword the comments at lines 80 and 83. Add the single template
     hook.
   - Run `tests/test_css_wp4_4_a11y_contracts.py`. It must red in **exactly** the three
     predicted places. A fourth red is new information: stop and investigate it before
     going on (T-N2).
   - Apply the WP4.4 edits, with every A-S2 text and the **provisional** 43 pin.
   - Add the new contract file with assertions (a)–(d) and their mutations.
4. **Phase A — diagnosis.** Unchanged from v1: the navbar, then the modal, separately.
5. **Phase B2 — fixes and final pins.**
   - Apply the fix the decision rule selects for each element, or none, or stop.
   - Then write assertion (e) to match the selected form.
   - Recompute the `!important` pin as 50 − 8 + 1 + any B2 delta, record any
     `!important` the fix introduced and its justification, and prove the red paths
     again.
6. **Chromium invariance differential.** Unchanged from v1.
7. **Phase C — Firefox acceptance.** Cases C1–C7 and C9, plus the diagnostic sweep C8.
8. **Docs.** Update `APP_FLOW.md`, `DESIGN_BRIEF.md` and `CSS_OWNERSHIP_MAP.md` under
   the doc wording rules below.
9. **Inventory.** Run `scripts/generate_test_inventory.py`, then `--check`, on the
   clean #607 branch only.
10. **Gates.** Run the gates below, then `/verify-and-polish`.
11. **PR and dispatch.** As v1, and add the migration notes and the naming note to the
    PR description. Mark the PR ready and stop; there is no merge without the owner's
    explicit confirmation naming the PR. The Linux compare dispatch against the
    implementation commit is unchanged from v1.
12. **Report.** As v1. If C0 shows the empty item or the dividers visible today, the
    owner decides on an OQ2 follow-up.

**Doc wording rules** (P-N1, P-N2, P-N3, RQ5). These are implementation guidance;
criterion 9's approved text is unchanged.
- Use the name "application scale" in all new doc text.
- State the behavior as capability-based. Where the browser supports CSS `zoom`, the
  control is shown, "subject to the existing responsive visibility". Where it does
  not, the control and its divider are hidden.
- State validation as "validated on Firefox <version> on <date>; other releases not
  verified". Make no Safari claim.
- If C7 could not run, add that the fallback "is guarded by a source-shape test and
  was not exercised at runtime".
- The exact build ID and the evidence table go in the PR description and the #607
  comment, not in the docs.

**Migration notes for the PR description** (P-S2, as the refactor invariant requires):
- In Firefox builds that support CSS `zoom`, the application-scale control becomes
  visible, subject to the existing responsive visibility.
- Stored `ui-scale-level` values now take effect in those builds. That includes
  values already in the cookie or localStorage, including old ones.
- The reset path is the existing −/+ buttons.
- Nothing migrates server-side. Schema, API, mapping, keys and the cookie are
  unchanged.
- Chromium and Edge behavior is unchanged (criterion 10).
- The names "UI scale", "text size" and "application scale" are used inconsistently
  across the markup and the docs. This PR uses "application scale" in new text and
  does not rename anything else (P-N3).

**Expected gates (v2)**
- **pytest:** unchanged from v1. This includes the pyright baseline diff for the new
  `.py` file.
- **e2e (Chromium):**
  - From the shared-surface row: `smoke-navigation`, `nav-dropdown`, `accessibility`,
    `dark-mode`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`
    and `ui-hardening`.
  - From the `QUALITY_GATE.md` feature-map row for accessibility changes, which
    `accessibility.js` reaches: also `validation-boundary`, `error-handling` and
    `empty-states` (T-S1).
  - The template row's `base` specs (`smoke-navigation`, `nav-dropdown`, `dark-mode`)
    are already in the shared-surface set. The JS row's accessibility mapping is what
    adds the three specs above. This corrects v1's "also covers" sentence.
  - Add `workout-plan.spec.ts` if `components.css` changes (T-S1).
  - `e2e/accessibility.spec.ts` › "Native zoom and application scale" passes
    **unmodified**.
  - The known historical red at `e2e/program-backup.spec.ts:79` is outside this gate
    set. If a full run includes it, record whether it passes in isolation (T-N6).
- **Visual:** unchanged from v1 (the Windows matrix with `PW_VISUAL_SEED=1`, and the
  approved Linux compare dispatch). No `generate` mode and no `--update-snapshots`.
- **Other:** unchanged from v1 (seven-surface Stylelint with no category rising, the
  inventory `--check`, the manual smokes, `/verify-and-polish`). No Vitest (D7).

### Risks (v2)

The v1 risks are unchanged. The fallback-runtime risk is narrowed: C7 v2 adds the
fixed viewport and the hook-removal control. One PM note is added.

**PM note (source reading, raised while writing v2; not a reviewer finding).**
`AccessibilityController.init` reads the level from localStorage only, defaulting to
6. `syncCookie` then overwrites a different cookie. A profile with a level-8 cookie and
no localStorage entry is therefore rendered by the server at level 8 (inline zoom
`1.2`). After load, the cookie is rewritten to `6` and the indicator shows `6`, while
the page stays at `1.2` until the next scale action. This is pre-existing behavior in
every browser and is not introduced by #607. Changing it would move the persistence
contract that criterion 12 freezes. C9's cookie-only variant records it in both
engines, and the PR migration notes mention it if C9 confirms it. Any fix needs a
separate owner decision.

### Open questions for Gate 1

**Owner dispositions, approved 2026-11-18:**
- **OQ1. Hide only the trailing divider.** Recommended. It matches the owner's
  singular "its associated divider" and the A-S1 structure.
- **OQ2. Post a follow-up if C0 contradicts the correction.** If C0 shows that today's
  Firefox block leaves the empty item or the dividers visible, post a short factual
  follow-up on #607 with owner-approved text. Do not change the approved correction
  retroactively. Recommended.
- **OQ3. No committed evidence summary.** The PR description and a #607 comment are
  enough, with the raw evidence under `artifacts/`. Recommended.

The owner also approved checking rendered geometry before `accessibility.js`
initializes in C4 and C9. Temporarily delay the script in the disposable profile
and measure computed zoom or geometry before releasing it, then confirm a normal
navigation or reload.

**For the reviewers:** none open. RQ1, RQ3 and RQ5 are answered in the response
matrix, RQ2 is settled by A-S1, and RQ4 keeps the v1 choice.

---

## Sign-off

- [x] Gate 0 complete when required by planning size; otherwise marked not applicable. — owner, 2026-11-18
- [x] Every finding has a disposition. — dispositions proposed by the coordinator, 2026-11-18; the owner confirms them at Gate 1
- [x] Agent provenance complete — both `product-manager` IDs, same-PM-resumed yes/no, the three reviewer IDs, and an evidence-gap line (or `none`).
- [x] Owner approved Plan v2 (Gate 1) and the dispositions above on 2026-11-18.
- [x] Ready to implement. Run the diff-time gate after code.
