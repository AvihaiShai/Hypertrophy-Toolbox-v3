# Fatigue Body Heatmap — Planning

**Status:** **Gate 0 CLOSED** (owner walk 2026-08-13, six locked decisions in §0).
**Gate 1 CLOSED** — council run 2026-08-13, Plan v2 below is the approved plan.
**Implemented** on `wt/fatigue-heatmap` (PR #339), reviewed a second time against the built
code — see §6.

**Goal:** On `/fatigue`, color a MuscleMap body figure by each muscle's fatigue band so the
user sees at a glance where load is concentrated. Picks up the deferred item in
[`PHASE2_PLANNING.md`](PHASE2_PLANNING.md) §3.

This is a **visualization** of data the fatigue meter already computes — it adds no fatigue
math and changes no thresholds.

---

## §0 — Owner-locked decisions (Gate 0)

| # | Decision | Locked choice |
|---|---|---|
| **L1** | Middle-Shoulder region coverage | **Colors both** front- and rear-delt regions. |
| **L2** | Metric basis | The **existing per-muscle band**, following the page's existing planned/logged state and the current period selector. **No new metric basis.** |
| **L3** | Color scale | **Four discrete existing band colors**, not a gradient. |
| **L4** | Placement | **Separate collapsible panel above** the detailed bar list. Collapsed state remembered **only if an existing page-local pattern supports it without new persistence**. |
| **L5** | Unranked muscles | Render **neutral gray and remain visible**. |
| **L6** | Cosmetic head | Keep the **current flat-gray head**; no demo hair. |

**Not authorized:** any API, schema, fatigue-formula, threshold, calibration, recommendation,
or suggestion-number change. The fatigue calculation must not be forked.

---

## §1 — Ground truth

1. `build_fatigue_page_context()` **already** returns `muscle_rows` — one dict per muscle with
   `{muscle, planned|None, logged|None, has_landmarks, max_percent_of_mrv, max_score}`
   ([`utils/fatigue_data.py:384`](../../utils/fatigue_data.py)). **No route or util change is needed.**
2. The period selector is a plain GET form, so a period change is a full server round-trip.
   Embedded data cannot go stale on period change — there is no client-side period state.
3. `templates/fatigue.html` loads **no route CSS bundle and no JS**. All fatigue styling lives in
   `scss/_fatigue.scss` → compiled into `static/css/bootstrap.custom.min.css`, which
   `templates/base.html:15` loads on **every page**. `e2e/fixtures.ts:91` documents this route as
   the app's highest shared-CSS exposure.
4. `.muscle-region` paths carry **no inline `fill`**, so CSS fully controls them. Cosmetic parts sit
   in a non-interactive `<g class="body-outline">` whose head is already flat gray `#d9dee4`
   — **L6 requires no work.**
5. Region keys actually drawn (union = 17): anterior `neck, front-deltoid, chest, biceps, triceps,
   forearms, abs, obliques, adductors, quadriceps, calves`; posterior `neck, rear-deltoid,
   trapezius, lats, lower-back, triceps, forearms, gluteal, hamstring, calves`.
6. The band palette already exists: `.fatigue-{light,moderate,heavy,very-heavy}` + `.fatigue-unranked`,
   with full dark-mode variants. **L3 and L5 are pure reuse.**
7. `/fatigue` **is** in the visual matrix, so a panel moves 6 captures per platform.
8. `e2e/visual-helpers.ts` has a `TERMINAL_MARKERS` hook that blocks a capture until a page-specific
   sentinel attaches.

### Errors in the pre-council draft
- The draft mapped an **`upper-back`** region. The SVGs draw no such region — the vendor README
  confirms `upper-back` and `hip-abductors` are legend-only.
- The draft omitted **`obliques`**. `canonicalize_muscle_for_fatigue('External Obliques')` returns
  **`Abdominals`** (a ranked muscle), so it is a real mapping decision, not an omission.
- The draft's §4 also called `moderate` yellow. It is **blue** `#0d6efd` (`scss/_fatigue.scss:165`).

---

## §2 — Council record (Gate 1)

Reviewers: **A** = `architecture-reviewer`, **T** = `test-strategist`, **P** = `product-risk-reviewer`,
run in parallel on Plan v1, 2026-08-13, then again on the implementation. Every finding has a row.

Agent identifiers are not surfaced into repository artifacts by this harness, so none are cited.

### Response matrix

| # | Finding | Rev | Disposition | Action in v2 |
|---|---|---|---|---|
| 1 | Heatmap does not render at all in the required functional gate — `prepare_e2e_db.py` wipes plan+logs and `fatigue.spec.ts:66` erases mid-file | A,T | accept | New describe placed **above** the existing one, self-seeding via `POST /add_exercise`; also asserts the panel is absent on the empty state. |
| 2 | Six stale Linux baselines red the weekly `visual-linux` cron | A | accept (scoped) | Explicit owner follow-up in PR body + handover. Does not block merge: `visual-linux` is schedule/dispatch-only and not one of the 11 required contexts. The 2026-08-17 deep-gate validation checks *job execution*, not greenness, so it is unaffected. |
| 3 | `TERMINAL_MARKERS` on a conditionally-rendered element hard-fails instead of skipping | A,T | accept | `data-heatmap-state` moves to the **always-rendered** page `<section>` with values `ready`\|`empty`; marker registered as `[data-heatmap-state]`. |
| 4 | Two figure columns → 4 duplicate DOM `id`s + 4 copies of the SVG's inline `<style>` | A | accept | Dissolved by the Q1 ruling — 2 SVGs, and anterior/posterior ids differ, so no duplicate exists. |
| 5 | Per-region `role="img"`/`aria-label` are **inert**: the SVG root already has `role="img"`, making descendants presentational | A | accept | Per-region ARIA dropped. Root `<svg>` carries the channel/side label. Per-region `<title>` kept **only** as a sighted-user hover tooltip; no a11y claim is made for it. |
| 6 | `fill: var(--fatigue-accent-strong)` with no fallback → black silhouette; the 727-viewBox `stroke-width` never reaches `/fatigue` | A | accept | `var(..., <neutral>)` fallback, explicit `stroke-width: 0.9`, and the JS always writes exactly one of five band classes. |
| 7 | Any new `d-*` utility reds `test_css_display_utilities_contracts.py`; `fatigue.html:22` is pinned in `KNOWN_INERT` | A,T | accept | **No `d-*` class** in the new partial or module; line 22 untouched. |
| 8 | `.text-muted`/`.text-center`/`.text-danger` in the new SCSS reds `test_css_wp4_4_base_contracts.py:149` | A | accept | Those names never appear in `_fatigue.scss`; asserted by a new test. |
| 9 | Any literal `.css` substring (or `page_css`) in `fatigue.html` reds `test_visual_selector_contracts.py:134` | A | accept | Neither appears. Recorded as an implementer constraint. |
| 10 | A bare `.muscle-region` rule in the globally-loaded bundle silently repaints two other pages | A | accept | All selectors scoped under `.fatigue-heatmap`, made **mechanical** by a new test asserting no `.muscle-region` in the bundle except immediately preceded by `.fatigue-heatmap `. |
| 11 | Extend the `test_css_cascade_contracts.py` tuple with `.fatigue-heatmap` | A | **reject** | That file is amendable only by WP4.4 packet **i** (`test_css_wp4_4_a_baseline_contracts.py:675-704`). Equivalent guarantee obtained in the new test file instead. |
| 12 | Must not call `annotateBodymapPolygons` (writes Profile-specific data from a different mapping) | A | accept | Module imports only `loadBodymapSvg`; asserted by a source-text test. |
| 13 | Importing `bodymap-svg.js` places ~160 lines of Profile-only data on `/fatigue` | A | accept (documented) | Recorded as a known coupling; not refactored — splitting that module is out of scope. |
| 14 | `docs/MASTER_HANDOVER.md` missing from the file list | A | **defer** | Owner instruction for this session forbids concurrent MASTER_HANDOVER edits. Recorded in `MASTER_HANDOVER.local.md`. |
| 15 | `visual-windows` (`ci.yml`, the `visual-windows:` job — line 549 when this row was written, **626** at `116d3c5`) runs on **every PR** and byte-compares all 66 win32 `visual.spec.ts` baselines on `windows-2022`. It does **not** cover the 15 thumbnail captures | T | accept | Promoted to a first-class gate: after regenerating the six PNGs, confirm **Visual Regression (Windows baselines)** is green before treating them as accepted. A red is never answered with `--update-snapshots`. |
| 16 | The module `<script>` must carry `?v={{ app_version }}` **outside** `url_for()` or `test_version.py` reds | T | accept | Exact markup pinned; the literal `random` must not appear. |
| 17 | `test_version.py` node count moves 22 → 23 (new partial picked up by `rglob`) | T | accept | Handled by regenerating the test inventory. |
| 18 | Never add a screenshot assertion to `fatigue.spec.ts` — `test_no_screenshot_spec_is_benchmarked` would red **pytest** | T | accept | Implementer constraint; visual coverage stays in `visual.spec.ts`. |
| 19 | Module must be importable with zero DOM/fetch side effects (vitest runs in node env) | T | accept | Pure exports at top; mounting behind `initFatigueHeatmap()`, self-invoked on `DOMContentLoaded` only. |
| 20 | Mutation-test the vitest cases: assert the returned **band**, not just the muscle | T | accept | Every case asserts the band; plus a nonsense-band passthrough case. |
| 21 | flake8 `F401` and `tsc --noEmit` are blocking CI jobs | T | accept | Both in the local gate list. |
| 22 | Seven-surface Stylelint does **not** apply (`bootstrap.custom.min.css` is excluded) | T | accept | Recorded so the gate is not over-escalated; `npm run lint:css` still covers `scss/**`. |
| 23 | Compiled-CSS drift gate (PR #335) is **not** on `main`; rebuild is discipline, not a gate | T | accept | Rebuild + commit bundle **and** `.map`; repair the autocrlf phantom with `git checkout-index -f`. |
| 24 | `prepareForScreenshot`'s inline stage never reaches a late-mounted SVG → recommend server-rendering | T | **reject (measured)** | The inline stage targets only `[data-visual-control], input, textarea, select` (`visual-helpers.ts:251-260`) — an SVG `<path>` matches none at any mount time. The `addStyleTag` stage uses `*` with `!important` (live CSS, reaches late nodes), and `prepareForScreenshot` opens with `waitForLoadState('networkidle')`, which already awaits the fetch. Server-rendering would also need a Jinja loader change (SVGs live outside the template root), destroying the zero-Python-change property. Mitigations 3 + 25 adopted instead. |
| 25 | Flip the marker after paint, not after mount | T | accept | `ready` is set inside a `requestAnimationFrame` after the last band class; and `.fatigue-heatmap .muscle-region` declares only `fill`/`stroke`/`stroke-width` — nothing a neutralizer could miss. |
| 26 | `git add` the new files or the packaged-smoke job fails | T | accept | Explicit step. |
| 27 | Front-delt region can show a **false low** — `Front-Shoulder` has no landmarks and drives no region, so press volume is invisible while the delts show lateral-raise load | P | accept | L1 preserved. Mitigated by a per-region `<title>` naming the source muscle plus a panel note. |
| 28 | Five mapped regions can never render `light`; `Abdominals` can never render `heavy` — cross-region color comparison is invalid | P | accept (verified) | Independently reproduced: `Glutes`/`Traps`/`Forearms` have `MEV = 0`; `Abdominals` is `(0, 6, 25, 25)` so `MAV_high == MRV`. **Every region's `<title>` carries the `%` of range**, so the number travels with the color. A characterization test records the reachable set. **No threshold change.** |
| 29 | With an empty `workout_log` the whole Logged figure is gray, reading "you trained nothing" | P | accept | A channel's figure renders **only** when that channel has data; otherwise that channel's empty-state line renders in its place. |
| 30 | One gray conflates "no reference range exists" with "no volume in this window" | P | accept | One swatch, differentiated in the `<title>`. |
| 31 | Legend labels drift from shipped vocabulary ("Lighter", "Not assessed") | P | accept | Exactly `Light · Moderate · Heavy · Very heavy · No reading`; sentences use the `_BAND_LABELS` lowercase forms. |
| 32 | `<summary>` and panel-note copy — the first strings every user reads — left unspecified | P | accept | Pinned verbatim in §4. |
| 33 | Palette is not perceptually ordered (green → **blue** → amber → red) and the map makes color the sole encoding | P | accept | Colors unchanged (L3); legend is an explicitly ordered list with a `lower → higher` caption. |
| 34 | Painted **area** is an implicit quantity encoding; two muscles each paint two regions | P | accept | Covered by 27/30 — identical source-muscle naming on both members of each shared pair. |
| 35 | Stage-4 felt-band evidence before vs after ship is not cleanly comparable | P | accept (relocated) | Ship date recorded in §5 **here** rather than in `calibration-notes.md`, because a concurrent session holds uncommitted edits to that file. **No threshold change.** |
| 36 | Migration notes not stated | P | accept | PR body states them explicitly. |
| 37 | `row.muscle` is an arbitrary DB string — never `innerHTML` | A | accept | Implementer constraint + a pytest case using a `</script>` label. |
| 38 | Draft §3 mapped a non-existent `upper-back` region and omitted `obliques` | — | accept | Corrected in §3; a both-directions set-equality test makes the error class unreproducible. |
| 39 | Draft §4 called `moderate` yellow | P | accept | Corrected — it is blue `#0d6efd`. |

### Q1 — adjudicated (the reviewers disagreed)

**P** argued for two figure columns and against a channel control (a hidden channel risks reading
planned intent as logged reality). **A** argued for one figure + a control on measured grounds:
two columns mount 4 SVGs → 4 duplicate DOM `id`s, 4 copies of the SVG's inline `<style>`,
~226 region nodes, and push the panel past the fold at 375×812.

**Ruling: one channel at a time; front *and* back both visible side by side; a segmented
Planned/Logged control; and a permanently visible caption naming the active channel.**

- Smaller on every axis **A** raised — **2** SVGs, not 4. Anterior and posterior ids differ, so the
  duplicate-`id` defect disappears rather than being patched around.
- It also *removes* the front/back toggle the draft proposed, so the panel has **one** control.
- **P**'s misreading risk is closed by the permanent caption: the active channel is always stated in
  visible text beside the figure, not merely implied by a pressed state.
- L2's literal wording — "follows the page's existing planned/logged **toggle**" — points here.
- Per finding 29, when only one channel has data **no control renders at all**. With the live DB at
  0 logged rows, that is today's actual state.

### Q2 — `obliques` → `Abdominals`
Confirmed by both **A** and **P**. `utils/volume_taxonomy.py:97` is literally
`"External Obliques": "Abdominals"`, so the accumulator already folds oblique work into that bar;
leaving the region gray would make the figure contradict the bar list in the more damaging
direction. Condition: `abs` and `obliques` carry the **identical** `<title>`. Visual consequence
recorded so it is not read as a bug: 16 oblique paths + 8 abs paths render one color.

---

## §3 — Canonical region → fatigue-muscle mapping

Single-valued **region → muscle**.

| Region key | Fatigue muscle | Note |
|---|---|---|
| `chest` | Chest | |
| `lats` | Latissimus-Dorsi | |
| `front-deltoid` | **Middle-Shoulder** | **L1** |
| `rear-deltoid` | **Middle-Shoulder** | **L1** |
| `biceps` | Biceps | |
| `triceps` | Triceps | front + back |
| `quadriceps` | Quadriceps | |
| `hamstring` | Hamstrings | |
| `gluteal` | Glutes | |
| `calves` | Calves | front + back |
| `abs` | Abdominals | |
| `obliques` | Abdominals | External Obliques canonicalizes to Abdominals |
| `trapezius` | Traps | |
| `forearms` | Forearms | front + back |
| `neck` | — | unmapped → neutral gray (**L5**) |
| `adductors` | — | unmapped → neutral gray (**L5**) |
| `lower-back` | — | unmapped → neutral gray (**L5**) |

Consequence of **L1**: the unranked `Front-Shoulder` / `Rear-Shoulder` labels drive no region, and
`Middle-Traps` likewise (Traps owns `trapezius`). Those muscles keep their existing bars — nothing
is hidden, and the panel note says so.

---

## §4 — Pinned user-facing copy (D2.10: descriptive, no verbs, no MRV/MEV)

- `<summary>`: **Body map**
- Panel note: **Colors show each muscle's band for the selected period. Regions without a reading stay gray.**
- Shoulder note: **Shoulder regions show Middle-Shoulder; the upper-back region shows Traps. Front-Shoulder, Rear-Shoulder and Middle-Traps are listed separately below.** *(Corrected to the shipped copy. §6 finding #42 widened this note to cover Traps/Middle-Traps and moved it above the figures; a stale second copy of the older sentence survived at the foot of the panel until it was removed. Until this correction, §4 was the last place in the repository asserting the deleted sentence was current — which invited its reintroduction. `tests/test_fatigue_heatmap_mapping.py` now asserts the note renders exactly once.)*
- Legend caption: **Lower → higher**
- Legend items: **Light · Moderate · Heavy · Very heavy · No reading**
- Channel caption: **Showing: Planned** / **Showing: Logged**
- Region `<title>`, mapped with data: **Chest — heavy · 78% of typical recoverable range**
- Region `<title>`, mapped without data: **Chest — no volume in this window**
- Region `<title>`, unmapped: **Neck — no typical range yet**

The page-level "Descriptive only" line already exists at `templates/fatigue.html:10-12` and is not repeated.

### Collapsed-state persistence (L4)
**None.** The only in-repo collapse-persistence pattern is `plan_volume_panel.js`, which owns a
`localStorage` key on the *workout-plan* page; reusing it would mean a **new** key, which L4's
"without new persistence" clause forbids. The panel defaults to open.

---

## §5 — Plan v2

**Scope — In:** collapsible `<details open>` panel above `.fatigue-page__bars`, front + back figures
side by side; segmented Planned/Logged control (only when both channels have data) plus a permanent
active-channel caption; the §3 mapping; ordered textual legend; per-region hover `<title>` carrying
muscle · band · % of range; dark mode and 375px layout by reusing existing tokens and the existing
breakpoint.

**Scope — Out:** no API, schema, route or util change; no fatigue math, threshold, landmark or
`SCENARIOS` edit; no new CSS bundle, `<link>`, E2E spec file or required CI check; no persistence of
the collapsed state; no Linux baseline regeneration (owner follow-up).

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `static/js/modules/fatigue-heatmap.js` | new | Pure exports at top; mounting behind `initFatigueHeatmap()`. Imports only `loadBodymapSvg`. |
| `static/js/modules/__tests__/fatigue-heatmap.test.js` | new | vitest, node env. |
| `templates/_fatigue_heatmap.html` | new | No `<main>`, no `role="main"`, no `d-*`. |
| `tests/test_fatigue_heatmap_mapping.py` | new | Mapping / palette / plumbing contracts. |
| `templates/fatigue.html` | modify | Partial include, embedded JSON, versioned module script, `data-heatmap-state`. No `.css` substring, no `page_css`, line 22 untouched. |
| `scss/_fatigue.scss` | modify | `.fatigue-heatmap`-scoped block only. |
| `static/css/bootstrap.custom.min.css` + `.map` | rebuilt | `npm run build:css`. |
| `e2e/fatigue.spec.ts` | modify | New describe above the existing one, self-seeding. No screenshot assertion. |
| `e2e/visual-helpers.ts` | modify | One `TERMINAL_MARKERS` entry. |
| `e2e/__screenshots__/win32/visual.spec.ts-snapshots/fatigue-*.png` | regenerated ×6 | Scoped `-g`, never a blanket update. |
| `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` | modify | **One** value: the win32 `nameAndSizeSha256`. Never `emit_baseline.py`. |
| `docs/test_inventory/TEST_INVENTORY.{md,json}` | regenerated | |
| `docs/fatigue_meter/HEATMAP_PLANNING.md` | modify | This document. |

**NOT touched** (regression flag if they move): `utils/fatigue.py`, `utils/_fatigue/**`,
`utils/fatigue_data.py`, `routes/fatigue.py`, `app.py`, `tests/conftest.py`,
`templates/_fatigue_muscle_bar.html`, `static/js/modules/bodymap-svg.js`, the SVG assets,
`tests/test_css_cascade_contracts.py`, `docs/MASTER_HANDOVER.md`,
`docs/fatigue_meter/PHASE2_PLANNING.md`, `docs/fatigue_meter/calibration-notes.md`
(the last two are held by a concurrent session), and any threshold / landmark / scenario.
**Known coupling:** importing `bodymap-svg.js` places its Profile-only constants on `/fatigue`.

**Expected gates:** full pytest; `npm run test:js`; e2e `fatigue`, `visual` (win32,
`PW_VISUAL_SEED=1`), `accessibility`, `dark-mode`, `smoke-navigation`; `npm run build:css`;
`scripts/generate_test_inventory.py`; `npx tsc --noEmit`; flake8; `npm run lint:css`.
CI watch: **Visual Regression (Windows baselines)** — non-required but runs on every PR.

### §6 - Post-implementation review (same three reviewers, on the built code)

Three defects survived Plan v2 and were caught only by reviewing the shipped diff. All are fixed.

| # | Finding | Rev | Fix |
|---|---|---|---|
| 40 | **The channel control could never appear.** The partial ships it `hidden`; the module only ever set `hidden = true`, and reboot's `[hidden]{display:none !important}` meant the container beat its children un-hiding. The two-channel path had zero coverage - the one E2E asserting it seeded planned data only and passed for the wrong reason. | A, unslop | Assign both ways. A new E2E seeds an exported **and scored** log (an unscored export produces no bar), then asserts the control appears, the caption flips, `aria-pressed` swaps, and exactly one band class survives the repaint. |
| 41 | **`data-heatmap-state` could strand at `pending`.** The panel gates on raw row counts, the module on aggregated bars; a row whose sets resolve to 0 satisfies the first and not the second. The module returned early without flipping the marker, so all six visual captures would die on an opaque timeout - the exact failure the template comment claimed impossible. | A, P | Every exit is now terminal (double `requestAnimationFrame`, since one callback runs before that frame's paint). The zero-aggregate branch shows *"No set volume in this window."* rather than leaving the figure fallbacks blaming the asset loader. Covered by pytest; it is not reachable through the app's own endpoints, which the test records. |
| 42 | **`trapezius` carries the same false low as the delts, and had no caveat.** `volume_taxonomy` routes the common `Upper Back` catalog label into the unranked `Middle-Traps` bucket, which paints no region, while the upper-back region shows `Traps`. The shipped copy named only the shoulders. | P | Caveat extended to name Middle-Traps, and **moved above the figures** - it has to reach the reader before the gray region it explains, and the per-region title is hover-only so touch users never see it. |

Also applied: copy now says *"fatigue band"* and *"Lower → higher fatigue"* rather than the bare noun;
dead code removed (an unused parameter, a write-only dataset attribute, an identity map, two
`[hidden]` rules redundant against reboot); duplicated assertions cut from all three test layers.

Confirmed clean by review: **no DOM-XSS path** (the database-derived muscle label never reaches the
DOM - it is only ever a lookup key, and the one `innerHTML` takes a hardcoded same-origin asset), no
contract drift, `paint()` cannot leave a stale or doubled band class, and the `<title>` insertion is
correct for SVG and idempotent across repaints.

### Owner follow-up
**Linux visual baselines for `/fatigue` are stale after this ship.** Regenerate via the
`visual-linux` deep-gate job (`run_visual=true`, `visual_mode=generate`) and commit the six PNGs;
CI never pushes pixels. Until then the weekly `visual-linux` compare run reds on those six captures
only.
