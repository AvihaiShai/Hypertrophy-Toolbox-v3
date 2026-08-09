# Plan Review — `.tbl-show-*` / `.tbl-hide-*` breakpoint-helper family: certify-and-delete or close as a durable no-op

*Artifact shell from [`docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md`](../ai_workflow/PLAN_REVIEW_TEMPLATE.md). Planning size is **Large** — a shared-surface `static/css/**` change under [QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) — so Gate 0 and Gate 1 both apply.*

**Worktree**: `D:/development/Hypertrophy-Toolbox-v3-tblhelpers` · branch `wt/css-tbl-helpers` · based on `origin/main` @ `ac2923b`.
The main checkout at `D:/development/Hypertrophy-Toolbox-v3-main` is read-only for this packet and is never touched.

**Document state — COMPLETE.** Council run, Gate 1 approved 2026-08-04, implementation finished; the outcome is recorded in the Sign-off section and in [`EVIDENCE.md`](EVIDENCE.md). All three reviewer outputs are pasted verbatim; 26 findings carry dispositions; Agent provenance is stamped with the IDs the manager supplied; Plan v2 folds in the executed evidence run. Section 0 and Plan v1 are otherwise unaltered — every correction a finding forced is marked inline with `⟢`, leaving the superseded claim standing beside it, because a packet whose deliverable is a true record may not quietly rewrite its own history.

---

## Section 0 — Requirements Brief

**Raw request** (verbatim)

> Work ONLY in the worktree `D:/development/Hypertrophy-Toolbox-v3-tblhelpers` (branch `wt/css-tbl-helpers`, based on `origin/main` @ `ac2923b`). Never touch the main checkout at `D:/development/Hypertrophy-Toolbox-v3-main`.
>
> Write **Section 0 and Plan v1 only** into a NEW file `docs/css_table_helpers_cleanup/PLANNING.md` (the directory already exists). Use the shell of `docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md`. Write no other file. Do NOT write the response matrix or Plan v2 — a later message will ask for those.
>
> ## The packet
>
> Re-audit the nine deferred `.tbl-show-*` / `.tbl-hide-*` breakpoint-helper rules in `static/css/layout.css` (source lines 1594–1634) and either certify and delete them **atomically** or close the packet with durable evidence proving why the family must remain. **Partial deletion is forbidden.**
>
> The nine rules are exactly:
> - base `.tbl-show-sm` (1594–1596), `.tbl-show-md` (1598–1600), `.tbl-show-lg` (1602–1604) → each `display: none`
> - `@media (max-width: 820px)`: `.tbl-hide-sm` (1607–1609) `display:none`; `.tbl-show-sm` (1611–1613) `display:block`
> - `@media (min-width: 821px) and (max-width: 1200px)`: `.tbl-hide-md` (1617–1619) `display:none`; `.tbl-show-md` (1621–1623) `display:block`
> - `@media (min-width: 1201px)`: `.tbl-hide-lg` (1627–1629) `display:none`; `.tbl-show-lg` (1631–1633) `display:block`
>
> ## Owner decisions ALREADY SETTLED — record these as binding, do not re-open
>
> - **Gate 0 is APPROVED by the owner's instruction**, before any council work. Mark all three Section 0 sign-off checkboxes as owner-approved-in-prompt and say so explicitly.
> - The family is indivisible: delete all nine or none.
> - A rigorous no-op / retention outcome **completes** the packet. It is not a failure.
> - Do NOT trim selector branches, alter breakpoint values, rename utilities, redesign responsive behaviour, or replace the family with another utility system.
> - Do NOT edit `components.css`, table JavaScript, templates, visual snapshots, tolerances, masks, retries, Playwright configuration, visual helpers, workflow files, baseline JSON, or unrelated layout rules — unless Plan v1/v2 identifies a strictly necessary contract-only change, which then needs owner approval at Gate 1.
> - Do NOT weaken the existing exact-occurrence contract merely to make deletion pass. It may only be replaced by *stronger* structural post-deletion and reachability contracts.
> - No P3 (`theme-dark.css`) work is authorized.
> - Preserve rendering, table behaviour, accessibility, calculations, APIs, schemas and database state.
>
> ## Inherited evidence to be re-proved, not trusted
>
> `docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md` §4a records that WP4.4-e deferred these nine because: natural census 0; six of nine visible to its synthetic oracle; three (`display: block` media overrides) were considered **indistinguishable because `block` is a bare `div`'s initial value** — described as "an inherent limit, not a fixable probe defect". Partial deletion was rejected because it would leave `@media` overrides without base rules. The family is pinned by exact occurrence counts in `tests/test_css_wp4_4_layout_contracts.py` (`DEFERRED_HELPER_COUNTS`, asserted by `test_retained_rules_are_still_present`).
>
> **That "inherent limit" has now been measured and REFUTED.** A feasibility spike already ran in this worktree (artifacts are gitignored under `artifacts/tblhelpers/`). Record these as measured facts in Plan v1:
>
> - The limit was a property of the **probe host** WP4.4-e chose (a bare `div`, initial `display: block`), not of the rules.
> - A new oracle uses three hosts whose UA initial `display` is not `block`: `<span>` → `inline`, `<li>` → `list-item`, `<td>` → `table-cell`. No author CSS is injected to manufacture a baseline.
> - Spike result over 2 routes × 2 themes × 13 widths (52 contexts): **all nine rules distinguished from their control in 100% of the contexts where each rule owns `display`** — `base-show-sm` 108/108, `base-show-md` 96/96, `base-show-lg` 108/108, `sm-hide` 48/48, `sm-show` 48/48, `md-hide` 60/60, `md-show` 60/60, `lg-hide` 48/48, `lg-show` 48/48. Declaration owner resolved through CDP to the correct `layout.css` source range in every one of those contexts.
> - Controls all passed: sentinel took effect 1560/1560 and reverted cleanly 1560/1560 (transitions and animations suppressed before apply, read AND remove); known-live 312/312; known-dead 156/156; no foreign stylesheet defines a candidate class; the single unreadable cross-origin sheet is Google Fonts, verified out-of-band to contain 4 `@font-face` rules and zero class selectors.
> - A first version of the oracle used `.tbl-wrap` as the known-live control and it read **0/78** — because `layout.css` styles `.tbl-wrap` but never with `display`. That is the WP4.4-e "hand-written property list" defect reappearing on the control side. It was fixed by moving the known-live control to `.tbl-controls` (`display: flex`, layout.css:1423) and `.tbl-view-mode-toggle` (`display: inline-flex`, layout.css:1451), both created at runtime by `static/js/table-responsiveness.js` (:112 and :239) and both retained by this packet. **Record this defect and its fix in the plan** — the packet's credibility rests on the controls.
> - Static census is 0: the only definition site anywhere in the repository is `layout.css`; no template, no JS, no other stylesheet, no dynamic class construction (`grep` for `tbl-show`/`tbl-hide` and for string-built class names found nothing), and there is no `build/` or `dist/` directory in the tree.
> - Natural-reachability control: on the table routes `.tbl-wrap`, `.tbl`, `.tbl-controls` and `.tbl-view-mode-toggle` each census 26/26, proving the census reaches pages where `layout.css` is doing work while the six candidate classes stay at 0.
>
> ## Proof obligations the plan must commit to
>
> 1. Inventory all natural template/JS/class-application paths; exclude generated `build/`/`dist/` copies as evidence.
> 2. Full-selector census before any injection.
> 3. Widths immediately below, at and above 820/821 and 1200/1201, plus representative interior widths. Rule applicability must be driven by **measured `matchMedia`**, never by nominal viewport width.
> 4. Measure every rule only where its media condition applies — and note that the three *base* rules are superseded inside their own class's media block, so each is observable only outside it.
> 5. Derive observed properties from the rule's own declarations.
> 6. A synthetic control that fails the selector by exactly one compound.
> 7. Each rule's positive before-state effect AND its post-deletion flip.
> 8. Source identity proven **structurally** (CDP styleSheetId + source range + media text), never by substring.
> 9. Transition-safe sentinel handling even though `display` is not currently animated.
> 10. Same-CSS controls run before and after.
> 11. Preserve the live print `.tbl-controls, .tbl-toolbar` rule and all unrelated `.input-frame`/`.action-frame` contracts in `tests/test_css_wp4_4_layout_contracts.py`.
> 12. Red paths proven for every new or changed contract.
> 13. **If any one of the nine cannot be fully certified, retain all nine.**
>
> ## Conservative fallbacks to state explicitly in the plan
>
> evidence uncertainty → retain; partial proof → retain the whole family; visual noise without candidate-specific computed differences → record the noise, never rebaseline; scope-expanding recommendation → defer with rationale.
>
> ## Planning size and gates
>
> This is a **shared-surface `static/css/**` change**, which `docs/ai_workflow/QUALITY_GATE.md` classifies as **Large** at plan stage. Read that file's `CSS (static bundles)` row and derive the gate list from it, including: full pytest; Chromium `smoke-navigation`, `nav-dropdown`, `accessibility`, `dark-mode`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening`; the full seeded `visual.spec.ts` matrix; seven-surface Stylelint via `node scripts/css_audit/stylelint_surfaces.mjs` with no category increase; and the Linux `visual-linux` deep gate.
>
> ## The external visual blocker — state it accurately, do not plan around it
>
> PR #296 (`fix/visual-table-raster-stability`) is OPEN, draft, investigation-only and explicitly must-not-merge. Its files must not be touched and its experimental switches must not be used. Measured on `main` @ `ac2923b`: three back-to-back `visual-linux` compare runs at one SHA gave 84-passed / (2 failed + 1 flaky) / (1 flaky + 83 passed) — one run in three meets the bar, so a single green compare proves nothing. Instability is confined to the wide desktop captures (`workout-plan-desktop-{dark,light}`, `plan-desktop-{dark,light}-advanced`). Separately, `e2e/__screenshots__/win32` is already stale on `main` independently of this packet — PR #296 measured `plan-desktop-light-advanced` alone at 541,849 px (29%) against its committed baseline on a pristine tree.
>
> Consequences the plan must adopt: the pixel matrix **cannot** carry candidate-specific evidence here; it is run as a gate and reported honestly. The verdict rests on computed-style and declaration-owner measurement. The Linux deep gate is interpreted against the **current accepted baselines**, not the stale `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` ledger (whose `sourceCommit` `46e340e` predates PR #281's owner-accepted regeneration — `QUALITY_GATE.md` records this caveat). If global visual nondeterminism remains, the draft PR is left accurately blocked on that external merge gate. No snapshot, tolerance, mask, retry or config may be changed.
>
> ## Required reading before you write
>
> `CLAUDE.md`; `docs/ai_workflow/QUALITY_GATE.md`; `docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md`; `.claude/rules/verification.md`; `.claude/rules/frontend.md`; `.claude/rules/testing.md`; `docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md`; `tests/test_css_wp4_4_layout_contracts.py`; `static/css/layout.css` lines 1548–1725; and `docs/css_phase4_wp4_4/PLANNING.md` §2b (method rules M1–M12) and §2 (standing constraints G1–G11) — note that `.claude/rules/verification.md` says the WP4.4 arc's arc-specific constraints retired when that arc closed, while the durable method in `verification.md` still binds. Say which rules you are treating as binding and why.
>
> ## Plan v1 must contain
>
> - Both possible terminal outcomes, A (atomic nine-rule deletion with complete proof) and B (durable no-op audit naming exactly which member is uncertifiable and why), with the decision rule that selects between them stated **before** the evidence is complete.
> - The artifact table: `static/css/layout.css` (delete-or-no-op), `tests/test_css_wp4_4_layout_contracts.py` (replace `DEFERRED_HELPER_COUNTS` + `test_retained_rules_are_still_present`'s helper assertion with stronger absence + unreachable-use contracts on outcome A; strengthen-in-place on outcome B), `docs/css_table_helpers_cleanup/PLANNING.md`, and a new evidence document.
> - The exact shape of the replacement contracts for outcome A, and why each is *stronger* than the occurrence-count pin it replaces.
> - The sequence, effort (L), and the expected gates.
>
> Leave the Agent provenance table present but unstamped — the manager will supply IDs later. Report the artifact path and a concise summary when done.

**Problem**

`static/css/layout.css:1594–1634` carries nine breakpoint-helper rules that nothing in the application uses. WP4.4-e proved the *unreachability* case for them as strongly as for the 33 rules it deleted, then deferred all nine on a stated **measurement limit**: three of the nine declare `display: block`, and the packet's probe host was a bare `<div>` whose UA initial `display` is already `block`, so those three could not be distinguished from their control. WP4.4-e recorded that as "an inherent limit, not a fixable probe defect".

Two things are now wrong with the repository's state, and they are separable:

1. **The stylesheet carries nine rules that may be certifiably dead.** Whether they should go is genuinely open until measured.
2. **The record is false regardless of outcome 1.** `tests/test_css_wp4_4_layout_contracts.py:76–94` and `docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md` §4a both assert, as a durable justification, that no control element can distinguish those three rules. A feasibility spike in this worktree has refuted that: the limit belonged to the *host*, not to the rules, and three hosts whose UA initial `display` is not `block` (`<span>`, `<li>`, `<td>`) distinguish all nine. A contract whose stated reason is known to be untrue is a liability whichever way the deletion decision falls.

The packet's deliverable is therefore **a true record plus the strongest contract the evidence supports**, not a line-count reduction. Under-delivery on lines is explicitly not a failure mode here.

**Acceptance criteria**

1. Given the nine rules at `layout.css:1594–1634`, when the packet completes, then **either** all nine are deleted **or** all nine remain — never a subset — and the choice is justified by a decision rule that was written down before the evidence existed (DR-1, Plan v1).
2. Given a fresh oracle run in this worktree, when each of the nine rules is measured, then for every context in which `matchMedia` reports its media condition applies **and** the rule owns `display`, the rule is distinguished from a control that fails its selector by exactly one compound, and its declaration owner resolves structurally (CDP `styleSheetId` + source range + media text) to that rule's own source range in `layout.css`.
3. Given the oracle, when its controls are read, then known-live reads live, known-dead reads dead, every sentinel took effect and reverted cleanly, the control host's own computed `display` equals its UA initial value with no author `display` rule matching it, and the same-CSS control reports zero differing records — **before and after**. A failed control voids the entire run (`.claude/rules/verification.md`).
4. Given outcome A (deletion), when the after-run executes, then every one of the nine flips: no `layout.css` rule owns `display` on the synthetic host, and the host's computed `display` equals its control's.
5. Given outcome A, when `tests/test_css_wp4_4_layout_contracts.py` is inspected, then `DEFERRED_HELPER_COUNTS` and its assertion in `test_retained_rules_are_still_present` are replaced by structural-absence, all-or-nothing and unreachable-use contracts that are **strictly stronger** (each strength claim stated and defended in the evidence document), and every one is proven to go red under its own violation.
6. Given outcome B (retention), when the packet closes, then the exact-occurrence pin survives undiminished, is *added to* by the same all-or-nothing and unreachable-use contracts, the refuted "inherently blind" rationale in the file's comment is replaced by the measured facts, and the evidence document names **exactly which member(s)** could not be certified and on which criterion.
7. Given either outcome, when the gate list is run, then rendering, table behaviour, accessibility, calculations, APIs, schemas and database state are unchanged, and `git diff --name-only` shows zero paths under `e2e/__screenshots__/`, zero changes to `e2e/visual-helpers.ts`, `playwright.config.ts`, `static/css/components.css`, `static/js/**`, `templates/**`, and zero changes to any file owned by PR #296.
8. Given the known Windows/Linux visual nondeterminism, when the pixel matrices are reported, then they are reported as gates against the packet's own same-machine pre-change run, no pixel result is cited as candidate-specific evidence, and no snapshot, tolerance, mask, retry or configuration value is changed. If nondeterminism persists, the PR is left accurately blocked on that external gate.

**Calculation surface**

`none`.

- Functions changed: **none**. The packet's production surface is `static/css/layout.css` (deletion or no-op) and one pytest contract file. No Python or JavaScript in `utils/**`, `routes/**` or `static/js/**` is opened, so `calculate_effective_sets()`, `calculate_weekly_summary()`, `calculate_session_summary()`, the progression suggester and the fatigue calculators are untouched by construction.
- Worked example: not applicable — no input/output pair changes. The equivalent obligation for a CSS-deletion packet is the **computed-style differential**, whose worked before/after is specified in Plan v1 §"The oracle": for host `<span class="tbl-show-sm">` at a measured `matchMedia('(max-width: 820px)') === false` context, before `computed display = none`, owner = `layout.css` range 1594–1596; after `computed display = inline`, owner = none. That is the calculation-surface analogue and it is required for every one of the nine rules.
- Migration notes: the PR description states the outcome (A or B), the DR-1 verdict member by member, and links the evidence document. Test coverage moves in the same PR: the contract file gains the replacement or additive contracts, every one red-path-proven, and `docs/test_inventory/TEST_INVENTORY.{md,json}` is regenerated and committed because the test count changes (`.claude/rules/testing.md`; `Test Inventory Drift` is a required branch-protection context per `QUALITY_GATE.md`).
- CLAUDE.md's refactor invariant ("any change to core workflow behavior … requires migration notes and updated test coverage") is **not triggered** by a behavioural change here — it is honoured pre-emptively, because a display-utility deletion that turned out to be reachable would be exactly such a change, and the reachability contracts are what convert that risk into a pytest red.

**In scope**

- Re-audit of the nine rules at `static/css/layout.css:1594–1634` as one indivisible unit.
- A fresh three-host oracle, its controls, and both a before-run and an after-run, executed in this worktree only.
- Atomic deletion of all nine (outcome A) **or** a durable no-op closure (outcome B).
- Replacement or strengthening of the `DEFERRED_HELPER_COUNTS` pin in `tests/test_css_wp4_4_layout_contracts.py`, plus the module docstring/comment corrections that keep that file's stated reasoning true.
- A new evidence document under `docs/css_table_helpers_cleanup/`.
- The full Large-change gate list derived from `QUALITY_GATE.md`'s `CSS (static bundles)` shared-surface row.

**Out of scope / non-goals**

- Any partial deletion, in either direction (base rules only, or `@media` overrides only).
- Trimming selector branches, altering the 820/821/1200/1201 breakpoint values, renaming the utilities, redesigning responsive behaviour, or introducing a replacement utility system.
- `static/css/components.css`, `static/css/theme-dark.css` (no P3 work is authorized), any other bundle, `scss/**`, `static/js/**` (including `table-responsiveness.js`), `templates/**`.
- `e2e/__screenshots__/**`, `e2e/visual-helpers.ts`, `playwright.config.ts`, tolerances, masks, retries, `--update-snapshots` in any form.
- `docs/ai_workflow/**`, `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json`, `docs/CSS_PHASE4_WP4_4_A_BASELINE.json`, `docs/CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json`, and every other pinned baseline JSON.
- `tests/test_css_cascade_contracts.py` and `tests/test_visual_selector_contracts.py` — **run always, edit never** for this packet.
- Any file owned by PR #296 (`fix/visual-table-raster-stability`), and its experimental switches.
- The main checkout `D:/development/Hypertrophy-Toolbox-v3-main`.
- Editing the historical record in `docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md` (see Assumption A6).
- Committing the bespoke oracle into `scripts/css_audit/` (see Assumption A5).

**Assumptions made**

- ⚠️ **A1 — The feasibility spike's numbers are treated as facts about *feasibility*, not as the packet's certification.** The prompt records them as measured, and Plan v1 records them as measured; but they were produced by a spike whose artifacts are gitignored, so the packet re-runs the full before/after pair under its own base commit and publishes its own denominators. If the packet's own run disagrees with the spike, the packet's run governs and the disagreement is recorded, not smoothed over.
- ⚠️ **A2 — The spike's reported ratios are internally consistent and I have checked the arithmetic, not the measurement.** With 3 hosts × 52 contexts = 156 records per rule, the base-rule and media-rule denominators are exact complements: `base-show-sm` 108 + `sm-*` 48 = 156; `base-show-md` 96 + `md-*` 60 = 156; `base-show-lg` 108 + `lg-*` 48 = 156. That implies a width set split **4 / 5 / 4** across the three bands (13 widths), and `known-live 312 = 2 controls × 156`, `known-dead 156 = 1 × 156`. This is a coherence check on the reported numbers only. The packet must publish the full denominator derivation for every ratio it reports, including the `1560` sentinel figure, which I have not been able to derive unambiguously.
  > **⟢ CORRECTED at Plan v2** (architecture #5, test-strategist F12; the original claim above is left standing). The full evidence run has now executed and the decomposition is resolved. The real geometry is **11 routes × 2 themes × 13 widths = 286 contexts**, not 52; per context the probe mounts **3 hosts × 10 elements** (1 control + 6 candidate classes + 2 known-live + 1 known-dead) = **30 elements**. Therefore sentinel records = 286 × 30 = **8,580**, known-live = 286 × 3 × 2 = **1,716**, known-dead = 286 × 3 = **858**, per-rule universe = 286 × 3 = **858**. The spike's unexplained `1560` was **52 × 30**, not `156 × 10` — my guessed decomposition was wrong in structure while right in complementarity. The band complements still hold exactly: 594 + 264 = 528 + 330 = 594 + 264 = 858. One decomposition remains unpublished — the same-CSS control's **30,316** compared records over 286 contexts (106 per context) — and Plan v2 carries it as residual obligation **R1**.
- ⚠️ **A3 — Deleting the family removes a capability nothing currently supplies elsewhere.** `grep` for `d-none` across `static/css/**` finds only `#error-message-container.d-none` in `a11y.css:565`; the local `bootstrap.custom.min.css` contains no `d-none` token at all, so Bootstrap's responsive display utilities are **not** available from the local bundles (they would only appear via the CDN fallback on `templates/base.html:15`, which is an error path, not the normal one). Outcome A therefore removes the only responsive show/hide utility family in the local CSS. I judge this acceptable because census is 0 and the reachability contract converts any future adoption into a pytest red — a deliberate decision beats a silently-present, never-exercised utility — but it is a real product trade-off and the `product-risk-reviewer` should rule on it rather than inherit it.
  > **⟢ CORRECTED at Plan v2** (product-risk #1, #2, #3; the original claim above is left standing because this packet's whole point is that a superseded claim must remain visible next to its correction). The `product-risk-reviewer` ruled: **the premise is right, the conclusion is wrong, and the correction strengthens the case for outcome A.**
  > - **Premise — verified, and more durable than I stated.** `bootstrap.custom.min.css` contains **zero** `.d-` selectors, and the cause is structural: `scss/custom-bootstrap.scss:34` imports `bootstrap/scss/utilities` (the utility *map*) but never `bootstrap/scss/utilities/api`, the partial that emits utility classes. No `/build-css` run can reintroduce `.d-*` without an SCSS edit.
  > - **Conclusion — refuted.** The nine helpers are **not** the only responsive show/hide family. The live one sits ~300 lines above them in the same file: `.col--high` / `.col--med` / `.col--low` progressive column disclosure at `layout.css:1218–1306` (container queries at 1200/992px, media fallbacks at 1366/1200px, zoom-detection variants at 1440px+1.1dppx and 1200px+1.25dppx); row-card mode at `layout.css:1312+`; the print restore at `layout.css:1569–1575`; and the ResizeObserver view-mode toggle in `static/js/table-responsiveness.js`. It is applied in production by `static/js/modules/workout-plan-table.js:383+` and `templates/volume_splitter.html:94–97`. **Deleting the nine removes no capability.** The trade-off is stated as *"no responsive capability is lost"*, not *"acceptable loss"*.
  > - **The CDN clause is withdrawn.** Treating `cdn.jsdelivr.net` on `templates/base.html:15` as a degraded-but-present capability source is wrong in the wrong direction for a local-first app that may run offline. It was never load-bearing — Bootstrap defines no `.tbl-*` under any load path.
  > - **The grep that produced A3 walked past a live defect, recorded as a named follow-up and deliberately NOT absorbed** — see Plan v2 §"Named deferrals and follow-ups" **FU-2**.
- ⚠️ **A4 — This packet edits WP4.4-e's own contract file rather than adding a new one.** `tests/test_css_wp4_4_layout_contracts.py` is described in its docstring as packet-owned; WP4.4-e is closed and merged, and the family this packet audits is exactly what that file pins. Adding a parallel contract file would split one guarantee across two files and leave the refuted rationale standing in the first. The WP4.4 arc's N1 ("per-packet contract files, no consolidation") retired with the arc.
- ⚠️ **A5 — The bespoke oracle lives under the gitignored `artifacts/tblhelpers/`, not in `scripts/css_audit/`.** `.claude/rules/verification.md` says "reuse the committed harness"; `CLAUDE.md`'s repository-root policy and ADR-002 say generated output goes under `artifacts/`. The resolution taken is WP4.4-e's own precedent (its `_E_LAYOUT_` §9): reuse `scripts/css_audit/runtime_probe.mjs` **unchanged** for the rest-state differential, keep the bespoke breakpoint oracle in `artifacts/tblhelpers/`, and publish a byte-exact reproduction recipe in the evidence document. Committing the oracle is a scope expansion and is deferred with this rationale.
- ⚠️ **A6 — `docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md` is left byte-unchanged.** Its §4a and §10 become factually superseded under either outcome. It is a closed packet's historical record, and editing history to match a later finding is the wrong repair; the new evidence document states "supersedes `_E_LAYOUT_` §4a" explicitly and the contract file's docstring is updated to point at both. Adding a `superseded-by` pointer into `_E_LAYOUT_` is a scope-expanding recommendation and is deferred. (Checked: `_E_LAYOUT_` is referenced from `tests/test_css_wp4_4_layout_contracts.py:5` in a **docstring only** — no test asserts that path, so this is a documentation judgement, not a CI one.)
  > **⟢ EXTENDED at Plan v2** (architecture #10). A6's measurement is right and the artifact table's N7 citation contradicted it. N7 in `docs/LEFTOVERS_BY_PRIORITY.md:224–231` **over-counts**: only the two JSON baselines are genuinely asserted by pytest (`tests/test_css_cascade_contracts.py:161`, `tests/test_css_wp4_4_a_baseline_contracts.py:34`); the markdown evidence files are not. N7 is now cited only for the two JSON baselines.
- ⚠️ **A7 — "Preserve rendering" is verified by computed-style differential, not by pixels.** With census 0 no element on any page carries a candidate class, so *by construction* no pixel can change; a green pixel matrix is therefore consistent with deletion and also consistent with a broken oracle, and proves neither. Note precisely: `display` is **not** in the `prepareForScreenshot()` blind-spot register (`CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md` §8), so the register is not the reason the pixel matrix is uninformative here — census 0 plus the measured wide-desktop instability is.
- ⚠️ **A8 — Two routes and two themes are sufficient breadth.** The candidate classes are table utilities; the spike used 2 routes × 2 themes × 13 widths. Plan v1 names `/workout_plan` and `/workout_log` as those routes. The *census* half of the evidence must nonetheless be taken across the full rendered-route set (11 routes), because a class applied on a non-table page would still falsify unreachability. The council should confirm this split — narrow synthetic measurement, wide census.
  > **⟢ SUPERSEDED IN THE STRONGER DIRECTION at Plan v2.** The `product-risk-reviewer` endorsed the narrow-measurement / wide-census split as the correct call. The executed run then went **wider than planned**: the synthetic oracle ran on all **11 routes** × 2 themes × 13 widths = 286 contexts, not 2 routes × 2 themes × 13 widths = 52. A8's split is therefore moot — measurement and census now share the full rendered-route set. Plan v2 pins 11 routes so the executed geometry, not the planned one, is what the evidence document must reproduce.

**Open questions for the user**

`none` — all owner decisions listed in the raw request are settled and are recorded above as binding. Three items are flagged for the **council** rather than the owner (A3 product trade-off, A5 oracle-location precedent, A8 route breadth); anything the council escalates returns to the owner at Gate 1 with Plan v2.

One item is pre-declared as requiring owner approval **at Gate 1** if it materializes: if Plan v2 concludes that a strictly necessary contract-only change must touch a file outside the four-artifact table, it is presented at Gate 1 as a named exception and is not taken on packet authority.

### Section 0 sign-off — GATE 0

**Gate 0 is APPROVED by the owner's instruction in the raw request, before any council work.** All three boxes below are checked as *owner-approved-in-prompt*: the owner stated the decisions, the indivisibility rule, the no-op-completes-the-packet rule, the exclusions and the gate list directly, so there is nothing outstanding for the owner to confirm at this gate. No blocking question remains open.

- [x] User confirms the acceptance criteria match intent. — *owner-approved-in-prompt.* The acceptance criteria are derived only from the owner's own stated obligations (13 proof obligations, the four conservative fallbacks, the indivisibility rule, the preservation list); nothing was added.
- [x] User reviewed the assumptions and corrected or accepted each one. — *owner-approved-in-prompt.* A1, A2, A6 and A7 are restatements of constraints the owner supplied. A3, A4, A5 and A8 are the planner's judgements and are routed to the council for challenge; they do **not** hold up Gate 0, and any that the council overturns returns to the owner inside Plan v2 at Gate 1.
- [x] Blocking questions are answered. — *owner-approved-in-prompt.* The owner pre-answered the only decisions that could have blocked: delete-or-retain granularity, whether a no-op counts as completion, the treatment of the contract pin, and the treatment of the external visual blocker.

---

## Plan v1

**Goal**: Establish, by fresh measurement with validated controls, whether all nine `.tbl-show-*` / `.tbl-hide-*` rules in `layout.css` are certifiably unreachable and unobservable — then either delete all nine atomically or retain all nine — and in both cases leave the repository holding a **true** justification and a **stronger** contract than the occurrence-count pin whose stated reason has been refuted.

### Scope

- **In**
  - `static/css/layout.css:1594–1634` — the nine rules, their two enclosing comments, and the three `@media` shells, treated as one unit. **⟢ CORRECTED at Plan v2** (architecture #6): the range is wrong — `:1594` is `.tbl-show-sm {`, and the two comments sit at `:1589–1591` (banner) and `:1593`. The atomic unit is **`layout.css:1589–1634`**. The already-empty `LOADING STATE` banner at `:1584–1586` is **deliberately left**.
  - `tests/test_css_wp4_4_layout_contracts.py` — replace (outcome A) or strengthen in place (outcome B) the deferred-family pin; correct the module docstring and the family comment under both outcomes.
  - `docs/css_table_helpers_cleanup/PLANNING.md` — this artifact.
  - `docs/css_table_helpers_cleanup/EVIDENCE.md` — new.
  - A bespoke three-host breakpoint oracle plus its controls, under the gitignored `artifacts/tblhelpers/`.
  - The full Large / shared-surface gate list.
- **Out** — as Section 0 "Out of scope / non-goals", without exception. In particular: no partial deletion, no breakpoint-value change, no `components.css`, no JS, no templates, no snapshots/tolerances/masks/retries/config, no baseline JSON, no `theme-dark.css`, no PR #296 file or switch, no edit to `tests/test_css_cascade_contracts.py` or `tests/test_visual_selector_contracts.py`, no main-checkout access.

### Which rules bind, and why

The prompt asks this explicitly. `.claude/rules/verification.md` states that the WP4.4 arc's *arc-specific* constraints retired when the arc closed, while its durable method still binds.

| Source | Binding? | Why |
|---|---|---|
| `.claude/rules/verification.md` — oracle validation (known-live / known-dead / same-CSS control), converging evidence, `@media` capture under its own condition, sentinel/transition symmetry, "a probe that changes nothing proves nothing", adversarial control selection, reuse-the-committed-harness, Windows scripting hazards, one-Playwright-run-at-a-time | **Yes, in full** | It is the durable method file for exactly this claim shape ("this rule is dead"). Its `paths:` front matter matches `static/css/**/*.css`, so it loads for this packet automatically. |
| `docs/ai_workflow/QUALITY_GATE.md` — plan-stage routing + the `CSS (static bundles)` shared-surface row + its notes and Linux-ledger caveat | **Yes** | Canonical for both planning size and gates. It is what makes this packet Large. |
| `CLAUDE.md` — repository-root policy / ADR-002 (`artifacts/` for generated output), refactor invariant, module boundaries | **Yes** | Project-wide operating instructions. |
| `.claude/rules/frontend.md` — 18-bundle runtime cap; no new runtime CSS file | **Yes** | Constrains the shape of any remedy: a deletion cannot be "replaced" by a new stylesheet, which is independently forbidden by the owner. |
| `.claude/rules/testing.md` — regenerate and commit `docs/test_inventory/TEST_INVENTORY.{md,json}` whenever a test count moves | **Yes, and load-bearing** | This packet changes the test count under both outcomes. `Test Inventory Drift` is a required branch-protection context (`QUALITY_GATE.md` §"CI job naming"), so skipping it reds a required check. |
| WP4.4 §2b method rules **M1, M4, M5, M6, M6a, M8, M11, M12** | **Adopted voluntarily as method**, by name, for continuity of the evidence record | Each is the arc's phrasing of an obligation that `verification.md` states durably. Naming them keeps the evidence chain readable against `_E_LAYOUT_`. M11 (no `@media` declaration classified dead without a capture under its own condition) and M6a (transition-symmetric sentinels) are the two that most directly shape this oracle. |
| WP4.4 §2b **M2, M3, M7** (pixel-space differencing, element-scoped capture, the animated-logo *band*) | **Adopted as reporting discipline only** | They govern how a pixel result may be described. No pixel result is evidence in this packet (A7), so they constrain the gate report, not the verdict. |
| WP4.4 §2b **M9** (custom properties) | **Not applicable** | None of the nine declares a custom property. |
| WP4.4 §2b **M10** (JS-applied classes non-deletable unless proven under that state) | **Applicable and discharged by the reachability contract** | These classes are JS-*applicable* in principle. The discharge is that no code path applies them — proven statically (inventory) and dynamically (census before injection), and then contract-pinned. |
| WP4.4 §5 preservation invariants **V1, V2, V3, V4, V6** | **Adopted voluntarily** | V1 no unexplained visual difference; V2 no rebaseline; V3 no re-weighting (`!important`, `selector-max-id`, `selector-max-specificity` must not rise); V4 no duplication increase; V6 cascade correctness outranks line count. All are outcome-neutral and all are cheap to measure. |
| WP4.4 §5 **V5** (30% Phase-4 line target) | **Reported, never an acceptance criterion** | Phase 4's P3 was terminated at a0; the arc's own PR#13 ruling already says under-delivery never widens scope. The owner has independently ruled that a no-op completes this packet. |
| WP4.4 **G1–G11** and **N1, N3–N10** | **Retired with the arc; not inherited** | Per `verification.md`'s division of ownership. Where one of them protects something still live, that liveness is asserted by a green test, and *the test* is what binds — see the next row. |
| WP4.4 **N2 / G10** (`@layer` freeze) | **Binds — but via the test, not the arc** | `test_layout_css_declares_no_cascade_layer` is a currently-green contract in the very file this packet edits. It must stay green; the packet adds no `@layer`. |
| `tests/test_css_cascade_contracts.py`, `tests/test_visual_selector_contracts.py` | **Run always, edit never** | `QUALITY_GATE.md`'s shared-surface row requires any edit to them to be explicitly scoped and justified and to weaken nothing. This packet edits neither, which is the cheapest way to satisfy it. |

### The two terminal outcomes, and the decision rule that selects between them

**Both outcomes are legitimate completions. The decision rule below is fixed now, before any measurement exists**, so that deletion cannot be justified retroactively by relaxing a criterion, and so that retention cannot be dismissed as a failure to try.

**Outcome A — atomic nine-rule deletion.** All nine rules, the two comments that exist only to introduce them (`/* ===== RESPONSIVE BREAKPOINT HELPERS ===== */` and `/* Show/hide specific content at breakpoints */`), and the three now-empty `@media` shells are removed in one edit. `DEFERRED_HELPER_COUNTS` and its assertion are replaced by the contracts in the next section. The evidence document records the certification member by member.

**Outcome B — durable no-op audit.** No production line changes. The evidence document names **exactly which member(s)** failed certification and **on which DR-1 criterion**, with the raw record. The pin stays and is added to. The refuted "inherently blind" rationale is replaced by the measured facts, including the refutation itself — because the refutation is durable knowledge independent of the retention decision.

#### DR-1 — the decision rule (pre-committed)

Outcome A is selected **if and only if every one** of (a)–(g) holds, for **every one** of the nine rules, measured in this worktree at the packet's own base commit, with every control green:

| # | Criterion |
|---|---|
| **(a)** | Static inventory finds no definition site outside `static/css/layout.css` and no application site anywhere in `templates/**`, `static/js/**`, `static/css/**`, `scss/**`, `routes/**`, `utils/**` — including dynamic class construction. Generated `build/`/`dist/` copies are excluded as evidence; the absence of such a tree is recorded, not assumed. |
| **(b)** | Runtime full-selector census is **0** for all six class names, taken **before any injection**, across the full rendered-route set × 2 themes × 13 widths — while the natural-reachability controls (`.tbl-wrap`, `.tbl`, `.tbl-controls`, `.tbl-view-mode-toggle`) census non-zero on the table routes, proving the census reaches pages where `layout.css` is working. |
| **(c)** | Before-state positive effect: in **100%** of contexts where measured `matchMedia` says the rule's media condition applies **and** the rule owns `display` (see the applicability matrix), the synthetic host's computed `display` differs from its one-compound control, and equals the rule's own declared value. |
| **(d)** | Structural ownership: in every such context, CDP `matchedRules` attributes the winning `display` declaration to `layout.css` by `styleSheetId` + source range + media text — that rule's own range, never matched by substring. |
| **(e)** | Post-deletion flip: the identical measurement re-run after deletion reports **no** `layout.css` owner for `display` on the host, and the host's computed `display` equals its control's, in every context from (c). |
| **(f)** | Controls, before **and** after: known-live reads live; known-dead reads dead; every control host's own computed `display` equals its UA initial with **no** author `display` rule matching it; sentinel took effect and reverted cleanly on every record with transitions and animations suppressed before apply, read and remove; same-CSS control reports **zero** differing records; every stylesheet reachable at runtime is enumerated and any unreadable cross-origin sheet is accounted for out-of-band. |
| **(g)** | No candidate-attributable computed-style difference anywhere on any rendered page (`scripts/css_audit/runtime_probe.mjs` rest-state differential, before vs after, declaration-owner oracle **0** differing records outside the ledgered Welcome blind spot). |

**If any single criterion fails for any single member, outcome B is selected for the whole family.** There is no partial outcome and no per-member outcome. If (a)–(d) fail, outcome B is entered without any deletion being attempted. If (e)–(g) fail, the deletion is reverted (`git checkout -- static/css/layout.css`) and outcome B is entered.

#### Conservative fallbacks (stated explicitly, as required)

| Situation | Action |
|---|---|
| Evidence uncertainty of any kind | **Retain.** Uncertainty is never resolved in favour of deletion. |
| Partial proof — some members certified, others not | **Retain the whole family.** DR-1 admits no subset. |
| Visual noise without candidate-specific computed differences | **Record the noise; never rebaseline.** No snapshot, tolerance, mask, retry or config value is touched. Attribute the noise, or leave it attributed to the external blocker and say so. |
| A recommendation that expands scope | **Defer with a written rationale.** Already applied to A5 (committing the oracle) and A6 (annotating `_E_LAYOUT_`). |
| A control fails | **The run is void.** Fix the control, re-run everything, and report the defect in the evidence document — the packet's credibility rests on the controls, not on the result. |

### The oracle

#### Applicability matrix (proof obligation 4)

The three **base** rules are superseded inside their own class's `@media` block by a later rule of equal specificity, so each base rule owns `display` only **outside** that band. The `.tbl-hide-*` classes have no base rule at all, so outside their band nothing in `layout.css` declares `display` on them.

| # | Rule | Source lines | Declares | Owns `display` when measured `matchMedia` says |
|---|---|---|---|---|
| 1 | `.tbl-show-sm` (base) | 1594–1596 | `display: none` | `(max-width: 820px)` is **false** |
| 2 | `.tbl-show-md` (base) | 1598–1600 | `display: none` | `(min-width: 821px) and (max-width: 1200px)` is **false** |
| 3 | `.tbl-show-lg` (base) | 1602–1604 | `display: none` | `(min-width: 1201px)` is **false** |
| 4 | `.tbl-hide-sm` | 1607–1609 | `display: none` | `(max-width: 820px)` is **true** |
| 5 | `.tbl-show-sm` (override) | 1611–1613 | `display: block` | `(max-width: 820px)` is **true** |
| 6 | `.tbl-hide-md` | 1617–1619 | `display: none` | `(min-width: 821px) and (max-width: 1200px)` is **true** |
| 7 | `.tbl-show-md` (override) | 1621–1623 | `display: block` | that query is **true** |
| 8 | `.tbl-hide-lg` | 1627–1629 | `display: none` | `(min-width: 1201px)` is **true** |
| 9 | `.tbl-show-lg` (override) | 1631–1633 | `display: block` | `(min-width: 1201px)` is **true** |

Rules 5, 7 and 9 are the three WP4.4-e could not distinguish. They are distinguishable on a host whose UA initial `display` is not `block`.

#### Hosts, controls and widths

- **Hosts** (proof obligation 6's other half): `<span>` → `inline`, `<li>` inside a `<ul>` → `list-item`, `<td>` inside `table > tbody > tr` → `table-cell`. Each host is built in a valid ancestor chain so no anonymous-box fixup distorts the reading. **No author CSS is injected to manufacture a baseline** — the whole point is that the UA initial is already not `block`.
- **Control**: the same host, same tag, same DOM position and ancestry, same (empty) inline style, differing **only** by the presence of the single candidate class. That is "fails the selector by exactly one compound" for a one-compound selector.
- **Control validation** (the WP4.4-e lesson, generalized): the control's own computed `display` must equal its UA initial **and** CDP `matchedRules` must show **no author rule declaring `display`** on it, in every context. A control that reads `block` means something else is styling the host and the record is void — this is the check that would have caught the `.tbl-wrap` known-live defect on the control side.
- **Widths** — 13, chosen to sit immediately below / at / above both boundaries and to reproduce the spike's 4 / 5 / 4 band split exactly:
  - `≤ 820`: **360, 480, 819, 820**
  - `821–1200`: **821, 900, 1024, 1199, 1200**
  - `≥ 1201`: **1201, 1202, 1440, 1920**
  Applicability is read from **measured `matchMedia`** inside the page, never from the nominal viewport width — scrollbar and device-pixel effects can move the layout viewport off the number Playwright was given.
  > **⟢ CORRECTED at Plan v2 — the guessed set is not the set that ran.** The executed run used **`375, 600, 819, 820, 821, 822, 1000, 1199, 1200, 1201, 1202, 1440, 1920`**. Same 4 / 5 / 4 band split, different interior widths, and one extra boundary probe (`822`) my set lacked. Applicability was read from measured `matchMedia` in every context, and **the nominal width matched the measured band at all 13 widths** — so the scrollbar hazard I named did not fire here, which is itself worth recording rather than assuming.
- **Denominators** that this width set implies, published in the evidence document and checkable by the reader: 3 hosts × 2 routes × 2 themes × 13 widths = **156** records per rule; base rules 156 − (their band) and media rules exactly their band, so `1 → 108, 2 → 96, 3 → 108, 4 → 48, 5 → 48, 6 → 60, 7 → 60, 8 → 48, 9 → 48`. These are the spike's numbers, and their complementarity (108+48 = 96+60 = 108+48 = 156) is a coherence check, not a substitute for re-measuring.
  > **⟢ CORRECTED at Plan v2 — superseded by measurement.** Per-rule universe is **3 hosts × 11 routes × 2 themes × 13 widths = 858**, not 156. Measured denominators, now binding under DR-1(h): `1 base-show-sm → 594`, `2 base-show-md → 528`, `3 base-show-lg → 594`, `4 sm-hide → 264`, `5 sm-show → 264`, `6 md-hide → 330`, `7 md-show → 330`, `8 lg-hide → 264`, `9 lg-show → 264`. Complements exact: 594+264 = 528+330 = 594+264 = 858.
- **Census breadth**: the *synthetic* measurement runs on 2 table routes (`/workout_plan`, `/workout_log`); the *census* runs across the full rendered-route set, because a candidate class applied on a non-table page would falsify unreachability just as thoroughly.
  > **⟢ SUPERSEDED at Plan v2**: the synthetic measurement also ran across all 11 rendered routes, so measurement and census share one geometry. See the A8 correction in Section 0.

#### Sentinel handling (proof obligation 9)

`display` is not currently animated, and `transition-behavior: allow-discrete` is not in use — but the procedure is applied anyway, because M6a is procedural, cheap, and the failure it prevents (a sentinel reading back its pre-sentinel value) is silent. Suppress transitions **and** animations before applying, before reading, and before removing the sentinel; release symmetrically. The sentinel value is `grid` — chosen because it collides with none of `none` / `block` / `inline` / `list-item` / `table-cell`, so "took effect" and "reverted cleanly" are both unambiguous. Assert both **per record**, never in aggregate.

#### Source identity (proof obligation 8)

Ownership is resolved through CDP `CSS.getMatchedStylesForNode`: `styleSheetId` → the sheet's URL, plus the rule's `range` (start/end line and column) and its enclosing `media.text`. Never by substring, never by `nth-child` position, never by re-serialized CSS text — `verification.md` records that re-serialization is not byte-preserving. Offsets are computed on LF-normalized text (the repo is `core.autocrlf=true` with no `.gitattributes`).

### Artifacts

| Path | Change | Notes |
|---|---|---|
| `static/css/layout.css` | **delete** (outcome A) / **no-op** (outcome B) | **⟢ CORRECTED at Plan v2: the unit is `1589–1634`, not `1594–1634`** (architecture #6); the `LOADING STATE` banner at `:1584–1586` is deliberately left. Outcome A removes lines 1594–1634 as one unit: the three base rules, the three `@media` blocks in full (they contain nothing else), and the two comments that exist only to introduce them. Outcome B leaves the file byte-identical. No other line of this file is touched under either outcome; the print `.tbl-controls, .tbl-toolbar` rule, `.tbl-controls`, `.tbl-view-mode-toggle` and the separator block are all explicitly preserved. |
| `tests/test_css_wp4_4_layout_contracts.py` | **modify** | Outcome A: remove `DEFERRED_HELPER_COUNTS` and its assertion inside `test_retained_rules_are_still_present`, add contracts C1–C5 below. Outcome B: keep both, add C2–C4, correct the rationale comment. Under both outcomes the module docstring gains a pointer to the new evidence document. `RETAINED_SNIPPETS`, `test_partially_reachable_rules_kept_their_dead_branch` (including the `.input-frame` = 9 / `.tbl-toolbar` = 1 occurrence pins), `test_dark_theme_table_tokens_have_a_live_definition`, `test_body_dark_mode_block_stays_deleted`, `test_layout_css_declares_no_cascade_layer`, `test_orphaned_keyframes_went_with_their_only_consumer` and the four separator-contrast tests are **not weakened, not renamed, not reordered**. **⟢ CORRECTED at Plan v2** (architecture #8): there are **two** collected separator tests, not four — one function `test_table_separator_clears_non_text_contrast` at `:379–419` parametrized light/dark. |
| `docs/css_table_helpers_cleanup/PLANNING.md` | **new** (this file) | Section 0 + Plan v1 now; response matrix + Plan v2 after the council. |
| `docs/css_table_helpers_cleanup/EVIDENCE.md` | **new** | Outcome, DR-1 applied member by member, full denominator derivation, raw control output, the known-live control defect and its fix, the refutation of the WP4.4-e "inherent limit", the reproduction recipe, the gate table, the preservation invariants, and — on outcome B — exactly which member failed and on which criterion. Placed in the feature folder rather than at `docs/` root: the root `CSS_PHASE4_*` sprawl is a recorded archive problem (`docs/LEFTOVERS_BY_PRIORITY.md` v23 N7), and **no pytest assertion is added on this document's path**, deliberately, so it does not join the six evidence files whose relocation would red a required CI context. **⟢ CORRECTED at Plan v2** (architecture #10): N7 over-counts — only the two JSON baselines are pytest-asserted, not the markdown evidence files. The placement decision stands; its stated justification is narrowed to "do not create a new pytest-asserted doc path", which is true independently of N7. |
| `docs/test_inventory/TEST_INVENTORY.md` + `.json` | **regenerate** | Mandatory, both outcomes: the test count moves. `Test Inventory Drift` is a required branch-protection context. |
| `artifacts/tblhelpers/**` | generated, **gitignored** | Oracle, controls, raw records, before/after runs, gate logs. Never committed (ADR-002). |

Anything not in this table is not written. If implementation discovers a strictly necessary contract-only change outside it, the packet **stops** and presents it at Gate 1.

### Replacement contracts for outcome A — exact shape, and why each is stronger

The pin being replaced is:

```python
DEFERRED_HELPER_COUNTS = {
    "tbl-show-sm": 2, "tbl-show-md": 2, "tbl-show-lg": 2,
    "tbl-hide-sm": 1, "tbl-hide-md": 1, "tbl-hide-lg": 1,
}
```
asserted inside `test_retained_rules_are_still_present` by counting `re.findall(rf"\.{cls}(?![\w-])", stripped)` over the comment-stripped file. **⟢ CORRECTED at Plan v2** (architecture #8): the file's actual regex at `:198` is `rf"\.{re.escape(cls)}(?![\w-])"` — my transcription dropped the `re.escape`.

Its three structural weaknesses, stated plainly, because "stronger" only means something against a named weakness:

- **W1 — it pins a number, not a state.** `2` is satisfied by two live rules and by nothing else; it cannot express "gone".
- **W2 — it pins the stylesheet only.** It says nothing about whether any template or module *applies* the class, which is the premise the whole deletion argument rests on. WP4.4-e proved census 0 by measurement and then locked only the CSS side of it.
- **W3 — it pins one file.** A sibling bundle or a page bundle could define `.tbl-show-md` tomorrow and this assertion would stay green.

| # | Contract | Shape | Why strictly stronger |
|---|---|---|---|
| **C1** | `test_breakpoint_helper_family_is_absent_from_layout_css` | For each of the six class names, count **rule heads** whose selector list contains a compound carrying that class — at any nesting depth, including inside `@media` — using the file's existing length-preserving `_strip_comments` and the `(?![\w-])` boundary guard, and assert the count is `0`, reporting offenders by name. | Fixes **W1**: `0` is a state, not a tally, and it admits no member. Rule-head counting rather than substring matching also survives reformatting and reports *where*, which the `findall` form cannot. It is the same technique `tests/test_css_wp4_4_components_contracts.py::test_whole_rule_generations_are_gone` already uses — and whose docstring cites the WP4.4-e red path on `.tbl-show-sm` as the reason substring presence was too weak. |
| **C2** | `test_breakpoint_helper_family_is_all_or_nothing` | Count family selector occurrences **inside** the three `@media` blocks and **outside** them, and assert the two sets are consistent: either both empty (family deleted) or the full 3-base + 6-override shape present. Fails on any partial state in **either** direction. | Fixes the failure mode the family's indivisibility exists to prevent, which the count pin only encoded accidentally: an `@media` override left targeting a class with no base rule, or base rules left with no overrides. It is **outcome-independent** — the same contract holds under A and under B — so it keeps the indivisibility guarantee permanently, not just until this packet lands. |
| **C3** | `test_breakpoint_helper_classes_are_unreachable` | Add the six names to the corpus scan that `test_deleted_classes_are_still_unreachable` already performs over `templates/**/*.html` and `static/js/**/*.js`, **and widen the detector**: today it sees only `class="…"` attributes and `classList.add/toggle/replace('literal')`. Add `className =`, `setAttribute('class', …)`, and — the important one — **dynamic construction**: assert the literal tokens `tbl-show` and `tbl-hide` do not appear *anywhere* in those two trees, in any syntactic position, which catches `'tbl-show-' + size` and `` `tbl-${size}` `` alike. (Verified clean today: `grep` finds the tokens only in `layout.css`, two test files and docs.) | Fixes **W2**, which is the largest gap. The old pin could not notice a template adopting the class; this one turns adoption into a pytest red and therefore into a deliberate decision. It also discharges M10 (JS-applied classes) permanently rather than as a one-time measurement, and it is a contract that *should exist under outcome B too* — retention without a reachability gate leaves the same hole. |
| **C4** | `test_breakpoint_helper_classes_have_no_definition_site_in_any_bundle` | Glob **every** `static/css/*.css` (not a fixed parametrize list) and assert none defines any of the six as a selector. Includes `bootstrap.custom.min.css` and every page bundle; new bundles are covered automatically. | Fixes **W3**, and is stronger than the existing `test_deleted_classes_are_not_resurrected_by_a_sibling_surface`, whose surface list is hard-coded to five files. It also converts the spike's "no foreign stylesheet defines a candidate class" finding from a one-time measurement into a standing guarantee. |
| **C5** | `test_layout_css_has_no_empty_media_block` | Assert `layout.css` contains no `@media …{ }` whose body is whitespace-only. | Small, but it forecloses the specific sloppy deletion — removing the rules while leaving three empty `@media` shells — that would produce a passing C1 and a residue that later reads as intentional. Adds a guarantee the old pin had no analogue for. |

**Not weakened, not replaced:** `RETAINED_SNIPPETS` (`[data-theme="dark"]`, `.tbl-controls,`), `test_partially_reachable_rules_kept_their_dead_branch`, and every other test in the file. `test_retained_rules_are_still_present` survives with its `RETAINED_SNIPPETS` half intact; only its `DEFERRED_HELPER_COUNTS` half is removed, and it is removed **into** C1–C5, not away. Note that `.tbl-controls` and `.tbl-view-mode-toggle` are simultaneously the oracle's known-live controls and rules this packet retains — a deletion that touched either would invalidate its own measurement apparatus.

**On outcome B**, `DEFERRED_HELPER_COUNTS` and its assertion stay **exactly as they are**, C2, C3 and C4 are added alongside them, and the block comment at lines 76–94 is rewritten to state (i) the measured refutation of the "no control element can distinguish them" claim, (ii) which member actually failed and on which DR-1 criterion, and (iii) that the family remains indivisible. Nothing about outcome B loosens the existing gate; it only stops the file from asserting something untrue.

### Effort · Owner · Depends on

**Effort**: **L** — three-host oracle across 52 contexts *(⟢ CORRECTED: the executed run used **286** contexts — 11 routes, not 2)* with a full control suite, two complete oracle runs, a rest-state differential run pair, five new contracts with red paths, and the full shared-surface gate list including a Linux deep gate against a known-unstable pixel matrix.

**Owner**: `senior-developer` in the `wt/css-tbl-helpers` worktree, after Gate 1. **Depends on**: Gate 1 approval of Plan v2. **Externally blocked at merge, not at implementation**, by the visual nondeterminism PR #296 is investigating.

### Sequence

Steps 1–13 execute **only after Gate 1**. Nothing below is authorized by Gate 0.

1. **Isolation and base pinning.** Work exclusively in `D:/development/Hypertrophy-Toolbox-v3-tblhelpers`; never read-modify the main checkout. Record the base commit. Confirm `PW_REUSE_SERVER` is unset and that no other worktree is running Playwright — `verification.md`'s parallelism rule and `playwright.config.ts`'s hard-coded port 5000 make a concurrent run capable of certifying this packet against another worktree's CSS. Confirm no PR #296 file is present in the diff and no experimental switch is enabled.
2. **Static inventory** (obligation 1, DR-1(a)). Enumerate every definition and application site for the six class names across `templates/**`, `static/js/**`, `static/css/**`, `scss/**`, `routes/**`, `utils/**`, `e2e/**`, `tests/**`, `docs/**`, including dynamic construction patterns. Record that no `build/`/`dist/` tree exists and that any such copy would be excluded as evidence. Record the exact grep forms used, so the reader can re-run them.
3. **Pre-change gate baseline.** On the unmodified tree at the base commit: full `pytest tests/`, the nine Chromium specs, the seeded `visual.spec.ts` matrix, seven-surface Stylelint, `generate_test_inventory.py --check`. Store under `artifacts/tblhelpers/before/`. This is the comparison basis — given the measured Windows staleness and the wide-desktop instability, "all green" is not available as an acceptance criterion and a same-machine differential is the only honest one.
4. **Build the oracle** in `artifacts/tblhelpers/`: three hosts, two table routes *(⟢ CORRECTED: **all 11 rendered routes** were measured, not two)*, two themes, thirteen widths, `matchMedia`-driven applicability, CDP structural ownership, `grid` sentinel with transition+animation suppression on apply/read/remove, one-compound controls with control-baseline validation, known-live (`.tbl-controls`, `.tbl-view-mode-toggle`) and known-dead controls, full stylesheet enumeration with cross-origin sheets accounted for out-of-band, and full-selector census taken **before** any injection. Write the script to the scratchpad/artifacts and run the file — no bash heredocs; quote every path.
5. **Validate the oracle before trusting it.** All controls green; same-CSS control zero differing records; every denominator derived and published. **If any control fails, stop** — the run is void; repair the control, re-run everything, and record the defect (this is exactly how the `.tbl-wrap` 0/78 defect was caught).
6. **Before-run**: census + per-rule positive effect + structural owner, all 156 records per rule *(⟢ CORRECTED: **858** per rule = 3 hosts x 286 contexts)*. Also run `scripts/css_audit/runtime_probe.mjs` **unchanged** for the rest-state differential before-state.
7. **Apply DR-1 (a)–(d).** If any member fails, go to step 10B without touching `layout.css`.
8. **Outcome A — the atomic edit.** Delete all nine rules, the three `@media` shells and the two introducing comments in one edit. Nothing else in the file changes. **⟢ CORRECTED at Plan v2: the range is `layout.css:1589–1634`**; the `LOADING STATE` banner at `:1584–1586` is deliberately left.
9. **After-run + flip check + rest-state differential after-state.** Apply DR-1 (e)–(g). If any member fails, `git checkout -- static/css/layout.css` and go to step 10B.
10. **Contracts.**
    - **10A (outcome A)**: implement C1–C5, remove `DEFERRED_HELPER_COUNTS` and its assertion, update the module docstring. Prove each red path — re-add `.tbl-show-md { display: none; }` (C1); add only the `@media (max-width:820px)` override with no base rule (C2); add `class="tbl-hide-lg"` to a template, `classList.add('tbl-show-sm')` to a module, and `'tbl-show-' + size` string construction (C3, three separate paths); add `.tbl-show-sm {}` to `components.css` (C4); leave `@media (min-width:1201px) { }` behind (C5). Restore the tree after each and re-confirm green.
    - **10B (outcome B)**: keep the pin intact, add C2–C4, rewrite the rationale comment to the measured facts and name the uncertifiable member. Prove the same red paths for C2–C4.
11. **Evidence document** `docs/css_table_helpers_cleanup/EVIDENCE.md`, per the artifact table.
12. **Post-change gates**, differenced against step 3: full `pytest tests/`; the nine Chromium specs; the seeded `visual.spec.ts` matrix; seven-surface Stylelint with no category increase and V3/V4 checked (`!important`, `selector-max-id`, `selector-max-specificity`, `no-duplicate-selectors`, `declaration-block-no-duplicate-properties`); test inventory regenerated and committed; pyright measure-only clean of net-new diagnostics from the new test code; and a `git diff --name-only HEAD` + `git ls-files --others --exclude-standard` proof that the changed set is exactly the artifact table.
13. **Linux `visual-linux` deep gate**, interpreted against the **current accepted baselines** (post-PR #281 `864043f`), explicitly **not** against `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json`, whose `sourceCommit` `46e340e` predates that regeneration — `QUALITY_GATE.md` records this caveat and the ledger is not re-pinned by this packet. Classify each red: inside the known-unstable capture set (`workout-plan-desktop-{dark,light}`, `plan-desktop-{dark,light}-advanced`) → attributed to the external blocker and cross-referenced to the three same-SHA runs measured on `main` @ `ac2923b`; outside it → a V1 rollback trigger. Because one run in three meets the bar at a fixed SHA, a single green compare is reported as *a gate that ran*, never as evidence. Repeat runs only to characterize a red that falls **outside** the known-unstable set. If nondeterminism persists, the draft PR is left accurately blocked on that external merge gate and says so.

**Rollback.** At any point, `git checkout -- static/css/layout.css` restores the production surface; nothing else in the packet touches a production path. Outcome B is reachable from any step and is a completion, not a rollback.

### Expected gates

*(To be confirmed or corrected by `test-strategist` at council — this is the planner's derivation from `QUALITY_GATE.md`'s `CSS (static bundles)` shared-surface row, which is canonical.)*

- **pytest**: full `tests/` suite. `tests/test_css_wp4_4_layout_contracts.py` is the packet's own target; `tests/test_css_cascade_contracts.py` and `tests/test_visual_selector_contracts.py` run **inside that total, unedited**.
- **e2e (Chromium)**: `smoke-navigation`, `nav-dropdown`, `accessibility`, `dark-mode`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening`.
- **visual**: the full `visual.spec.ts` matrix with `PW_VISUAL_SEED=1` (66 tests per platform over 11 pages). Run as a gate; reported as a differential against the step-3 same-machine pre-run; **never** cited as candidate-specific evidence (A7). No snapshot written, no `--update-snapshots`, no tolerance/mask/retry/config change.
- **Stylelint**: `node scripts/css_audit/stylelint_surfaces.mjs`, seven surfaces, **no category may rise**. Under outcome A a decrease is expected and is reported with per-rule attribution; under outcome B the delta must be exactly zero.
- **Linux deep gate**: `visual-linux`, per step 13 — against current accepted baselines, not the stale ledger.
- **Test inventory**: `scripts/generate_test_inventory.py` regenerated and committed; `--check` clean. Required branch-protection context.
- **Type check**: pyright measure-only must gain no net-new diagnostics from the new test code.
- **Not required**: `/build-css` — `scss/**` is untouched and `bootstrap.custom.min.css` is not regenerated.

### Preservation invariants for this packet

| # | Invariant | Pass condition |
|---|---|---|
| **P1** | Rendering, table behaviour and accessibility unchanged | Rest-state differential: declaration-owner oracle **0** differing records outside the ledgered Welcome blind spot; the nine Chromium specs green vs the step-3 baseline; `accessibility.spec.ts` in particular. |
| **P2** | Calculations, APIs, schemas and DB state unchanged | No Python or JS production file opened; full pytest green. |
| **P3** | No rebaseline, no tolerance change | `git diff --name-only` shows zero paths under `e2e/__screenshots__/` and zero changes to `e2e/visual-helpers.ts` or `playwright.config.ts`. |
| **P4** | No re-weighting (V3) | `!important` count, `selector-max-id` and `selector-max-specificity` do not rise. Pure deletion or pure no-op. |
| **P5** | No duplication increase (V4) | `no-duplicate-selectors` and `declaration-block-no-duplicate-properties` do not rise. |
| **P6** | `@layer` membership unchanged (N2, via the live test) | `test_layout_css_declares_no_cascade_layer` stays green; `layout.css` declares no `@layer`. |
| **P7** | The record is true | No contract, comment or document in the tree asserts the refuted "inherently blind" rationale after this packet, under either outcome. **⟢ CORRECTED at Plan v2 — unsatisfiable as written** (architecture #1, product-risk #4). Four documents this packet does not write still carry the claim, and A6 deliberately leaves one of them alone. Rescoped in Plan v2 §"Preservation invariants (revised)" to the files the packet writes, with the four exempt documents named. |
| **P8** | Line contribution is reported, never chased (V5) | Outcome A ≈ −41 lines / −9 rules *(⟢ CORRECTED: **−47** lines, once the introducing banner and comment were included in the atomic unit)*; outcome B 0. Neither number is an acceptance criterion. |

---

## Agent provenance

*Required for every council run. The manager records each agent ID returned by its `Agent(...)` call and supplies the `product-manager` its own ID back, because an agent cannot know its own ID. The `product-manager` stamps the IDs the manager supplies — **never invent an ID**, never rerun completed council work to manufacture continuity, and record an unrecoverable ID as an evidence gap.*

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `a55d705da312a5f00` | Author of Section 0 and Plan v1. |
| `product-manager` — response matrix + Plan v2 | `a55d705da312a5f00` | Author of the matrix and Plan v2. Same agent as the row above. |
| `architecture-reviewer` | `abeba54f95e4ae9ea` | Step 2 reviewer. |
| `test-strategist` | `ac3ff43eb4c23f005` | Step 2 reviewer. |
| `product-risk-reviewer` | `a7788ede81f30d751` | Step 2 reviewer. |

**Same product-manager resumed for the matrix + Plan v2?** `yes` — resumed via `SendMessage` to the Plan v1 agent ID `a55d705da312a5f00`.

**Evidence gap**: `none`.

*Every ID above was supplied by the manager and stamped exactly as supplied. None was inferred, reconstructed or invented, and no completed council work was rerun to manufacture continuity.*

---

## Reviewer findings

*Run [`.claude/commands/council-plan.md`](../../.claude/commands/council-plan.md) step 2 — three agents in parallel. Paste each agent's output verbatim below. Do not summarize. Head each section with the reviewer's agent ID, matching the Agent provenance table.*

*Line references inside the three reviews point at Plan v1 as it stood when they read it. The inline `⟢ CORRECTED` notes added afterwards shift those line numbers; the citations are left exactly as written, because a review is a record of what was reviewed.*

### architecture-reviewer (agent `abeba54f95e4ae9ea`)

## Findings

**1. Plan v1 §"Preservation invariants" P7 (PLANNING.md:383) vs the artifact table (PLANNING.md:291–300) — P7 is unsatisfiable as written.**
P7 says "No contract, comment or document **in the tree** asserts the refuted 'inherently blind' rationale after this packet, under either outcome." The artifact table writes four paths plus the test inventory, and A6 deliberately leaves `_E_LAYOUT_` unchanged. The claim survives in at least four places the packet will not write:
- `D:/development/Hypertrophy-Toolbox-v3-tblhelpers/docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md:190` — "**No control element can distinguish them**: that is an inherent limit, not a fixable probe defect"
- `D:/development/Hypertrophy-Toolbox-v3-tblhelpers/docs/ACTIVE_DEVELOPMENT.md:275` — "three declare `display: block` … so no control element can distinguish them"
- `D:/development/Hypertrophy-Toolbox-v3-tblhelpers/docs/MASTER_HANDOVER.md:1781` — same claim
- `D:/development/Hypertrophy-Toolbox-v3-tblhelpers/docs/REFACTOR_PLAN.md:1412` — same claim

  Risk: the packet's stated deliverable is "a true record", and its own truth invariant either gets ticked falsely or stops the packet at step 12.
  Fix: scope P7 to the files the packet writes, and add an explicit deferral row naming those four documents as knowingly left stating a refuted rationale.

**2. Artifact table (PLANNING.md:291–300) — `docs/MASTER_HANDOVER.md` is a coordinated shared path and is neither claimed nor declared-deferred.**
`docs/ai_workflow/WORKSTREAM_OWNERSHIP.md:29–33` lists `docs/MASTER_HANDOVER.md` under "Never-claimed shared paths (coordinate per-edit)". `MASTER_HANDOVER.md:1779` is not history — it is a live directive: "**Deferred by `e`, owner-gated, do not act:** the nine-rule `.tbl-show-*` / `.tbl-hide-*` breakpoint-helper family". Under outcome A that instructs a future session not to act on a family that no longer exists; under outcome B its stated reason is refuted. `ACTIVE_DEVELOPMENT.md:274–279` carries the same directive ("**Do not erode it rule by rule.**"). The plan's "Anything not in this table is not written" (PLANNING.md:300) closes the door without a decision.
  Risk: either a stale operating directive ships, or the implementer edits a coordinated shared path with no declared coordination — the failure mode WORKSTREAM_OWNERSHIP.md exists to prevent.
  Fix: add one artifact-table row declaring `docs/MASTER_HANDOVER.md` and `docs/ACTIVE_DEVELOPMENT.md` as coordinated shared-state edits under both outcomes, or defer them explicitly as a named Gate 1 exception.

**3. Contract C4 (PLANNING.md:325) vs step 10B (PLANNING.md:353) — C4 is red on arrival under outcome B.**
C4 "Glob **every** `static/css/*.css` … and assert none defines any of the six as a selector." Step 10B adds C2–C4 under retention, where `static/css/layout.css:1594–1634` defines all six. The glob includes `layout.css`.
  Risk: outcome B lands a permanently failing required check, or the implementer weakens C4 at 10B to make it pass — exactly the "do not weaken a contract to make an outcome pass" move the owner forbade (PLANNING.md:37).
  Fix: specify C4 as "no bundle **other than `layout.css`**" for both outcomes, with an outcome-A-only tightening to "no bundle at all", and write both shapes into Plan v2. (Related trap for C5: keep it `layout.css`-scoped — `static/css/pages-workout-log.css:459,464,469,496,501` already contain five whitespace-only `@media` blocks, so a C4-style glob-all form of C5 is red on arrival.)

**4. Contract C3 (PLANNING.md:324) — it mutates a contract whose scope is 12 other classes, and the plan does not say where the six names live.**
`DELETED_CLASSES` (`tests/test_css_wp4_4_layout_contracts.py:38–51`) feeds three tests: `test_deleted_rule_blocks_stay_deleted` via `FULLY_REMOVED_CLASSES` (:58), `test_deleted_classes_are_still_unreachable` (:172), and `test_deleted_classes_are_not_resurrected_by_a_sibling_surface` (:312). "Add the six names to the corpus scan that `test_deleted_classes_are_still_unreachable` already performs" invites appending them to `DELETED_CLASSES`, which would make `test_deleted_rule_blocks_stay_deleted` assert their absence *from layout.css* — a second red-on-arrival under outcome B, and a silent duplicate of C1 under outcome A.
  Risk: outcome B cannot go green, or C1's strength claim is quietly carried by an unrelated WP4.4-e test.
  Fix: state in Plan v2 that the six names live in a separate `HELPER_CLASSES` tuple consumed only by the new contracts, and record the verification that the widened `className =` / `setAttribute` detector stays green for all 12 existing `DELETED_CLASSES` (I checked: the only hit in `static/js/**` is `toolbarSel = '[data-tbl-toolbar]'` at `static/js/table-responsiveness.js:363`, an attribute selector, not a class application).

**5. DR-1 criteria (c) and (e) (PLANNING.md:230, 232) — certification can be satisfied vacuously.**
Both read "in **100%** of contexts where measured `matchMedia` says the rule's media condition applies". Applicability is measured, not nominal — correctly, and PLANNING.md:277 names the reason (the layout viewport can differ from the requested width; headless Chromium's classic scrollbar can put a nominal 821px viewport inside `(max-width: 820px)`). Nothing in DR-1 requires the measured denominator to be non-zero or to equal the published 108/96/108/48/60/48. A rule whose band emptied would pass (c) on zero records and (e) on zero records.
  Risk: the inverse of `.claude/rules/verification.md:75` ("A probe that changes nothing proves nothing") — a rule certified dead by an empty measurement, in a packet whose entire premise is that WP4.4-e mis-measured.
  Fix: add DR-1(h): every rule's measured applicable-record count must be non-zero **and** equal its published denominator; any deviation is recorded and re-derived, never repaired by moving a width.

**6. Scope (PLANNING.md:185) and artifact table (PLANNING.md:293) — the stated deletion range excludes the comments it says it deletes.**
Both say "lines 1594–1634 … and the two comments that exist only to introduce them". In the file, `static/css/layout.css:1594` is `.tbl-show-sm {`; the two comments are at `:1589–1591` (the `RESPONSIVE BREAKPOINT HELPERS` banner) and `:1593`. The atomic unit is 1589–1634. Separately, `layout.css:1584–1586` is an already-empty `LOADING STATE` banner (its content went with `.tbl--loading` in WP4.4-e) that the deletion would leave stranded against the separator block.
  Risk: an "atomic, nothing else touched" edit whose declared range is wrong — the reviewer either sees a leftover banner or an unreviewed off-range edit.
  Fix: restate the unit as `layout.css:1589–1634` and say explicitly whether the empty `LOADING STATE` banner at :1584–1586 is in scope or deliberately left.

**7. Step 10A (PLANNING.md:352) vs Scope/Out (PLANNING.md:191) and acceptance criterion 7 (PLANNING.md:117) — the C3 red paths require edits to trees the plan forbids absolutely.**
10A requires adding `class="tbl-hide-lg"` to a template, `classList.add('tbl-show-sm')` to a module, and a `'tbl-show-' + size` construction. Out-of-scope bars `static/js/**` and `templates/**` without qualification, and AC7 asserts `git diff --name-only` shows zero changes to both.
  Risk: the implementer skips the red paths (owner proof obligation 12) or leaves a stray edit behind.
  Fix: add one sentence permitting transient, never-committed red-path edits under `templates/**` and `static/js/**`, verified clean by the `git status --others` proof step 12 already runs.

**8. Artifact table (PLANNING.md:294) and the quoted pin (PLANNING.md:312) — two factual errors about the file being edited.**
"the four separator-contrast tests" — the file has one separator function, `test_table_separator_clears_non_text_contrast`, parametrized light/dark (`tests/test_css_wp4_4_layout_contracts.py:379–419`), i.e. two collected tests. The quoted pin regex is given as `re.findall(rf"\.{cls}(?![\w-])", stripped)`; the file has `rf"\.{re.escape(cls)}(?![\w-])"` (`:198`).
  Risk: small on its own, but the mandatory `TEST_INVENTORY` regeneration is driven by exact test counts, and this is the packet whose deliverable is that the record is true.
  Fix: correct both to what the file states.

**9. "Run always, edit never" (PLANNING.md:191, 212) — the coupling inventory names 2 of the 6 test files that read `layout.css`.**
The other four are `tests/test_css_wp4_4_base_contracts.py:39`, `tests/test_css_field_separator_contracts.py:24`, `tests/test_css_wp4_4_a_baseline_contracts.py:49`, `tests/test_css_wp4_4_a11y_contracts.py:427`. I checked each against a nine-rule deletion and **none reds**: base contracts assert only `"animation: fadeIn" in LAYOUT` (:131); field-separator matches the separator rules by pattern (:168–175); the a-baseline test compares the JSON against its own `sourceCommit` with `git show`, deliberately not the working tree (:69–74, :101–106); the a11y sibling test scans only `LEGACY_CLASSES`.
  Risk: none measured — but an unstated coupling is one an implementer will not re-check when the deletion range shifts.
  Fix: record those four in Plan v2 as checked-and-unaffected, with the reason for each.

**10. A6 (PLANNING.md:158) vs the N7 citation (PLANNING.md:296) — the plan repeats a claim it elsewhere disproves.**
The evidence-doc location is justified by `docs/LEFTOVERS_BY_PRIORITY.md:224–231` (N7), which lists `_E_LAYOUT_` among "six … asserted by pytest". A6 correctly measures that `_E_LAYOUT_` appears only in a docstring at `tests/test_css_wp4_4_layout_contracts.py:5`, with no assertion on its path. Only the two JSON baselines are genuinely asserted (`tests/test_css_cascade_contracts.py:161`, `tests/test_css_wp4_4_a_baseline_contracts.py:34`).
  Risk: the packet's own doc-truth standard applied unevenly, in the paragraph that chooses where its evidence lives.
  Fix: cite N7 only for the two JSON baselines, and note that N7 over-counts the markdown evidence files.

## What is sound

- **Charter items 1–7 are not triggered.** No `routes/**`, `utils/**`, `app.py`, `tests/conftest.py`, schema, `DatabaseHandler`, `success_response`/`error_response`, `get_logger` or normalization surface is opened; PLANNING.md:124 states this and the grep confirms the six class names exist nowhere outside `static/css/layout.css` plus two test files and docs.
- **The factual base checks out.** `layout.css:1594–1634` holds exactly the nine rules with the declared values; the applicability matrix (PLANNING.md:254–264) is correct, including that each base rule is superseded inside its own band and that `.tbl-hide-*` has no base rule.
- **The control selection is verified live.** `.tbl-controls` `display: flex` at `layout.css:1423`, `.tbl-view-mode-toggle` `display: inline-flex` at `:1451`, created at `static/js/table-responsiveness.js:112` and `:239` — all four citations exact, and both rules are retained by this packet.
- **A3's Bootstrap claim holds.** `d-none` appears in `static/css/**` only at `a11y.css:565` and `:569`; `bootstrap.custom.min.css` has no such token.
- **The gate derivation is verbatim-correct** against `docs/ai_workflow/QUALITY_GATE.md:32` (nine Chromium specs, 66 visual tests over 11 pages, seven-surface Stylelint, Linux deep gate, shared-surface = Large) and the ledger caveat at `:39`, which does say to re-derive rather than reconcile against the stale `sourceCommit 46e340e`.
- **A5 needs no shared-state edit.** `/artifacts/` is already ignored at `.gitignore:57`.
- **The step-1 parallelism hazard is real.** `playwright.config.ts:74,120` hard-code `http://127.0.0.1:5000` and `:9` gates reuse on `PW_REUSE_SERVER`, so a concurrent worktree run could certify against another checkout's CSS.
- **C1's precedent claim is accurate** — `tests/test_css_wp4_4_components_contracts.py:305–316` counts rule heads and its docstring cites the WP4.4-e `.tbl-show-sm` red path as the reason substring presence is too weak.
- **The M-rule and `verification.md` citations are real** — front matter `static/css/**/*.css` at `.claude/rules/verification.md:3`; M6a at `docs/css_phase4_wp4_4/PLANNING.md:78`/`:1523`, M10 `:1537`, M11 `:1538`, M12 `:1539`.
- **DR-1 pre-commitment, the indivisibility rule, the conservative-fallback table and the refusal to treat pixels as candidate evidence (A7) are the right architecture for this claim shape**, and DR-1(b)'s positive census control closes the hole WP4.4-e's `.tbl-wrap` defect opened.

Not verified: the base commit `ac2923b` (no shell available to me in this session).

**Needs revision** — findings 1–5 are design-level and each has a one-line fix; nothing here is unfixable at Plan v2.

### test-strategist (agent `ac3ff43eb4c23f005`)

## Required gates

- **pytest:** full `tests/` suite (canonical: `docs/ai_workflow/QUALITY_GATE.md:32`, `static/css/**` shared-surface row). Packet target `D:/development/Hypertrophy-Toolbox-v3-tblhelpers/tests/test_css_wp4_4_layout_contracts.py`; `tests/test_css_cascade_contracts.py` and `tests/test_visual_selector_contracts.py` run inside that total, unedited.
- **e2e (Chromium):** `smoke-navigation`, `nav-dropdown`, `accessibility`, `dark-mode`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening` — plus, per F3/F4 below, `e2e/visual-baseline-thumbnails.spec.ts` and `e2e/visual-field-separator.spec.ts`.
- **visual:** `e2e/visual.spec.ts` (66) **and** `e2e/visual-baseline-thumbnails.spec.ts` (18) with `PW_VISUAL_SEED=1`.
- **other:** seven-surface Stylelint (`node scripts/css_audit/stylelint_surfaces.mjs`); Linux `visual-linux` deep gate; `scripts/generate_test_inventory.py` regenerate + commit; pyright measure-only. **Not** `/build-css` — correct, `scss/**` is untouched.

---

## Findings

### F1 — BLOCKING. C4 is red-by-construction under outcome B

PLANNING.md:325 defines C4 as "Glob **every** `static/css/*.css` … and assert none defines any of the six as a selector." PLANNING.md:330 then says outcome B adds "C2, C3 and C4" alongside the retained pin. Under outcome B, `D:/development/Hypertrophy-Toolbox-v3-tblhelpers/static/css/layout.css:1594-1633` still defines all six, so C4 fails on the first run. The two statements cannot both hold.

Fix: C4 must exclude `layout.css` by name. That also makes it a clean W3 contract (siblings only) and genuinely outcome-independent, with C1 owning the layout.css-side statement.

### F2 — BLOCKING. Under outcome A, C2 has no independent red path and half its logic is unexercised

C1 asserts rule-head count `0` for all six classes at any nesting depth. C2's failure state (a partial family) is by definition a non-zero count, so **every** state that reds C2 also reds C1. The step-10A red-path proof for C2 — "add only the `@media (max-width:820px)` override with no base rule" (PLANNING.md:352) — reds C1 too. A contract that cannot be the sole failure is not "strictly stronger"; it is subsumed.

Worse, C2's second branch ("the full 3-base + 6-override shape present") is never reachable under outcome A, so a mis-parse of `@media` nesting inside it would be undetectable and would sit in the tree as a green-looking guarantee.

Fix, either: (a) prove C2 two-sidedly — restore all nine and demonstrate C2 green while C1 red, which is the only proof its positive branch has meaning; or (b) drop the "outcome-independent / permanent indivisibility" claim and state that C2 is load-bearing under outcome B only. The owner's constraint was that replacements be *stronger* and red-path-provable; as written C2 satisfies neither under A.

### F3 — BLOCKING. The gate list omits `e2e/visual-baseline-thumbnails.spec.ts`, which the plan's own step 13 runs

`D:/development/Hypertrophy-Toolbox-v3-tblhelpers/.github/workflows/deep-gate.yml:399-400` runs both visual specs:

```
npx playwright test --project=chromium \
  e2e/visual.spec.ts e2e/visual-baseline-thumbnails.spec.ts $UPDATE
```

`docs/test_inventory/TEST_INVENTORY.json` records `visual.spec.ts` = 66 and `visual-baseline-thumbnails.spec.ts` = 18. **66 + 18 = 84** — exactly the "84 passed" denominator in the plan's own measurement of `main` @ `ac2923b`. The plan's "Expected gates" (PLANNING.md:366) names only "the full `visual.spec.ts` matrix … (66 tests per platform over 11 pages)."

Three consequences:
1. Steps 3 and 12 would build a local Windows before/after pair that omits 18 pixel-baselined tests captured on **plan and log tables** — the exact surface `layout.css` owns.
2. The step-13 denominator will be 84 against a stated 66; the gate report will not reconcile.
3. The pre-declared "known-unstable capture set" (`workout-plan-desktop-{dark,light}`, `plan-desktop-{dark,light}-advanced`) covers `visual.spec.ts` captures only, so a thumbnails red has no classification and would default to a V1 rollback trigger.

QUALITY_GATE.md:32 is itself partial here (it names only the 66-test matrix) — the plan copied it faithfully. But the plan independently commits to the `visual-linux` job, and that job runs both. Name both specs and extend the classification list.

### F4 — SHOULD FIX. `e2e/visual-field-separator.spec.ts` is the one deterministic computed-style Chromium oracle over `layout.css` and is absent

It runs in the required functional gate (`.github/workflows/ci.yml:286`), has no pixel baseline, is cross-OS stable by construction, and asserts rendered separator/outline contrast across 7 surfaces × 3 viewports × 2 themes (42 tests; `.claude/rules/testing.md:100`). Given A7 disclaims all pixel evidence and puts the verdict on computed style, this is the highest-value spec available and it is not in the nine. Adding it strengthens the gate, so it needs no owner exception.

Its pytest twin `tests/test_css_field_separator_contracts.py` reads `layout.css` and runs inside the full suite — no action, but it belongs in the plan's coverage map.

### F5 — SHOULD FIX. The Windows visual matrix has no repeat policy — the same trap the plan correctly refuses on Linux

Step 13 pre-commits to "one run in three meets the bar, so a single green compare proves nothing" and authorizes repeat runs for Linux. Steps 3 and 12 commit to exactly **one** Windows pre-run and **one** post-run, then "difference" them (PLANNING.md:344, 355). If the wide-desktop instability is renderer-level rather than platform-level, a single Windows pair is subject to the identical single-sample error — and `e2e/__screenshots__/win32` is independently stale on `main` (the plan's own Section 0 records `plan-desktop-light-advanced` at 541,849 px / 29% on a pristine tree).

A one-sample comparison is not a differential. Run the Windows pre-change matrix at least twice at the base commit — three times matches the Linux characterization — publish the per-capture stable/unstable partition as a **pre-declared** list, and treat only post-change reds *outside* that partition as signal.

### F6 — SHOULD FIX. `Test Inventory Drift` risk if C1/C4 are parametrized over a glob

`Test Inventory Drift` is a required branch-protection context (QUALITY_GATE.md:114-119) and the job at `.github/workflows/ci.yml:938-960` regenerates on Linux via `pytest --collect-only` **without** running `npm run build:css`. `scripts/generate_test_inventory.py` records per-file collected node counts and has exactly one escape hatch (`ENVIRONMENT_DEPENDENT_PYTEST_FILES`, lines 56-65) whose comment forbids using it to silence a real diff.

If C4 is `@pytest.mark.parametrize` over `glob("static/css/*.css")`, its node count becomes a function of the files present on the collecting machine — any untracked local `.css` scratch file in the dev worktree moves the Windows count without moving the Linux one, and reds a required context.

Fix: implement C4 as a single test looping `sorted(...)` and reporting all offenders. Same for C1 (one test over six classes, not six params). Node count then stays 1 regardless of bundle set.

### F7 — SHOULD FIX. C3's "add the six names to the corpus scan" is ambiguous, and one reading is red-by-construction under outcome B

If "add the six names" means extending `DELETED_CLASSES` (`tests/test_css_wp4_4_layout_contracts.py:38-51`), then under outcome B both `test_deleted_rule_blocks_stay_deleted` (line 97) and `test_deleted_classes_are_not_resurrected_by_a_sibling_surface` (line 296) iterate that tuple and red immediately, because `layout.css` still styles the family. Declare a separate `BREAKPOINT_HELPER_CLASSES` tuple; do not extend `DELETED_CLASSES` under either outcome.

Separately, state whether the detector widening (`className =`, `setAttribute('class', …)`) applies to the new test only or also to `test_deleted_classes_are_still_unreachable`. Widening the shared detector extends it over WP4.4-e's twelve classes and is a scope expansion needing its own green proof.

**C3's factual premise is sound and I verified it.** `tbl-show` / `tbl-hide` appear only in `static/css/layout.css`, `tests/test_css_wp4_4_layout_contracts.py`, `tests/test_css_wp4_4_components_contracts.py:312`, and docs. Zero hits in `templates/**` and `static/js/**`.

### F8 — NOTE. Existing coverage the plan does not name, two items of which enforce its own invariants

All run inside "full pytest", so no gate changes — but the plan should cite them:

- `tests/test_css_wp4_4_a_baseline_contracts.py:39-44` — `EXPECTED_SNAPSHOT_COUNTS` manifests the committed screenshot trees (`win32` 66/18, `linux` 68/18). **This is the mechanical enforcement of the plan's P3 ("no rebaseline")**, stronger than the `git diff --name-only` check P3 currently relies on. Cite it as the P3 gate.
- `tests/test_css_wp4_4_a_baseline_contracts.py:61` — compares per-surface line counts against the baseline's own `sourceCommit` via `git show`, deliberately **not** the working tree (docstring lines 69-74; WP4.4-c fixed exactly this). So outcome A's ~41-line deletion does **not** red it. Record that, or a reviewer will read a line-count pin as a blocker.
- The other four files reading `layout.css`: `tests/test_css_cascade_contracts.py`, `tests/test_css_field_separator_contracts.py`, `tests/test_css_wp4_4_base_contracts.py`, `tests/test_css_wp4_4_a11y_contracts.py`.

### F9 — NOTE. Known-red awareness is absent

Per QUALITY_GATE.md:121-126 the only current known exception is `e2e/program-backup.spec.ts:79` (DB-pollution flake), and that spec is not in the nine, so nothing is waivable. `nav-dropdown.spec.ts` **is** in the nine and is explicitly no longer a known red as of 2026-06-11 — "failures there should block navbar/theme changes." Say so, because "differenced against step 3" could otherwise be used to wave through a nav-dropdown red that was already red locally. (My charter's stale list still names `nav-dropdown.spec.ts:117`; QUALITY_GATE supersedes it.)

### F10 — NOTE. The Stylelint gate is local discipline, not CI enforcement

`scripts/css_audit/stylelint_surfaces.mjs` covers the seven surfaces including `layout.css` (script lines 2, 60-61; same seven as `SEVEN_SURFACES` in `tests/test_css_wp4_4_a_baseline_contracts.py:46-54`) — the plan's citation is correct. But the CI job `CSS Stylelint Measurement (non-required)` (`.github/workflows/ci.yml:826-830`) is `continue-on-error: true` and measures a **different** scope (`static/css/**/*.css` + `scss/**/*.scss`) against `docs/CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json`. Say plainly that the seven-surface gate is enforced by the packet, not by CI. Outcome A's expected decrease does not move the committed WP4.1 baseline JSON, which the plan correctly holds out of scope — no drift.

### F11 — NOTE. No conftest / fixture work

No blueprint, no table, no route, no `app.py`. `tests/conftest.py` is untouched, which is also why the QUALITY_GATE.md:60 `static/css/**` routing governs instead of the `/verify-suite` cross-cutting fallback. Correct as planned.

### F12 — NOTE. A2's arithmetic: I can confirm the complements, not the sentinel figure

The published 4/5/4 width split over 13 widths reproduces the complements exactly (108+48 = 96+60 = 108+48 = 156), and `known-live 312 = 2 × 156`, `known-dead 156 = 1 × 156` both check. `1560` is `156 × 10`, but which ten records per context set that is (nine candidate rules plus one control? three hosts across some other axis?) is not derivable from the plan. A2 flags this honestly; the packet must publish the decomposition, not just the total.

---

## What is sound — stated plainly

- **Planning size and gate derivation.** Large is correct (QUALITY_GATE.md plan-stage routing row 3 plus the trailing clause of the `static/css/**` row). Full pytest, the nine Chromium specs, seven-surface Stylelint and the Linux deep gate are transcribed correctly from QUALITY_GATE.md:32.
- **The Linux ledger departure (step 13)** is explicitly authorized by the 2026-08-04 caveat at QUALITY_GATE.md:39 and is correctly cited rather than asserted.
- **`/build-css` correctly excluded.** `scss/**` untouched, `bootstrap.custom.min.css` not regenerated.
- **Test-inventory obligation correctly classified as mandatory and required.** The plan is right and `.claude/rules/testing.md:22` (which still calls the job "non-required") is the stale document.
- **A7's precision on the blind-spot register** — noting that `display` is *not* in it, so the register is not the reason the pixel matrix is uninformative — is a real catch and pre-empts a bad citation.
- **The known-live control fix is verified.** `static/js/table-responsiveness.js:112` (`controls.className = 'tbl-controls'`) and `:239` (`toggle.className = 'tbl-view-mode-toggle'`) do create both at runtime, so the `.tbl-wrap` → `.tbl-controls`/`.tbl-view-mode-toggle` correction is substantive, not cosmetic.
- **W1/W2/W3** are accurate against `tests/test_css_wp4_4_layout_contracts.py:87-94` and `:195-206`.
- **C1 and C5** are both genuinely stronger than the count pin and cleanly red-path provable as specified. C3's premise is verified clean.
- **DR-1** is pre-committed, all-or-nothing, and has before-and-after control symmetry. That is the right shape.

---

## Coverage gaps

- `static/css/layout.css:1594-1634` (delete-or-no-op) — pixel coverage on the plan/log **table** surface exists only in `e2e/visual-baseline-thumbnails.spec.ts`, which the plan does not run locally (F3).
- `static/css/layout.css` computed-style table coverage — `e2e/visual-field-separator.spec.ts` exists and is not in the gate list (F4).
- `tests/test_css_wp4_4_layout_contracts.py` C2 positive branch — no proposed case exercises it under outcome A (F2). Needs a restore-all-nine green proof or a scope-honest downgrade.
- No new test **file** is required. All five contracts belong in the existing packet-owned file, and A4's reasoning for editing it rather than adding a sibling is correct.

## Conftest / fixture work

None. No blueprint, no table, no `erase_data()` impact.

## Verdict

**Full shared-surface CSS gate required** — not Targeted, not the `/verify-suite` fallback. The plan's derived gate set is *nearly* complete and is honestly reasoned about the visual blocker, but it is **not yet mergeable as specified**: F1 and F7 make two contracts red-by-construction under outcome B, F2 leaves C2's "strictly stronger" claim unproven under outcome A, and F3 omits a visual spec the plan's own deep gate executes. F1–F3 must be dispositioned in Plan v2 before Gate 1; F4–F7 should be. The verdict rests on measurement, and on that the method is sound.

### product-risk-reviewer (agent `a7788ede81f30d751`)

## Ruling on the question routed to me (Assumption A3)

I verified both halves of A3 independently. **The premise is right; the conclusion is wrong.**

**Premise — verified true, and stronger than the plan states.** `D:/development/Hypertrophy-Toolbox-v3-tblhelpers/static/css/bootstrap.custom.min.css` contains **zero** `.d-` selectors. This is structural, not incidental: `D:/development/Hypertrophy-Toolbox-v3-tblhelpers/scss/custom-bootstrap.scss:34` imports `bootstrap/scss/utilities` (the utility *map* definitions) but never `bootstrap/scss/utilities/api`, which is the partial that actually emits utility classes. No `/build-css` run can reintroduce `.d-*` without an SCSS edit. A3 proved this by grep; the SCSS cause makes it durable.

**Conclusion — refuted.** The `.tbl-show-*` / `.tbl-hide-*` family is **not** "the only responsive show/hide utility family in the local CSS." The live one sits 300 lines above it in the same file:

- `D:/development/Hypertrophy-Toolbox-v3-tblhelpers/static/css/layout.css:1218–1306` — `.col--high` / `.col--med` / `.col--low` progressive column disclosure: container queries at 1200px/992px, media-query fallbacks at 1366px/1200px, zoom-detection variants at 1440px+1.1dppx and 1200px+1.25dppx.
- `layout.css:1312+` — row-card mode at ≤576px container width (`.tbl--responsive` switches `display` on table/thead/tbody/tr).
- `layout.css:1569–1575` — print override re-showing `.col--low` / `.col--med`.
- `D:/development/Hypertrophy-Toolbox-v3-tblhelpers/static/js/table-responsiveness.js` — ResizeObserver-driven card/table view-mode toggle (`.tbl-view-mode-toggle`, `.tbl-controls`).

This family is live, exercised (`templates/volume_splitter.html:94–97` applies `col--high`), and covers the same domain the nine helpers were written for — table content at breakpoints. **Deleting the nine removes no capability.** I approve outcome A on the capability question; it is not a product risk and not a future-maintenance risk.

---

## Findings

**1. Assumption A3 (line 155) — the "only responsive show/hide utility family" claim is false and would be written into a durable evidence document.**
  Invariant at risk: the packet's own P8/P7 deliverable — "a **true** record" (Plan v1 goal, line 180; P7, line 383). This packet exists precisely because a closed packet's evidence file asserts something untrue.
  Risk: `docs/css_table_helpers_cleanup/EVIDENCE.md` ships a false capability claim. A future maintainer reading "we removed the only responsive show/hide family" reintroduces a redundant utility system that duplicates `.col--*`, or blocks a legitimate cleanup on a phantom gap. This is the exact failure mode the packet is repairing one file over.
  Fix: replace A3's conclusion with the measured facts — `.col--high/.col--med/.col--low` at `layout.css:1218–1306`, row-card mode at `layout.css:1312+`, print restore at `layout.css:1569–1575`, and the JS view-mode toggle — and state the trade-off as "no responsive capability is lost," not "acceptable loss."

**2. Assumption A3 (line 155) — the CDN clause is load-bearing in the argument and should not be.**
  Invariant at risk: CLAUDE.md §1 "local-first… runs on `localhost:5000`."
  Risk: A3 reasons that `.d-*` utilities "would only appear via the CDN fallback on `templates/base.html:15`, which is an error path." For a local-first app that may run offline, a `cdn.jsdelivr.net` fallback is not a capability source at all — treating it as a degraded-but-present one is wrong in the wrong direction. (The fallback and the unconditional Google Fonts load at `base.html:11–13` are pre-existing and **not** a non-goals violation — no user data leaves the machine — so nothing here blocks the packet.)
  Fix: delete the CDN clause from A3's reasoning; it does not affect the A/B decision either way, because Bootstrap never defines `.tbl-*`.

**3. Assumption A3 (line 155) — the grep that produced A3 walked past a live `.d-none` defect in the Distribute workflow.**
  Invariant at risk: CLAUDE.md §1 "Core workflows" #5 Distribute (`/volume_splitter`).
  Risk: `templates/volume_splitter.html:85` and `:114` carry `class="results-section d-none"` / `class="ai-suggestions-section d-none"`, toggled by `static/js/modules/volume-splitter.js:151,169,332,346,848,849`. No local bundle defines a general `.d-none` — the only definition is `#error-message-container.d-none` at `static/css/a11y.css:565`. `.results-section` has no `display` default (`static/css/pages-volume-splitter.css:159`; `static/css/components.css:4286`) and its parent `.volume-insights-panel` is `display: grid` (`pages-volume-splitter.css:837–840`) with per-child border/background/padding (`:678–686`). So on page load, before any split is calculated, the user sees a bordered "Distribution" card containing an empty table plus live **Export Volume Plan** and **Save &amp; Activate** buttons, and an empty "AI Suggestions" card. The gates cannot catch it: `e2e/volume-splitter.spec.ts:148` asserts `toHaveClass(/d-none/)` — class-token presence, never visibility — and `tests/test_css_cascade_contracts.py:494–495` pins the literal markup `class="results-section d-none"` as a hook that must stay intact. Both are green while the class does nothing.
  Fix: record it in A3 as a named follow-up packet and do **not** fold it in — the owner forbade `templates/**` and `static/js/**` edits, and `test_css_cascade_contracts.py` is run-always/edit-never here; folding it in would be the scope expansion the plan's own fallback table forbids.
  *(The sibling `d-none d-lg-inline` usage at `base.html:213,219` is materially less severe: `static/css/navbar.css:1234–1236` and `:1256–1258` already hide those labels with bespoke `!important` rules in the 992–1600px and 1360–1500px bands, and below 992px the navbar is collapsed. Cosmetic residue only — and its existence is itself evidence someone already patched around the missing `.d-*`.)*

**4. Preservation invariant P7 (line 383) vs Assumption A6 (line 158) — P7 is unsatisfiable as written.**
  Invariant at risk: CLAUDE.md §1 "Refactor invariant" — the packet's deliverable is a true record; an invariant that cannot pass is not an invariant.
  Risk: P7 says "No contract, comment or **document in the tree** asserts the refuted 'inherently blind' rationale after this packet, under either outcome." A6 deliberately leaves `docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md` byte-unchanged, and that file at lines 190–192 states verbatim: "**No control element can distinguish them**: that is an inherent limit, not a fixable probe defect". The packet therefore fails its own P7 by construction, and the implementer must either break A6 (unauthorized doc edit) or record P7 as failed.
  Fix: rescope P7 to "no *active* contract, comment or current-state document" and explicitly exempt closed historical evidence files, naming `_E_LAYOUT_` §4a/§10 as the known exemption with the new evidence document as its supersession pointer.

---

## What is sound — stated plainly, not padded

- **Calculation surface (lines 120–128): correctly declared `none`, and the declaration is structural, not asserted.** No file under `utils/**`, `routes/**` or `static/js/**` is opened; the nine rules are `display`-only CSS at census 0. `calculate_effective_sets()`, `calculate_weekly_summary()`, `calculate_session_summary()`, the progression suggester and the fatigue calculators are untouched by construction. Substituting a per-rule computed-style differential for the "worked before/after example" obligation is the right analogue for a CSS packet, and line 125 gives a concrete one. Nothing to flag.
- **"Effective sets are informational only" (`utils/effective_sets.py:6-7`): untouched.** Nothing here gates UI on Effective vs Raw, auto-adjusts, or blocks input.
- **Non-goals: clean.** No accounts, no auth, no cloud sync, no remote DB, no telemetry — introduced or implied.
- **Terminology: no drift.** The packet ships no user-facing copy. RIR, RPE, Effective/Raw sets, `CountingMode`, `ContributionMode`, Routine, Movement pattern and Superset are all untouched. The two comments slated for deletion are internal.
- **Workflow disruption: none, and it is proven rather than asserted.** No navigation, layout or workflow-ownership change. DR-1(b) requires census 0 across the full rendered-route set (not just the two synthetic routes) — the narrow-measurement / wide-census split in A8 is the correct call, and I endorse it.
- **Accessibility risk: correctly bounded.** At census 0 no element carries a candidate class, so no focus order, landmark or AT-tree change is reachable. P1 naming `accessibility.spec.ts` specifically is right.
- **Responsive-behaviour risk from the deletion itself: nil.** Verified independently: `tbl-show` / `tbl-hide` appear **only** in `static/css/layout.css` (9 occurrences), two test files and docs — zero in `templates/**`, `static/js/**`, `e2e/**`. C3's and C4's premises hold today.
- **Backup contract: not engaged.** No DB schema change; `program_backup` / `auto_backup` unaffected. P2 covers it.
- **Parked workstreams: correctly respected.** `fatigue` and `fatigue-stage4-smokes` are run as gates only, nothing in the fatigue surface is edited, and the plan correctly declines P3/`theme-dark.css` work per the terminated-at-a0 ruling. No quiet resumption.
- **Migration notes (line 126): satisfied ahead of requirement.** The PR description is committed to the outcome, the member-by-member DR-1 verdict, the evidence link, and `TEST_INVENTORY.{md,json}` regeneration.
- **DR-1 pre-commitment and the all-or-nothing rule are the strongest part of this plan.** Fixing the decision rule before evidence exists, and making C2 outcome-independent so indivisibility survives past this packet, are both correct.

None of my findings change the A/B decision, and none touch a calculation or a non-goal. All four are corrections to the *record* the packet will leave behind — which is this packet's stated primary deliverable.

**Verdict: Needs revision** (findings 1, 2 and 4 must be dispositioned before Gate 1; finding 3 must be recorded as a named follow-up, not absorbed).

---

## Response matrix

Every finding gets a row — **26 findings, 26 dispositions**. "Defer" carries a one-line reason and a commitment to a `MASTER_HANDOVER.local.md` note at implementation time (this `product-manager` writes only `PLANNING.md`, so it cannot write that file now).

**Verdicts received**: architecture-reviewer *Needs revision* (1–5 design-level); test-strategist *Not yet mergeable as specified* (F1–F3 blocking, F4–F7 should-fix); product-risk-reviewer *Needs revision* (1, 2, 4 blocking; 3 record-only). **All three blocking sets are dispositioned below.**

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| **1.** P7 is unsatisfiable — four unwritten documents keep the refuted rationale (`_E_LAYOUT_:190`, `ACTIVE_DEVELOPMENT.md:275`, `MASTER_HANDOVER.md:1781`, `REFACTOR_PLAN.md:1412`) | architecture-reviewer | **accept** | P7 rescoped to *"no file this packet writes"*. New §"Named deferrals" **D-1** lists all four documents by path and line as knowingly left stating a refuted rationale, with the new evidence document as the supersession pointer. Merged with product-risk #4. |
| **2.** `MASTER_HANDOVER.md` / `ACTIVE_DEVELOPMENT.md` carry a live "do not act" directive and are coordinated shared paths, neither claimed nor deferred | architecture-reviewer | **defer — with rationale, and escalated at Gate 1** | Reason: the packet's artifact table is closed by the owner ("write no other file"), and the owner's standing instruction for this packet — relayed by the manager — is *"Do not edit shared status documents. Use the local handover file."* Both grounds point the same way, so the packet does not write them. Recorded as **D-2** and as Gate-1 owner decision **OD-1** (option: a separate docs packet), plus a `MASTER_HANDOVER.local.md` note at implementation time. Not taken on packet authority. |
| **3.** C4 is red on arrival under outcome B; C5 would be too if globbed (five whitespace-only `@media` blocks already exist at `pages-workout-log.css:459,464,469,496,501`) | architecture-reviewer | **accept — with one departure** | C4 becomes *"no bundle **other than** `layout.css`"* under **both** outcomes. C5 stays `layout.css`-scoped. **Departure**: the proposed outcome-A-only tightening to "no bundle at all" is **not** adopted — see §"Where Plan v2 departs from the proposed dispositions", D-A. |
| **4.** C3 must not extend `DELETED_CLASSES` — three tests consume it and two would red on arrival under outcome B | architecture-reviewer | **accept** | New module-level `BREAKPOINT_HELPER_CLASSES` tuple, consumed **only** by C1–C5. `DELETED_CLASSES` and `FULLY_REMOVED_CLASSES` are untouched. The widened detector applies to the **new test only**; widening the shared detector over WP4.4-e's twelve classes is declined as scope expansion. The reviewer's verification is recorded: the only `static/js/**` hit is `toolbarSel = '[data-tbl-toolbar]'` at `table-responsiveness.js:363`, an attribute selector, not a class application. |
| **5.** DR-1 (c)/(e) can be satisfied **vacuously** — nothing requires the measured denominator to be non-zero or to match | architecture-reviewer | **accept — highest-value finding in the council** | New **DR-1(h)**: every rule's measured applicable-record count must be non-zero **and** equal its published denominator. Denominators are now the measured ones (594 / 528 / 594 / 264 / 264 / 330 / 330 / 264 / 264 against an 858 universe). Any deviation is recorded and re-derived, **never** repaired by moving a width. |
| **6.** Deletion range excludes the comments it claims to delete; stranded `LOADING STATE` banner | architecture-reviewer | **accept** | Atomic unit restated as **`layout.css:1589–1634`**. The already-empty `LOADING STATE` banner at `:1584–1586` is **deliberately left** and the reason is stated: it is not part of this family, WP4.4-e emptied it, and removing it is an unproven separate cleanup. Corrected inline in Plan v1 in three places. |
| **7.** C3's red paths require edits to trees the plan forbids absolutely | architecture-reviewer | **accept** | Plan v2 permits **transient, never-committed** red-path edits under `templates/**` and `static/js/**`, each reverted immediately, with cleanliness proven by the `git status --porcelain` + `git ls-files --others --exclude-standard` step. AC7 is read as a statement about the **committed** diff. |
| **8.** Two factual errors — "four separator-contrast tests" (it is two) and the pin regex (it has `re.escape`) | architecture-reviewer | **accept** | Both corrected inline in Plan v1 and restated in Plan v2. |
| **9.** Four further test files read `layout.css` and are unnamed | architecture-reviewer | **accept** | All six recorded in Plan v2 §"Coupling inventory", each with the reviewer's per-file reason for being unaffected by a nine-rule deletion. |
| **10.** N7 over-counts — only the two JSON baselines are pytest-asserted | architecture-reviewer | **accept** | N7 now cited only for `tests/test_css_cascade_contracts.py:161` and `tests/test_css_wp4_4_a_baseline_contracts.py:34`. The evidence-doc placement decision stands on the narrower, true justification. Corrected inline at A6 and at the artifact table. |
| **F1.** C4 red-by-construction under outcome B (BLOCKING) | test-strategist | **accept** | Same fix as architecture #3. C4 excludes `layout.css` by name; C1 owns the `layout.css`-side statement. |
| **F2.** Under outcome A, C2 has no independent red path and its positive branch is never exercised (BLOCKING) | test-strategist | **accept — option (a), the two-sided proof** | Plan v2 requires a **restore-all-nine** proof demonstrating C2 **green** while C1 is **red**. That is the only evidence C2's positive branch means anything. If that proof cannot be produced, C2's claim is **downgraded honestly** to "load-bearing under outcome B only" rather than keeping an unproven "strictly stronger" label. The W1/W2/W3 defence is re-argued accordingly. |
| **F3.** Gate list omits `e2e/visual-baseline-thumbnails.spec.ts`, which the plan's own deep gate runs (BLOCKING) | test-strategist | **accept** | Added to the gate list. **66 + 18 = 84** now reconciles the deep-gate denominator against the three same-SHA runs measured on `main` @ `ac2923b`. The pre-declared known-unstable classification set is extended to cover thumbnail captures, so a thumbnails red has a classification instead of defaulting to a V1 rollback trigger. |
| **F4.** `e2e/visual-field-separator.spec.ts` — the one deterministic computed-style oracle over `layout.css` — is absent | test-strategist | **accept** | Added (42 tests, no pixel baseline, cross-OS stable). Adding a spec strengthens the gate, so no owner exception is needed. Its pytest twin `tests/test_css_field_separator_contracts.py` is recorded in the coupling inventory. |
| **F5.** Windows visual matrix has no repeat policy — the single-sample trap the plan correctly refuses on Linux | test-strategist | **accept** | Windows pre-change matrix runs **three times** at the base commit; the per-capture stable/unstable partition is published as a **pre-declared** list before any change; only post-change reds **outside** that partition are signal. No `--update-snapshots` at any point; `e2e/__screenshots__/**` is never a write target. **⟢ Executed differently — see the F5 addendum immediately below. F5's intent (three samples, a pre-declared partition, committed tree never written) is fully satisfied; its literal method was not usable and the reason is itself a finding.** |

> **⟢ F5 addendum — recorded 2026-08-04, after execution. F5's literal method is not merely uninformative on Windows, it is not read-only.**
>
> The disposition above assumed the Windows matrix could be *compared* three times against the committed `win32` baselines. It cannot, for two measured reasons:
>
> 1. **`e2e/__screenshots__/win32` is incomplete, not just stale.** It holds **66** `visual.spec.ts` baselines against linux's **68**: PR #281 regenerated only the linux half of the segmented `user-profile-mobile-{dark,light}` captures, and `docs/visual_determinism/PLANNING.md` §5/§7 records the Windows half as an open owner-local follow-up.
> 2. **A missing baseline is *written*, not failed.** Playwright creates an absent snapshot even without `--update-snapshots`. A single compare run against the committed tree left **four untracked PNGs** in `e2e/__screenshots__/win32/visual.spec.ts-snapshots/` — `user-profile-mobile-{dark,light}-segment-{1,2}.png`. They were moved to the gitignored `artifacts/tblhelpers/stray_win32_segments/` and the tree verified clean (`git status --porcelain e2e/__screenshots__` empty; win32 back to 66 PNGs). Nothing was deleted.
>
> **Anyone running this gate on Windows must check for those four files afterwards.** Running the committed-baseline compare as a "read-only gate" silently stages an unreviewed baseline addition.
>
> **Method actually used**, which is the one `docs/visual_determinism/PLANNING.md` §6 records as safe: a scratch config (`artifacts/tblhelpers/pw-scratch.config.ts`) that changes **only** `snapshotPathTemplate`, `testDir`, `outputDir` and the webServer command's path anchoring — inheriting viewport, the deterministic Chromium args, the seeded DB, workers, serial ordering, `maxDiffPixels` and `threshold` unchanged — resolving snapshots under gitignored `artifacts/`. One generate run plus **two** compare runs pre-change, all three at base `ac2923b`.
>
> **Result — 84 passed / 84 on every one of the three runs, 86 images.** (84 tests → 86 images: the two segmented user-profile mobile captures emit two images each.) The committed tree was untouched by all three (`git status --porcelain e2e/__screenshots__` empty after each).
>
> **The pre-declared unstable partition on this host is therefore EMPTY.** That is a stronger position than F5 anticipated and it *raises* the bar: with no capture excused in advance, **any** post-change red is signal and none can be waved through as known instability. It says nothing about the Linux runner, whose measured coin-flip behaviour is unchanged and still governs the deep gate.
| **F6.** `Test Inventory Drift` risk if C1/C4 are parametrized over a glob | test-strategist | **accept** | C1 and C4 are **single tests** looping `sorted(...)` and reporting all offenders — never `@pytest.mark.parametrize` over a glob — so the collected node count cannot vary with the files present on the collecting machine. |
| **F7.** C3's "add the six names" is ambiguous; one reading is red-by-construction | test-strategist | **accept** | Same fix as architecture #4: `BREAKPOINT_HELPER_CLASSES`, new test only. |
| **F8.** Unnamed existing coverage, two items of which enforce the plan's own invariants | test-strategist | **accept** | `tests/test_css_wp4_4_a_baseline_contracts.py:39–44` (`EXPECTED_SNAPSHOT_COUNTS`, `win32` 66/18 · `linux` 68/18) is now cited as the **mechanical P3 gate**, stronger than the `git diff` check P3 leaned on. `:61` compares line counts against the baseline's own `sourceCommit` via `git show`, not the working tree — so outcome A's deletion does **not** red it, and that is recorded so no reviewer mistakes it for a blocker. |
| **F9.** Known-red awareness absent | test-strategist | **accept** | Plan v2 states: the only known exception is `e2e/program-backup.spec.ts:79`, which is **not** in the gate set, so nothing is waivable; and `nav-dropdown.spec.ts` is **no longer** a known red — a red there blocks and may not be waved through as "already red locally". |
| **F10.** The Stylelint gate is packet discipline, not CI enforcement | test-strategist | **accept** | Stated plainly: `CSS Stylelint Measurement (non-required)` is `continue-on-error: true` and measures a different scope against the WP4.1 baseline JSON, which this packet holds out of scope and does not move. The seven-surface gate is enforced by the packet. |
| **F11.** No conftest / fixture work | test-strategist | **accept (note)** | Recorded: `tests/conftest.py` untouched, which is also why the `static/css/**` routing governs rather than the `/verify-suite` cross-cutting fallback. |
| **F12.** A2's sentinel decomposition is not derivable from the plan | test-strategist | **accept — resolved, with one residual** | Resolved by the executed run: 3 hosts × 10 elements = 30 per context; 286 × 30 = **8,580** sentinel records; the spike's `1560` was `52 × 30`. One decomposition remains unpublished — the same-CSS control's **30,316** compared records (106 per context) — carried as residual obligation **R1**. |
| **1.** A3's conclusion is false — `.col--high/med/low` + row-card mode + print restore + the JS toggle are the live responsive-disclosure system | product-risk-reviewer | **accept — and it strengthens the case for outcome A** | A3 corrected inline: premise verified and made durable (`scss/custom-bootstrap.scss:34` imports `utilities` but never `utilities/api`, so no `/build-css` can emit `.d-*`); conclusion replaced with the measured facts. The trade-off is now stated as **"no responsive capability is lost"**, not "acceptable loss". |
| **2.** The CDN clause is load-bearing and should not be | product-risk-reviewer | **accept** | Clause withdrawn from A3's reasoning. Treating a `cdn.jsdelivr.net` fallback as a degraded-but-present capability source is wrong in the wrong direction for a local-first app; it was never load-bearing, since Bootstrap defines no `.tbl-*` under any load path. |
| **3.** The A3 grep walked past a live `.d-none` defect in the Distribute workflow | product-risk-reviewer | **accept as a NAMED FOLLOW-UP — explicitly not absorbed** | Recorded as **FU-2** with the reviewer's runtime evidence, verified in this worktree before any change at 1440×900 on `/volume_splitter`: `.results-section d-none` computes `display: block` at 461×144 visible; `.ai-suggestions-section d-none` computes `display: block` at 461×70 visible; `[...document.styleSheets]` contains **no** rule whose `selectorText === '.d-none'`; `#error-message-container` is hidden only by its own inline `style="display: none !important;"` at `base.html:271`. Not folded in — `templates/**` and `static/js/**` are forbidden and `tests/test_css_cascade_contracts.py` is run-always/edit-never. **Elevated** to Gate-1 owner decision **OD-2** — see the departures section. |
| **4.** P7 unsatisfiable (independent confirmation) | product-risk-reviewer | **accept** | Merged with architecture #1 into the P7 rescope and deferral **D-1**. |

---

## Plan v2

**Goal**: unchanged from v1 — establish by fresh measurement with validated controls whether all nine `.tbl-show-*` / `.tbl-hide-*` rules are certifiably unreachable and unobservable, then delete all nine atomically or retain all nine, leaving the repository holding a **true** justification and a **stronger** contract than the refuted occurrence-count pin.

**What changed.** The decomposition, DR-1's pre-commitment and all-or-nothing shape, the indivisibility rule, the conservative-fallback table and the refusal to treat pixels as candidate evidence all survived review — all three reviewers endorsed them by name. What did not survive: one preservation invariant that could not pass, two contracts that were red-by-construction under outcome B, one contract whose "stronger" claim was unproven under outcome A, a missing visual spec, a missing deterministic spec, a single-sample Windows policy, a wrong deletion range, two factual errors about the file being edited, and one product claim that was simply false. Plus: **the evidence run has since executed**, so four of DR-1's criteria are now measured rather than projected.

### §0 Factual corrections carried into v2

Each is also marked inline at its original location in Section 0 / Plan v1, so the superseded claim and its correction both survive.

| Was (v1) | Is (v2) | Source |
|---|---|---|
| Deletion range `layout.css:1594–1634` | **`1589–1634`** — `:1594` is `.tbl-show-sm {`; the banner is `:1589–1591` and the inline comment `:1593`. The empty `LOADING STATE` banner at `:1584–1586` is **deliberately left** | architecture #6 |
| Widths `360, 480, 819, 820 / 821, 900, 1024, 1199, 1200 / 1201, 1202, 1440, 1920` | **`375, 600, 819, 820, 821, 822, 1000, 1199, 1200, 1201, 1202, 1440, 1920`** — same 4/5/4 split, one extra boundary probe (`822`). Nominal width matched the measured band at all 13 | measured run |
| Per-rule universe 156 (2 routes) | **858** (3 hosts × **11 routes** × 2 themes × 13 widths); 286 contexts | measured run |
| Denominators 108/96/108/48/48/60/60/48/48 | **594 / 528 / 594 / 264 / 264 / 330 / 330 / 264 / 264**; complements exact at 858 | measured run; architecture #5 |
| Sentinel `1560 = 156 × 10`, undecomposed | **8,580 = 286 contexts × 30 elements** (3 hosts × [1 control + 6 candidates + 2 known-live + 1 known-dead]); the spike's `1560` was `52 × 30` | measured run; F12 |
| "the four separator-contrast tests" | **two** collected tests — one function at `:379–419` parametrized light/dark | architecture #8 |
| Pin regex `rf"\.{cls}(?![\w-])"` | **`rf"\.{re.escape(cls)}(?![\w-])"`** at `:198` | architecture #8 |
| N7 lists `_E_LAYOUT_` among six pytest-asserted docs | N7 **over-counts**; only the two JSON baselines are asserted (`test_css_cascade_contracts.py:161`, `test_css_wp4_4_a_baseline_contracts.py:34`) | architecture #10 |
| A3: the nine are the only responsive show/hide family; deletion is an "acceptable loss" | **False.** `.col--high/.col--med/.col--low` (`layout.css:1218–1306`), row-card mode (`:1312+`), the print restore (`:1569–1575`) and the JS view-mode toggle are the live system. **No responsive capability is lost** | product-risk #1 |
| A3: `.d-*` would appear via the CDN fallback | **Withdrawn.** `scss/custom-bootstrap.scss:34` imports `bootstrap/scss/utilities` but never `utilities/api`, so no `/build-css` can emit `.d-*`; and a CDN fallback is not a capability source for a local-first app | product-risk #2 |
| Visual gate = `visual.spec.ts` (66) | **66 + `visual-baseline-thumbnails.spec.ts` (18) = 84**, reconciling the deep-gate denominator; plus `visual-field-separator.spec.ts` (42) | F3, F4 |
| P7 "no document **in the tree**" | Rescoped to **"no file this packet writes"**, with four documents named as deferral **D-1** | architecture #1, product-risk #4 |

### Measured results — DR-1 status at Gate 1

The full evidence run has executed on the **unmodified** tree at base `ac2923b`. **Four of DR-1's criteria are PASS for all nine members. Three remain unmeasured because they require the deletion, which is Gate-1-gated.**

**Oracle before-sweep — 11 routes × 2 themes × 13 widths = 286 contexts, 3 hosts, applicability read from measured `matchMedia` in every context.**

| Rule | distinguished | structural owner OK | observed value | control values (inline / list-item / table-cell) |
|---|---|---|---|---|
| `base-show-sm` | **594 / 594** | 594 / 594 | `none` | 198 / 198 / 198 |
| `base-show-md` | **528 / 528** | 528 / 528 | `none` | 176 / 176 / 176 |
| `base-show-lg` | **594 / 594** | 594 / 594 | `none` | 198 / 198 / 198 |
| `sm-hide` | **264 / 264** | 264 / 264 | `none` | 88 / 88 / 88 |
| `sm-show` | **264 / 264** | 264 / 264 | **`block`** | 88 / 88 / 88 |
| `md-hide` | **330 / 330** | 330 / 330 | `none` | 110 / 110 / 110 |
| `md-show` | **330 / 330** | 330 / 330 | **`block`** | 110 / 110 / 110 |
| `lg-hide` | **264 / 264** | 264 / 264 | `none` | 88 / 88 / 88 |
| `lg-show` | **264 / 264** | 264 / 264 | **`block`** | 88 / 88 / 88 |

**The three `display: block` rows are the WP4.4-e refutation, measured.** `sm-show`, `md-show` and `lg-show` are the three members that packet declared indistinguishable "as an inherent limit, not a fixable probe defect". Each is distinguished in **100%** of its applicable contexts against hosts whose UA initial `display` is `inline`, `list-item` and `table-cell`. The limit was the probe host, not the rules.

**Controls, before-run:**

| Control | Result |
|---|---|
| Sentinel took effect | **8,580 / 8,580** |
| Sentinel reverted cleanly | **8,580 / 8,580** |
| Known-live (`.tbl-controls`, `.tbl-view-mode-toggle`) | **1,716 / 1,716** |
| Known-dead | **858 / 858** |
| Control-baseline validation (control at its UA initial **and** no author `display` rule matching it) | **858 / 858** |
| Full-selector census, all six candidates, taken before injection | **0** in all 286 contexts |
| Positive census control | `.tbl-wrap` **338**, `.tbl` **338**, `.tbl-controls` **26**, `.tbl-view-mode-toggle` **26** |
| Same-CSS control (M5) — two full independent runs on identical CSS | **0 differing records / 30,316 compared** across 286 contexts — **PASS** |

**Stylesheet enumeration.** No foreign stylesheet defines any candidate class. Exactly two cross-origin sheets are unreadable from CSSOM, and **both were accounted for out-of-band by fetching them**: Google Fonts (4 `@font-face` rules, 0 class selectors) and jsdelivr flatpickr on `/progression` (16,166 bytes, 0 `tbl` tokens, every selector flatpickr-namespaced). **FontAwesome is now vendored locally** at `static/vendor/fontawesome/`, so it is readable and was scanned — the `.sr-only` CDN blind spot that caught WP4.4-e **does not recur**.

**Static inventory (DR-1(a)) — PASS.** Sole definition site is `static/css/layout.css`. Zero application sites in `templates/**`, `static/js/**`, `routes/**`, `utils/**`. No dynamic construction: the only `tbl-` string literals in `static/js/**` are `tbl-controls`, `tbl-view-mode-toggle`, `tbl--view-simple`, `tbl--view-advanced`. No `build/`, `dist/`, `out/` or `.next/` tree exists.

**Pre-change gate baselines at `ac2923b`.** Full pytest **2,523 passed / 2 skipped** (447.96s). Seven-surface Stylelint **2,759**; `layout.css` **92**, across four categories — `declaration-no-important` 28, `declaration-property-value-disallowed-list` 54, `no-descending-specificity` 9, `no-duplicate-selectors` 1.

| DR-1 criterion | Status |
|---|---|
| **(a)** static inventory | **PASS**, all nine |
| **(b)** runtime census 0 + positive census control | **PASS**, all nine |
| **(c)** before-state positive effect | **PASS**, all nine, 100% of applicable contexts |
| **(d)** structural declaration ownership | **PASS**, all nine, 100% of applicable contexts |
| **(h)** *(new)* non-zero denominator equal to published | **PASS**, all nine — the table above *is* the published denominator set |
| **(e)** post-deletion flip | **not yet measured** — requires the deletion |
| **(f-before)** controls, before-run | **PASS** |
| **(f-after)** controls, after-run | **not yet measured** |
| **(g)** rest-state differential, before vs after | **not yet measured** |

**Nothing is certified yet.** Outcome A remains unselected until (e), (f-after) and (g) are measured after Gate 1. The evidence to date is necessary, not sufficient, and DR-1 is unchanged in its all-or-nothing form.

### DR-1 — carried forward, with criterion (h)

(a)–(g) are unchanged from Plan v1. Added:

| # | Criterion |
|---|---|
| **(h)** | **Non-vacuity.** Every rule's measured applicable-record count must be **non-zero** and must **equal its published denominator**: `base-show-sm` 594, `base-show-md` 528, `base-show-lg` 594, `sm-hide` 264, `sm-show` 264, `md-hide` 330, `md-show` 330, `lg-hide` 264, `lg-show` 264 — against a per-rule universe of 858 (3 hosts × 286 contexts), with the band complements 594+264 = 528+330 = 594+264 = 858 holding exactly. Any deviation is **recorded and re-derived, never repaired by moving a width.** |

Rationale, in the reviewer's words: without (h), criteria (c) and (e) are satisfiable on **zero records** — the inverse of `verification.md`'s "a probe that changes nothing proves nothing", in a packet whose entire premise is that the previous packet mis-measured. **If any single one of (a)–(h) fails for any single member, outcome B is selected for the whole family.**

### Scope

- **In**: unchanged from v1, with the deletion unit corrected to `layout.css:1589–1634` and the `LOADING STATE` banner at `:1584–1586` explicitly excluded. Additionally in scope: **transient, never-committed** red-path edits under `templates/**` and `static/js/**`, reverted immediately and proven clean.
- **Out**: unchanged from v1, plus the four narrowings the matrix records — `docs/MASTER_HANDOVER.md` and `docs/ACTIVE_DEVELOPMENT.md` (**D-2**), the `.d-none` Distribute defect (**FU-2**), widening the shared `DELETED_CLASSES` detector (architecture #4), and the outcome-A tightening of C4 (departure D-A).

### Artifacts

| Path | Change | Notes |
|---|---|---|
| `static/css/layout.css` | **delete `1589–1634`** (outcome A) / **byte-unchanged no-op** (outcome B) | The nine rules, the three `@media` blocks in full, the `RESPONSIVE BREAKPOINT HELPERS` banner (`:1589–1591`) and the inline comment (`:1593`). The empty `LOADING STATE` banner at `:1584–1586` is **deliberately left**: it is not part of this family, WP4.4-e emptied it, and removing it is an unproven separate cleanup. Nothing else in the file changes — the print `.tbl-controls, .tbl-toolbar` rule, `.tbl-controls` (`:1423`), `.tbl-view-mode-toggle` (`:1451`), the `.col--*` disclosure family (`:1218–1306`), row-card mode (`:1312+`) and the separator block are all preserved. |
| `tests/test_css_wp4_4_layout_contracts.py` | **modify** | Outcome A: remove `DEFERRED_HELPER_COUNTS` and its assertion inside `test_retained_rules_are_still_present`; add C1–C5. Outcome B: keep both intact, add C2–C4, rewrite the refuted rationale comment. Both outcomes: new `BREAKPOINT_HELPER_CLASSES` tuple; `DELETED_CLASSES` / `FULLY_REMOVED_CLASSES` untouched; module docstring updated to point at the new evidence document. **Not weakened, not renamed, not reordered**: `RETAINED_SNIPPETS`, `test_partially_reachable_rules_kept_their_dead_branch` (`.input-frame` = 9 / `.tbl-toolbar` = 1), `test_dark_theme_table_tokens_have_a_live_definition`, `test_body_dark_mode_block_stays_deleted`, `test_layout_css_declares_no_cascade_layer`, `test_orphaned_keyframes_went_with_their_only_consumer`, `test_deleted_classes_are_not_resurrected_by_a_sibling_surface`, and the **two** separator-contrast tests. |
| `docs/css_table_helpers_cleanup/PLANNING.md` | **modify** (this file) | Section 0 + Plan v1 + council record + matrix + Plan v2. |
| `docs/css_table_helpers_cleanup/EVIDENCE.md` | **new** | Outcome; DR-1 (a)–(h) applied member by member; **every** denominator derived, including residual **R1**; raw control output; the known-live `.tbl-wrap` 0/78 defect and its fix; the measured refutation of the WP4.4-e "inherent limit"; the reproduction recipe; the gate table; preservation invariants; deferrals D-1/D-2 and follow-ups FU-1/FU-2; and — on outcome B — exactly which member failed and on which criterion. Explicitly supersedes `_E_LAYOUT_` §4a/§10. **No pytest assertion is added on its path.** |
| `docs/test_inventory/TEST_INVENTORY.md` + `.json` | **regenerate** | Mandatory under both outcomes; `Test Inventory Drift` is a required branch-protection context. |
| `artifacts/tblhelpers/**` | generated, **gitignored** (`.gitignore:57`) | Oracle, controls, raw records, before/after runs, gate logs, the three-run Windows visual partition, the council transcripts. |

Anything not in this table is not written. A strictly necessary contract-only change outside it **stops the packet** and is presented at Gate 1.

### Replacement contracts C1–C5 — corrected shapes and re-defended strength claims

Weaknesses of the pin being replaced, unchanged and confirmed accurate by the test-strategist against `:87–94` and `:195–206`: **W1** it pins a number, not a state · **W2** it pins the stylesheet, not the app · **W3** it pins one file.

| # | Contract | Corrected shape | Strength claim, re-defended |
|---|---|---|---|
| **C1** | `test_breakpoint_helper_family_is_absent_from_layout_css` | **One** test looping `sorted(BREAKPOINT_HELPER_CLASSES)` (never `parametrize`, per F6), counting **rule heads** whose selector list carries the class at any nesting depth including inside `@media`, using the file's existing length-preserving `_strip_comments` and `(?![\w-])` guard, asserting `0` and reporting **all** offenders. Outcome A only. | **Fixes W1, unchallenged.** `0` is a state, not a tally; the count pin explicitly permitted six live rules. Rule-head counting survives reformatting and names the offender. Precedent verified by the reviewer at `tests/test_css_wp4_4_components_contracts.py:305–316`, whose docstring cites the WP4.4-e `.tbl-show-sm` red path as the reason substring presence was too weak. |
| **C2** | `test_breakpoint_helper_family_is_all_or_nothing` | Count family selector occurrences **inside** the three `@media` blocks and **outside** them; assert both-empty **or** the full 3-base + 6-override shape. Fails on any partial state in either direction. | **Claim narrowed under F2 — honestly.** As written it is *subsumed* by C1 under outcome A: every partial state that reds C2 also reds C1, so C2 cannot be the sole failure. Plan v2 requires a **two-sided proof**: restore all nine and demonstrate **C2 green while C1 red**, which is the only evidence its positive branch has meaning and the only thing that makes "outcome-independent permanent indivisibility" a real claim rather than a green-looking guarantee hiding a possible `@media`-nesting mis-parse. **If that proof cannot be produced, C2's claim is downgraded in the evidence document to "load-bearing under outcome B only"** — the label shrinks, the contract stays. No unproven "strictly stronger" claim ships. |
| **C3** | `test_breakpoint_helper_classes_are_unreachable` | Scans `templates/**/*.html` and `static/js/**/*.js` for `BREAKPOINT_HELPER_CLASSES` **only**. Detector widened **for this test only**: `class="…"`, `classList.add/toggle/replace`, `className =`, `setAttribute('class', …)`, and — the important one — the literal tokens `tbl-show` / `tbl-hide` in **any** syntactic position, which catches `'tbl-show-' + size` and `` `tbl-${size}` ``. **Does not extend `DELETED_CLASSES`.** | **Fixes W2 — the largest gap, unchallenged.** The count pin could not notice a template adopting the class; this turns adoption into a pytest red and therefore into a deliberate decision. It discharges M10 permanently instead of as a one-time measurement. Premise independently verified by two reviewers: zero hits in `templates/**` and `static/js/**`. Shared-detector widening over WP4.4-e's twelve classes is **declined** as scope expansion. |
| **C4** | `test_breakpoint_helper_classes_have_no_definition_site_in_a_sibling_bundle` | **One** test (F6) globbing `static/css/*.css` **excluding `layout.css` by name**, asserting no sibling bundle defines any of the six. Identical under **both** outcomes. | **Fixes W3, and the exclusion makes it stronger, not weaker.** The old pin covered `layout.css` only; a page bundle could have defined `.tbl-show-md` tomorrow unnoticed. Excluding `layout.css` is what makes C4 outcome-independent and red-path-provable rather than red-on-arrival under outcome B — and it keeps the `layout.css` statement with C1, which asserts it by the **stronger** rule-head technique. It also converts the run's "no foreign stylesheet defines a candidate class" finding into a standing guarantee. |
| **C5** | `test_layout_css_has_no_empty_media_block` | Scoped to **`layout.css` only** — `pages-workout-log.css:459,464,469,496,501` already hold five whitespace-only `@media` blocks, so a glob-all form would be red on arrival. Outcome A only. | **A new guarantee rather than a replacement.** It forecloses the specific sloppy deletion — rules removed, three empty `@media` shells left — that would pass C1 and leave a residue later read as intentional. The count pin had no analogue. |

**Outcome B** keeps `DEFERRED_HELPER_COUNTS` and its assertion **exactly as they are**, adds C2, C3 and C4, and rewrites the `:76–94` comment to state (i) the measured refutation of "no control element can distinguish them", (ii) which member failed and on which DR-1 criterion, and (iii) that the family remains indivisible. Nothing loosens; the file merely stops asserting something untrue.

### Named deferrals and follow-ups

| # | Item | Disposition |
|---|---|---|
| **D-1** | Four documents keep the refuted "inherently blind" rationale and are **not** written by this packet: `docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md:190`, `docs/ACTIVE_DEVELOPMENT.md:275`, `docs/MASTER_HANDOVER.md:1781`, `docs/REFACTOR_PLAN.md:1412` | **Knowingly deferred.** Named by path and line in the evidence document, with the new evidence document as the supersession pointer. P7 is rescoped to the files the packet writes so the invariant can actually pass. |
| **D-2** | `docs/MASTER_HANDOVER.md:1779` and `docs/ACTIVE_DEVELOPMENT.md:274–279` carry a **live operating directive** — "Deferred by `e`, owner-gated, do not act" / "Do not erode it rule by rule" — which outcome A makes obsolete and outcome B leaves resting on a refuted reason | **Deferred, escalated at Gate 1 as OD-1.** Two independent grounds: the owner closed the artifact table ("write no other file"), and the owner's standing instruction relayed by the manager is *"Do not edit shared status documents. Use the local handover file."* `WORKSTREAM_OWNERSHIP.md:29–33` additionally classes `MASTER_HANDOVER.md` as a never-claimed coordinated path. Recorded in `MASTER_HANDOVER.local.md` at implementation time. Owner option: a separate docs packet. |
| **FU-1** | Whether `_E_LAYOUT_` should gain a `superseded-by` pointer | **Deferred** (Plan v1 A6, unchanged). Editing a closed packet's historical record to match a later finding is the wrong repair; the new document carries the supersession. |
| **FU-2** | **Live `.d-none` defect in the Distribute workflow.** `.d-none` is defined by no local bundle, so `templates/volume_splitter.html:85,114` render visible. Root cause, user impact, the runtime measurements and why two green gates cannot see it are recorded once, in [`EVIDENCE.md`](EVIDENCE.md) §10 FU-2. | **Recorded, explicitly NOT absorbed**, and elevated to Gate-1 owner decision **OD-2** (see departures). Folding it in would require `templates/**`, `static/js/**` or `scss/**` edits the owner forbade, and would be the scope expansion this plan's own fallback table prohibits. |
| **R1** | Residual denominator obligation: the same-CSS control's **30,316** compared records over 286 contexts (106 per context) is not yet decomposed | The evidence document must publish the decomposition, to the same standard the packet applied to the sentinel figure. A total without its decomposition is exactly what F12 objected to. |

### Coupling inventory — the six test files that read `layout.css`

Checked against a nine-rule deletion; **none reds**. Recorded so a later range shift is re-checked rather than assumed.

| File | Why unaffected |
|---|---|
| `tests/test_css_wp4_4_layout_contracts.py` | The packet's own target; edited deliberately. |
| `tests/test_css_cascade_contracts.py` | **Run always, edit never.** Does not reference the family. |
| `tests/test_css_wp4_4_base_contracts.py:39` | Asserts only `"animation: fadeIn" in LAYOUT` (`:131`). |
| `tests/test_css_field_separator_contracts.py:24` | Matches the separator rules by pattern (`:168–175`) — untouched by the deletion. Pytest twin of `visual-field-separator.spec.ts`. |
| `tests/test_css_wp4_4_a_baseline_contracts.py:49` | `:61` compares per-surface line counts against the baseline's **own `sourceCommit`** via `git show`, deliberately **not** the working tree (`:69–74`, `:101–106`; WP4.4-c fixed exactly this). Outcome A's ~46-line deletion therefore does **not** red it. `:39–44` `EXPECTED_SNAPSHOT_COUNTS` (`win32` 66/18, `linux` 68/18) is cited below as the mechanical P3 gate. |
| `tests/test_css_wp4_4_a11y_contracts.py:427` | Scans only `LEGACY_CLASSES`. |

### Expected gates

- **pytest**: full `tests/` suite. Packet target `tests/test_css_wp4_4_layout_contracts.py`; `tests/test_css_cascade_contracts.py` and `tests/test_visual_selector_contracts.py` run inside that total, **unedited**. Pre-change baseline **2,523 passed / 2 skipped**.
- **e2e (Chromium), eleven specs**: `smoke-navigation`, `nav-dropdown`, `accessibility`, `dark-mode`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening`, **+ `visual-field-separator` (F4)**, **+ `visual-baseline-thumbnails` (F3)**.
- **visual**: `visual.spec.ts` (66) **and** `visual-baseline-thumbnails.spec.ts` (18) with `PW_VISUAL_SEED=1`. **66 + 18 = 84**, reconciling the deep-gate denominator against the three same-SHA runs measured on `main` @ `ac2923b`. Run as gates, differenced against the pre-change partition; **never** cited as candidate-specific evidence.
- **Windows visual policy (F5)**: the matrix runs **three times** at the base commit before any change; the per-capture stable/unstable partition is published as a **pre-declared** list; only post-change reds **outside** that partition are signal. `e2e/__screenshots__/win32` is independently stale on `main` (`plan-desktop-light-advanced` at 541,849 px / 29% on a pristine tree), which is why "all green" is not available as a criterion.
- **Stylelint**: seven surfaces via `node scripts/css_audit/stylelint_surfaces.mjs`, no category may rise. Baseline **2,759** total, `layout.css` **92** (important 28 · disallowed-value 54 · descending-specificity 9 · duplicate-selectors 1). **This gate is packet discipline, not CI enforcement** (F10): `CSS Stylelint Measurement (non-required)` is `continue-on-error: true` and measures a different scope against the WP4.1 baseline JSON, which this packet holds out of scope and does not move.
- **Linux `visual-linux` deep gate**: against the **current accepted baselines** (post-PR #281 `864043f`), explicitly **not** `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` (`sourceCommit 46e340e` predates the regeneration; the departure is authorized by `QUALITY_GATE.md:39`). Reds inside the known-unstable set — `workout-plan-desktop-{dark,light}`, `plan-desktop-{dark,light}-advanced`, **plus thumbnail captures (F3)** — are attributed to the external blocker; reds outside it are a V1 rollback trigger. One green compare is *a gate that ran*, never evidence.
- **Test inventory**: regenerated and committed; `--check` clean. **Required** branch-protection context. C1 and C4 are single tests, never parametrized over a glob (F6), so the collected node count cannot vary with the collecting machine's file set.
- **Type check**: pyright measure-only, no net-new diagnostics from the new test code.
- **Known reds (F9)**: the only current exception is `e2e/program-backup.spec.ts:79`, which is **not** in the gate set — nothing is waivable. **`nav-dropdown.spec.ts` is no longer a known red**; a red there blocks and may not be waved through as "already red locally".
- **Not required**: `/build-css` — `scss/**` untouched, `bootstrap.custom.min.css` not regenerated.
- **PR #296**: no file touched, no experimental switch used.

### Preservation invariants (revised)

P1–P6 and P8 carry forward from Plan v1 unchanged. Changed:

| # | Invariant | Pass condition (v2) |
|---|---|---|
| **P3** | No rebaseline, no tolerance change | **Now mechanically gated, not promised**: `tests/test_css_wp4_4_a_baseline_contracts.py:39–44` (`EXPECTED_SNAPSHOT_COUNTS`, `win32` 66/18 · `linux` 68/18) manifests the committed screenshot trees inside the full pytest run — stronger than the `git diff --name-only` check P3 leaned on, which is retained as a second check alongside zero changes to `e2e/visual-helpers.ts` and `playwright.config.ts`. |
| **P7** | The record is true | **Rescoped** to: *no file this packet writes* asserts the refuted "inherently blind" rationale, under either outcome. The four documents it does not write are named in deferral **D-1**, with the evidence document as the supersession pointer. The v1 wording ("no document in the tree") was unsatisfiable by construction and is corrected rather than ticked falsely. |
| **P9** *(new)* | Red paths leave no residue | Every transient red-path edit under `templates/**` and `static/js/**` is reverted immediately, and `git status --porcelain` + `git ls-files --others --exclude-standard` prove the committed diff is exactly the artifact table. AC7 is read as a statement about the **committed** diff. |

### Sequence

Unchanged from Plan v1 except as below. Steps execute **only after Gate 1**.

- **Steps 1–7 are already executed** on the unmodified tree at `ac2923b` and their results are recorded above. They are re-runnable from the evidence document's reproduction recipe.
- **Step 3 amended (F3, F5)**: the Windows pre-change baseline includes `visual-baseline-thumbnails.spec.ts` and `visual-field-separator.spec.ts`, and the visual matrix runs **three times** with the stable/unstable partition published before any change.
- **Step 8 corrected (architecture #6)**: the atomic edit is `layout.css:1589–1634`; the `LOADING STATE` banner at `:1584–1586` is left.
- **Step 10 amended (F2, F6, F7, architecture #4, #7)**: contracts use `BREAKPOINT_HELPER_CLASSES`; C1 and C4 are single non-parametrized tests; C4 excludes `layout.css`; C5 is `layout.css`-scoped. Red-path proofs may make **transient, never-committed** edits under `templates/**` and `static/js/**`, each reverted immediately. **New sub-step 10A-bis**: the two-sided C2 proof — restore all nine, demonstrate C2 green while C1 red, restore the deletion. If that proof fails, downgrade C2's claim in writing.
- **Step 11 amended**: the evidence document additionally carries D-1, D-2, FU-1, FU-2 and residual **R1**.
- **Step 12 amended (F8, F9, P9)**: cite `EXPECTED_SNAPSHOT_COUNTS` as the mechanical P3 gate; treat a `nav-dropdown` red as blocking; run the P9 residue proof.
- **Step 13 amended (F3)**: the known-unstable classification set extends to thumbnail captures.

**Effort**: **L**, unchanged. **Owner**: `senior-developer` in `wt/css-tbl-helpers` after Gate 1. **Rollback**: `git checkout -- static/css/layout.css` at any point; outcome B is reachable from any step and is a completion, not a rollback.

### Where Plan v2 departs from the proposed dispositions

Both departures are recorded rather than silently applied.

- **D-A — C4's outcome-A tightening is not adopted.** The proposed disposition (following architecture #3) was C4 = "no bundle other than `layout.css`" under both outcomes **with an outcome-A-only tightening to "no bundle at all"**. Plan v2 keeps the single shape under both outcomes, following the test-strategist's F1 fix instead — the two reviewers differed here. Reasons: (i) the tightening re-creates exactly the F2 subsumption problem, since under outcome A "no bundle at all" is red in every state where C1 is red, so it has no independent red path; (ii) C4's technique is selector-presence globbing while C1's is rule-head counting, so a tightened C4 would state the `layout.css` guarantee **more weakly** than C1 already does, and if C1 were ever removed C4 would silently become the only `layout.css` guarantee at the weaker strength. Keeping the two disjoint — C1 owns `layout.css` by the stronger technique, C4 owns the siblings — is the shape that survives both F1 and F2.
- **D-B — FU-2 is elevated from "record it" to a Gate-1 owner decision (OD-2).** The proposed disposition was to record the `.d-none` defect in the evidence document and `MASTER_HANDOVER.local.md`. Plan v2 does that **and** surfaces it at Gate 1, because it is not a documentation nit: it is a live user-facing defect in a core workflow (CLAUDE.md §1 workflow #5, Distribute), the user sees an empty Distribution card with live **Export Volume Plan** and **Save & Activate** buttons before any split is calculated, and **two green gates cannot see it** by construction. Burying that in a follow-up list is the same failure mode this packet exists to repair. The scope discipline is unchanged — nothing is absorbed, no forbidden file is touched — only the visibility is raised, and the owner decides.

### Gate-1 owner decisions

| # | Decision | Recommendation |
|---|---|---|
| **OD-1** | The stale "do not act" directive in `MASTER_HANDOVER.md:1779` and `ACTIVE_DEVELOPMENT.md:274–279` (and the refuted rationale in `_E_LAYOUT_:190`, `REFACTOR_PLAN.md:1412`) — leave, or authorize a separate docs packet? | **Separate docs packet.** Not this packet: its artifact table is closed and shared status documents are off-limits to it. |
| **OD-2** | The live `.d-none` defect on `/volume_splitter` (FU-2) — schedule now, or park? | **Schedule as its own packet.** It is a real user-visible defect in a core workflow with zero gate coverage; the fix touches `scss/**` or `templates/**`, both forbidden here. Do not absorb it. |
| **OD-3** | Proceed to implementation on the four-criteria-PASS evidence, with (e), (f-after) and (g) to be measured after approval? | **Yes.** DR-1 remains all-or-nothing; approval authorizes the measurement, not the outcome. |

---

## Sign-off

- [x] Gate 0 complete when required by planning size; otherwise marked not applicable. — **Complete**: owner-approved-in-prompt, all three Section 0 boxes checked above.
- [x] Every finding has a disposition. — **26 of 26.** architecture-reviewer 1–10, test-strategist F1–F12, product-risk-reviewer 1–4. One `defer` (architecture #2 → **D-2**), carrying its one-line reason and a commitment to a `MASTER_HANDOVER.local.md` note at implementation time; all other 25 accepted, two with recorded departures (**D-A**, **D-B**).
- [x] Agent provenance complete — both `product-manager` IDs, same-PM-resumed yes/no, the three reviewer IDs, and an evidence-gap line (or `none`). — All five IDs stamped exactly as the manager supplied them; same-PM-resumed `yes`; evidence gap `none`.
- [x] User approved Plan v2. — **GATE 1 APPROVED by the owner, 2026-08-04.** All three decisions were answered:
  - **OD-1** → *a separate docs packet.* The four documents keep the refuted rationale and the two stale operating directives; this packet writes none of them (deferral **D-1** / **D-2**).
  - **OD-2** → *schedule the `.d-none` Distribute defect as its own packet.* Recorded as **FU-2** with runtime evidence; explicitly not absorbed.
  - **OD-3** → *proceed.* Approval authorized the measurement, not the outcome; DR-1 remained all-or-nothing.
- [x] Ready to implement — implementation completed; see [`EVIDENCE.md`](EVIDENCE.md).

### Outcome

**Outcome A — all nine rules deleted atomically**, `layout.css:1589–1634`, **47 lines removed, 0 inserted**. DR-1 (a)–(h) passed for all nine members; the three `display: block` rules WP4.4-e called indistinguishable were each distinguished in 100% of their applicable contexts and each flipped in 100% of them after deletion. `DEFERRED_HELPER_COUNTS` was replaced by C1–C5, with 11/11 red paths executed — including the two-sided C2 proof (C2 green on a fully restored family while C1 red on the same tree).

Two external merge blockers are recorded in [`EVIDENCE.md`](EVIDENCE.md) §8 and in `MASTER_HANDOVER.local.md`; neither is caused by this change and neither is fixed here.

---

## See also
- [`.claude/commands/council-plan.md`](../../.claude/commands/council-plan.md) — how to run the council.
- [QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md) — change-type → required tests/reviewers; the `CSS (static bundles)` row governs this packet.
- [`.claude/rules/verification.md`](../../.claude/rules/verification.md) — the durable evidence method this packet is bound by.
- [`docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md`](../CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md) §4a — the deferral this packet re-opens; superseded by this packet's evidence document, and left byte-unchanged (Assumption A6).
- [`tests/test_css_wp4_4_layout_contracts.py`](../../tests/test_css_wp4_4_layout_contracts.py) — the contract file this packet edits.
