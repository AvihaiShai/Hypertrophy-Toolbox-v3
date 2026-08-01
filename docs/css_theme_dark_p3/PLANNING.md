# Plan Review — CSS `theme-dark.css` inertia arc (WP4.4 closeout proposal **P3**)

*Phase 4 CSS, successor arc to WP4.4. Planning artifact only. Follows [`docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md`](../ai_workflow/PLAN_REVIEW_TEMPLATE.md).*

**Planning size:** **Large / cross-cutting** per the plan-stage routing table in
[QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) — a shared-surface
`static/css/**` change, which that file's own `static/css/**` row declares *"Large at plan
stage."* → **Gate 0 + Gate 1 both required.**

**Gate status: NEITHER GATE IS SIGNED.**

| Gate | State |
|---|---|
| **Gate 0** (requirements) | **PENDING — presented together with Plan v2**, at owner direction. Not approved. No packet may cite Gate 0 as discharged. |
| **Gate 1** (council-reviewed plan) | **NOT REACHED.** Plan v1 below has not been through [`/council-plan`](../../.claude/commands/council-plan.md). |

**Base:** `main` @ **`4b0670b`** (the commit that merged proposal **P2**, PR #222 — the
`static/css/**` gate row). *Re-pinned at council: Plan v1 read `d543a4b`, which is **P1**
(PR #223, the schema-v2 Linux ledger). All three reviewers flagged it; the correction is
recorded in the response matrix and applied throughout this document.*

**Status of this document:** Section 0 (as amended at council), Plan v1 (historical), the three
council reviews, the response matrix, **Plan v2**, and the **Plan v2 re-review**.
**Review rounds are closed** — four reviewer passes, **41 findings, all dispositioned**, every
verdict now `approve-with-changes`. **Nothing in this arc is authorized to execute.** Gate 0
and Gate 1 both remain **unsigned**; Plan v2 is a proposal awaiting the owner.

> **Section 0 was amended after council and before owner presentation.** Gate 0 is unsigned,
> so Section 0 is still a draft; presenting the owner a brief that reviewers had already
> proven factually wrong would be worse than amending it. Every amendment is itemized in the
> response matrix. The amendments are: the base commit re-pin; assumptions 1–2 promoted from
> ⚠️ to verified fact; **Q7 withdrawn** (answered); **Q2 withdrawn** (converted to a plan rule
> — see the adjudication of architecture-reviewer #2); **Q8 and Q9 added**; a third contract
> ceiling recorded; G4 restored to full strength; AC4 and AC7 restated.

---

## Section 0 — Requirements Brief

### Raw request (verbatim)

> Write **Section 0 (Requirements Brief) and Plan v1** for a new CSS work arc, into a new planning document at `docs/css_theme_dark_p3/PLANNING.md`. Use the shell in `docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md`. Base: `main` at `d543a4b`.
>
> **You write only that PLANNING.md. Do not touch any production CSS, template, test or config file.**
>
> ## Gate status — state this explicitly in the document
>
> Per the plan-stage routing table in `docs/ai_workflow/QUALITY_GATE.md`, this work is **Large** (cross-cutting shared-surface CSS change), so it requires **Gate 0 + Gate 1**. **Neither is signed.** The owner has directed that Section 0 and the council-reviewed Plan v2 be presented together for sign-off. Mark Gate 0 as **PENDING — presented with Plan v2**, and do not represent it as approved.
>
> ## The finding this arc addresses (WP4.4 closeout proposal P3)
>
> Read these first — do not take my summary as the source:
> - `docs/CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md` §5 (proposal P3) and §7
> - `docs/CSS_PHASE4_WP4_4_J_THEME_DARK_EVIDENCE.md` (the packet that measured it)
> - `docs/css_phase4_wp4_4/PLANNING.md` — owner rulings N1–N10, and R1–R6, especially **R4**
> - `docs/CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md` §8 (oracle blind-spot register) and §12
>
> The finding: **`static/css/theme-dark.css` is largely inert.** It wraps nearly every selector in `:where()`, which contributes **zero specificity**, so its unlayered `!important` declarations lose to any more specific `!important` elsewhere — including the `:is(#workout…) .table.table-calm` family in `components.css` at specificity (1,2,0). WP4.4-j measured this directly: re-pointing `background: none !important`, a declaration shadowing several of j's certified removals, moved **zero** computed values in either theme. j reduced the file 621 → 574 lines under constraint C11; a far larger reduction is likely available on evidence **no packet in the arc gathered**.
>
> ## Hard constraints — these are binding, not suggestions
>
> - **R4 stands: `theme-dark.css` may NOT be unlinked, and `templates/base.html` is frozen.** Removing the file from the page is out of scope entirely.
> - **N2 freezes `@layer` membership** arc-wide. Do not propose moving declarations between layers.
> - **C8 — the 235 declarations WP4.4-h withheld** behind the frozen `@layer workout` span (`openLine 3539 / closeLine 4104` in `components.css`) stay deferred and untouched.
> - **G4 — the superset dark-tint gap** stays deferred.
> - No snapshot may be rebaselined. The Windows animated-logo red is a **band** (875/882 ∪ 1,039/1,046), never a constant, and is never resolved with `--update-snapshots`.
>
> ## Method rules the arc has already paid for — Plan v1 must show how it satisfies each
>
> - **M-h3 (the central one): a cascade census is NOT deletion authority.** WP4.4-g's census nominated 342 zero-winner declarations; WP4.4-h's live-CSSOM **removal oracle** proved **35 of them live on removal**. Delete only on the **intersection** of census ∩ zero-winner recount ∩ removal oracle. Treat `neverProbed`, unresolved selectors and missing blast coverage as **exclusions, not passes**.
> - **M-h2: never run a census with `TESTING=1`** — `utils/db_initializer.py` drops `user_selection` and `workout_log` under that flag, so data-bearing routes render empty and declarations are classified against a DOM that does not exist in use. Seeded vs unseeded was 21,693 → 37,915 DOM nodes and dead 342 → 388. Use a frozen seeded probe DB with `TESTING` unset, and give every harness an explicit `DB_FILE`.
> - **M-h1: `pause()` before `currentTime = 0`**, not after — the reverse re-anchors a running animation and it keeps advancing.
> - **M6a: suppress transitions before applying, reading AND removing a sentinel** — and note the committed CSS-only universal `transition: none !important` suppressor in `scripts/css_audit/runtime_probe.mjs` is **beatable** by layered `!important` and by more-specific unlayered `!important`. No packet may assume that stylesheet rule alone enforces M6a.
> - **From the i–k tail:** (a) *a gate that cannot fail is worse than no gate* — for every control, state what input makes it fail; (b) *a zero means nothing without a live control* — bracket every differential with a same-CSS control AND a committed, digest-pinned known-live mutation; (c) *provenance is content, not filenames* — record checkout root and served digest on every capture.
>
> ## Required gates for this change type
>
> Derive them from the `static/css/**` row of `docs/ai_workflow/QUALITY_GATE.md`. Note that row is being added by PR #222 and may not be on `main` when you read it — if absent, derive from the WP4.4 evidence documents and say so. The set includes full `pytest` (cascade contracts run inside that total), the nine required Chromium specs, the `visual.spec.ts` matrix at **66 tests per platform** run with **`PW_VISUAL_SEED=1`**, seven-surface Stylelint with no category rising without a recorded owner exception, and the **Linux N8 deep gate** reconciled against `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` — which is now **schema v2, 11 inherited reds across two spec files** (`visual.spec.ts` 10 + `visual-baseline-thumbnails.spec.ts` 1).
>
> ## What Plan v1 must contain
>
> Goal; scope in/out (with R4 explicitly out); a packet decomposition with a proof-first ordering; the artifact list with paths; effort; sequence; expected gates per packet; and an explicit **abandonment criterion** — WP4.4's N3 precedent pre-authorized abandonment as an acceptable arc outcome rather than a failure, and this arc should say under what measured condition it stops.
>
> Be concrete about the *oracle design*, because that is where every packet in WP4.4 actually failed first. Do not propose a line-count target as an acceptance criterion — WP4.4-f1 shipped one rule against a projected −150 to −400 and that was the correct outcome.
>
> When done, report the absolute path you wrote, the packet count you propose, and the abandonment criterion. Do not proceed past Plan v1 — stop there and wait.

---

### Problem

`static/css/theme-dark.css` occupies 574 lines and 124 `!important` declarations of the
Phase-4 hand-maintained CSS denominator, and the arc that just closed has evidence that a
large fraction of it **cannot win anywhere** — but no packet measured *which* fraction, and
the repository currently has no instrument capable of measuring it.

Three separable problems, stated without proposing the fix:

**1. The file's specificity is structurally zero.** Every rule except the final block wraps
its selector in `:where()`, which contributes zero specificity. The file is unlayered
(pinned by `test_the_file_declares_no_layer`) and is the **last** stylesheet in
`templates/base.html`, so it wins same-specificity, same-importance ties — but it loses
every contest against a more specific `!important`, and, because unlayered `!important` is
the weakest importance position in the app (G10/A6), it loses to **every** layered
`!important` at any specificity, including the ~900 lines inside `@layer navbar` and the
`@layer workout` block in `components.css`. Against the unlayered
`:is(#workout…) .table.table-calm` family at (1,2,0) it also loses.

**2. The one direct measurement points at a large opportunity and stops.** WP4.4-j's second
known-live control re-pointed `background: none !important` — the declaration whose presence
made several of j's certified removals dead — and it moved **0 computed values in either
theme** across 66 contexts and 2,275,668 values. j reported this as informative rather than
comfortable, and explicitly handed it forward: *"a bundle whose specificity is zeroed by
`:where()` is a candidate for far larger reduction than C11 permits here, on evidence this
packet did not gather."* That is a single declaration. The status of the other ~570 lines is
**unmeasured**, and "largely inert" is a claim about a distribution, not a warrant for any
particular deletion.

**3. The instrument that could settle it no longer exists in the repository.** M-h3 makes a
live-CSSOM **removal oracle** the only deletion authority. The only removal oracle this
repository ever had was WP4.4-h's `h_certify.mjs`, which — with `h_census.mjs`,
`h_zero_winner_check.mjs`, `h_differential.mjs`, `h_compare_strict.mjs`,
`h_build_manifest.mjs`, `h_apply.mjs`, `h_ranges.mjs` and `h_seed_probe_db.py` — lived under
the **gitignored** `artifacts/wp4_4/` per constraint A11. `artifacts/wp4_4/*.mjs` matches
nothing on this tree and `scripts/css_audit/` contains no `h_*` file. What *is* committed
(`j_theme_differential.mjs`, `j_diff_theme.mjs`, `j_known_live_mutation.mjs`,
`j_shadow_certification.mjs`, `j_theme_dark_inventory.mjs`, `i_seed_probe_db.py`,
`measure.py`, `specificity.py`, `resolution_check.py`, `stylelint_surfaces.mjs`,
`runtime_probe.mjs`) is a *differential* apparatus and an *intra-file shadowing* certifier —
neither of which grants deletion authority under M-h3.

**And the differential is nearly blind on this specific file.** For a bundle hypothesised
inert, removing a declaration moves zero computed values **whether the declaration is dead
or the instrument is broken**. A zero is the expected reading under both hypotheses. That is
not a hypothetical: it is exactly what j's shadow-winner control returned. Any plan that
treats "the differential reported zero" as evidence here is measuring nothing.

**Fourteen** assertions bound the size of any answer, and all of them are already in the
codebase rather than in prose. Plan v1 named **two**; the council found the rest. The three
narrative entries below are kept because each carries an argument; the complete enumeration
follows in the table, and **Plan v2 makes producing that table a mechanical step of P3-a
derived from `measure.contract_anchors()` / `measure.pinned_declarations()`, not from reading**
— deriving it by reading is exactly how Plan v1 missed twelve of them.

- **Ceiling 1 — count pins.**
  `tests/test_css_wp4_4_theme_dark_contracts.py::test_every_custom_property_declaration_survives`
  pins the custom-property declaration count at **exactly 34**, and
  `test_theme_dark_is_still_linked_and_nonempty` asserts the comment-stripped file contains
  **at least 50** `{`. Counted by reading at this base, the file has 72 top-level rules plus
  one `@media` wrapper plus its one nested rule = **74** brace-opening blocks — so **at most
  24** blocks may be removed whole, arc-wide, before a WP4.4-j contract reds.
- **Ceiling 2 — a pinned comment.**
  `tests/test_css_wp4_4_a_baseline_contracts.py::test_important_is_counted_in_reconcilable_units`
  asserts the literal string `"Zero !important. */"` is present in the **working tree** copy
  of `theme-dark.css`, at `:546–548`, directly above the token block at `:550`. *Adjudicated
  at council (architecture-reviewer #2): this instance **cannot fire**, because `:546–548` is
  the leading comment of `:550`, and `:550` is the surviving winner that no packet deletes.
  The general defect it exposed is real and is retained as plan rule **O10b**.*
- **Ceiling 3 — a cross-surface pin, with no reachable amendment path.**
  `tests/test_css_cascade_contracts.py:1006–1007` asserts, against the **working tree**, that
  `':where([data-theme="dark"] .frame-header) {'` and `"backdrop-filter: blur(8px) !important;"`
  are both present in `theme-dark.css`. The rule is at `:100–105` and is squarely inside
  family **F2**, i.e. inside P3-c's declared scope. Two things make this the sharpest of the
  three:
  1. **The assertion is non-specific and cannot fail for the thing it protects.**
     `backdrop-filter: blur(8px) !important;` occurs **twice** — at `:102` inside
     `.frame-header`, and at `:144` inside the `.form-control` / `.form-select` /
     `.input-group-text` rule. It is a substring check, so deleting `:102` leaves it green
     while removing exactly what the comment at `test_css_cascade_contracts.py:993–995`
     documents the pin as existing to protect: *"the late dark theme is why the route retains
     one explicit dark frame-header blur override."* This is the same class of defect as the
     `occurrences <= 1` assertion below — a gate that passes for the wrong reason.
  2. **The P2 amendment path exists but does not reach this case.** Since PR #222 merged,
     `QUALITY_GATE.md`'s `static/css/**` row states that edits to the cascade contracts *"must
     be explicitly scoped, justified, and must not weaken an existing guarantee."* Deleting
     the `.frame-header` rule, or its `backdrop-filter`, necessarily weakens the guarantee the
     assertion encodes. So the path is real but closed here — and the outcome is **over-determined**:
     under *every* reading of the authority question it comes out the same. See the adjudication
     of product-risk-reviewer #2.
  3. **It is double-locked.** Editing `tests/test_css_cascade_contracts.py` at all additionally
     reds `test_contract_anchor_register_covers_every_shared_surface`
     (`tests/test_css_wp4_4_a_baseline_contracts.py:285`, assertion at `:297`), because
     `measure.CONTRACT_FILES` (`scripts/css_audit/measure.py:34–37`) pins `startLine` /
     `endLine` / `assertionLines` for every test in that file. *(test-strategist #3. **Name
     corrected per re-review N6** — `test_the_contract_anchor_registry_is_exact` does not
     exist; it entered this document through the reviewer's verbatim text and I propagated it
     without checking, having read the real name earlier in the same session. The cited line
     `:297` was right. The offsetting good news, which Plan v1 also missed: `CONTRACT_FILES`
     covers **only the two shared files**, so amending
     `tests/test_css_wp4_4_theme_dark_contracts.py` under **Q1** does not disturb the registry
     — which is what makes Q1 cheap.)*

  **`.frame-header` is excluded from candidacy pending Q8.**

#### The complete ceiling enumeration

*Every working-tree assertion that reads `static/css/theme-dark.css`, with the ceiling each
imposes. **P3-a regenerates this table mechanically; the copy below is Gate-0 material, not a
source any packet may inherit.*** *(architecture-reviewer #7, product-risk-reviewer #2,
test-strategist "required gates".)*

| Assertion | Ceiling it imposes | Amendable? |
|---|---|---|
| `theme_dark_contracts.py:32` — `"css/theme-dark.css" in base.html` | R4: file stays linked | n/a — not in scope |
| `:34` — file non-empty after comment strip | file may not be emptied | Q1 |
| `:35` — `body.count("{") >= 50` | **at most 24 of 74 brace-blocks removed, arc-wide** | Q1 — **but this is a floor by design, not a count** (architecture #13) |
| `:45` — custom-property declarations `== 34` | **blocks P3-d entirely** | Q1 — the one assertion the "re-pin exactly" rule targets |
| `:52` — `css.count("@media") == 1` | **exact equality, not a floor**: F6 may be neither removed nor duplicated | Q1 |
| `:53` — `"prefers-reduced-motion: reduce"` present | F6 preserved | Q1 |
| `:55` — the `@media` block still covers `.value-changed` | F6 preserved | Q1 |
| `:62` — `css.count(".value-changed") >= 7` | **zero headroom — the file contains exactly 7** (`:519, 520, 525, 526, 531, 532, 539`). Deleting *any* reds it. | Q1 |
| `:68` — `"superset" not in css` | G4 back-door half | Q1 |
| `:88` — `occurrences <= 1` on four `(selector, property)` pairs | **passes at zero** — see O14 | Q1 (strengthen to `== 1`) |
| `:98` — `"@layer" not in css` | N2 premise; forbids the "make it win" shape | Q1 |
| `a_baseline_contracts.py:128` — `"Zero !important. */"` present | Ceiling 2 — **unreachable by this arc's deletion set** | not needed |
| `cascade_contracts.py:1006` — `':where([data-theme="dark"] .frame-header) {'` | **the `.frame-header` rule head may not be deleted or reformatted** | **no** — double-locked |
| `cascade_contracts.py:1007` — `"backdrop-filter: blur(8px) !important;"` | at most one of `:102` / `:144` may lose it — **and the check cannot tell which** | **no** — double-locked |

Two further working-tree readers impose no deletion ceiling and are recorded so no packet
re-derives them: `a11y_contracts.py:427` and `layout_contracts.py:294` both assert that
`theme-dark.css` does **not** style a generation another packet dropped — additive
constraints, satisfied by deletion.

The outcome that is missing is a **measured, per-declaration classification** of
`theme-dark.css` with deletion authority behind it — or a measured finding that no such
authority can be obtained, which is an equally valid result.

---

### Acceptance criteria

*Deliverable criteria — checkable by reading the finished artifacts.*

1. **Instrument exists and is committed.** Given the WP4.4-h removal-oracle harness is absent
   from this repository, when the first packet completes, then a live-CSSOM removal oracle, a
   seeded cascade census and an **independent** zero-winner recount exist as committed files
   under `scripts/css_audit/`, each with a recorded red-path proof, and each is demonstrated
   to report **LIVE** for a declaration independently proven live.
2. **Deletion only on the intersection (M-h3).** Given any declaration this arc proposes to
   delete, when its warrant is read, then it appears in **all three** of: the seeded census
   non-winner set, the independent zero-winner recount over the differential's own ownership
   records, and the removal oracle's `deadCertified` set. `neverProbed`, unresolved selectors,
   `reachedNothing`, missing blast coverage, uncertifiable elements and interaction-state-only
   records are recorded as **exclusions with counts**, never as passes.
3. **Per-family live control (the file-specific rule).** Given any family of declarations in a
   proposed deletion set, when the differential reports zero movement for that family, then a
   **committed, digest-pinned** known-live mutation sited *inside that family's own region* is
   shown to move ≥1 computed value in that family's own theme and **0** in the other theme. A
   family whose own control moves zero is **excluded from deletion**, because on this file a
   zero is the expected reading under both hypotheses.
4. **Seeding, isolation and containment (M-h2).** *Restated at council — product-risk-reviewer
   #4 proved the Plan v1 wording unsatisfiable and unsafe.* Given every browser probe this arc
   runs, when its provenance block is read, then:
   - `TESTING` was unset, and an explicit `DB_FILE` was passed;
   - **every harness refused to start unless the resolved `DB_FILE` path is under
     `artifacts/`** — a hard guard, asserted before the server is spawned;
   - the digest compared is that of a **post-startup frozen artefact**, not of the seed file.
     With `TESTING` unset, real `app.py` startup runs `prepare_runtime_database()`,
     `bootstrap_runtime_database()`, `run_all_initializers()`, `upgrade_catalog_from_seed()`
     **and** `create_startup_backup()` against whatever `DB_FILE` names — so the database is
     mutated by the first server start and "identical at start and end" is unachievable as
     Plan v1 wrote it. The frozen reference is captured *after* one full startup has completed
     and quiesced, with WAL/SHM checkpointed and removed, and every subsequent run is asserted
     against that;
   - **`<probe dir>/auto_backup/` is cleared** before each half, and **`FLASK_DEBUG` is
     pinned** — `app.py` defaults it to `'0'` and `utils/database.py` to `'1'`, and that flag
     decides the journal mode, i.e. whether WAL sidecars exist at all;
   - the frozen artefact is **restored byte-exactly before each half** of a before/after pair,
     so the two halves are never seeded from differently-mutated databases;
   - port 5000 was asserted free before the server was started, and exactly one listener PID
     was observed at every guard checkpoint.
5. **Provenance is content (i–k rule c).** Given any before/after comparison, when the differ
   runs, then it **refuses** a same-root pair (except the known-live control, which must opt in
   explicitly), refuses two halves that served the same `theme-dark.css` digest, refuses a half
   whose own same-CSS control failed, and refuses an empty comparison; and every capture
   records checkout root, on-disk digest and **served** digest.
6. **Blind-spot discipline (A §8).** Given the oracle blind-spot register, when this arc cites
   evidence for a declaration setting `backdrop-filter`, `-webkit-backdrop-filter`,
   `background`, `background-image`, `border-color`, `border-radius`, `box-shadow` or
   `text-shadow`, then it cites a **computed-style differential** and does **not** cite the
   pixel matrix. Those properties cover the large majority of this file; the pixel matrix is a
   regression gate for this arc, not an evidence source.
7. **Contract ceiling is known before the first cut.** Given **all** contracts that read
   `theme-dark.css` from the working tree — enumerated mechanically, not by recall — when
   Plan v2 is read, then each is named with its exact assertion, the deletion ceiling it
   imposes, and whether an amendment path exists for it under the `QUALITY_GATE.md`
   `static/css/**` row. No packet may remove, weaken, loosen or `xfail` an existing assertion.
   **Enumerating them is a mechanical step of the first packet, emitted from
   `measure.contract_anchors()` and `measure.pinned_declarations()`** — the registers that
   already exist and are already asserted exact by
   `tests/test_css_wp4_4_a_baseline_contracts.py:293–302`, which explicitly asserts
   `theme-dark.css` is among the bound surfaces. Not a prose list carried forward from this
   document: Plan v1 derived its ceiling **by reading**, carried two, and missed twelve —
   including one inside the main deletion family with no amendment path.
8. **Gate set run in full.** Given any packet that writes production CSS, when its gates run,
   then the complete `static/css/**` shared-surface set is run: full `pytest` (cascade
   contracts inside that total), the nine required Chromium specs, the full `visual.spec.ts`
   matrix at 66 tests per platform with `PW_VISUAL_SEED=1`, seven-surface Stylelint, and the
   Linux N8 deep gate reconciled against the **schema-v2** ledger (11 reds across two spec
   files). No snapshot is regenerated; `--update-snapshots` is never run under packet
   authority; the Windows animated-logo red is reconciled as a **band** (875/882 ∪
   1,039/1,046), never as a constant.
9. **Stylelint anchored correctly.** Given the seven-surface Stylelint measurement, when this
   arc reports movement, then no category rises on any surface without a recorded owner
   exception, and every figure is anchored to **this arc's own base**, never to the pinned
   WP4.1 baseline (which predates WP4.3 and would report an improvement as a regression).
10. **Line count is a report, not a target.** Given any packet, when it is judged, then line
    count, `!important` count and Stylelint delta are **reported figures only** and never
    pass/fail criteria. A packet that certifies one declaration and deletes one declaration is
    a correct outcome; so is a packet that certifies none and deletes none.
11. **Abandonment is a pre-authorized outcome.** Given the classification checkpoint, when the
    certified intersection is empty or the instrument fails a fatal control, then the arc ends
    as **audit-only**, `theme-dark.css` is byte-identical to its arc base, and this is recorded
    as an acceptable result rather than a failure.
12. **Preservation invariants are asserted, not described.** Given the arc's end state, when
    contracts run, then R4 (file still linked from an unchanged `templates/base.html`, file
    nonempty), N2 + the no-`@layer` premise, C8 (`components.css` untouched by this arc) and G4
    (`superset` appears nowhere in the file) are each asserted by a test, not by prose.
13. **Planning-session scope.** Given this session, when Gate 0 is reached, then **no file
    other than `docs/css_theme_dark_p3/PLANNING.md` has been created or modified**, and no
    packet has been implemented.

---

### Calculation surface

**`none`.**

This is a CSS-only arc. No Python calculation module is read for behavior, called, or
changed. Specifically untouched: `utils/effective_sets.py` (`calculate_effective_sets`,
`CountingMode`, `ContributionMode`), `utils/weekly_summary.py`, `utils/session_summary.py`,
the progression logic under `utils/`, and the fatigue modules. No route, response shape, DB
schema, or `data/database.db` byte is in scope.

Two clarifications, because this arc *does* touch executable files:

- The arc adds **measurement scripts** under `scripts/css_audit/` and **contract tests**
  under `tests/`. Neither is application code; neither is imported by `app.py`, any
  blueprint or any `utils` module; neither can affect a rendered response. They are held to
  the same review bar as application code but they are not a calculation surface.
- The arc uses a **frozen seeded probe database** built by the committed
  `scripts/css_audit/i_seed_probe_db.py` into a scratch path under gitignored `artifacts/`.
  It derives from the committed synthetic fixture `e2e/fixtures/database.visual.seed.db`
  (`i_seed_probe_db.py:35`), **not** from the user's `data/database.db` — so nothing of the
  user's leaves the machine via the N8 CI dispatch. `data/database.db` and
  `data/catalog.seed.db` are never written, and **no harness may run without an explicit
  `DB_FILE` under `artifacts/`** (**O13**).
- **Recorded once so it is not re-litigated per packet** (architecture-reviewer #14):
  `scripts/css_audit/i_seed_probe_db.py:68,93` uses raw `sqlite3.connect()` rather than
  `with DatabaseHandler() as db:`. This is a **deliberate, scoped exception**, not an
  oversight — the file is committed audit tooling outside the `app.py → routes/ → utils/`
  chain, it takes an explicit `--out` rather than reading `utils.config.DB_FILE`, and this arc
  reuses it **unmodified**, which is the correct treatment for a certified harness. Any packet
  that modifies it loses this exception and must justify the change on its own.

No worked before/after example is applicable because no numeric output exists in this arc's
surface. The only "values" in scope are CSS token values and computed style values, covered
by the differential and pixel gates rather than by calculation migration notes. Should any
packet ever propose touching a Python calculation module, that packet is **out of scope for
this plan** and requires its own Gate 0.

*Recorded so `product-risk-reviewer` can confirm the `none` claim at council time rather than
infer it.*

---

### In scope

- **Rebuilding the WP4.4-h class of oracle as committed, red-path-proven tooling** under
  `scripts/css_audit/` — a live-CSSOM removal oracle, a seeded cascade census, an independent
  zero-winner recount, a postcss character-offset range emitter, a self-validating deletion
  manifest builder, a digest-asserting applier/restorer, and a per-family known-live control
  generator.
- **A whole-file, per-declaration classification of `static/css/theme-dark.css`** — 574 lines,
  72 top-level rules, 124 `!important` declarations, 34 custom-property declarations across
  two token blocks (counted by reading at this base; the first packet re-measures and pins).
- **Deletion of exactly the certified intersection**, in two separately certified production
  packets: the paint declarations, and the shadowed legacy token block.
- Per-packet contract test files following the **N1** pattern (one file per packet, never
  consolidated), per-packet evidence documents, and one integration/closeout packet.
- Recording, unacted, anything the classification surfaces that this arc is not authorized to
  change.

### Out of scope / non-goals

- **R4 — unlinking `theme-dark.css`, and any edit to `templates/base.html`.** Out entirely.
  Not a stretch goal, not a fast-follow, not a "if the file ends up small enough" clause. The
  REFACTOR_PLAN §WP4.4 end-state *"or is removed after proof"* remains out of reach.
- **Making the file win.** Removing `:where()`, adding `@layer`, adding a class or ID hook,
  or re-weighting any declaration upward. The finding is that the file is inert; that is a
  reason to *delete*, not a mandate to *repair*. A repair changes dark-theme rendering on
  every route, violates V3 (maximum specificity must not rise) and V1 (no unexplained visual
  differences), and is forbidden in the `@layer` shape by **N2** and by
  `test_the_file_declares_no_layer`. It is a visible-change proposal needing its own Gate 0.
  *(Owner confirmation requested — Q3.)*
- **N2** — no packet may move a rule across a layer boundary, add a layered block or remove
  one, in any file.
- **C8** — the **235** declarations WP4.4-h withheld behind the frozen `@layer workout` span
  (`components.css` `openLine 3539 / closeLine 4104`). Deferred and untouched. This arc writes
  no byte of `components.css`.
- **G4** — the superset dark-tint gap (`--superset-bg-1..4`). Deferred; `superset` must appear
  nowhere in `theme-dark.css`, and `pages-workout-plan.css` is not pulled into this arc.
  **G4's operative clause is restored at full strength (product-risk-reviewer #1 — Plan v1
  carried G4 at half strength):** *any change in superset row rendering is a rollback trigger,
  including from a packet that never opens `pages-workout-plan.css`.* The mechanism is
  specific and this arc walks straight into it — superset rows are ~8%-alpha tints that
  composite over ancestor backgrounds, and those ancestors are themselves family-F2
  candidates. A computed differential keyed on the row's own `background-color` therefore
  reports **zero** while the rendered colour changes, because the row's own declared value
  never moved — only what it composites over did. Worse, the probe database seeds no
  `superset_group`, so the superset declarations are `neverProbed` **by construction** while
  their ancestors are fully probed. Plan v2 answers this with oracle rule **O12**.
- **R1** — `tokens.css` remains read-only.
- The other six shared surfaces (`base`, `layout`, `components`, `navbar`, `a11y`, `motion`),
  all ten `pages-*.css` route bundles, everything under `scss/**`, and the generated
  `bootstrap.custom.min.css`.
- **Any snapshot rebaseline.** `--update-snapshots` is never run under packet authority. A
  needed rebaseline stops and escalates (V2).
- Any Python application, route, blueprint, schema, template or JavaScript change.
- Interaction-state and JS-applied-class declarations — `:hover`, `:focus`, `::placeholder`,
  `:not(:disabled)` and `.value-changed`. Declared out **up front** per M12, matching WP4.4-h.
  *(Owner ruling requested — Q6.)*
- Worktree creation, removal, merging or moving from any planning session.

---

### Assumptions made

- ✅ **VERIFIED FACT (was ⚠️; promoted at council, all three reviewers) — P1 and P2 are both
  owner-approved and merged, and this arc's sequencing precondition is discharged.**
  `docs/MASTER_HANDOVER.md:1357`, `:1376`, `:1409` and `:1410` record **P1 = `d543a4b`
  (PR #223)** and **P2 = `4b0670b` (PR #222)**, both owner-approved;
  `ACTIVE_DEVELOPMENT.md` and `REFACTOR_PLAN.md` agree.
  `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` on disk is `schemaVersion: 2`,
  `totalCount: 11` across two `specs[]` entries. The recorded rule *"land P1 before P3"* is
  therefore discharged, and this arc's base is **`4b0670b`**, not `d543a4b`.
- ✅ **VERIFIED FACT (was ⚠️) — the `static/css/**` row is on `main`.**
  `docs/ai_workflow/QUALITY_GATE.md` carries the change-type row at `:32`, the notes paragraph
  at `:39` and the Targeted-test-derivation bullet at `:60`. This arc's gates are derived from
  that row, cross-checked against `_K_INTEGRATION_` §7, `_J_THEME_DARK_` §7,
  `_H_COMPONENTS_DEAD_` §10 and `_A_BASELINE_` §12, which agree. **P2 also carries two owner
  amendments that bind this arc directly:** cascade-contract edits must be *"explicitly scoped,
  justified, and must not weaken an existing guarantee"*, and `static/css/**` now routes to
  that row instead of the empty-union `/verify-suite` fallback. **Q7 is withdrawn.**
- ⚠️ **The WP4.4-h harness is absent from the repository.** `artifacts/wp4_4/*.mjs` matches
  nothing; `scripts/css_audit/` contains no `h_*` file. This single fact drives the entire
  packet ordering — the arc cannot satisfy M-h3 without rebuilding it. If those files survive
  in a stash, a deleted branch or an unpushed worktree, **recovering them is strictly better
  than rewriting them** and the first packet must attempt recovery before writing new code.
- ⚠️ **File measurements were counted by reading, not by running a tool.** 574 lines; 72
  top-level rules; one `@media (prefers-reduced-motion: reduce)` wrapper containing one nested
  rule (⇒ **74** brace-opening blocks); 34 custom-property declarations split **16** in the
  `:where([data-theme="dark"])` block at `:2–22` and **18** in the unwrapped
  `[data-theme="dark"]` block at `:550–574`; 124 `!important` declarations per WP4.4-j. **No
  later packet may inherit these** — re-measuring and pinning them is the first step of the
  first packet, exactly as WP4.4's own §assumptions required of Packet a.
- ⚠️ **The "legacy token block is fully shadowed" hypothesis is mine, from reading, and is a
  nomination rather than a warrant.** The 16 declarations at `:2–22` sit at specificity
  (0,0,0) inside `:where()`; the block at `:550` redeclares all 16 names unwrapped at (0,1,0),
  later in document order, matching the same element. It reads as a complete shadow. But j's
  certifier **excludes custom properties by design (M9)**, and j's known-live control
  re-points *every* `--bg-primary` line — both occurrences — so j's "12 dark values" result
  does **not** distinguish which block produced them. Custom-property deadness needs its own
  proof, not this argument.
- ⚠️ **Assumed j's committed controls still run against the current tree.**
  `scripts/css_audit/j_known_live_mutation.mjs` hard-pins
  `EXPECTED_INPUT = e54818bf790eb2c11474f68ecddc25d66304d9edf650cf698853276e419f2fca` and
  refuses any other input digest. If `theme-dark.css` has changed since WP4.4-j, that control
  will refuse to run and must be re-pinned deliberately, not with `--expect-sha` passed to
  silence it. Not verified by hashing in this read-only session.
- ⚠️ **Assumed `selector-max-id: 24` on this file measures syntax, not cascade weight.**
  Stylelint counts ID tokens lexically; every one of them is inside `:where()` and therefore
  contributes zero specificity. No packet may read "24 IDs" as "24 heavy selectors", and a
  packet that deletes ID-bearing rules will move that count without moving any specificity.
- ⚠️ **Assumed WP4.4-j's characterization of the Workout Plan pastel input rules
  (`:438–535`) as "live" was an assertion under C11 preservation-only, not a measurement.**
  This arc treats them as the most probable in-file **known-live spikes** and measures them
  rather than inheriting the label.
- ⚠️ **Assumed measurement environment:** Windows / Chromium locally for pytest, the nine
  required specs and the Windows visual matrix; the `visual-linux` deep-gate workflow for N8;
  the pinned Stylelint `16.11.0` + `postcss-scss` `4.0.9` dev-dependency pins; Python
  3.14.6+ per the repository-wide runtime policy. Not re-verified in this read-only session.
- ⚠️ **Assumed a single implementer and strictly sequential merges.**
  `static/css/theme-dark.css` is **single-writer** for the whole arc; no two packets in this
  arc are ever concurrent, because every production packet writes the same file.
- ⚠️ **CORRECTED AT COUNCIL (architecture-reviewer #8) — Plan v1 self-bound to constraints
  that have already retired.** `.claude/rules/verification.md:21–24` states plainly:
  *"`docs/css_phase4_wp4_4/PLANNING.md` owns the arc … **When that arc closes, its
  arc-specific constraints retire with it; these do not.**"* WP4.4 closed at `k`. The owner's
  brief re-issued exactly **R4, N2, C8, G4** plus the method rules **M-h1, M-h2, M-h3, M6a**,
  the three i–k tail rules, the no-rebaseline rule and the animated-logo band. Plan v1
  additionally cited **C7, C10, C11, G10/A6, A8/F6, A11, M1, M3, M4, M5, M7, M9, M11, M12,
  N1, N3, N6, R1, R6 and V1–V6** as if they still bound. Most do not. Plan v2 resolves this in
  two ways rather than asking the owner to re-issue twenty numbers: constraints with a
  **durable home** in `.claude/rules/verification.md` are re-cited there and need no re-issue;
  the genuinely arc-specific remainder is **restated as P3-owned constraints P1–P8** with this
  arc's own numbering, for owner acceptance at Gate 0 (**Q9**). One consequence is called out
  explicitly: **Q1's Plan v1 reasoning "on the N6 pattern" is withdrawn** — N6 is a retired
  WP4.4 ruling and is not a precedent this arc may self-apply.

---

### Open questions for the user — ALL BLOCKING at Gate 0

*Amended at council: **Q2 and Q7 are withdrawn**; **Q8 and Q9 are added**. Numbers are not
recycled — a withdrawn question keeps its slot so the audit trail stays traceable.*

| # | Question | Why it blocks | Recommendation |
|---|---|---|---|
| **Q1** | **May this arc amend `tests/test_css_wp4_4_theme_dark_contracts.py`?** It is a WP4.4-j packet contract pinning eleven assertions over this file — see the ceiling table. Without amendment authority P3-d is impossible, whole-rule deletion is capped at 24 blocks, and the `occurrences <= 1` defect stays standing. | Determines whether one of the two proposed deletion packets can exist at all, and caps the other. | **Yes — narrowly.** Amendment restricted to **re-expressing the same premise against the newly certified state**, plus **strengthening `:88` from `<= 1` to `== 1`** (test-strategist #2). No assertion removed, weakened, loosened or `xfail`-ed; every re-pin accompanied by the certification that justifies it. **Two scoping corrections from council:** (a) the "re-pinned exactly, never converted to a floor" rule applies to **`:45` alone** — `:35`'s `>= 50` is a floor *by design*, R4's non-empty guard, and converting it to an exact pin would be a defect, not a fix (architecture #13); (b) **Q1 is cheap**: `measure.CONTRACT_FILES` (`scripts/css_audit/measure.py:34–37`) covers only the two *shared* contract files, so amending this one does not disturb `test_contract_anchor_register_covers_every_shared_surface` (`tests/test_css_wp4_4_a_baseline_contracts.py:285`, assertion at `:297`) (test-strategist #3, name corrected per re-review N6). *Plan v1's justification "on the N6 pattern" is **withdrawn** — see Q9. The live standard is the P2 owner amendment in `QUALITY_GATE.md`: explicitly scoped, justified, non-weakening. This request meets it; the owner must still grant it directly.* |
| ~~**Q2**~~ | ~~May a whole-rule deletion absorb the comment at `theme-dark.css:546–548`?~~ | — | **WITHDRAWN at council.** architecture-reviewer #2 established that this instance cannot fire: `:546–548` is the leading comment of the rule at `:550`, and `:550` is the surviving winner no packet deletes. The *general* obligation it exposed is real and is retained as plan rule **O10b** (the manifest builder derives contract-pinned literals from the contract files' ASTs and refuses any cut that would remove one) — a plan rule, not an owner decision. One less question for the owner. |
| **Q3** | **Is "make `theme-dark.css` win" in scope in any form** — removing `:where()`, adding `@layer`, adding specificity? | The finding "the file is inert" can be read either as a deletion opportunity or a bug to fix. They are opposite arcs with opposite risk profiles. | **Explicitly OUT.** It changes dark-theme rendering on every route and the `@layer` shape is forbidden by the owner-re-issued **N2** and by `test_the_file_declares_no_layer`. It needs its own Gate 0 as a visible-change proposal. |
| **Q4** | **Evidence-doc naming for this arc.** WP4.4's R6 governed that arc only and has retired with it. | Two packets colliding on one evidence path is the failure R6 existed to prevent. | **`docs/CSS_THEME_DARK_P3_<PACKET>_EVIDENCE.md`**, flat, matching the existing convention. |
| **Q5** | **N8 cadence for this arc.** WP4.4 ran the Linux deep gate at h, i, j and k. | Each deep-gate dispatch costs ~15 minutes of CI and must be budgeted per packet. | **Run it at every packet that writes production CSS, and at integration.** Read-only packets do not dispatch it — there is nothing for it to measure. |
| **Q6** | **Are interaction-state and JS-applied-class declarations in scope?** The file carries `:hover`, `:focus`, `::placeholder`, `:not(:disabled)`, the JS-set `.active` / `[data-view-mode]` view-mode state, and `.value-changed`. | ~26 of 72 rules. Declaring scope up front is a durable obligation (`.claude/rules/verification.md:58–61`); discovering it mid-packet is what shrank WP4.3i-dead from 24 declarations to 14. | **OUT, declared up front.** An inline sentinel cannot address a pseudo-element; interaction states animate, so their proof is unreliable until a control reaches zero. This lowers the ceiling and that is the correct trade. |
| ~~**Q7**~~ | ~~Is PR #222 merged?~~ | — | **WITHDRAWN at council — answered.** `MASTER_HANDOVER.md:1357/1376/1409/1410`, `ACTIVE_DEVELOPMENT.md` and `REFACTOR_PLAN.md` all record P1 (`d543a4b`, #223) and P2 (`4b0670b`, #222) as owner-approved and merged. Promoted to verified fact in the assumptions above. |
| **Q8** *(new)* | **Is the `.frame-header` dark blur override at `theme-dark.css:100–105` still a guarantee you want held** — given this arc may prove it inert, and given that the assertion protecting it cannot detect its loss? | Ceiling 3, and the only one that is **double-locked**: `tests/test_css_cascade_contracts.py:1006–1007` pins it, and editing *that* file reds `test_the_contract_anchor_registry_is_exact` via `measure.CONTRACT_FILES`. `.frame-header` sits inside family **F2**, the main deletion family. Without a ruling, P3-c must exclude it. | **Exclude `.frame-header` from candidacy** unless the owner rules otherwise — the outcome is over-determined across all three readings of the authority question (see the adjudication of product-risk #2), so this does **not** wait on Q9. **Separately, and regardless of the answer: the assertion should be repaired.** `:1007` is a bare substring check satisfied by an unrelated line at `:144`, so it stays green when `:102` is deleted — it does not protect what its own comment at `:993–995` says it protects. Anchoring it to the `.frame-header` block is a strengthening, but it is inside the double lock, so it needs the owner's word rather than packet authority. |
| **Q10** *(new, at re-review)* | **May P3-a1 repair the two shared WP4.4 registers and regenerate `docs/CSS_PHASE4_WP4_4_A_BASELINE.json`?** Specifically: add the eight unregistered neutralizers to `measure.BLIND_SPOT_REGISTER`, and optionally extend `measure.CONTRACT_FILES` beyond the two shared files. | Both are pinned to the committed baseline — `a_baseline_contracts.py:224` asserts `len(register) == len(measure.BLIND_SPOT_REGISTER)`, and `:297` pins the anchor registers. Changing either needs a baseline regeneration, which no packet has claimed, and which **Q1 does not cover**. | **Yes for the blind-spot register; optional for `CONTRACT_FILES`.** The blind-spot gap is a *live correctness defect* that `QUALITY_GATE.md:39` routes **every future CSS packet** into, and `A_BASELINE_EVIDENCE.md:181`'s claim that "the register cannot drift from the file it describes" is false in the only direction that matters. **This arc is safe either way** — P3-a1 owns complete P3-local registers regardless (see *Changes to the packets*), so a refusal costs nothing here and only leaves the shared defect standing for the next arc. That is the owner's call, not the packet's. |
| **Q9** *(new)* | **Which WP4.4 constraints does this arc still carry?** `.claude/rules/verification.md:21–24` retires arc-specific constraints when the arc closes. WP4.4 is closed. The owner re-issued R4, N2, C8, G4 and the method rules; Plan v1 additionally self-bound to ~20 others. | An arc that invents its own authority is the failure mode this whole document exists to avoid. It also determines whether the token-block packet's M9 exclusion still binds. | **Accept the P-constraint restatement in Plan v2 (P-1 … P-8)** rather than re-issuing twenty WP4.4 numbers. Constraints with a durable home in `.claude/rules/verification.md` are cited there and need no owner action; the arc-specific remainder is restated under this arc's own numbering. |

**No question here is answerable by an agent.** Q1, Q3, Q6, Q8 and Q9 each change what the arc
is allowed to produce; Q4 and Q5 change how it is executed and recorded.

---

### Section 0 sign-off — GATE 0

**Status: PENDING — presented together with Plan v2, at owner direction. NOT APPROVED.**

- [ ] User confirms the acceptance criteria match intent.
- [ ] User reviewed the assumptions and corrected or accepted each one.
- [ ] Blocking questions **Q1, Q3, Q4, Q5, Q6, Q8, Q9** are answered. *(Q2 and Q7 withdrawn at
      council — see the table above.)*
- [ ] **Q9 specifically**: the P-1 … P-8 constraint restatement in Plan v2 is accepted, or the
      owner names which WP4.4 constraints to re-issue instead.

---

## Plan v1

> **Historical. Superseded by Plan v2 below.** Retained verbatim as the audit trail the
> council reviewed. Where it conflicts with Plan v2 — the base commit, the two-not-three
> contract ceilings, AC4's frozen-DB wording, the F3/F5 family split, the 24-block budget
> attribution, and every constraint it self-inherited from the closed WP4.4 arc — **Plan v2
> governs**. Section 0 above has been amended in place because Gate 0 is unsigned; Plan v1 has
> not.

**Goal**: Measure, declaration by declaration, how much of `static/css/theme-dark.css` can
never win — using a rebuilt, committed, red-path-proven removal oracle rather than a census —
and delete exactly the certified non-winners, leaving the file linked, nonempty, and
byte-identical if nothing certifies.

**Nothing in this session implements anything.** No packet is executed, no worktree is
created or moved, no `senior-developer` is dispatched, and the only file written is this
artifact.

### Scope

- **In**: the committed oracle rebuild; the whole-file classification; the certified deletions
  in two separately-certified production packets; per-packet contracts and evidence docs; the
  integration/closeout packet.
- **Out**: everything under Section 0 "Out of scope / non-goals" — most importantly **R4**
  (the file stays linked and `templates/base.html` is frozen), making the file win, **N2**,
  **C8**, **G4**, **R1**, the other six shared surfaces, every page bundle, `scss/**`, and any
  snapshot rebaseline.

### Why the ordering is what it is

Every packet in WP4.4 failed at its oracle before it failed anywhere else. `h` threw away
**four** measurement cycles — two to `TESTING=1`, one to an animation-seek race, one to a
port collision between two harnesses using different databases. `i` shipped a G3 gate that
recorded a file no admissible repair touched, and an M4 self-check that reported 0 mismatches
unconditionally; both passed and neither could fail. `j` found its own animation freeze only
because its same-CSS control failed on one context.

So this arc is ordered **instrument → measurement → checkpoint → deletion → integration**,
and the instrument packet ships **before any classification result exists to bias it**. A
combined "build the tool and use it" packet is how you get a tool tuned until it agrees with
the answer you already have.

### Packets — five

| # | Packet | Nature | Writes production CSS? | Visible rendering may change? |
|---|---|---|---|---|
| 1 | **P3-a** — oracle restoration and certification | tooling + tests | **no** | **no** |
| 2 | **P3-b** — whole-file classification and the go/no-go checkpoint | read-only measurement | **no** | **no** |
| 3 | **P3-c** — certified paint-declaration deletion | production | **yes** | **no** |
| 4 | **P3-d** — certified legacy token-block deletion | production | **yes** | **no** |
| 5 | **P3-e** — integration, closeout and status reconciliation | documentation | **no** | **no** |

**DAG** — linear, with one owner checkpoint:

```
P3-a ──(evidence: no classification is admissible without a certified instrument)──▶
P3-b ──(OWNER CHECKPOINT: abandonment decision on measured yield)──▶
P3-c ──(shared-file exclusivity: same production path, strictly serialized)──▶
P3-d ──(integration dependency)──▶ P3-e
```

**Concurrency classification.** Every production packet writes the same file, so per the
four-label scheme: P3-a and P3-b are **(b) parallel read-only audit only** with respect to
`theme-dark.css`; P3-c and P3-d are **(d) single-writer shared file** and also **(c)
sequential by cascade coupling**; P3-e is **(c) sequential**. **No pair in this arc may run
concurrently.** Stating it once here rather than re-litigating it per session, per
`.claude/rules/verification.md`.

---

#### P3-a — Oracle restoration and certification

*Tooling packet. Writes no production CSS. This is the packet that makes M-h3 satisfiable.*

| Attribute | Value |
|---|---|
| **Production paths owned** | **none.** `git diff static/css/` must be empty, asserted by this packet's own contract. |
| **New committed paths owned** | `scripts/css_audit/p3_census.mjs`, `p3_removal_oracle.mjs`, `p3_zero_winner_check.mjs`, `p3_ranges.mjs`, `p3_build_manifest.mjs`, `p3_apply.mjs`, `p3_family_controls.mjs`; `tests/test_css_theme_dark_p3_instrument_contracts.py`; `docs/CSS_THEME_DARK_P3_A_ORACLE_EVIDENCE.md` |
| **Reused unmodified** | `scripts/css_audit/j_theme_differential.mjs`, `j_diff_theme.mjs`, `j_theme_dark_inventory.mjs`, `j_shadow_certification.mjs`, `j_known_live_mutation.mjs`, `i_seed_probe_db.py`, `measure.py`, `specificity.py`, `resolution_check.py`, `stylelint_surfaces.mjs` |
| **Explicit exclusions** | no production CSS, no template, no JS, no existing contract file. `tests/test_css_cascade_contracts.py`, `tests/test_visual_selector_contracts.py`, `tests/test_css_wp4_4_*_contracts.py` are **run always, edited never**. |
| **First step, before any code** | Attempt **recovery** of the WP4.4-h harness (`git stash list`, `git log --all --diff-filter=D -- 'artifacts/wp4_4/h_*'`, any surviving `wt/` worktree). Recovering reviewed code beats rewriting it. Record the outcome either way. |
| **Second step** | Re-measure and pin the arc base: `theme-dark.css` line count, rule count, brace count, `!important` declarations in all three reconcilable units, custom-property declarations, seven-surface Stylelint totals, and the digest. **No later packet may inherit a figure from this planning document.** |
| **Rollback** | Not applicable — no production file is modified. A failing instrument control blocks P3-b outright rather than being waived. |

**Deliverable, stated as a bar rather than a file list:** an oracle that a reviewer can break.
Each tool ships with a recorded **red-path proof** — the exact input that makes it fail — and
the fatal-control set from WP4.4-h §7.3, which is what turned h's first certification from
"zero differences" into a real result:

| Control | What input makes it fail |
|---|---|
| Known-live spikes | ≥5 declarations independently proven live are carried in a **separate result set**; the run is **fatal-failed** if any one is not reported LIVE. |
| Idempotence | removing and restoring twice must produce identical readings. |
| Restoration | every removed declaration must be restored and the restoration verified. |
| CSSOM↔source alignment | every candidate must resolve to exactly one source rule; **any** unresolved candidate fails the run. |
| Candidate disposition | a candidate classified `live`, `neverProbed`, `reachedNothing` or unresolved **fails the run** rather than being silently retained. |
| Selector identity | postcss↔CDP matching requires three normalizations — strip CDP's leading `& ` on nested rules, canonicalize attribute quotes (`[data-theme='dark']` → `"dark"`), strip the ` !important` suffix CDP puts in the *value* field. Without them, h's tools mismatched **93 of 103** candidates and reported it as "unmatched". |
| Offset model | the applier must reproduce the pristine digest by re-encoding the untouched string before it cuts. postcss reports **character** offsets, not byte offsets, and the file is CRLF — h lost a cycle to each. |

**In-file known-live spikes — where they come from for this file.** h's spikes came from
`components.css` declarations that obviously win. This file has no such obvious set, which is
the whole problem. P3-a must establish spikes **inside `theme-dark.css`**, and the strongest
candidates are the Workout Plan Controls pastel input rules at `:438–535` (`#min_rep`,
`#max_rep_range`, `#rir`, `#rpe`, `#weight`, `#sets`) — distinctive literal colours
(`#fce4ec`, `#e8f5e9`, `#fff9c4`) that are visible in dark mode and that nothing else in the
app is likely to declare. If P3-a **cannot** find a live declaration inside
`theme-dark.css`, that is itself a major finding (the file is entirely inert) and must be
reported as such; the spikes then fall back to the `--bg-primary` token whose liveness j
already measured at 12 dark / 0 light values.

**Gates for P3-a**

| Gate | Requirement |
|---|---|
| `pytest` | **full suite**, including the new instrument contract file and every existing cascade contract. |
| Production CSS diff | **empty**, asserted by contract. |
| Instrument controls | every control above green, each with its recorded red path. |
| Stylelint | seven-surface measurement **recorded as the arc anchor**; not gated (nothing changed). |
| E2E / visual / N8 | **not run.** No CSS changed; running them would produce a pass that means nothing. |

---

#### P3-b — Whole-file classification and the go/no-go checkpoint

*Read-only measurement. Writes no production CSS. Ends at an owner checkpoint.*

| Attribute | Value |
|---|---|
| **Production paths owned** | **none.** `git diff static/css/` must be empty, asserted. |
| **Evidence paths owned** | `docs/CSS_THEME_DARK_P3_B_CLASSIFICATION_EVIDENCE.md`; generated output under gitignored `artifacts/theme_dark_p3/b/` |
| **Scope** | every declaration in `theme-dark.css`: classify as winner / non-winner / uncertifiable / excluded, per declaration, with the **winning owner named** for every non-winner claim. |
| **Exclusions** | interaction-state, pseudo-element and JS-class declarations (Q6); the 8 uncertifiable Welcome elements (C7); anything the transition-suppression verifier could not clear. |
| **Rollback** | not applicable — read-only. A failed same-CSS control or a dead per-family live control **voids the run**; its numbers may not be quoted and the run is repeated after repair. |

**Candidate families this packet must classify separately.** Read off the file at this base
and offered as **nominations, not warrants** — membership is the measurement:

| Family | Where | Why it is a separate family |
|---|---|---|
| **F1 — legacy token block** | `:2–22`, 16 custom-property declarations | Every name is redeclared unwrapped at `:550–574` at (0,1,0), later in document order. But M9 excludes custom properties from the non-winner rule, and j's control re-points *both* blocks, so its result does not separate them. Needs a `var()`-consumer proof, not an ownership sweep. **Owned by P3-d, not P3-c.** |
| **F2 — `:where()`-wrapped `!important` paint** | the bulk of `:25–535` | The family the finding names. Exactly **one** member is measured: `background: none !important` at `:361` wins nowhere. Every other member's status is unknown. |
| **F3 — `:where()`-wrapped *normal* declarations** | `:190`, `:194`, `:200–225`, `:239`, `:249`, `:268`, `:273`, `:278`, `:282`, `:306` | At (0,0,0) with no importance these lose to essentially any competitor — the highest a-priori non-winner density in the file. **But `:where([data-theme="dark"] .hero-section)` at `:282` paints the Welcome hero, and C7 registers 8 Welcome elements as uncertifiable.** Part of F3 is out of reach of any rest-state instrument this repository has. |
| **F4 — Workout Plan pastel input rules** | `:438–535` | The one region that plausibly wins. Treated as **expected-live spikes**, not as candidates. j called them live under C11 preservation; this packet measures rather than inherits. |
| **F5 — interaction-state / pseudo-element / JS class** | `:58`, `:151`, `:157`, `:172`, `:177`, `:185`, `:207`, `:220`, `:268`, `:352`, `:403`, `:447`, `:474`, `:501`, `:519–544` | Out per Q6. Enumerated so the exclusion is a counted bucket, not an omission. |
| **F6 — reduced-motion `@media`** | `:538–544` | Requires a capture under its own condition (M11). Preserved by a WP4.4-j contract regardless of classification. |

**The checkpoint.** P3-b ends by presenting, per family: the census non-winner count, the
zero-winner recount, the removal-oracle `deadCertified` count, the **intersection**, and every
exclusion bucket with its count. That table is the input to the abandonment decision below.
**P3-b does not delete anything and does not decide.**

**Gates for P3-b**

| Gate | Requirement |
|---|---|
| `pytest` | full suite (nothing should move; a move means the packet touched something it should not have). |
| Production CSS diff | **empty**, asserted. |
| Same-CSS control | zero differing records on both halves, reported raw alongside the result. |
| Per-family live controls | each family's own control moves ≥1 value in its own theme and 0 in the other, or that family is excluded. |
| E2E / visual / N8 | **not run** — nothing changed. |
| Stylelint | re-measured and reconciled against the P3-a anchor; unchanged expected. |

---

#### P3-c — Certified paint-declaration deletion

*Production packet. Single writer on `static/css/theme-dark.css`.*

| Attribute | Value |
|---|---|
| **Production paths owned** | `static/css/theme-dark.css` — **exclusively**, for the duration. |
| **Evidence/test paths owned** | `tests/test_css_theme_dark_p3_contracts.py`; `docs/CSS_THEME_DARK_P3_C_DELETION_EVIDENCE.md` |
| **Scope** | families **F2** and **F3** only, and within them only declarations in the certified intersection from P3-b. |
| **Explicit exclusions** | F1 (custom properties — P3-d); F4 (live); F5 (Q6); F6 (contract-preserved); the 8 uncertifiable Welcome elements; every `neverProbed` / unresolved / uncovered record; the comment at `:546–548` (Q2). |
| **Hard ceiling** | at most **24** brace-opening blocks may be removed whole before `test_theme_dark_is_still_linked_and_nonempty` reds (74 → 50). Custom-property count must stay at exactly **34**. |
| **Diff shape** | **pure removal** — 0 insertions, no reformatting, no re-weighting, no new `!important`. Asserted by contract, the way h asserted it. |
| **Token value / visible rendering may change** | **no**, on both counts. A `yes` on either would require separate owner approval and is not requested. |
| **Rollback** | any computed-value difference in either theme; any dark difference; any light difference *at all* (a dark-only file that moves light rendering means the classification was wrong); any visual identity outside the recorded band or the schema-v2 ledger; any Stylelint category rise without a recorded exception; any cascade-contract red. Rollback, never rebaseline. |

**This packet's own contract must close the gap it inherits.** WP4.4-j's
`test_the_certified_removals_stay_removed` asserts `occurrences <= 1`, which passes at zero —
so **deleting j's surviving winner would pass it silently**. That is a gate that cannot fail
in one direction. P3-c's contract asserts each retained winner **positively present** (h's
pattern for its two withdrawn declarations), and asserts every exclusion bucket as a count,
because a prose exclusion is unenforceable.

**Gates for P3-c — the full `static/css/**` shared-surface set**

| Gate | Requirement |
|---|---|
| `pytest` | **full suite.** `tests/test_css_cascade_contracts.py` and `tests/test_visual_selector_contracts.py` run inside that total and are **not edited**. |
| Chromium, required nine | `smoke-navigation`, `nav-dropdown`, `accessibility`, `dark-mode`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening`. |
| Windows visual matrix | full `visual.spec.ts` — **66 tests per platform**, run with **`PW_VISUAL_SEED=1`** (without it 36 of 66 fail on a page-*height* mismatch on unmodified CSS too). Failure **identities** must be identical before and after; the animated-logo red is reconciled as a **band** (875/882 ∪ 1,039/1,046). `git status e2e/__screenshots__/` empty. |
| Stylelint | `node scripts/css_audit/stylelint_surfaces.mjs`, all seven surfaces. **No category may rise on any surface** without a recorded owner exception. Anchored to the P3-a arc base, never to WP4.1. |
| Linux N8 deep gate | `visual-linux` (`visual_mode=compare`), reconciled against `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` **schema v2** — 11 inherited reds across two spec files (`visual.spec.ts` 10 + `visual-baseline-thumbnails.spec.ts` 1). A red on a file **not** in the ledger is a rollback trigger. |
| Whole-page computed differential | before/after over 11 routes × 2 themes × 3 widths = **66 contexts**, both halves' own same-CSS controls green, served digests different, roots different. **0 dark / 0 light.** |
| Per-family live controls | re-run at this packet's digests; each certified family's control moves ≥1 value in its own theme, 0 in the other. |
| Snapshots | **none regenerated.** `--update-snapshots` not run. |

---

#### P3-d — Certified legacy token-block deletion

*Production packet. Single writer. Separately certified and independently abandonable.*

| Attribute | Value |
|---|---|
| **Production paths owned** | `static/css/theme-dark.css` — exclusively, **after P3-c has merged**. |
| **Evidence/test paths owned** | `tests/test_css_theme_dark_p3_tokens_contracts.py`; `docs/CSS_THEME_DARK_P3_D_TOKENS_EVIDENCE.md` |
| **Scope** | family **F1** only — the 16 custom-property declarations in the `:where([data-theme="dark"])` block at `:2–22`, if and only if each is certified. |
| **Why it is separate** | M9 and `test_every_custom_property_declaration_survives` both exclude custom properties from the non-winner rule, and for a good reason: a `var()` consumer in any of the other twenty hand-maintained sources keeps a token live, and proving otherwise needs a **dependency graph**, not an ownership sweep. This packet must supply that graph *and* a removal-oracle result — a strictly higher bar than P3-c's, on a family of 16. |
| **The distinct proof obligation** | for each of the 16: (a) the unwrapped block at `:550` declares the same name, matches the same element, and is later and more specific; (b) a `var()`-consumer graph over all 21 hand-maintained sources shows no consumer resolves to the earlier declaration; (c) the removal oracle reports `deadCertified`; (d) a **per-token** known-live control — re-pointing *only the earlier* declaration — moves **0** values, while re-pointing *only the later* one moves **>0**. (d) is the control j could not perform, because its mutation hit both lines. |
| **Contract consequence** | deleting any of the 16 **reds `test_every_custom_property_declaration_survives` (exactly 34)**. This packet cannot ship without the **Q1** ruling. If Q1 is refused, P3-d does not exist and the arc ends at P3-c. |
| **Rollback** | as P3-c, plus: any token whose per-token control cannot separate the two blocks is retained, not argued about. |
| **Gates** | identical to P3-c's full set. |

---

#### P3-e — Integration, closeout and status reconciliation

*Documentation packet. Writes no production CSS.*

| Attribute | Value |
|---|---|
| **Production paths owned** | **none.** |
| **Paths owned** | `docs/CSS_THEME_DARK_P3_E_INTEGRATION_EVIDENCE.md`; status updates to `docs/MASTER_HANDOVER.md`, `docs/ACTIVE_DEVELOPMENT.md`, `docs/REFACTOR_PLAN.md` — each a never-claimed shared path, **one writer, at integration only**. |
| **Scope** | rebase onto all predecessors; run the full gate set once more on the integrated tree; take an **arc-base → arc-end** computed differential over all 66 contexts; re-measure seven-surface Stylelint against the P3-a anchor; reconcile the per-packet deltas against a single `git diff --numstat` of the whole arc so no contribution is double-counted or missing; assert every per-packet contract file exists and is collected (**N1** — no consolidation); record what remains deferred (R4, C8, G4, and anything P3-b surfaced and this arc could not act on). |
| **Mandatory reconciliation discipline** | WP4.4-k *claimed* to reconcile three status documents together and updated only each file's **lead block**; all three still asserted "packet i is active" in their trailing sections, and `## Next Safe Step` — the one section a new session acts on — was among them. **Grep each whole file for the live claim and confirm every remaining hit sits inside a `>` supersession blockquote.** |
| **Gates** | `/verify-suite` (full pytest + full Chromium), full Windows visual matrix, Stylelint re-measure, Linux N8 deep gate, arc-wide differential 0/0. |

---

### Oracle design

*This section is the plan. Everything above is scheduling.*

**The governing fact: on this file, a zero from the differential is not evidence.** If the
bundle is inert, deleting from it moves zero computed values. If the instrument is broken, it
also reports zero. Those are indistinguishable without a control that fires *in the region
under test*. j's shadow-winner control returning 0/0 is the proof that this is a live hazard
here, not a theoretical one.

| # | Rule | What it prevents | What input makes it fail |
|---|---|---|---|
| **O1** | **Every deletion family carries its own committed, digest-pinned known-live mutation, sited inside that family's own region.** A family whose control moves zero is **excluded from deletion**, not passed. | The whole-file failure mode above: a global control (j's `--bg-primary`, 12 values on volume-splitter tables) proves the instrument works *somewhere*, and says nothing about the region a packet actually cut. | A family control that moves 0 values → that family is excluded and the packet shrinks. |
| **O2** | **Known-live spikes must include declarations from `theme-dark.css` itself**, carried in a separate result set, with a missing spike a **fatal run failure**. Best candidates: the Workout Plan pastel input rules at `:438–535`. If none can be found, "the file is entirely inert" is the finding and must be reported. | h's design gap, stated in its own §7.3: *"a run containing only deletion candidates can return zero differences both when every candidate is dead and when the oracle is blind."* | The oracle reporting anything but LIVE for a spike. |
| **O3** | **Name the winner, don't just observe the absence.** For every non-winner claim, record which declaration actually owns that longhand on every matched element, keyed **line-free** — `sheet \| selector \| property \| value \| important \| specificity \| layers`. | "Nothing changed when I removed it" is compatible with "the probe never reached it". Naming the owner makes `neverProbed` visible instead of invisible. A line-keyed identity would report the whole file as changed, because deletion renumbers. | A candidate with no named owner on some matched element → `neverProbed`, retained, counted. |
| **O4** | **M-h2 seeding and probe isolation.** Frozen seeded probe DB via the committed `scripts/css_audit/i_seed_probe_db.py`; `TESTING` **unset**; an explicit `DB_FILE` for *every* harness; WAL/SHM sidecars deleted before restore; DB digest asserted at start and end; port 5000 asserted free before the server starts; one listener PID at every guard checkpoint; never two probes overlapping. | h lost two cycles to `TESTING=1` (21,693 → 37,915 DOM nodes; dead 342 → 388) and one to two harnesses binding 5000 with **different** databases — `/backup` rendered 279 nodes in one run and 235 in the other under byte-identical CSS, producing 5,486 false computed differences. | A non-free port, a second listener PID, a DB digest that moves mid-run, or `TESTING` set. |
| **O5** | **M6a / M-h1, made falsifiable.** Suppress transitions before applying, reading **and** removing the sentinel — and then **verify per element that the suppression actually won**, by reading back `transition-duration`. Any element still reading non-zero is registered **uncertifiable**, never silently measured. Animations: `pause()` **then** `currentTime = 0` (never the reverse), plus CDP playback rate 0 so animations starting later are also stopped, plus a verifier that each animation sits *at* its canonical instant (0 for infinite, `endTime` for finite). | The committed CSS-only universal `transition: none !important` suppressor in `runtime_probe.mjs` is **beatable** — by layered `!important` and by more-specific unlayered `!important`, which is precisely the cascade shape this file lives in. WP4.4-f2 proved this with a transitioned known-live control and 7 externally settled `CSSTransition` objects. And "paused" alone is insufficient: an animation registering mid-pass pauses at an arbitrary phase that reads **stably within a run** and differently between runs. | An element whose `transition-duration` does not read `0s` after suppression; an animation not at its canonical instant. |
| **O6** | **Provenance is content.** Every capture records checkout root, on-disk digest, **served** digest (the bytes the browser cascaded), frozen-DB digest, network-cache manifest and PID. The differ refuses: same-root pairs (unless the control opts in explicitly), equal served digests, a half whose own control failed, and empty comparisons. | i's *primary* oracle compared two states via an in-place file swap from one root, leaving no proof of which bytes were served when; it had to be re-captured. | Reuse `scripts/css_audit/j_diff_theme.mjs` unmodified — it already implements all four refusals. |
| **O7** | **The pixel matrix is a regression gate for this arc, not an evidence source.** `prepareForScreenshot()` neutralizes `backdrop-filter` / `-webkit-backdrop-filter` globally; `background`, `background-image`, `border-color`, `border-radius`, `box-shadow` and `text-shadow` on `[data-visual-surface][data-visual-surface]` **in dark only**; and `border-radius` / `box-shadow` / `text-shadow` on form controls. | Those properties are the large majority of `theme-dark.css`, and the blind-spot register names **j** on three of its six rows. A packet citing "the visual matrix is unchanged" as evidence for a `backdrop-filter` deletion is citing a property the harness erased before the shutter opened. | Any evidence claim for a register-covered property that does not carry a computed-style differential. |
| **O8** | **Uncertifiable sets are registered, not dropped.** The 8 infinite-animation Welcome elements (C7) plus any element failing O5's suppression verifier. No declaration affecting them may be classified dead on this harness's authority. | This is not theoretical here: `:where([data-theme="dark"] .hero-section)` at `:282` paints the Welcome hero directly, so part of family F3 is structurally out of reach. | A candidate whose matched set intersects the uncertifiable set → excluded, counted. |
| **O9** | **Interaction states, pseudo-elements and JS classes declared out up front (M12).** An inline sentinel cannot address a pseudo-element; interaction states animate, so their proof is unreliable until a control reaches zero. | WP4.3i-dead's same-CSS control on exactly this class produced 52 differing records and correctly shrank that packet from 24 declarations to 14. h declared them out up front and did not re-open the ground. | Any candidate matching family F5 → excluded before classification, with a count. |
| **O10** | **Deletion geometry is proven before it cuts.** postcss reports **character** offsets, not bytes; the file is CRLF; a whole-rule deletion absorbs its contiguous leading comment block and a declaration absorbs its trailing same-line comment — **except** where a contract pins the comment text (Q2). The manifest builder is trusted only after it reproduces a known-good manifest **exactly**; the applier re-encodes the untouched string to the pristine digest before it cuts anything. | h hit both offset hazards. Either one lands a cut mid-declaration while still producing a plausible-looking diff. | A re-encode that does not reproduce the pristine digest; a manifest that does not reproduce the reference. |
| **O11** | **Contract identity by `(selector, line)`, never by `(selector, nth occurrence)`.** | In `components.css`, occurrence-keyed assertions silently resolved **10 of 19** rules to the wrong rule, several inside `@layer workout` where the packet never reached. The line-anchored form reds instead of drifting. | A moved rule → the assertion reds, which is the point. |

**Two design points specific to this arc, which no WP4.4 packet faced:**

1. **Non-winning is the null hypothesis here, so the burden inverts.** In `components.css`
   most declarations win, and a non-winner claim was surprising. In `theme-dark.css` the
   finding predicts most declarations lose, so a non-winner result is *unsurprising and
   therefore uninformative on its own*. The removal oracle plus O1 plus O3 are what convert
   an unsurprising observation into a warrant. This is the reason the arc is instrument-first.
2. **Custom properties need a different instrument entirely.** A removal oracle removes a
   declaration and re-reads computed values; for a custom property, the consumers are
   everywhere and the effect is indirect. P3-d's obligation (d) — re-point *only* the earlier
   declaration and *only* the later one, separately, and show the split — is the control j's
   mutation could not perform because it rewrote both lines in one pass.

---

### Effort and sequence

**Effort**: P3-a **L** · P3-b **M** · P3-c **M** · P3-d **S** (16 declarations, highest proof
bar per declaration in the arc) · P3-e **S/M**.
**Owner**: one implementer, one worktree, strictly sequential.
**Depends on**: WP4.4 closed at `k` (`c521d3a`); proposal **P1** merged (PR #223 — appears
satisfied, see assumptions); proposal **P2** status confirmed (**Q7**).

1. **Gate 0** — owner answers Q1–Q7. *(Presented with Plan v2 per owner direction.)*
2. **`/council-plan`** — three reviewers in parallel against this artifact → response matrix →
   Plan v2. **Gate 1.**
3. **P3-a.** Attempt harness recovery; re-measure and pin the arc base; build or restore the
   oracle set; prove every red path; ship with a contract file. Merge.
4. **P3-b.** Classify the whole file. Present the per-family intersection-and-exclusion table.
   **Stop at the checkpoint.**
5. **Owner checkpoint** — apply the abandonment criterion below. Three outcomes: proceed to
   P3-c; proceed to P3-c with a narrowed family set; or **end the arc as audit-only**.
6. **P3-c.** Delete the F2/F3 intersection. Full gate set. Merge.
7. **P3-d.** Only if **Q1** was granted and family F1 certified. Full gate set. Merge.
8. **P3-e.** Integrate, reconcile, close.

---

### Expected gates per packet

*(Derived from the `static/css/**` row of `docs/ai_workflow/QUALITY_GATE.md`, merged on `main`
via P2 / PR #222 — Q7's caveat is withdrawn — and cross-checked against `_K_INTEGRATION_` §7,
`_J_THEME_DARK_` §7, `_H_COMPONENTS_DEAD_` §10 and `_A_BASELINE_` §12, which agree. Superseded
by the Plan v2 gate table below.)*

| | P3-a | P3-b | P3-c | P3-d | P3-e |
|---|---|---|---|---|---|
| Full `pytest` (cascade contracts inside the total) | ✔ | ✔ | ✔ | ✔ | ✔ |
| Required nine Chromium specs | — | — | ✔ | ✔ | ✔ (full suite) |
| `visual.spec.ts`, 66/platform, `PW_VISUAL_SEED=1` | — | — | ✔ | ✔ | ✔ |
| Seven-surface Stylelint, no category rise | anchor only | reconcile | ✔ | ✔ | ✔ |
| Linux N8 deep gate vs schema-v2 ledger (11 / 2 specs) | — | — | ✔ | ✔ | ✔ |
| Whole-page computed differential, 66 contexts, 0/0 | — | control only | ✔ | ✔ | ✔ arc-wide |
| Per-family known-live controls (O1) | red-path proofs | ✔ | ✔ | ✔ per token | — |
| Production CSS diff empty (asserted) | ✔ | ✔ | — | — | ✔ |
| No snapshot regenerated; `--update-snapshots` never run | ✔ | ✔ | ✔ | ✔ | ✔ |

**Read-only packets do not run the E2E or visual gates.** Nothing changed, so a pass would
carry no information — and a gate that cannot fail is worse than no gate.

---

### Abandonment criterion

**WP4.4's N3 pre-authorized abandonment as an acceptable arc outcome rather than a failure.**
This arc adopts that precedent explicitly, at two named points, on measured conditions.

**AB-1 — instrument failure, at P3-a.** If the rebuilt removal oracle cannot satisfy its
fatal controls — specifically if it cannot report **LIVE** for every one of its ≥5
independently proven live spikes, or if it records any idempotence, restoration or
CSSOM↔source-alignment failure, or if any candidate rule fails to resolve — then **the arc
stops at P3-a**. The instrument work is recorded, no classification result is quoted from a
failed run, and `theme-dark.css` is not touched. An oracle that cannot fail on a known-live
input grants no deletion authority.

**AB-2 — empty certified yield, at the P3-b checkpoint.** The arc proceeds to P3-c only if the
certified intersection — census non-winner **∩** independent zero-winner recount **∩**
removal-oracle `deadCertified` — is **non-empty for at least one family whose own known-live
control fired (O1)**. If the intersection is empty, or if every candidate lands in an
exclusion bucket (`neverProbed`, unresolved, no blast coverage, uncertifiable element,
interaction-state-only, media-condition-only-without-capture), then **the arc ends at P3-b as
an audit**: the measured per-declaration distribution is published, `theme-dark.css` is left
**byte-identical** to its arc base, and the finding is recorded as *measured and not
actionable under current constraints*. That is a success. It converts a standing "a far larger
reduction is likely available" into a measured answer, which is the durable deliverable
whichever way the number falls.

**AB-3 — per-family narrowing, continuously.** Abandonment is not all-or-nothing. Any family
whose live control does not fire, or whose candidates all land in exclusion buckets, is
dropped from the deletion set and the arc continues with the rest — the N3 "narrow, then
abandon" shape. P3-d is independently abandonable and is expected to be dropped outright if
**Q1** is refused.

**What is explicitly NOT an abandonment trigger, and not an acceptance criterion either:**

- **A line-count shortfall is not a reason to abandon, and a line-count achievement is not a
  reason to accept.** WP4.4-f1 shipped **one rule** against a projected −150 to −400, and that
  was the correct outcome. C10 states it directly: projections and line counts are not
  acceptance criteria. This plan therefore proposes **no line-count target**, and any figure
  quoted at closeout is a report.
- **A removal-oracle contradiction is handled by exclusion, not abandonment.** h's oracle
  contradicted its census on 2 of 103 candidates; the correct response was to withdraw those
  two and ship 101, and to assert their continued presence *positively* so a later packet
  could not delete them by omission.
- **A failed same-CSS control, or a family control that does not fire, voids the run** — its
  numbers may not be quoted — but it is a re-instrument-and-repeat condition, not an
  abandonment.

---

### New owner decisions surfaced by Plan v1

*Gate-1 decisions, additional to the Gate-0 questions Q1–Q7 above.*

- **D1 — Does P3-c require its own owner checkpoint before the first cut,** in the way **N4**
  required one before WP4.4-i? Plan v1 assumes **yes**: step 5 above stops for it, with the
  P3-b intersection-and-exclusion table as the presented artifact.
- **D2 — Per-packet contract files, permanently, with no consolidation at closeout** — the
  **N1** answer, carried into this arc. Plan v1 assumes yes; P3-e asserts the files exist and
  are collected and may not merge them.
- **D3 — May P3-e append per-packet status lines to `MASTER_HANDOVER.md` /
  `ACTIVE_DEVELOPMENT.md` / `REFACTOR_PLAN.md` at merge time,** or must all status writing
  wait for closeout? WP4.4 permitted per-packet appends as an owner-coordinated step (A14).
  Plan v1 assumes the same.
- **D4 — Does the arc need a `theme-dark`-specific row or note in `QUALITY_GATE.md`?** Plan v1
  assumes **no** — the existing `static/css/**` row already routes it. Recorded so the answer
  is deliberate rather than absent.

---

## Agent provenance

*Required for every council run. The manager records each agent ID returned by its `Agent(...)` call and supplies the `product-manager` its own ID back, because an agent cannot know its own ID. The `product-manager` stamps the IDs the manager supplies — **never invent an ID**, never rerun completed council work to manufacture continuity, and record an unrecoverable ID as an evidence gap.*

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `a72cabec430ff9c82` | Author of Section 0 and Plan v1. |
| `product-manager` — response matrix + Plan v2 | `a72cabec430ff9c82` | Author of the matrix, the Section 0 amendments and Plan v2. |
| `architecture-reviewer` | `a0cf22638cb17fefb` | Step 2 reviewer. Verdict: **BLOCKING**, 15 findings. |
| `test-strategist` | `a2b52c47a43c8c917` | Step 2 reviewer. Verdict: **approve-with-changes**, 11 findings (#3 and #5 must-fix). |
| `product-risk-reviewer` | `a04a1ab89adadd267` | Step 2 reviewer. Verdict: **approve-with-changes**, 7 findings (#1 and #2 must-fix). |
| `architecture-reviewer` — **Plan v2 re-review** | `a9ceef15d1ad059e4` | Re-review of Plan v2. **BLOCKING lifted → approve-with-changes.** 13 of 15 originals cleared, #14 recorded, **#12 not cleared**; **#11 retracted by the reviewer**; **8 new findings**. |

**Same product-manager resumed for the matrix + Plan v2?** **`yes`** — resumed via
`SendMessage` to the Plan v1 agent ID. All five IDs above are stamped exactly as the manager
supplied them; none was inferred, reconstructed or invented.

**Evidence gap** — `none` for agent identity and continuity.

**Separate gap, on relay completeness — not an identity gap:** see the banner at the head of
*Reviewer findings*. The reviewers' outputs were **not relayed verbatim**; the manager relayed
verdicts, counts, three converged findings and roughly a dozen individually described
findings. The matrix below covers every finding that was relayed and states, per reviewer, how
many were not. No finding text was invented to fill the arithmetic.

---

## Reviewer findings

> **Relay note (resolved).** An earlier revision of this document recorded that the reviewers'
> outputs had been summarized rather than relayed verbatim, and marked the template's
> "paste verbatim, do not summarize" requirement as unmet. The manager has since supplied all
> three in full; they are reproduced below unedited, and the response matrix now dispositions
> **all 33 findings**. The gap is closed. It is recorded rather than deleted because three of
> the dispositions below **changed** once the full text was available — see architecture #11,
> product-risk #2 and test-strategist #2 — which is the argument for the requirement.

### architecture-reviewer (agent `a0cf22638cb17fefb`) — verdict **BLOCKING**, 15 findings

Plan v1 cannot go to /council-plan as written. Nothing has shipped, so no damage — but three of the plan's own load-bearing claims are wrong against the files, and the single most important one (finding 1) defeats acceptance criterion 7, the plan's own "know the ceiling before the first cut" rule.

Charter items 1, 2, 3, 5, 6, 7 (module boundaries, blueprint triple, schema registration, response contract, logger, normalization) are N/A and correctly claimed — PLANNING.md:219-242 asserts a `none` calculation surface and no route/blueprint/schema/response-shape change, and that survives inspection. My findings are in the test-contract coupling, the family decomposition, and constraint-inheritance authority.

BLOCKING

1. PLANNING.md:123-137 — a third working-tree contract on theme-dark.css is missing from the ceiling analysis, and it has no amendment path. tests/test_css_cascade_contracts.py:1006-1007 (inside test_workout_plan_page_header_and_collapsible_frame_ownership_cleanup, defined at :950) reads the working-tree file and pins two literals: `assert ':where([data-theme="dark"] .frame-header) {' in theme_dark` and `assert "backdrop-filter: blur(8px) !important;" in theme_dark`. The first resolves to static/css/theme-dark.css:100; the second to :102. That rule is a :where()-wrapped !important paint rule — squarely inside family F2 (PLANNING.md:518, "the bulk of :25–535"). The plan says "Two further constraints bound the size of any answer" (:123) and names only the WP4.4-j and WP4.4-a files. Risk: P3-c certifies .frame-header dead and deletes it, redding a contract that PLANNING.md:457 declares "run always, edited never" and that ruling N6 (docs/css_phase4_wp4_4/PLANNING.md:1662) confines to packet i on lines 1614-1627 only — a different range, in a closed arc. Discovered at apply time, this is the exact cycle-cost Q2 was written to avoid. Fix: add the pin to the Section-0 ceiling table and open a Q8 asking whether P3-c may make an "explicitly scoped, justified, non-weakening" cascade-contract edit under the clause in docs/ai_workflow/QUALITY_GATE.md:32, or must exclude .frame-header from candidacy outright.

2. PLANNING.md:132-137 and Q2 at :363 — the comment-absorption hazard is misattributed and cannot arise from the plan's own deletion set. tests/test_css_wp4_4_a_baseline_contracts.py:128 does assert `"Zero !important. */" in theme_dark` — that part is verified. But the comment at static/css/theme-dark.css:546-548 is the leading comment of the rule at :550, and the arc never deletes :550: PLANNING.md:587 scopes F1 to "the 16 custom-property declarations in the :where([data-theme="dark"]) block at :2–22", and the :550 block is the retained winner in the plan's own shadowing argument. The only other neighbour is the @media at :538-544, which is F6 and preserved by contract. Risk: a blocking Gate-0 question consumes owner attention on a hazard that cannot fire, while the real one (finding 1) is never asked. Fix: withdraw Q2 as framed; keep the manifest-builder exception rule but derive it from the actual pinned strings — "Zero !important. */", ':where([data-theme="dark"] .frame-header) {', "backdrop-filter: blur(8px) !important;".

3. PLANNING.md:17 and :27 — the base SHA is the wrong commit. The plan pins main @ d543a4b. docs/MASTER_HANDOVER.md:1357 reads "d543a4b (PR #223) and P2 as 4b0670b (PR #222)" — d543a4b is P1, not the arc base; 4b0670b is P2 / PR #222, which is the base I was given for this review. Risk: every "counted by reading at this base" figure (:323-325), the digest pin, and the entire Q7 caveat are anchored to a commit that predates the static/css/** row's merge — which is precisely why the plan doubts its own gate derivation. Fix: re-pin to 4b0670b and re-state the base in :17, :27, :308 and :654.

4. PLANNING.md:301-308 and Q7 at :368 — the assumption is contradicted by the file it cites. docs/MASTER_HANDOVER.md:1376 reads "P1 and P2 are approved and merged — d543a4b (#223) and 4b0670b (#222)", and :1410 records PR #222 as "Owner-approved and merged (N10 discharged)". The plan states MASTER_HANDOVER "still records PR #222 as open, awaiting owner review". The row is present exactly where the plan says (QUALITY_GATE.md:32, :39, :60). Risk: one of seven blocking Gate-0 questions is not a question, and the plan carries a "gates may be derived from the wrong source" caveat through five packets for no reason. Fix: delete Q7; promote :301-308 to a verified fact citing docs/MASTER_HANDOVER.md:1376.

NEEDS REVISION BEFORE GATE 1

5. PLANNING.md:622 (O1) and :555 — the "≥1 in own theme, 0 in the other" control bracket is false for four rules in the file. static/css/theme-dark.css:239-246, :249-257, :259-262 and :268-270 carry no [data-theme="dark"] — they match in both themes (`:where(body), :where(.navbar)…{transition:…}`, `:where(#darkModeToggle){…}`, `:where(#darkModeToggle i){color:#0d6efd!important}`, `:where(#darkModeToggle:hover){opacity:.8}`). :239, :249 and :268 are listed as F3 deletion candidates at :519, and :555 makes "any light difference at all" a rollback trigger on the premise this is "a dark-only file". Risk: a correct live control on those rules moves values in both themes, which O1 reads as a failed control → "voids the run… re-instrument-and-repeat" (:738) — an unfalsifiable loop; and any legitimate deletion there trips the :555 rollback and the 0-dark/0-light gate at :573 by construction. Fix: split F3 into dark-scoped and theme-agnostic sub-families, give the theme-agnostic one a both-themes control bracket, and remove "dark-only file" from the :555 rollback wording.

6. PLANNING.md:519-522 — the family table is not a partition; four line ranges are double-assigned and one JS-applied rule is misfiled. :519 puts :200–225 and :268 in F3 (a P3-c deletion family); :521 puts :207, :220 and :268 in F5 (excluded); :521's :519–544 swallows :522's F6 range :538–544. Separately, static/css/theme-dark.css:213-218 (.tbl-view-mode-toggle.active, [data-view-mode="advanced"]) is JS-applied state and sits inside F3's :200–225 range while being absent from F5. Risk: acceptance criterion 2 (:158-159) requires exclusions to be counted buckets; overlapping ranges make the count unverifiable. And :213 is exactly the rest-state-sweep false positive that O9 (:630) cites WP4.3i-dead for. Fix: make F1–F6 a partition derived by the instrument rather than by reading, and move :213 into F5.

7. PLANNING.md:123 — the ceiling enumeration omits three more assertions inside the file it does name. In tests/test_css_wp4_4_theme_dark_contracts.py: :62 asserts `css.count(".value-changed") >= 7`, and the file contains exactly 7 (theme-dark.css:519, 520, 525, 526, 531, 532, 539) — zero headroom; :52 asserts `css.count("@media") == 1`, an exact equality, not a floor; :68 and :98 pin superset and @layer. Risk: criterion 7 (:182-186) requires each contract be named with its exact assertion and ceiling before Plan v2; the Section-0 "two constraints" framing understates it by a factor of five. Fix: replace the prose with a table covering theme_dark_contracts.py:32, 34, 35, 45, 52, 53, 55, 62, 68, 88, 98; a_baseline_contracts.py:128; cascade_contracts.py:1006, 1007.

8. PLANNING.md:40, 362, 365 — fifteen WP4.4 constraints are inherited without citing the authority that carries them. .claude/rules/verification.md ("Division of ownership") states that when the WP4.4 arc closes "its arc-specific constraints retire with it". WP4.4 is closed. The owner has re-issued R4 and N2; the plan additionally binds itself to C7, C8, C10, C11, G4, M9, M11, M12, N1, N3, N6, R1, R6, V1–V3. Q4 (:365) correctly notices R6 does not carry — and then applies that test to nothing else. Risk: Q1's recommendation "on the N6 pattern" (:362) invokes a ruling whose own text (docs/css_phase4_wp4_4/PLANNING.md:1662) grants amendment authority to packet i, on one line range of one file, in a closed arc. It is not a precedent a new arc can self-apply. Fix: add a Gate-0 item listing each inherited constraint for the owner to re-issue for P3, or restate each as a P3-owned constraint with its own number.

9. PLANNING.md:283-284 and :555 — G4 is restated with its operative half removed. docs/css_phase4_wp4_4/PLANNING.md:1550 makes "any change in superset row rendering a rollback trigger (PR#6), including a change produced by a packet that never opens pages-workout-plan.css". The plan reduces G4 to a textual check ("superset must appear nowhere in theme-dark.css"), and the P3-c rollback list never names superset rendering. Risk: P3-d deletes 16 custom-property declarations (--card-bg, --table-stripe, --hover-bg, --glass-*) that superset rows consume through var(); a superset rendering change trips no listed trigger. Fix: add superset-row rendering to the P3-c and P3-d rollback lists and to P3-d's var()-consumer route coverage.

10. PLANNING.md:589(b) — M9's route-coverage half is dropped from P3-d's proof obligation. docs/css_phase4_wp4_4/PLANNING.md:1536 requires the var() dependency graph across all 21 hand-maintained sources "plus route coverage for every consumer found". Obligation (b) requires only that "no consumer resolves to the earlier declaration". Risk: a consumer that exists but was never rendered on a probed route reads as "no consumer" — reintroducing the neverProbed failure that the plan's own O3 (:624) exists to prevent, in the packet with the highest per-declaration bar. Fix: append route coverage per consumer to obligation (b).

11. PLANNING.md:509, 519, 629 — the C7 exclusion set is not resolvable as assumed, and its one named member is an over-claim. docs/CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md:142 states the 8 element paths live in artifacts/wp4_4/runtime/summary.json; /artifacts/ is gitignored (.gitignore:55) and the plan's own assumption (:314-318) establishes that tree is gone. Only the class-level list survives, at A_BASELINE_EVIDENCE.md:139 — .hero-center-icon, .hero-card-1..6, .credit-heart, .developer-credit-banner::before. .hero-section (theme-dark.css:282) is the container, not one of the 8, and neither background nor backdrop-filter inherits onto them. Risk: the plan treats "the 8 uncertifiable Welcome elements" as a fixed, enumerable bucket and asserts at :519 and :629 that :282 is "structurally out of reach" — stated as fact, not measured. Fix: extend P3-a's recovery step (:458) to the C7 path list, re-derive it if unrecoverable, and demote the :282 claim to a nomination the instrument settles.

12. PLANNING.md:754 (D3) vs :455, 507, 549, 586 — D3 grants four packets an undeclared shared-path claim. :603 correctly names P3-e as the single writer of docs/MASTER_HANDOVER.md, docs/ACTIVE_DEVELOPMENT.md and docs/REFACTOR_PLAN.md. D3 proposes per-packet appends at merge time, and none of the four preceding packets' "Paths owned" rows list those three files. Risk: if D3 is granted as assumed, four packets write three never-claimed shared docs with no ownership row — the exact WP4.4-k reconciliation failure the plan documents at :605. Fix: if D3 is granted, add the three paths to every packet's "Paths owned" row with an append-only, lead-block-and-`## Next Safe Step` rule.

13. PLANNING.md:362 (Q1 recommendation) — "never converted to floors or >=" collides with the assertion it governs. tests/test_css_wp4_4_theme_dark_contracts.py:35 is `assert body.count("{") >= 50` — a floor by design, R4's nonempty guard, not a count. Risk: applied literally, Q1's rule converts an intentional floor into an exact pin. Fix: scope the "re-pinned exactly" rule to test_every_custom_property_declaration_survives:45 alone.

INFORMATIONAL (record, don't churn)

14. scripts/css_audit/i_seed_probe_db.py:68 and :93 — raw sqlite3.connect() rather than `with DatabaseHandler() as db:`. Charter item 4 would normally flag this. It is committed audit tooling outside the app.py → routes/ → utils/ chain, it takes an explicit --out rather than reading utils.config.DB_FILE, and PLANNING.md:456 reuses it unmodified — which is the right call for a certified harness. Fix: one line in the Calculation-surface section (:233-236) recording it as a deliberate, scoped exception, so code-reviewer does not re-litigate it per packet.

15. PLANNING.md:111-114 — the committed-harness inventory is incomplete. scripts/css_audit/ also contains emit_baseline.py, i_diff_computed.mjs, i_diff_g3.mjs, i_element_pixel_diff.mjs, i_five_route_computed.mjs, i_known_live_mutation.mjs, n4_regions_abc.mjs and visual_helper_band_proof.mjs. The plan's conclusion is unaffected — none is a removal oracle — but P3-a proposes writing seven new tools (:455) without assessing these eight. Fix: complete the inventory and state per tool why it is not reusable.

VERIFIED AS STATED — do not re-derive at council: theme-dark.css has exactly 74 brace-opening blocks (72 top-level + the @media at :538 + its nested rule at :539 + the unwrapped block at :550); the "at most 24 whole blocks" ceiling at :131 against test_theme_dark_is_still_linked_and_nonempty (>= 50) is arithmetically exact. 34 custom-property declarations: 16 at :4-21, 18 at :552-573; all 16 names in the first block are redeclared in the second; :323-324 correct. tests/test_css_wp4_4_theme_dark_contracts.py:88 is `assert occurrences <= 1` and does pass at zero; the P3-c gap analysis at :557-562 is correct and is the strongest observation in the document. No h_* file exists under scripts/css_audit/; :109-111 correct. scripts/css_audit/j_known_live_mutation.mjs:39 hard-pins EXPECTED_INPUT and :56 exposes --expect-sha; :334-339 including the "do not silence it" warning is correct. theme-dark.css IS the last stylesheet in templates/base.html:28 (a11y :23, page_css :26, motion :27); :86-87 correct. LINUX_INHERITED_REDS.json:2,35,37 — schema v2, totalCount 11, two specs[]; :63 correct. components.css @layer workout span openLine 3539 / closeLine 4104 (a_baseline_contracts.py:149-151); :49 correct. /artifacts/ gitignored at .gitignore:55, so artifacts/theme_dark_p3/ needs no .gitignore edit.

### test-strategist (agent `a2b52c47a43c8c917`) — verdict **APPROVE-WITH-CHANGES** (3 and 5 must-fix), 11 findings

The plan's method is stronger than anything in its predecessor arc, and both claims flagged are verified true — one is understated. But its contract-ceiling inventory is incomplete in a way that forbids deleting one of its own headline candidates, its base commit is wrong, and the artifact it nominates as the authority for "the pixel matrix is not evidence" is itself enforced by a check that cannot fail. Findings 3 and 5 must be fixed before Gate 1.

REQUIRED GATES (per QUALITY_GATE.md:32) — pytest: full suite; cascade contracts run inside the total: tests/test_css_cascade_contracts.py, tests/test_visual_selector_contracts.py. Working-tree readers of theme-dark.css: tests/test_css_wp4_4_theme_dark_contracts.py, tests/test_css_wp4_4_a_baseline_contracts.py, tests/test_css_wp4_4_a11y_contracts.py:427, tests/test_css_wp4_4_layout_contracts.py:294, tests/test_css_cascade_contracts.py:957. e2e (nine): smoke-navigation, nav-dropdown, accessibility, dark-mode, summary-pages, volume-progress, fatigue, fatigue-stage4-smokes, ui-hardening — production packets only. visual: full e2e/visual.spec.ts (66) with PW_VISUAL_SEED=1; ADD e2e/visual-baseline-thumbnails.spec.ts (18) — see finding 8. other: seven-surface Stylelint (scripts/css_audit/stylelint_surfaces.mjs); Linux visual-linux deep gate vs the schema-v2 ledger. Conftest/fixture work: none. No blueprint, table or erase_data() change — the "Calculation surface: none" claim at :219 is confirmed. Gate derivation itself is correct — the plan cites QUALITY_GATE.md :32, :39, :60 exactly as they read, and the static/css/** row does supersede the /verify-suite fallback.

1. The base commit is wrong, and Q7 is already answered in-repo. Plan :17, :303-308, :368, :654 pin base d543a4b and assert MASTER_HANDOVER records PR #222 as open. It does not: MASTER_HANDOVER.md:1357 and :1376 record P1 = d543a4b (#223) and P2 = 4b0670b (#222) as both owner-approved and merged; ACTIVE_DEVELOPMENT.md:249-250 and REFACTOR_PLAN.md:1538 agree. The stated base 4b0670b is P2 — one commit after the plan's base, and the commit that adds the row the plan derives every gate from. Re-pin to 4b0670b, delete Q7, drop the ⚠️ on Assumption 1, and correct plan :370 ("No question here is answerable by an agent").

2. VERIFIED — `occurrences <= 1` does pass at zero, and it is a live hazard for P3-c itself, not a future packet. tests/test_css_wp4_4_theme_dark_contracts.py:83-91: blocks is built by substring match on the selector; delete the rule whole and blocks == [], occurrences == 0, 0 <= 1 passes. Confirmed. What the plan misses: all four pinned selectors (:78-81) are :where([data-theme="dark"] …) paint rules — squarely inside P3-c's own F2 family (:518, :550). Plan :557-562 closes the gap only in a new file and leaves the broken assertion standing. Extend Q1 to authorize strengthening <= 1 → == 1 in place; a strengthening is not a weakening under the plan's own N6-shaped rule at :362. P3-c's contract must enumerate exactly those four (selector, property) pairs as positively present.

3. MUST FIX — the ceiling inventory misses a cascade-contract pin that forbids a headline F2 deletion. tests/test_css_cascade_contracts.py:1006-1007 reads theme-dark.css from the working tree and pins two literals — ':where([data-theme="dark"] .frame-header) {' (present at static/css/theme-dark.css:100) and "backdrop-filter: blur(8px) !important;" (:102, :144). That is a :where()-wrapped !important paint rule, exactly the F2 shape P3-c targets. Deleting it reds a file plan :457 declares "run always, edited never" — and editing that file instead additionally reds test_the_contract_anchor_registry_is_exact (tests/test_css_wp4_4_a_baseline_contracts.py:297), because measure.CONTRACT_FILES (scripts/css_audit/measure.py:34-37) makes the registry pin startLine/endLine/assertionLines for every test in it. Double lock, no owner question raised. Plan v2 needs this as a named ceiling plus a new Q. Offsetting good news the plan should state: CONTRACT_FILES covers only the two shared files, so amending test_css_wp4_4_theme_dark_contracts.py under Q1 does not disturb the registry — which is what makes Q1 cheap.

4. The 24-block ceiling is arc-wide, not per-packet. Verified: theme-dark.css contains exactly 74 {, and theme_dark_contracts.py:35 asserts >= 50, so 24 is arithmetically right. But plan :552 books all 24 to P3-c while plan :587 has P3-d delete the block at :2-22 — a 25th brace from the same budget. P3-c at 24 makes P3-d red on arrival. State the budget as shared and reserve P3-d's share, or make "P3-d empties the rule rather than removing the block" an explicit owner choice.

5. MUST FIX — the plan's authority for "the pixel matrix is not evidence" is itself a gate that cannot fail. The claim is true and understated. But measure.verify_blind_spots() at scripts/css_audit/measure.py:444-453 only checks that each register entry's helperEvidence string is present in e2e/visual-helpers.ts; it never checks the converse, and tests/test_css_wp4_4_a_baseline_contracts.py:212-224 then pins the register against itself (len(register) == len(measure.BLIND_SPOT_REGISTER)). A neutralizer added to the helper is invisible. So A_BASELINE_EVIDENCE.md:181 ("the register cannot drift from the file it describes") is false in the only direction that matters. Unregistered today in e2e/visual-helpers.ts: :62-66 — `html[data-theme] body, body { background: var(--visual-surface-0) !important; background-attachment: scroll !important; }`, both themes. This blinds theme-dark.css:25-31, the multi-gradient :where([data-theme="dark"] body) background — a headline F2/F3 candidate. Also :100-102 [data-visual-header]::before { background } · :103-109 [data-visual-accent] { background, border-radius, box-shadow, transform, transition } · :111 caret-color · :112-116 select { appearance, background-image } · :126-132 navbar ::before { background-color, border-radius, transform, transition } · :133-135 [data-visual-dropdown-toggle]::after { border-color } · :149 ::-webkit-scrollbar. Plan :628 (O7) reproduces only 3 of the register's 6 rows, i.e. a subset of an already-incomplete set; QUALITY_GATE.md:39 routes to the same §8 and inherits the gap. P3-a must own a bidirectional derivation (every neutralizing declaration maps to a register entry; red path = add a rule, pytest goes red) and O7 must be re-derived from the repaired register.

6. With the pixel gate gone, the entire proof burden sits on instruments P3-a writes and P3-a certifies — with no independent check. Of plan :679-689: full pytest is string pins, the nine are functional, Stylelint is lint, and the Linux N8 gate is the same pixel oracle with the same visual-helpers.ts blind spots. The only gate that reads the neutralized properties is the computed differential — which the plan itself says (:116-121) returns an uninformative zero here unless bracketed by O1. So authority reduces to (removal oracle ∩ census ∩ recount) × O1, all built and self-certified in P3-a. This repository has shipped two self-authored controls that cannot fail (findings 2 and 5). Plan :462-476 records red paths as prose in an evidence doc; prose is not a gate. Require each red path to be executed and committed — a fixture input the instrument contract asserts does fail. Note also there is currently no pytest coverage of any .mjs tool in scripts/css_audit/ (only measure.py/specificity.py, via a_baseline_contracts.py:30 and i_is_repair_contracts.py:239), so tests/test_css_theme_dark_p3_instrument_contracts.py is new ground — P3-a's L must absorb it.

7. N8 reconciliation: the ledger's own denominator does not close. LINUX_INHERITED_REDS.json:177 states the job runs both specs together — confirmed at .github/workflows/deep-gate.yml:400. a_baseline_contracts.py:39-44 pins 66 + 18 committed baselines per platform, so the expected N8 total is 84. All three recorded runs at :83-98 report 68 (11 failed / 57 passed; 11 / 56 + 1 flaky). Sixteen tests are unaccounted for, and under the ledger's own rule at :28 an unreconciled gap is exactly where an unledgered red hides. Plan :572 and :685 adopt "11 reds / two spec files" without reconciling the denominator. Plan v2 must state and reconcile the expected N8 total before the first dispatch at P3-c.

8. The Windows gate never runs the spec the arc now reconciles against. Plan :570, :683 and AC8 :190 set the Windows matrix at 66 = visual.spec.ts only, yet a_baseline_contracts.py:41 shows 18 committed win32 thumbnail baselines that no gate in this arc exercises. Since P1 added a visual-baseline-thumbnails.spec.ts red to the ledger, the arc reconciles against a spec it only ever runs on Linux — one ~15-minute dispatch late. Add the 18 tests to the Windows row for P3-c/P3-d/P3-e, or record explicitly why they stay ungated.

9. There is no Chromium known-red on this arc — say so. QUALITY_GATE.md:94 de-listed nav-dropdown on 2026-06-11 and states failures there "should block navbar/theme changes". theme-dark.css IS the theme surface and nav-dropdown is in the required nine (plan :569). The sole surviving exception is e2e/program-backup.spec.ts:79 (QUALITY_GATE.md:92), which is not in the nine. P3-c's rollback list (:555) should state that any red in the nine is a rollback trigger with no band and no ledger.

10. P3-a's "reused unmodified" inventory omits eight committed tools. Plan :111-114 and :456 list eleven; scripts/css_audit/ also holds emit_baseline.py, i_diff_computed.mjs, i_diff_g3.mjs, i_element_pixel_diff.mjs, i_five_route_computed.mjs, i_known_live_mutation.mjs, n4_regions_abc.mjs, visual_helper_band_proof.mjs. The first, fifth and sixth sit on P3-a's build path; visual_helper_band_proof.mjs sits on the animated-logo band reconciliation the plan commits to at :570. The plan's core claim — no h_* file exists and artifacts/wp4_4/*.mjs matches nothing — is verified correct; only the inventory is short, and it may be inflating P3-a.

11. The no-rebaseline invariant already has a committed assertion; the plan substitutes a manual one. Plan :570 gates on `git status e2e/__screenshots__/` being empty, while AC12 (:208-210) asks for invariants asserted rather than described. a_baseline_contracts.py:234-255 already turns an accidental --update-snapshots into a pytest red via a name+size digest across all four snapshot dirs, inside the full-pytest gate the arc already runs. Cite it; demote the manual check to redundancy.

VERIFIED AS STATED (no action): theme-dark.css = 74 brace-opening blocks; 34 custom properties = 16 at :2-22 + 18 at :550-574; `background: none !important` at :361; the `Zero !important. */` comment at :546-548 immediately above the token block at :550, pinned in the working tree by a_baseline_contracts.py:128 (Q2 is a real hazard and "retain the comment" is the right call); test_the_file_declares_no_layer at theme_dark_contracts.py:94-98 pins the N2 premise; no h_* in scripts/css_audit/. One harmless drift for P3-a's re-pin step: scripts/css_audit/measure.py:81 still cites theme-dark.css:595 for the "Zero !important." comment, which now sits at :548.

### product-risk-reviewer (agent `a04a1ab89adadd267`) — verdict **APPROVE-WITH-CHANGES** (1 and 2 must-fix), 7 findings

No calculation surface is touched, no non-goal is violated, and R4/N2/C8 are respected structurally. Findings 1 and 2 are must-fix before Gate 1 — both are places where a user-visible dark-mode regression can pass every gate the plan lists.

CONFIRMATIONS FIRST: Calculation surface `none` — confirmed, not merely accepted. PLANNING.md:217-245 is accurate. theme-dark.css is pure CSS; the arc's new files are scripts/css_audit/p3_*.mjs and tests/test_css_theme_dark_p3_*.py. Nothing reaches utils/effective_sets.py, utils/weekly_summary.py, utils/session_summary.py, utils/progression_plan.py, utils/volume_*.py or utils/fatigue*.py. No route, no response shape, no DB schema. The "Effective sets are informational only" rule is not implicated. Non-goals clean — no auth, cloud sync, remote DB, telemetry. The probe DB derives from the committed synthetic fixture e2e/fixtures/database.visual.seed.db (i_seed_probe_db.py:35), not the user's data/database.db, so nothing of the user's leaves the machine via the N8 CI dispatch. R4/N2/C8 respected; templates/base.html untouched; AC12 (:207-210) asserts each as a test rather than prose, the right shape; no @layer movement; components.css explicitly written by no packet. Workflow ownership untouched; the 11-route matrix (e2e/visual.spec.ts:10-20) covers all seven core workflows plus body-composition and fatigue. No user-facing copy is introduced anywhere.

1. Section 0 "Out of scope" (:283-284) and AC12 (:210) — G4 is inherited at half strength; the rollback-trigger clause and the superset-present capture are dropped. Invariant at risk: G4 as it actually reads in docs/css_phase4_wp4_4/PLANNING.md:1550 — "The superset dark-tint gap stays unacted (R2) — and any change in superset row rendering is a rollback trigger (PR#6), including a change produced by a packet that never opens pages-workout-plan.css" — plus the obligation at :1376(c): "require WP4.4-i and WP4.4-j to capture Workout Plan with at least one linked superset present, in both themes." Plan v1 reduces G4 to the back-door half only: superset must appear nowhere in the file. That is the half that protects against adding a tint. The half that protects against breaking one is gone. The mechanism is concrete: superset rows are painted by static/css/pages-workout-plan.css:3551-3568 — `tr.superset-group-1 { background-color: var(--superset-bg-1) !important; }` /* rgba(124, 58, 237, 0.08) */. Those are 8%-alpha tints (:3424-3427). Their rendered colour is a composite against the ancestor stack — and every ancestor background in dark mode is a family F2 deletion candidate: theme-dark.css:333-341 (.results-section .table tbody tr), :358-362 (background: none !important on .table / .table-responsive / .results-section), :377-400 (.table.table-hover tbody / tr / #results-body). A computed-style differential keyed on the superset row's own background-color longhand reports zero for all of these, because tr.superset-group-1's own computed value never changes — only what it composites over does. The plan's headline gate ("whole-page computed differential … 0 dark / 0 light", :573) is structurally blind to this class of change, and O7 (:628) already establishes the pixel matrix is blind to background on [data-visual-surface] in dark. Worse, the probe cannot see it at all: I found no superset_group seeding in e2e/scripts/build_visual_seed.py or anywhere in the visual-seed path, so the frozen probe DB renders Workout Plan with no linked superset. Every superset declaration is neverProbed by construction — which the plan correctly treats as an exclusion, but the ancestor declarations are not excluded, and they are the ones that move the pixels. Risk: P3-c deletes a tbody/tr/table background from F2, every gate is green, and superset rows on Workout Plan render a different colour in dark mode — a visible change to the exact gap the owner deferred, produced by a packet that never opened pages-workout-plan.css. That is the scenario G4's second clause was written for. Fix: restate G4 in Section 0 with both clauses, add "any change in superset row rendering is a rollback trigger" to P3-c's and P3-d's Rollback rows (:555, :591), and add a P3-a obligation to extend the frozen probe DB with at least one linked superset_group pair so Workout Plan renders superset rows in both themes under a scoped element capture.

2. AC7 (:182-186) and P3-a "Explicit exclusions" (:457) — the contract-ceiling enumeration misses the one ceiling that cannot be amended. Invariant at risk: the plan's own AC7 — "each is named with its exact assertion and the deletion ceiling it imposes" — and CLAUDE.md §1 "Refactor invariant". Plan v1 names two working-tree contracts (:126-137). There is a third, and it is the hardest one: tests/test_css_cascade_contracts.py:1006-1007 pins the whole rule at theme-dark.css:100-105 — its exact selector text cannot be deleted or reformatted — and the literal "backdrop-filter: blur(8px) !important;", which occurs at :102 and :144, so at most one of those two rules may lose it. Both are family F2, i.e. squarely inside P3-c's declared scope (:550), and both properties (background, backdrop-filter) sit in the O7 blind-spot register. The critical part: this assertion lives in tests/test_css_cascade_contracts.py, which Plan v1 designates "run always, edited never" (:457, :568) and which N6 restricts to packet i alone (scripts/css_audit/measure.py:327). So unlike the Q1 ceiling, there is no amendment path. A mechanically correct F2 deletion of .frame-header reds a contract this arc may not touch — the same failure Q2 was written to pre-empt, but without Q2's escape hatch. Note the register that answers this already exists and is already asserted exact: measure.pinned_declarations() and measure.contract_anchors(), gated by a_baseline_contracts.py:293-302, which explicitly asserts theme-dark.css is among the bound surfaces. The plan derived its ceiling by reading instead of by querying the register. Risk: P3-c discovers a hard, unamendable stop at apply time and burns a cycle — or, worse, the implementer resolves it by editing the frozen contract file. Fix: make P3-a's "Second step" (:459) emit the contract ceiling from measure.contract_anchors() / measure.pinned_declarations() rather than by reading, and list test_css_cascade_contracts.py:1006-1007 in AC7 with its two pinned strings and the note that it is not amendable under any Gate-0 answer.

3. P3-b family table (:516-522) and P3-c scope (:550) — F3/F4/F5 membership is contradictory, and one JS-applied-state rule sits inside a deletion range. Invariant at risk: M12 / Q6 — interaction and JS-applied state must be declared out up front, and the plan's own rule that "a prose exclusion is unenforceable" (:562). F3 (a P3-c deletion family) is :190, :194, :200–225, :239, :249, :268, :273, :278, :282, :306. F5 (excluded per Q6) is :58, :151, :157, :172, :177, :185, :207, :220, :268, :352, :403, :447, :474, :501, :519–544. Consequences: :207, :220 and :268 are in both F3 and F5 simultaneously. :213-218 — :where([data-theme="dark"] .tbl-view-mode-toggle.active), :where(… [data-view-mode="advanced"]) — is inside F3's :200–225 deletion range and absent from F5, despite being pure JS-applied state: the element itself is constructed by JS (static/js/table-responsiveness.js:239) and [data-view-mode="advanced"] is a JS-set attribute. A rest-state probe never sees it applied, so a census classifies it dead by construction. This is the advanced/simple view-mode toggle on the summary tables — the Analyze workflow control that switches the Effective/Raw column display. F5 also omits :455, :482, :509 (the three :focus rules on the pastel inputs); those are saved only by F4's overlapping range. F2 is defined as "the bulk of :25–535" (:518), which set-theoretically contains all of F3, F4 and F5. Risk: exactly the WP4.3i-dead failure the plan cites at O9 (:630) — a JS-state declaration nominated dead by a rest-state sweep and deleted, removing the dark-mode "advanced view active" styling from the summary tables. Fix: make family membership disjoint and machine-derived in P3-b (every declaration in exactly one family, emitted by p3_ranges.mjs, with F5 computed from a selector predicate rather than a hand-typed line list) and add :213 to F5 explicitly.

4. AC4 (:167-170) and O4 (:625) — the "frozen probe DB" is not frozen, and there is no hard DB_FILE guard protecting the user's backups. Invariant at risk: CLAUDE.md §2 "Startup sequence" and .claude/rules/database.md; the Backup contract. AC4 requires "the frozen probe-DB digest is recorded identical at run start and run end." Real app.py startup makes that false. With TESTING unset (mandatory under M-h2) and DB_FILE pointing at an existing probe DB (so not a fresh seed): run_all_initializers() runs CREATE TABLE IF NOT EXISTS / ALTER TABLE against the probe DB; upgrade_catalog_from_seed() runs — additive inserts plus refresh of movement_pattern, movement_subpattern, youtube_video_id, media_path on existing rows; create_startup_backup() runs — utils/auto_backup.py:45 only skips on TESTING == "1" — writing database_<ts>.db into <probe dir>/auto_backup/ and rotating at AUTO_BACKUP_KEEP = 7 (:15, :19-20, :68-80). So AC4 fails on the first run, and the likely workaround (hash after the first startup) leaves the two halves of a before/after pair seeded from differently-mutated DBs unless each half restores byte-exactly — the h-class hazard O4 exists to prevent. The plan deletes WAL/SHM sidecars before restore but never mentions the auto_backup/ directory or FLASK_DEBUG, which is what decides whether WAL sidecars exist at all (.claude/rules/database.md: app.py defaults '0', utils/database.py defaults '1'). The Backup-contract half: _backup_dir() is derived from DB_FILE.parent. Plan v1 states "an explicit DB_FILE for every harness" as a provenance obligation but proposes no enforcement. A single harness that forgets it starts app.py against the user's real data/database.db, and create_startup_backup() + _rotate(..., keep=7) writes a snapshot and evicts the oldest genuine auto-backup. Across a campaign of repeated server starts (P3-a red-path proofs, P3-b classification, per-family controls, P3-c/P3-d re-runs) that silently destroys the user's entire seven-deep auto-backup ring. Fix: replace AC4's "digest identical at start and end" with "digest identical to a recorded post-startup frozen artefact, restored byte-exactly before each half, with <probe dir>/auto_backup/ cleared and FLASK_DEBUG pinned"; and add a hard guard to every harness — refuse to start unless the resolved DB_FILE is under artifacts/.

5. P3-c gates (:569) — a fatigue-stage4-smokes dark-contrast red must be declared a rollback trigger, not a repair opportunity. Invariant at risk: the parked fatigue-meter workstream — Stage 4 calibration is OPEN with "no threshold tweaks without ≥2 disagreements." /fatigue is one of the 11 differential routes, and fatigue-stage4-smokes.spec.ts is in the required nine; per .claude/rules/testing.md it tests "Badge mobile geometry and dark contrast." A theme-dark F2 deletion that changes a badge's dark background is exactly the kind of thing that reds it, and the natural in-packet fix is to adjust the badge contrast values — which is parked Stage-4 territory requiring explicit owner go-ahead. Risk: a CSS packet quietly resumes a parked calibration workstream to turn a gate green. Fix: add one line to P3-c/P3-d Rollback: a fatigue-stage4-smokes or fatigue red is a rollback trigger for this arc; no fatigue threshold, badge or calibration value may be touched under packet authority.

6. Base line (:17, :27, :308) — the arc's base commit does not match the review base. The plan pins main @ d543a4b and anchors every figure ("counted by reading at this base") and its whole gate derivation to it. This review was dispatched at base 4b0670b; the checkout's most recent commit is 09bf9a0. The plan's own O6 rule is "provenance is content." Risk: the contract ceilings and the 574/72/34/124 figures describe a tree that is not the one P3-a will start from, and the Q7 QUALITY_GATE.md uncertainty is already flagged as resting on the same base. Fix: re-pin the Base line at Plan v2 and have P3-a's "Second step" record the base SHA it actually measured, rather than inheriting d543a4b.

7. Plan prose (:344, :477) — "Workout Plan Controls" drifts from the canonical "Workout Controls". Invariant at risk: CLAUDE.md §1 key terminology / core workflow 6, which names the surface Workout Controls. theme-dark.css itself uses the canonical form in its own section banner (:417, :433). Non-blocking and not user-facing — this is planning prose, and no template or UI string is introduced anywhere in the arc. Flagged only because evidence documents from this arc will be cited by later sessions. Fix: use "Workout Controls" in Plan v2 and in the P3-a/P3-b evidence docs.

ON THE INERTNESS PREMISE ITSELF: The plan's handling of its own premise is the strongest part of it and I would not weaken it: it explicitly refuses to treat "the differential reported zero" as evidence (:114-121), requires a per-family live control sited inside the family's own region with exclusion-on-zero (O1, AC3), names the winner rather than observing absence (O3), and treats neverProbed / uncertifiable / unresolved as exclusions. AC11's pre-authorized audit-only outcome and the P3-b owner checkpoint mean the default trajectory on weak evidence is "delete nothing," which is the right default. Findings 1 and 3 are the two places where that discipline has a hole — a change the instrument is structurally unable to see (alpha compositing on unseeded superset rows), and a rule that falls through the gap between two family definitions.

---

## Response matrix

Every finding gets a row. **All 33 are dispositioned** — architecture 15, test-strategist 11,
product-risk 7.

**Dispositions: 30 accepted · 3 partial (each accepts the finding's substance and rejects one
stated premise or conclusion, with the evidence) · 0 deferred · 0 rejected outright.**

Three dispositions **changed** when the verbatim text arrived and are marked ⟳: architecture
#11, product-risk #2, and the attribution of test-strategist #2.

### architecture-reviewer `a0cf22638cb17fefb` — 15 findings

| # | Finding | Disposition | Action in v2 |
|---|---|---|---|
| 1 | Third working-tree contract missed: `cascade_contracts.py:1006–1007` pins `.frame-header` `:100` and `backdrop-filter` `:102`, inside F2. | **accept** | Recorded as **Ceiling 3**; full 14-row ceiling enumeration added to Section 0; new **Q8** opened in exactly the shape proposed (may P3-c make a scoped non-weakening cascade-contract edit under `QUALITY_GATE.md:32`, or exclude `.frame-header` outright). Recommendation: exclude. |
| 2 | Q2's comment-absorption hazard is misattributed and cannot fire — `:546–548` is `:550`'s leading comment and `:550` is never deleted. | **accept mechanism · reject the framing that the *rule* goes with the question** | Verified: F1 deletes `:2–22`, whose own leading comment at `:1` is unpinned. **Q2 withdrawn** — a real reduction in owner load. But the reviewer's own fix says *"keep the manifest-builder exception rule but derive it from the actual pinned strings"* — which is precisely **O10b**, retained and now derived from `measure.pinned_declarations()`. Recorded as partial only because the disposition splits, not because the reviewer and I disagree on the outcome. |
| 3 | Base SHA is wrong: `d543a4b` is P1; base is `4b0670b`. | **accept** | Re-pinned in the header and throughout. Plan v1 left unamended as the audit trail; P3-a's second step records the SHA it actually measured rather than inheriting one. |
| 4 | Q7's assumption is contradicted by `MASTER_HANDOVER.md:1376`. | **accept** | **Q7 withdrawn**; assumptions promoted to ✅ verified fact citing `:1357/1376/1409/1410`; the Q7 caveat removed from the gate table. Q-numbers are not recycled. |
| 5 | O1's "≥1 own theme, 0 in the other" bracket is **false for four theme-agnostic rules** — `:239–246`, `:249–257`, `:259–262`, `:268–270` carry no `[data-theme="dark"]`; and `:555`'s "any light difference at all" rests on a "dark-only file" premise that is not true. | **accept in full** | The best-reasoned finding in the set, and one Plan v1 got structurally wrong: a *correct* control on those rules moves both themes, which O1 would have read as a failed control — an unfalsifiable loop. **F3 splits into F3-dark and F3-agnostic**; F3-agnostic gets a both-themes control bracket; **"dark-only file" is struck from the rollback wording** and replaced with a per-family expectation. |
| 6 | Family table is not a partition — `:207`, `:220`, `:268` double-assigned; F5's `:519–544` swallows F6's `:538–544`; `:213–218` is JS state inside an F3 deletion range. | **accept** | Families become a **machine-derived partition** emitted by `p3_ranges.mjs` (every declaration in exactly one family), not a hand-typed line list. `:213–218` → F5. F6 carved out of F5's range explicitly. |
| 7 | Ceiling enumeration omits three more assertions in the file it does name — `.value-changed >= 7` with **exactly 7** present (zero headroom), `@media == 1` (exact equality), plus the `superset` and `@layer` pins. | **accept in full** | Verified: the seven occurrences are `:519, 520, 525, 526, 531, 532, 539`. Plan v1's "two constraints" understated it five-fold. Section 0 now carries the **full 14-row table** in exactly the shape proposed. |
| 8 | Fifteen WP4.4 constraints inherited without citing the authority that carries them; `.claude/rules/verification.md` retires arc-specific constraints on arc close. | **accept in full** | The most consequential finding. Plan v2 §*Constraint provenance* splits every inherited constraint into **Tier 1** (owner-re-issued), **Tier 2** (durably homed in `.claude/rules/verification.md`, re-cited there, no owner action) and **Tier 3** (arc-specific and retired → restated as this arc's own **P-1 … P-8** for owner acceptance at new **Q9**). Q1's "N6 pattern" justification struck. |
| 9 | G4 restated with its operative half removed; P3-d's 16 custom properties (`--card-bg`, `--table-stripe`, `--hover-bg`, `--glass-*`) are consumed by superset rows through `var()`. | **accept in full** | G4 restored with both clauses. Superset-row rendering added to **both** P3-c's and P3-d's rollback lists — the `var()` consumption path is why P3-d needs it too, which product-risk #1 did not cover. Folded into **O12**. |
| 10 | M9's route-coverage half dropped from P3-d obligation (b). | **accept** | Obligation (b) now reads: no consumer resolves to the earlier declaration, **and every consumer found is exercised on a probed route**. A consumer that exists but never renders reads as "no consumer" — the `neverProbed` failure O3 exists to prevent, in the packet with the highest per-declaration bar. |
| 11 | ⟳ C7's 8-element set is unresolvable (its paths lived in gitignored `artifacts/`), and `.hero-section` `:282` is the container, not one of the 8 — so "structurally out of reach" is asserted, not measured. | **accept the `.hero-section` correction · REJECT the "unresolvable" premise, with evidence** | **`:282` demoted to a nomination the instrument settles** — the reviewer is right that Plan v1 stated it as fact, and right that neither `background` nor `backdrop-filter` inherits onto the animated children. **But the set is not lost.** `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` → `uncertifiableElements.elements[]` carries **all 8 with both `domPath` and `selector`**, plus an `adjacentNote` for `div.developer-credit-banner::before`, in a **committed** file with no dependency on the deleted `artifacts/` tree. So P3-a's recovery step does not need to re-derive C7 — it reads it. *(This disposition changed once the verbatim text was available: my earlier partial matrix had accepted the "structurally out of reach" claim unexamined.)* |
| 12 | D3 grants four packets an undeclared shared-path claim on the three status documents. | **accept** | If D3 is granted, the three paths are added to **every** packet's "Paths owned" row with an append-only rule scoped to the lead block and `## Next Safe Step` — the two places WP4.4-k's reconciliation actually failed. If D3 is refused, P3-e remains the single writer and the packets stay silent. |
| 13 | Q1's "never converted to floors or `>=`" collides with `body.count("{") >= 50`, a floor **by design**. | **accept** | Q1's exact-re-pin rule is now scoped to `test_every_custom_property_declaration_survives:45` **alone**. Applied literally, Plan v1's wording would have converted R4's non-empty guard into an exact pin — a defect introduced in the name of rigour. |
| 14 | `i_seed_probe_db.py:68,93` uses raw `sqlite3.connect()` rather than `DatabaseHandler`; record as a scoped exception so `code-reviewer` does not re-litigate it per packet. | **accept** | One line added to the Calculation-surface section recording it as deliberate and scoped: committed audit tooling outside the `app.py → routes/ → utils/` chain, taking an explicit `--out` rather than reading `utils.config.DB_FILE`, reused unmodified. |
| 15 | Committed-harness inventory incomplete — eight more tools exist. | **accept** *(merged with test-strategist #10)* | P3-a's first step now assesses **all nineteen** committed tools and states per tool why it is or is not reusable, before proposing to write anything. May reduce P3-a's scope; see the effort note in Plan v2. |

### test-strategist `a2b52c47a43c8c917` — 11 findings

| # | Finding | Disposition | Action in v2 |
|---|---|---|---|
| 1 | Base commit wrong; Q7 already answered in-repo. | **accept** | As architecture #3/#4. Also corrects the "No question here is answerable by an agent" line, which now excludes the withdrawn questions. |
| 2 | ⟳ `occurrences <= 1` passes at zero — **verified** — and all four pinned selectors are inside P3-c's own F2 family, so it is a live hazard for P3-c, not a future packet. | **accept in full** | Plan v1 closed the gap only in a *new* file and left the broken assertion standing. Plan v2 **strengthens it in place, `<= 1` → `== 1`**, under Q1, and P3-c's contract enumerates the four `(selector, property)` pairs as positively present. Generalized as **O14**. *(Attribution corrected: this is test-strategist #2 alone. Architecture recorded it under "VERIFIED AS STATED — the strongest observation in the document", which is a confirmation, not a finding; my earlier matrix mis-credited it to two reviewers.)* |
| 3 | **MUST FIX** — ceiling inventory misses the cascade-contract pin; and editing that file *additionally* reds the anchor-registry contract via `measure.CONTRACT_FILES`, which pins `startLine`/`endLine`/`assertionLines`. **Double lock.** Offsetting: `CONTRACT_FILES` covers only the two shared files, so Q1 is cheap. | **accept in full** | The double-lock mechanism was missed by both other reviewers and by me. Recorded in Ceiling 3 and in **Q8**. The offsetting half is recorded in **Q1**. **Name corrected per re-review N6:** the test is `test_contract_anchor_register_covers_every_shared_surface` (`a_baseline_contracts.py:285`), not `test_the_contract_anchor_registry_is_exact`, which does not exist; the cited assertion line `:297` was right. |
| 4 | The 24-block ceiling is arc-wide, not per-packet; P3-c at 24 makes P3-d red on arrival. | **accept** | **One shared budget of 24**, drawn in order: P3-d spends 1 (the `:2–22` rule), so P3-c's ceiling is **23** when P3-d is expected to proceed and 24 when Q1 is refused. The reviewer's alternative — "P3-d empties the rule rather than removing the block" — is recorded as the fallback if Q1 is granted but the budget binds. P3-e asserts the arc total. |
| 5 | **MUST FIX** — the blind-spot register's verifier is unidirectional: `measure.verify_blind_spots()` (`measure.py:444–453`) checks only that each entry's `helperEvidence` appears in the helper, and `a_baseline_contracts.py:212–224` pins the register against itself. **Eight** unregistered neutralizers listed; O7 reproduces only 3 of the register's 6 rows. | **accept in full** | So `A_BASELINE_EVIDENCE.md:181` — *"the register cannot drift from the file it describes"* — is false in the only direction that matters, and `QUALITY_GATE.md:39` inherits the gap by routing to the same §8. **P3-a owns a bidirectional derivation** (every neutralizing declaration maps to a register entry; red path = add a rule to the helper, pytest goes red), and **O7 is re-derived from the repaired register** rather than from the incomplete one Plan v1 quoted. *(Refinement: `:62–66` neutralizes the `background` shorthand at `theme-dark.css:26–32` and `background-attachment: fixed !important` at `:33`; `color` at `:34` is **not** neutralized. The reviewer's `:25–31` and my earlier `:25–35` were both approximations of the rule span.)* |
| 6 | With the pixel gate gone, the whole proof burden sits on instruments P3-a writes **and** P3-a certifies, with no independent check; this repo has shipped two self-authored controls that cannot fail; and there is no pytest coverage of any `.mjs` tool today. | **accept in full** | The sharpest structural observation in the council. Recorded verbatim as a standing risk in Plan v2, with three consequences: red paths become **committed executed fixtures** (**O15**); `tests/test_css_theme_dark_p3_instrument_contracts.py` is **new ground** — the first pytest coverage of any `.mjs` tool in `scripts/css_audit/` — and P3-a's **L** must absorb writing that harness; and **AB-1** is restated so instrument-control failure ends the arc rather than triggering a repair loop. |
| 7 | The N8 ledger's denominator does not close: 66 + 18 = **84** expected, all three recorded runs report **68**. Sixteen unaccounted. | **accept in full** | New to me and material — under the ledger's own rule an unreconciled gap is exactly where an unledgered red hides, and this arc's N8 reconciliation rests on it. **P3-a must state and reconcile the expected N8 total before P3-c's first dispatch**, and P3-c may not dispatch until it closes. Added to AC8 and to the P3-a gate row. |
| 8 | The Windows gate never runs `visual-baseline-thumbnails.spec.ts`, yet the arc reconciles against a ledger entry from that spec. | **accept** | **18 Windows thumbnail tests added** to the visual row for P3-c, P3-d and P3-e. Reconciling on Linux only means discovering a thumbnail red one ~15-minute dispatch late. |
| 9 | There is no Chromium known-red on this arc — `nav-dropdown` was de-listed and should block theme changes; `program-backup.spec.ts:79` is not in the nine. | **accept** | Added to P3-c/P3-d rollback: **any red in the required nine is a rollback trigger — no band, no ledger, no known-red allowance.** `theme-dark.css` *is* the theme surface, so the de-listing applies with full force. |
| 10 | P3-a's "reused unmodified" inventory omits eight committed tools; three sit on P3-a's build path and `visual_helper_band_proof.mjs` sits on the band reconciliation. | **accept** *(merged with architecture #15)* | As architecture #15, plus the specific routing: `emit_baseline.py`, `i_five_route_computed.mjs` and `i_known_live_mutation.mjs` are assessed as build-path inputs, and `visual_helper_band_proof.mjs` is named as the band-reconciliation tool rather than re-derived. |
| 11 | The no-rebaseline invariant already has a committed assertion (`a_baseline_contracts.py:234–255`); the plan substitutes a manual `git status` check. | **accept** | AC12 asked for invariants asserted rather than described, and Plan v1 then described this one. The committed digest assertion is now **cited as the gate**; the manual check is demoted to redundancy. |

### product-risk-reviewer `a04a1ab89adadd267` — 7 findings

| # | Finding | Disposition | Action in v2 |
|---|---|---|---|
| 1 | **MUST FIX** — G4 inherited at half strength: the rollback-trigger clause and the superset-present capture obligation are both dropped. Superset rows are 8%-alpha tints over ancestor backgrounds that are themselves F2 candidates (`:333–341`, `:358–362`, `:377–400`), so the headline differential is structurally blind; and no `superset_group` seeding exists in the visual-seed path, so superset declarations are `neverProbed` by construction while their ancestors are not. | **accept in full** | The finding that identifies how this arc could ship a real user-visible regression with every gate green. G4 restored with both clauses; superset-row rendering added to P3-c **and** P3-d rollback; **O12** requires an ancestor-composited check measuring superset rows as *rendered* rather than as *declared*; and **P3-a must extend the frozen probe DB with at least one linked `superset_group` pair** so Workout Plan renders superset rows in both themes under a scoped element capture. If that seeding cannot be done, **every ancestor of a superset row is excluded** — `neverProbed`-by-construction is an exclusion, not a pass. |
| 2 | ⟳ **MUST FIX** — the ceiling enumeration misses the one ceiling that **cannot be amended**; derive it from `measure.contract_anchors()` / `measure.pinned_declarations()` instead of by reading. | **accept the conclusion and the fix · REJECT the "no amendment path" premise** | **The fix is the best part and is adopted in full**: P3-a emits the ceiling from the two registers, which already exist and are already asserted exact by `a_baseline_contracts.py:293–302`. **But "no amendment path" is not established.** A path exists and is live — the P2 owner amendment in `QUALITY_GATE.md:32` permits cascade-contract edits that are *"explicitly scoped, justified, and must not weaken an existing guarantee."* **The conclusion survives anyway, and is over-determined**: under *all three* readings of the authority question the answer is the same — (i) if N6 carried, it reserves that file to packet `i` and, per architecture #1, to lines `1614–1627`, a different range; (ii) if N6 retired with the arc, there is no standing authority to invoke; (iii) under the live P2 clause, deleting `.frame-header` or its `backdrop-filter` **weakens** the guarantee, so the clause does not reach it. **Because it is over-determined, Q8's answer does not depend on Q9** — which matters, since Q9 is precisely the open question of whether inherited constraints carry, and leaning on "N6 retired" as settled while asking the owner to decide that would be circular. *(This adjudication was rewritten after the verbatim text arrived: my earlier matrix did lean on "N6 retired" as settled.)* |
| 3 | F3/F4/F5 membership is contradictory; `:213–218` is JS-applied state inside a deletion range — the element is built by JS (`table-responsiveness.js:239`) and `[data-view-mode="advanced"]` is JS-set; F5 also omits `:455`, `:482`, `:509`, saved only by F4's overlapping range; F2 set-theoretically contains F3, F4 and F5. | **accept in full** *(supersedes architecture #6, which found the same defect with less of it)* | Machine-derived disjoint partition in P3-b, **F5 computed from a selector predicate rather than a hand-typed line list** — that is the fix that makes the whole class of error impossible, and it is the reviewer's, not mine. `:213` → F5. `:455`/`:482`/`:509` → F5 on their own merits, not by F4 overlap. **F2 is redefined as a residual** — `!important` paint declarations *not* in F1/F3/F4/F5/F6 — instead of "the bulk of `:25–535`", which was never a family definition. Named risk recorded: `:213–218` is the Analyze-workflow view-mode toggle that switches Effective/Raw column display; deleting it would remove the dark-mode "advanced view active" styling. |
| 4 | **The "frozen probe DB" is not frozen**, and there is no hard `DB_FILE` guard protecting the user's backups. `run_all_initializers()`, `upgrade_catalog_from_seed()` and `create_startup_backup()` all mutate it; `_backup_dir()` derives from `DB_FILE.parent`; a forgotten `DB_FILE` destroys the user's seven-deep auto-backup ring across a probe campaign. `FLASK_DEBUG` decides whether WAL sidecars exist at all. | **accept in full** | Verified independently at `utils/auto_backup.py:14–15` and `:37–84`. **AC4 fully restated**: digest identical to a recorded **post-startup** frozen artefact, **restored byte-exactly before each half**, with `<probe dir>/auto_backup/` cleared and `FLASK_DEBUG` pinned. New rule **O13**: every harness refuses to start unless the resolved `DB_FILE` is under `artifacts/`. The only finding in the council whose blast radius reaches outside the repository — it can destroy user data — and Plan v1 had the obligation as *provenance* with no enforcement. |
| 5 | A `fatigue-stage4-smokes` dark-contrast red must be a rollback trigger, not a repair opportunity — the natural in-packet fix is adjusting badge contrast, which is parked Stage-4 calibration territory. | **accept in full** | Added to P3-c/P3-d rollback: **a `fatigue` or `fatigue-stage4-smokes` red is a rollback trigger for this arc, and no fatigue threshold, badge or calibration value may be touched under packet authority.** Catches a CSS packet quietly resuming a parked workstream to turn a gate green — a failure mode no other reviewer looked for. |
| 6 | Base commit does not match the review base; "provenance is content" is the plan's own O6. | **accept** | As architecture #3. P3-a's second step records the SHA it measured rather than inheriting one — the reviewer's framing, adopted. |
| 7 | "Workout Plan Controls" drifts from the canonical "Workout Controls" (`CLAUDE.md` §1 / workflow 6); `theme-dark.css:417,433` uses the canonical form. | **accept** | Corrected throughout Plan v2 and required of the P3-a/P3-b evidence documents. Non-user-facing, but this arc's evidence docs get cited by later sessions. |

---

## Plan v2

**Goal**: *(unchanged from v1)* Measure, declaration by declaration, how much of
`static/css/theme-dark.css` can never win — using a rebuilt, committed, red-path-proven
removal oracle rather than a census — and delete exactly the certified non-winners, leaving
the file linked, nonempty, and byte-identical if nothing certifies.

**Base**: `main` @ **`4b0670b`**.

### Scope

- **In**: *(unchanged from v1)* the committed oracle rebuild; the whole-file classification;
  the certified deletions across two separately-certified production packets; per-packet
  contracts and evidence docs; the integration/closeout packet.
- **Out**: *(unchanged, with two restorations)* everything in Section 0 *Out of scope* —
  **R4** (the file stays linked, `templates/base.html` frozen), making the file win, **N2**,
  **C8**, **R1**, the other six shared surfaces, every page bundle, `scss/**`, snapshot
  rebaselining, and interaction-state / JS-class declarations. **Restored at council:**
  **G4 at full strength** (any change in superset row rendering is a rollback trigger, from
  any packet), and **`.frame-header` at `theme-dark.css:100–105` excluded from candidacy**
  pending Q8.

### Constraint provenance — new in v2 (architecture-reviewer #8)

WP4.4 is closed, and `.claude/rules/verification.md:21–24` retires an arc's constraints with
it. This arc therefore states where each obligation it carries actually comes from, instead of
citing retired numbers.

**Tier 1 — re-issued by the owner in this arc's brief.** Binding, no further action:
`R4`, `N2`, `C8`, `G4`, `M-h1`, `M-h2`, `M-h3`, `M6a`, the three i–k tail rules, the
no-rebaseline rule, and the animated-logo band (875/882 ∪ 1,039/1,046).

**Tier 2 — durable, homed in `.claude/rules/verification.md`.** Binding by that file, cited
there rather than to WP4.4. No owner action needed:

| Obligation | Durable home |
|---|---|
| known-live + known-dead + same-CSS control; control output reported raw; adversarial control selection | `:29–50` |
| converging evidence, not one sweep | `:52–56` |
| interaction-state / JS-class scope declared up front or deferred | `:58–61` |
| `@media` captures under their own condition | `:63–64` |
| sentinel/transition suppression, symmetric release, per-record sentinel assertion | `:66–76` |
| `PW_VISUAL_SEED=1`; element-scoped capture; animated-logo diff is a band, never a constant | `:78–88` |
| reuse the committed harness; specificity model handles `:is()`/`:where()`/`:not()`/`:has()`, no naive comma split, `@layer` order + `!important` inversion | `:90–96` |
| CRLF and character-offset math; never use `nth-child` or re-serialized text for rule identity; length-preserving comment stripping | `:98–107` |
| CSS packets on the same bundle run serially | `:109–112` |

**Tier 3 — arc-specific, retired with WP4.4, restated here under this arc's own numbering.**
These need owner acceptance at **Q9**:

| # | P3-owned constraint | Retired source |
|---|---|---|
| **P-1** | Line counts and projections are **not** acceptance criteria, in either direction. | C10 |
| **P-2** | Custom-property declarations are never candidates under the non-winner rule alone; deleting one requires a `var()`-consumer dependency graph **and** a removal-oracle result **and** a per-token split control. | M9 |
| **P-3** | The 8 infinite-animation Welcome elements are uncertifiable by any rest-state harness in this repository. *(Also survives independently: the rule is written into `CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` → `uncertifiableElements.rule`, a committed data file with no arc dependency.)* | C7 |
| **P-4** | Each packet adds its own contract file; none is ever consolidated or merged into another. | N1 |
| **P-5** | Narrow first, abandon second: a family that cannot be proven safe is dropped, and if none survives the arc ends as audit. | N3 |
| **P-6** | Evidence documents are flat `docs/CSS_THEME_DARK_P3_*_EVIDENCE.md`. | R6 |
| **P-7** | No unexplained visual difference; no snapshot rebaseline under packet authority; no rise in maximum specificity or unexplained `!important`; monotonic duplicate reduction; cascade correctness outranks line count. | V1–V6 |
| **P-8** | Every packet knows its contract ceiling before it starts, enumerated **mechanically** from the test files rather than recalled. | A8/F6 |

**Not carried at all:** `C11` (spent on packet j; its *effects* survive as j's live contract
file, which is what this arc actually gates against), `N6` (retired; superseded for the two
cascade-contract files by the live P2 amendment in `QUALITY_GATE.md`), `A11` (this arc commits
its harness to `scripts/css_audit/` rather than leaving it in gitignored `artifacts/` —
that is the whole reason P3-a exists).

### What the owner must decide before anything can start

| Gate 0 | **Q1** amend the WP4.4-j contract · **Q3** "make it win" is OUT · **Q4** evidence-doc naming · **Q5** N8 cadence · **Q6** interaction states OUT · **Q8** `.frame-header` candidacy · **Q9** the P-1…P-8 constraint restatement · **Q10** *(new)* repair of the two shared registers + baseline regeneration |
|---|---|
| **Gate 1** | Plan v2 as a whole, plus **the P3-a split** (accepted below, but it changes the packet count 5 → 6) and the four **D1–D4** decisions |
| Withdrawn | ~~Q2~~ (cannot fire), ~~Q7~~ (answered) |

Nothing in this arc may begin until Gate 0 and Gate 1 are both signed. **Neither is.**

### Packets — six (P3-a split at re-review)

| # | Packet | Nature | Writes production CSS? | Visible rendering may change? |
|---|---|---|---|---|
| 1 | **P3-a0** — audit, ceiling emission, tool assessment, documentary reconciliation | **read-only** | no | no |
| 2 | **P3-a1** — apparatus repair + oracle build and certification | tooling + tests | no | no |
| 3 | **P3-b** — whole-file classification, ends at the go/no-go checkpoint | read-only | no | no |
| 4 | **P3-c** — certified paint-declaration deletion | production | yes | no |
| 5 | **P3-d** — certified legacy token-block deletion | production | yes | no |
| 6 | **P3-e** — integration, closeout, status reconciliation | documentation | no | no |

**The split is accepted; here is the reasoning, since it is my call.** Plan v2's P3-a had grown
to carry four units with different blast radii — a read-only audit, a *repair of
already-certified WP4.4 apparatus*, a new-oracle build, and probe-DB seeding. The decisive
argument is the reviewer's: **the packet repairing the apparatus is the same packet whose new
instruments are measured against that apparatus.** That is a self-certification loop, and this
arc's entire method exists to refuse those. Two further reasons the reviewer did not give:
**Q10 and the N1 emitter question both resolve inside the old P3-a**, so a refusal would have
left a half-built oracle; splitting puts every owner question in a packet that completes
*before* any oracle exists. And P3-a0's outputs — the emitted ceiling, the nineteen-tool
assessment, the documentary N8 reconciliation — **are the evidence the owner needs to answer
Q10**, which cannot be true if they are produced by the packet the answer governs. The
reviewer is also right that Plan v2's "present a re-scoped tool list before building anything"
was a checkpoint in disguise; making it a packet boundary makes it enforceable.

*Cost, stated honestly: one more merge, and the arc goes 5 → 6 packets. The DAG stays linear
and no concurrency claim changes.*

**DAG:**

```
P3-a0 ──(evidence + owner answers Q10)──▶ P3-a1 ──(no classification without a certified
instrument)──▶ P3-b ──(OWNER CHECKPOINT)──▶ P3-c ──(single-writer)──▶ P3-d ──▶ P3-e
```

Concurrency classification and the P3-b/P3-c/P3-d/P3-e attribute tables are **unchanged from
Plan v1** except where amended below. Every production packet writes the same file, so no pair
in this arc is ever concurrent.

### Changes to the packets

**P3-a0 — audit, ceiling, inventory, documentary reconciliation.** *Read-only. Owns
`docs/CSS_THEME_DARK_P3_A0_AUDIT_EVIDENCE.md`, `scripts/css_audit/p3_ceiling.py`,
`tests/test_css_theme_dark_p3_audit_contracts.py`. Writes no production CSS and repairs no
existing apparatus.*

- **Emit the contract ceiling with a P3-owned emitter** (AC7, P-8; re-review **N1**).
  `measure.contract_anchors()` / `pinned_declarations()` iterate `measure.CONTRACT_FILES`
  (`measure.py:273`, `:332`), which is **only the two shared files** (`:34–37`) — so run today
  they would emit **Ceiling 3 and nothing else**, reaching 2 of the 14 rows. Plan v2's
  "emit from the registers" was therefore unbuildable as written. `p3_ceiling.py` walks
  **every working-tree reader of `theme-dark.css`** independently of `CONTRACT_FILES`, so
  nothing shared is touched and no baseline moves.
- **Assess all nineteen committed tools before anything is written** (architecture #15,
  test-strategist #10) — including `emit_baseline.py`, `i_five_route_computed.mjs` and
  `i_known_live_mutation.mjs`, which sit on the build path, and `visual_helper_band_proof.mjs`,
  the band-reconciliation tool this arc commits to using. State per tool why it is or is not
  reusable. **This is the packet boundary that makes "re-scope before building" enforceable.**
- **Recover C7's uncertifiable set from the committed ledger** (architecture #11, retracted at
  re-review): `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` →
  `uncertifiableElements.elements[]` carries all 8 with both `domPath` and `selector`, plus the
  `adjacentNote` for `div.developer-credit-banner::before`. Read it; do not re-derive it.
- **Reconcile the N8 denominator — documentarily** (test-strategist #7; re-review **N8**).
  66 + 18 = **84** expected against **68** reported in all three recorded runs; 16 unaccounted.
  **P3-a0 does not and may not dispatch the deep gate** — the reconciliation is a desk exercise
  over `.github/workflows/deep-gate.yml`, the ledger's `scopeNote` (`:177`) and the 66 + 18
  baseline pins at `a_baseline_contracts.py:39–44`. The gap must close **before P3-c's first
  dispatch**, which is the packet that actually runs it.
- **Re-measure and pin the arc base**, recording **the SHA it actually measured** rather than
  inheriting one (product-risk #6).

**P3-a1 — apparatus repair, oracle build, certification.** *Tooling + tests. Writes no
production CSS. Depends on P3-a0's evidence and on the owner's answer to **Q10**.*

- **Build the oracle set**, scoped to whatever P3-a0's tool assessment leaves.
- **Own a P3-local bidirectional blind-spot register** (test-strategist #5; re-review **N2**).
  The accepted repair to the *shared* register cannot ship unilaterally:
  `a_baseline_contracts.py:224` asserts
  `len(register) == len(measure.BLIND_SPOT_REGISTER)` against the committed baseline, so adding
  the eight missing neutralizers changes that length and needs either a baseline regeneration
  or an edit to a "run always, edited never" file. **So the arc de-risks itself first:**
  `p3_blind_spots.mjs` enumerates every neutralizing declaration in `e2e/visual-helpers.ts` and
  fails if any is unregistered **in the P3 register**, and **O7 derives from the P3 register**.
  This needs no owner permission and leaves the shared register untouched. **Q10** then asks
  separately whether the shared defect may also be repaired — see below.
- **Own `scripts/css_audit/p3_seed_probe_db.py`** (re-review **N3**). Plan v2's superset-seeding
  obligation contradicted "reuse `i_seed_probe_db.py` unmodified" *and* voided the sqlite3
  exception, which is conditioned on not modifying that file. Worse, the obvious reading —
  seed the **committed** fixture `e2e/fixtures/database.visual.seed.db` — would change what
  `PW_VISUAL_SEED=1` renders and force the rebaseline this arc forbids absolutely. So: a
  **new, P3-owned** seeder that writes **only its `--out` copy** and **never** the committed
  fixture. The scoped raw-`sqlite3` exception is extended to it **by name**;
  `i_seed_probe_db.py` stays unmodified and keeps its own exception.
- **The `DB_FILE` containment guard (O13)**, a precondition for every later browser run.
- **Capture the frozen probe artefact post-startup** (AC4), quiesced, WAL/SHM checkpointed and
  removed, `<probe dir>/auto_backup/` cleared, `FLASK_DEBUG` pinned.
- **Red paths ship as committed, executed fixtures** (**O15**).
  `tests/test_css_theme_dark_p3_instrument_contracts.py` is the **first pytest coverage of any
  `.mjs` tool** in `scripts/css_audit/` — new ground this packet's **L** must absorb.
- **Fix the recorded drift** *(only if Q10 is granted; otherwise record it)*:
  `scripts/css_audit/measure.py:81` still cites `theme-dark.css:595` for the `Zero !important.`
  comment, which now sits at `:548`.

**P3-b — additions**

- **Families are a machine-derived disjoint partition** emitted by `p3_ranges.mjs` — every
  declaration in exactly one family, **F5 computed from a selector predicate** rather than a
  hand-typed line list (product-risk #3). Plan v1's table double-assigned four ranges and let
  F5 swallow F6.
- **Membership is per-declaration, never per-rule** — `:298`, `:311–315` and `:323–331` each
  mix `!important` and normal declarations.
- **Corrected family definitions**:

| Family | Definition | Notes |
|---|---|---|
| **F1** — legacy token block | the 16 custom-property declarations at `:2–22` | P3-d only |
| **F2** — residual `!important` paint | `!important` paint declarations **not** in F1/F3/F4/F5/F6 | *Redefined.* "The bulk of `:25–535`" was never a family definition — set-theoretically it contained F3, F4 and F5. **Less `.frame-header` `:100–105`** (Ceiling 3 / Q8) |
| **F3-dark** — dark-scoped normal declarations | selector contains `[data-theme="dark"]` | `:190`, `:194`, `:200–205`, `:273`, `:278`, `:282`, `:306` |
| **F3-agnostic** — theme-agnostic normal declarations | **no `[data-theme="dark"]` in the selector** | `:239–246`, `:249–257` **only**. **Match in both themes** — see O1′ |
| **F4** — Workout Controls pastel input rules | `:438–535` | expected-live spikes, not candidates |
| **F5** — interaction / pseudo-element / JS-applied state | selector predicate: any of `:hover`, `:focus`, `::placeholder`, `:not(:disabled)`, `.active`, `[data-view-mode]`, `.value-changed` | includes `:207–211`, **`:213–218`**, `:220–225`, and **`:455`, `:482`, `:509`** on their own merits rather than by F4 overlap |
| **F6** — reduced-motion `@media` | `:538–544`, **carved out of F5's range** | preserved by contract |

- **Precedence is an ordered chain, not a set of independent predicates** (re-review **N5**).
  Plan v2's corrected table still double-assigned, because "no `[data-theme="dark"]`" and
  "contains `:hover`" can both be true. Evaluation order, first match wins:

  ```
  F1  →  F5  →  F6  →  F4  →  F3-dark  →  F3-agnostic  →  F2 (residual)
  ```

  The two corrections this forces, both verified against the file: **`:268–270`** is
  `:where(#darkModeToggle:hover)` — F5 catches it before F3-agnostic; and **`:259–262`**'s only
  declaration is `color: #0d6efd !important` — it fails F3's *normal-declaration* predicate and
  falls through to **F2 residual**. Both are dropped from the F3-agnostic note above.
- **Theme scope is a per-declaration attribute, not a family attribute.** F2-residual now
  contains both theme-scoped and theme-agnostic members (`:259–262` is the proof), so **O1′'s
  expected partition is declared per control, keyed on whether the controlled declaration's own
  selector is theme-scoped** — not per family. This is a genuine strengthening of the O1′
  wording Plan v2 shipped, forced by N5.
- **Named risk, recorded rather than left implicit:** `:213–218` is the Analyze-workflow
  view-mode toggle that switches Effective/Raw column display. Its element is built by JS
  (`static/js/table-responsiveness.js:239`) and `[data-view-mode="advanced"]` is a JS-set
  attribute, so a rest-state census classifies it dead **by construction**. Deleting it would
  remove the dark-mode "advanced view active" styling from the summary tables.
- **The ancestor-composited check (O12)** runs here, so the superset hazard is measured before
  any deletion set is proposed.

**P3-c / P3-d — additions**

- **One shared 24-block budget**, drawn in order: P3-d spends 1 (the `:2–22` rule), so P3-c's
  ceiling is **23** when P3-d is expected to proceed, **24** when Q1 is refused. Fallback if
  the budget binds: **P3-d empties the rule rather than removing the block** — recorded as an
  owner choice, not taken on packet authority. P3-e asserts the arc total.
- **`test_the_certified_removals_stay_removed` strengthened in place, `<= 1` → `== 1`**, with
  the four pinned pairs enumerated positively (**O14**). Requires Q1; cheap, because
  `measure.CONTRACT_FILES` does not cover that file.
- **`.frame-header` `:100–105` excluded** from candidacy pending Q8. Anchoring
  `cascade_contracts.py:1007` to that block is a strengthening but sits inside the **double
  lock**, so it goes to the owner with Q8 rather than being taken under packet authority.
- **P3-d obligation (b) gains route coverage** (architecture #10): no consumer resolves to the
  earlier declaration, **and every consumer found is exercised on a probed route**. A consumer
  that exists but never renders reads as "no consumer".
- **Rollback list — four additions**:
  1. **any change in superset row rendering**, including from a packet that never opens
     `pages-workout-plan.css` (G4 restored). Applies to **P3-d too**, because its 16 custom
     properties are consumed by superset rows through `var()`;
  2. **any red in the required nine** — no band, no ledger, no known-red allowance.
     `nav-dropdown` was de-listed on 2026-06-11 and `theme-dark.css` *is* the theme surface;
     the only surviving exception, `program-backup.spec.ts:79`, is not in the nine;
  3. **a `fatigue` or `fatigue-stage4-smokes` red**, with the explicit rider that **no fatigue
     threshold, badge or calibration value may be touched under packet authority** — that is
     parked Stage-4 calibration territory;
  4. **"dark-only file" is struck** from the light-difference trigger. F3-agnostic declarations
     legitimately move both themes; the trigger becomes *per-family expectation violated*, not
     *any light difference at all*.
- **Windows visual row gains the 18 `visual-baseline-thumbnails.spec.ts` tests** — the arc
  reconciles against a ledger entry from that spec, and Plan v1 only ever ran it on Linux.

**P3-e — additions**

- Assert the arc-wide 24-block budget, the P3-emitted contract ceiling, the bidirectional
  P3 blind-spot register, and the reconciled N8 denominator.

**D3 — the operative amendment** *(re-review **N7**; Plan v2 dispositioned architecture #12 in
the matrix and never wired it into the plan, which is exactly the failure mode that finding
was about)*:

> **If D3 is granted**, `docs/MASTER_HANDOVER.md`, `docs/ACTIVE_DEVELOPMENT.md` and
> `docs/REFACTOR_PLAN.md` are added to the **"Paths owned"** row of **every** packet
> (P3-a0, P3-a1, P3-b, P3-c, P3-d, P3-e), with the claim restricted to an **append-only** edit
> of the **lead block** and **`## Next Safe Step`** — the two places WP4.4-k's reconciliation
> actually failed. Serialized by the one-at-a-time merge rule, so still single-writer at any
> instant. **If D3 is refused**, P3-e remains the sole writer and no other packet names those
> paths. Either way the ownership rows and the decision agree; Plan v2 had them disagreeing.

### Expected gates per packet — the v2 table

*Re-review **N4**: Plan v2 annotated the Plan v1 gate matrix "superseded by the Plan v2 gate
table below" and then never printed one, leaving the single artifact a packet reads to know
what to run formally void. Reprinted here with the v2 deltas applied. **This table supersedes
the Plan v1 matrix.***

| | P3-a0 | P3-a1 | P3-b | P3-c | P3-d | P3-e |
|---|---|---|---|---|---|---|
| Full `pytest` (cascade contracts inside the total) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| Required nine Chromium specs | — | — | — | ✔ | ✔ | ✔ (full suite) |
| `visual.spec.ts`, 66/platform, `PW_VISUAL_SEED=1` | — | — | — | ✔ | ✔ | ✔ |
| **`visual-baseline-thumbnails.spec.ts`, 18/platform, Windows** *(new — test-strategist #8)* | — | — | — | ✔ | ✔ | ✔ |
| Seven-surface Stylelint, no category rise | anchor only | — | reconcile | ✔ | ✔ | ✔ |
| Linux N8 deep gate vs schema-v2 ledger | — | — | — | ✔ | ✔ | ✔ |
| **N8 denominator reconciled (documentary)** *(new)* | ✔ **produces it** | — | — | ✔ **precondition to dispatch** | ✔ | ✔ |
| Whole-page computed differential, 66 contexts, 0/0 | — | — | control only | ✔ | ✔ | ✔ arc-wide |
| Per-family known-live controls (**O1′**) | — | red-path proofs | ✔ | ✔ | ✔ per token | — |
| Production CSS diff empty (asserted) | ✔ | ✔ | ✔ | — | — | ✔ |
| No snapshot regenerated; committed digest assertion (`a_baseline_contracts.py:234–255`) is the gate, manual `git status` is redundancy | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |

**Read-only packets do not run the E2E or visual gates.** Nothing changed, so a pass would
carry no information — and a gate that cannot fail is worse than no gate.

### Oracle design — v1 rules O1–O11 unchanged; four added

| # | Rule | Origin |
|---|---|---|
| **O10b** | **The deletion-manifest builder derives the set of contract-pinned literals from the contract files' ASTs and refuses any cut that would remove one.** Not a hard-coded exception list — a derived one, so a new pin cannot silently fall outside it. | architecture #2, adjudicated: the specific `:546–548` instance cannot fire, but Ceiling 3 proves the general defect does. |
| **O12** | **Ancestor-composited check.** For any candidate that is an ancestor of a superset row, a differential keyed on the candidate's own computed value is **insufficient** — alpha-composited descendants must be measured as *rendered*, not as *declared*. The probe database must seed `superset_group`; if it cannot, every ancestor of a superset row is **excluded**, because `neverProbed`-by-construction is an exclusion, not a pass. | product-risk #1 |
| **O13** | **`DB_FILE` containment guard.** Every harness refuses to start unless the resolved `DB_FILE` is under `artifacts/`. With `TESTING` unset — which M-h2 requires — startup runs `create_startup_backup()`, which rotates the user's auto-backup ring at keep=7. A forgotten `DB_FILE` across a probe campaign silently destroys seven generations of the user's real backups. | product-risk #4 |
| **O14** | **An assertion satisfiable by absence is not a gate.** Any contract this arc writes or strengthens must be shown to fail when the thing it protects is removed — not merely when something unrelated changes. Two live instances: `test_the_certified_removals_stay_removed`'s `<= 1`, and `test_css_cascade_contracts.py:1007`'s bare substring check. | test-strategist, generalized |
| **O15** | **Red paths are committed executed fixtures, not prose.** A red path recorded in markdown is unverifiable at review time and rots silently. | test-strategist #6 |

**O1 is amended, not merely retained** (architecture-reviewer #5). Plan v1's bracket —
*"≥1 computed value in that family's own theme and 0 in the other"* — is **false for four
rules**: `theme-dark.css:239–246`, `:249–257`, `:259–262` and `:268–270` carry no
`[data-theme="dark"]` and match in **both** themes. A *correct* control on those rules moves
both, which Plan v1's O1 would have read as a failed control and sent into an
unfalsifiable re-instrument loop. The amended rule:

> **O1′** — every family carries a committed, digest-pinned known-live mutation sited inside
> its own region, and the **expected partition is declared per family before the control
> runs**: dark-scoped families must move their own theme and **0** in the other;
> **theme-agnostic families (F3-agnostic) must move both**. A control whose result contradicts
> its declared partition fails; a control that moves **nothing** excludes the family. The
> partition is a per-family property, never a property of the file.

### Standing risk — recorded, not resolved (test-strategist #6)

With the pixel matrix ruled out as evidence (**O7**), the entire proof burden sits on
instruments **P3-a writes and P3-a certifies**, with no independent check. Of the gate set:
full `pytest` is string pins, the required nine are functional, Stylelint is lint, and the
Linux N8 gate is the same pixel oracle carrying the same `visual-helpers.ts` blind spots. The
only gate that reads the neutralized properties is the computed differential — which this plan
itself says returns an uninformative zero here unless bracketed by O1′. So deletion authority
reduces to **(removal oracle ∩ census ∩ recount) × O1′**, all self-certified in one packet.

**This repository has already shipped two self-authored controls that cannot fail** — the
`occurrences <= 1` assertion and `measure.verify_blind_spots()`. That is the base rate this
arc is working against, and it is why P3-a's red paths must be executed fixtures (**O15**),
why **O14** applies to every contract this arc writes, and why **AB-1** ends the arc on
instrument-control failure rather than triggering a repair loop. No mitigation makes this risk
zero; it is recorded so the owner accepts it explicitly at Gate 1 rather than discovering it.

### Sequence

Unchanged from Plan v1 except: Gate 0 now covers **Q1, Q3, Q4, Q5, Q6, Q8, Q9** (Q2 and Q7
withdrawn); P3-a gains the register-emitted ceiling, the nineteen-tool assessment, the C7
ledger read, the `superset_group` seeding, the N8 denominator reconciliation, the `DB_FILE`
guard, the post-startup frozen artefact, the bidirectional register, the executed red-path
fixtures and the first `.mjs` pytest coverage in the repository; P3-b gains the machine-derived
disjoint partition and the ancestor-composited check; P3-c/P3-d gain four rollback triggers and
the 18 Windows thumbnail tests; the 24-block budget is arc-wide.

**One effort note.** P3-a grew materially at council and is the packet most likely to be
mis-sized. It stays **L**, but two of the additions cut in opposite directions: the
nineteen-tool assessment may *reduce* the number of new tools below the seven Plan v1 proposed,
while the first-ever `.mjs` pytest coverage, the bidirectional register and the N8 denominator
reconciliation each add work Plan v1 did not price. P3-a's first deliverable should be a
re-scoped tool list, presented before it builds anything.

### Abandonment criterion

**Unchanged in structure from Plan v1** — AB-1 (instrument failure at P3-a), AB-2 (empty
certified yield at the P3-b checkpoint), AB-3 (continuous per-family narrowing), and the
explicit statement that a line-count shortfall is neither an abandonment trigger nor an
acceptance criterion. **No reviewer challenged it**, and product-risk-reviewer explicitly
endorsed the default trajectory it produces: *"the default trajectory on weak evidence is
'delete nothing,' which is the right default."*

Three clarifications added at council:

1. A family excluded under **O12** (superset ancestor, unseeded) or **O13** counts toward
   AB-2's "every candidate lands in an exclusion bucket" test exactly as any other exclusion.
2. **AB-1 is restated as terminal, not iterative** (test-strategist #6): a failed instrument
   control ends the arc at P3-a. It does not license a repair-and-retry loop, because the
   instrument is self-certified and an unbounded retry loop against a self-certified control
   is how a gate that cannot fail gets built.
3. A family whose **O1′ partition is contradicted** — rather than merely quiet — is excluded,
   not re-instrumented, unless the contradiction is traced to a named harness defect with its
   own red path.

---

## Plan v2 re-review (architecture-reviewer, agent `a9ceef15d1ad059e4`)

**Verdict: BLOCKING lifted → approve-with-changes.** This is the **final review round**; no
further revision cycle follows.

### Result on the original 15

**Cleared — 13:** #1 (Ceiling 3 + Q8 + F2 redefined "less `.frame-header`"), #2 (*"exactly the
fix I proposed"*), #3, #4, #5 (substance), #6 (mechanism), #7 (all 14 ceiling rows verified
against source; `.value-changed` exactly 7, zero headroom — confirmed), #8 (*"not evasion:
Tier 2 removes nine obligations from the owner's desk"*; every Tier-2 citation verified exact),
#9, #10, #13, #15 (19 files confirmed).
**Recorded — 1:** #14.
**Retracted by the reviewer — 1:** **#11.** The reviewer verified the rejection and withdrew
its own finding; the manager confirmed independently that
`CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` → `uncertifiableElements.elements[]` carries all 8
with both `domPath` and `selector`, committed, with no `artifacts/` dependency.
**Not cleared — 1:** **#12** — dispositioned in the matrix only, never reaching the plan.

### Eight new findings (verbatim)

**N1 (blocking-class).** `measure.contract_anchors()` / `pinned_declarations()` both iterate `CONTRACT_FILES` (`measure.py:273`, `:332`), which is only the two shared files (`:34-37`). Run today the mechanical ceiling emitter produces **Ceiling 3 and nothing else** — it cannot reach 12 of the 14. So AC7 / P-8 is unbuildable as written. And extending `CONTRACT_FILES` changes both registers, which `a_baseline_contracts.py:297-298` pins to the committed `CSS_PHASE4_WP4_4_A_BASELINE.json` — redding a contract P3-a's own exclusions row calls "run always, edited never". Fix: give P3-a a **P3-owned** emitter walking every working-tree reader of `theme-dark.css` independently of `measure.CONTRACT_FILES`; or open extending it as an owner question naming the baseline regeneration.

**N2 (blocking-class).** The bidirectional blind-spot register repair you accepted in full from test-strategist #5 cannot ship: `a_baseline_contracts.py:224` asserts `len(register) == len(measure.BLIND_SPOT_REGISTER)` against the committed baseline. Adding the eight missing neutralizers changes that length, so it needs either a baseline regeneration or an edit to `a_baseline_contracts.py` — the latter forbidden, the former unclaimed, and **Q1 covers neither**. Open this as **Q10** and name the owned path in P3-a.

**N3.** The superset-seeding obligation contradicts "reused unmodified" and voids its own sqlite3 exception, which is explicitly conditioned on not modifying `i_seed_probe_db.py`. Danger: an implementer seeds the **committed** fixture `e2e/fixtures/database.visual.seed.db` instead of the `--out` copy, changing what `PW_VISUAL_SEED=1` renders and forcing the rebaseline this arc forbids absolutely. Fix: name `scripts/css_audit/p3_seed_probe_db.py` in P3-a's owned paths, state it writes only the `--out` copy and never the committed fixture, and extend the scoped exception to it by name.

**N4.** Plan v1's gate matrix at `:833-843` is annotated "Superseded by the Plan v2 gate table below" — **and Plan v2 has no gate table.** The one artifact a packet reads to know what to run is formally void. Reprint it with the v2 deltas applied (+18 Windows thumbnails, N8 denominator as a P3-c precondition), or strike the annotation and list the deltas as amendments.

**N5.** The corrected family table still double-assigns and has no precedence order: `:268-270` is `:where(#darkModeToggle:hover)` and F5's predicate includes `:hover`; `:259-262`'s only declaration is `color: #0d6efd !important`, which by F2's residual definition is F2, not F3-agnostic "normal declarations". Fix: state an ordered predicate chain (F1 → F5 → F6 → F4 → F3-dark/F3-agnostic → F2 residual) and drop both ranges from the F3-agnostic note.

**N6.** `test_the_contract_anchor_registry_is_exact` **does not exist**. The real name is `test_contract_anchor_register_covers_every_shared_surface`, `a_baseline_contracts.py:285`; the cited assertion line `:297` is right. Fix all three sites.

**N7.** Your #12 disposition lives in the matrix only. "Changes to the packets" has no such amendment, `:1190-1192` says attribute tables are unchanged except where amended below, and D3 is in neither the Gate-0 checklist nor the Gate-1 sign-off. Fix: one operative bullet under "Changes to the packets", and add D1–D4 to the Gate-1 sign-off list.

**N8.** P3-a must reconcile the N8 denominator but is forbidden from running N8. Say the reconciliation is **documentary** — `deep-gate.yml`, the ledger's `scopeNote` (`:177`), and the 66+18 baseline pins — and that no dispatch is authorised at P3-a.

### Structural recommendation (verbatim)

> **P3-a is no longer one packet** and should split into **P3-a0** (audit + ceiling emission +
> tool list, read-only) → **P3-a1** (apparatus repair + oracle build). Reasoning: P3-a now
> carries four units with different blast radii, and the unit that *repairs already-certified
> WP4.4 apparatus* is the same packet whose instruments are *measured against* that apparatus —
> a self-certification loop. Your own "present a re-scoped tool list before building anything"
> is already a checkpoint in disguise. Your call, with reasons either way; if you accept,
> renumber cleanly and keep the DAG linear.

### Disposition table — re-review

| # | Disposition | Action |
|---|---|---|
| **N1** | **accept** | Verified: `CONTRACT_FILES` at `measure.py:34–37` is exactly the two shared files, so the Plan v2 emitter would have reached **2 of 14 rows**. Route (a) taken — **P3-a0 owns `scripts/css_audit/p3_ceiling.py`**, walking every working-tree reader independently of `CONTRACT_FILES`, touching nothing shared and moving no baseline. Route (b) folded into **Q10** as the optional half. |
| **N2** | **accept** | Verified at `a_baseline_contracts.py:212–224` (`test_oracle_blind_spot_register_matches_the_live_helper`). **Q10 opened.** Also de-risked so the arc never depends on the answer: **P3-a1 owns a P3-local bidirectional register** (`p3_blind_spots.mjs`) and **O7 derives from it**. Q10 then governs only whether the *shared* defect is also repaired — which matters because `QUALITY_GATE.md:39` routes every future CSS packet into it. |
| **N3** | **accept** | The contradiction was real and the named danger is the more serious half: seeding the committed `e2e/fixtures/database.visual.seed.db` would change what `PW_VISUAL_SEED=1` renders and force the one thing this arc forbids absolutely. **`scripts/css_audit/p3_seed_probe_db.py` is now a P3-a1 owned path**, writes only its `--out` copy, never the committed fixture; the scoped raw-`sqlite3` exception extends to it **by name**; `i_seed_probe_db.py` stays unmodified. |
| **N4** | **accept** | Correct and embarrassing: Plan v2 voided the Plan v1 gate matrix and printed no replacement. **The v2 gate table is now printed** with both deltas applied and the two new rows, and it states that it supersedes the v1 matrix. |
| **N5** | **accept** | Both corrections verified against the file. **Ordered predicate chain adopted exactly as proposed**; `:268–270` and `:259–262` dropped from F3-agnostic. **Extended beyond the finding:** because F2-residual now demonstrably contains both theme-scoped and theme-agnostic members, **O1′'s expected partition is declared per control keyed on the controlled declaration's own selector**, not per family — the family-level phrasing Plan v2 shipped would have failed on `:259–262`. |
| **N6** | **accept** | Verified: the real name is `test_contract_anchor_register_covers_every_shared_surface` at `a_baseline_contracts.py:285`; `:297` was right. **All three of my sites corrected.** Provenance recorded rather than quietly fixed: the wrong name entered through test-strategist #3's *verbatim* text and I propagated it without checking, having read the real name earlier in the same session. The verbatim reviewer text is left unaltered, as the template requires. |
| **N7** | **accept** | The finding is self-demonstrating — a disposition that never reaches the plan is not a disposition. **D3 now has an operative bullet** under *Changes to the packets*, stating both branches, and **D1–D4 are in the Gate-1 sign-off list**. |
| **N8** | **accept** | Correct: P3-a0 is read-only and cannot dispatch a CI deep gate. The reconciliation is now explicitly **documentary** — `deep-gate.yml`, the ledger `scopeNote` `:177`, and the 66 + 18 pins at `a_baseline_contracts.py:39–44` — and the closure is a **precondition on P3-c**, the packet that actually dispatches. |
| **#12** *(carried, not cleared)* | **accept — now wired** | See N7. Plan v2 had it in the matrix only; it is now in the plan. |
| **Structural — split P3-a** | **ACCEPTED** | Adjudicated in *Packets* above with reasons. The decisive argument is the reviewer's self-certification loop; two further reasons are that **Q10 and N1 both resolve inside the old P3-a**, so a refusal would strand a half-built oracle, and that **P3-a0's outputs are the evidence the owner needs to answer Q10** — which cannot hold if the packet the answer governs produces them. Arc goes **5 → 6 packets**; DAG stays linear; no concurrency claim changes. |

---

## Sign-off

- [ ] **Gate 0 — UNSIGNED.** Open: **Q1, Q3, Q4, Q5, Q6, Q8, Q9, Q10**. *(Q2 and Q7 withdrawn
      at council.)*
- [x] **Every finding has a disposition** — **MET.** All **41** are dispositioned: council 33
      (architecture 15, test-strategist 11, product-risk 7) + re-review 8. **38 accepted ·
      3 partial · 0 deferred · 0 rejected outright**, plus the structural split recommendation
      **accepted**. All four reviewer outputs are reproduced verbatim.
- [x] **Agent provenance complete** — both `product-manager` IDs (`a72cabec430ff9c82`, the same
      agent resumed via `SendMessage`), the three council reviewer IDs, the re-review ID
      `a9ceef15d1ad059e4`, and the evidence-gap line: **`none`**.
- [ ] **Gate 1 — UNSIGNED.** All reviewer verdicts are now **approve-with-changes**; the
      architecture-reviewer's BLOCKING verdict was lifted at re-review. Gate 1 additionally
      requires the owner to decide:
      - [ ] **D1** — does P3-c need its own owner checkpoint before the first cut?
      - [ ] **D2** — per-packet contract files, permanently, no consolidation?
      - [ ] **D3** — per-packet status-doc appends at merge time, or P3-e as sole writer?
      - [ ] **D4** — does this arc need its own `QUALITY_GATE.md` note? *(recommendation: no)*
      - [ ] **The P3-a split** — accepted by the author at re-review; it changes the packet
            count **5 → 6** and is the owner's to confirm.
- [ ] Ready to implement — proceed to code, then `/unslop` or `/verify-and-polish` for the
      diff-time gate.

**Standing risk the owner accepts at Gate 1, or does not:** deletion authority in this arc
reduces to instruments **P3-a1** both writes and certifies, with no independent check — see
*Standing risk* in Plan v2. The P3-a0/P3-a1 split narrows it (the apparatus repair is no longer
in the same packet as the instruments measured against it) but does not eliminate it.

**Review rounds are closed.** Four reviewer passes, 41 findings, all dispositioned. This
document now waits on the owner, not on another agent.

---

## See also

- [`docs/CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md`](../CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md) §5 (proposal P3), §7 (gates)
- [`docs/CSS_PHASE4_WP4_4_J_THEME_DARK_EVIDENCE.md`](../CSS_PHASE4_WP4_4_J_THEME_DARK_EVIDENCE.md) — the packet that measured the inertia
- [`docs/CSS_PHASE4_WP4_4_H_COMPONENTS_DEAD_EVIDENCE.md`](../CSS_PHASE4_WP4_4_H_COMPONENTS_DEAD_EVIDENCE.md) — the removal-oracle design this arc rebuilds
- [`docs/CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md`](../CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md) §8 (blind-spot register), §12 (gates)
- [`docs/css_phase4_wp4_4/PLANNING.md`](../css_phase4_wp4_4/PLANNING.md) — R1–R6, N1–N10, G1–G11, M1–M12, V1–V6
- [`docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json`](../CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json) — schema v2, 11 reds, two spec files
- [`docs/ai_workflow/QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) — plan-stage routing; the `static/css/**` row
- [`.claude/rules/verification.md`](../../.claude/rules/verification.md) — durable oracle-validation method
