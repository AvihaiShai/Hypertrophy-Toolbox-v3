# Plan Review — Mobile menu panel (#733)

**Status** — Gate 0 approved by the owner on 19 November 2026 (assumptions A1-A5 accepted as written). Council review is complete (three reviewers: sound with advisories, no blocking finding). The owner approved Gate 1 directly on 19 November 2026 with one D5 amendment (see "Gate 1 owner approval and amendment"). Implementation is authorized under that approved scope. Merge needs the owner's separate confirmation naming the PR.

## Section 0 — Requirements Brief

**Planning size**: Large. The fix edits the shared CSS surface `static/css/navbar.css`
(`QUALITY_GATE.md`, "CSS (static bundles)" row). Gate 0 + Gate 1.

**Raw request** (verbatim)

> https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/733
> handle this item until it get done end to end complelety using multiple agents in order to work quicker ( use smaller models for the agents in order to work effectively - use the bigger models  only when needed)
>
> in case decisions are blocking this item, span the ai consulting team to decide and uplift the blocker.

**Problem**

[Issue #733](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/733) ("Navbar: mobile menu panel clipped to header height, and related mobile-menu defects", observed on `main` at `6ad06a7d`, Chromium, 375px) reports four defects:

1. The open mobile menu panel (`#navbarNav`) renders about 63px tall for about 291px of content, so only "Plan" is visible, in both themes. The issue's stated cause is that `#navbar` has `backdrop-filter`, which makes it the containing block of the panel's `position: fixed; inset: 0; top: var(--nav-height)`. `e2e/nav-dropdown.spec.ts` passes because `toBeVisible()` does not detect overflow clipping. The owner's 19 Nov comment confirms the panel is still 62px tall at 375px dark on the PR #740 build.
2. Clicking empty space inside the open panel reopens it. The overlay-click handler in `static/js/modules/navbar-enhancements.js` calls `closeMobileMenu()` and then `mobileMenuToggle.click()`, which Bootstrap treats as an open request. The menu flickers and stays open with the scroll lock re-applied. The handler's comment states the intent to close.
3. After the window is widened past 992px with the menu open, the menu closes but the focus-trap `keydown` listeners stay attached and `isMenuOpen` is never reset. Tab then wraps from the last navbar control to "Plan" instead of moving into the page. Escape clears it.
4. Hard-coded `aria-current="page"` on the brand link. **Not part of this work**: PR #740 already fixes it (see Out of scope).

The issue also states that the #575 AUD-0418 `navbar.css` comment correction ("Navbar comments still misdescribe the live unlayered fixed-position owner") is held for this batch.

**Acceptance criteria**

1. Given a hamburger-layout viewport (375px), when the menu is opened, then every primary link and the right-hand controls are reachable: fully visible, or scrollable within the area between the header and the viewport bottom. The panel is not clipped to the header height. This holds in light and dark themes and with the header in its normal and compact (scrolled) states.
2. Given the menu is open, when the user clicks empty space inside the panel, then the menu closes and stays closed, page scroll is unlocked, the toggler reports `aria-expanded="false"`, and focus returns to the toggler. ⚠️ see assumption A1.
3. Given the menu is open, when the viewport is widened out of the hamburger layout, then the menu is closed, scroll lock and any overlay are released, and pressing Tab from the last navbar control moves focus into the page without pressing Escape. Reopening the menu afterwards still traps focus and Escape still closes it.
4. Given the closed header, or any desktop-layout viewport, when pages render and the desktop navigation and hover dropdowns are used, then appearance and behaviour are unchanged. The only visual change is the open mobile panel.
5. Given the regression suite, when the pre-fix code is run against it, then tests fail for each of defects 1-3. Defect 1 is asserted by geometry (panel height and content reachability), not by `toBeVisible()`.
6. Given the batch lands, then the #575 AUD-0418 `navbar.css` comment correction is included, and the comments describe the live fixed-position owner accurately.

**Calculation surface**

- `none`. No calculation, schema or API response shape is involved. The PR still carries migration notes on the changed navbar behaviour and the regression coverage above.

**In scope**

- Defects 1-3 of #733 and the AUD-0418 comment correction in `static/css/navbar.css`.
- Defining the single width at which the navbar leaves the hamburger layout, so the resize close (defect 3) and the CSS agree (see Facts).
- Regression tests per criterion 5, including affected existing navbar contract tests and the test inventory.

**Out of scope / non-goals**

- Defect 4 and everything else in #736 / PR #740 (brand name on phones, design step 1).
- The duplicate navbar initialisation recorded under #634.
- Any redesign of the menu or its contents.
- Desktop hover dropdown behaviour.
- Regenerating visual baselines without the owner's by-eye sign-off.

**Facts recorded for planning (not decisions)**

- Hamburger layout exists in two CSS bands: the max-width phone/tablet band (near `navbar.css` lines 696-760) and `@media (min-width: 992px) and (max-width: 1359.98px)` (near line 1250). The JS `handleResize()` closes the open menu when `window.innerWidth > 992`, so the menu closes while the hamburger layout is still in effect between 992px and 1359.98px.
- `handleResize()` removes `.show`, resets `aria-expanded` and unlocks scroll, but does not set `isMenuOpen = false` or remove the two `keydown` listeners (added at lines 159-160).
- `#navbar` has `backdrop-filter: blur(20px) saturate(180%) !important` and `isolation: isolate !important` (lines 908-935).
- PR #740 (branch `fix/736-design-step-one`, unmerged, awaiting the owner's by-eye visual-baseline decision) touches the same files: `static/css/navbar.css`, `templates/base.html`, `e2e/nav-dropdown.spec.ts`, `tests/test_css_wp4_4_navbar_contracts.py`. Branch base and merge order are therefore an open plan-stage decision. Committed visual baselines currently represent the pre-#740 design.
- The working branch is `fix/733-mobile-menu-panel`, created from `origin/main` at `8884ec51` on 19 November 2026, independent of unmerged PR #740. The base choice remains open to council review in the plan.

**Assumptions made** (accepted by the owner as written, 19 November 2026)

- ⚠️ A1. Clicking empty panel space should close the menu (the code's stated intent), rather than being ignored.
- ⚠️ A2. Aligning the resize-close threshold with the CSS hamburger breakpoint (1359.98px) is in scope, because the repair of defect 3 must define when the menu leaves the hamburger layout.
- ⚠️ A3. "Calculation surface: none" and "Large" planning size, as stated above.
- ⚠️ A4. Defect 4 is treated as delivered by PR #740 and out of this work. If #740 is abandoned, it would need re-scoping.
- ⚠️ A5. Verification is Chromium at 375px plus a widening resize, in light and dark themes; no other browsers or devices are required.

**Open questions for the user**

- none open.

**Answered questions**

- **Q1 (delegation) — answered by the owner, 19 November 2026**, through a selection prompt. Selected answer, verbatim: **"Gate 1 stays direct"** — option text: "The team decides technical choices only; stop and show me Plan v2 for my own Gate 1 approval before any implementation." Merge also stays the owner's explicit confirmation naming the PR.

**Owner Gate 0 decision — 19 November 2026**

The Gate 0 prompt listed the six criteria and stated that clicking empty panel space closes the menu, that the close threshold is aligned with the real hamburger breakpoint (1360px) instead of 992px, and that item 4 stays with PR #740. Selected answer, verbatim: **"Approve all (Recommended)"** — option text: "I approve Gate 0: the six acceptance criteria and assumptions A1-A5 as written."

### Section 0 sign-off — GATE 0

- [x] User confirms the acceptance criteria match intent (owner selected "Approve all (Recommended)", 19 November 2026).
- [x] User reviewed the assumptions and corrected or accepted each one (A1-A5 accepted as written).
- [x] Blocking questions are answered (Q1: "Gate 1 stays direct").

---

## Measured diagnosis (19 Nov 2026)

*Browser measurements below come from a read-only senior-developer agent on the real app at `8884ec51` (Chromium via Playwright MCP, nothing edited on disk); the product-manager did not re-measure them. Source line numbers were re-read by the product-manager the same day.*

**Defect 1 — clipped panel.** At 375x812 in both themes the open `#navbarNav` computes `position: fixed; top: 64px; bottom: 0; height: 63px; overflow-y: auto` (`scrollHeight` 291, `clientHeight` 62). Nine of 13 controls are not visible-and-hittable (Plan, Log, Analyze, Progress, Profile, Body Composition, Distribute, Backup, `#darkModeToggle`).

- Cause, by one-at-a-time style injection: `#navbar`'s `backdrop-filter` makes the header the containing block of the fixed panel, and the unlayered `#navbar .navbar-collapse { height: 100% !important }` (`navbar.css` 969-973) resolves against the 64px header. With header blur off alone the panel becomes 812px tall and overflows the viewport by 64px. With `height: calc(100dvh - var(--nav-height)) !important` on the panel alone the panel is top 64 / height 748 / bottom 812 with every control reachable, identical with the header blur on or off. A viewport-derived panel height is therefore correct in both containing-block states and `#navbar` itself need not change.
- Where each band sits (source): the phone band `@media (max-width: 991.98px)` (694-733) lies **inside** `@layer navbar` (opens line 6, closes 883) and sets no height. The 992-1359.98px band (1264-1292) lies **after** the layer closes and already sets `height: calc(100vh - var(--nav-height, 64px)) !important; max-height: none !important; inset: 0`, which wins over 969-973 on specificity (1,2,1 vs 1,1,0); it measured full height with no failing controls. Compact (`.nb-compact`, 56px) header: `--nav-height` stays 64px; the phone band has a compact `top` rule (731-733), the tablet band has none, so at 1100x900 compact the panel top is 64 while the header bottom is 56 (pre-existing 8px gap).
- Cascade trap: a layered `!important` beats an unlayered `!important` regardless of specificity. An unlayered `#navbar { backdrop-filter: none !important }` injection had no effect. The comment at 901-904 ("MUST be outside @layer for highest specificity") is misleading. Any new declaration's winner must be confirmed by computed style.
- A candidate injected at runtime passed at 375x812, 768x1024 and 1100x900, light and dark, normal and compact, with and without header blur (panel top = header bottom, panel bottom = viewport bottom; at 375x500 the panel scrolled with every control reachable). It is evidence that a panel-scoped fix exists, not the mandated CSS.
- **Transparent panel (new finding).** `#navbarNav` computes `background-color: rgba(0,0,0,0)` in both themes. The unlayered `#navbar .navbar-collapse { background: transparent !important }` (969-973) defeats the band backgrounds (714 `rgba(255,255,255,.92)`, 728 `rgba(11,13,18,.95)`, 1278/1295/1475 `color-mix(surface-2 88%)`), all non-`!important`. The panel's own `backdrop-filter` blurs nothing because the header is already a backdrop root, so page text shows through unblurred behind the links (at 375 dark; already true today at 1100px). It becomes obvious once the panel is full height.
- Scroll lock holds (`body.style.overflow: hidden`; wheel leaves `scrollY` 0); panel `z-index` 999. Observation only, out of scope: the visual harness's `*{backdrop-filter:none!important}` (`e2e/visual-helpers.ts` ~130-140) does not remove `#navbar`'s blur in real Chromium for the same layered-important reason.

**Defect 2 — reopen on empty-space click.** A real click on `#navbarNav` itself: immediately `.show` false, `aria-expanded` false, body overflow "", focus on toggler; after 600ms `.show` true, `aria-expanded` true, body overflow hidden, `MAIN#main-content` inert, focus on Plan. Source (`navbar-enhancements.js` 188-194): the handler calls `closeMobileMenu()`, which removes `.show` by hand, then `mobileMenuToggle.click()`, which Bootstrap treats as open. On `main` the only empty target is a 4px strip; with a full-height panel the empty area is large. `initializeNavbarEnhancements()` runs twice per page (#634 AUD-0845, not fixed here), so every handler, and each closure's own `isMenuOpen`, is registered twice; the repair must be idempotent under double registration.

**Defect 3 — trap survives widening.** After 375 to 1440 with the menu open: `.show` false, `aria-expanded` false, body overflow "", no inert (the scroll lock is not stuck), but Tab from `#darkModeToggle` lands on `#nav-workout-plan`: `handleResize` (203-212) does not run the close routine, so `isMenuOpen` (61, 165) and both `keydown` listeners (159-160, removed only at 172-173) survive. The handler tests `innerWidth > 992` while the hamburger layout runs to 1359.98px, so open at 1100 then resize to 1101 closes the menu and drops focus to `BODY`.

**AUD-0418.** `navbar.css` 885-899 labels the unlayered `.navbar { position: fixed; top: 0; left: 0; right: 0; z-index: 1000 }` rule "Deprecated" / "Legacy fallback - only applies outside #navbar wrapper". It is the live winner for `position` on `#navbar` (pinned by `RETAINED_LEGACY_DECLS`, `tests/test_css_wp4_4_navbar_contracts.py:135`; evidence `docs/CSS_PHASE4_WP4_4_F1_NAVBAR_EVIDENCE.md` §13.1). `#navbar` is `<header class="navbar navbar-expand-lg ...">` (`templates/base.html:37`), so the rule applies to it.

---

## Plan v1

**Goal**: At hamburger widths the open mobile menu is a full-height, readable panel that closes cleanly on an empty-space click and releases its focus trap and scroll lock when the viewport leaves the hamburger layout, with the closed header and desktop navigation unchanged.

**Scope**
- **In**: panel-scoped CSS for the open panel (`nav.navbar-collapse.show` and its `.nb-compact` variant) in both hamburger bands: viewport-derived height, `top` equal to the header's real bottom edge in normal and compact states, effective panel background in both themes. JS: idempotent empty-space close; resize teardown through the normal close routine; one breakpoint source matching the CSS. AUD-0418 comment correction. Red-before/green-after E2E coverage. Docs and pin updates the change forces.
- **Out**: any declaration on `#navbar` itself or that paints when the menu is closed or at 1360px and up; defect 4 and #736/#740; the double initialisation (#634); the visual-harness blur observation; the 901-904 comment (not the AUD-0418 block; correct it only if it falls in a block already being edited); desktop hover dropdowns (note: their query at `navbar-enhancements.js:223` is `min-width: 992px`, also mismatched with the 1360px layout; recorded, not touched); redesign; unlabeled controls and the "by Avihai" overhang seen in the open panel (observations for a follow-up issue); Firefox/WebKit (assumption A5); `--update-snapshots`.

**Decisions the plan makes (reviewers may challenge each)**

- **D1 Base and merge order.** Branch `fix/733-mobile-menu-panel` from `origin/main` `8884ec51`, independent of unmerged #740 (awaiting the owner's baseline decision, red Windows visual job). Rationale: clean comparison against committed goldens, own CI, no stacked PR. Known overlap: contract pin counts in `tests/test_css_wp4_4_navbar_contracts.py`, `docs/test_inventory/*`, possibly `e2e/nav-dropdown.spec.ts`. Whichever PR merges second merges `main` in, recounts pins, regenerates the inventory and reruns affected gates.
- **D2 CSS placement and layer-span pin.** `tests/test_css_wp4_4_a_baseline_contracts.py:159-161` pins `navbar.css` layer span `{openLine: 6, closeLine: 883}` against `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` (hand-edit only the affected entries, never `emit_baseline.py`). Lines added inside the layer move `closeLine`; lines added after 883 do not. An unlayered `!important` panel rule with selector `#navbar nav.navbar-collapse.show` (1,2,1) beats the unlayered 969-973 rules on specificity, so the fix can live after the layer (the file already has unlayered phone-band rules at 1473-1477 and the tablet band at 1264). Preferred: unlayered, to keep the layer span stable; the architecture reviewer decides. Either way the winner of every changed property is confirmed by computed style, with the fewest new rules and `!important`s.
- **D3 Panel background (owner-visible at Gate 1).** Recommended: fully opaque panel in the existing per-theme surface colour (light `--surface-2`/white; dark the existing dark panel colour), because blur cannot work inside the header's backdrop root and any translucency leaves page text ghosting behind the links. Alternative: keep the authored 88-95% translucency and accept faint ghosting. This clarifies criterion 1 (a readable panel) and needs the owner's approval or change at Gate 1.
- **D4 Close mechanism.** Empty-space click (target is the panel element itself, today's definition) closes through one idempotent path (Bootstrap `Collapse.hide()` or equivalent), never by toggling. Must be correct under double registration (a second call is a no-op) and under reduced motion, and end with criterion 2's state.
- **D5 Resize.** Leaving the hamburger layout runs the same teardown as a normal close (state flag, both `keydown` listeners, scroll lock, inert, `aria-expanded`, toggler state) without moving focus to the now-hidden toggler. The layout test uses `matchMedia('(min-width: 1360px)')` (or equivalent single source) in place of `innerWidth > 992`. Resizes inside the hamburger layout leave the menu open.
- **D6 Tests.** All in `e2e/nav-dropdown.spec.ts` (no new spec file: CI pins the spec list count at 25). It takes `test` from `./strict-fixtures`, so the zero-allowance console guard applies. The existing helper `openMobileNavbar` (lines 32-39) asserts only `toHaveClass(/show/)`, which is why clipping passed; new tests assert geometry. No Vitest cases (adding or removing one moves four pytest pins in `test_vitest_inventory_contracts.py`).

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `static/css/navbar.css` | modify | Open-panel height/top/background in both bands and compact variants (D2, D3); AUD-0418 comment at 885-899 corrected; `#navbar` and closed-state rules untouched. |
| `static/js/modules/navbar-enhancements.js` | modify | D4 and D5. Overlay handler (188-194) and `handleResize` (203-212); teardown shared with `closeMobileMenu` (164-177) minus focus move. |
| `e2e/nav-dropdown.spec.ts` | modify | D6 cases below, red on `main`. |
| `tests/test_css_wp4_4_navbar_contracts.py` | modify | Pins at lines 233-263 (`IMPORTANT_DECLARATIONS = 93`, `CUSTOM_PROPERTY_DECLARATIONS = 72`, `STYLE_RULES = 190`, layered 101 / unlayered 89) move only as far as the change needs; each moved pin gets its exact new value and a one-line reason. No guarantee weakened. |
| `tests/test_css_wp4_4_a_baseline_contracts.py` and `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` | modify only if lines are added inside the layer or another offset-bearing entry moves | Layer span at 159-161 (`closeLine: 883`); hand-edit affected entries only. Whether other baseline entries (`contractAnchors`, `pinnedDeclarations`, pinned at 689-690) shift is not yet verified; the implementer checks by running the file. |
| `docs/CSS_PHASE4_WP4_4_F1_NAVBAR_EVIDENCE.md` | check | AUD-0418 source pointer (~line 379); add a correction note only if the doc must stay truthful after the comment change. |
| `docs/product/DESIGN_BRIEF.md` | modify | Lines 157-159 describe the header's glass only and stay true; add one sentence that the open mobile panel is opaque (D3 outcome) and why. Accessibility section (381-398) has no menu focus-trap statement; add one bullet for the trap, Escape, empty-space close and resize release. |
| `docs/product/APP_FLOW.md` | modify | "Global navigation" table (200-213) has no row for the menu toggle; add one describing open, close (toggle, Escape, empty-space click, widening past 1360px). |
| `docs/test_inventory/TEST_INVENTORY.md`, `.json` | regenerate | `scripts/generate_test_inventory.py`, then `--check`. |
| `docs/mobile_menu_panel/PLANNING.md` | complete | Council record and evidence. |
| `templates/base.html`, any `tests/` Vitest file | no change | Defect 4 is #740; no Vitest cases. |

**Effort**: M · **Owner**: automation-qa (tests first), senior-developer (implementation and verification); reviewers independent · **Depends on**: none (independent of #740, D1)

**Sequence**
1. Write the E2E cases and run them on `main`'s code to record red for each defect (D6).
2. Implement CSS and JS (D2-D5) and the AUD-0418 comment correction.
3. Run targeted specs green, then move the pins and inventory exactly as needed.
4. Update the two product docs; run the full gates below.
5. `code-reviewer` then `unslop-reviewer` on the diff.
6. Push, open the PR, mark it ready, and stop. Merge only on the owner's explicit confirmation naming the PR. Close-out: comment on #733, tick AUD-0418 on #575.

**E2E cases (all in `nav-dropdown.spec.ts`; poll after collapse transitions, never fixed waits)**
- Geometry: panel top equals header bottom and panel bottom equals viewport bottom; every primary link and right-hand control is visible and hittable via `elementFromPoint`, scrolling the panel when the viewport is short; at 375 and 1100, light and dark, normal and compact header; computed panel background is effectively opaque in both themes.
- Empty-space click closes and stays closed after settling, with scroll unlocked, `aria-expanded="false"` and focus on the toggler.
- Widen 375 to 1440: Tab from the last navbar control leaves the navbar; reopening at 375 still traps and Escape closes. 1100 to 1101 keeps the menu open; 1100 to 1440 closes it.

**Expected gates** (QUALITY_GATE rows: CSS static bundles shared surface; frontend JS; E2E spec; the product-manager did not re-read the JS and E2E row text)
- pytest: full suite, including `test_css_wp4_4_navbar_contracts.py`, `test_css_wp4_4_a_baseline_contracts.py`, `test_css_cascade_contracts.py`, `test_vitest_inventory_contracts.py`, `test_playwright_shard_launcher_contracts.py`.
- e2e (Chromium): `smoke-navigation`, `nav-dropdown`, `accessibility`, `dark-mode`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening`; also `listener-cleanup` as a targeted run because the resize listener changes (it counts window `resize` listeners).
- visual: full `visual.spec.ts` matrix with `PW_VISUAL_SEED=1` on Windows, expecting zero diffs (the orchestrator reports the matrix never opens the menu; nothing closed-state changes). Never `--update-snapshots`. Linux deep gate (`gh workflow run deep-gate-visual.yml --ref <branch>`) is a workflow dispatch the owner is asked to authorize at Gate 1.
- other: seven-surface Stylelint (`node scripts/css_audit/stylelint_surfaces.mjs`, no category rises); `tsc`; inventory `--check`; `/verify` runtime smoke of the changed flow (`docs/ai_workflow/AUTONOMY.md`); PR description with migration notes (navigation is not a core calculation workflow; state the user-visible behaviour changes).

**Risks for reviewers**
- Opaque-versus-translucent panel is a visual choice the owner has not seen (D3).
- The layered/unlayered choice trades layer-span pin churn against specificity reliance (D2).
- Moving the breakpoint changes behaviour for users resizing between 992 and 1359px (the menu now stays open); the desktop hover dropdown query at 223 still uses 992px.
- Double registration (#634) means every JS change runs twice per page.
- `dvh` is used for height; the supported matrix is Chromium only (A5).
- #740 merge order (D1) may force a second pin and inventory recount.

---

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `a42b0076266c8a6b5` | Author of Section 0 and Plan v1. |
| `product-manager` — response matrix + Plan v2 | `a42b0076266c8a6b5` | Same agent, resumed. |
| `architecture-reviewer` | `acbcbb03bd6105a8f` | Step 2 reviewer. |
| `test-strategist` | `a9055a77f08029fa6` | Step 2 reviewer. |
| `product-risk-reviewer` | `a04ed6bbceda5c7d7` | Step 2 reviewer. |
| read-only diagnosis (`senior-developer`) | `aee82c5b120ae522b` | Source of the measured diagnosis above. |

**Same product-manager resumed for the matrix + Plan v2?** `yes` (via `SendMessage` to the Plan v1 agent ID).

**Evidence gap**: none for continuity.

**Recorded limitations**
- All reviewers and the product-manager ran on a smaller model at the owner's request.
- The test-strategist stated it did not read `e2e/visual-helpers.ts`, the two navbar/baseline contract test files, `scripts/generate_test_inventory.py` or `ci.yml` in full, so its pin and inventory findings rest on the plan's citations. Where it conflicts with the architecture-reviewer (who read the baseline contract), the architecture reading is adopted, and the implementer confirms by running the two contract files first.
- Reviewer findings are recorded below as relayed by the orchestrating session (the main Claude Code session), which also proposed the dispositions; the owner confirms them at Gate 1. They are summaries, not verbatim reviewer output.

---

## Reviewer verdicts

All three reviewers returned **sound with advisories, no blocking finding**.
- `architecture-reviewer` verified clean: phone-band cascade, the unlayered (1,2,1) `!important` fix beating 969-973, tablet-band analysis, base on `main`.
- `product-risk-reviewer` confirmed Calculation surface `none`, the non-goals, assumptions A1-A5 respected, and nothing dropped from criteria 1-6.

## Response matrix

| ID | Finding (summary) | Disposition | Plan v2 |
|---|---|---|---|
| A1 | `handleResize` (203-212) sits outside the block owning `closeMobileMenu`/`trapFocus`/`isMenuOpen`; teardown must be hoisted in and use the closure's own state, not the last-writer-wins `window.navbarUnlockBodyScroll`. | Accept | D5 |
| A2 | Name the call: `bootstrap.Collapse.getOrCreateInstance(mobileMenu, { toggle: false }).hide()`; without `{ toggle: false }` a new instance toggles in its constructor (defect 2 again); a second `hide()` is a no-op. Resize teardown stays manual and resets `.show`, toggler `collapsed` and `aria-expanded`. | Accept | D4, D5 |
| A3 | Exactly one window `resize` listener evaluating `matchMedia('(min-width: 1360px)').matches` at call time; no `matchMedia` `change` listener. | Accept | D5 |
| A4 | Specify the CSS exactly (one unlayered `@media (max-width: 1359.98px)` block, `!important` on height/background including dark, compact `top` at (1,3,1), keep the tablet rule). | Accept in part: constraints adopted; the exact CSS stays the implementer's choice between two designs under a fixed preference order. Panel-top = header-bottom and panel-bottom = viewport-bottom accepted. | D2 |
| A5 | "No Stylelint category may rise" is unachievable with new `!important`/`#navbar` rules; the script only reports; a rise needs a recorded owner exception. | Accept: reword to a reported per-category delta; request the bounded exception at Gate 1. | Gates, Gate 1 ask 4 |
| A6 | Baseline pin compares recorded counts to `sourceCommit`; only `spans` (`closeLine: 883`) concerns this change; unlayered additions and the AUD-0418 edit sit after 883, so no JSON edit is expected. Moving navbar-contract pins: `IMPORTANT_DECLARATIONS`, `STYLE_RULES`, unlayered count; layered 101 and `LAYER_BLOCKS` stay. No existing declaration deleted; every moved literal justified. Update the stale docstring reference `navbar.css:892` (test file line 10) and the F1 evidence pointer if line numbers move. | Accept | D2, Artifacts |
| A7 | Second PR to merge resolves the pin conflict by recounting against the merged file, never by taking a side; rerun the geometry tests after merging `main` (#740 changes phone header content); note in the PR body. | Accept | D1 |
| T1 | Explicit geometry assertions (`clientHeight` >= viewport height - header bottom - 1; top = header bottom; bottom = `innerHeight`; each control hit-tested with `elementFromPoint` after scrolling into the panel); record red on `main` (62 vs 291); short viewport asserts reachability by scrolling. | Accept | Tests |
| T2 | Hit-test only after the 200ms `slideInDown` settles; `expect.poll`/`toPass` on stable geometry, never `waitForTimeout`. | Accept | Tests |
| T3 | Empty-click test red through the reopen, not clipping: choose the click point dynamically (`elementFromPoint` is `#navbarNav`; a 4px strip exists on `main`), real mouse click, poll past the ~600ms reopen window; assert `aria-expanded`, body overflow, `inert` cleared, focus on toggler. | Accept | Tests |
| T4 | Prove idempotence under double registration by observation. | Accept, simplified: zero `shown.bs.collapse` events and a stable closed state in the hold window; no MutationObserver unless insufficient. | Tests |
| T5 | Tab test stays red on `main`: after 375 to 1440, focus `#darkModeToggle`, Tab, assert focus is not `#nav-workout-plan` or inside `#navbarNav` and keydown not default-prevented. | Accept | Tests |
| T6 | Run the empty-click test once with `reducedMotion: 'reduce'`. | Accept | Tests |
| T7 | Opaque-background assertion parses `rgb()/rgba()` and `color(srgb ...)`, checks alpha = 1; red on `main` (`rgba(0, 0, 0, 0)`); follows the owner's D3 choice. | Accept | Tests, D3 |
| T8 | No new spec; modest case count (loop viewports/themes inside a few tests); regenerate the inventory after names are final and before the first push. | Accept | Tests, Sequence |
| T9 | `listener-cleanup.spec.ts` asserts a relative delta, so the Plan v1 rationale is partly wrong; keep as a cheap targeted run catching a new permanent window listener. | Accept (Plan v1 rationale corrected; A3 keeps the listener count unchanged) | Gates |
| T10 | Pin the boundary: 1359 stays open, 1360 closes, plus 1100 to 1101 and 1100 to 1440. | Accept | Tests |
| T11 | New CSS at file end to minimise baseline offset shifts; edited comment line count; Stylelint `!important` category. | Accept in part: offset concern superseded by A6; implementer runs the two contract files first after the edit to enumerate real failures; keep the AUD-0418 comment the same line count if practical (otherwise update references per A6); Stylelint per A5. | D2, Sequence |
| T12 | "Zero visual diffs" holds for the closed state only; declarations under the oracle blind-spot register (`docs/CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md` section 8) are not provable by the pixel matrix. | Accept: add a scripted computed-style differential of the closed state as primary evidence for criterion 4; Linux deep gate required, a green reached through retries is not a pass. | Evidence |
| T13 | State that `accessibility.spec.ts` axe pins are not expected to move (axe does not scan the open menu); name `test_css_wp4_4_layout_contracts.py` and `test_css_theme_dark_p3_audit_contracts.py` among pytest files that read `navbar.css`. | Accept | Gates |
| T14 | No fixture/conftest work. | Accept (no action) | none |
| P1 | The opaque panel is an addition beyond criteria 1-6, not a clarification; `DESIGN_BRIEF.md:303` documents the navbar as translucent blur; the 992-1359px band changes visibly too. | Accept: relabelled an owner decision at Gate 1 with both options and costs; before/after screenshots (light/dark, phone and tablet band) in the PR for by-eye review. | D3, Gate 1 ask 2 |
| P2 | Behaviour during Bootstrap's `.collapsing` phase unspecified (possible one-frame snap; `hidden.bs.collapse` must still fire). | Accept: by source the panel is `display: none` whenever `.show` is absent in both bands (704; 1272-1274 `!important`), so no snap is expected; the implementer confirms by observation in `/verify`; tests assert the close completes (`hidden` reached, focus returned). A rule is added only if a flash is measured. | Tests |
| P3 | Escape (104-106) also closes by hand, leaving Bootstrap/toggler state diverged. | Accept: Escape and empty-click share the single `hide()` path; assert one toggler click reopens after an Escape close, an empty-click close and a resize close. | D4, Tests |
| P4 | Focus after resize teardown. | Accept as a stated decision (focus left where it is; nothing focused programmatically; if the focused element became hidden, focus falling to the document is accepted). Reject the extra "start Tab from the toggler" case: the toggler is hidden at 1360px and up and cannot hold focus. | D5 |
| P5 | Accidental close acceptable: only `e.target === mobileMenu` closes, the toggler stays visible outside the `inert` region, reopening is one tap. | Accept the rationale; reject a touch-drag test (a scroll drag synthesises no click; not worth a test identity). | D4 |
| P6 | Test the 1359/1360 boundary and idempotence under double registration. | Accept (as T10/T4) | Tests |
| P7 | Doc wording: APP_FLOW row uses the table's fixed "Action type" vocabulary (Presentation) and the app's link names, and says "widening to 1360px or wider"; DESIGN_BRIEF sentence names the hamburger widths (up to 1359.98px), does not contradict line 236, names the per-theme panel colours as shipped; PR text lists each user-visible change. | Accept | Docs, PR |

**Repository reconciliation notes** (checked 19 Nov 2026): `DESIGN_BRIEF.md:303` and `test_css_wp4_4_navbar_contracts.py:10` (`navbar.css:892`), `LAYER_BLOCKS = 1` (line 235), layered 101 (line 257), `.stylelintrc.json` rules `declaration-no-important` (line 14) and `selector-max-id: 1` (line 24), and `CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md` section 8 all exist as cited. One citation differs: the tablet-band `display: none !important` is at `navbar.css` 1272-1274, not 1258. The exact wording of the QUALITY_GATE Stylelint/exception clause could not be read in isolation (it sits in one long table line, 52; line 38 states owner exceptions are given directly and never inferred); Gate 1 ask 4 therefore requests the exception explicitly.

---

## Plan v2

**Goal**: At hamburger widths (up to 1359.98px) the open mobile menu is a full-height, readable panel; an empty-space click or Escape closes it through one path and leaves it closed; widening to 1360px or wider releases its focus trap, scroll lock and inert state; the closed header and desktop navigation are unchanged.

**Scope**
- **In**: panel-scoped CSS for the open panel (`nav.navbar-collapse.show` and its `.nb-compact` variant) in both hamburger bands; the JS close and resize repairs; the AUD-0418 comment correction; E2E coverage red before and green after; the docs and pin updates the change forces.
- **Out**: unchanged from Plan v1 (anything on `#navbar` itself or that changes the closed state or the 1360px-and-up layout; defect 4 and #736/#740; #634 double initialisation; visual-harness blur observation; the 901-904 comment; hover dropdown query at `navbar-enhancements.js:223`; redesign; unlabeled controls and "by Avihai" overhang; Firefox/WebKit; `--update-snapshots`).

**Decisions**

- **D1 Base and merge order.** Branch `fix/733-mobile-menu-panel` from `origin/main` `8884ec51`, independent of #740. Overlap: contract pin counts, test inventory, possibly `e2e/nav-dropdown.spec.ts`. The second PR to merge merges `main` in, recounts every pin against the merged file (never taking one side), regenerates the inventory, and reruns the new geometry tests (#740 changes phone header content). The PR body says so.
- **D2 CSS.** Constraints:
  - Only declarations that apply to the open panel change; nothing on `#navbar` itself; nothing that changes computed styles when the menu is closed or at 1360px and up.
  - No existing declaration is deleted; the layered rule count (101), `LAYER_BLOCKS` and `closeLine: 883` do not move.
  - Height uses `dvh`. Compact state: panel top equals the 56px header bottom in both bands.
  - The winner of every changed property is proven by computed style.
  - The implementer chooses between two designs by this preference order: (1) no weakened guarantee; (2) fewest new `!important` declarations and `#navbar` selectors (`.stylelintrc.json`: `declaration-no-important`, `selector-max-id: 1`); (3) fewest moved pins.
  - **Design X** (reviewed by the council): a new unlayered `@media (max-width: 1359.98px)` block with `#navbar nav.navbar-collapse.show` height and background `!important`, a dark variant, and compact `top`/height at (1,3,1); the tablet-band rule stays.
  - **Design Y** (not reviewed by the council): narrow the unlayered override at 969-973 to `#navbar .navbar-collapse:not(.show)` so the authored band declarations apply to the open panel without new `!important`, plus the missing viewport-derived height and compact declarations (a fixed panel still resolves against the 64px header, so an explicit height remains necessary). If chosen, the implementer shows that the computed-style differential for the closed state and at 1360px and up is empty, and says so in the evidence.
  - The AUD-0418 comment (885-899) is corrected, keeping its line count if practical.
- **D3 Panel background: owner decision at Gate 1.** Option 1 (recommended): fully opaque per theme using the existing surface colours; cost: a visual change beyond criteria 1-6 in both bands, and the panel stops resembling the translucent navbar (`DESIGN_BRIEF.md:303`). Option 2: the authored translucent values (88-95%); cost: unblurred page text ghosts behind the links, because blur cannot work inside the header's backdrop root. The choice applies to both bands, and the T7 assertion follows it. Before/after screenshots (light and dark, phone and tablet band) go in the PR for the owner's by-eye review.
- **D4 Close path.** Escape and empty-space click (target is the panel element itself) call `bootstrap.Collapse.getOrCreateInstance(mobileMenu, { toggle: false }).hide()`; cleanup runs on `hidden.bs.collapse`. A second call is a no-op, which makes it safe under double registration (#634) and reduced motion. Never toggle. Accidental close is acceptable: only `e.target === mobileMenu` closes, the toggler stays visible outside the `inert` region, reopening is one tap.
- **D5 Resize.** `handleResize` moves into the block that owns `closeMobileMenu`, `trapFocus` and `isMenuOpen` and uses that closure's state (not `window.navbarUnlockBodyScroll`). Exactly one window `resize` listener evaluates `matchMedia('(min-width: 1360px)').matches` at call time; no `matchMedia` `change` listener. When it matches with the menu open, teardown runs manually: `isMenuOpen = false`, both `keydown` listeners removed, `.show` removed, toggler `collapsed` class and `aria-expanded` reset, scroll lock and inert released. Focus is left where it is and nothing is focused programmatically. Resizes inside the hamburger layout leave the menu open.
- **D6 Tests.** All in `e2e/nav-dropdown.spec.ts` (no new spec; CI pins 25), on `./strict-fixtures`, a modest case count (loop viewports and themes inside a few tests). No Vitest cases. Names are final and the inventory regenerated before the first push.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `static/css/navbar.css` | modify | D2, D3, AUD-0418 comment. |
| `static/js/modules/navbar-enhancements.js` | modify | D4, D5. |
| `e2e/nav-dropdown.spec.ts` | modify | Cases below. |
| `tests/test_css_wp4_4_navbar_contracts.py` | modify | Moving pins: `IMPORTANT_DECLARATIONS`, `STYLE_RULES`, unlayered count; layered 101 and `LAYER_BLOCKS` stay; each moved literal justified; docstring reference `navbar.css:892` (line 10) updated if lines move. |
| `tests/test_css_wp4_4_a_baseline_contracts.py`, `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` | none expected | Only `spans` (`closeLine: 883`) concerns this change and all additions land after it. The implementer runs both contract files first after the edit; the architecture reading governs where the test-strategist differs. |
| `docs/CSS_PHASE4_WP4_4_F1_NAVBAR_EVIDENCE.md` | check | AUD-0418 pointer (~379) if line numbers move. |
| `docs/product/DESIGN_BRIEF.md` | modify | One sentence: at hamburger widths (up to 1359.98px) the open panel's per-theme background as shipped (D3), without contradicting line 236 ("There is no mobile band"); one Accessibility bullet for trap, Escape, empty-space close and resize release. |
| `docs/product/APP_FLOW.md` | modify | One row in Global navigation (200-213): "Action type" Presentation; the app's link names; open, close by toggle, Escape and empty-space click, and release when widening to 1360px or wider. |
| `docs/test_inventory/TEST_INVENTORY.md`, `.json` | regenerate | Then `--check`. |
| `docs/mobile_menu_panel/PLANNING.md` | complete | Council record. |
| `templates/base.html`, Vitest files, other spec files | no change | |

**Effort**: M · **Owner**: automation-qa (tests first), senior-developer (implementation and verification); reviewers independent · **Depends on**: none

**Sequence**
1. Write the E2E cases and record red on `main` for each defect.
2. Implement D2-D5 and the AUD-0418 comment.
3. Run `test_css_wp4_4_navbar_contracts.py` and `test_css_wp4_4_a_baseline_contracts.py` first to enumerate real failures; move only the pins the change forces.
4. Finalise test names, update the product docs, regenerate the inventory.
5. Run the full gates; then `code-reviewer` and `unslop-reviewer` on the diff.
6. Push, open the PR, mark it ready, and stop. Merge only on the owner's explicit confirmation naming the PR. Close-out: comment on #733, tick AUD-0418 on #575.

**Tests (all red on `main` before the fix, green after; `expect.poll`/`toPass`, never `waitForTimeout`)**
- Geometry at 375 and 1100, light and dark, normal and compact header: panel `clientHeight` >= viewport height - header bottom - 1; panel top = header bottom; panel bottom = `innerHeight`; every primary link and right-hand control hit-tested with `elementFromPoint` after scrolling it into view inside the panel, only after the 200ms `slideInDown` settles. Record red on `main` (62 vs 291). A short viewport asserts reachability by scrolling. The panel background is opaque (alpha 1, parsing `rgb()/rgba()` and `color(srgb ...)`; `rgba(0, 0, 0, 0)` on `main`) per the D3 choice.
- Empty-space click: choose the click point dynamically (`elementFromPoint` is `#navbarNav`), real mouse click, then poll past the ~600ms reopen window. Assert the menu stays closed, `aria-expanded="false"`, body overflow cleared, `inert` cleared, focus on the toggler, zero `shown.bs.collapse` events, and the close completed (`hidden` reached). Run once with `reducedMotion: 'reduce'`.
- Reopen: one toggler click reopens after an Escape close, an empty-click close and a resize close.
- Resize: 375 to 1440 with the menu open, focus `#darkModeToggle`, press Tab; focus is not `#nav-workout-plan` or inside `#navbarNav` and the keydown is not default-prevented. Reopening at 375 still traps focus and Escape closes. Boundary: 1359 stays open, 1360 closes; 1100 to 1101 stays open; 1100 to 1440 closes.

**Evidence for criterion 4 (closed state)**: a scripted computed-style differential, before versus after, of the closed-state `#navbar`, `#navbar > .container-fluid`, `#navbarNav` and the nav links and controls at 375, 768, 1100 and 1440, light and dark, normal and compact; the expected diff is empty. It is the primary evidence, with the `visual.spec.ts` matrix alongside (declarations under the oracle blind-spot register are not provable by pixels alone).

**Expected gates**
- pytest: full suite, including `test_css_wp4_4_navbar_contracts.py`, `test_css_wp4_4_a_baseline_contracts.py`, `test_css_cascade_contracts.py`, `test_css_wp4_4_layout_contracts.py`, `test_css_theme_dark_p3_audit_contracts.py`, `test_vitest_inventory_contracts.py`, `test_playwright_shard_launcher_contracts.py`.
- e2e (Chromium): `smoke-navigation`, `nav-dropdown`, `accessibility` (axe node-count pins not expected to move; axe does not scan the open menu), `dark-mode`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening`; plus `listener-cleanup` as a cheap targeted run to catch any new permanent window listener (it asserts a relative delta; the Plan v1 rationale was partly wrong).
- visual: full `visual.spec.ts` matrix with `PW_VISUAL_SEED=1` on Windows, zero diffs expected for the closed state; never `--update-snapshots`. Linux deep gate required on the branch (Gate 1 ask 3); a green reached through retries is not a pass.
- other: seven-surface Stylelint (`node scripts/css_audit/stylelint_surfaces.mjs`) with the per-category delta reported and nothing rising except what the open-panel fix strictly needs; `tsc`; inventory `--check`; `/verify` runtime smoke of the changed flow, including observing that no flash occurs during the `.collapsing` phase; PR description with migration notes listing each user-visible change (panel full height, panel background, empty click closes, menu stays open between 992 and 1359px on resize) and the before/after screenshots.

**Risks**
- D3 is a visual choice outside criteria 1-6.
- Design Y is unreviewed; Design X adds `!important` declarations and `#navbar` selectors.
- The breakpoint change alters behaviour for users resizing between 992 and 1359px; the hover dropdown query still uses 992px.
- Double registration (#634) runs every JS change twice per page.
- `dvh` is Chromium-only verified (A5).
- #740 merge order may force a pin and inventory recount (D1).

### Gate 1 asks (for the owner)

1. Approve Plan v2 as written, including the council dispositions in the response matrix.
2. Choose the D3 panel background: Option 1 (recommended), a fully opaque panel per theme using the existing surface colours; or Option 2, the authored translucent values, accepting unblurred page text ghosting behind the links. This applies to both hamburger bands.
3. Authorize one dispatch of the Linux visual deep gate (`gh workflow run deep-gate-visual.yml --ref fix/733-mobile-menu-panel`) once local gates are green.
4. Record an exception allowing the Stylelint `declaration-no-important` and `selector-max-id` (or equivalent id-selector) categories to rise only by what the open-panel fix strictly needs, with the exact delta reported in the PR. If you decline, Design Y becomes mandatory and any unavoidable rise comes back to you.

### Gate 1 owner approval and amendment

The owner answered the four Gate 1 asks directly in the 19 November 2026 conversation. Answers, verbatim:

1. **Ask 1 (approve Plan v2):** "Approve Plan v2 with one amendment to D5. Give the mobile menu a single lifecycle owner even when navbar initialization runs twice. Add a regression test that crosses 1360px while the menu is opening and verifies that scroll lock, inert state, and the focus trap stay cleared after Bootstrap finishes. Merge still requires my separate confirmation."
2. **Ask 2 (D3 background):** selected **"Fully opaque (Recommended)"** — option text: "Solid panel in the existing surface colour per theme (light/dark). Links are fully readable; the panel no longer looks like translucent glass."
3. **Ask 3 (Linux visual deep gate):** selected **"Authorize one dispatch"** — option text: "Run the Linux visual deep gate once on the #733 branch; result is reported in the PR."
4. **Ask 4 (Stylelint):** "Allow only the minimum declaration-no-important increase needed for the open panel. Report the exact before and after counts in the PR. Hold every other category at or below baseline."

**Consequences (the orchestrating session's reading of the answers; where they differ from the reviewed Plan v2 text above, this section supersedes it)**

- **D5 amended.** The mobile-menu lifecycle (collapse `shown`/`hidden` handlers, panel click, keydown trap, resize teardown, scroll lock and inert) is registered once per page even though `initializeNavbarEnhancements()` is still called twice; the second call must be a no-op for the mobile menu. This brings the mobile-menu part of the #634 double registration into scope; the duplicate call sites themselves are not required to change. Mid-open crossing: if the layout is no longer the hamburger layout when Bootstrap finishes opening (`shown.bs.collapse`), the menu must end torn down: scroll unlocked, nothing inert, no focus trap.
- **D6 gains two regression tests.** (a) Open the menu and cross to 1360px or wider while Bootstrap is still opening; after Bootstrap finishes, scroll lock, inert state and the focus trap are cleared and stay cleared. (b) The mobile-menu lifecycle listeners are registered exactly once after page load (red on `main`, where they register twice).
- **D3 is Option 1 (opaque).** The alpha = 1 assertion stands.
- **Stylelint.** Only `declaration-no-important` may rise, by the minimum the open panel needs, with exact before and after counts in the PR; every other category stays at or below baseline. `.stylelintrc.json` `selector-max-id: 1` is not tripped by a single `#navbar` id. The choice between Design X and Design Y stays the implementer's under the D2 preference order, now with this hard limit.
- **Linux deep gate:** one dispatch is authorized on `fix/733-mobile-menu-panel` once local gates are green.
- **Merge** still requires the owner's separate explicit confirmation naming the PR.

This amendment is the owner's direct instruction. No council re-review was run on it; it is not a reviewer pass.

### Plan v2 sign-off — GATE 1

- [x] Gate 0 complete (19 November 2026).
- [x] Every reviewer finding has a disposition in the response matrix.
- [x] Agent provenance is complete.
- [x] Owner approved Plan v2 (Gate 1 asks 1-4), with the D5 amendment above, on 19 November 2026.
- [x] Ready to implement.

---

## Evidence — implementation (19 Nov 2026)

**Changed paths**: `static/css/navbar.css`, `static/js/modules/navbar-enhancements.js`, `tests/test_css_wp4_4_navbar_contracts.py` (3 pins), `docs/product/DESIGN_BRIEF.md`, `docs/product/APP_FLOW.md`, `docs/test_inventory/TEST_INVENTORY.{md,json}` (regenerated), `docs/product/review-733/{before,after}/*.png`. `e2e/nav-dropdown.spec.ts` untouched by the implementer.

**Design (Design Y)**: unlayered `#navbar .navbar-collapse` and `.navbar-nav` `!important` overrides narrowed to `:not(.show)` (the latter through `:where()` to keep specificity); open-panel `height: calc(100dvh - var(--nav-height))` and opaque `var(--surface-2)` added or edited in place in existing unlayered rules; one new unlayered rule scoping `--nav-height` to `--nav-height-compact` on the open compact panel. New `!important`: 0 (93 -> 93). Layer span untouched (101 layered, `closeLine: 883`). JS: one init guard, one `hide()` close path, one `resize` listener evaluating `matchMedia('(min-width: 1360px)')`, mid-open crossing teardown in `shown.bs.collapse`.

**Commands**: `nav-dropdown` spec 17/17 twice; six contract pytest files 150 passed, 1 failed (`test_this_packet_wrote_no_production_css`, reads uncommitted `git status` under `static/css`; expected red until the change is committed); smoke-navigation + dark-mode + accessibility + listener-cleanup 70/70; `tsc --noEmit` clean; inventory `--check` up to date. Computed-style differential of the closed state (16 scenarios, about 97k values): 0 differences, same-CSS control also 0. Stylelint seven surfaces 2760 -> 2757 (only `navbar.css` `declaration-property-value-disallowed-list` 98 -> 95).
**Known reds / blockers**: the one working-tree pytest above; Linux deep gate and full visual matrix not run here.

## Evidence — merge of `main` and post-merge review (19 Nov 2026)

PR #740 merged to `main` as `5dc83cef` after this branch was cut, so D1 fell to this branch. Commits after `f700e92c`: `6468fb14` (merge of `origin/main`), `8e77b732` (comment and prose follow-up from the first review round, which read the pre-merge diff) and `bc8fadca` (post-merge review fixes). Every gate below ran on `bc8fadca`. The commit after it changes only this file and the screenshots under `docs/product/review-733/`.

**Merge (D1)**: conflicts in `tests/test_css_wp4_4_navbar_contracts.py` and `docs/test_inventory/TEST_INVENTORY.md`. The pins were recounted with the contract file's own parser against the merged `navbar.css`, not taken from either side: custom properties 72, style rules 188, unlayered 89, layered 99, `!important` 93, layer span lines 6-874. The docstring pointer to the `.navbar` rule moved from `navbar.css:892` to `883`. The inventory was regenerated: 740 Playwright tests, 590 required-functional, 4701 pytest nodes, 80 hard waits. Where the sections above say 101 layered rules, `closeLine: 883` or 190/191 rules, they describe the file before the merge.

**Red before, green after (criterion 5)**: `e2e/nav-dropdown.spec.ts` against `main`'s `navbar.css` and `navbar-enhancements.js` (a local proxy served those two files from `5dc83cef`; every other byte came from the branch): 10 failed, 7 passed. All ten `#733 mobile menu panel` tests were red, each on its own assertion. On the branch: 17 passed.

**Post-merge review**: `code-reviewer` and `unslop-reviewer` read the diff against `origin/main`. Fixed in `bc8fadca`:
- The short-viewport test could not fail if panel scrolling were disabled, because its `scrollTop` check was satisfied by its own `scrollIntoView`. It now scrolls with a wheel gesture. Mutation `overflow-y: hidden` on the open panel: exactly that test fails.
- The release assertions never showed that the lock had engaged. They now assert a locked, inert page first. Mutation with the scroll lock removed: exactly the four tests carrying that assertion fail.
- The 100ms open-menu focus timer survived a resize teardown and moved focus to the desktop Plan link, against D5 (nothing is focused programmatically). The teardown now clears it. Checked both ways with the timer stretched: focus landed on `#nav-workout-plan` before the fix and stayed where it was after. No test was added for it.
- Cleanup: the one-caller `closeMobileMenu` folded into the `hidden.bs.collapse` handler, a fixed one-second hold replaced by a wait for the closed state, a shared geometry helper, an unreachable `try/catch` removed, pin comments reworded.

`code-reviewer` re-read that delta and reported no finding. Not changed, with reasons: `hideMobileMenu` has no `typeof bootstrap` guard (the menu can only be open after Bootstrap fired `shown`); the collect-then-assert pattern in two tests stays (it reports every failing method in one run and still fails the test); the corrected `.navbar` comment block keeps its line count (D2); the trailing-whitespace hunks in `navbar-enhancements.js` and the `var(--nav-height, 64px)` / `var(--nav-height)` difference stay as they are.

**Gates on `bc8fadca`**:
- pytest, full suite: 6946 passed, 1 failed, 3 skipped. The failure is `test_worktree_lifecycle.py::test_open_terminal_child_payload_sets_target_runtime_before_use[pwsh]`, the known local failure where `pwsh` on PATH is a Microsoft Store alias; CI's pytest job is the arbiter.
- E2E (Chromium), the ten gate specs: 185 passed.
- Visual: `visual.spec.ts` with `PW_VISUAL_SEED=1` on Windows, 66 passed, no snapshot updated.
- Closed-state computed-style differential, `main`'s two navbar files against the branch's, 16 scenarios (375, 768, 1100 and 1440 wide, light and dark, normal and compact header): 376,296 values, 0 differences. A control run with `main`'s files on both sides also reported 0.
- Stylelint, seven surfaces, `main` at `5dc83cef` to the branch: 2758 to 2755. `declaration-no-important` 1214 to 1214 (`navbar.css` 93 to 93). `declaration-property-value-disallowed-list` 1057 to 1054 (`navbar.css` 98 to 95). No other category or surface moved.
- `tsc --noEmit` clean; inventory `--check` up to date.

**Open panel, measured** (screenshots in `docs/product/review-733/`, visual seed database, `/workout_plan`; "before" is `main` at `5dc83cef`): at 375x812 the panel went from 63px tall with 1 of 13 controls reachable to 748px with 13 of 13. Its background went from `rgba(0, 0, 0, 0)` to `rgb(255, 255, 255)` light and `rgb(38, 49, 61)` dark. At 1100x900 with the compact header the panel top moved from 64 to 56, the header's bottom edge.

**Not done here**: the Linux visual deep gate (one dispatch authorized at Gate 1) is dispatched after the push, and its result is reported in the PR. Merge needs the owner's confirmation naming the PR.
