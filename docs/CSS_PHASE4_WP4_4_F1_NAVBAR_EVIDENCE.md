# WP4.4-f1 — `static/css/navbar.css` pure deletion

*Phase 4 CSS. Plan: [`docs/css_phase4_wp4_4/PLANNING.md`](css_phase4_wp4_4/PLANNING.md)
(Gate 1 approved, rulings N1–N10). Base: `wt/wp4-4-f1-navbar` from `main` @
`c75d155`, worktree seeded `-Seed visual`.*

**One rule deleted. `−6` lines, `0` insertions.** `!important` **93 → 93**,
custom properties **72 → 72**, `@layer` blocks **1 → 1**, layered/unlayered rule
split **103/91 → 103/90**. Zero declaration-owner changes across 64,961 records;
zero motion changes across 306,864.

The packet's yield is deliberately small. The census nominated **39** candidate
rules on its first run and **38 of those were instrumentation artifacts**;
§7 records how each was exposed. `f1` deletes only what survived that, and
scope was not widened to improve the line count (the plan's `−150 to −400`
projection is explicitly not an acceptance criterion).

---

## 1. What was deleted

```css
/* Only apply legacy styles if NOT inside #navbar */          ← navbar.css:901
body:not(:has(#navbar)) .navbar {                             ← :902
  background-color: #212529;
  height: 40px;
}                                                             ← :905
```

Six source lines (901–906, comment + rule + the separating blank).

### Why it is unreachable — by construction, not only by census

| Step | Evidence |
|---|---|
| `navbar.css` is linked from exactly one template | `templates/base.html:22`; no other template references it |
| that template renders `#navbar` unconditionally | `templates/base.html:36`, first element inside `<body>`, no enclosing `{% if %}` |
| every other template extends it | the only two non-extending templates are the partials `_fatigue_badge.html` and `_fatigue_muscle_bar.html`, which are included fragments, not documents, and link no stylesheet |
| `error.html` is not an exception | it extends `base.html:1`, so it too carries `#navbar` |

So **every document that loads this stylesheet contains `#navbar`**, and
`body:not(:has(#navbar))` is unsatisfiable in all of them. Both premises are
contract-pinned (`test_navbar_css_is_linked_only_from_base_html`,
`test_base_html_renders_the_navbar_unconditionally`) precisely because the
deletion is only safe while they hold.

The runtime census agreed independently: **0 matches in 522/522 contexts.**

---

## 2. The generations — established rule by rule, not inherited

`REFACTOR_PLAN.md:1376` says "triage navbar's three live generations".
`PLANNING.md:471` marks that count as an assumption this packet must establish.
Derived from the source (`artifacts/wp4_4/navbar_generations.py`):

| Generation | Rules | Declarations | `!important` | Custom props | Lines |
|---|---:|---:|---:|---:|---|
| **A** layered scoped (`@layer navbar`) | 103 | 433 | 8 | 48 | 10–882 |
| **B** legacy `.navbar` fallback | 2 | 7 | 0 | 0 | 892–905 |
| **C** unlayered override tail | 89 | 255 | 85 | 24 | 913–1541 |
| — `@keyframes` steps (not style rules) | 5 | — | — | — | — |

**The count is confirmed at exactly three**, and the boundaries are the ones N2
freezes: `@layer navbar` spans 6–883 (matching WP4.4-a §3 exactly), and the
`navbar.css:908` comment's "MUST be outside @layer" tail begins at 913.

### Generation B is *not* dead legacy — and that is the packet's main retention finding

The banner at `:885` calls the whole block "Legacy Support … overridden by the
scoped styles above", and `:893` says the `.navbar` rule "only applies outside
#navbar wrapper". **Both comments are wrong**, and a packet that trusted them
would have deleted a live winner:

- `#navbar` carries the Bootstrap class `navbar`, so `.navbar` matches it.
- `.navbar` at `:892` is **unlayered**; `#navbar { position: sticky }` at `:90`
  is **inside `@layer navbar`**. For *normal* declarations the unlayered rule
  wins **regardless of specificity** — an ID selector loses to a class selector
  here.
- Therefore `position: fixed` at `:894` is the value the browser actually
  computes. This is independently corroborated by WP4.4-a §5 defect 5, which
  had to clip captures below a **fixed** top bar.

Deleting `.navbar` would have unpinned the navbar. It is retained whole and
contract-pinned, including its layer membership
(`test_the_retained_legacy_rule_is_unlayered`).

Only the *second* rule of generation B — the one actually gated on the absence
of `#navbar` — is unreachable.

---

## 3. Oracle validity gate — run before anything was believed

`.claude/rules/verification.md` requires a known-live case, a known-dead case,
and a same-CSS control before any result counts.

| Control | Result |
|---|---|
| `#navbar` | census > 0 in **522/522** contexts |
| `.navbar-brand`, `.navbar-toggler`, `.navbar-collapse`, `.navbar-nav` | **522/522** each |
| `.nav-link` (max 17), `.nav-item` (max 19), `.nav-link-with-icon` (max 11) | **522/522** each |
| `.dropdown-toggle`, `.dropdown-menu`, `.dropdown-item`, `.navbar-brand-icon` | **522/522** each |
| known-**dead** `.wp44-f1-known-dead-control` | census > 0 in **0/522** — required |

Twelve known-live controls seen everywhere and a known-dead control seen
nowhere: the census discriminates in both directions.

---

## 4. Runtime census — 522 contexts

`artifacts/wp4_4/navbar_probe.mjs`. Each rule's selector branches are relaxed to
a **superset** base (state pseudo-classes, pseudo-elements and runtime-toggled
classes/attributes removed). Census 0 on the superset proves the real selector
can never match; census > 0 proves nothing and the rule is **retained**.

| Slice | Contexts |
|---|---:|
| 11 rendered routes × 2 themes × 14 widths | 308 |
| collapsed / expanded-by-click / expanded-by-class / dropdown-by-click / dropdown-by-class, × 2 themes × 3 widths | 30 |
| CDP-forced `hover`, `focus`, `focus-visible`, `active`, `hover+focus`, `focus-within` on 5 navbar targets × 2 themes × 3 widths | 178 |
| `prefers-reduced-motion: reduce`, `prefers-contrast: more`, `print`, × 2 themes | 6 |
| **total** | **522** |

The 14 widths cover every breakpoint edge in the file's **11 distinct `@media`
conditions** (576, 768, 991, 991.98, 992, 1359.98, 1360, 1500, 1600) — no media
rule was classified without a capture under its own condition.

**Result: 1 of 100 base selectors never matched anywhere**, and exactly one rule
has all of its branches in that set:

| Line | Selector | Layer | Census |
|---:|---|---|---:|
| 902–905 | `body:not(:has(#navbar)) .navbar` | unlayered | **0 / 522** |

---

## 5. Completeness check from the other side

The relaxation deliberately strips runtime-toggled classes, so a rule gated on a
class that *nothing* ever applies would be retained rather than nominated.
`artifacts/wp4_4/navbar_tokens.py` closes that gap: every non-Bootstrap class,
id and attribute token `navbar.css` selects on was searched across `templates/`,
`static/js/`, `routes/`, `utils/` and `static/css/`.

**28 tokens probed, 0 unreferenced.** Every JS-applied class the census relaxed
away is real:

| Token | Applied at |
|---|---|
| `.nb-compact` | `static/js/modules/navbar-enhancements.js:28` |
| `.is-hover-open` | `static/js/modules/navbar-enhancements.js:249` |
| `.scientific-mode` | `static/js/modules/filter-view-mode.js:594` |
| `.fa-microscope` | `static/js/modules/filter-view-mode.js:597` |

Validity control for this scan: `nb-compact` 5 hits, `is-hover-open` 3,
`scientific-mode` 2, `nb-skip-link` 1, `darkModeToggle` 13 — against
`wp44f1nosuchtoken` 0 and `nb-compactXYZ` 0. It discriminates.

---

## 6. Oracles and controls

### 6a. Rest-state differential — `scripts/css_audit/runtime_probe.mjs`, 22 captures

| Oracle | Records | Differing |
|---|---:|---:|
| declaration owner (CDP `matchedRules`) | 64,961 | **0** |
| motion | 153,432 | **0** |
| motionReduced | 153,432 | **0** |
| paint | 340,960 | **2** |

### 6b. The 2 paint records are noise, proven by a same-CSS control

Both are the animating Welcome glow, one per theme, on
`html/body[1]/main[1]/div[0]/div[0]/section[1]/div[1]/div[0]` — `box-shadow`
blur differing in the 4th decimal (58.55 → 58.88). That element is one of the
**8 uncertifiable Welcome elements** registered by WP4.4-a §6.

A **third probe run on identical post-deletion CSS** (`nav_rt_after` vs
`nav_rt_after2`) reproduces **the same 2 records, on the same path, in the same
property, with the same magnitude** (58.88 → 58.72). The deletion contributes
nothing; the drift is the animation.

### 6c. Built-in self-checks — all three runs

| Check | before | after | after2 (control) |
|---|---|---|---|
| same-CSS control | 0 differing / **17,048** elements, 22 caps | 0 / 17,048 | 0 / 17,048 |
| sentinel took effect (M6a) | **4,270 / 4,270** | 4,270 / 4,270 | 4,270 / 4,270 |
| sentinel reverted (M6a) | **4,270 / 4,270** | 4,270 / 4,270 | 4,270 / 4,270 |
| screenshot control | **22 / 22** | 22 / 22 | 22 / 22 |
| uncertifiable elements | 16 | 16 | 16 |

M6a is honoured throughout: transitions are suppressed **before** the sentinel is
applied, read, and removed, and both effect and reversion are asserted per
record. A dedicated navbar sentinel sweep over `#navbar`, `.navbar-brand`,
`.nav-link`, `.navbar-toggler`, `.dropdown-menu`, `.navbar-collapse` reported
**6/6 took effect and 6/6 reverted in both themes**.

---

## 7. The post-deletion flip, stated by source identity

A zero differential alone is equally consistent with "deleted the right rule"
and "the probe went blind". The four things kept apart, per the `d1` finding:

1. **deleted rule identity** — the source block at its own source range;
2. **surviving selector text** — `.navbar` occurs in several retained rules;
3. **retained source rule** — `.navbar` at `navbar.css:892–899`;
4. **computed declaration owner** — which rule actually supplies the value.

### 7a. A synthetic element that really satisfies the deleted selector

No real page can satisfy `body:not(:has(#navbar))` — that is the whole basis of
the deletion — so the probe **removes `#navbar` from the DOM** and inserts a
`.navbar` element. The **control fails by exactly one compound**: the identical
element in a document where `#navbar` is still present.

| Theme | Case | `body` matches `:not(:has(#navbar))` | `background-color` | `height` |
|---|---|---|---|---|
| light | control (`#navbar` present) | false | `rgba(0,0,0,0)` | `16px` |
| light | **synthetic, BEFORE** | true | **`rgb(33,37,41)`** = `#212529` | **`40px`** |
| light | **synthetic, AFTER** | true | `rgba(0,0,0,0)` | `16px` |
| dark | control (`#navbar` present) | false | `rgba(0,0,0,0)` | `16px` |
| dark | **synthetic, BEFORE** | true | **`rgb(33,37,41)`** | **`40px`** |
| dark | **synthetic, AFTER** | true | `rgba(0,0,0,0)` | `16px` |

The control never takes those values, before or after. The synthetic element
took them before and does not after.

### 7b. Declaration owner by source range (CDP `CSS.getMatchedStylesForNode`)

`navbar.css` author rules owning that synthetic element — universal selectors
excluded, since `*` resets say nothing about whether a deleted block survived:

| | Rules | Owners |
|---|---:|---|
| **BEFORE** | **2** | `.navbar` @ **892–899** → `position: fixed; top: 0; left: 0; right: 0; z-index: 1000;`<br>`body:not(:has(#navbar)) .navbar` @ **902–905** → `background-color: #212529; height: 40px;` |
| **AFTER** | **1** | `.navbar` @ **892–899** → `position: fixed; top: 0; left: 0; right: 0; z-index: 1000;` |

Identical in both themes.

**The oracle demonstrably did not go blind.** After deletion it still resolves
the retained rule, at its **unchanged** source range 892–899, with its unchanged
declarations — and `element.matches('body:not(:has(#navbar)) .navbar')` still
returns **`true`** in the after run, because selector matching is a DOM
operation independent of whether any rule uses that selector. The element still
*satisfies the selector*; no source block *supplies the declarations*. That is
exactly the distinction a substring contract cannot make.

---

## 8. Instrumentation defects found and corrected

The first census run nominated **39 rules**. **38 were artifacts.** Each was
caught by a control, not by inspection of the verdicts.

| # | Defect | Symptom | How it was exposed | Fix |
|---|---|---|---|---|
| 1 | Relaxation inserted `*` around `>` combinators | `#navbar > .container-fluid` became `#navbar *>* .container-fluid`, matching nothing | `.container-fluid` is at `base.html:38` — a "dead" selector for an element plainly in the DOM | split on combinators at paren depth 0; never rewrite them |
| 2 | Substitution ran **inside** `:not(...)` | `:not(.active)` became the invalid `:not()`, which throws, scored as census 0 | `#navbar .nav-link:not()` in the verdict list is not a selector anyone wrote | mask functional-pseudo arguments before substituting; `:not(.active)` is already conservative as written |
| 3 | `@keyframes` steps parsed as style rules | `from`, `to`, `0%`, `55%`, `100%` nominated as dead rules | keyframe stops have no DOM census by definition | exclude any rule under an `@keyframes` at-rule (5 of 199) |
| 4 | Owner probe attached `CSS.styleSheetAdded` **after** `CSS.enable` | **0** navbar declarations matched — every rule would have looked cascade-dead | a file that certainly matches reporting zero matches is impossible | attach the listener before `enable`, which replays existing sheets |

Defects 1–3 all point the same way: **a relaxation that is not provably a
superset silently manufactures deadness.** Defect 4 is the `d1` lesson in a new
place — an oracle reporting a uniform zero must be assumed blind until a
known-live case proves otherwise, which is why every probe here carries one.

---

## 9. Accessibility and keyboard, both themes

| Theme | Result |
|---|---|
| light | **12/12** traversed elements have a computed visible-focus indicator; **12/12** inside `#navbar` |
| dark | **12/12**; **12/12** inside `#navbar` |

Measured as computed evidence (`outline-style` ≠ `none` and `outline-width` > 0,
or a non-`none` `box-shadow`), not as a screenshot.

---

## 10. Gates

| Gate | Result |
|---|---|
| `tests/test_css_wp4_4_navbar_contracts.py` | **16 passed** |
| Red-path proof | **16/16** go red under their own violation; tree restores **sha256-identical**; final run 16 passed |
| Full `pytest tests/` | **2,262 passed, 1 skipped** (396.91s) |
| Shared `test_css_cascade_contracts.py` + `test_visual_selector_contracts.py` + `test_css_wp4_4_a_baseline_contracts.py` | **43 passed**, run and **unedited** (`git diff` vs `origin/main` empty) |
| `nav-dropdown` (**required, blocking**), `accessibility`, `dark-mode`, `smoke-navigation`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening` | **127 passed** (3.5m) |
| `visual.spec.ts`, Chromium, full matrix | **65 passed, 1 failed** — the ledgered red, below |
| Rest-state differential | 0 owner / 0 motion / 0 motionReduced; 2 paint, both ledgered |
| Same-CSS control (M5) | 0 differing / 17,048 elements, on **both** sides |
| Stylelint, seven surfaces | **2,851 → 2,850 (−1)**, no rule increased, **0** parse errors |
| Snapshot / helper integrity | **0** changed paths under `e2e/__screenshots__/`, `e2e/visual-helpers.ts`, `playwright.config.ts`, `scripts/css_audit/` |

Test count reconciles: `main` @ `c75d155` collects **2,247**; this branch
collects **2,263** = 2,247 + the 16 new contracts.

### The visual failure is the ledgered animated-logo red — and it is in band

`visual.spec.ts:40 › visual baseline: workout-plan › workout-plan desktop dark`
— **875 pixels, 882 on retry.**

**This reproduces the two most recent recorded observations exactly**, both
taken before `f1`:

- **WP4.4-c** — "Its current diff is 875 pixels, localized to the navbar GIF",
  repeated three times.
- **WP4.4-b** — "failed at **875 pixels** (retry 882) … This run widens the
  recorded range: 875/882 here against 1,039/1,046 previously", recorded under
  **M7: the band is not an invariant**.

The ledgered band is therefore **875/882 ∪ 1,039/1,046**, and this run sits on
the recent half of it.

**A same-CSS pixel control settles authorship.** With `navbar.css` restored
byte-identical to `main` (`git diff --numstat` = 0), the identical test in the
identical worktree produced **the identical 875 pixels, 882 on retry**. The
count is independent of this packet.

875 still exceeds `maxDiffPixels: 800`, so it presents as a real snapshot
failure, exactly as WP4.4-a §8 says it must. `maxDiffPixels` was **not** touched
and **no snapshot was written**. **No non-ledger visual difference appeared** in
any route, theme or viewport. `f1` does not run the Linux deep gate (N8).

### Stylelint attribution

| Rule | Before | After | Δ |
|---|---:|---:|---:|
| `declaration-property-value-disallowed-list` | 1,100 | 1,099 | **−1** (the `#212529` literal) |
| `declaration-no-important` | 1,263 | 1,263 | **0** |
| `no-descending-specificity` | 244 | 244 | 0 |
| `no-duplicate-selectors` | 25 | 25 | 0 |
| `selector-max-id` / `selector-max-specificity` | 116 / 102 | 116 / 102 | **0 / 0** |
| `navbar.css` alone | 362 | 361 | −1 |

`declaration-no-important` holding at 1,263 — and at **93 within `navbar.css`** —
is independent confirmation that nothing was re-weighted.

---

## 11. Preservation invariants

| Invariant | Verdict |
|---|---|
| **V1** no visual difference | Owner/motion differentials 0; the 2 paint records reproduce on identical CSS; screenshot control 22/22 byte-identical on both sides |
| **V2** no rebaseline | 0 changed paths under `e2e/__screenshots__/`; no `e2e/visual-helpers.ts` or `playwright.config.ts` change |
| **V3** no re-weighting | `!important` **93 → 93**; `selector-max-id` +0; `selector-max-specificity` +0 |
| **V4** no duplication increase | `no-duplicate-selectors` 25 → 25; `declaration-block-no-duplicate-properties` 2 → 2 |
| **V5** contribution | −6 lines, −1 rule, −2 declarations. Scope was **not** widened to approach the `−150 to −400` projection |
| **V6** no conflict | Single writer, single production file |
| **N2** layer membership frozen | `@layer` blocks 1 → 1; layered rules 103 → 103; no rule crossed the boundary |
| **G11** last layer block preserved | `@layer navbar` is single-sourced at `navbar.css:6` and survives, contract-pinned |
| **F6** contract-pinned declarations | `--nav-gap: var(--s-3)`, `--nav-padding-y: var(--s-3)`, `--nav-padding-x: 1rem` all present, each with its own red path |

---

## 12. Surface accounting

| Metric | Before | After | Δ |
|---|---:|---:|---:|
| lines | 1,542 | 1,536 | **−6** |
| style rules | 194 | 193 | **−1** |
| declarations | 695 | 693 | **−2** |
| layered / unlayered rules | 103 / 91 | 103 / 90 | 0 / −1 |
| `!important` | 93 | 93 | **0** |
| custom-property declarations | 72 | 72 | **0** |
| `@layer` blocks | 1 | 1 | **0** |
| `@keyframes` steps | 5 | 5 | **0** |
| Stylelint (`navbar.css`) | 362 | 361 | −1 |

---

## 13. Retained and deferred — binding on `f2`

1. **Generation B's comments are wrong and must not be trusted.** `:885` and
   `:893` describe the `.navbar` rule as an overridden legacy fallback that
   "only applies outside #navbar". It is the live winner for `position`.
   Correcting the comments is an edit `f1` may not make (pure deletion), so the
   defect is recorded rather than fixed.

2. **A cascade-dead declaration nomination exists and is NOT certified.** A
   declaration-owner sweep over 150 document states reported 570 `navbar.css`
   declarations matched, 415 winning somewhere, and **155 matched-but-never-
   winning**. That set is **not** acted on here: the sweep's winner resolution
   is hand-rolled and its `!important`/layer arbitration was not independently
   validated against a known-live *overridden* control. Per the standing rule
   that an uncertified interaction-state result must remain, all 155 are
   retained. Certifying them belongs to a packet that can pay for the control.

3. **The 11 distinct `@media` conditions include near-duplicates**
   (`max-width: 991px` and `max-width: 991.98px`; `min-width: 992px` appears
   with three different upper bounds). Consolidating them is generation
   consolidation — **`f2`'s, not `f1`'s**.

4. **Six rules share the selector `#navbar > .container-fluid`** across both
   layers (`:155`, `:807`, `:964`, `:1050`, `:1131`, `:1249`). This is the
   clearest consolidation target in the file and is left entirely to `f2`.

---

## 14. Reproducing this

```bash
python artifacts/wp4_4/navbar_static.py        # parse: 199 rules, 11 media conditions
python artifacts/wp4_4/navbar_generations.py   # the three generations, rule by rule
python artifacts/wp4_4/make_navbar_specs.py    # superset relaxation + admissible widths
python artifacts/wp4_4/navbar_tokens.py        # token reachability, both directions

node artifacts/wp4_4/navbar_probe.mjs  --out artifacts/wp4_4/navbar_census
node scripts/css_audit/runtime_probe.mjs --out artifacts/wp4_4/nav_rt_before
node artifacts/wp4_4/navbar_flip.mjs --label BEFORE-deletion --out artifacts/wp4_4/flip_before
#   … apply the deletion …
node scripts/css_audit/runtime_probe.mjs --out artifacts/wp4_4/nav_rt_after
node scripts/css_audit/runtime_probe.mjs --out artifacts/wp4_4/nav_rt_after2   # same-CSS control
node artifacts/wp4_4/navbar_flip.mjs --label AFTER-deletion --out artifacts/wp4_4/flip_after
python artifacts/wp4_4/diff_runs.py artifacts/wp4_4/nav_rt_before artifacts/wp4_4/nav_rt_after
python artifacts/wp4_4/diff_runs.py artifacts/wp4_4/nav_rt_after  artifacts/wp4_4/nav_rt_after2

python artifacts/wp4_4/redpath_f1.py
node scripts/css_audit/stylelint_surfaces.mjs artifacts/wp4_4/stylelint_after.json
```

Analysis scripts live under the gitignored `artifacts/` tree.
`scripts/css_audit/` stays packet-`a`-owned and was not modified (A11).

---

## 15. Out of scope

- **All re-weighting** — `!important` reduction, specificity changes, selector
  rewrites, trimming live selector lists, `@media` consolidation, and merging the
  six `#navbar > .container-fluid` rules. That is **`f2`**.
- **Moving anything across the `@layer navbar` boundary** — frozen arc-wide by
  N2, and the boundary is load-bearing for generation B.
- **The 155 uncertified cascade-dead declarations** of §13.2.
- **Correcting the misleading `:885` / `:893` comments** — an insertion, which a
  pure-deletion packet may not make.
