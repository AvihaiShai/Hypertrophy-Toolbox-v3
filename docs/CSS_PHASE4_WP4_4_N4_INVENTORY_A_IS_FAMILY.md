# WP4.4 N4 checkpoint — Inventory A: the complete `components.css` `:is()` family

**Status:** pre-change inventory for the N4 owner checkpoint. **Read-only — no production
file changed.** This document authorizes nothing; it is one of the two inventories ruling
N4 requires to be presented *before* any WP4.4-i edit.

**Measured commit:** `a895cb043ebfa050429c66ae8749acf65cf0315d` (`main` after PR #209).
**`static/css/components.css`:** SHA-256
`883e6aa85564c42b36ca801529081b279f119e5c99a539dc235bc84d72107964`, 5,207 lines — the
post-WP4.4-h file, byte-identical to the SHA that packet's evidence records as its "after".

---

## 1. What N4 asks for, and what this covers

Ruling **N4** ([PLANNING.md](css_phase4_wp4_4/PLANNING.md) §New owner decisions) stops the
arc after `h` and requires *"i's enumerated repair shape and both pre-change inventories
(the complete `:is()` family from g/h, and the G3 regions A–C measurement)"*. This is the
first. The second is
[`CSS_PHASE4_WP4_4_N4_INVENTORY_B_REGIONS_ABC.md`](CSS_PHASE4_WP4_4_N4_INVENTORY_B_REGIONS_ABC.md).

"Complete" means all **19** `:is(` tokens in the file, not only the cross-route ones —
R3 condition 1 needs a defensible closure argument, and that requires enumerating the
constructs that are *out* of scope as explicitly as the ones that are in.

| Group | Rules | `:is(` tokens | In WP4.4-i scope? |
|---|---:|---:|---|
| **§3** Shared cross-route family, four-branch | 12 | 13 | **yes** — this is the specificity leak |
| **§4** Reduced-motion rule, three-branch | 1 | 1 | **yes** — same leak, narrower branch set |
| **§5** `input.input-calm-inset:is(#weight, …)` | 4 | 5 | **no** — already ID-scoped, not a cross-route leak |
| **Total** | **17** | **19** | |

Seventeen rules carry 19 tokens because two rules have two selector lines that each carry
one: the rule opened at `:3335` (second line `:3336`) and the rule opened at `:3749`
(second line `:3750`).

---

## 2. Terminology corrections this inventory makes

Three statements in the planning documents describe the family shape incorrectly against
the measured file. Each is corrected here; none changes any ruling.

### 2.1 The specificity range is **(1,2,0)–(1,5,3)**, not (1,3,0)–(1,5,3)

Correction **C1** records the family range as **(1,3,0)–(1,5,3)**. That is the range of
per-*rule* maxima. The rule at `:3335` has **two selector lines with different
specificities**, and the lower one is the floor of the whole family:

| Selector line | Specificity |
|---|---|
| `:3335` `:is(…) :where(.table).table-calm` | **(1,2,0)** |
| `:3336` `:is(…) .table.table-calm` | (1,3,0) |

`:where()` contributes zero, so the `:where(.table).table-calm` arm is one class lighter
than its `.table.table-calm` twin. **A repair that reasons about "the family's
specificity" as a single band will get `:3335` wrong** — it is the one arm a page-local
`(0,2,x)` rule is closest to reaching. C1's headline claim is unaffected: every arm still
exports `a = 1`.

### 2.2 `components.css:4433` is now `:4413`; the rule opens at `:4398`

WP4.4-h deleted 138 lines, **20 of them before pristine line 4417**, so every identity in
the reduced-motion block shifts by exactly −20:

| Identity | Pristine (pre-`h`) | Current (post-`h`) |
|---|---:|---:|
| `@media (prefers-reduced-motion: reduce)` opens | 4417 | **4397** |
| rule opens | 4418 | **4398** |
| the `:is()`-bearing selector line | 4433 | **4413** |

Every document that cites this rule as "`:4433`" — G1, packet i's scope row, the
Terminology table — is citing a line that no longer exists. The rule itself is unchanged;
only its address moved. The twelve four-branch rules at `:3335`–`:3411` sit entirely
before `h`'s legal deletion window (lines 4105–5345) and did **not** move.

### 2.3 `:3336` is part of the enumeration (A15)

Packet i's scope row lists thirteen line identities and omits `:3336`. Council item **A15**
already required adding it; this inventory records it as a first-class row (§3, row 1b)
because it is the family's lowest-specificity arm and therefore its highest-risk one.

---

## 3. The shared cross-route family — twelve four-branch rules

All twelve are **unlayered** and sit at the top level of the file, *before* `@layer workout`
opens at `:3539`. Every arm's `:is()` branch set is identical:

```
:is(#workout[data-page="workout-plan"],
    .workout-log-page,
    .summary-frame.frame-calm-glass,
    .progression-plan-container)
```

`:is()` takes the specificity of its most specific argument. That is
`#workout[data-page="workout-plan"]` at **(1,1,0)** — an ID *plus* an attribute, which is
why the family floor is (1,2,0)/(1,3,0) and not (1,1,0)/(1,2,0). Every branch therefore
inherits ID-level weight, **including the three that contain no ID at all**. That is the
leak.

| # | Rule lines | Selector line | Complete selector | Specificity | Decls |
|---|---|---|---|---|---:|
| 1a | 3335–3349 | **3335** | `:is(…) :where(.table).table-calm` | **(1,2,0)** | 12 |
| 1b | 3335–3349 | **3336** | `:is(…) .table.table-calm` | (1,3,0) | ↑ same block |
| 2 | 3351–3358 | 3351 | `:is(…) .table.table-calm > :not(caption) > * > *` | (1,3,1) | 6 |
| 3 | 3360–3366 | 3360 | `:is(…) .table.table-calm thead th` | (1,3,2) | 5 |
| 4 | 3368–3375 | 3368 | `:is(…) .table.table-calm tbody td` | (1,3,2) | 3 |
| 5 | 3377–3379 | 3377 | `:is(…) .table.table-calm tbody tr:nth-child(even) td` | (1,4,3) | 1 |
| 6 | 3381–3384 | 3381 | `:is(…) .table.table-calm tbody tr:hover td` | (1,4,3) | 2 |
| 7 | 3386–3388 | 3386 | `:is(…) .table.table-calm tbody tr:last-child td` | (1,4,3) | 1 |
| 8 | 3390–3393 | 3390 | `[data-theme='dark'] :is(…) .table.table-calm` | (1,4,0) | 2 |
| 9 | 3395–3398 | 3395 | `[data-theme='dark'] :is(…) .table.table-calm thead th` | (1,4,2) | 2 |
| 10 | 3400–3403 | 3400 | `[data-theme='dark'] :is(…) .table.table-calm tbody td` | (1,4,2) | 2 |
| 11 | 3405–3407 | 3405 | `[data-theme='dark'] :is(…) .table.table-calm tbody tr:nth-child(even) td` | (1,5,3) | 1 |
| 12 | 3409–3411 | 3409 | `[data-theme='dark'] :is(…) .table.table-calm tbody tr:hover td` | (1,5,3) | 1 |
| | | | | **38 declarations** | |

**Condition:** all twelve are unconditional — no `@media`, no `@supports`, no `@layer`.
They apply in both themes (rules 8–12 gate on `[data-theme='dark']` by selector, not by
media query) and at every width.

### 3.1 Branch → route mapping

| Branch | Specificity | Template anchor | Route |
|---|---|---|---|
| `#workout[data-page="workout-plan"]` | (1,1,0) | [templates/workout_plan.html:10](../templates/workout_plan.html#L10) | Workout Plan `/workout_plan` |
| `.workout-log-page` | (0,1,0) | [templates/workout_log.html:10](../templates/workout_log.html#L10) | Workout Log `/workout_log` |
| `.summary-frame.frame-calm-glass` | (0,2,0) | [templates/weekly_summary.html:18](../templates/weekly_summary.html#L18) **and** [templates/session_summary.html:18](../templates/session_summary.html#L18) | Weekly Summary `/weekly_summary` **and** Session Summary `/session_summary` |
| `.progression-plan-container` | (0,1,0) | [templates/progression_plan.html:12](../templates/progression_plan.html#L12) | Progression `/progression` |

**Four branches, five routes.** The single `.summary-frame.frame-calm-glass` branch matches
on both summary pages. Per the binding terminology rule, never write "four contexts" as a
synonym for "five routes"; every gate that says "all affected routes" means all five.

---

## 4. The thirteenth rule — three branches, reduced motion only

| Field | Value |
|---|---|
| Rule lines | **4398–4415** (pristine 4418–4435) |
| `:is()`-bearing selector line | **4413** (pristine 4433) |
| Condition | `@media (prefers-reduced-motion: reduce)`, opened at **4397** (pristine 4417) |
| Layer | unlayered |
| Complete `:is()` selector | `:is(#workout[data-page="workout-plan"], .workout-log-page, .progression-plan-container) .table.table-calm tbody td` |
| Branch set | **3** — omits `.summary-frame.frame-calm-glass` |
| Specificity | **(1,3,2)** |
| Declarations | **1** — `transition: none !important` |

The rule's selector *list* has sixteen arms (buttons, cards, inputs); only the sixteenth
carries `:is()`. The other fifteen are ordinary class selectors and are out of scope.

**The three-branch set is a pre-existing behavioural asymmetry, not a typo.** Because
`.summary-frame.frame-calm-glass` is absent, reduced-motion transition suppression is **not
applied to Weekly Summary or Session Summary table cells**. Normalizing it would be a
visible behavioural change on two routes under `prefers-reduced-motion: reduce` and
requires separate owner approval — it must not be "fixed in passing" by i.

---

## 5. The five remaining `:is(` tokens — enumerated and excluded

Four rules, all inside `@layer workout` (opened at `:3539`), all already scoped under
`#workout[data-page="workout-plan"]`. The `:is()` here lists **element IDs of the Workout
Plan input fields**, so it is a within-page shorthand, not a cross-route leak.

```
:is(#weight, #sets, #rir, #rpe, #min_rep, #max_rep_range)
```

| Rule lines | Selector line | Shape | Specificity | Decls |
|---|---|---|---|---:|
| 3635–3642 | 3635 | `#workout[…] .input-fields-group .input-group input.input-calm-inset:is(…)` | (2,4,1) | 6 |
| 3655–3661 | 3655 | …`:hover:not(:disabled)` | (2,6,1) | 5 |
| 3678–3687 | 3678 | …`:focus` | (2,5,1) | 6 |
| 3749–3757 | 3749 | `[data-theme='dark'] #workout[…] .input-fields-group .input-group input.input-calm-inset:is(…)` | (2,5,1) | 6 |
| 3749–3757 | 3750 | `[data-theme='dark'] #workout[…] .input-fields-group input.input-calm-inset:is(…)` | (2,4,1) | ↑ same block |

**Why excluded from i.** These carry `a = 2` — one ID from the ancestor `#workout`, one
from the `:is()` list — but both IDs are *already on the Workout Plan page*. No other route
can match them, so removing the `:is()` weight would change nothing for any other page.
They are also inside `@layer workout`, and **N2 freezes layer membership arc-wide**, so
touching them is barred independently of scope. Enumerated here so R3 condition 1 closes
over all 19 tokens.

---

## 6. What this inventory does *not* establish

- **It does not authorize a repair.** N3 requires i to proceed only on branches where it is
  *proven* that no page-local rule would become a winner. This document establishes the
  family's shape and weight; Inventory B establishes what is currently suppressed behind it
  on Workout Log. Neither is a safety proof for any specific repair shape.
- **It does not cover the other four affected routes' page-local rules.** G3 names Workout
  Log specifically. Workout Plan, Weekly Summary, Session Summary and Progression each need
  the same would-become-winner sweep before a branch touching them can be called safe — see
  the risk list at the N4 checkpoint.
- **It is a rest-state structural reading**, not a runtime ownership census. Rules 6 and 12
  carry hover paint, and interaction states are excluded from the deletion packets by M12;
  they are *not* excluded from i, which is exactly why i needs its own hover-capable oracle.

## 7. Reproduction

```bash
# identity
sha256sum static/css/components.css     # 883e6aa8…
grep -c ':is(' static/css/components.css # 19

# line translation across the WP4.4-h squash
git diff -U0 4b7ca58 b2b1cb7 -- static/css/components.css   # 138 removed, 20 before 4417
```

The enumeration and specificity figures were produced with the same unit-checked
specificity model committed as part of Inventory B
([`scripts/css_audit/n4_regions_abc.mjs`](../scripts/css_audit/n4_regions_abc.mjs),
`specificityOf` + `checkSpecificityModel`), which handles `:is()` / `:where()` / `:not()` /
`:has()` and never splits a selector list on a naive comma (M4). Its ten unit cases pass;
one of them (`:is(#a, .b) .table.table-calm tbody td` → `(1,2,2)`) caught a wrong
hand-computed expectation during authoring, which is why the model is asserted before use
rather than trusted.
