# Plan review — #736 Step 4, Navigation

## Section 0 — Requirements brief

**Raw request** (verbatim owner instructions)

> Navigation uses bundled Font Awesome Free solid icons, and no template references a navigation GIF. The six GIF files stay in `static/images/` (see "Left for the owner").

> At 320 px at app scale 8 the navbar menu button floats over the page. Fix it in step 4's navigation work.

> D2: B. Open on the first routine tab. Keep All available and keep the choice stateless between visits.
> D3: C. Collapse the filters and show each active filter by name as a removable chip.
> For all other questions through D24, I accept the published defaults. This is my Gate 0 reply for steps 3–5. Begin step 3 after #748 merges.

**Problem.** A user visiting one of eleven pages sees a mixture of animated pictures and coloured symbols. On an Analyze child the bar can fail to identify the user's location. At maximum app scale on a 320 px phone the hamburger extends past the header and the open panel intercepts its control. On intermediate desktop widths some utility controls disappear.

**Acceptance criteria**

1. Given the same Fatigue content, the [phone and desktop mockup](mockup.html) shows the closed header and open navigation at 390 px, the complete bar with Analyze open at 1440 px, and the closed-header clearance at 320 px and app scale 8. Actual before/after evidence includes both themes and visible glyphs with ordinary rendering.
2. Given any of the eleven routes at 390, 768 and 1440 CSS px at default scale 6 in both themes, the visible brand glyph begins on the 16, 24 and 32 px frame gutter respectively. The header has an opaque shared surface, 1 px bottom edge, no shadow or backdrop blur, and the pilot's Inter type roles. No header control introduces a page-level horizontal scrollbar. Compare pre-existing body-only overflow on unmigrated routes to their control, where relevant. Check the already migrated Log and Plan frames.
3. Given a visible destination including an open submenu, the label remains visible and the icon has the same computed colour, measures 1em, and renders its specified Font Awesome Free solid glyph. Preserve destination order. Home/brand uses `dumbbell`, Plan `tasks`, Log `book-open`, Analyze `chart-line`, Weekly `calendar-week`, Session `calendar-day`, Fatigue `battery-half`, Progress `level-up-alt`, Profile `user-circle`, Body Composition `ruler`, Distribute `sliders-h` and Backup `folder-open`. Check visible glyphs on normal pages at 390, 768 and 1440 px, light and dark.
4. Given a direct visit, reload or back/forward navigation, the correct destination has server-rendered `.active` and `aria-current="page"`. On Weekly, Session and Fatigue, Analyze and the selected child both have the indigo visual marker. Its 2 px bar sits under a desktop link or along the leading edge of an open phone row. Hover, keyboard focus and location are distinguishable. Neither icons nor links lift on hover. Theme or muscle-mode changes preserve the current location.
5. Given 320/360/390 px at scale 8 in each theme, the menu button is at least 44 × 44 viewport CSS px, fully within its header, and owns the pointer at centre and near each interior edge in closed, open and Analyze-expanded states. A real click opens, closes and reopens the panel. No button overlaps the first usable page control. Verify full menu reachability and unchanged page scroll width.
6. Given a short viewport or a compact scrolled header, opening the hamburger keeps the page inert, locks background scroll, and lets the menu itself scroll to every item. Keyboard focus wraps. Escape and empty-space dismissal return focus as before. Resizing through 1359/1360 releases scroll lock, inert and focus trap, including a race with Bootstrap's opening transition. The next single click after returning to phone width reopens it. Preserve desktop hover/click/keyboard Analyze, mobile inline Analyze, the skip link, route hrefs/order, LinkedIn destination and scale, muscle-name and theme operations. Right-hand controls keep their existing glyphs with inherited colour.
7. Given 1360/1440/1501/1601 px at scale 6 or 8, every available operation fits in the viewport and remains hit-testable, with its accessible name, original workflow and enabled/disabled state. Check rendered geometry, control overlap, text clipping and first body content immediately below the actual header. At scale 6 show the complete tools and destinations on one row at the desktop threshold. Check whether maximum scale fits one row; if a taller layout is needed, its actual height must clear the first page operation and the open menu.
8. Given a full template scan, all six navbar GIF references and the Session PNG reference are gone. Retain `static/images/{7-days.gif,dividers.gif,icons8-bench-press.gif,icons8-growth.gif,icons8-to-do.gif,notebook.gif}` and `static/images/icons8-session-50.png`, including the PNG's packaging pin.
9. Given a verified precursor fixture and an implementation, a fresh manual reviewer compares normal-rendering before/after screenshots to the committed mockup and acceptance criteria before regeneration. Include both themes, phone menu closed/open/Analyze, desktop Analyze and scale-8 phone stress states. Masked baseline images continue to hide nav icons. Verify glyphs and hit targets independently of those images.
10. Given a proposed visual update, only the 64 permitted existing PNG paths per platform below may change. Protect both lower Profile segments and all 15 thumbnail PNGs per platform, retain all five byte exemptions, and compare both operating systems on the final head. Re-pin superseded colour, motion and CSS census expectations to the shipped behaviours and measurements. Preserve existing functional and accessibility coverage.

**Calculation surface** — none.

**In scope.** The single shared navigation PR, its documentation, mockup, acceptance coverage, narrow-phone repair and scoped visual updates. D8–D11 determine the icon set, selected marker, Analyze grouping and full frame. K16–K26 determine inherited colour, 1em icons with labels, server state, stable order, hover behaviour, utility glyphs, token-based dark styling, independent PR and normal-rendering glyph testing. Home tile adoption is reserved for the Home PR.

**Out of scope.** Route body redesign, calculation changes, DB schema, API response shapes, global motion restyling, file deletion, broader capture regeneration and re-admission of exempt snapshots.

**Assumptions for council disposition**

| Assumption | What the owner sees | What is lost | Recommendation |
|---|---|---|---|
| ⚠️ Use Fatigue for both mockup widths | Both levels of the current marker in one view | Separate mockups per destination | Use Fatigue and verify all eleven routes functionally |
| ⚠️ Analyze takes the active class, only the child takes current-page ARIA | Two visible markers, one announced current page | Separate current-page announcement on the group | Keep one actual current destination |
| ⚠️ Use bundled solid `bars` for the labelled hamburger | The same familiar three strokes in both themes | Bootstrap's SVG rendering | Adopt the mockup glyph |
| ⚠️ Restore all utility operations at 1360–1500 | Scale and signature become reachable as at 1501 | Extra spacing between groups | Use the demonstrated one-row scale-6 fit; council selects the maximum-scale fallback |

**Owner questions.** None. The owner signed Gate 0 for steps 3–5 in the 2026-11-26 Decisions reply. On 2026-11-27 the owner delegated remaining questions to the plan council and Astra. The assumptions above await that disposition; they are not newly attributed owner choices.

### Section 0 sign-off — Gate 0

- [x] Owner confirmed intent and settled the defaults through D24, with D2/D3 exceptions on Workout Plan.
- [x] Owner assigned further presentation assumptions to the council and Astra.
- [x] No unanswered owner decision blocks planning.

## Plan v1

**Goal.** A user can recognize the current page and operate the complete shared navigation in either theme, including when the app is zoomed on a narrow phone.

**Effort and dependency.** Large, cross-route presentation change. Step 3 merged in PR #752. This branch, `feat/736-navigation`, starts at freshly fetched `origin/main` commit `006fa3fa`. The manager handles commits, pushes and merges. A single writer works at a time. Keep normal browser, Playwright and seeded DB work serial.

### Control and mockup evidence

The current [merged-base ordinary control](../../artifacts/design-736/step4-navigation/before-q5y280jq/) is being captured from `006fa3fa`. Final image counts and metrics are pending verification. The historical [ordinary predecessor capture](../../artifacts/design-736/step4-navigation/before-tqm9s07m/) at `7f32a18cc1fd7467c39946db0327b68899190ae5` includes 34 states, measurements, font index and an input-blob manifest. The [earlier evidence](../../artifacts/design-736/step4-navigation/before-wrxp2pt7/) is secondary. Verify the merged-base fixture, template, styles, scripts and fonts against the recorded input blobs before implementation. The [mockup measurements](../../artifacts/design-736/step3/resume-unit/nav-mock-m88AVC/), [desktop control log](../../artifacts/p736-check-939dc4b/predecessor.log) and [mockup fit measurements](../../artifacts/p736-check-0e3f6e6/nav-fit.jsonl) support these predictions. Use ordinary application captures for live comparisons.

| Measured item | Before | After to verify |
|---|---|---|
| Visible brand glyph x at scale 6 | 31, 31, 29 px at 390, 768, 1440 | 16, 24, 32 px respectively; compare glyph and frame in one evaluation |
| 320 px, scale 8 | Button 39.97 px square, bottom 101.86 vs header bottom 63.97. Open nav owns the centre | At least 44 px each axis; contains and owns all sampled points in every state. Mockup button bottom 59.39 in 67 px header |
| 360/390 px, scale 8 | Button centre reachable in all three states | Reachability and containment preserved |
| Default desktop fit | Signature and scale occupy zero width at 1360 and 1440; centres and right edges work again at 1501/1601 | All visible at 1360/1440 with no collision. Mockup's scale-6 right edges were 1328/1408 |
| Real zoom and page clearance | Default validated scale is 6 in `app.py::inject_scale_level`. Root scale 8 zooms by 1.2; `a11y.css` counter-zooms navbar | Exercise actual cookies and CSS. Measure row tops, last control bottom, header bottom, first page interaction, scroll width and disabled `+` state. A horizontal fit alone does not prove vertical clearance |
| Glyphs, location and colour | Seven nav image references; JS map omits Fatigue, no marked Analyze parent, three coloured icons | Twelve destination glyphs, all routes selected correctly, one current destination, 2 px marker, zero decorative transforms |

### Artifacts and implementation sequence

1. **Confirm the prerequisite and document the visual targets.** Commit Section 0 and the mockup beside it on the Navigation branch. Validate relative font/style links in the committed mockup. Obtain the independent architecture, test-strategy and product-risk reviews, then record their verbatim findings, response matrix, Plan v2 and delegated Gate 1 before implementation.
2. **Write acceptance tests before changing production.** In `tests/test_visual_selector_contracts.py`, cover the actual bundled glyph names emitted by `templates/base.html`, the retired template image references, and retained files. Use a Flask test client on all eleven routes to verify active class, one current-page link and visual-only Analyze parent in original response HTML. In `e2e/nav-dropdown.spec.ts`, open the hamburger and Analyze as necessary; check the loaded FA solid font, nonempty mapped glyphs and their rendered visibility, inherited colour, font size, accessible labels and marker geometry in each theme/width. Require actual font mappings or browser glyph evidence rather than trusting a CSS class alone. Run narrow, short, regular and compact states, plus all four desktop widths. Reuse existing strict fixtures and selectors. Exercise both right edges and centres, guarded against zero-size rectangles and occlusion. Keep brand/Plan/Profile current-page checks, theme switching, desktop hover and all #743 release/race checks.
3. **Run the control.** Use a seeded disposable fixture, explicit `DB_FILE` and `HT_RUNTIME_DIR`, and an allowed unused port other than 5000/5060/5061. Run the new assertions against predecessor behaviour before implementation. Record distinct reds for seven references/glyphs, missing SSR current state, accent/hover, gutter/surface, hidden utilities and the 320 scale-8 open button. Preserve green controls for menu lifecycle, packaged PNG, enabled states and wider-phone ownership. Avoid one early failing assertion hiding the other measurements. Re-run each red and green group after implementation.
4. **Render state and icons once.** Update `templates/base.html` and remove the `initializeNavbar` import/call in `static/js/app.js`. Retire the map and its event listeners in `static/js/modules/navbar.js`; preserve the tracked file under the owner's deletion restriction and list it for owner action if retired. Keep stable IDs, hrefs, names, Bootstrap collapse/dropdown attributes, `data-visual-icon` and skip target. Keep `navbar-enhancements.js` lifecycle, focus/unlock/reopen logic and desktop interactions. Cover back/forward restoration. Scope destination paint away from `#darkModeToggle.active`; preserve `darkMode.js` sun/moon behaviour and naming-mode icons. Verify dynamic glyph names against rendered output if using Jinja abstractions.
5. **Replace the owning styles.** In `static/css/navbar.css` remove superseded layered and unlayered declarations for glass, pills, coloured icons, hover lift, SVG filters and forced active/hover paint. Inspect `#navbar.bg-dark`, compact state, `.nav-link.active`, `.dropdown.is-hover-open`, the 992–1359.98 open panel, 1360–1500 hide rules and phone equivalents. In `static/css/theme-dark.css` retire the unlayered forced navbar shadow/border/link colours. Check shared header overrides in `a11y.css`, Bootstrap utilities and JS-injected colour classes. Keep the existing fixed topbar, compact clearance and 1360 behaviour; keep #743's regular and compact panel positioning, scrollability and focus styles. Use existing frame tokens and Inter with one owner per new rule, no page bundle or additional `!important`. Inspect the normal and compact states separately.
6. **Verify wide and zoomed layout.** Establish a one-row scale-6 fit starting with the 32 px gutter and 1360 desktop breakpoint. Reclaim inter-group space and link padding first. Use compact utility labels with existing accessible names only if necessary. Keep destination labels and all controls. Test 1360/1440/1501/1601 at scale 8 in both themes. Distinguish a disabled increase-at-maximum from a missing button. If a single row fails, compare the existing navbar counter-zoom with a growing header that moves body clearance and panel origin to the measured bottom. Avoid fixed-height clipping. Record row count and full hit geometry on real pages before choosing the smaller reversible solution; bring competing fallbacks to the plan council.
7. **Re-pin deliberate contracts and update documentation.** Replace three-colour and Backup-pop expectations with inherited label colour and zero transform. Keep per-control tests and the brand-target guarantee when repinning its obsolete padding. Inspect `tests/test_css_wp4_4_navbar_contracts.py`, `tests/test_css_cascade_contracts.py`, `tests/test_css_wp4_4_a_baseline_contracts.py`, `tests/test_visual_selector_contracts.py`, `e2e/user-profile.spec.ts`, `e2e/dark-mode.spec.ts`, smoke and accessibility specs. Source census starts at 93 important declarations, 72 custom properties, 188 rules (99 layered/89 unlayered), two keyframes/five steps. Measure the actual result; replace only superseded pins including the old dark toggle indicator/container sizing. Preserve fixed positioning and layer ownership where still live. Update relevant fields in `docs/CSS_PHASE4_WP4_4_A_BASELINE.json`, `docs/product/DESIGN_BRIEF.md`, `docs/product/APP_FLOW.md` and any generated inventory required by the changed tests. Preserve asset staging treatment.
8. **Manual evidence, snapshots and release.** Capture ordinary after states from the same scratch fixture as the before evidence. Have fresh manual QA compare actual screens against the mockup before any regeneration. Record discrepancies, decisions, measurements and evidence paths. Run the scoped visual process below. Run affected pytest and functional E2E first, then full pytest, functional Chromium, both visual suites plus workout-plan desktop contracts, TypeScript, Vitest, inventory, pyright baseline and Stylelint as derived from changed paths. Run independent required code, manual and polish reviews. Verify Windows CI and a no-retry Linux compare actually ran on the final head. Record Gate 2 only after all required checks and reviews pass, squash-merge under the owner's conditions, and comment on #736.

### Exact visual update and controls

For each `e2e/__screenshots__/{win32,linux}/visual.spec.ts-snapshots/`, expand these existing stem/suffix combinations. Theme is `dark` or `light`.

| Stem | Allowed suffix before .png | Count per platform |
|---|---|---:|
| `welcome`, `workout-log`, `weekly-summary`, `session-summary`, `progression`, `body-composition`, `volume-splitter`, `backup`, `fatigue` | `-{mobile,tablet,desktop}-{theme}` | 54 |
| `workout-plan` | `-{mobile,tablet}-{theme}` | 4 |
| `user-profile` | `-{tablet,desktop}-{theme}` and `-mobile-{theme}-segment-1` | 6 |
| **Maximum** | | **64** |

Verify against actual files on the merged base. Record hashes of both Profile mobile `segment-2` PNGs and all 15 thumbnail PNGs per OS first. Full-page Workout Plan desktop light/dark and thumbnails `plan-desktop-light-advanced`, `plan-desktop-dark-advanced`, `plan-desktop-dark-simple` stay render-only. Desktop contract cases introduce no new PNG.

Each mobile Profile test checks segments sequentially. A segment-1 mismatch can prevent segment 2 from being compared. Independently run compare-only tail checks for both themes using the unchanged helper's measurement, deterministic preparation, clip and comparator settings before a Windows update can address either Profile title. Preserve original tail PNGs on any discrepancy, diagnose the layout and rerun. Validate the permitted Windows title expansion with `--list`, use changed-only updates on those titles and check paths and protected hashes afterward. Run the complete thumbnail suite in comparison mode. On Linux inspect generated tail images against committed controls using the comparison gate; copy only exact allowed files from the generation artifact. Recompute only changed manifest groups. An unlisted red is a regression to investigate. Keep both final native comparisons and their job logs.

### Council questions and provenance

- Select the smallest desktop scale-8 fallback which keeps every operation, the threshold and header/body clearance. Validate the resulting real geometry for regular and compact headers.
- Confirm the server-side parent indication, hamburger glyph and independently executable tail safeguards. Establish how to safeguard existing route-body regressions without taking on their redesign.

| Role | Agent ID | Status |
|---|---|---|
| Product manager, Section 0 and Plan v1 | `/root/nav_pm` | Author of canonical Section 0 and Plan v1 on the Navigation branch at base 006fa3fa |
| Product manager, matrix and Plan v2 | Pending | Resume after independent review |
| Architecture reviewer | Pending | Council has not run |
| Test strategist | Pending | Council has not run |
| Product-risk reviewer | Pending | Council has not run |

**Continuity, Gate 1 and Gate 2** are pending. Record the actual IDs, same-PM status and any evidence gap when the reviews take place. Record each delegated approval as “approved by Astra under the owner's delegation of 2026-11-27”.
