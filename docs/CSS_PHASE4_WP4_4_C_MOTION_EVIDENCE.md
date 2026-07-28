# WP4.4-c — `motion.css` triage

*Phase 4 CSS. Pure deletion of proven non-winners. Plan:
[`docs/css_phase4_wp4_4/PLANNING.md`](css_phase4_wp4_4/PLANNING.md) (Gate 1 approved, rulings N1–N10).*

**Base:** `wt/wp4-4-c-motion` from `main` @ `6ebf4b1`, worktree seeded `-Seed visual`.
**Baseline cited:** [`docs/CSS_PHASE4_WP4_4_A_BASELINE.json`](CSS_PHASE4_WP4_4_A_BASELINE.json) (F13 — every number below appears there or is measured here).

---

## 1. Outcome

**Three declarations deleted, all from `.is-success`, all proven non-winners.
Everything else in the file was measured live and retained.**

```diff
 .is-success {
   animation: success-pulse 1s var(--ease-out, ease) !important;
-  background-color: var(--success, #10b981) !important;
-  border-color: color-mix(in srgb, var(--success, #10b981) 80%, white 20%) !important;
-  color: #ffffff !important;
 }
```

`motion.css` **71 → 73 lines** (three declarations removed, a five-line comment added recording why). No selector was rewritten, no declaration re-weighted, no `@layer` membership touched (N2), and no behaviour changed.

---

## 2. Why these three, and only these three

`.is-success` is applied by `static/js/modules/workout-plan-add-exercise.js:275-278` to **`#add_exercise_btn`** and to nothing else in the codebase, for 1,000 ms after a successful add. That makes the whole rule an **M10 declaration** — reachable only through a JS-applied class, and therefore non-deletable *unless proven under that state*.

It was proven under that state, on the real element, in both themes, with M6a applied.

| Property | before `.is-success` | after `.is-success` | verdict |
|---|---|---|---|
| `background-color` | `rgb(76, 110, 245)` | `rgb(76, 110, 245)` | **non-winner** |
| `color` | `rgb(255, 255, 255)` | `rgb(255, 255, 255)` | **non-winner** |
| `border-top-color` | `color(srgb 0.452471 0.556471 0.969412)` | *unchanged* | **non-winner** |
| `border-right-color` | *as above* | *unchanged* | **non-winner** |
| `border-bottom-color` | *as above* | *unchanged* | **non-winner** |
| `border-left-color` | *as above* | *unchanged* | **non-winner** |
| `animation-name` | `none` | **`success-pulse`** | **winner — retained** |
| `animation-duration` | `0s` | **`1s`** | **winner — retained** |

**The positive control passes on the same element** (M5): the sweep demonstrably *can* detect a live declaration on `#add_exercise_btn`, because it detected the animation. A probe that changed nothing would have proved nothing (M6).

**M6a was applied and was necessary.** `transition-property: none` is set inline *before* the class is added and released only *after* the read; the button carries a transition, so an unsuppressed read returns the pre-class value and would have reported the animation as dead too.

### What beats them — the layered `!important` inversion (G10 / A6)

`.is-success` in `motion.css` is **unlayered** and `!important`, at specificity `(0,1,0)`.

The declarations that actually render are `components.css:3540-3548`, which sit **inside `@layer workout`** (opened at `components.css:3539`) and are **also `!important`**:

```css
@layer workout {
#workout[data-page="workout-plan"] .btn.btn-calm-primary,
#workout[data-page="workout-plan"] :where(.btn).btn-calm-primary,
#workout[data-page="workout-plan"] .modal-content.frame-calm-glass .btn.btn-calm-primary {
  background: var(--accent, #4c6ef5) !important;
  border: 1px solid color-mix(in srgb, var(--accent, #4c6ef5) 78%, white 22%) !important;
  color: var(--accent-ink, #ffffff) !important;
  …
}
```

**In the important half of the cascade, layer order is inverted.** For normal declarations, unlayered rules beat layered ones; for `!important` declarations the ordering reverses and **unlayered `!important` is the weakest tier**, so a layered `!important` outranks every unlayered `!important` *regardless of specificity*. This is exactly the mechanism recorded as **G10** and council finding **A6** in `docs/css_phase4_wp4_4/PLANNING.md:165-170`, and it is why **N2** freezes layer membership arc-wide.

`#add_exercise_btn` carries `class="btn btn-primary btn-calm-primary"` (`templates/workout_plan.html:247`) inside `<div id="workout" data-page="workout-plan">` (`:10`), so the layered block matches it on every render. **`.is-success` therefore could never win `background-color`, `border-*-color` or `color` on that element — in either theme, in any interaction state, at any specificity it could have been given.** The three deleted declarations are dead by cascade construction, not merely dead by measurement.

The measured values are the layered block's own, to the digit:

| Property | Winning declaration (`components.css:3540-3548`, `@layer workout`, `!important`) | Computed |
|---|---|---|
| `background-color` | `background: var(--accent, #4c6ef5)` | `rgb(76, 110, 245)` |
| `color` | `color: var(--accent-ink, #ffffff)` | `rgb(255, 255, 255)` |
| `border-*-color` | `border: 1px solid color-mix(in srgb, var(--accent, #4c6ef5) 78%, white 22%)` | `color(srgb 0.452471 0.556471 0.969412)` |

The `color-mix` arithmetic checks out against the observed value: `#4c6ef5` is srgb `(0.2980, 0.4314, 0.9608)`, and `channel × 0.78 + 0.22` gives `(0.4524, 0.5562, 0.9694)`.

Two unlayered rules also declare these properties with `!important` — `#add_exercise_btn.btn` (`components.css:242`, `(1,1,0)`, seafoam `#98DFD6`) and `.btn.btn-calm-primary` (`components.css:3154`, `(0,2,0)`) — and `.is-success` at `(0,1,0)` loses to both of those on specificity as well. Neither is the winner: both are unlayered `!important`, so both are outranked by the layered block. The seafoam colour at `components.css:242` does not render on this button. That is the documented behaviour of `@layer`, not an anomaly.

---

## 3. Product observation — surfaced, not fixed

The intended "success" styling of the add-exercise button was **a green fill, green border and white text plus a green pulse ring**. Only the pulse ring has ever rendered; the three colour declarations have been inert since they were written.

Deleting them changes nothing a user sees. But if the green flash is *wanted*, this packet does not deliver it — that is a deliberate product change needing its own owner decision, and it is out of scope for a pure-deletion packet. **Recorded here so the intent is not lost with the code.**

---

## 4. What was measured and retained

Per-declaration ownership was resolved over Chrome's own `CSS.getMatchedStylesForNode` data across **11 routes × 2 themes**, under both `prefers-reduced-motion` states and under each JS-applied state.

| Family | States probed | Verdict |
|---|---|---|
| `@media (prefers-reduced-motion: reduce)` `*` block | `reduce` | **Retained.** Winner on **17,194** element-matches (animation longhands) and **16,651** (transition longhands). The single highest-impact rule in the file. |
| `body > .container-fluid.mt-4` (`page-enter`) | `no-preference`, `reduce` | **Retained.** Wins on all 22 contexts under `no-preference`; loses to the reduced-motion block under `reduce` — which is the intended behaviour, not deadness (M11). |
| `.skeleton`, `[data-theme="dark"] .skeleton`, `@keyframes skeleton-shimmer` | JS-inserted skeleton (M10) | **Retained.** All 55 observed declarations win somewhere under that state. |
| `@keyframes success-pulse` | success (M10) | **Retained** — it is the half of `.is-success` that renders. |
| `.is-success` `animation` | success (M10) | **Retained** — proven winner. |

**M11 discharged.** The `@media` block was never judged from a default-preference capture: it was captured under its own condition, where it wins, and the `page-enter` rule was captured under both conditions to confirm the suppression is real rather than assumed.

### Retained, and *why* it is not redundant

`[data-theme="dark"] .skeleton` re-declares `background-size: 200% 100%`, which also appears on `.skeleton`. It is **not** a duplicate: the dark rule re-declares the `background` *shorthand*, which resets `background-size` to `auto`, so the repeat is load-bearing. Deleting it would have been a visible regression in dark mode.

---

## 5. Gates

| Gate | Result |
|---|---|
| Full `pytest tests/` | *(see §8)* |
| `tests/test_css_wp4_4_motion_contracts.py` (new, 5 tests) | *(see §8)* |
| `tests/test_css_cascade_contracts.py`, `tests/test_visual_selector_contracts.py` | run, never edited (N6) |
| `tests/test_css_wp4_4_a_baseline_contracts.py` | run and corrected to pin the baseline to its own source commit (see §8) |
| Windows `visual.spec.ts` — full **66**-test matrix | *(see §8)* |
| `accessibility.spec.ts`, `ui-hardening.spec.ts`, `fatigue.spec.ts`, `fatigue-stage4-smokes.spec.ts`, `summary-pages.spec.ts`, `smoke-navigation.spec.ts`, `dark-mode.spec.ts` | *(see §8)* |
| Harness pre/post capture, all 22 contexts | *(see §8)* |
| Seven-surface Stylelint delta | *(see §8)* |
| Linux deep gate | **not run** — N8 requires it at h, i, j, k only |
| Snapshot updates | **none** — `git diff` shows zero `e2e/__screenshots__/` paths |

**`visual.spec.ts` is a backstop only, not the primary proof (F1).** `prepareForScreenshot()` (`e2e/visual-helpers.ts:45,47`) sets `animation-duration: 0s !important` and `transition-duration: 0s !important` globally before every capture. It therefore suppresses animation and transition **timing**, and `visual.spec.ts` **cannot by itself falsify a timing-only `motion.css` regression**.

That is the whole of the claim. `motion.css` also carries non-timing paint and geometry — the `.skeleton` gradient, `background-size`, `border-radius`, and two `!important` colour declarations — so deleting the entire file would **not** be expected to leave the matrix byte-identical, and this document does not assert that it would. For Packet c specifically, the visual matrix is a backstop; the deletion's safety is established by the cascade argument and computed-style differential in §2, the per-packet contract tests, and the pre/post ownership capture in §8.

---

## 6. Method-rule compliance

| Rule | How it was satisfied |
|---|---|
| **M1** | Ownership resolution **and** rest-state differential **and** same-CSS control, all three. |
| **M3** | Captures element-scoped and clipped below the fixed navbar. |
| **M5** | Positive control passes on the element under test (`animation-*` moved). |
| **M6** | Sentinel-took-effect asserted per record by the harness. |
| **M6a** | Transitions suppressed before applying, reading and removing the class. Necessary here — the button carries a transition. |
| **M8** | Only proven non-winners deleted. |
| **M10** | `.is-success` and `.skeleton` judged **under their JS-applied states**, never at rest. |
| **M11** | The `@media` block captured under its own condition. |
| **N2** | `motion.css` is entirely unlayered; contract asserts it stays that way. |

---

## 7. Findings handed on

1. **Observation, not a defect: the seafoam `#add_exercise_btn` paint at `components.css:242` never renders.** It is unlayered `!important` at `(1,1,0)`; the layered `!important` block at `components.css:3540-3548` outranks it under the `@layer` importance inversion (§2). **Packet h is not being asked to investigate this as an unresolved issue** — the mechanism is known, documented at G10/A6, and frozen by N2. It is noted only because `components.css:242` is a candidate that h will encounter, and h's own classification must model layers before judging it either way.
2. **`base.css` also defines `.skeleton`** (`base.css:93`) with `background`, `background-size` and `animation: skeleton-loading`. `motion.css` loads after `base.css` at equal specificity, so **every one of those declarations is overridden**, and `@keyframes skeleton-loading` has no live consumer. This is a **packet b** candidate — not touched here, because `base.css` is b's exclusive path.
3. **The exploratory ownership prober does not model cascade-layer `!important` inversion.** That is the precise limitation, and the only one this packet observed: it ranks candidate winners by specificity and source order within the unlayered tier, so when the true winner is a layered `!important` rule it names an unlayered runner-up instead. Its non-winner identification was correct and was independently confirmed here; its **winner attribution** is unsound wherever `@layer` is in play — `components.css:3539`, `navbar.css:6`, `pages-workout-plan.css:468`/`:718`, `pages-welcome.css:6`. This is **not** a claim that its winner attribution is unreliable in general. It is preserved as the generated artifact `artifacts/wp4_4/ownership_probe.mjs`, not committed into the packet-a-owned `scripts/css_audit/` directory. Treat its output as **nomination-only**, exactly as the plan treats packet `g`: every nomination must be confirmed by a direct computed-style differential before deletion, and any packet touching a layered surface must resolve the winner with layer awareness.
4. **Documentation drift in the Gate-1 planning artifact.** `docs/css_phase4_wp4_4/PLANNING.md:1133`, `:1416` and `:1517` still name the baseline contract by its former name, `test_wp4_4_baseline_is_pinned_and_matches_disk`. The test was renamed to `test_wp4_4_baseline_is_pinned_and_matches_its_source_commit` by this packet (§8). **`PLANNING.md` is deliberately not edited** — it is the approved Gate-1 artifact and no implementation packet may amend it. The drift is recorded here so the reference is traceable; `scripts/css_audit/emit_baseline.py` and `docs/CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md` were updated, since those describe the test's behaviour rather than record an approved decision.

---

## 8. Results

### Primary computed-style proof

On the real `#add_exercise_btn` in both themes, with transitions suppressed per
M6a:

- adding `.is-success` left `background-color`, `color`, and all four
  `border-*-color` longhands byte-identical;
- `animation-name` changed `none` → `success-pulse`;
- `animation-duration` changed `0s` → `1s`.

The live animation is the same-element positive control. The three deleted paint
declarations are therefore proven non-winners, not declarations missed by the
probe.

### Harness pre/post differential

The committed Packet-a harness ran before and after the deletion over **11
routes × 2 themes = 22 contexts**, under both reduced-motion preferences. Both
phases passed their self-checks.

| Comparison | Result |
|---|---:|
| motion-record differences (`reduce` + `no-preference`) | **0** |
| element screenshot differences | **0 / 22** |
| attributable paint-record differences | **0** |
| raw paint-record differences | 2 |

The two raw paint differences are sub-pixel `box-shadow` blur-radius movement on
Welcome's infinitely animated `.hero-center-icon`, one per theme. That exact DOM
path is one of the eight uncertifiable elements in
`CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json`; neither difference is attributable
to this packet.

### Automated gates

| Gate | Result |
|---|---|
| Full `pytest tests/ -q` | **1,874 passed, 1 skipped** in 302.83s |
| Packet/shared CSS contracts | **48 passed** |
| New Packet-c contract red path | **failed as intended** against the genuine pre-deletion rule; the failure named `background-color`; passed after restoration |
| Corrected Packet-a baseline-pin red path | **failed as intended** after corrupting recorded `motion.css` lines 71 → 72; **9 passed** after restoration |
| Chromium functional/accessibility set | **104 passed**: `ui-hardening`, `accessibility`, `smoke-navigation`, `fatigue`, `fatigue-stage4-smokes`, `summary-pages`, and the extra `dark-mode` mechanics check |
| Windows `visual.spec.ts` | **65 passed, 1 inherited known red** (`workout-plan desktop dark`) |
| Snapshot/visual-helper writes | **none** |
| Linux deep gate | **not run**, per N8 |

The visual run used `PW_VISUAL_SEED=1` and reproduced only the WP4.0 animated
Workout Plan red. Its current diff is 875 pixels, localized to the navbar GIF
and two exercise video controls. Because that count differs from the historical
1,039/1,046 observations, the failing case was repeated three times and then
run once with the original `motion.css` and once with the packet change. Every
run produced 875 pixels, and the original/changed diff PNGs are byte-identical:

`sha256 0B7C76DD8D98B20195F073E03EBA13202C0EE62E941EF5A593D9131D5E1DC4E2`

This is direct pre/post isolation of the inherited red, not acceptance based on
its filename alone. An initial local invocation omitted `PW_VISUAL_SEED=1` and
therefore exercised the intentionally empty functional DB; it was invalidated
and rerun correctly. It changed no snapshot or protected path.

### Stylelint delta

The seven-surface filtered measurement moved **2,883 → 2,877 warnings (−6)**.
`motion.css` moved **16 → 10**. The only category changes were:

- `declaration-no-important`: **1,263 → 1,260 (−3)**;
- `declaration-property-value-disallowed-list`: **1,127 → 1,124 (−3)**.

Every other category and all other six shared surfaces are unchanged. Maximum
specificity, ID count, duplicate selectors, and duplicate declarations did not
increase.

### Baseline-contract infrastructure correction

The first legitimate deletion exposed a defect in Packet a's baseline pin:
`test_wp4_4_baseline_is_pinned_and_matches_disk` compared the immutable
Packet-a measurement to the current working tree, so every later authorized
deletion necessarily failed it. The correction checks each surface through
`git show <sourceCommit>:static/css/<surface>` instead. This is both the intended
semantics and a stronger pin: editing current CSS and the baseline JSON together
cannot satisfy it.

The correction is isolated to `scripts/css_audit/measure.py` and
`tests/test_css_wp4_4_a_baseline_contracts.py`; it does not change a measured
value or production behavior.

The first PR run exposed a CI-only prerequisite: Actions' default shallow
checkout did not contain Packet a's historical source commit, so `git show`
failed before it could measure the CSS. The baseline is now pinned to Packet
a's merged squash commit (`46e340e`), whose seven shared CSS surfaces are
byte-identical to the original measurement commit, and only the pytest job uses
`fetch-depth: 0`. This preserves the strong source-commit check without a
network operation inside pytest or a dependency on Packet a's temporary branch.

---

## 9. Must-retain handoff to Packet h

**Packet h owns `components.css`. This is a must-retain, in the same class as
the `.value-changed` blocks (PR#3, M10).**

> **`components.css:3540-3548` — the layered `@layer workout` success-state
> paint on `#workout[data-page="workout-plan"] .btn.btn-calm-primary` — must
> remain, as `!important` and inside its layer, for as long as the deleted
> `motion.css` `.is-success` fallback stays absent.** An equivalent owner
> providing the same required paint on that element is an acceptable
> substitute; nothing else is.

**Why this is now load-bearing.** Before WP4.4-c, `.is-success` carried
`background-color`, `border-color` and `color` as unlayered `!important`
declarations. They never rendered — the layered block outranked them at every
moment (§2) — but they were a latent fallback: had the layered block been
removed or de-`!important`ed, they would have become the winners. This packet
deleted them as proven non-winners under M8, which is correct, and which also
means **that fallback no longer exists**.

**Obligation on h.** If h removes `components.css:3540-3548`, drops its
`!important`, moves it across a layer boundary (already forbidden by N2), or
narrows its selector list so `#add_exercise_btn` no longer matches, then h
must:

1. re-prove the `.is-success` success state on the real `#add_exercise_btn`
   under M6a, exactly as §2 and §8 did here;
2. provide a replacement owner for `background-color`, `border-*-color` and
   `color` on that element in **both** themes; and
3. record the result in its own evidence doc.

Without a replacement, the button falls back to `components.css:242`
(seafoam `#98DFD6 !important`) or, failing that, to Bootstrap's `.btn-primary`
— a visible change, and therefore a V1 rollback trigger, on a route the packet
may not have captured.

**A documentation handoff is deliberate here; no cross-packet test was added.**
A contract in `tests/test_css_wp4_4_motion_contracts.py` asserting the presence
of a `components.css` rule would make Packet c's contract file a claim on
Packet h's exclusive production path, which N1 exists to prevent, and would red
h's legitimate work rather than inform it. The obligation belongs in h's own
must-retain register.

---

## 10. Ownership ruling — owner-authorized cross-packet corrections

Three of this PR's seven files lie outside Packet c's declared ownership
(`PLANNING.md:419`): the Packet-a measurement/test/baseline paths
(`scripts/css_audit/measure.py`, `tests/test_css_wp4_4_a_baseline_contracts.py`,
`docs/CSS_PHASE4_WP4_4_A_BASELINE.json`) and `.github/workflows/ci.yml`, a
never-claimed shared path.

**The owner explicitly authorized these corrections, on review, as an exception
scoped to this PR.** Recorded terms:

- The exception covers **only** the Packet-a measurement/test/baseline paths and
  `.github/workflows/ci.yml`.
- The changes were **necessary**, not opportunistic: Packet a's baseline contract
  compared an immutable measurement against the working tree, so the arc's first
  authorized deletion necessarily red it, and the corrected `git show` form could
  not execute under Actions' default shallow checkout.
- **No concurrent writer existed.** Packet a is merged and closed; no other packet
  was open against these paths.
- The authorization **does not broaden Packet c's production ownership**. Packet c
  still owns exactly `static/css/motion.css`,
  `tests/test_css_wp4_4_motion_contracts.py`, and this evidence document.
- The authorization **does not permit unrelated cleanup** in the touched files, and
  none was performed — the diffs are confined to the baseline-semantics fix, the
  `sourceCommit` repin, and the single `fetch-depth: 0` on the pytest job.

The `docs/CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md` and
`scripts/css_audit/emit_baseline.py` edits in the follow-up commit fall under the
same exception: both describe the renamed contract's behaviour and would
otherwise document semantics the code no longer has.
