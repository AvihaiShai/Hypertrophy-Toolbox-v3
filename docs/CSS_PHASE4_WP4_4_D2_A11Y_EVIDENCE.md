# WP4.4-d2 — `static/css/a11y.css` `!important` re-weighting

Packet `d2` of the WP4.4 shared-bundle arc — the re-weighting half of the split
`d` packet. `d1` was pure deletion and removed no `!important`; every one of the
51 annotations it left behind is this packet's subject.

**Re-weighting is not deletion.** Removing `!important` from a declaration does
not remove the declaration; it lowers its cascade weight and asks whether the
same declaration still wins. A candidate ships only if it remains the
**effective owner wherever it is intended to own the property**, with zero
computed-value differences and zero declaration-owner differences.

Base commit: `3a23333`. Production ownership: `static/css/a11y.css` only.

**Result: 1 annotation de-weighted, 50 retained.** `!important` **51 → 50**.
Declarations **240 → 240**, style rules **94 → 94**, custom properties
**17 → 17**, `@layer` **0 → 0**. Lines 714 → 728, entirely from two explanatory
comments — no selector, value, declaration, rule order or media placement
changed anywhere in the file.

| | |
|---|---|
| **Certified and shipped** | `.is-invalid { box-shadow }` — 1 |
| **Certification attempted and failed → retained** | `.selection-field.has-validation-error label { color }` — 1 |
| **Retained without an attempt** (live, uncertified, protected, or engine-invisible) | 49 |

The yield is deliberately small and the packet does not chase the count: a
zero-removal result was an acceptable outcome, and safety outranks the
`!important` total. The substantive output is the adjudication of all 51
annotations, the seven instrumentation defects in §2, and **the discovery that
M6a's transition suppressor has never actually been enforced arc-wide** (§2, D7)
— a correction that reaches beyond this packet.

---

## 0. How to read this document

Section 1 is the candidate inventory and its identity anchoring. Section 2 is
the instrumentation-defect record — **the largest part of this packet's work**,
and load-bearing, because every verdict below is only as good as the harness
that produced it. Section 3 adjudicates the two candidates that survived to
certification. Section 4 is the retention ledger, split into the five classes
the assignment requires. Section 5 is the gate record.

---

## 1. Candidate inventory and identity

`a11y.css` at `3a23333`: 714 lines, 80 style rules, 7 keyframe-step rules,
**51 `!important` annotations**, 0 inside `@keyframes`, 0 `@layer` tokens.

Candidates are `C01`–`C51`, emitted by `artifacts/wp4_4/d2_static.py` in source
order. **C-numbers are labels, not identity.** Every candidate is anchored by
the tuple *(at-rule chain, selector, property, value, source line, exact
character offset of the `!important` token)*, and rule identity is never taken
from nth-child position or re-serialized text — the hazard
`.claude/rules/verification.md` calls out.

The inventory was regenerated against the final source at the end of the packet
and compared field-by-field with the inventory the sweep consumed:
**51/51 candidates, 0 field differences.** The two candidates carried to
certification are therefore cited by source identity, not by label:

| Label | Source identity |
|---|---|
| **C34** | `static/css/a11y.css:502` — chain *(none)* — selector `.is-invalid` — `box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25) !important` — token offset 13821–13831 |
| **C50** | `static/css/a11y.css:693` — chain *(none)* — selector `.selection-field.has-validation-error label` — `color: #dc3545 !important` — token offset 18619–18629 |

### 1.1 What the engine can and cannot see

Of the 51 annotations, **12 never reach Chromium at all** and are excluded from
the probed population (`liveIds` = 39). They are not "dead"; they are invisible
to *this* engine, which is a different claim and a weaker one:

| Count | Cause | Candidates |
|---|---|---|
| 8 | inside `@-moz-document url-prefix()`, an at-rule Chromium never parses, so the rule object does not exist | C01–C08 |
| 4 | `-moz-box-shadow`, dropped by Chromium's declaration parser (`declaration-absent`, live priority `""`) | C19, C23, C27, C32 |

39 located + 12 dropped = 51, with `unCanonicalizable: []` and `ambiguous: []`.

**None of the 12 is a removal candidate.** Chromium's inability to parse a
declaration is evidence about Chromium, not about whether the annotation does
work in Firefox, and this packet has no Firefox oracle.

---

## 2. Instrumentation defect record

An `!important` sweep is an unusually easy thing to get confidently wrong: the
failure mode is a harness that cannot see the cascade answer, reports the
absence of a signal, and has that read as "safe to remove". Every defect below
was found by a **control**, not by inspection, and each is recorded with the
verdict it *would have produced* had it survived.

The prior session recorded **six** defects. This session found **one more**
(defect 7) while re-verifying the sweep, so the record below has **seven**
entries. The seventh is reported as a new finding, not folded silently into the
accepted six.

### D1 — the engine elides the universal selector, so selector matching by source text fails

| | |
|---|---|
| **Incorrect verdict** | The entire focus system — C11–C18, C20–C22, C28–C31 — fails to bind to a live rule and drops out of the report. An annotation that produces no row reads as "no live rule", i.e. dead. This is the single most dangerous possible error in this file: `a11y.css:396-497` is the app-wide focus-visibility guarantee. |
| **Control that exposed it** | The static-vs-live reconciliation: `located + dropped` must equal the static count of 51, and `unCanonicalizable` must be empty. It was not. `artifacts/wp4_4/d2_recon.json` is the pre-fix reconnaissance pass and still shows the magnitude — its naive text matcher reconciles only 2 of 51. |
| **Root cause** | Chromium serializes `*:focus` as `:focus` and `*.active:focus` as `.active:focus`. The source says `*:focus, *:active:focus, *.active:focus, button:focus, …`; the live `selectorText` says `:focus, :active:focus, .active:focus, button:focus, …`. A hand-written normalizer cannot be trusted to predict this. |
| **Correction** | `D2.canonical()` round-trips the source selector through a scratch stylesheet and takes the engine's own `selectorText` back. Both sides are then named by the engine, and the harness never guesses. |
| **Post-correction control** | `located: 39`, `dropped: 12`, `unCanonicalizable: []`, `ambiguous: []`; 39 + 12 = 51 exactly. |

### D2 — duplicate `(chain, selector)` pairs all bound to the first live rule

| | |
|---|---|
| **Incorrect verdict** | Where two source rules share a canonical chain+selector, both candidates bound to the *first* live rule. The sentinel then mutates a declaration the candidate does not correspond to, and the verdict is attributed to the wrong source line — in either direction, including certifying a live declaration as removable. |
| **Control that exposed it** | `report.ambiguous`, which records every canonical key matching more than one live rule together with which occurrence was consumed. |
| **Root cause** | Binding was `rules.find(...)` — first match wins — with no notion of which *occurrence* a candidate belonged to. |
| **Correction** | Candidates are grouped by source rule (they are emitted adjacent by `d2_static.py`), and each group consumes the *n*-th live hit for its key via a `used` counter, so duplicates resolve positionally in source order. |
| **Post-correction control** | `ambiguous: []` in every run; the 2 duplicate groups (`consumedInOrder: 2`) resolve in source order. |

### D3 — Chromium re-serializes unchanged colours into OKLab, so string comparison reported differences that do not exist

| | |
|---|---|
| **Incorrect verdict** | False `value-changes` and false `reversion-failed` on every colour-valued candidate — which is the conservative direction for removal, but a failing M6a reversion control invalidates the whole sweep under M5, so it does not merely cost opportunities. |
| **Control that exposed it** | The M6a reversion check: `restored` must equal `baseline` byte-for-byte on an untouched element. It failed on colours that had not changed. |
| **Root cause** | `getComputedStyle` returns a **spelling**, not a value. Once the cascade is recomputed, `rgba(255,255,255,0.9)` comes back as `oklab(0.999994 0.0000455678 0.0000200868 / 0.901961)`. |
| **Correction** | Every colour token is pushed through the engine with `color-mix(in srgb, X 100%, transparent 0%)`, which maps both spellings onto one `color(srgb …)` form, then quantized to 5 decimals. No hand-rolled OKLab arithmetic. |
| **Post-correction control** | `normaliserSelfCheck`: `knownEqualCollapses: true` while `knownDifferentAlphaKept`, `knownDifferentChannelKept`, `knownDifferentGeometryKept` all stay `true`. |

### D4 — the colour normaliser's own self-check used a control pair finer than the engine's resolution

| | |
|---|---|
| **Incorrect verdict** | None directly — the bogus control *failed*, correctly. The danger was the obvious "fix": loosening quantization until it passed would have collapsed genuine 1/255 colour differences and produced **false REMOVABLE** verdicts on colour candidates. |
| **Control that exposed it** | The self-check failing on a pair that ought to have been distinguishable. |
| **Root cause** | The pair was `rgba(…, 0.5)` vs `rgba(…, 0.503)`. CSS alpha is stored 8-bit, so **the engine** collapses both to 128/255 = 0.501961 before the normaliser is ever reached. The control was asserting a difference below the engine's own resolution. |
| **Correction** | Control pairs are now the smallest difference 8-bit colour can actually express: `rgb(1,2,3)` vs `rgb(2,2,3)`, and alpha `0.5` vs `0.51`. |
| **Post-correction control** | `oneChannelStepKept: true` and `oneAlphaStepKept: true` added to the self-check, which grew from 4 assertions to 6 and passes on all of them. |

### D5 — transition suppression was cycled per candidate, so one candidate's mutation was read mid-flight by the next

| | |
|---|---|
| **Incorrect verdict** | **141 false reversion misses on C21**, i.e. `reversion-failed`, which invalidates the sweep under M5 rather than costing one candidate. |
| **Control that exposed it** | The M6a reversion check again; the tell was a computed colour numerically identical to the baseline but serialized as `oklab(...)` — the signature of an interpolated value. |
| **Root cause** | `suppress()`/`release()` were called inside `probe()`, so suppression dropped between candidates and reopened a window in which a transition could start. |
| **Correction** | `hold()`/`unhold()` keep suppression up across the **whole** candidate loop for a context; `release()` is a no-op while held. |
| **Post-correction control** | C21 moves from `reversion-failed` to `owner-changes`; it is retained either way, but the sweep is no longer invalid. |

### D6 — synthetic states focused "the first focusable element" instead of an element carrying the injected class

| | |
|---|---|
| **Incorrect verdict** | `.is-invalid:focus` (C35, C36), `.is-invalid-required:focus` (C44, C45) and their dark twins (C48, C49) reported **`never-matched`** — the class+focus combination was never reached. Worse than the six wrong rows: **C34's rest-state verdict was being taken without its own `:focus` competitor ever in play**, which is precisely the state where Bootstrap's validation rules compete. |
| **Control that exposed it** | `never-matched` on rules that provably exist in the live sheet and whose class the same pass had just injected — an impossible combination. |
| **Root cause** | Two compounding errors: focusing "the first focusable element" rather than one carrying the class, and `querySelector` returning the first DOM match, which for `.is-invalid-required` is the non-focusable `.wpdd` wrapper. |
| **Correction** | Each synthetic state declares a **priority list** of focus selectors; each is tried in turn and only accepted once `document.activeElement === el` confirms focus actually landed. The focused element is then also driven through `hover`/`focus`/`focus-visible`/`active`/`focus-within` via CDP. |
| **Post-correction control** | C44/C45/C48/C49 move from `never-matched` to `never-owner` with real context counts; C33/C34 measured element counts roughly double. |

### D7 — *(new this session)* the M6a transition suppressor is itself beatable by the cascade

| | |
|---|---|
| **Incorrect verdict** | Mid-transition reads on any element whose transition the suppressor failed to stop. Observed directly: C45's baseline read `0 0 0 1.7978px rgba(220,53,69,0.141)` — a value strictly between C43's `3.2px/0.251` and C45's `4px/0.349`, i.e. an interpolation, not either rule's value. Downstream this produced `reversion-failed` on C21/C28/C45 and **13 same-CSS control drift records**, all on C21. Under M5 that invalidates the sweep. For the CTLF control the wrong answer is `owned=0` — an annotation that *is* the effective owner classified as `never-owner`. |
| **Control that exposed it** | The same-CSS control (M5): run the identical candidate loop twice on identical CSS. 13 of 18,174 paired records differed, always in the same direction — first pass mid-flight, second pass settled. |
| **Root cause** | The suppressor is `*, *::before, *::after { transition: none !important }` — **unlayered, specificity (0,0,0)**. Two independent classes of rule beat it, and both exist in this codebase: (1) **layered `!important`** — `pages-workout-plan.css:959` declares `transition: all 200ms … !important` inside `@layer workout`, and `tokens.css:2` orders `workout` first, so for `!important` the layer order inverts and layered beats unlayered outright; (2) **unlayered `!important` with any specificity at all** — e.g. `components.css:25`. M6a was therefore never actually enforced app-wide, only believed to be. |
| **Why it survived to the full matrix** | The six-control population contained **no transitioned element**. A control suite that cannot fail a defect cannot catch it. |
| **Correction** | The repair does not go through the cascade at all: `settle()` finishes in-flight `CSSTransition` objects via the Web Animations API, which no stylesheet can outrank. Infinite CSS animations (the 8 uncertifiable Welcome elements, plan C7) are `CSSAnimation`, are excluded by construction, and are left running. To keep the full matrix affordable the settle set is narrowed to the elements that *defeat* the suppressor — those whose computed `transition-duration` is still non-zero after suppression — which is exactly the population the defect is about. That gating was verified to change **0 verdict fields across 506 contexts**. |
| **Post-correction control** | New control **CTLF**: a candidate whose element carries a **layered `!important`** transition, mirroring `pages-workout-plan.css:959`. Green: `owned=1/1 kept=1/1 same=1/1`. The `suppressorSelfCheck` reports `cssSuppressorBeaten: true` (the defect is real and still real) and `settleReachesEndValue: true` (the repair works anyway). Same-CSS control drift falls to **0**. |
| **Red path** | `--no-settle` disables the repair. CTLF then reports `owned=0/1 kept=0/1`, the driver fails the controls, and the run aborts with *"oracle validity controls failed — no candidate result from this run counts (M5)"*. The control provably catches the defect it was written for. |

### 2.1 Harness scope

All instrumentation lives under the gitignored `artifacts/wp4_4/` inside the
packet worktree. **No harness file and no `scripts/css_audit/**` file is
committed by this packet**, and the implementation PR carries the authorized
three-file scope only.

---

## 3. Certification of the surviving candidates

Two of the 51 annotations reached `REMOVABLE` in the full matrix. Both were
then re-examined **individually, at declaration granularity**, because each is
asymmetric with a sibling that must be retained — C34 with C33 in the same rule,
C50 with its dark twin C51. Asymmetry is not disqualifying, but it raises the
proof burden, so the census verdict was not accepted on its own for either.

The census oracle answers *"is this declaration the effective owner?"*. That is
not sufficient here. The targeted pass in `artifacts/wp4_4/d2_c34c50.mjs`
answers the stronger question — **which declaration owns the property**,
identified by sheet and selector — by sentinelling each competing declaration
in turn and seeing which one moves the computed value. The engine still
performs the cascade; nothing models specificity or layers.

**Result: C34 ships. C50 fails and is retained.**

### 3.1 C34 — `.is-invalid { box-shadow }` — CERTIFIED

`static/css/a11y.css:502`, chain *(none)*, `box-shadow: 0 0 0 0.2rem rgba(220,
53, 69, 0.25) !important`, token offset 13821–13831.

**Why the asymmetry with C33 is structural, not a fluke.** Bootstrap declares
`border-color` on `.is-invalid` **at rest** (`.was-validated .form-control:invalid,
.form-control.is-invalid`), but declares `box-shadow` **only in its `:focus`
variants** (`.form-control.is-invalid:focus`, `.form-select.is-invalid:focus`,
`.form-check-input.is-invalid:focus`). Specificity, from
`scripts/css_audit/specificity.py`: `.is-invalid` is (0,1,0),
`.form-control.is-invalid` is (0,2,0). So de-weighting `border-color` hands it
to Bootstrap and changes the computed value — which is exactly what the census
measured for C33 (`value-changes`, owner 2,634 / kept 1,232) — while at rest
**nothing at all competes for `box-shadow`**. One rule, two annotations, two
different answers, for a reason that can be pointed at in the source.

**Targeted result: 176 measurements, 176 reached, 0 failures.**

| Dimension | Coverage |
|---|---|
| Instances | **real** rendered instance on `/workout_log` (48) + exact synthetic `.form-control.is-invalid` on two routes (128) |
| States | `rest` 48, `focused` 48, `blurred-after-focus` 48, `disabled` 32 |
| Themes | light 88, dark 88 |
| Scales | all 8 `data-scale` levels |
| Exact-element check | `matchesExact` true in 176/176 — the `.is-invalid` element itself, never a nearby focusable |
| Mutation integrity | `flipOk` and `backOk` true in 176/176 |
| Verdict | computed value identical 176/176; declaration owner identical 176/176; reversion clean 176/176 |

The **real** instance is produced by the shipping code path, not injected:
`ui-handlers.js:225` toggles `.is-invalid` on `.editable-input:not(.date-input)`
when `validateScoredValue()` (`workout-log.js:539`) rejects the typed value.
*(The first attempt fed a non-numeric string to a `type=number` input, which the
browser coerces to `''`, and `''` is explicitly valid — the element came back
`.is-valid`. The setup was wrong, not the candidate; each field now gets a value
genuinely out of its range.)*

**Ownership transfer behaves exactly as intended**, before and after the
re-weighting alike:

| State | Effective owner | Scales |
|---|---|---|
| rest | `a11y.css .is-invalid` | 1–8 |
| focused | `a11y.css html[data-scale="1..5"] .btn:focus` | 1–5 |
| focused | `a11y.css .is-invalid:focus` | 6–8 |
| blurred-after-focus | `a11y.css .is-invalid` (rest owner restored) | 1–8 |
| disabled | `a11y.css .is-invalid` | 1–8 |

On the **real** `/workout_log` element the owner is
`components.css :where(.form-control).input-calm-inset` in every state — a
**layered** `!important` inside `@layer workout`, which outranks a11y's
unlayered `!important` under the same inversion described in D7. C34 is
therefore not the owner there at all, before or after; de-weighting it changes
nothing. So across every measured state C34 is either the owner and stays the
owner, or was never the owner — there is no state in which removing the
annotation moves anything.

Corroboration from the full matrix: 512 matched contexts, 13,980 element
observations, owner 3,784, **owner-after-de-weighting 3,784**, value identical
13,980/13,980, reversion clean 13,980/13,980, 0 mutation failures.

**Counter-evidence that the method can fail this test.** The same pass, pointed
at `.is-invalid:focus` (C36) instead, reports owner and value changes in 12 of
32 measurements. The procedure that certified C34 rejects its own rule-mate.

### 3.2 C50 — `.selection-field.has-validation-error label { color }` — CERTIFICATION FAILED, RETAINED

`static/css/a11y.css:693`, chain *(none)*, `color: #dc3545 !important`, token
offset 18619–18629.

The exact structure is reached, and by the shipping path: clicking
`#add_exercise_btn` with no exercise selected runs `validateRequiredSelections()`
→ `setFieldValidationState('exercise', true)` → `container.classList.add(
'has-validation-error')` on the `.exercise-selector.selection-field` at
`templates/workout_plan.html:211`, whose `<label for="exercise">` is the subject.

| Variant | Measurements | Value differences | **Owner differences** |
|---|---|---|---|
| real rendered instance | 30 | 0 | 0 |
| exact synthetic instance | 30 | 0 | 0 |
| **both ancestors carry `.has-validation-error`** | 30 | **0** | **15** |
| light → dark → light toggle | 3 | 0 | 0 |

**The failure.** When an ancestor also carries `.has-validation-error`, a label
matches both a11y's rule and `pages-workout-plan.css:4449`
`.cascade-dropdown-wrapper.has-validation-error label`. Both are **(0,2,1)**
(verified with `scripts/css_audit/specificity.py`), both are unlayered, and the
page bundle loads **after** `a11y.css` (`templates/base.html:23` vs the
`page_css` block). Removing a11y's `!important` therefore loses the
source-order tie: the declaration owner moves to `pages-workout-plan.css` in
**15/15 light-mode measurements**. The page rule declares the same `#dc3545`, so
the **computed value is identical** — this is precisely the "same value, new
owner" case control **CTLE** exists to catch, and the packet's bar is *zero
computed-value **and** zero declaration-owner differences*.

The first version of this stress state did **not** catch it: it targeted
`.selection-field.has-validation-error label` and `querySelector` returned a
label that only a11y's rule reaches, so the state never actually stressed
anything and reported clean. The check now tags the specific label matching
**both** selectors and fails if no such label exists.

**The census oracle alone would have shipped C50 — the packet's most important
methodological result.** The full matrix reports C50 `REMOVABLE` both before and
after the edit, and it is not wrong to do so: its synthetic pass adds
`.has-validation-error` only to `.selection-field`, never to a
`.cascade-dropdown-wrapper`, so **the doubly-matched label the failure depends
on is never constructed**. A sweep can only adjudicate the states it builds.
Ownership-by-sentinel answers *"does this declaration win?"*; it does not answer
*"which declaration wins?"*, and only the second question exposes a same-value
owner transfer.

**M6b — an annotation that is asymmetric with a retained sibling requires a
declaration-owner adjudication, not a census verdict.** Binding on the remaining
re-weighting packets (`f2`, and any later `!important` work).

**Why it is retained rather than argued away.** The doubly-matched state does
not appear to be reachable in the shipping app today: the routine field is a
hidden input, so `setFieldValidationState` takes its `isCascadeRoutine` branch
and adds `has-validation-error` to `.cascade-dropdown-wrapper` elements rather
than to the enclosing `.selection-field`. That is a reachability *argument*, and
this arc's standing rule — inherited from d1 and the whole WP4.3i arc — is that
absence from templates is a hypothesis, not proof. A measured owner change is
proof. C50 keeps its `!important`.

**Two further findings recorded rather than acted on.** In dark mode on the real
page the label colour is owned by
`pages-workout-plan.css [data-theme="dark"] #workout[data-page="workout-plan"] .form-label`
(ID-level, `!important`) — **not** by a11y's dark twin C51, which is outranked
there. And C51 itself measures `owned 84 / ownedKept 0`: de-weighting it loses
ownership outright. Both confirm the retention; neither is in this packet's
scope to change.

---

## 4. Retention ledger

All 51 annotations, classified. The classes are disjoint and sum to 51.

| Class | Count |
|---|---|
| 1. Certified removal | **1** |
| 2. Certification attempted and **failed** → retained | **1** |
| 3. Live / behaviour-changing retentions | **16** |
| 4. Never-owner / never-matched, uncertified retentions | **1** |
| 5. Chromium-invisible or engine-dropped retentions | **12** |
| 6. Protected focus / accessibility retentions | **20** |
| | **51** |

Class 2 is a distinguished sub-class of "removals": it is the only annotation
this packet tried to remove and could not. It is called out separately so a
later reader does not re-nominate it as an untried candidate.

### 4.1 Certified removal (1)

| Id | Line | Selector | Property |
|---|---|---|---|
| C34 | 502 | `.is-invalid` | `box-shadow` |

### 4.2 Certification failed → retained (1)

| Id | Line | Selector | Property | Why retained |
|---|---|---|---|---|
| C50 | 693 | `.selection-field.has-validation-error label` | `color` | declaration owner moves to `pages-workout-plan.css:4449` in 15/15 light-mode ancestor-stress measurements (§3.2) |

### 4.3 Live / behaviour-changing retentions (16)

De-weighting these changes a computed value or a declaration owner in the full
matrix. They are live and are not removal candidates.

| Id | Line | Selector | Property | Verdict |
|---|---|---|---|---|
| C09 | 325 | `html[data-scale]` *(`@media print`)* | `zoom` | value-changes |
| C33 | 501 | `.is-invalid` | `border-color` | value-changes |
| C37 | 544 | `#liveToast.bg-warning` | `background` | value-changes |
| C38 | 545 | `#liveToast.bg-warning` | `color` | owner-changes |
| C39 | 549 | `#liveToast.bg-warning .btn-close` | `filter` | owner-changes |
| C40 | 556 | `#liveToast.bg-info` | `background` | value-changes |
| C41 | 561 | `#error-message-container.d-none` | `display` | owner-changes |
| C42 | 657 | `.form-select.is-invalid-required, .wpdd…` | `border-color` | value-changes |
| C43 | 658 | `.form-select.is-invalid-required, .wpdd…` | `box-shadow` | value-changes |
| C44 | 665 | `.form-select.is-invalid-required:focus, …` | `border-color` | value-changes |
| C45 | 666 | `.form-select.is-invalid-required:focus, …` | `box-shadow` | value-changes |
| C46 | 672 | `[data-theme="dark"] .form-select.is-invalid-required…` | `border-color` | value-changes |
| C47 | 673 | `[data-theme="dark"] .form-select.is-invalid-required…` | `box-shadow` | value-changes |
| C48 | 678 | `[data-theme="dark"] …is-invalid-required:focus` | `border-color` | value-changes |
| C49 | 679 | `[data-theme="dark"] …is-invalid-required:focus` | `box-shadow` | value-changes |
| C51 | 697 | `[data-theme="dark"] .selection-field.has-validation-error label` | `color` | value-changes |

### 4.4 Never-owner / never-matched, uncertified retentions (1)

| Id | Line | Selector | Property | Status |
|---|---|---|---|---|
| C10 | 330 | `.scale-control, .accessibility-dropdown` *(`@media print`)* | `display` | `never-matched` in 11,654/11,654 contexts |

`.scale-control` is the legacy generation **d1 deleted**, and
`.accessibility-dropdown` renders nowhere. The annotation is retained because
d2's approved transformation cannot be proven against a real effective-owner
state: there is no state in which it owns, so there is nothing to certify.
"Never observed to matter" is not "proven not to matter", and print media is
invisible to every screen capture in the gate set.

### 4.5 Chromium-invisible / engine-dropped retentions (12)

Not measurable by this oracle at all, therefore not certifiable by it.

| Ids | Lines | Cause |
|---|---|---|
| C01–C08 | 95–119 | inside `@-moz-document url-prefix()`; Chromium never parses the at-rule, so the rule object does not exist (`rule-absent`) |
| C19, C23, C27, C32 | 434, 471, 483, 496 | `-moz-box-shadow`; dropped by Chromium's declaration parser (`declaration-absent`, live priority `""`) |

These are Firefox-facing by construction — the `@-moz-document` block is the
Firefox fallback for the scale system, which is documented in the source as
unsupported there. A Chromium-only harness reporting nothing about them is a
statement about the harness.

### 4.6 Protected focus / accessibility retentions (20)

`a11y.css:396-497` is the app-wide focus-visibility guarantee: a suppression
half (`:focus`), a restore half (`:focus-visible`), and a per-scale re-suppression
ladder for `data-scale` 1–5. Plan v2's guard on this file is explicit — no
focus-visible or skip-link rule may be weakened to reduce an `!important` count.
Every one of these 20 also measured live (`value-changes` or `owner-changes`),
so the protection and the measurement agree.

| Ids | Lines | Family |
|---|---|---|
| C11–C12 | 396–397 | `:focus` global suppression |
| C13–C15 | 412–414 | `:focus-visible` restore (contract-pinned selector) |
| C16–C18 | 431–433 | per-scale `:focus` re-suppression |
| C20–C22 | 468–470 | per-scale `.btn:focus` |
| C24–C26 | 480–482 | per-scale `.modal *:focus` |
| C28–C31 | 492–495 | per-scale `:focus-visible` |
| C35–C36 | 506–507 | `.is-invalid:focus` — the focus half of the validation pair |

---

## 5. Gate record

| Gate | Result |
|---|---|
| `tests/test_css_wp4_4_a11y_contracts.py` | **22 passed** (16 d1 + 6 d2) |
| Red-path proof | **22/22** go red under their own violation; every source restored **sha256-identical**; green after — **but see the correction below, the first run of this proof was broken** |
| Full `pytest tests/` | **2,268 passed, 1 skipped** (503.85s; independently re-run at 431.27s, same counts) |
| Shared `test_css_cascade_contracts.py`, `test_visual_selector_contracts.py`, `test_css_wp4_4_a_baseline_contracts.py` | run **unedited** inside the full suite; `git status` on them is empty |
| `accessibility`, `dark-mode`, `smoke-navigation`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening`, `nav-dropdown` | **127 passed** (3.6m); independent re-run of the same selector set **133 passed** (4.5m) |
| `visual.spec.ts`, Chromium, full matrix, `PW_VISUAL_SEED=1` | **65 passed, 1 failed** — the ledgered red, below |
| Positive flip check (`d2_flip.mjs`) | **PASS** |
| Stylelint, seven surfaces | **2,850 → 2,849 (−1)**, no rule increased, **0** parse errors |
| Snapshot / helper integrity | **0** changed paths under `e2e/__screenshots__/`, `e2e/visual-helpers.ts`, `playwright.config.ts`, `scripts/css_audit/` |

Test count reconciles: `f1` recorded 2,262 passed on `main`; this branch adds
the 6 new d2 contracts and collects **2,268**.

### 5.0 Correction — the red-path proof was itself broken on its first run

This is recorded rather than quietly repaired, because it is the same failure
class the packet exists to guard against: **a check that cannot fail proves
nothing, and a mutation that does not apply is exactly such a check.**

`redpath_d2.py` first reported **14/22**, with **8 cases silently no-op**. The
sources on this checkout are **CRLF**, and every mutation written with a plain
`\n` matched nothing at all — the script printed a line per case regardless, so
the eight broken cases were indistinguishable from real ones at a glance. The
affected cases were `mixed_selector_lists`, `focus_visible_premise` (×2),
`no_custom_property`, `certified_removal_kept`, `asymmetric_sibling`, the
`.is-invalid:focus` retention, and the `@-moz-document` retention.

Three of those guard **d2's own dispositions**, so before the repair the packet
had *no* proof that its asymmetric-sibling, protected-focus and
Chromium-invisible contracts could fail.

**Repair.** The replace helper now tries both line endings; the regex helper
widens `\n` to `\r?\n` (with one pattern fixed by hand — in a *raw* string `\n`
is backslash-plus-n, so the widening never saw a newline to widen); and a no-op
is now printed as **"NO-OP (proof broken)"** and counted as a failure.

**Post-correction: 22/22 go red, all sources restored byte-identically, suite
green after.** The `22/22` figure in the table above is only true of the
repaired script.

### 5.1 The one visual failure is the ledgered animated-logo red, in band

`visual.spec.ts:40 › visual baseline: workout-plan › workout-plan desktop dark`
— **875 pixels, 882 on retry, 875 on the second retry.**

That is the lower half of the reconciled union band **875/882 ∪ 1,039/1,046**
accepted at the `f1` boundary. `a11y.css` does not style the animated logo, the
change is confined to a `box-shadow` on `.is-invalid`, and no `.is-invalid`
element exists on the Workout Plan page at rest. `maxDiffPixels` was **not**
touched and **no snapshot was written** (0 changed paths under
`e2e/__screenshots__/`). **No non-ledger visual difference appeared** in any
route, theme or viewport. `d2` does not run the Linux deep gate (N8).

### 5.2 Positive flip check — stated by source identity

A zero differential is equally consistent with "the packet did the right thing"
and "the probe went blind". `artifacts/wp4_4/d2_flip.mjs` therefore asserts the
change positively, in the live CSSOM, matching on *(chain, engine-canonical
selector, property)*:

| Check | Result |
|---|---|
| inventory candidates | 50 |
| located in live CSSOM / engine-invisible | **38 / 12** (= 50) |
| of the located, priority `important` | **38** |
| of the located, priority `""` | **0** |
| de-weighted declaration still exists, exact value | **yes** — `rgba(220, 53, 69, 0.25) 0px 0px 0px 0.2rem` |
| its priority is now `""` | **yes** |
| asymmetric sibling `border-color` still `important` | **yes** |

Before the change the same probe located **39 + 12 = 51**. One annotation left
the located population and nothing else moved.

*The first run of this check reported FAIL for a reason worth recording: it
compared the CSSOM value against the **source spelling**
`0 0 0 0.2rem rgba(220, 53, 69, 0.25)`, while Chromium serializes `box-shadow`
colour-first with normalized lengths. The assertion was wrong, not the CSS —
defect D3's lesson recurring inside the verification of the fix for D3. The
expected value is now round-tripped through the engine.*

### 5.3 Sweep controls (the run the certification rests on)

| Control | Result |
|---|---|
| cascade controls CTLA–CTLE | **5/5 pass** |
| `@layer` / `!important` inversion, both directions (CTLC, CTLC2) | **pass** |
| defect-7 control CTLF (layered `!important` transition) | **pass**; red path `--no-settle` → `owned=0/1`, run aborts |
| colour-normaliser self-check | **6/6** — known-equal collapses, 1/255 channel and alpha steps kept |
| same-CSS control (M5) | **466 paired runs, 0 differing records** |
| sheet contamination (fingerprint before/after every context) | **0 contexts** |
| M6a reversion | **105,956 / 105,956 element-records** |
| mutation integrity | **0** failures across all candidates |
| contexts | **11,654** |

### 5.4 Rest-state differential — reported with its control, which invalidates it

`scripts/css_audit/runtime_probe.mjs` was run three times (before, after, and a
second after on identical CSS). Its own internal self-checks passed on every
run (`control=PASS`, `sentinel=PASS`, `shot=PASS`, 22/22 captures).

The **cross-run** differential, however, is **not usable as evidence**, and this
is reported rather than quietly dropped:

| Oracle | records | before→after | after→after2 *(same CSS)* |
|---|---:|---:|---:|
| paint | 19,668 | 2,678 | **2,678** |
| motion | 19,668 | 2,634 | **2,634** |
| motionReduced | 19,668 | 2,632 | **2,632** |
| declaration owner (`matchedRules`) | 3,600 | 1,924 | **1,924** |

The same-CSS control reproduces the differential **exactly, capture for
capture** (273/273, 530/530, 847/847, 898/898, 1,332/1,332, 1,029/1,029, 1/1,
and 0/0 on the three captures that differ in neither). Under M5 that
invalidates the comparison as a measure of *this change* — and it identifies the
cause: every run boots `app.py`, whose startup writes a new automatic backup
row, so data-dependent pages legitimately differ between any two runs.

**Attempted repair, and why it was abandoned.** Restoring the seeded DB before
each capture removes that variance, but with the full visual fixture loaded the
harness's own screenshot control **fails** on `workout-plan`
(`shot=FAIL(3906px)`) because the seeded content animates. Trading a known
data-drift confound for a failing harness self-check is not an improvement, so
the DB-stabilised run is recorded as a finding and not used.

**What carries the packet instead** is §5.2's flip check and §5.3's sweep, both
of which are deterministic (0 same-CSS drift over 466 paired runs) and measure
declaration ownership directly rather than inferring it from a whole-page
snapshot. This is a limitation of the shared runtime harness on a re-weighting
packet, and it is left for `f2`/`g` to fix rather than patched over here.

### 5.5 Keyboard focus-indicator census — measured against its own noise floor

Packet `d` must not weaken keyboard focus visibility, so this is reported with a
control rather than as a bare number. An element counts as having an indicator
when `outline-style ≠ none` with `outline-width > 0`, **or** `box-shadow ≠ none`.

The first comparison looked like a regression — 1,329/2,046 before against
1,307/2,040 after — and it was **not** one. `data/database.db` was rewritten
between those two matrices, so they traversed different DOMs; the differing stop
counts are the tell. Re-measured in one session against one database:

| `a11y.css` | Tab stops | with indicator |
|---|---:|---:|
| `main` (`c280a6e1…`) run 1 | 2,040 | 1,306 |
| `main` run 2 | 2,040 | **1,309** |
| `main` run 3 | 2,040 | 1,308 |
| **d2** (`adce3716…`) run 1 | 2,040 | 1,308 |
| **d2** run 2 | 2,040 | 1,308 |

`main` disagrees with itself across a spread of **3**; d2's 1,308 sits inside
it, and the stop count is identical in all five runs. The four differing
contexts all resolve to the **same** element,
`html/body/header/div/nav/ul[0]/li[2]/a` (a navbar link) at `data-scale` 3, and
the direction is inconsistent — gained in three contexts, lost in one. That is
flake, not causation. The mechanism is the D7 class: the keyboard pass reads
computed style without the settle repair, so a transitioned navbar link can be
read mid-flight. **No effect attributable to d2**, and `.is-invalid` is applied
nowhere during a Tab traversal, so the de-weighted declaration cannot reach this
measure at all.

### 5.6 Same-CSS pixel control settles authorship of the visual red

With `a11y.css` restored **byte-identical to `main`** (`git diff` empty,
sha `c280a6e1…`) in the same worktree, the same spec produced the **identical
875 / 882 / 875**. The red is independent of this packet, exactly as the same
control established at the `b`, `c` and `f1` boundaries. The packet version was
then restored and re-verified (sha `adce3716…`, contracts 22/22).

---

## 6. Preservation invariants

| Invariant | Verdict |
|---|---|
| **V1** no visual difference | 65/66 visual captures byte-identical; the 1 failure is the ledgered logo red at 875/882, in band |
| **V2** no rebaseline | 0 changed paths under `e2e/__screenshots__/`; no `visual-helpers.ts` or `playwright.config.ts` change |
| **V3** re-weighting is *this packet's* purpose, and is bounded | exactly **1** annotation de-weighted, certified; `selector-max-id` +0, `selector-max-specificity` +0 — no specificity was traded for weight |
| **V4** no duplication increase | `no-duplicate-selectors` 25 → 25; `declaration-block-no-duplicate-properties` 2 → 2 |
| **V5** contribution | −1 `!important`; scope was not widened to improve the count |
| **V6** no conflict | single writer, single production file |
| **N2** layer membership frozen | `@layer` 0 → 0, contract-pinned |
| **M9** no custom property touched | 17 → 17, contract-pinned |
| **PR#9** focus guarantee | all 20 focus-family annotations retained and contract-pinned; keyboard traversal green in `accessibility.spec.ts` (127-test run) |

---

## 7. Out of scope / carried forward

- **The other 49 retentions.** Any future attempt needs its own certification
  run; `never-owner` and `never-matched` are *absence of proof*, not proof.
- **The 12 Chromium-invisible annotations** (§4.5) — certifying them needs a
  Firefox oracle, which this arc does not have.
- **`.is-invalid:focus` (C35/C36)** — measured live and protected; the focus
  half of the validation pair.
- **D7's consequences for earlier packets.** The suppressor defect was present
  for every WP4.4 packet that used a sentinel. This packet does not re-open
  `a`–`f1`; it records the defect, ships the repair in its own harness, and
  flags that `scripts/css_audit/runtime_probe.mjs` still carries the beatable
  CSS-only suppressor. **Fixing the shared harness belongs to a packet that
  owns it (A11), not to `d2`.**
- **The rest-state differential limitation** in §5.4.
