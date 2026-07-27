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

### What beats them

Both `#add_exercise_btn.btn` (`components.css:242`, `(1,1,0)`) and `.btn.btn-calm-primary` (`components.css:3154`, `(0,2,0)`) declare the same properties with `!important`. `.is-success` is `(0,1,0)` with `!important` and loses to both on specificity.

⚠️ **The rendered value is neither of the two rules' colours** — the button computes to `rgb(76, 110, 245)` (the calm-primary accent), not the seafoam `#98DFD6` that `components.css:242` declares at higher specificity. That inversion is **unexplained and out of scope for this packet**; it is recorded in §7 as a finding, not acted on. It does not affect this deletion: `.is-success` loses to *both* candidates, so which of them ultimately wins cannot make a deleted non-winner live.

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

**`visual.spec.ts` is a backstop only, not the primary proof (F1).** `prepareForScreenshot()` sets `animation-duration: 0s !important` and `transition-duration: 0s !important` globally before every capture, so it cannot falsify a change to `motion.css` — deleting the entire file would leave the matrix byte-identical. The primary proof is the ownership differential in §2 and the pre/post harness capture in §8.

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

1. **Unexplained cascade inversion on `#add_exercise_btn`** (§2). `components.css:242` declares `background-color: #98DFD6 !important` at `(1,1,0)`; `components.css:3154` declares `background: var(--accent, #4c6ef5) !important` at `(0,2,0)`. The lower-specificity rule is what renders. Both are `components.css`, so this belongs to **packet h**, which owns that surface. Worth resolving before h deletes anything in that neighbourhood.
2. **`base.css` also defines `.skeleton`** (`base.css:93`) with `background`, `background-size` and `animation: skeleton-loading`. `motion.css` loads after `base.css` at equal specificity, so **every one of those declarations is overridden**, and `@keyframes skeleton-loading` has no live consumer. This is a **packet b** candidate — not touched here, because `base.css` is b's exclusive path.
3. **The exploratory ownership prober's winner attribution is not authoritative.** It correctly identified the non-winners, but named a beater whose colour is not what renders (§2). It is preserved as the generated artifact `artifacts/wp4_4/ownership_probe.mjs`, not committed into the packet-a-owned `scripts/css_audit/` directory. Treat its output as **nomination-only**, exactly as the plan treats packet `g` — every nomination must be confirmed by a direct computed-style differential before deletion. Its "never wins anywhere" output was independently confirmed here; its "beaten by" output was not.

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
