# Table breakpoint-helper re-audit — evidence

Re-audit of the nine `.tbl-show-*` / `.tbl-hide-*` rules WP4.4-e deferred in
`static/css/layout.css`. Gate 0 owner-approved in the commissioning prompt; Gate 1
owner-approved 2026-08-04 after a full `/council-plan` (three reviewers, **26 findings,
26 dispositions**).

**This document supersedes [`CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md`](../CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md)
§4a and §10.** That packet's stated reason for deferring the family — *"No control
element can distinguish them: that is an inherent limit, not a fixable probe defect"* —
has been measured and refuted. `_E_LAYOUT_` is left byte-unchanged as a closed packet's
historical record; see deferral **D-1**.

Base commit: `ac2923b`. Production ownership: `static/css/layout.css` only.
Planning artifact: [`PLANNING.md`](PLANNING.md).

---

## 1. Outcome

**Outcome A — all nine rules deleted atomically.** `static/css/layout.css:1589–1634`,
**47 lines removed, 0 inserted**, pure deletion.

| | |
|---|---|
| `layout.css` sha256 before | `0e447a58ec2e649c393a1d0ae37c007559f4b617f1bc613d155ccdbf35e3fd7a` |
| `layout.css` sha256 after | `3e13542e2b0a164398d517658e87f813c09c8af93aa570f57932abc08dadf4f9` |
| lines | 1,726 → 1,679 (−47) |
| bytes | 46,315 → 45,586 (−729) |

The occurrence-count pin `DEFERRED_HELPER_COUNTS` is replaced by five contracts (C1–C5),
each proven to fail under its own violation.

---

## 2. The refutation — what WP4.4-e actually measured

WP4.4-e's probe host was a bare `<div>`. A `<div>`'s UA initial `display` is **`block`**,
which is exactly the value the three `@media` overrides declare, so on that host the rule
and its control read identically. The packet recorded this as a property of the rules.

It is a property of the host.

The re-audit uses three hosts whose UA initial `display` is **not** `block`, in valid
ancestor chains, with **no author CSS injected to manufacture a baseline**:

| Host | UA initial `display` |
|---|---|
| `<span>` | `inline` |
| `<li>` inside a `<ul>` | `list-item` |
| `<td>` inside `table > tbody > tr` | `table-cell` |

On all three, every one of the nine rules is distinguished from a control that fails its
selector by exactly one compound.

**A `<span>` carrying a display utility is not a contrived premise** — it is the ordinary
way such a utility is used. No unrealistic construction was needed; WP4.4-e simply picked
the one host type that could not see the answer.

---

## 3. Controls — reported before the result

`.claude/rules/verification.md`: *"A result without its control is not reportable."*

| Control | Before-run | After-run |
|---|---|---|
| Same-CSS control (M5) — two independent full runs, identical CSS | **0 differing / 30,316** | *(§7)* |
| Sentinel took effect, per record | **8,580 / 8,580** | *(§7)* |
| Sentinel reverted cleanly, per record | **8,580 / 8,580** | *(§7)* |
| Known-live — `.tbl-controls`, `.tbl-view-mode-toggle` | **1,716 / 1,716** | *(§7)* |
| Known-dead — `.tbl-show-zz` | **858 / 858** | *(§7)* |
| Control-baseline — control at UA initial **and** no author `display` rule matches it | **858 / 858** | *(§7)* |

### 3a. A control defect, found and fixed before any deletion

The first version of the oracle used **`.tbl-wrap`** as the known-live control. It read
**0 / 78** — a failing control, which under `verification.md` voids the entire run.

The cause: `layout.css` styles `.tbl-wrap` (`position`, `max-width`, `overflow-x`,
`overflow-y`, `container-type`) but **never with `display`**, and the oracle resolves
ownership of `display`. **This is WP4.4-e's own "hand-written property list" defect
reappearing on the control side** — the same class of error, in the packet auditing it.

Fixed by moving the known-live control to two classes that *do* declare `display` in
`layout.css`, are created at runtime, and are retained by this packet:

| Control class | Declaration | Source | Created at |
|---|---|---|---|
| `.tbl-controls` | `display: flex` | `layout.css:1423` | `static/js/table-responsiveness.js:112` |
| `.tbl-view-mode-toggle` | `display: inline-flex` | `layout.css:1451` | `static/js/table-responsiveness.js:239` |

Both then read **1,716 / 1,716**.

**Generalized so it cannot recur silently:** the oracle now also validates the *control*
host — its computed `display` must equal its UA initial **and** CDP must report no author
rule declaring `display` on it (**858 / 858**). A control that drifts off its initial now
fails loudly instead of quietly certifying whatever it is compared against.

### 3b. Every loaded stylesheet enumerated, including the unreadable ones

The `.sr-only` lesson from WP4.4-e — a local grep is not a census of what the browser
loaded — is closed here rather than repeated.

No stylesheet reachable at runtime defines any candidate class. Exactly **two**
cross-origin sheets are unreadable from CSSOM, and both were fetched out-of-band:

| Sheet | Contents | Verdict |
|---|---|---|
| `fonts.googleapis.com/css2?family=Inter…` | 4 `@font-face` rules, **0** class selectors | cannot define a candidate class |
| `cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css` (on `/progression`) | 16,166 bytes, **0** `tbl` tokens, every selector flatpickr-namespaced | cannot define a candidate class |

**FontAwesome is now vendored locally** at `static/vendor/fontawesome/`, so it is
same-origin, readable, and was scanned. The exact blind spot that caught WP4.4-e's
`.sr-only` cannot recur on this surface.

---

## 4. DR-1 — the decision rule, applied member by member

DR-1 was fixed in Plan v1 **before any measurement existed**, and criterion (h) was added
at council. Outcome A required **all** of (a)–(h) for **all nine**; any single failure
would have selected outcome B for the whole family.

### (a) Static inventory — PASS

Sole definition site: `static/css/layout.css`. **Zero** application sites in
`templates/**`, `static/js/**`, `routes/**`, `utils/**`. No dynamic construction — the
only `tbl-` string literals in `static/js/**` are `tbl-controls`, `tbl-view-mode-toggle`,
`tbl--view-simple`, `tbl--view-advanced`, none of which can produce a candidate name. No
`build/`, `dist/`, `out/` or `.next/` tree exists, so no generated copy was available to
be mistaken for evidence. Raw output: `artifacts/tblhelpers/static_inventory.txt`.

### (b) Runtime census — PASS

Full-selector `querySelectorAll`, taken **before any synthetic is injected**, across
**286 contexts** (11 routes × 2 themes × 13 widths):

| Class | Census |
|---|---|
| all six candidates | **0** in all 286 |
| `.tbl-wrap`, `.tbl` *(positive control)* | **338** each |
| `.tbl-controls`, `.tbl-view-mode-toggle` *(positive control)* | **26** each |

The positive control is what makes the zero a finding: the census demonstrably reaches
pages where `layout.css` is doing work.

### (c) Before-state positive effect and (d) structural ownership — PASS

Applicability is read from **measured `matchMedia` inside the page**, never from the
nominal viewport width. Widths: `375, 600, 819, 820 · 821, 822, 1000, 1199, 1200 · 1201,
1202, 1440, 1920` — immediately below, at and above both boundaries, plus interior
widths. The nominal width matched the measured band at all 13.

| # | Rule | Source | Declares | Distinguished | Structural owner OK |
|---|---|---|---|---|---|
| 1 | `.tbl-show-sm` base | 1594–1596 | `display: none` | **594 / 594** | 594 / 594 |
| 2 | `.tbl-show-md` base | 1598–1600 | `display: none` | **528 / 528** | 528 / 528 |
| 3 | `.tbl-show-lg` base | 1602–1604 | `display: none` | **594 / 594** | 594 / 594 |
| 4 | `.tbl-hide-sm` | 1607–1609 | `display: none` | **264 / 264** | 264 / 264 |
| 5 | **`.tbl-show-sm` override** | 1611–1613 | **`display: block`** | **264 / 264** | 264 / 264 |
| 6 | `.tbl-hide-md` | 1617–1619 | `display: none` | **330 / 330** | 330 / 330 |
| 7 | **`.tbl-show-md` override** | 1621–1623 | **`display: block`** | **330 / 330** | 330 / 330 |
| 8 | `.tbl-hide-lg` | 1627–1629 | `display: none` | **264 / 264** | 264 / 264 |
| 9 | **`.tbl-show-lg` override** | 1631–1633 | **`display: block`** | **264 / 264** | 264 / 264 |

**Rules 5, 7 and 9 are the three WP4.4-e declared indistinguishable.** Each is
distinguished in 100% of its applicable contexts.

Each rule is measured **only where its media condition applies**. The three base rules are
superseded inside their own class's `@media` band by a later rule of equal specificity, so
each is observable only *outside* that band — which is why their denominators are the
complements of the override denominators.

Ownership is resolved through CDP `CSS.getMatchedStylesForNode` as
**styleSheetId → sourceURL, plus the rule's source range and enclosing media text**. Never
by substring, never by `nth-child` position, never by re-serialized CSS text.

### (h) Non-vacuity — PASS

Added at council: without it, (c) and (e) are satisfiable on **zero records** — the
inverse of *"a probe that changes nothing proves nothing"*, in a packet whose premise is
that the previous packet mis-measured.

Per-rule universe **858** = 3 hosts × 286 contexts. Band complements hold exactly:

```
594 + 264 = 858      528 + 330 = 858      594 + 264 = 858
```

Every denominator is non-zero and equals its published value.

### Full denominator decomposition

Every ratio in this document decomposes; none is reported as a bare total.

Per context the probe mounts **30 elements** = 3 hosts × 10
(1 control + 6 candidates + 2 known-live + 1 known-dead).

| Figure | Decomposition |
|---|---|
| Sentinel **8,580** | 286 contexts × 30 elements |
| Known-live **1,716** | 286 × 3 hosts × 2 classes |
| Known-dead **858** | 286 × 3 × 1 |
| Control-baseline **858** | 286 × 3 controls |
| Per-rule universe **858** | 286 × 3 |
| **R1** — same-CSS control **30,316** | 286 × **106 records per context** = 11 census + 5 `matchMedia`/viewport + 30 computed `display` + 30 sentinel + 30 declaration-owner |

*(The feasibility spike's unexplained `1560` was `52 contexts × 30`, not `156 × 10`.)*

---

## 5. What was retained, and why it is load-bearing

Deleting these nine removes **no responsive capability**. The live responsive
table-disclosure system is a different family in the same file, and it is untouched:

| Retained | Source |
|---|---|
| `.col--high` / `.col--med` / `.col--low` progressive column disclosure — container queries at 1200/992px, media fallbacks at 1366/1200px, zoom-detection variants | `layout.css:1218–1306` |
| Row-card mode at ≤576px container width | `layout.css:1312+` |
| Print override re-showing `.col--low` / `.col--med` | `layout.css:1569–1575` |
| Print rule `.tbl-controls, .tbl-toolbar { display: none }` — `.tbl-controls` is live | retained whole, contract-pinned |
| `.tbl-controls` (`display: flex`), `.tbl-view-mode-toggle` (`display: inline-flex`) | `layout.css:1423`, `:1451` |
| ResizeObserver card/table view-mode toggle | `static/js/table-responsiveness.js` |
| `[data-theme="dark"]` token block, the separator-contrast block, `.input-frame`/`.action-frame` | unchanged |

`.col--high` is applied by `static/js/modules/workout-plan-table.js:383+` and
`templates/volume_splitter.html:94–97`.

**The empty `LOADING STATE` banner at `layout.css:1584–1586` is deliberately left.** It is
not part of this family — WP4.4-e emptied it when it deleted `.tbl--loading` — and
removing it is an unproven separate cleanup.

**Note on the deletion range.** Plan v1 said `1594–1634`; `:1594` is `.tbl-show-sm {`. The
family's introducing banner is `:1589–1591` and its inline comment `:1593`, so the atomic
unit is **`1589–1634`** plus one trailing blank line, preserving the file's existing
two-blank-line convention between banners. The boundary is **re-derived from file content
by the deleter**, which asserts the block contains exactly six candidate classes, three
`@media`, nine `display` declarations, balanced braces, and none of the must-survive
constructs — and refuses to write on any failed assertion.

---

## 6. Contracts — C1–C5, and why each is stronger

The replaced pin and its three structural weaknesses:

```python
DEFERRED_HELPER_COUNTS = {"tbl-show-sm": 2, ..., "tbl-hide-lg": 1}
```

- **W1** — it pins a **number**, not a state. `2` is satisfied by two live rules and by
  nothing else; it cannot express "gone".
- **W2** — it pins the **stylesheet** only. It says nothing about whether anything
  *applies* the class, which is the premise the deletion rests on.
- **W3** — it pins **one file**. A sibling bundle could define `.tbl-show-md` tomorrow and
  the assertion would stay green.

| # | Contract | Closes | Why stronger |
|---|---|---|---|
| **C1** | `test_breakpoint_helper_family_is_absent_from_layout_css` | **W1** | Asserts a **state** (`0` rule heads), not a tally. Counts rule heads by scanning brace boundaries, so it sees the class at any nesting depth, inside `@media`, and in any position within a compound or descendant chain — including `.foo.tbl-show-sm` and `.tbl-show-sm .bar`, which the selector-shape matcher used elsewhere in the suite would miss. Reports the offender by name. |
| **C2** | `test_breakpoint_helper_family_is_all_or_nothing` | indivisibility | Fails on any partial state in **either** direction — an `@media` override left with no base rule, or base rules left with no overrides. **Outcome-independent**: the same contract holds whether the family is deleted or restored, so indivisibility survives past this packet rather than expiring with it. |
| **C3** | `test_breakpoint_helper_classes_are_unreachable` | **W2**, the largest gap | Turns the deletion's premise into a standing gate. The detector matches the **bare stems `tbl-show` / `tbl-hide` anywhere** in `templates/**` and `static/js/**` — deliberately *simpler* than `test_deleted_classes_are_still_unreachable`'s form-enumerating parser, not a wider version of it. That test enumerates `class="…"` attributes and `classList.add/toggle/replace` literals, so it cannot see `className =`, `setAttribute('class', …)`, or a runtime-assembled name; enumerating more forms only moves the boundary. One substring match subsumes all of them, including `'tbl-show-' + size` and `` `tbl-hide-${size}` ``, which are real class names containing no full class literal. It can only over-fire, never under-fire, and over-firing is the safe direction. Discharges M10 permanently instead of as a one-time measurement. |
| **C4** | `test_breakpoint_helper_classes_have_no_definition_site_in_a_sibling_bundle` | **W3** | Globs **every** `static/css/*.css`, so a bundle added later is covered automatically — unlike the existing five-surface hard-coded list. Excludes `layout.css` by name; C1 owns that file at the stronger rule-head granularity. That split is what makes C4 hold unchanged under both outcomes instead of being red-on-arrival under retention. |
| **C5** | `test_layout_css_has_no_empty_media_block` | new guarantee | Forecloses the specific sloppy deletion — rules removed, three empty `@media` shells left — that passes C1 and leaves a residue a later reader takes for intentional. Scoped to `layout.css`: `pages-workout-log.css:459,464,469,496,501` already carry five whitespace-only `@media` blocks that WP4.3j-b-dead kept deliberately. |

**C1 and C4 are single tests looping `sorted(...)`, never `@pytest.mark.parametrize` over
a glob.** A parametrized glob would make the collected node count a function of the files
present on the collecting machine, and `Test Inventory Drift` is a required
branch-protection context.

**A separate `BREAKPOINT_HELPER_CLASSES` tuple is used.** Extending `DELETED_CLASSES`
would have changed the scope of three unrelated WP4.4-e tests. Widening the *shared*
detector over WP4.4-e's twelve classes was declined as scope expansion.

### Not weakened, not renamed, not reordered

`RETAINED_SNIPPETS`; `test_partially_reachable_rules_kept_their_dead_branch` (including
the `.input-frame` = 9 / `.tbl-toolbar` = 1 occurrence pins);
`test_dark_theme_table_tokens_have_a_live_definition`;
`test_body_dark_mode_block_stays_deleted`; `test_layout_css_declares_no_cascade_layer`;
`test_orphaned_keyframes_went_with_their_only_consumer`;
`test_deleted_classes_are_not_resurrected_by_a_sibling_surface`; and the **two**
separator-contrast tests. `test_retained_rules_are_still_present` keeps its
`RETAINED_SNIPPETS` half intact; only its `DEFERRED_HELPER_COUNTS` half is removed, and it
is removed **into** C1–C5.

`tests/test_css_cascade_contracts.py` and `tests/test_visual_selector_contracts.py` are
**run always, edited never**.

### Red paths — 12 / 12 proven

Every contract this packet adds or changes was **executed** in its failing state, then the
tree restored and re-confirmed green.

| Violation | Contract | Result |
|---|---|---|
| re-add `.tbl-show-md { display: none; }` | C1 | RED |
| add only the `max-width: 820px` override, no base rule | C2 | RED |
| **restore all nine** | **C2** | **GREEN** |
| **restore all nine** | **C1** | **RED** |
| restore all nine minus one member | C2 | RED |
| `class="tbl-hide-lg"` in a template | C3 | RED |
| `classList.add('tbl-show-sm')` in a module | C3 | RED |
| `className = 'tbl-show-' + size` | C3 | RED |

**The three C3 rows exercise three application *shapes*, not three detector branches.** C3
is one substring scan; all three are red for the same reason, and that is the design — a
single mechanism that no application form can slip past. They are listed separately
because each is a shape a real change could take, and each was executed.
| `.tbl-show-sm {}` in `components.css` | C4 | RED |
| leave `@media (min-width: 1201px) { }` behind | C5 | RED |
| merged restoration collapsing the three bands into one `@media` (sums to 3 base / 6 nested) | C2 | RED |
| drop the print rule's live `.tbl-controls` branch | `test_retained_rules_are_still_present` | RED |

### What `code-reviewer` changed after the first encoding

Three defects in this packet's own contracts, found at the diff-time gate and fixed
before the branch was pushed. Recorded because the packet's subject is a contract whose
stated reason was false.

| Defect | Effect | Fix |
|---|---|---|
| **C2 counted class-head *incidences*, not shape.** A restoration merging all six classes into two selector lists inside **one** `@media` still sums to 3 base / 6 nested. | It passed — while collapsing the three breakpoint bands into one, which is precisely what the contract exists to prevent. Per-class counting alone did **not** fix it either: per-class counts cannot see *which* query a rule is in. | `_rule_heads` now carries the enclosing at-rule preludes rather than a depth integer. C2 asserts the shape per class **and** requires the sm/md/lg overrides to sit under three **distinct** preludes. The merged-collapse case is the twelfth red path. |
| **`_rule_heads` clamped on unbalanced braces** (`depth = max(0, depth - 1)`). | One surplus `}` would silently rebase every later head one level shallower, flipping the classification C2 is built from — a false green. | Raises on a stray `}` and asserts the stack is empty at the end, matching the sibling walker in `test_css_wp4_4_components_contracts.py:99`. |
| **C4 globbed `static/css/*.css` only.** | `static/vendor/fontawesome/css/all.min.css` is a real loaded stylesheet, and §3b claims it was scanned. The one-time census covered it; the standing gate did not. | Recursive walk of `static/**`, with `layout.css` excluded by **resolved path** rather than bare filename, so a future `vendor/**/layout.css` cannot slip through on its name. |

C3 also gained two narrow exemptions — comments and `static/js/**/__tests__/` — because a
note beside `table-responsiveness.js:112` explaining why the family went is a legitimate
mention that applies nothing, and the bare-stem scan would otherwise have fired on it.
All three C3 red paths still go red.

**The two-sided C2 proof is the one that matters.** Rows 3 and 4 are the same tree: with
all nine restored, C2 is **green** while C1 is **red**. Without that pair, every state
that reds C2 also reds C1, C2 would be subsumed, and its positive branch would never have
been exercised — a green-looking guarantee that could hide an `@media`-nesting mis-parse.

Red-path edits under `templates/**` and `static/js/**` were transient, reverted
immediately from a byte snapshot, and the files verified byte-identical afterwards.
Harness: `artifacts/tblhelpers/redpath.py`.

**A defect in the first red-path harness, recorded because it produced a wrong answer.**
It restored files with `git checkout --`, which restores from the index — and this
packet's deletion is *uncommitted*, so the restore silently reverted the deletion
mid-run. The family then existed twice in the file and C2's "green on a restored family"
proof failed for a reason that had nothing to do with C2. Fixed by restoring from a byte
snapshot taken at start, which is the only correct form while the change is uncommitted.
The failure was visible because the harness verifies byte-identity after every step.

---

## 7. Post-deletion measurement

### (e) The flip — PASS, all nine

For every context in which a rule both owned `display` and was distinguished from its
control before, the after-run must show **no `layout.css` owner** and the host's computed
`display` must **equal its control's**.

| Rule | flipped / expected | residue |
|---|---|---|
| `base-show-sm` | **594 / 594** | clean |
| `base-show-md` | **528 / 528** | clean |
| `base-show-lg` | **594 / 594** | clean |
| `sm-hide` | **264 / 264** | clean |
| **`sm-show`** | **264 / 264** | clean |
| `md-hide` | **330 / 330** | clean |
| **`md-show`** | **330 / 330** | clean |
| `lg-hide` | **264 / 264** | clean |
| **`lg-show`** | **264 / 264** | clean |

After deletion the test host's computed `display` is **identical to its control's** in
every context — `inline` on `<span>`, `list-item` on `<li>`, `table-cell` on `<td>`. The
classes select nothing and style nothing.

**The known-live controls survived the deletion: 1,716 / 1,716 still `layout.css`-owned.**
That matters more than it looks: `.tbl-controls` and `.tbl-view-mode-toggle` are
simultaneously the oracle's known-live controls *and* rules this packet retains, so a
deletion that had over-reached would have destroyed its own measurement apparatus and the
flip result would have been unreadable.

### (f-after) Controls — PASS

| Control | After-run |
|---|---|
| Same-CSS control (M5) — `after1` vs `after2`, identical CSS | **0 differing / 30,316** |
| Sentinel took effect / reverted cleanly | **8,580 / 8,580** · **8,580 / 8,580** |
| Known-live | **1,716 / 1,716** |
| Known-dead | **858 / 858** |
| Control-baseline | **858 / 858** |
| Census, all six candidates | **0** in all 286 contexts |
| Positive census control | `.tbl-wrap` 338, `.tbl` 338, `.tbl-controls` 26, `.tbl-view-mode-toggle` 26 |

### (g) Rest-state differential — PASS

Back-to-back pair, 22 route × theme contexts, both halves captured on an isolated port
with nothing in between (see §9b for the two invalid attempts that preceded it).

| Oracle | Differing | Records | Ledgered blind spot |
|---|---:|---:|---:|
| paint | **0** | 340,880 | 2 |
| motion | **0** | 153,396 | 0 |
| motionReduced | **0** | 153,396 | 0 |
| **declaration owner** | **0** | 2,640 | 0 |

**Outside the ledgered blind spot the differential is zero on every oracle.**

The two blind-spot records are one element in each theme —
`html/body[1]/main[1]/div[0]/div[0]/section[1]/div[1]/div[0]`, property `box-shadow`,
differing in the **blur radius at the fourth significant decimal**
(58.7186 vs 58.719 px dark; 58.8783 vs 58.8774 px light). That is an animating glow
captured at a slightly different phase.

Three independent reasons it is not attributable to this deletion, and they are the same
three WP4.4-e recorded for the same element:

1. The path is in the harness's own `uncertifiablePaths` — one of the eight animating
   Welcome elements the WP4.4-a blind-spot register names. **N8 forbids classifying a
   declaration affecting them from this harness**, and none was.
2. **Each run's own same-CSS control reproduces it on identical CSS**: the before-run
   reported `uncertifiableDifferingRecords: 1` and the after-run `2`, while both reported
   **0** ordinary differing records across all 22 contexts and `allSelfChecksPass: true`.
   A difference that appears when nothing changed is not evidence about a change.
3. `layout.css` never styled that element — the **declaration-owner differential is 0
   across all 2,640 records**, so no declaration changed hands anywhere on any route.

`scripts/css_audit/runtime_probe.mjs` was used **unmodified** for both halves in the
sense that matters — see §9b for why a byte-identical copy differing only in a port
constant had to drive it, and what that copy changes.

---

## 8. Gates

| Gate | Before | After |
|---|---|---|
| `tests/test_css_wp4_4_layout_contracts.py` | 15 passed | **20 passed** (+5: C1–C5) |
| Red-path proofs | — | **12 / 12**, tree byte-identical after each |
| Full `pytest tests/` | **2,523 passed / 2 skipped** (447.96s) | §8a — one known blocker |
| Seven-surface Stylelint | **2,759** | **2,759 (+0)**, no category increased, 0 parse errors |
| `layout.css` Stylelint | 92 | **92 (+0)** |
| Windows visual (`visual.spec.ts` + `visual-baseline-thumbnails.spec.ts`) | **84 / 84 on three consecutive runs**, 86 images | §8b |

**Stylelint moved by zero, and that is reported as zero.** None of the nine deleted
declarations triggers a rule in this configuration — they are plain `display: none` /
`display: block` with no literal colour, no `!important` and no specificity cost. The same
was true of WP4.3j-b-dead, and the same conclusion applies: the win is 47 lines that could
never render, not a lint reduction. V3 (no re-weighting) and V4 (no duplication increase)
hold exactly: `declaration-no-important` 1,219 → 1,219, `selector-max-id` 115 → 115,
`selector-max-specificity` 101 → 101, `no-duplicate-selectors` 21 → 21,
`declaration-block-no-duplicate-properties` 1 → 1.

### 8a. A P3-a0 contract that fires locally but does not gate CI

While the deletion was uncommitted,
`tests/test_css_theme_dark_p3_audit_contracts.py::test_this_packet_wrote_no_production_css`
failed on this branch:

```
AssertionError: P3-a0 writes no production CSS, but git reports changes under
static/css: ['M static/css/layout.css']
```

**This packet first recorded that as a merge blocker. That was wrong, and the
correction is kept here rather than quietly dropped.** `code-reviewer` pointed out
that `scripts/css_audit/p3_ceiling.py:199` runs `git status --porcelain -- static/css`,
which compares HEAD / index / working tree — so it reports nothing once a change is
**committed**. `Run Tests` (`ci.yml:504-514`) runs on a clean `actions/checkout@v7`
with no CSS build step, so the working tree there is always clean.

**Verified, not reasoned:** with this packet's change committed and
`git status --porcelain` empty, the file is **37 passed**. CI is unaffected and the
merge is not gated by it.

What the contract actually catches is an *uncommitted* `static/css` edit — local
friction for any CSS packet mid-flight, nothing more. **The repair this document
originally proposed — diffing `static/css/**` at `cd93480` against its parent — would
have made it strictly weaker**, since it would stop catching the uncommitted edit that
is the only thing it catches today, in exchange for nothing. That recommendation is
withdrawn.

The residual observation still worth recording is narrow: the docstring justifies
working-tree scoping by *"a base-SHA pin … would red the moment P3-c makes its
authorized cut"*, and **the same commit that added the contract terminated P3 at a0**
(`cd93480`, PR #280), so `P3-c` will never exist. The stated reason is obsolete; the
behaviour it produced is nonetheless correct and should be left alone.

### 8b. The Windows visual gate — and why the committed baselines could not be used

See §10. `e2e/__screenshots__/win32` is stale **and incomplete** on `main` at `ac2923b`
(66 baselines against linux's 68), and Playwright *writes* an absent snapshot even without
`--update-snapshots`, so a compare against the committed tree is not a read-only gate. The
differential therefore runs through a scratch config resolving snapshots under gitignored
`artifacts/`, inheriting every capture-affecting setting unchanged.

Pre-change: **84 / 84 on three consecutive runs** (one generate + two compare), 86 images,
`git status --porcelain e2e/__screenshots__` empty after each. **The pre-declared unstable
partition on this host is therefore empty**, which raises rather than lowers the bar: no
capture is excused in advance, so any post-change red is signal.

This says nothing about the Linux runner. On `main` at `ac2923b`, three back-to-back
`visual-linux` compare runs at one SHA produced 84-passed / (2 failed + 1 flaky) /
(1 flaky + 83 passed) — one run in three meets the bar. That gate is a coin flip
independently of this packet, PR #296 is investigating it, and a single green compare
there proves nothing.

---

## 9. Three discarded measurement runs

A packet whose subject is a mis-measurement has no standing to hide one of its own. All
three were caught by controls or by arithmetic, none by reading the verdict.

### 9a. A contaminated after-run — concurrency with a file-mutating harness

The first after-run executed concurrently with the red-path harness, which deliberately
mutates `layout.css` — and at one point reverted it to `HEAD` — while the oracle was
reading that same file over HTTP. Its records describe a mixture of tree states.

Quarantined at `artifacts/tblhelpers/after1_CONTAMINATED_DISCARDED/` rather than deleted.
The after-runs were re-executed serially against a tree verified stable at `3e13542e…`,
with the server confirmed to be serving the post-deletion file (0 occurrences of
`tbl-show`/`tbl-hide`, 3 of `tbl-controls`). This is `verification.md`'s parallelism rule
— *"CSS packets that touch the same bundle run serially"* — violated and caught.

### 9b. A rest-state pair that measured ANOTHER WORKTREE

The first `rest_before` / `rest_after` pair reported 5,316 paint differences. Every one was
of the form `value -> None` — a path present before and absent after, i.e. a **DOM-shape**
change, never a computed value that changed — and they were confined to four
database-driven routes whose element counts had moved: `backup` 229 → 351,
`user-profile` 1,487 → 1,502, `fatigue` 134 → 150, `body-composition` 210 → 213.

**Root cause: `scripts/css_audit/runtime_probe.mjs` hard-codes port 5000, and a
concurrent worktree owned it.** `Hypertrophy-Toolbox-v3-pyright-vp` was serving `app.py`
on 5000 (PID 8560, started 21:41). The probe's own `app.py` could not bind, its
`waitForServer()` connected to the foreign server instead, and the capture measured a
different checkout with a different database.

This is precisely the hazard `.claude/rules/verification.md` names under Parallelism and
that Plan v2 step 1 pre-declared — encountered live rather than hypothetically.

**Remedy, without touching the committed harness.** `scripts/css_audit/` is packet-`a`-owned
(A11) and was **not modified**. A copy at `artifacts/tblhelpers/runtime_probe_5178.mjs`
differs from it in **exactly three lines**, all the same constant — `BASE_URL`, the TCP
readiness probe's port, and an added `HT_PORT` in the spawned server's environment. The
pair was then re-run back-to-back on the isolated port, which is also the only form in
which the two captures are same-data. `artifacts/tblhelpers/pw-scratch.config.ts` gained
the same `PW_SCRATCH_PORT` treatment for the same reason.

### 9c. A restore that reverted the packet's own deletion, and a vacuous pass

Two smaller defects, both in this packet's own scaffolding:

- The first red-path harness restored files with `git checkout --`, which restores from the
  index — and this deletion is **uncommitted**, so it silently reverted the deletion
  mid-run. The family then existed twice and C2's "green on a restored family" proof failed
  for a reason unrelated to C2. Fixed by restoring from a byte snapshot taken at start,
  the only correct form while a change is uncommitted. It was visible because the harness
  verifies byte-identity after every step.
- The rest-state differ printed **PASS after comparing 0 contexts**. That is the vacuous
  success the council's DR-1(h) exists to forbid, reproduced in the tooling rather than in
  the criterion. The differ now exits non-zero on zero contexts or any zero-record oracle.
- `git show HEAD:static/css/layout.css` emits the blob as stored — **LF** — while the
  working tree is **CRLF** under `core.autocrlf`. Restoring the blob verbatim would have
  measured a line-ending change rather than a CSS change. The harness re-applies the
  checkout conversion and asserts the resulting sha256 before running.

---

## 10. Deferrals, follow-ups and residuals

| # | Item | Disposition |
|---|---|---|
| **D-1** | Four documents keep the refuted "inherently blind" rationale and are **not** written by this packet: `CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md:190`, `ACTIVE_DEVELOPMENT.md:275`, `MASTER_HANDOVER.md:1781`, `REFACTOR_PLAN.md:1412` | Knowingly deferred. Named by path and line; this document is the supersession pointer. P7 is scoped to the files this packet writes so the invariant can actually pass rather than be ticked falsely. |
| **D-2** | `MASTER_HANDOVER.md:1779` and `ACTIVE_DEVELOPMENT.md:274–279` carry a **live operating directive** — *"Deferred by `e`, owner-gated, do not act"* / *"Do not erode it rule by rule"* — which this deletion makes obsolete | Deferred; **owner decided at Gate 1: a separate docs packet.** Shared status documents are off-limits to this packet, and `WORKSTREAM_OWNERSHIP.md:29–33` classes `MASTER_HANDOVER.md` as a never-claimed coordinated path. |
| **FU-1** | Whether `_E_LAYOUT_` should gain a `superseded-by` pointer | Deferred. Editing a closed packet's historical record to match a later finding is the wrong repair. |
| **FU-2** | **Live `.d-none` defect in the Distribute workflow** — see below | **Owner decided at Gate 1: schedule as its own packet.** Not absorbed. |
| **R1** | Same-CSS control denominator decomposition | **Published** in §4. |

### FU-2 — `.d-none` does nothing in this application

Found by `product-risk-reviewer` at council while checking an unrelated claim, and
runtime-verified in this worktree **before any change**, at 1440×900 on `/volume_splitter`:

| Element | Computed `display` | Rect |
|---|---|---|
| `.results-section d-none` | **`block`** | 461 × 144, visible |
| `.ai-suggestions-section d-none` | **`block`** | 461 × 70, visible |
| `#error-message-container d-none` | `none` | 0 × 0 — hidden only by its own inline `style="display: none !important;"` at `base.html:271` |

`[...document.styleSheets]` contains **no** rule whose `selectorText === '.d-none'`.

**Root cause is structural:** `scss/custom-bootstrap.scss:34` imports
`bootstrap/scss/utilities` (the utility *map*) but never `bootstrap/scss/utilities/api`
(the partial that *emits* the classes), so the local `bootstrap.custom.min.css` ships
**zero** `.d-*` utilities and no `/build-css` run can reintroduce them. The only local
definition is the ID-scoped `#error-message-container.d-none` at `a11y.css:565`.

**User impact:** on `/volume_splitter`, before any split is calculated, an empty bordered
"Distribution" card containing an empty table plus live **Export Volume Plan** and
**Save & Activate** buttons, and an empty "AI Suggestions" card.

**Why no gate sees it:** `e2e/volume-splitter.spec.ts:148` asserts
`toHaveClass(/d-none/)` — class-token presence, never visibility — and
`tests/test_css_cascade_contracts.py:494–495` pins the literal markup as a hook that must
stay intact. Both are green while the class does nothing.

Not folded in: the fix needs `scss/**`, `templates/**` or `static/js/**`, all outside this
packet's write set, and `test_css_cascade_contracts.py` is run-always/edit-never here.

### A second operational finding — running the visual gate on Windows is not read-only

`e2e/__screenshots__/win32` holds, **at `ac2923b`**, **66** `visual.spec.ts` baselines
against linux's **68**: PR #281 regenerated only the linux half of the segmented `user-profile-mobile`
captures, and `docs/visual_determinism/PLANNING.md` §5/§7 tracks the Windows half as an
open owner-local follow-up.

Playwright **writes** an absent snapshot even without `--update-snapshots`. One compare
run against the committed tree left **four untracked PNGs** —
`user-profile-mobile-{dark,light}-segment-{1,2}.png`. They were **moved** (not deleted) to
`artifacts/tblhelpers/stray_win32_segments/` and the tree verified clean.

**Anyone running this gate on Windows must check `git status --porcelain e2e/__screenshots__`
afterwards**, or an unreviewed baseline addition is staged silently. This packet's visual
differential therefore uses a scratch config resolving snapshots under gitignored
`artifacts/` — the method `visual_determinism/PLANNING.md` §6 records as safe.

---

## 11. Reproducing this

```bash
# static inventory (DR-1(a))
bash artifacts/tblhelpers/static_inventory.sh

# probe server on an isolated port
env HT_PORT=5177 FLASK_DEBUG=0 FLASK_USE_RELOADER=0 .venv/Scripts/python.exe app.py

# oracle: before x2 (the second run IS the same-CSS control)
node artifacts/tblhelpers/tbl_oracle.mjs --out artifacts/tblhelpers/before1 --phase before --port 5177
node artifacts/tblhelpers/tbl_oracle.mjs --out artifacts/tblhelpers/before2 --phase before --port 5177
node artifacts/tblhelpers/summarize.mjs artifacts/tblhelpers/before1
node artifacts/tblhelpers/compare.mjs --same-css artifacts/tblhelpers/before1 artifacts/tblhelpers/before2

# rest-state differential, committed harness, unmodified (A11)
node scripts/css_audit/runtime_probe.mjs --out artifacts/tblhelpers/rest_before

#   ... apply the deletion ...
.venv/Scripts/python.exe artifacts/tblhelpers/apply_deletion.py

# oracle: after x2, and the flip check
node artifacts/tblhelpers/tbl_oracle.mjs --out artifacts/tblhelpers/after1 --phase after --port 5177
node artifacts/tblhelpers/tbl_oracle.mjs --out artifacts/tblhelpers/after2 --phase after --port 5177
node artifacts/tblhelpers/compare.mjs --flip artifacts/tblhelpers/before1 artifacts/tblhelpers/after1
node scripts/css_audit/runtime_probe.mjs --out artifacts/tblhelpers/rest_after

# red paths
.venv/Scripts/python.exe artifacts/tblhelpers/redpath.py

# visual differential, scratch snapshot path under gitignored artifacts/
npx playwright test -c artifacts/tblhelpers/pw-scratch.config.ts --project=chromium \
  e2e/visual.spec.ts e2e/visual-baseline-thumbnails.spec.ts

# seven-surface stylelint
node scripts/css_audit/stylelint_surfaces.mjs artifacts/tblhelpers/stylelint_after.json
```

Analysis scripts live under the gitignored `artifacts/` tree. `scripts/css_audit/` stays
packet-`a`-owned and was **not modified** (A11); `runtime_probe.mjs` is used unchanged.
