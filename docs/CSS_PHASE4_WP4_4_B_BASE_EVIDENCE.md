# WP4.4-b — `static/css/base.css` triage

Packet **b** of the WP4.4 shared-bundle arc. Gate 1 approved (owner, 2026-07-27,
rulings N1–N10); `b` became eligible when the `c`-first prerequisite was
discharged by PR #188.

**Result:** `base.css` 123 → **79 lines** (−44), pure deletion, 0 insertions.
Four blocks removed. **0 certifiable differing records** across 17,048
element-records in 22 route × theme contexts. All 22 page screenshots
byte-identical.

---

## 1. What was deleted, and why each block qualified

Two different justifications are in play, and the difference matters for
anything built on this packet later.

| Block | Lines | Basis | Rendered before deletion? |
|---|---|---|---|
| `.skeleton` | 93–102 | **cascade non-winner** — `motion.css` beat every declaration | no |
| `@keyframes skeleton-loading` | 104–111 | orphaned once the above lost its only `animation` reference | no |
| `.loading-spinner` | 82–90 | **unreachable** — no element in the app carries the class | no |
| `.fade-enter` / `.fade-enter-active` | 114–123 | **unreachable** — same | no |

### 1a. `.skeleton` — beaten by `motion.css` at equal specificity

`templates/base.html` loads `base.css` at line 19 and `motion.css` at line 27.
Both declare `.skeleton` at specificity (0,1,0), unlayered, without
`!important` — so source order decides and the later file wins. base.css wrote
exactly three properties; `motion.css:35-47` writes all three plus
`border-radius`, `color` and `border-color`.

Both declarations are shorthands, which is what makes this total rather than
partial: `background` and `animation` each reset their full longhand set, so
motion.css's copies overwrite every longhand base.css touched, including
`background-size` where the two files happened to declare the same value.

Measured on a synthetic `.skeleton` element across all 11 routes × 2 themes:

| Longhand | Read | Source |
|---|---|---|
| `animation-name` | `skeleton-shimmer` | `motion.css` |
| `animation-timing-function` | `linear` | `motion.css` (base.css set no timing function) |
| `background-image` | `linear-gradient(90deg, rgb(244,246,250) 25%, rgb(255,255,255) 50%, …)` | `motion.css` via `var(--surface-1)` / `var(--surface-2)` |
| `border-radius` | `14px` | `motion.css` |
| `color` | `rgba(0, 0, 0, 0)` | `motion.css` |

base.css's `skeleton-loading` never appeared in `animation-name` in any of the
22 contexts, and its `#f0f0f0`/`#e0e0e0` literals never appeared in
`background-image`. Deleting a non-winner cannot change a computed value (M8).

### 1b. The three unreachable classes

These rules were **not** overridden — a synthetic element carrying the class was
painted by them (`.loading-spinner` → `animation-name: spin`,
`border-radius: 50%`; `.fade-enter` → `opacity: 0`, `translateY(10px)`). They
were deleted because **no element ever carries the class**:

- **Census, 22 contexts:** 0 elements for `.loading-spinner`, `.fade-enter`,
  `.fade-enter-active` on every route in both themes.
- **Source reachability:** the strings appear in **no** `.html` and no `.js`
  file repo-wide. The only non-CSS hits anywhere are prose in `docs/`.
- **Dynamic construction ruled out:** every site that computes a class name at
  runtime resolves to a closed literal set — `toast.js:91-98` (`bg-*`),
  `volume-splitter.js:755-762` (`volume-value-pill--*`),
  `workout-plan-helpers.js:16-22` (`volume-value-*`),
  `workout-log.js:289` (`sort-asc`/`sort-desc`),
  `workout-dropdowns.js:442` (copies an existing element's `className`),
  `workout-plan-table.js:365` (superset classes),
  `exercise-video-modal.js:155` (Font Awesome icons). None can produce any of
  the three names.

**Precedent.** Deleting an unreachable rule rather than an overridden one is
established in this arc: WP4.3i-filter-btn removed five rules gated on a
`#filter-btn` that does not exist. The commutativity argument behind class-(a)
concurrency (§4c) holds a fortiori — a rule matching zero elements contributes
to zero computed values, so its removal commutes with any other packet's.

**This is the fragile half of the packet.** An unreachable rule becomes
reachable the moment someone adds the class name to a template.
`test_deleted_classes_are_still_unreachable` converts that from an assumption
into a gate: adding `class="loading-spinner"` to any template now fails pytest
with an explanation, rather than silently yielding an unstyled element.

---

## 2. What was retained — including three corrections to inherited claims

`docs/scan/PHASE_20.md` (the codebase grounding scan) nominated more of this
file than survived re-measurement. Three of its claims are **false** and are now
pinned by contract so they are not acted on later.

| Retained | Scan's claim | Measured reality |
|---|---|---|
| `@keyframes fadeIn` (`:70-79`) | dead, "backing the `.fade-enter*` classes" | **live.** `.fade-enter-active` animates via `transition`, not this keyframe. The real consumer is `layout.css:208` (`animation: fadeIn 0.8s ease-in-out`) — a different file. Deleting it with the `.fade-enter*` block would have broken that animation. |
| `.text-center`, `.text-muted`, `.text-danger` (`:56-67`) | redundant with Bootstrap's utilities | **live and sole source.** The compiled `bootstrap.custom.min.css` in this repo contains no rule for any of the three — the custom build excludes that part of the utilities API. The census found **40** live `.text-muted` elements across the route matrix. |
| `:root` custom properties (`:2-17`) | — | Retained under **M9**: no packet in this arc may delete a custom-property declaration under the non-winner rule. Resolving a `var()` dependency graph across all 21 hand-maintained sources is out of scope for a single-file packet. |

Also retained: `body`, `h1, h2, h3`, `h2`, `h3`, `p, label` — all measured live.

This is the second time in the arc that an inherited deadness claim has failed
re-verification (WP4.4-c corrected the `.is-success` ownership attribution).
Treat `docs/scan/` nominations as hypotheses, never as findings.

---

## 3. Oracles and controls

### 3a. Rest-state differential — the committed harness

`scripts/css_audit/runtime_probe.mjs` (WP4.4-a), run before and after the
deletion over 11 routes × 2 themes. Deliberately **not** run under the
`visual-helpers.ts` determinism tag, whose animation/transition zeroing is the
F1/F2 blind spot.

```
TOTAL: 17,048 element-records compared across 22 contexts
CERTIFIABLE DIFFERING RECORDS: 0
uncertifiable (animating) differing records: 2
page screenshots byte-identical: 22/22
harness self-checks (both runs): 22/22 PASS
  same-CSS control PASS · sentinel PASS · screenshot control PASS
```

### 3b. The 2 uncertifiable records, and why they are not this packet's

Two records differed on `welcome`, one per theme, on
`html/body[1]/main[1]/div[0]/div[0]/section[1]/div[1]/div[0]` — a `box-shadow`
blur radius moving by ~0.16px:

```
'rgba(99,102,241,0.59) 0px 0px 58.8787px 0px, …'
  ->  'rgba(99,102,241,0.59) 0px 0px 58.7187px 0px, …'
```

That element runs `pulse-glow 3s ease-in-out infinite`
(`pages-welcome.css:352-365`), which interpolates `box-shadow` from
`0 0 40px rgba(99,102,241,0.4)` to `0 0 60px rgba(99,102,241,0.6)`. The observed
values sit mid-interpolation. `pages-welcome.css` is a route bundle this packet
never opens.

**Cross-run control (the decisive check).** The harness's built-in same-CSS
control compares two captures *within* one run; it cannot certify a comparison
*between* two runs. So the harness was run a second time on the identical
post-deletion tree:

```
CROSS-RUN CONTROL (base_after vs base_after2, identical CSS): 2 differing records
  welcome--dark   box-shadow  58.7187px -> 58.7193px
  welcome--light  box-shadow  58.7185px -> 58.7193px
  uncertifiableElements: run1=8  run2=8  (same 8 paths, incl. this one)
```

Identical CSS reproduces the same two records on the same element. The
differential is therefore **0 certifiable records**, and the harness
independently registers that element as animating/uncertifiable in every run
(M12).

Worth recording: the harness reported `uncert=0` for `welcome` in the two full
runs and `uncert=8` in the welcome-only run. The animating-element detector is
itself phase-dependent, so `uncert=0` must not be read as "nothing on this route
animates."

### 3c. Bespoke oracle — census + synthetic elements

The rest-state differential is *silent* on both of this packet's claim types:
`.skeleton` elements are transient loading states and are absent at rest, and
the three unreachable classes are absent by definition. A differential over
elements that do not exist is trivially zero and proves nothing (M6).

A companion probe therefore injects a synthetic element per class on every
route/theme and reads the longhands. Its direction of proof is **opposite** to
the differential's — the deletion *must* change these:

```
.loading-spinner      changed in 22/22 contexts   (expected 22 — rule deleted)
.fade-enter           changed in 22/22 contexts   (expected 22 — rule deleted)
.fade-enter-active    changed in 22/22 contexts   (expected 22 — rule deleted)
.skeleton             changed in  0/22 contexts   (expected  0 — motion.css already won)
.text-muted           changed in  0/22 contexts   (expected  0 — retained by this packet)

sample:  .loading-spinner  animation-name 'spin' -> 'none'
                           border-radius  '50%'  -> '0px'
         .fade-enter       opacity        '0'    -> '1'
                           transform      'matrix(1,0,0,1,0,10)' -> 'none'

census (summed over 22 contexts):
  .loading-spinner   before=0   after=0
  .fade-enter        before=0   after=0
  .fade-enter-active before=0   after=0
  .skeleton          before=0   after=0
  .text-muted        before=40  after=40
```

Controls: **known-live (M5)** — `.text-muted`, a rule this packet retains, must
read differently from a bare `<div>`; PASS in 22/22 before and after.
**Negative** — a bare `<div>` reads inherited defaults. **Same-CSS (M1)** — the
whole capture runs twice per context and must agree exactly; PASS in 22/22.

The probe suppresses **transitions** before injecting, reading and removing
elements (**M6a**) but deliberately does **not** suppress animations:
`animation-name` is the value the `.skeleton` ownership claim turns on, and
zeroing it is precisely the F1 blind spot this oracle exists to route around.

The probe source is reproduced in §7; it is generated tooling and lives under
the gitignored `artifacts/`, matching WP4.4-c, which documented its bespoke
motion oracle rather than committing it.

---

## 4. Method rules and standing constraints

| Rule | How this packet satisfies it |
|---|---|
| **M1** | Sweep + rest-state differential + same-CSS control all present; the cross-run control in §3b is what makes the between-run comparison legitimate. |
| **M2** | Not applicable — no overpaint claim. Page screenshots are byte-identical in 22/22 anyway. |
| **M3** | Every synthetic capture is element-scoped. The full-page oracle is used only as a corroborating signal, never as the deciding one. |
| **M4** | No new specificity model written; ownership rests on equal specificity + source order, and is confirmed by computed values, not by a parser. |
| **M5** | Known-live control `.text-muted`, PASS 22/22 before and after. |
| **M6** | Every synthetic record asserts a visible effect; the deletion is required to *change* the synthetic probe (22/22), which is what stops the differential's silence from being vacuous. |
| **M6a** | Transitions suppressed across the whole probe window — apply, read, and remove. Animations deliberately left running (see §3c). |
| **M7** | The animated-logo red is treated as a band and never asserted as a pixel count. Observed here at 875/882 px, below the 1,039/1,046 previously recorded — see §5. |
| **M8** | `.skeleton` deleted as a proven non-winner. The three unreachable rules win nothing because they match nothing. No winning declaration was deleted. |
| **M9** | **Binding here.** No custom-property declaration deleted; all 12 `:root` properties retained and contract-pinned. |
| **M10** | The unreachable classes are exactly the JS-applied-class hazard M10 names. Discharged by source reachability + census rather than by a state capture, since no state can apply a name that appears in no template or script. |
| **M11** | No `@media` block in `base.css` at baseline or after (0 at both). |
| **M12** | Interaction states are **out of scope** for this packet, stated up front. No `:hover`/`:focus`/`:active` declaration was touched. The 2 animating records in §3b are bucketed, not attributed. |

| Constraint | Status |
|---|---|
| G1, G2, G3 | Untouched — this packet changes no shared selector ownership and never opens `components.css`. |
| G4 | Superset dark tint unacted. Superset row rendering identical: `workout-plan` differential 0/4,884 records in both themes. |
| G5 | `layout.css:1120` is packet **e**'s, not touched. |
| G6 | The ten frozen Workout Plan interaction-state declarations neither reopened nor resurrected — no specificity anywhere changed. |
| G7 | WP4.3i-c Page Header contract untouched and passing. |
| G8 | WP4.3i-jm / WP4.3i-o not re-dispatched. |
| G9 | `REGION_H_SHA256` unchanged and passing. |
| G10 / N2 | `base.css` declares no `@layer` before or after; no rule's layer membership changed. Contract-pinned. |
| G11 | No `@layer` block deleted — none exists in this file. |

---

## 5. Gates

| Gate | Result |
|---|---|
| `pytest tests/test_css_wp4_4_base_contracts.py` | **8 passed** |
| `pytest tests/` (full suite) | **2,204 passed, 1 skipped** (528.96s) |
| `accessibility.spec.ts`, `dark-mode.spec.ts`, `smoke-navigation.spec.ts`, `summary-pages.spec.ts`, `fatigue.spec.ts` | **68 passed** |
| `visual.spec.ts`, all 6 variants × 11 routes | **65 passed, 1 failed** — the ledgered known red, see below |
| Stylelint, seven surfaces, vs pinned a-baseline | **−2**, no rule increased |
| V2 mechanical check | 0 paths under `e2e/__screenshots__/`; 0 changes to `e2e/visual-helpers.ts` |

The gate set follows Plan v2's consolidated specification, which adds
`accessibility.spec.ts` (F19), `summary-pages` and `fatigue` (PR#7) to the v1
packet table.

### The one visual failure is pre-existing

`workout-plan desktop dark` failed at **875 pixels** (retry 882), above the
`maxDiffPixels: 800` tolerance. This is the animated-logo known red that the
WP4.4-a baseline evidence already records as "a real snapshot failure of
`workout-plan-desktop-dark`, not a diff the option absorbs."

Proven pre-existing by direct control: `base.css` was reverted to HEAD in the
same worktree and the same single test re-run, producing **the identical
failure — 875 pixels, retry 882**. The red is independent of this packet.

Per M7 the band is not an invariant. This run widens the recorded range: 875/882
here against 1,039/1,046 previously. Nobody may "fix" it by raising
`maxDiffPixels` (F3), and no snapshot was rebaselined (V2).

### Stylelint attribution

The pinned baseline sits at packet **a**'s commit, so a naive delta credits this
packet with packet **c**'s already-merged `motion.css` reduction. Measured
against merged `main` instead:

| Surface | a-baseline | merged main | this branch | **this packet** |
|---|---|---|---|---|
| `base.css` | 15 | 15 | 13 | **−2** |
| `motion.css` | 16 | 10 | 10 | 0 *(packet c)* |
| all seven | 2,883 | 2,877 | 2,875 | **−2** |

Both removed warnings are `declaration-property-value-disallowed-list` (raw
literals). `selector-max-specificity`, `selector-max-id`,
`declaration-no-important`, `no-duplicate-selectors` and
`declaration-block-no-duplicate-properties` are all unchanged — V3 and V4 hold.

---

## 6. Preservation invariants

| # | Verdict |
|---|---|
| **V1** | **PASS** — 0 certifiable differing records / 17,048; 22/22 screenshots byte-identical; `visual.spec.ts` reproduces only the ledger red, proven pre-existing by control. |
| **V2** | **PASS** — no `--update-snapshots`; 0 screenshot paths and 0 `visual-helpers.ts` changes in the diff. |
| **V3** | **PASS** — `selector-max-specificity` +0, `selector-max-id` +0; `base.css` remains `!important`-free (0 at baseline, 0 now), contract-pinned. |
| **V4** | **PASS** — `no-duplicate-selectors` +0, `declaration-block-no-duplicate-properties` +0. |
| **V5** | Contribution: **44 lines** against the 30,768-line Phase-4 denominator (0.14%). The packet's projection was −0 to −10; the measurement is −44. Per PR#13 the projection is a measurement to be corrected, not an acceptance criterion — recorded, and the scope was **not** widened to chase it. |
| **V6** | No conflict arose. |

---

## 7. Reproducing this

```bash
# rest-state differential + same-CSS + sentinel + screenshot controls
node scripts/css_audit/runtime_probe.mjs --out artifacts/wp4_4/base_before
#   … apply the deletion …
node scripts/css_audit/runtime_probe.mjs --out artifacts/wp4_4/base_after
# cross-run control on identical CSS
node scripts/css_audit/runtime_probe.mjs --out artifacts/wp4_4/base_after2 --routes welcome

# stylelint, seven surfaces
node scripts/css_audit/stylelint_surfaces.mjs artifacts/wp4_4/stylelint_after.json
```

The bespoke census/synthetic probe and the three analysis scripts
(`base_probe.mjs`, `diff_runs.py`, `control_diff.py`, `redpath.ps1`) are
generated tooling under the gitignored `artifacts/`. `base_probe.mjs` boots the
app on a throwaway `DB_FILE`, walks the 11 routes × 2 themes, counts elements
per class, injects one synthetic element per class with transitions suppressed,
and captures 28 longhands per element, running each capture twice for the
same-CSS control.

### F16 — red-path proof

Every contract was proven to fail under its own violation before being trusted.
Nine mutations, nine isolated reds, each turning exactly one test (`1 failed,
7 passed`):

| Mutation | Test turned red |
|---|---|
| restore the deleted `.skeleton` block | `test_cascade_dead_skeleton_block_stays_deleted` |
| restore `@keyframes skeleton-loading` | `test_cascade_dead_skeleton_block_stays_deleted` |
| restore the `.loading-spinner` rule | `test_unreachable_classes_stay_deleted` |
| reference `loading-spinner` from a template | `test_deleted_classes_are_still_unreachable` |
| delete `@keyframes fadeIn` | `test_fadein_keyframes_are_retained_and_still_consumed` |
| delete `.text-muted` | `test_bootstrap_text_utilities_are_retained` |
| delete the `--glass-blur` custom property | `test_element_defaults_and_tokens_are_retained` |
| introduce `!important` into `base.css` | `test_base_css_remains_important_free_and_unlayered` |
| delete `motion.css`'s `.skeleton` | `test_motion_css_still_owns_the_skeleton_family` |

The last one is a cross-file contract: it fails on a change to a file this
packet does not own. That is deliberate — `base.css` no longer carries a
skeleton fallback, so a future packet deleting `motion.css`'s `.skeleton` would
silently strip the loader of all its paint. The gate belongs with the premise it
protects.

---

## 8. Out of scope

- **`pages-workout-plan.css:5009`** also defines `.loading-spinner`, and it is
  unreachable for the same reason. It is a **route** bundle, outside packet b's
  exclusive path. Recorded here; not touched.
- Interaction states (`:hover`/`:focus`/`:active`) — declared out of scope up
  front per M12.
- Token extraction from the retained rules (`#333`, `#222`, `#6c757d`,
  `#dc3545`, the mesh-gradient literals). That is re-weighting, not deletion,
  and F17 restricts class-(a) concurrent packets to pure deletion; attempting it
  would reclassify this packet out of the concurrent set.
