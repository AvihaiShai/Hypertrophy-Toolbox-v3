# Plan Review — WPB.4 (OD4) Weekly-summary `Unassigned` bucket for falsy routines

> # ✅ SHIPPED 2026-08-01 — PR #256, squash `9fe5dbd`. DO NOT EXECUTE THIS PLAN.
>
> **This document is a historical record, not a work order.** Everything below —
> the Gate 1 authorization, the 15-step **Sequence**, and every imperative
> instruction — **has already been carried out.** `utils/weekly_summary.py` now
> buckets falsy routines as `Unassigned`; the goldens were regenerated once, under
> review, and merged.
>
> **Re-running any step would cause damage, not duplication.** Step 8 sets
> `GENERATE_GOLDEN` and regenerates `tests/goldens/weekly_summary_golden.json` — a
> protected calculation zone. That flag is **shared** with
> `tests/test_fatigue_golden.py`, so re-running it would also silently re-baseline
> `tests/goldens/fatigue_golden.json` while both tests report `skipped`, under an
> active calibration freeze.
>
> Gates at merge: **18/18 checks green**. Write set held to D4 (a) / D5 (a) — no
> `static/js/**`, `templates/**`, or `e2e/**`. Verified post-merge against
> `origin/main`.
>
> *Line-number citations below (notably **F13**'s pointers into
> `MASTER_HANDOVER.md`) were accurate when written and have since drifted. They are
> historical references to edits already made — do not follow them as instructions.*

*Protected calculation zone. Plan-stage size is **Large** under
[QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) — "any
schema/API/calculation-surface change" — so **both** Gate 0 and Gate 1 are required.
Nothing below authorizes an edit to `utils/weekly_summary.py`.*

**Status: Gate 0 ✅ APPROVED · council complete (3 reviewers, 19 findings, all
dispositioned) · Gate 1 ✅ APPROVED 2026-08-01 with D4 (a), D5 (a), D2 re-put
confirmed and F12 acknowledged. Implementation authorized on branch
`wt/wpb4-unassigned-bucket` — and **since executed and merged as `9fe5dbd`**.**

---

## Section 0 — Requirements Brief

**Raw request** (verbatim)

> TASK: WPB.4 (OD4) - weekly summary buckets falsy-routine rows as `Unassigned`
> instead of dropping them from frequency, matching session_summary.
>
> This is a PROTECTED CALCULATION CHANGE. Do NOT start implementing.
> Step 1 is Gate 0 + /council-plan. Only implement after owner sign-off.
>
> THE DECISION THAT MUST NOT BE MADE IMPLICITLY
> Whether `global_sessions` includes the synthetic Unassigned bucket. The plan
> requires this be decided separately and explicitly. Surface it at Gate 0 with
> a recommendation and the consequences either way. Do not let it fall out of
> the implementation.
>
> FACTS ALREADY ESTABLISHED - do not re-derive
> - Production schema is `routine TEXT NOT NULL`, so the reachable case is the
>   EMPTY STRING. `None` only matters for mocked/legacy rows. All falsy values
>   coalesce into ONE synthetic bucket - state that assumption explicitly.
> - Prerequisite is satisfied: WP2.3 goldens landed in 3696fdc.
> - The golden WILL change, on purpose, and the expected delta is already
>   written down. Calves sentinel: frequency 0->1; effective sets_per_session
>   0.85->5.1; raw sets_per_session 1->6; effective avg/max 0/0 -> 5.1/5.1.
>   Weekly totals and classifications MUST remain identical. Regenerate the
>   golden only after reviewing the exact delta against that expectation.
> - Known quirk locked by the golden, leave as-is: 'Calves' does not contain
>   substring 'calf', so _infer_pattern falls through to 'other'.
>
> SCOPE FREEZE - these must not change: weekly raw/effective totals, reps,
> volume, status, contribution weights, rounding, response fields, pattern
> coverage. Session-derived metrics only.
>
> TEST COVERAGE required by the gate: empty-string and None routines; frequency
> thresholds above and below 1.0; multiple anonymous rows accumulating into one
> bucket; mixed named/anonymous routines - across the FULL counting-mode x
> contribution-mode matrix.
>
> GATES: weekly-summary pytest + reviewed intentional golden diff + summary-page
> functional and visual E2E. product-risk review required before merge. PR needs
> migration notes describing the intentional semantic change and the
> conservative one-bucket assumption.

**Problem**

`utils/weekly_summary.py` and `utils/session_summary.py` disagree about what a
falsy `routine` value means, and the disagreement is user-visible.

`session_summary.py:90` coalesces a falsy routine into a named bucket
(`row.get('routine') or 'Unassigned'`), so those rows appear as a session.
`weekly_summary.py:139-140` guards the same accumulation with `if routine:`, so
those rows contribute **volume** but are silently excluded from the frequency
signal. The consequence on `/weekly_summary` is that a muscle trained only in
rows with no routine name reports **0 in the "Routines" column** while
simultaneously reporting non-zero Effective Sets and Total Volume in the same
table row — the page shows work that was apparently performed in zero sessions.

The same muscle's per-session figures are then divided by an unrelated
denominator: `weekly_summary.py:174` falls back to `len(global_sessions)`, the
count of *all other* distinct named routines, so its `sets_per_session` is
diluted by sessions it never appeared in.

`docs/DUPLICATION_REGISTRY.md` row 4 records this as the OD4/WPB.4 seam and
freezes it pending exactly this owner decision.

**Acceptance criteria**

1. Given a `user_selection` row whose `routine` is the empty string `''`, when
   `calculate_weekly_summary()` runs, then that row's effective contribution is
   accumulated into a single session bucket named `Unassigned` rather than
   discarded, in all four `counting_mode` × `contribution_mode` combinations.
2. Given a `routine` of `None` (reachable only from mocked or legacy rows, not
   from the production schema), when `calculate_weekly_summary()` runs, then it
   is treated identically to `''` and lands in the same `Unassigned` bucket.
3. Given several rows with differing falsy routine values in the same plan, when
   `calculate_weekly_summary()` runs, then they accumulate into **one** bucket —
   the summary must never report more than one anonymous session.
4. Given a muscle whose `Unassigned` bucket accumulates **≥ 1.0** effective sets,
   when the summary is built, then its `frequency` includes that bucket
   (contributing exactly 1), and `avg_sets_per_session` / `max_sets_per_session`
   are computed from it.
5. Given a muscle whose `Unassigned` bucket accumulates **< 1.0** effective sets,
   when the summary is built, then the bucket does **not** raise `frequency` —
   the existing `>= 1.0` threshold applies to the synthetic bucket on exactly the
   same terms as to a named routine.
6. Given a plan mixing named and anonymous routines, when the summary is built,
   then a muscle trained in both counts the named routines and the single
   `Unassigned` bucket additively.
7. Given any plan, when the summary is built, then `weekly_sets`,
   `raw_weekly_sets`, `effective_weekly_sets`, `total_reps`, `total_volume`,
   `raw_total_reps`, `raw_total_volume`, `status` and `volume_class` are
   **bit-identical** to the pre-change output. The change is observable only in
   `frequency`, `sets_per_session`, `avg_sets_per_session` and
   `max_sets_per_session`.
8. Given any plan, when the summary is built, then the set of muscle keys in the
   returned dict is unchanged. `Unassigned` is a **session-bucket key inside
   `sessions_by_muscle`**, never a new muscle row in the output.
9. Given the WP2.3 golden scenario, when the golden is regenerated, then the diff
   is confined to the `Calves` sentinel and matches the pre-written expectation
   in `docs/REFACTOR_PLAN.md` §WPB.4 exactly (see the worked example below).
10. Given `/weekly_summary` rendered in a browser, when a muscle is sourced only
    from anonymous rows carrying ≥ 1.0 effective sets, then its **"Routines"**
    column reads `1` rather than `0`.
11. Given `calculate_pattern_coverage()`, when it runs on any plan, then its
    output is unchanged — `_tally_patterns` continues to key falsy routines as
    `''`, and no `Unassigned` or `Unknown` key appears.

**Calculation surface**

- Functions changed:
  - `utils.weekly_summary._aggregate_weekly_volumes` — the `if routine:` guard at
    `weekly_summary.py:139` and the `routine` binding at `weekly_summary.py:70`.
  - `utils.weekly_summary.calculate_weekly_summary` — **not changed.** The
    `global_sessions` comprehension at `weekly_summary.py:244` stays exactly as
    it is, per the owner's resolution of Open Question 1 (Option A, 2026-08-01).
  - `utils.weekly_summary._build_weekly_summary_output` — **not changed**. It
    already handles a populated `muscle_sessions` correctly; the fix is upstream.

- Worked example — the WP2.3 golden `Calves` sentinel. `Calf Raise` is seeded at
  `tests/test_weekly_summary_golden.py:131` with `routine=''`, 6 sets, reps 8–10,
  RIR 2, 50 kg. `Calves` is sourced from **no other row**. The seed also contains
  6 distinct named routines, so `len(global_sessions) == 6`.

  | Field | Before | After (measured) |
  |---|---:|---:|
  | `frequency` | `0` | `1` |
  | `sets_per_session` (effective modes) | `0.85` | `5.1` |
  | `sets_per_session` (raw modes) | `1.0` | `6.0` |
  | `avg_sets_per_session` (all modes) | `0.0` | `5.1` |
  | `max_sets_per_session` (all modes) | `0.0` | `5.1` |
  | `effective_weekly_sets` | `5.1` | `5.1` (unchanged) |
  | `raw_weekly_sets` | `6.0` | `6.0` (unchanged) |
  | `total_reps` / `total_volume` | `45.9` / `2295.0` | unchanged |
  | `status` / `volume_class` | `low` / `low-volume` | unchanged |

  Before, `frequency == 0` forces the `weekly_summary.py:174` fallback
  `session_count = len(global_sessions) = 6`, so `5.1 / 6 = 0.85`. After, the
  `Unassigned` bucket holds 5.1 effective sets, clears the `>= 1.0` threshold,
  and yields `frequency = 1`, so `session_count = 1` and `5.1 / 1 = 5.1`.

  This was **measured**, not projected: a read-only harness seeded the golden
  scenario and ran the current and candidate aggregations side by side. The
  measured delta is exactly the four fields above on `Calves` across all four
  modes, and **nothing else in the entire golden**. It reproduces the
  `docs/REFACTOR_PLAN.md` §WPB.4 expectation field for field.

- Migration notes: the PR description will state that this is an **intentional
  semantic change** to a protected calculation, name the four affected response
  fields, record the conservative one-bucket assumption (all falsy routine values
  — `''`, `None`, and any other falsy value — coalesce into a single synthetic
  session, never one bucket per distinct falsy value), record the resolution of
  Open Question 1 with its rationale, and link the reviewed golden diff. Test
  coverage is extended per criteria 1–8 across the full counting × contribution
  matrix before the golden is regenerated.

**In scope**

- `utils/weekly_summary.py` falsy-routine bucketing for the frequency signal.
- New pytest coverage in `tests/test_weekly_summary.py` for criteria 1–8 across
  the full `counting_mode` × `contribution_mode` matrix.
- One reviewed, intentional regeneration of
  `tests/goldens/weekly_summary_golden.json` — **after** the diff is read against
  criterion 9, never to make a red test pass.
- A route-level assertion that the `/weekly_summary` JSON payload carries the
  corrected `frequency`, `avg_sets_per_session` and `max_sets_per_session`.
- An E2E assertion in `e2e/summary-pages.spec.ts` for the rendered **"Routines"**
  column (criterion 10).
- The export pytest family, added to the required gate per decision **D2**, plus
  a migration note that the exported "Weekly Summary" workbook figures change.
- Migration notes in the PR description.

**Out of scope / non-goals**

- `utils/session_summary.py` — it is already correct and is the model being
  matched. Not touched.
- `utils/fatigue_data.py` — it coalesces falsy routines to a `''` key
  (`fatigue_data.py:100,123`), a **third** convention. Unifying it is a separate
  behavior change with its own fatigue goldens and calibration freeze. This
  packet leaves it alone, so the seam narrows from three conventions to two.
- `calculate_pattern_coverage()` / `_tally_patterns` — frozen by criterion 11.
  `_tally_patterns` reads `row.get('routine', 'Unknown')`, whose default fires
  only on a **missing key**, so an empty-string routine keys as `''` today. The
  golden locks `''` in `per_routine` and `sets_per_routine`. Not touched.
- Weekly totals, reps, volume, status, contribution weights, rounding, and the
  response field list — frozen by criterion 7.
- Renaming or re-labelling the "Routines" column, or adding any `Unassigned` row
  to the weekly table.
- The `docs/REFACTOR_PLAN.md:1601` stale-status row, which is being corrected in
  its own separate docs-only PR.

**Assumptions made**

- ⚠️ **The bucket label is exactly `Unassigned`**, matching
  `session_summary.py:90` byte for byte. Not owner-confirmed as user-facing copy,
  though it is currently invisible on `/weekly_summary` — the bucket is a
  dictionary key used for counting, and the page renders only the resulting
  integer in the "Routines" column. It becomes visible only if a future packet
  displays session names.
- ⚠️ **One bucket for all falsy values.** `''`, `None`, and any other falsy
  routine collapse into a single synthetic session. The conservative reading:
  the alternative — one bucket per distinct falsy value — would let `''` and
  `None` count as two separate sessions, which no user action can distinguish.
- ⚠️ **The `>= 1.0` effective-set threshold applies unchanged to the synthetic
  bucket.** The alternative (always counting the bucket as one session
  regardless of magnitude) would make the synthetic bucket privileged over named
  routines. Criteria 4 and 5 pin the symmetric reading.
- ⚠️ **`avg_sets_per_session` and `max_sets_per_session` remain
  effective-derived in RAW counting mode.** This is why the worked example shows
  `5.1`, not `6.0`, in raw mode — `weekly_summary.py:192-193` reads
  `weekly_eff_sets` and the effective-valued `muscle_sessions`. Pre-existing
  behavior, deliberately preserved, and the reason the raw-mode rows of the
  expected delta read `5.1/5.1` rather than `6.0/6.0`.
- ⚠️ **The Excel export is an affected consumer that the risk-mitigation gate
  does not name.** `utils/export_service.py:317,382,443` call
  `calculate_weekly_summary()`, and `_weekly_summary_to_rows`
  (`export_service.py:174-181`) splats **every** stat field — including
  `frequency`, `sets_per_session`, `avg_sets_per_session` and
  `max_sets_per_session` — into the "Weekly Summary" sheet. The numbers in an
  exported workbook therefore change. Recommend adding the export pytest family
  to the gate; see Open Question 2.
- ⚠️ **`sets_per_session`, `avg_sets_per_session` and `max_sets_per_session` are
  not rendered on `/weekly_summary`.** The table renders Muscle Group, Effective
  Sets, Raw Sets, **Routines** (= `frequency`), Total Volume and Volume
  Classification (`static/js/modules/weekly-summary.js:207-222`). So the gate's
  "route/E2E assertions for the displayed frequency and average/max-per-session
  values" splits: `frequency` is E2E-assertable in the DOM; the average/max are
  assertable only at the route/JSON and Excel layers.

**Open questions for the user**

> **Q1 and Q2 are RESOLVED by the owner on 2026-08-01.** Q1 → **Option A
> (exclude)**. Q2 → **yes, extend the gate to the Excel export**. The reasoning
> that produced each recommendation is retained below as the decision record;
> the resolutions are restated in the Decisions section that follows.

**Q1 — BLOCKING. Does `global_sessions` include the synthetic `Unassigned`
bucket?** This is the decision the plan requires be made explicitly.
**RESOLVED: Option A — exclude.**

`global_sessions` (`weekly_summary.py:244`) is used at one place only —
`weekly_summary.py:174`, as the fallback denominator for `sets_per_session` when
a muscle's `frequency` is `0`. It therefore affects **only muscles that reach
≥ 1.0 effective sets in no session at all**, and never affects `Calves`, whose
frequency becomes 1 either way.

Both options were measured against the golden scenario:

| | Option A — **exclude** (recommended) | Option B — include |
|---|---|---|
| Code | `weekly_summary.py:244` unchanged | `{row.get('routine') or 'Unassigned' for row in rows}` |
| Golden delta | `Calves` only — exactly the 16 field changes the plan predicted | Same, **plus** `Forearms.sets_per_session` `0.13 → 0.11` (effective modes) and `0.33 → 0.29` (raw modes) |
| Matches the pre-written expected delta | **Yes, exactly** | No — adds an unpredicted delta |
| General blast radius | None beyond the bucket itself | Every zero-frequency muscle in any plan containing at least one anonymous row is diluted by a larger denominator |
| Semantic coherence | Split: the bucket is a session for frequency but not for the legacy fallback denominator | Uniform: the bucket is a session everywhere |

**Recommendation: Option A (exclude).**

The decisive measured fact is that Option B changes `Forearms` — a muscle with
**no anonymous rows whatsoever**. Its two exercises sit in the named routine
`Freq B` and sum to 0.77 effective sets, below the 1.0 threshold, so its
`sets_per_session` falls back to the global denominator. Including the synthetic
bucket raises that denominator from 6 to 7 and silently shrinks the reported
figure for a muscle the change has nothing to do with. Generalized: **Option B
lets one unnamed row perturb the per-session numbers of every unrelated
low-frequency muscle in the plan.**

Option A's asymmetry is real but narrow, and it is not a new inconsistency:
`frequency` and `global_sessions` already measure different things today —
`frequency` counts sessions where *this muscle* cleared 1.0 effective sets, while
`global_sessions` counts *all* distinct routines. They were never the same
denominator. Option A leaves that legacy fallback exactly as it is and confines
the packet to the frequency signal, which is what the scope freeze asks for.

If the owner prefers Option B for uniformity, it is defensible — but then the
pre-written expected golden delta in `docs/REFACTOR_PLAN.md` §WPB.4 is
**incomplete** and must be amended to include the `Forearms` rows before the
golden is regenerated, otherwise the reviewer checking the diff against the
written expectation will find an unexplained change and should reject it.

**Q2 — Non-blocking. Extend the gate to the Excel export?** The risk-mitigation
gate names weekly-summary pytest, the golden diff, and summary-page
functional/visual E2E. It does not name the export path, which
`utils/export_service.py` makes a genuine consumer of all four changed fields.
Recommend adding the export pytest family to the required gate and noting the
workbook change in the migration notes. Proceeding without it would ship a
user-visible spreadsheet change with no test asserting it.
**RESOLVED: yes — the export pytest family joins the required gate.**

**Q3 — Non-blocking, confirm the read.** The gate asks for "route/E2E assertions
for the displayed frequency and average/max-per-session values". Since the
average/max are not rendered anywhere on `/weekly_summary` (see the last
assumption above), the intended reading is taken to be: assert `frequency` in the
DOM via `e2e/summary-pages.spec.ts`, and assert the average/max in the route JSON
via pytest. Confirm, or name the surface where those values were expected to be
displayed.
**RESOLVED as D3: confirmed — `frequency` in the DOM, average/max through route
JSON and export tests. No new UI is added to display them.**

**Owner decisions — signed 2026-08-01**

| # | Decision | Resolution | Consequence carried into Plan v1 |
|---|---|---|---|
| **D1** | Does `global_sessions` include the synthetic `Unassigned` bucket? | **No — Option A, exclude.** | `weekly_summary.py:244` is **not** touched. The packet's write set is confined to `_aggregate_weekly_volumes`. The golden delta is the `Calves` sentinel only, matching `docs/REFACTOR_PLAN.md` §WPB.4 field for field — no amendment to the written expectation is required. A reviewer reading the regenerated diff against that expectation must find **zero** unexplained rows; a `Forearms` row appearing in the diff is a signal that Option B was implemented by accident and is grounds to reject the change. |
| **D2** | Extend the required gate to the Excel export path? | **Yes.** | The export pytest family joins the required gate, and the migration notes state that the exported "Weekly Summary" workbook figures change. |
| **D3** | Which surface asserts which changed field? | **`frequency` in the DOM; average/max via route JSON and export tests.** | `e2e/summary-pages.spec.ts` asserts the rendered "Routines" column only. `avg_sets_per_session` / `max_sets_per_session` are asserted at the route-JSON layer and in the export tests, because they are not rendered on `/weekly_summary`. No new UI is added to display them. |

D1 is the decision `docs/REFACTOR_PLAN.md` §WPB.4 required be made separately and
explicitly rather than falling out of the implementation. It is made, recorded,
and load-bearing on the golden review.

### Section 0 sign-off — GATE 0 ✅ APPROVED 2026-08-01
- [x] User confirms the acceptance criteria match intent.
- [x] User reviewed the assumptions and corrected or accepted each one —
      **all six accepted as written**: the exact `Unassigned` label; one bucket
      for all falsy routines; the existing `>= 1.0` threshold applied
      unchanged; effective-derived avg/max unchanged in RAW mode; the Excel
      export as an affected consumer included in the gate; and the
      not-rendered-on-page reading of the per-session fields.
- [x] Blocking questions are answered — **Q1 resolved as D1 (Option A,
      exclude)**, Q2 as D2 (export gate), Q3 as D3 (DOM asserts `frequency`;
      route JSON + export tests assert average/max).

**Gate 0 is APPROVED. Proceed to `/council-plan` for Plan v1 → council → Plan v2
→ Gate 1.** Implementation remains unauthorized until Gate 1 is signed.

---

## Plan v1

> **SUPERSEDED by Plan v2 below** (council run 2026-08-01). Retained **unedited**
> as the artifact the reviewer findings and the response matrix answer. Three of
> its premises are refuted by the council — see F1, F2 and F3 in the response
> matrix. **Do not implement from this section.**

*Drafted 2026-08-01 after Gate 0 approval. **Not authorization to implement** —
council review (step 2) and Gate 1 sign-off are still outstanding.*

**Goal**: A muscle trained only in rows with no routine name reports its work as
one real session on `/weekly_summary` — "Routines" reads `1` instead of `0`, and
its per-session figures stop being divided by unrelated routines — while every
weekly total, classification and response field stays bit-identical.

**Scope**

- **In**
  - `utils/weekly_summary._aggregate_weekly_volumes` only: the `routine` binding
    at `weekly_summary.py:70` and the `if routine:` guard at
    `weekly_summary.py:139-140`, so falsy routines coalesce into one synthetic
    `Unassigned` bucket in `sessions_by_muscle`, matching `session_summary.py:90`.
  - New pytest coverage for criteria 1–8 across the full `counting_mode` ×
    `contribution_mode` matrix: empty-string and `None` routines; frequency
    thresholds above and below `1.0`; multiple anonymous rows accumulating into
    one bucket; mixed named/anonymous routines.
  - Route-JSON assertions for `frequency`, `avg_sets_per_session` and
    `max_sets_per_session` (**D3**).
  - One reviewed, intentional regeneration of
    `tests/goldens/weekly_summary_golden.json`, plus rewriting the golden test's
    docstring and inline comment that currently assert the drop-from-frequency
    behavior as intentional.
  - Export pytest coverage for the changed workbook figures (**D2**).
  - An `e2e/summary-pages.spec.ts` assertion on the rendered "Routines" column
    (criterion 10).
  - Migration notes in the PR description.

- **Out** (this iteration)
  - `weekly_summary.py:244` — `global_sessions` keeps excluding the synthetic
    bucket (**D1**, owner-signed). Not touched, not "cleaned up".
  - `_build_weekly_summary_output` — already correct for a populated
    `muscle_sessions`; the fix is upstream.
  - `calculate_pattern_coverage()` / `_tally_patterns` — keeps keying falsy
    routines as `''` (criterion 11); the golden locks it and it is **not**
    unified in this packet.
  - `utils/session_summary.py`, `utils/fatigue_data.py`, `utils/export_service.py`
    — no production edits; the export family is a *test* gate, not a code change.
  - Any UI change: no new column, no relabelling, no `Unassigned` row in the
    weekly table, no surface added to display avg/max per session.
  - Weekly raw/effective totals, reps, volume, status, `volume_class`,
    contribution weights, rounding, and the response field list (criterion 7).
  - The `docs/REFACTOR_PLAN.md:1601` stale-status row — separate docs-only PR.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `utils/weekly_summary.py` | modify | The **only** production file. Two sites: the `routine` binding (`:70`) and the `if routine:` guard (`:139-140`). `:244` stays byte-identical per **D1**. |
| `tests/test_weekly_summary.py` | modify | Criteria 1–8 across all four `counting_mode` × `contribution_mode` combinations, including a criterion-7 invariance assertion that totals/status/`volume_class` are unchanged. |
| `tests/test_weekly_summary_routes.py` | modify | **D3** route-JSON assertions: `frequency`, `avg_sets_per_session`, `max_sets_per_session` on `/weekly_summary`. |
| `tests/test_weekly_summary_golden.py` | modify | Rewrite the docstring bullet at ~lines 21–26 ("This golden LOCKS that drop-from-frequency behavior; it must NOT be 'fixed' into a WPB.4 `Unassigned` bucket here") and the inline seed comment at ~line 130 ("volume but no frequency (M2/OD4)"). Left as-is, the file contradicts the golden it ships with. Seed data itself is unchanged. |
| `tests/goldens/weekly_summary_golden.json` | modify (regenerate **once**) | `Calves` sentinel only: 4 fields × 4 modes = 16 changed values. A `Forearms` row in the diff means Option B was implemented — reject (**D1**). |
| `tests/test_exports.py` | modify | **D2**. The only test file touching the export path (`utils/export_service.py:174-181,317,382,443` splats every stat field into the "Weekly Summary" sheet). Update any fixed expectations and pin the new figures. |
| `e2e/summary-pages.spec.ts` | modify | Criterion 10: "Routines" column reads `1` for an anonymous-only muscle. Needs spec-local seeding — the functional E2E DB is user-state-wiped (`e2e/scripts/prepare_e2e_db.py`), so today `weekly_summary` renders empty and the existing assertions are all `length > 0`-guarded. See risk R2. |
| `docs/DUPLICATION_REGISTRY.md` | modify | Row 4 records OD4/WPB.4 as frozen pending this decision; it should record the resolution. **Flagged: not named in Section 0's In-scope list** — confirm or cut at Gate 1. |
| PR description | new | Migration notes: intentional semantic change to a protected calculation; the four affected fields; the one-bucket assumption; the **D1** resolution and rationale; the reviewed golden diff; the changed exported workbook figures. |
| `utils/session_summary.py`, `utils/fatigue_data.py`, `utils/export_service.py`, `static/js/modules/weekly-summary.js`, `templates/**` | **not touched** | Listed explicitly so the diff review can assert an empty change set here. |

**Effort**: **M** for implementation (2 production lines; the weight is in test
coverage, the golden review and the E2E seeding) · plan-stage size is **Large**
under [QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md#plan-stage-routing), which
is why both gates apply · **Owner**: implementation agent in a dedicated
worktree; the human owner signs Gate 1 · **Depends on**: Gate 0 ✅ (2026-08-01);
Gate 1 (open); WP2.3 goldens ✅ (`3696fdc`); **a green `main`** — `main` is
currently RED (2 failures in `tests/test_trailing_slash_routing.py`, fix pending
in **PR #234**), and implementation must not start from a red base or the golden
review inherits an unrelated failure signal.

**Sequence**

1. **Do not start on red.** Confirm PR #234 has merged and `main` is green
   (`/run-tests`, full suite) before branching. Record the green baseline under
   the gitignored `artifacts/` (ADR-002), never the repository root.
2. Create a **dedicated worktree** via `/worktree` (isolated SQLite DB). All
   implementation happens there, never in the shared `main` checkout.
3. **Tests first.** Add the criteria 1–8 matrix coverage to
   `tests/test_weekly_summary.py` and watch it fail against unmodified
   production code. A test that passes before step 4 is not testing the change.
4. Apply the two-site edit in `_aggregate_weekly_volumes`. Confirm by diff that
   `weekly_summary.py:244` and `_build_weekly_summary_output` are untouched.
5. Run `tests/test_weekly_summary.py` + `tests/test_weekly_summary_routes.py`
   (add the **D3** route-JSON assertions here). Every pre-existing non-golden
   test must still pass unchanged — if one needs editing, that is a scope-freeze
   violation, so stop and report rather than adjust the expectation.
6. **Read the golden diff before regenerating.** Run
   `tests/test_weekly_summary_golden.py` *without* `GENERATE_GOLDEN` and capture
   the failure diff (or dump the candidate JSON from a read-only scratch harness
   under `artifacts/` and diff it against the committed golden). Check it against
   the Section 0 worked example: `Calves` `frequency` 0→1; effective
   `sets_per_session` 0.85→5.1; raw 1.0→6.0; `avg`/`max` 0.0/0.0→5.1/5.1, all
   four modes; totals, `status`, `volume_class` and pattern coverage unchanged.
   **Tripwire:** any `Forearms` row, any other muscle, or any 17th changed field
   means the wrong option was implemented — stop, do not regenerate, report.
7. Regenerate **exactly once**:
   `$env:GENERATE_GOLDEN=1; .venv/Scripts/python.exe -m pytest tests/test_weekly_summary_golden.py -q`,
   then **clear `GENERATE_GOLDEN`** and re-run to confirm it passes as an
   equality test. Leaving the variable set turns every later run into a silent
   re-baseline. Attach the reviewed diff to the PR.
8. Update the golden test's docstring (~21–26) and inline seed comment (~130) to
   describe the `Unassigned` bucket as the intended behavior, keeping the M2/OD4
   scenario labels so the coverage map stays readable.
9. **D2 export gate**: run `tests/test_exports.py`; update the affected
   expectations and add an assertion that pins the changed "Weekly Summary"
   figures, so the workbook change is asserted rather than incidental.
10. **E2E seeding spike (do before writing the assertion).** Verify that an
    anonymous-routine row can be created against the E2E server — `/add_exercise`
    passes `data.get('routine')` straight through (`routes/workout_plan.py:101,111`)
    with no observed non-empty validation, but this is unverified. Preferred:
    spec-local seed via `page.request`, torn down in the test. Fallback if the
    API rejects it: name the alternative in Plan v2 rather than editing
    `prepare_e2e_db.py`, whose seed is shared with `empty-states.spec.ts` and the
    visual baselines (risk R2).
11. Add the criterion-10 assertion to `e2e/summary-pages.spec.ts` and run
    `/run-e2e summary-pages.spec.ts`. **One Playwright run at a time on this
    machine** — `playwright.config.ts:67` pins port 5000, so no parallel run and
    no other agent's E2E may overlap.
12. **Visual**: check whether `e2e/fixtures/database.visual.seed.db` contains any
    falsy-routine rows. Expectation is **zero pixel change** on the weekly-summary
    screenshots. If pixels do move, that is an intentional re-baseline of *both*
    `linux/` and `win32/` baseline sets and needs owner sign-off — it is not a
    blanket `--update-snapshots`.
13. Run the full gate (`/verify-suite`) in the worktree, then
    `product-risk-reviewer` (**mandatory before merge**, QUALITY_GATE business-logic
    row: `weekly_summary` touched), then `/unslop` or `/verify-and-polish`.
14. Open the PR with the migration notes and the reviewed golden diff. Update
    `docs/DUPLICATION_REGISTRY.md` row 4 if that artifact is confirmed at Gate 1.

**Expected gates** *(draft — `test-strategist` confirms or extends at council
step 2)*

- **pytest** (required): `tests/test_weekly_summary.py`,
  `tests/test_weekly_summary_routes.py`, `tests/test_weekly_summary_golden.py`,
  `tests/test_exports.py` (**D2**), plus the full suite before merge.
- **e2e** (required): `e2e/summary-pages.spec.ts` functional.
- **e2e** (visual): weekly-summary screenshots in `visual.spec.ts` — deep-gate /
  manual only and never a required PR check, so it is a *reviewed expectation of
  no change*, not a blocking status check.
- **other**: reviewed intentional golden diff, checked against the Section 0
  expectation **before** regeneration (step 6 tripwire); `product-risk-reviewer`
  before merge; PR migration notes. No `/build-css` — no SCSS is touched.

**Risks and tripwires**

- **R1 — golden regenerated to make a red test green.** Mitigation: step 6
  strictly precedes step 7; the diff is reviewed against a pre-written
  expectation, and a `Forearms` row is an explicit reject signal (**D1**).
- **R2 — the criterion-10 E2E assertion has nowhere to stand.** The functional
  E2E DB wipes all plan rows, so the weekly table is empty by default and every
  existing assertion is guarded. Spec-local seeding is preferred; changing the
  shared seed would ripple into `empty-states.spec.ts` and the visual baselines.
- **R3 — `GENERATE_GOLDEN` left set** in a shell turns later runs into silent
  re-baselines. Step 7 clears it and re-runs as an equality check.
- **R4 — scope creep into `_tally_patterns` or `fatigue_data.py`.** Both use a
  different falsy-routine convention and both are frozen here. The seam narrows
  from three conventions to two on purpose; unifying the third needs its own
  goldens and the calibration freeze.
- **R5 — port-5000 contention.** Only one Playwright run at a time on this
  machine; a concurrent E2E run in another worktree will fail confusingly.

**Open items for the council**

- Is `docs/DUPLICATION_REGISTRY.md` row 4 in this PR or a follow-up? It is not in
  Section 0's In-scope list.
- Confirm the E2E seeding approach in step 10, or name a better one.
- Confirm the export assertion shape in step 9 (pin exact figures vs. assert the
  field is present and consistent with the route JSON).

---

## Agent provenance

*Required for every council run. The manager records each agent ID returned by
its `Agent(...)` call and supplies the `product-manager` its own ID back, because
an agent cannot know its own ID. The `product-manager` stamps the IDs the manager
supplies — **never invent an ID**, never rerun completed council work to
manufacture continuity, and record an unrecoverable ID as an evidence gap.*

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `a7d99db0dc548baa1` | Author of Section 0 and Plan v1. |
| `product-manager` — response matrix + Plan v2 | `a7d99db0dc548baa1` | Same agent, resumed. Author of the response matrix and Plan v2. |
| `architecture-reviewer` | `a5a63ebf61a4dfa32` | Step 2 reviewer. |
| `test-strategist` | `ae4943fedbcfe1e27` | Step 2 reviewer. |
| `product-risk-reviewer` | `a73ad39d0ec819678` | Step 2 reviewer. |

**Same product-manager resumed for the matrix + Plan v2?** **`yes`** — resumed via
`SendMessage` to the Plan v1 agent `a7d99db0dc548baa1`. Both IDs above were
supplied by the manager from its own `Agent(...)` records; none was inferred or
invented by this agent.

**Evidence gap** — fill in only when continuity cannot be established; otherwise
write `none`:
> `none`. All five IDs were recorded by the manager at dispatch and supplied back
> verbatim. The three reviewer outputs were read directly from the council
> scratchpad and are reproduced verbatim below, so no finding reaches the matrix
> through a relay. No council step was rerun.

---

## Reviewer findings

*Council step 2, run 2026-08-01 — three reviewers in parallel. Pasted verbatim
from the council scratchpad, which is session-temporary; this document is the
durable copy. The only alteration is that each file's own H1 title line is
replaced by the section heading below, which carries the same agent ID.*

### architecture-reviewer (agent `a5a63ebf61a4dfa32`)

## Findings — WPB.4 Plan v1

### Blocking

**B1. Plan §Sequence step 10 + Artifacts row `e2e/summary-pages.spec.ts` — the E2E seeding premise is factually wrong; no HTTP path can create a falsy routine.**

The plan states (PLANNING.md:452-455) that `/add_exercise` passes routine through "with no observed non-empty validation, but this is unverified." The validation exists, one layer down:

- `utils/exercise_manager.py:36` — `if not all([routine, exercise, sets, min_rep_range, max_rep_range]) or weight is None or weight == "": ... return "Error: Missing required fields."` — `routine=''` is rejected, and `routes/workout_plan.py:110-119` delegates straight to it, returning 400 `VALIDATION_ERROR`.
- `routes/workout_plan.py:398` — `valid_fields = {'sets', 'min_rep_range', 'max_rep_range', 'rir', 'rpe', 'weight'}`. `routine` is not updatable, so add-then-blank is also closed.
- `e2e/scripts/prepare_e2e_db.py:45-59` wipes `user_selection` on every run.

  Risk: acceptance criterion 10 and the required `e2e/summary-pages.spec.ts` gate item have no legal seeding path at all; the "preferred" approach is provably dead and the plan's own R2 forbids the only remaining one. This surfaces mid-implementation, after the golden has been regenerated.
  Fix: at Gate 1 either drop criterion 10 from the E2E gate and assert `frequency` at the route-JSON layer, or explicitly authorize the shared-seed change and accept the ripple into `empty-states.spec.ts` plus both `linux/` and `win32/` visual baseline sets.

**B2. Artifacts row `tests/test_weekly_summary_routes.py` — D3 assertions placed there either assert a mock or hit the live DB.**

- `tests/test_weekly_summary_routes.py:14-20` defines a module-local `app` fixture (bare `Flask(__name__)`, registers only `weekly_summary_bp`) that **shadows** the conftest fixture. `utils.config.DB_FILE` is patched only at `tests/conftest.py:68-72`.
- Every endpoint test in that file patches `routes.weekly_summary.calculate_weekly_summary` (`:97`, `:118`, `:140`, and 15 more).

  Risk: a D3 assertion written in that file's idiom validates the dict-mapping at `routes/weekly_summary.py:68-71` against a mock return value — it passes identically before and after the two-line edit, so D3 buys zero regression protection. An unmocked test added there instead calls `DatabaseHandler()` against the developer's live `data/database.db`.
  Fix: name a DB-backed venue for the D3 assertions that uses the shared conftest `client` fixture, and correct the artifacts table.

**B3. Criteria 1-2 seeding conflicts with the named test file's only idiom, and criterion 2 is unreachable through the DB.**

- `tests/test_weekly_summary.py:3-9,21-49` seeds exclusively via `save_exercise` + `add_exercise` — the same `exercise_manager.py:36` guard from B1. Criterion 1 (`routine=''`) cannot be seeded in that file's existing style.
- `utils/db_initializer.py:186` — `routine TEXT NOT NULL`. Criterion 2 (`None`) cannot be inserted at all; it is reachable only by calling the private `_aggregate_weekly_volumes(rows, contribution_mode)` with synthetic dicts, or by patching `db.fetch_all`.

  Risk: the implementing agent improvises. The most available improvisation — relaxing the `exercise_manager.py:36` guard so a blank routine can be seeded — is a silent scope-freeze violation on a different protected path (that guard is OD1's shipped behavior).
  Fix: artifacts table names direct `INSERT INTO user_selection` for `''` (the working pattern is `tests/test_weekly_summary_golden.py:87-95` `_add_sel`) and a direct `_aggregate_weekly_volumes` unit call for `None`.

### Non-blocking

**N1. D2 export gate is vacuous as scoped.** `tests/test_exports.py` contains zero references to `weekly_summary`, `Weekly Summary`, or `frequency`; its 40+ tests cover filenames, streaming, memory, `exercise_order` preservation and error paths. The artifacts note "Update any fixed expectations and pin the new figures" mischaracterizes the file — there are no affected expectations, so an unchanged green run satisfies D2 without asserting anything.
  Fix: state that D2 is net-new coverage of the `Weekly Summary` sheet built at `utils/export_service.py:315-321`, and that a green unchanged `test_exports.py` does not discharge it.

**N2. Artifacts list omits four of the five `docs/REFACTOR_PLAN.md` status locations.** The plan defers only `:1601`. Also stale on merge: `:38` ("WPB.4 remains unimplemented and product-risk gated"), `:425` ("remains prerequisite-gated (needs WP2.3 golden fixtures)" — already stale), `:1573`, `:1574` ("Gated / not started").
  Fix: name `docs/REFACTOR_PLAN.md` as a modify artifact covering all five rows, or scope the deferred docs-only PR to all five explicitly rather than to `:1601` alone.

**N3. `docs/MASTER_HANDOVER.md` is unnamed but is the canonical current-state doc and a never-claimed shared path** (`docs/ai_workflow/WORKSTREAM_OWNERSHIP.md:33`; root CLAUDE.md §5). It carries live "WPB.4 remains gated/unimplemented" statements at `:1188`, `:1206`, `:1231`, `:1245`.
  Fix: add a MASTER_HANDOVER entry to the artifacts table with the per-edit coordination declaration, or state explicitly that it is deliberately excluded.

**N4. `docs/DUPLICATION_REGISTRY.md` row 4 needs more than a status flip.** The plan's self-flag is correct — and the row is also wrong on the facts: `:35` says "weekly silently **drops** falsy rows from frequency (`weekly_summary.py:244`)", but the drop is the `if routine:` guard at `utils/weekly_summary.py:139`; `:244` is `global_sessions`. The row also labels the decision "OD13" where the rest of the repo says OD4, and currently reads "**DO NOT CHANGE** … Off-limits per handover".
  Fix: update row 4 in this PR (not a follow-up) including the `:139` citation correction, since leaving "DO NOT CHANGE" in place actively misdirects the next agent.

**N5. The `Unassigned` label already denotes a different concept in this codebase, making criterion 8 a false tripwire.** `scripts/fatigue_stage1_cleanup.py:26` (`UNASSIGNED = 'Unassigned'`) writes `exercises.primary_muscle_group = 'Unassigned'`, and `tests/test_fatigue.py:529` / `tests/test_fatigue_routes.py:96` lock it as its own **muscle** bucket. Since `utils/weekly_summary.py:104-106` accumulates any truthy muscle string, a weekly-summary **muscle row** keyed `Unassigned` can already exist today, independent of WPB.4. There is no numeric collision — `sessions_by_muscle[muscle][routine]` keeps the two at different nesting levels — but criterion 8's "never a new muscle row in the output" will read as a violation to a reviewer diffing against a real DB.
  Fix: restate criterion 8 as "no muscle key is added or removed relative to the pre-change run on the same DB", and note the pre-existing homonym in the migration notes.

### Confirmed sound (do not re-derive)

- **Module boundary**: write set is `utils/weekly_summary.py` only; that module imports solely from `utils` (`:7-16`), and no `from routes.X` appears. No `utils/__init__.py` re-export is proposed — and `tests/test_utils_package.py:28` would catch one.
- **Registration triples**: correctly absent. No blueprint, no table, no schema change; `user_selection` already exists at `utils/db_initializer.py:184`. Nothing is owed to `app.py` or `tests/conftest.py`.
- **Response contract genuinely preserved**: `routes/weekly_summary.py:57-78` builds a fixed key list and `:99` returns through `success_response()`. The change moves values of `frequency` / `sets_per_session` / `avg_sets_per_session` / `max_sets_per_session` only — no key added or removed, no new error path, no ad-hoc `{"success": …}` shape.
- **Consumer inventory is complete for behavior.** `routes/weekly_summary.py:50` and `utils/export_service.py:317,382,443` are the only production consumers. The two test references the plan does not list are both inert: `tests/test_error_page_contract.py:23` patches it to raise (error-page contract), and `tests/test_utils_package.py:28` asserts it is *not* re-exported from `utils/__init__`.
- **JS consumer assumption verified**: `static/js/modules/weekly-summary.js:211,221` is the only JS reader of `frequency`, and nothing under `static/js` reads `avg_sets_per_session` or `max_sets_per_session`. D3's split is correct.

**Blocking issues** — B1, B2 and B3 must be resolved before Gate 1.

### test-strategist (agent `ae4943fedbcfe1e27`)

## Required gates

```
## Required gates
- pytest (targeted, local):
    tests/test_weekly_summary.py
    tests/test_weekly_summary_golden.py
    tests/test_exports.py
    tests/test_downstream_normalization.py::test_weekly_summary_uses_canonical_muscles
  (tests/test_weekly_summary_routes.py is NOT a meaningful gate here — see B2)
- pytest (merge gate): full `pytest tests/` — the CI job is `test` /
  "Run Tests" (.github/workflows/ci.yml:438-463), which runs the whole suite;
  there is no per-file required check.
- e2e:  e2e/summary-pages.spec.ts — required via the fan-in context
        "E2E Functional (Chromium)" (ci.yml:232, :261). Per-shard contexts are
        NOT required.
- other: product-risk-reviewer (QUALITY_GATE.md:28, business-logic row names
         weekly_summary); reviewed intentional golden diff; PR migration notes.
- NOT required: /build-css (no scss/**, QUALITY_GATE.md:31);
         visual.spec.ts as a status check (deep-gate only, e2e/CLAUDE.md
         "Visual spec contract").
```

## Verdict

**Cannot sign Gate 1 as drafted.** The gate *selection* in Plan v1 is correct and matches `docs/ai_workflow/QUALITY_GATE.md`. What fails is **discharge**: three of the four named gates (criterion-10 E2E, D3 route-JSON, D2 export) are, as specified, either impossible to execute or guaranteed green regardless of whether the change works. Plan v2 must respecify them.

---

## Blocking findings

### B1 — The criterion-10 E2E assertion has no achievable seeding path. The plan's "preferred" approach is refuted by code the plan flagged as unverified.

`docs/wpb4_unassigned_bucket/PLANNING.md:451-454` says `/add_exercise` "passes `data.get('routine')` straight through … with no observed non-empty validation, but this is unverified."

It is now verified, and it is false. `utils/exercise_manager.py:36`:

```python
if not all([routine, exercise, sets, min_rep_range, max_rep_range]) or weight is None or weight == "":
    return "Error: Missing required fields."
```

A falsy `routine` is rejected before the INSERT; `routes/workout_plan.py:121-130` maps that string to `VALIDATION_ERROR` / HTTP 400. `page.request.post('/add_exercise', {routine: ''})` returns 400.

Every fallback vector is also closed:
- `routes/workout_plan.py:398` — `/update_exercise` `valid_fields = {'sets','min_rep_range','max_rep_range','rir','rpe','weight'}`; `routine` is not updatable.
- `utils/program_backup.py:467-537` — restore replays rows captured from `user_selection` itself; it cannot introduce a routine value the DB never had.
- `package.json:16-26` — no Node sqlite driver (`@playwright/test`, `sass`, `stylelint`, `typescript`, `vitest`, `jsdom`), and `engines.node >= 18` predates `node:sqlite`. A spec-local direct DB write is not available without shelling out to Python.

So sequence step 11 (`PLANNING.md:458-461`) cannot be executed as written, and step 10's "fallback … name the alternative in Plan v2" is not a contingency — it is the only branch. **Plan v2 must name a concrete mechanism, verified, before Gate 1.**

**B1a — the obvious workaround is a test that proves nothing.** If the spec instead stubs `/weekly_summary` via `page.route()`, it exercises only `static/js/modules/weekly-summary.js:211` (`const routines = row.frequency || 0`) rendering into `:221` (`<td data-label="Routines">`). That JS is untouched by this packet and the assertion passes identically against unmodified production code. Plan v2 must explicitly forbid a mocked criterion-10 E2E.

**Framing for the council:** no `templates/**` or `static/js/**` file is in the write set, so `QUALITY_GATE.md` does **not** derive any E2E for this change. The criterion-10 E2E is required by the WPB.4 risk-mitigation gate (`docs/REFACTOR_PLAN.md:493-494`), not by QUALITY_GATE. Therefore dropping or substituting it is an **owner amendment to the risk-mitigation gate**, not something a test-strategist can waive. Surface it as a Gate-1 decision with a named substitute (my recommendation: a `tests/`-level integration assertion on the rendered payload plus a documented waiver, since the DOM path is one `||` away from the JSON that pytest can assert directly).

### B2 — D3 route-JSON assertions cannot live in `tests/test_weekly_summary_routes.py`. That file is 100% mock-isolated and would go green either way.

`PLANNING.md:395` assigns the D3 assertions to `tests/test_weekly_summary_routes.py`. That file:
- defines its own `app` fixture at `tests/test_weekly_summary_routes.py:14-20` — a bare `Flask(__name__)` + blueprint, which **shadows** the conftest `app`/`client` fixtures. There is no database in that module at all.
- patches `routes.weekly_summary.calculate_weekly_summary` in every endpoint test (lines 97, 118, 140, 158, 176, 193, 210, 227, 244, 292, 321, 352, 369, 387, 407, 424, 440).
- already asserts `frequency == 3`, `avg_sets_per_session == 4.2`, `max_sets_per_session == 6.0` at `:281-284` — from a hand-written mock dict at `:247-261`.

More assertions of that shape test the route's dict→list mapper (`routes/weekly_summary.py:68-71`), which this packet does not change. They pass before the change and after it. Independent corroboration in the repo's own scan: `docs/scan/PHASE_21.md:220`.

**Correct home:** `tests/test_downstream_normalization.py:84-90` is the existing precedent for a real `/weekly_summary` integration assertion using the shared conftest `client` against a real DB. Plan v2 should route D3 to a new integration class (in `tests/test_weekly_summary.py` using `client` + `clean_db`, or a new `tests/test_weekly_summary_integration.py`) that seeds a `routine=''` row and asserts `frequency` / `avg_sets_per_session` / `max_sets_per_session` on the JSON payload. Fix the Artifacts row at `PLANNING.md:395` accordingly.

### B3 — The D2 export gate is a null gate as scoped. There are no "affected expectations" to update, and no test asserts a single Weekly Summary cell.

Sequence step 9 (`PLANNING.md:447-449`) says "run `tests/test_exports.py`; update the affected expectations and add an assertion that pins the changed figures." The first half is a no-op:

- `rg "export_service|build_summary_sheets|fetch_all_sheets|collect_excel_sheets|stream_export_rows|_weekly_summary_to_rows" tests` → **no matches**. Nothing in `tests/` references the export service directly.
- `rg "weekly|frequency|sets_per_session|Weekly Summary" tests/test_exports.py` → **no matches**.
- `tests/test_exports.py:284-304` (`test_export_to_excel_structure`) asserts only `'Workout Plan' in sheet_names or len(sheet_names) >= 1`.
- `tests/test_exports.py:314-325` (`test_export_summary_with_method`) uses the `sample_workout_log` fixture at `:626-642`, which inserts **only `workout_log` rows and zero `user_selection` rows**. So `calculate_weekly_summary('Total')` returns `{}`, `utils/export_service.py:383` (`if weekly_data_raw:`) is false, and the "Weekly Summary" sheet is never created. The test asserts a filename.
- Neither export fixture seeds a falsy-routine row.

`tests/test_exports.py` is therefore green before and after the change, with or without the bug. D2 would be satisfied on paper by a gate that cannot fail. Plan v2 must convert step 9 from "update expectations" to "author new coverage": a fixture with a `routine=''` `user_selection` row, exercising `/export_summary` (or `build_summary_sheets('Total')` directly), loading the workbook via `openpyxl`, and pinning the four changed fields for the anonymous-only muscle.

### B4 — Criterion 2 (`None` routine) is unreachable through every seam the plan names, and the plan does not say where it will be tested.

- Schema is `routine TEXT NOT NULL` (stated in `PLANNING.md:31-33`; mirrored at `utils/program_backup.py:56`). A raw `None` INSERT fails the constraint.
- `tests/test_weekly_summary.py` seeds through `utils.exercise_manager.add_exercise`, blocked by `exercise_manager.py:36`.
- `tests/test_weekly_summary_golden.py::_add_sel` (`:87-95`) raw-INSERTs and would hit NOT NULL.

The only viable expression of criterion 2 is a **direct unit call** to the private `utils.weekly_summary._aggregate_weekly_volumes(rows, contribution_mode)` with hand-built row dicts. That helper has **no direct test anywhere today** (`rg _aggregate_weekly_volumes tests` → no hits). Same applies to criterion 3's literal wording, "several rows with **differing** falsy routine values" — at DB level the only reachable falsy is `''`, so the DB-level version of criterion 3 is "several anonymous rows, all `''`", and the "differing values" version is helper-level only.

`PLANNING.md:358-361` reads as if all of criteria 1–8 land in one DB-seeded place. Plan v2 must state the split: which criteria are asserted through `calculate_weekly_summary()` against a seeded DB, and which through `_aggregate_weekly_volumes()` directly — and accept that testing a private helper is a new (justified) coupling.

### B5 — Step 6's diff-capture method will not produce a reviewable diff, which is the entire R1 mitigation.

`PLANNING.md:430-438` orders it: run the golden test without `GENERATE_GOLDEN`, capture the failure diff; *or* (parenthetically) dump a candidate to `artifacts/` and diff.

The assertion is `assert fresh == expected` — a single equality over a deeply nested ~1000-line dict (`tests/test_weekly_summary_golden.py:315`). pytest's rewritten diff on nested dicts of that size is truncated and effectively unreadable, and `-q` suppresses more. The reviewer will not get a clean "16 fields on Calves" readout, which is precisely what the R1 tripwire and criterion 9 depend on.

The parenthetical is the only method that works, and it works well: the golden is written with `json.dumps(fresh, indent=2, sort_keys=True)` (`:307`), so it is line-oriented and stably ordered, and a plain text diff yields exactly the 16 changed lines. **Invert step 6:** make the `artifacts/` candidate-dump + text diff the primary procedure, and drop the pytest-failure-diff route. This also makes "attach the reviewed diff to the PR" (`:443`) trivially satisfiable.

I verified the "before" side of the expected delta against the checked-in golden — it is correct. `tests/goldens/weekly_summary_golden.json:508-524, 646-662, 818-834, 956-972`: `frequency: 0`, `avg/max_sets_per_session: 0.0`, `sets_per_session: 0.85` (effective modes) / `1.0` (raw modes), with `effective_weekly_sets: 5.1`, `raw_weekly_sets: 6.0`, `total_reps: 45.9`, `total_volume: 2295.0`, `status: low`, `volume_class: low-volume`. The 4 fields × 4 modes = 16 arithmetic is right, and the untouched `global_sessions` set is 6 named routines, so `Forearms` (`:543-548`, `frequency: 0`, `max_sets_per_session: 0.77`) is genuinely unaffected under Option A. The tripwire is well-designed; only its capture mechanism is wrong.

### B6 — R3 is understated. `GENERATE_GOLDEN` is a **shared** flag; leaving it set silently re-baselines the fatigue golden too.

`PLANNING.md:496-497` describes R3 as "later runs become silent re-baselines". The actual blast radius:

- `tests/test_weekly_summary_golden.py:304` — `if os.environ.get("GENERATE_GOLDEN") == "1":`
- `tests/test_fatigue_golden.py:515` — **same env var**, writing `tests/goldens/fatigue_golden.json`

If the variable survives into step 13's `/verify-suite` in the same PowerShell session, that run re-baselines a **second protected calculation zone** — one under an active calibration freeze — and both tests report `skipped` (`:309`, `:522`), so nothing goes red. Two goldens are destroyed and the suite is green.

Plan v2 must: (a) name the second victim explicitly, (b) give the literal clear command (`Remove-Item Env:GENERATE_GOLDEN` — `$env:X=''` also works since both tests compare `== "1"`, but say which), (c) note that the regeneration run's success signal is `1 skipped`, not `1 passed`, so the implementer does not read it as "didn't run", and (d) add a post-regeneration `git status` check that `tests/goldens/fatigue_golden.json` is unmodified.

---

## Non-blocking findings

**N1 — Missing case: a routine literally named `Unassigned`.** `row.get('routine') or 'Unassigned'` merges a real routine named `Unassigned` with the synthetic bucket. The collision is pre-existing in `utils/session_summary.py:90`, but weekly is *acquiring* it here. Not in criteria 1–11 and not in the six accepted assumptions (`PLANNING.md:206-240`). Recommend a seventh assumption ("a real routine named `Unassigned` merges with the synthetic bucket — accepted, matching session_summary") plus one test. It does not touch the golden.

**N2 — Criterion 7's "invariance assertion" is not implementable as phrased.** `PLANNING.md:394` promises "a criterion-7 invariance assertion that totals/status/`volume_class` are unchanged" inside `tests/test_weekly_summary.py`. Unchanged relative to what? Within one run there is no pre-change baseline. The golden *is* the invariance mechanism for the golden scenario (via the step-6 tripwire); the new matrix seeds have none. Implementable substitute: for each anonymous-routine scenario, assert that the seed's `weekly_sets` / `raw_weekly_sets` / `total_reps` / `total_volume` / `status` / `volume_class` are **identical whether the row's routine is `''` or a named string** — a genuine invariance property expressible in a single run. Say which of these Plan v2 means.

**N3 — Export assertion shape (open council item, step 9).** Recommend **pin exact figures**, not field-presence. `utils/export_service.py:174-181` splats `**stats`, so a presence check passes whatever the numbers are and cannot catch a silent denominator regression. Additionally assert workbook cells == route JSON for the same seed. The seed is small and hand-computable, so the cost is low.

**N4 — `docs/DUPLICATION_REGISTRY.md` row 4 (open council item): put it in this PR.** `docs/DUPLICATION_REGISTRY.md:35` currently reads "**DO NOT CHANGE.** Owner-gated (OD13/WPB.4 …)" and "WP2.3 golden LOCKED **no** 'Unassigned' bucket for weekly". Merging without updating it leaves the registry actively instructing the next agent not to touch something already changed — the same class of stale-lock as the golden test docstring the plan already scopes in (`PLANNING.md:396`). It is docs-only under `docs/**`, which `QUALITY_GATE.md:35` gates at "none", so it adds zero test surface. While there: row 4 cites `weekly_summary.py:244` as the drop site; the drop is at `:139`.

**N5 — Step 12's visual pre-check is answerable from source now.** `e2e/scripts/build_visual_seed.py:111-133` (`_insert_plan_and_logs`) does `DELETE FROM user_selection` then inserts every row with the module-level constant `ROUTINE` — a single named routine. On the generator's evidence the visual seed contains no falsy-routine rows, so weekly-summary screenshots cannot move. I could not open the committed binary `e2e/fixtures/database.visual.seed.db` to confirm the artifact matches its generator. Plan v2 should cite `build_visual_seed.py:111-133` as the "zero pixel change" evidence and keep re-baselining as a contingency only.

**N6 — If step 12 is executed, two run-conditions must be honored or the result is misread.** Per `docs/ai_workflow/QUALITY_GATE.md:39`: run with `PW_VISUAL_SEED=1` (without it, 36 of 66 visual tests fail on page-height for data reasons on unmodified CSS), and the Windows matrix carries one inherited red (`workout-plan-desktop-dark`, animated-logo band) that must never be resolved with `--update-snapshots`.

**N7 — Known-red posture: clean for this packet's spec set.** Per `QUALITY_GATE.md:89-94`, the only current entry is `e2e/program-backup.spec.ts:79` (DB-pollution flake, isolated into its own CI job), which is not in scope; `nav-dropdown.spec.ts` is explicitly **no longer** a known red (`:94`) and is also not in scope. Conclusion to record in Plan v2: **`e2e/summary-pages.spec.ts` carries no documented known-red**, so any red there is real and blocks.

**N8 — Conftest / fixture work: none.** No new blueprint and no new table, so neither the `QUALITY_GATE.md:26` blueprint-registration clause nor the `tests/CLAUDE.md` "New table?" clause fires. New matrix tests should reuse the existing `clean_db` / `db_handler` fixtures, as `tests/test_weekly_summary.py:12,97,143,183` and `tests/test_weekly_summary_golden.py:293-294` already do. Do not add fixtures.

**N9 — Blast radius independently confirmed; two gate-scope conclusions follow.** Repo-wide, the only consumers of `frequency` / `avg_sets_per_session` / `max_sets_per_session` are `routes/weekly_summary.py:68-71` and `utils/export_service.py` (via the `**stats` splat). No fatigue, progression, or volume-progress consumer. Therefore: (a) `tests/test_session_summary*.py` is correctly **out** of the required set — `utils/session_summary.py:9` imports only `EFFECTIVE_STATUS_MAP`, which is untouched; (b) `e2e/api-integration.spec.ts:587-604` asserts only payload shape (`Array.isArray`, `toHaveProperty`) and cannot serve as criterion-10 coverage, though it runs anyway inside the required shard set.

**N10 — Visual-gate reconciliation is correct; say so in the PR.** `PLANNING.md:480-482` demotes visual to "a reviewed expectation of no change, not a blocking status check". That deliberately diverges from `docs/REFACTOR_PLAN.md:493-494` ("run summary-page functional **and visual** gates") and is right: per `e2e/CLAUDE.md` "Visual spec contract", visual specs run only via `deep-gate.yml`'s `visual-linux` job, `workflow_dispatch`-only, and are never a required check. *(**The cited claim was corrected 2026-08-29.** `visual.spec.ts` runs in `ci.yml`'s `visual-windows` job on every PR, and `visual-linux` also runs on a weekly `schedule`. The **conclusion** this note draws is unaffected — neither job is a **required** branch-protection context, so the visual gate still is not a blocking status check.)* State the reconciliation explicitly in the PR so a reviewer does not read the risk-mitigation gate as unmet.

**N11 — Name the required E2E context by its exact string.** `PLANNING.md:479` says "e2e (required): `e2e/summary-pages.spec.ts` functional". The branch-protection context is `E2E Functional (Chromium)` (`.github/workflows/ci.yml:261`), a fan-in gate over `E2E Functional Shard 1/2` and `2/2` (`:167`), which are **not** required. A new assertion that reds `summary-pages` reds that single context and blocks merge.

**N12 — Red-`main` precondition.** `PLANNING.md:410-412` records `main` as RED (2 failures in `tests/test_trailing_slash_routing.py`, fix pending in PR #234) and step 1 handles it. I did not run tests and cannot confirm the current state. Flagging only that the step-6 "zero unexplained diff" tripwire depends on a green base, and the step-1 baseline capture under `artifacts/` should be the exact artifact the golden diff is read against.

---

## Verified-correct (no action)

- Every `utils/weekly_summary.py` line reference in the plan is accurate: `:70` routine binding, `:139-140` the `if routine:` guard, `:174` the `len(global_sessions)` fallback, `:192-193` effective-derived avg/max, `:244` the `global_sessions` comprehension.
- The write set really is two lines in one function, and D1 (Option A) really does leave `:244` and `_build_weekly_summary_output` untouched.
- The `'Calves'` ⊅ `'calf'` quirk is real (`utils/weekly_summary.py:376`), so pattern coverage is unaffected and criterion 11 holds.
- The four-mode delta arithmetic (16 fields) and the pre-change golden values check out (see B5).
- `static/js/modules/weekly-summary.js:207-222` does render exactly Muscle Group / Effective Sets / Raw Sets / **Routines** / Total Volume / Volume Classification — the assumption at `PLANNING.md:234-240` is correct, and avg/max genuinely are not on the page.

### product-risk-reviewer (agent `a73ad39d0ec819678`)

## What I independently verified (not taken from the plan)

Re-derived the worked example from `tests/goldens/weekly_summary_golden.json` and `utils/weekly_summary.py` rather than trusting the "measured" table:

- Golden `Calves` before-values are exactly as claimed in all four modes: `frequency 0`, `sets_per_session` 0.85 (effective) / 1.0 (raw), `avg`/`max` 0.0/0.0, `effective_weekly_sets` 5.1, `raw_weekly_sets` 6.0, `total_reps` 45.9, `total_volume` 2295.0, `status` low, `volume_class` low-volume (golden lines 508-524, 646-662, 818-834, 956-972).
- After-values follow by construction: bucket holds 5.1 → clears `>= 1.0` at `weekly_summary.py:171` → `frequency 1` → `session_count = 1` at `:174` → 5.1 (effective) / 6.0 (raw); `avg = 5.1/1` at `:192`; `max = max({'Unassigned': 5.1})` at `:193`. 4 fields × 4 modes = 16 values. Correct.
- **Criterion 7 (totals bit-identical) holds by construction, not by hope.** The local `routine` binding at `weekly_summary.py:70` is read at exactly one place — `:139-140`. It feeds no total, no rep, no volume, no rounding, no classification. Nothing else in `_aggregate_weekly_volumes` touches it.
- **D1 (Option A) is correct and its evidence is complete.** `global_sessions` at `weekly_summary.py:244` reads `rows` directly, not the local binding, so leaving it untouched is coherent. The golden has exactly **two** zero-frequency muscles — `Calves` and `Forearms` — so the Option A/B table is exhaustive, not a sample. Option B's Forearms numbers check out arithmetically (0.77/7 = 0.11; 2.0/7 = 0.29). The `Forearms` tripwire in step 6 is a genuinely load-bearing reject signal.
- Consumers are complete: `calculate_weekly_summary` is called only from `routes/weekly_summary.py:50` and `utils/export_service.py:317,382,443`. The route does emit `avg_sets_per_session` / `max_sets_per_session` (`routes/weekly_summary.py:70-71`), so D3 is at least *shaped* right.
- **Local-first and non-goals: clean.** No auth, no accounts, no remote endpoint, no telemetry, no cloud sync, no schema change.
- **"Effective sets are informational only" (`utils/effective_sets.py:6-7`): respected.** The `>= 1.0` effective-set threshold already gates named-routine frequency at `weekly_summary.py:171`; applying it symmetrically to the synthetic bucket introduces no new gate, blocks no input, and auto-adjusts nothing. Assumption 3 in Section 0 is the right call.
- **Fatigue freeze respected.** `routes/weekly_summary.py:91` calls `compute_weekly_fatigue()` independently; `utils/fatigue_data.py` imports nothing from `weekly_summary`. No Stage-4 calibration surface moves.

---

## Blocking

**B1. Section 0 criterion 10 / Plan v1 "Out" — the "Routines" column will count something that is not a Routine.**
- Invariant at risk: `CLAUDE.md` §1 "Key terminology" — **Routine** = "Named exercise group, e.g. `GYM - Full Body - Workout A`". A bucket for rows with *no* name is by definition not a Routine.
- Risk: after this change a user reads "Routines: 1" for Calves on `/weekly_summary` (`static/js/modules/weekly-summary.js:221`), then goes to `/workout_plan` and finds no such routine in the tab strip. Criterion 10 plus the E2E assertion **enshrine the mislabel in a test**. Section 0's assumption list told the owner the *label* `Unassigned` stays invisible; it never said the integer under a column headed "Routines" would start counting a non-routine. That question was not squarely put at Gate 0.
- Fix: add a **D4** at Gate 1 — either accept explicitly that "Routines" counts unnamed sessions (and say so in the migration notes), or change the header/`data-label` string in `weekly-summary.js:221` to "Sessions", which matches `calculate_weekly_summary`'s own docstring at `weekly_summary.py:229` ("Number of **sessions** where muscle got >= 1.0 effective sets").

**B2. Owner decision D2 / Artifacts row `tests/test_exports.py` — the export test family does not exist.**
- Invariant at risk: `CLAUDE.md` §1 "Refactor invariant" — updated test coverage for a behavior change.
- Risk: **no test under `tests/` imports `utils/export_service.py`, and `tests/test_exports.py` contains zero references to weekly summary** — it tests `utils/export_utils.py` (filename sanitization, streaming thresholds, workbook creation). The only export-path coverage anywhere is `tests/test_ui_flows.py:321-338`, a 200 + content-type smoke. The plan's "update any fixed expectations and pin the new figures" and step 9's "update the affected expectations" describe work with no existing basis. The owner signed D2 believing a family existed to extend. This also breaks the **Effort: M** estimate — writing `build_summary_sheets` coverage from zero is new infrastructure, not a test edit.
- Fix: restate the D2 artifact as *new* test coverage for `utils/export_service.build_summary_sheets` / `_weekly_summary_to_rows` (`export_service.py:174-181`), and re-put D2 to the owner with the true cost.

**B3. Owner decision D3 — the route-JSON assertion cannot assert the changed values as specified.**
- Invariant at risk: `CLAUDE.md` §1 "Refactor invariant" (coverage must actually enshrine the new behavior).
- Risk: **every route test in `tests/test_weekly_summary_routes.py` patches `routes.weekly_summary.calculate_weekly_summary`** (decorators at lines 97, 118, 140, 158, 176, 193, …). An `avg_sets_per_session` / `max_sets_per_session` assertion added there asserts a hand-written mock dict — it proves pass-through, not the corrected number. D3 is the owner-signed mechanism for the two fields that are *not* rendered anywhere; as written, that mechanism gates nothing.
- Fix: state in Plan v2 that value-correctness for avg/max is owned by the golden plus the criteria 1–8 unit matrix, and that the route layer proves *field presence* only — or require an unmocked, seeded route test. Shape is `test-strategist`'s call; the decision-premise correction is what Gate 1 needs.

**B4. Section 0 "Problem" and Plan v1 step 10 — a falsy routine is not creatable through any product write path.**
- Invariant at risk: honesty of the user-visible problem statement; `CLAUDE.md` §1 "Core workflows" (Plan owns routine creation).
- Risk: step 10 says "`/add_exercise` passes `data.get('routine')` straight through (`routes/workout_plan.py:101,111`) with no observed non-empty validation." The validation is one layer down and it rejects:

  ```python
  # utils/exercise_manager.py:36
  if not all([routine, exercise, sets, min_rep_range, max_rep_range]) or weight is None or weight == "":
      logger.warning("Rejecting add_exercise due to missing fields")
      return "Error: Missing required fields."
  ```

  `''` is falsy → 400 `VALIDATION_ERROR`. No route sets or updates `routine` (`UPDATE user_selection` appears only for `exercise`, `exercise_order`, `superset_group`), and `utils/plan_generator.py` always names routines. The only in-app producer of an empty-routine row is a **program-backup restore**, which inserts snapshot rows verbatim (`utils/program_backup.py:467+`); otherwise it is legacy data or direct DB editing. Consequences: (a) step 10's preferred `page.request` seeding **will fail**, so the fallback is the actual path, not the contingency; (b) the Problem statement reads as a live defect when it is a legacy/restored-data defect; (c) criterion 10's E2E asserts a state the product itself cannot create.
- Fix: correct step 10's premise, restate the Problem as affecting legacy/restored/externally-edited rows, and resolve the E2E seeding path in Plan v2 before Gate 1 rather than after.

---

## Non-blocking

**N1. Plan v1 "Goal" overstates the per-session fix.**
- Risk: "its per-session figures stop being divided by unrelated routines" is true only when the bucket clears 1.0. Under **D1**, a below-threshold anonymous-only muscle keeps `sets_per_session = weekly_sets / len(global_sessions)` (`weekly_summary.py:174`) — still diluted by named routines it never appeared in — while its `max_sets_per_session` jumps from 0.0 to the bucket value.
- Fix: bound the Goal sentence to the `>= 1.0` case and note the residual dilution as a known, D1-accepted asymmetry.

**N2. Section 0 criterion 5 under-specifies the below-threshold case.**
- Risk: `weekly_summary.py:193` computes `max_sets_per_session` from `muscle_sessions` with **no threshold**, so a sub-1.0 anonymous bucket changes `max_sets_per_session` from `0.0` to the bucket value even though `frequency` stays `0`. Criterion 5 mentions only `frequency`, so a below-threshold matrix test could pass while leaving that delta unasserted.
- Fix: extend criterion 5 to state that `max_sets_per_session` becomes the bucket value while `frequency` stays 0, and pin it in the matrix.

**N3. Section 0 assumption 2 — `Unassigned` can collide with a real routine of that name.**
- Risk: criterion 3's absolute ("never more than one anonymous session") holds, but its converse fails — a routine literally named `Unassigned` merges with the synthetic bucket, under-counting `frequency` by 1 and reporting a summed `max_sets_per_session`. Not reachable through the Plan cascade, which composes the name from three fixed dropdowns (`templates/workout_plan.html:147-204`), but reachable via restore/legacy — the same population as B4. `utils/session_summary.py:90` already carries the identical collision.
- Fix: one line in the migration notes recording the collision as accepted and inherited from `session_summary.py:90`.

**N4. Plan v1 Artifacts / "Open items" — two canonical docs still declare this seam frozen.**
- Risk: `docs/DUPLICATION_REGISTRY.md:35` row 4 reads "**DO NOT CHANGE.** Owner-gated (OD13/WPB.4 …). Off-limits per handover", and `docs/REFACTOR_PLAN.md:1601` reads "WPB.4 and remaining Workout Plan/Log cleanup stay paused." The plan defers row 4 to a Gate 1 confirm and line 1601 to a separate docs-only PR. If WPB.4 merges first, the repository ships a change two governance documents forbid, and an implementation agent reading either file mid-packet has grounds to abort. The Gate 0 sign-off is real explicit go-ahead — this is a doc-sync problem, not a consent problem.
- Fix: answer the council's first open item as **yes** — fold both one-line status corrections into this PR.

**N5. Section 0 "Calculation surface" — provenance claims I cannot verify from the repository.**
- Risk: "This was **measured**, not projected: a read-only harness seeded the golden scenario and ran the current and candidate aggregations side by side" has no checked-in artifact (`artifacts/` is gitignored per ADR-002), so the harness cannot be confirmed. Same for "`main` is currently RED … fix pending in **PR #234**". **The conclusion survives** — I re-derived every number in the worked example and the Option A/B table independently and they are all correct — but the plan should not present unreproducible provenance as the warrant.
- Fix: drop the "measured by a harness" warrant in favor of the derivation from the committed golden plus `weekly_summary.py:171-193`, which any reviewer can reproduce.

**N6. Section 0 "Migration notes" — the backup/restore interaction is unstated.**
- Risk: no schema change, so existing `program_backup` snapshots stay restorable — that part is fine. But restore is the *primary* way empty-routine rows reach a live DB (`utils/program_backup.py:467+`), so restoring an older program will now produce different `frequency` / per-session numbers on `/weekly_summary` and in the exported workbook than it did before this packet.
- Fix: one line in the migration notes — snapshots remain restorable and byte-compatible; restored legacy rows with empty routines will now report one `Unassigned` session.

---

**Verdict: Needs revision.**

The calculation semantics are sound — the frequency change is correctly bounded, `sets_per_session` under D1 is coherent (with the N1 caveat), criterion 7 holds by construction, D1 is well-evidenced, and neither the local-first stance nor "effective sets are informational only" is touched. What needs fixing before Gate 1 is that **two of the three signed owner decisions rest on premises that are false in this repository** (B2, B3), the E2E/reachability story is wrong (B4), and the user-facing meaning of the "Routines" column changes without an owner decision (B1).

---

## Response matrix

*Every finding gets a row. Dispositions were synthesized by the manager at
council step 3 and are recorded here as **proposed**; the owner confirms them at
Gate 1. Where this `product-manager` disagrees or adds a caveat, it is stated
inline in the Action column rather than applied silently.*

| # | Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|---|
| **F1** | **No product write path can create a falsy routine.** `utils/exercise_manager.py:36` rejects `routine=''` → 400; `/update_exercise` cannot set `routine` (`routes/workout_plan.py:398`). Criterion 10's E2E has no legal seeding path, and a `page.route()` mock would pass against unmodified production code. | architecture B1; test-strategist B1 + B1a; product-risk B4 | **accept** → escalates to **D5** | Problem restated as a **legacy / restored / externally-edited data** defect (Plan v2 §Goal and §Problem restatement). A mocked criterion-10 E2E is **explicitly forbidden**. The seeding mechanism becomes owner decision **D5** with three named options — it is an amendment to the WPB.4 risk-mitigation gate (`docs/REFACTOR_PLAN.md:493-494`), not a strategist waiver. |
| **F2** | **D3's named venue is mock-isolated.** `tests/test_weekly_summary_routes.py:14-20` shadows the conftest fixture; all 17 endpoint tests patch `calculate_weekly_summary`, so assertions there are green before and after the change. | architecture B2; test-strategist B2; product-risk B3 | **accept** | D3 re-routed to a DB-backed venue: shared conftest `client` + `clean_db`, precedent `tests/test_downstream_normalization.py:84-90`. **D3's substance survives — only the venue changes, so no owner re-decision is needed.** Concur with the manager. The weaker alternative product-risk offered (route layer proves *presence* only) is **rejected** in favor of the DB-backed assertion, which can actually fail. |
| **F3** | **D2's export gate is vacuous.** Nothing under `tests/` imports `utils/export_service.py`; `tests/test_exports.py` has zero weekly-summary references and its fixture seeds no `user_selection` rows, so the "Weekly Summary" sheet is never built. Green regardless of the change. | architecture N1; test-strategist B3; product-risk B2 | **accept** → **D2 re-put** | Restated as **net-new** coverage of `build_summary_sheets` / `_weekly_summary_to_rows` with a `routine=''` fixture, an `openpyxl` load, and exact pinned figures cross-checked against the route JSON. **Effort revised M → L.** D2's true cost goes back to the owner. Correction to all three reviewers: the three call sites are in **three different functions** — `fetch_all_sheets:317`, `build_summary_sheets:382`, `stream_export_rows:443` — so Plan v2 names the sheet-building path precisely rather than "the export path". |
| **F4** | Criterion 1 (`''`) cannot be seeded in `tests/test_weekly_summary.py`'s `add_exercise` idiom; criterion 2 (`None`) is unreachable through the DB at all (`routine TEXT NOT NULL`). Risk: the implementer relaxes the `exercise_manager.py:36` guard — a scope-freeze violation on OD1's shipped behavior. | architecture B3; test-strategist B4 | **accept** | Plan v2 states the venue split explicitly: `''` via direct `INSERT INTO user_selection` (pattern `tests/test_weekly_summary_golden.py:87-95`); `None` and "differing falsy values" via a direct `_aggregate_weekly_volumes()` unit call. Touching the `exercise_manager.py:36` guard is named as a **stop-and-report** condition. The new private-helper coupling is accepted and justified in Plan v2. |
| **F5** | Step 6's golden-diff capture is inverted — `assert fresh == expected` over a ~1000-line nested dict truncates, defeating the R1 tripwire that criterion 9 depends on. | test-strategist B5 | **accept** | The `artifacts/` candidate dump + plain text diff becomes the **primary** procedure (the golden is written `json.dumps(indent=2, sort_keys=True)`, so a text diff yields exactly the 16 changed lines). The pytest-failure-diff route is dropped. |
| **F6** | **`GENERATE_GOLDEN` is shared with `tests/test_fatigue_golden.py:515`.** Leaving it set silently re-baselines `tests/goldens/fatigue_golden.json` — a second protected zone under an active calibration freeze — while both tests report `skipped`, so nothing reds. | test-strategist B6 | **accept** — highest-value cheap fix | All four sub-items land in Plan v2 step 8: name the second victim, give the literal `Remove-Item Env:GENERATE_GOLDEN`, state that the regeneration run's success signal is `1 skipped` (not `1 passed`), and add a post-regeneration `git status` check that `fatigue_golden.json` is unmodified. |
| **F7** | **The "Routines" column would count a non-Routine.** `CLAUDE.md` §1 defines Routine as a *named* group; the user reads "Routines: 1" then finds no such routine on `/workout_plan`. | product-risk B1 | **owner decision — D4** | Recorded unsigned under "Open Gate 1 decisions" with the manager's recommendation (**accept and document**) and its reason (renaming pulls `static/js` and both visual baseline sets into a packet that froze UI scope). Not decided here. Concur that this was not squarely put at Gate 0. |
| **F8** | Criterion 5 under-specifies: `max_sets_per_session` (`weekly_summary.py:193`) has **no threshold**, so a sub-1.0 bucket moves it `0.0 →` bucket value while `frequency` stays `0`. | product-risk N2 | **accept** | Pinned in the matrix as a distinct below-threshold case. Note this is an **amendment to Gate-0-signed criterion 5** — it strengthens, never weakens it, and stays inside criterion 7's four-field observable set. Listed under "Amendments to Gate-0-signed Section 0". |
| **F9** | Plan v1's Goal overstates: below-threshold anonymous-only muscles keep the diluted `sets_per_session = weekly_sets / len(global_sessions)`. | product-risk N1 | **accept** | Goal bounded to the `>= 1.0` case; the residual dilution is recorded as a known, D1-accepted asymmetry in Plan v2 §Goal and in the migration notes. |
| **F10** | A routine literally named `Unassigned` merges with the synthetic bucket, under-counting `frequency` by 1. Inherited from `utils/session_summary.py:90`. | test-strategist N1; product-risk N3 | **accept** | Added as a **7th assumption**, one matrix test, and a migration-note line. Does not touch the golden. Also an amendment to the Gate-0-signed assumption list — listed as such. |
| **F11** | `Unassigned` already denotes a **muscle** value (`scripts/fatigue_stage1_cleanup.py:26`), locked by `tests/test_fatigue.py:529`, so criterion 8's "never a new muscle row" is a false tripwire when diffing a real DB. | architecture N5 | **accept** | Criterion 8 restated for implementation as "no muscle key is added or removed **relative to the pre-change run on the same DB**"; the homonym goes in the migration notes. Amendment to Gate-0-signed criterion 8 — listed as such. |
| **F12** | `docs/DUPLICATION_REGISTRY.md:35` says "DO NOT CHANGE", miscites the drop site as `:244` (it is `:139`), and mislabels OD13 vs OD4. `docs/REFACTOR_PLAN.md` is stale in **five** places (`:38`, `:425`, `:1573`, `:1574`, `:1601`), not one. | architecture N2 + N4; test-strategist N4; product-risk N4 | **accept** — **with a caveat the owner must see** | Both files become artifacts of **this** PR (docs-only; `QUALITY_GATE.md` gates `docs/**` at "none"). **Caveat:** Section 0's owner-signed "Out of scope" says `docs/REFACTOR_PLAN.md:1601` "is being corrected in its own separate docs-only PR". Folding it in **reverses a Gate-0-signed exclusion**, so it needs owner acknowledgment at Gate 1 — or, equivalently, the separate docs PR must land first. Recorded under "Amendments to Gate-0-signed Section 0"; I am not treating a reviewer finding as authority to reverse a signed scope line. |
| **F13** | `docs/MASTER_HANDOVER.md` is unnamed but canonical, with live "WPB.4 gated/unimplemented" text at `:1188`, `:1206`, `:1231`, `:1245`. | architecture N3 | **accept** | Added to the artifacts table with the never-claimed-shared-path coordination declaration required by `docs/ai_workflow/WORKSTREAM_OWNERSHIP.md:33`. |
| **F14** | The "measured by a read-only harness" warrant is unreproducible (`artifacts/` is gitignored). The conclusion survives — product-risk re-derived every number independently. | product-risk N5 | **accept** | Plan v2 re-warrants the worked example from the committed golden (`tests/goldens/weekly_summary_golden.json:508-524, 646-662, 818-834, 956-972`) plus `weekly_summary.py:171-193`, which any reviewer can reproduce. **Section 0's wording is left untouched** — the correction is recorded as an amendment, not applied by editing a signed section. |
| **F15** | The backup/restore interaction is unstated, yet restore is the *primary* producer of empty-routine rows (`utils/program_backup.py:467+`). | product-risk N6 | **accept** | One migration-note line: snapshots stay restorable and byte-compatible; restored legacy rows with empty routines now report one `Unassigned` session and different per-session figures than before this packet. |
| **F16** | Export assertions must pin exact figures, not field presence — the `**stats` splat (`export_service.py:174-181`) passes any numbers. | test-strategist N3 | **accept** | Folded into F3's new coverage; closes the Plan v1 open item on assertion shape. |
| **F17** | The visual seed contains no falsy routines — `e2e/scripts/build_visual_seed.py:111-133` deletes `user_selection` then inserts every row with one named `ROUTINE` constant. | test-strategist N5 | **accept** | Cited as the "zero pixel change" evidence, replacing Plan v1's step-12 manual pre-check. Re-baselining stays a contingency requiring owner sign-off. Reviewer's caveat carried: the committed binary seed was not opened, only its generator. |
| **F18** | Visual is not a required check; the required context string is exactly `E2E Functional (Chromium)`; `PW_VISUAL_SEED=1` and the inherited `workout-plan-desktop-dark` red must be honored if visual is run. | test-strategist N6 + N10 + N11 | **accept** | Exact context string recorded in Plan v2 §Expected gates; the visual reconciliation against `docs/REFACTOR_PLAN.md:493-494` goes in the PR body so no reviewer reads the risk-mitigation gate as unmet. |
| **F19** | No conftest/fixture work is owed; `tests/test_session_summary*.py` is correctly out of the required set; `e2e/summary-pages.spec.ts` carries no documented known-red, so any red there is real. | test-strategist N7 + N8 + N9 | **accept — no action** | Recorded as confirmed in Plan v2 §Expected gates. Do **not** add fixtures; reuse `clean_db` / `db_handler`. |

**Dispositions: 19 of 19.** 16 accept, 1 accept-with-caveat (F12), 1 accept-and-escalate (F1 → D5), 1 owner decision (F7 → D4). Zero rejected, zero deferred. Three findings additionally change an owner-signed decision's premise (F1, F2, F3) — F2 alone is satisfiable without going back to the owner.

---

## Plan v2

*Supersedes Plan v1. Every change below traces to a finding ID in the matrix.*

**Goal**: A muscle whose work is recorded only in rows with **no routine name**
— legacy rows, restored program snapshots, or externally-edited databases — is
reported as one real session on `/weekly_summary` instead of zero, so its
"Routines" reads `1` and its `sets_per_session` is divided by that one session
rather than by every unrelated named routine in the plan. Bounded per **F9**:
this holds only when the bucket clears the `>= 1.0` effective-set threshold; a
below-threshold anonymous-only muscle keeps `frequency = 0` and the diluted
`len(global_sessions)` denominator (a D1-accepted asymmetry), while its
`max_sets_per_session` still moves off `0.0` (**F8**). All weekly totals,
statuses and classifications are unchanged.

**Problem restatement** (**F1**, replaces Plan v1's implicit framing; Section 0's
prose is left as signed)

This is **not** a live-workflow defect. No product write path can create a falsy
routine: `utils/exercise_manager.py:36` rejects `routine=''` with HTTP 400
`VALIDATION_ERROR`, `routes/workout_plan.py:398` excludes `routine` from the
updatable field set, and `utils/plan_generator.py` always names routines. The
affected population is **legacy rows, rows reinstated by a program-backup restore
(`utils/program_backup.py:467+`, which replays snapshot rows verbatim), and
externally-edited databases**. This reframing is what makes **D5** necessary: the
product cannot produce the state criterion 10 asks a browser to observe.

**Scope**

- **In**
  - `utils/weekly_summary._aggregate_weekly_volumes` only — the `routine` binding
    at `:70` and the `if routine:` guard at `:139-140`. Unchanged from v1.
  - Unit + integration coverage for criteria 1–8, **split by venue** (**F4**):
    DB-seeded via direct `INSERT INTO user_selection` for `''`; direct
    `_aggregate_weekly_volumes()` calls for `None` and for "differing falsy
    values"; both across the full `counting_mode` × `contribution_mode` matrix.
  - A **DB-backed** route-JSON assertion for `frequency` /
    `avg_sets_per_session` / `max_sets_per_session` (**D3** substance, **F2**
    venue).
  - **Net-new** export coverage of the "Weekly Summary" sheet (**D2** as
    re-scoped by **F3**/**F16**).
  - One reviewed, intentional regeneration of
    `tests/goldens/weekly_summary_golden.json`, plus the golden test's
    self-contradicting docstring and inline comment.
  - The three stale-governance doc corrections (**F12**, **F13**) — subject to
    the F12 caveat.
  - Migration notes covering: the intentional semantic change; the four affected
    fields; the one-bucket assumption; the D1 resolution; the `Unassigned`
    routine-name collision (**F10**); the `Unassigned` muscle-name homonym
    (**F11**); the restore interaction (**F15**); and the visual-gate
    reconciliation (**F18**).
  - Criterion 10's DOM assertion **only if D5 selects an option that provides
    one**.

- **Out** (unchanged from v1 unless noted)
  - `weekly_summary.py:244` — `global_sessions` still excludes the synthetic
    bucket (**D1**). Not touched.
  - `_build_weekly_summary_output`, `utils/session_summary.py`,
    `utils/fatigue_data.py`, `calculate_pattern_coverage()` / `_tally_patterns`.
  - `utils/export_service.py` — **test-only** work; no production edit.
  - **`utils/exercise_manager.py:36`** — newly named as out of scope (**F4**).
    Relaxing that guard to make seeding easier is a scope-freeze violation on
    OD1's shipped behavior and is a stop-and-report condition.
  - Any UI change, including the "Routines" header — **unless D4 selects the
    rename**, which would re-open `static/js` and both visual baseline sets.
  - A `page.route()`-mocked criterion-10 E2E — **explicitly forbidden** (**F1**).
    It exercises `static/js/modules/weekly-summary.js:211` only and passes
    against unmodified production code.
  - Weekly totals, reps, volume, status, `volume_class`, contribution weights,
    rounding, and the response field list.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `utils/weekly_summary.py` | modify | The **only** production file. Two sites: the `routine` binding (`:70`) and the `if routine:` guard (`:139-140`). `:244` stays byte-identical (**D1**). Criterion 7 holds *by construction* — product-risk verified the `:70` binding is read at exactly one place and feeds no total, rep, volume, rounding or classification. |
| `tests/test_weekly_summary.py` | modify | Criteria 1, 3–8 across all four mode combinations, seeded by **direct `INSERT INTO user_selection`** (pattern: `tests/test_weekly_summary_golden.py:87-95` `_add_sel`), **not** via `add_exercise` (**F4**). Includes the F8 below-threshold case (`frequency` stays 0, `max_sets_per_session` moves) and the F10 `Unassigned`-named-routine collision. Criterion 7 expressed as the implementable invariance of **F-N2**: for each scenario the totals/status/`volume_class` are identical whether the row's routine is `''` or a named string. Reuses `clean_db` / `db_handler`; no new fixtures (**F19**). |
| `tests/test_weekly_summary.py` (new integration class) **or** `tests/test_weekly_summary_integration.py` | new / modify | **D3's re-homed venue** (**F2**): shared conftest `client` + `clean_db`, seeded `routine=''` row, asserting `frequency` / `avg_sets_per_session` / `max_sets_per_session` on the real `/weekly_summary` JSON. Precedent: `tests/test_downstream_normalization.py:84-90`. Implementer picks the file; the requirement is a **DB-backed, unmocked** assertion. |
| `tests/test_weekly_summary.py` (helper-level cases) | modify | Criterion 2 (`None`) and criterion 3's "differing falsy values" via a **direct `_aggregate_weekly_volumes(rows, contribution_mode)` call** with hand-built row dicts — the only expression that exists, since the schema is `routine TEXT NOT NULL` (**F4**). Accepts new coupling to a private helper; justified in the PR body. |
| `tests/test_weekly_summary_routes.py` | **not modified** | **Reversal of Plan v1** (**F2**). The file is mock-isolated — a module-local `app` fixture at `:14-20` shadows conftest, and all 17 endpoint tests patch `calculate_weekly_summary`. Assertions added there would pass before and after the change. It stays in the suite as a regression check, not as a gate for this packet. |
| `tests/test_weekly_summary_golden.py` | modify | Rewrite the docstring bullet (~lines 21–26) and the inline seed comment (~line 130), both of which currently assert the drop-from-frequency behavior as intentional and instruct the reader **not** to introduce the `Unassigned` bucket. Seed data unchanged. |
| `tests/goldens/weekly_summary_golden.json` | modify (regenerate **once**) | `Calves` only: 4 fields × 4 modes = 16 values. Before-values independently confirmed by two reviewers at golden lines `508-524`, `646-662`, `818-834`, `956-972`. A `Forearms` row in the diff means Option B was implemented — reject (**D1**). |
| `tests/test_exports.py` (or a new `tests/test_export_service.py`) | **new coverage** | **D2 re-scoped** (**F3**). Nothing under `tests/` imports `utils/export_service.py` today and `tests/test_exports.py` has zero weekly-summary references, so an unchanged green run **does not discharge D2**. Required: a fixture with a `routine=''` `user_selection` row; exercise `build_summary_sheets('Total')` (`export_service.py:376`) or `/export_summary`; load with `openpyxl`; **pin exact figures** for the anonymous-only muscle and cross-check them against the route JSON for the same seed (**F16**). Note the three consumers are three distinct functions — `fetch_all_sheets:317`, `build_summary_sheets:382`, `stream_export_rows:443`. |
| `e2e/summary-pages.spec.ts` | **conditional on D5** | Criterion 10. No legal seeding path exists today (**F1**). Touched only under D5 option (b) or (c); untouched under option (a). A mocked assertion is forbidden. |
| `docs/DUPLICATION_REGISTRY.md` | modify | Row 4 (`:35`): remove "**DO NOT CHANGE** / Off-limits per handover", record the resolution, **correct the drop-site citation from `:244` to `:139`**, and fix the OD13/OD4 label (**F12**). Leaving it stale actively instructs the next agent not to touch what this PR changed. |
| `docs/REFACTOR_PLAN.md` | modify | **Five** stale locations, not one: `:38`, `:425`, `:1573`, `:1574`, `:1601` (**F12**). Subject to the F12 caveat — Section 0 signed `:1601` out to a separate PR. |
| `docs/MASTER_HANDOVER.md` | modify | Live "WPB.4 gated/unimplemented" text at `:1188`, `:1206`, `:1231`, `:1245` (**F13**). Never-claimed shared path — the per-edit coordination declaration in `docs/ai_workflow/WORKSTREAM_OWNERSHIP.md:33` applies. |
| PR description | new | Migration notes per §Scope. Plus the **F18** visual-gate reconciliation and the **F14** re-warrant (derive the worked example from the committed golden + `weekly_summary.py:171-193`, not from an unreproducible harness run). |
| `utils/session_summary.py`, `utils/fatigue_data.py`, `utils/export_service.py`, `utils/exercise_manager.py`, `static/js/**`, `templates/**` | **not touched** | Listed so the diff review can assert an empty change set here. `static/js` and `templates` move only if D4 selects the rename. |

**Effort**: **L** — revised up from M (**F3**). The production change is still two
lines; the export coverage must be written from zero against a service with no
existing test surface, the criteria split across two venues, and the doc
corrections span three governance files. · **Owner**: implementation agent in a
dedicated worktree; the human owner signs Gate 1 and D4/D5/D2-re-put. ·
**Depends on**: Gate 0 ✅ (2026-08-01); **Gate 1 + D4 + D5 + D2 re-put** (open);
WP2.3 goldens ✅ (`3696fdc`); **a green `main`** — RED at planning time (2
failures in `tests/test_trailing_slash_routing.py`, PR #234 pending); the
test-strategist could not confirm current state, and the step-6 tripwire depends
on a green base.

**Sequence**

1. **Do not start on red.** Confirm PR #234 merged and `main` green (`/run-tests`,
   full suite). Capture the baseline under the gitignored `artifacts/` (ADR-002);
   this exact artifact is what the golden diff is later read against (**F-N12**).
2. Create a **dedicated worktree** via `/worktree`. Never the shared `main`
   checkout.
3. **Tests first, split by venue** (**F4**): DB-seeded cases via direct
   `INSERT INTO user_selection`; `None` and differing-falsy cases via direct
   `_aggregate_weekly_volumes()` calls. All must fail against unmodified
   production code — a test that passes here is not testing the change. **If
   seeding tempts you to relax `utils/exercise_manager.py:36`, stop and report**;
   that guard is OD1's shipped behavior and out of scope.
4. Apply the two-site edit in `_aggregate_weekly_volumes`. Verify by diff that
   `:244` and `_build_weekly_summary_output` are untouched.
5. Add the **DB-backed** D3 integration assertion (**F2**) using conftest
   `client` + `clean_db`. Confirm it fails without the step-4 edit.
6. Run `tests/test_weekly_summary.py` and the new integration venue. Every
   pre-existing non-golden test must still pass **unmodified** — needing to edit
   one is a scope-freeze signal: stop and report rather than adjust it.
7. **Read the golden diff before regenerating** (**F5**, inverted from v1).
   Primary procedure: dump the candidate golden from a read-only scratch harness
   into `artifacts/`, then plain-text-diff it against the committed
   `tests/goldens/weekly_summary_golden.json`. The golden is written
   `json.dumps(..., indent=2, sort_keys=True)`, so the diff is line-oriented and
   yields exactly the 16 changed lines. Do **not** rely on the pytest assertion
   diff — it is one equality over a ~1000-line nested dict and truncates.
   **Tripwire:** any `Forearms` row, any other muscle, or any 17th changed field
   means the wrong option was implemented — stop, do not regenerate, report.
8. **Regenerate exactly once, then disarm the flag** (**F6**):
   - `$env:GENERATE_GOLDEN='1'; .venv/Scripts/python.exe -m pytest tests/test_weekly_summary_golden.py -q`
   - The success signal is **`1 skipped`, not `1 passed`** (`test_weekly_summary_golden.py:309`). Do not read `skipped` as "did not run".
   - **`Remove-Item Env:GENERATE_GOLDEN`** immediately. The flag is **shared with
     `tests/test_fatigue_golden.py:515`**; if it survives into the step-14
     `/verify-suite` in the same PowerShell session it silently re-baselines
     `tests/goldens/fatigue_golden.json` — a second protected zone under an
     active calibration freeze — and **both tests report `skipped`, so nothing
     goes red**.
   - Then `git status` and confirm `tests/goldens/fatigue_golden.json` is
     **unmodified**. Re-run the weekly golden test with the flag cleared to
     confirm it passes as an equality test. Attach the step-7 diff to the PR.
9. Update the golden test's docstring (~21–26) and inline seed comment (~130) to
   describe the `Unassigned` bucket as intended, keeping the M2/OD4 scenario
   labels so the coverage map stays readable.
10. **Author the export coverage from zero** (**F3**/**F16**): `routine=''`
    fixture → `build_summary_sheets('Total')` or `/export_summary` → `openpyxl`
    load → **exact pinned figures** for the anonymous-only muscle, cross-checked
    against the route JSON for the same seed. A green unchanged
    `tests/test_exports.py` does **not** discharge D2.
11. **Criterion 10 — execute only the option the owner selects at D5.** Under
    option (a) nothing is written here and `e2e/summary-pages.spec.ts` runs as a
    pure regression check. A mocked assertion is forbidden under every option.
12. Run `/run-e2e summary-pages.spec.ts`. **One Playwright run at a time on this
    machine** (`playwright.config.ts:67` pins port 5000). The spec carries **no
    documented known-red** (**F19**), so any red there is real and blocks.
13. **Visual**: no pre-check needed — `e2e/scripts/build_visual_seed.py:111-133`
    deletes `user_selection` and inserts every row with a single named `ROUTINE`
    constant, so the visual seed contains no falsy routines and weekly-summary
    screenshots cannot move (**F17**; the committed binary seed was not opened,
    only its generator). If visual is run anyway, use `PW_VISUAL_SEED=1` and
    leave the inherited `workout-plan-desktop-dark` red alone — never
    `--update-snapshots` (**F18**).
14. Full gate (`/verify-suite`) in the worktree — **after** confirming
    `GENERATE_GOLDEN` is cleared. Then `product-risk-reviewer` (mandatory before
    merge, `QUALITY_GATE.md:28` business-logic row names `weekly_summary`), then
    `/unslop` or `/verify-and-polish`.
15. Apply the three doc corrections (**F12**, **F13**) and open the PR with the
    migration notes and the reviewed golden diff.

**Expected gates** *(from `test-strategist` `ae4943fedbcfe1e27`, with the F2/F3
venue corrections applied)*

- **pytest (targeted, local)**: `tests/test_weekly_summary.py`; the new DB-backed
  D3 integration venue; the new export-service coverage;
  `tests/test_weekly_summary_golden.py`;
  `tests/test_downstream_normalization.py::test_weekly_summary_uses_canonical_muscles`.
- **pytest (merge gate)**: full `pytest tests/`. The CI job is `test` / "Run
  Tests" (`.github/workflows/ci.yml:438-463`) and runs the whole suite; there is
  **no per-file required check**.
- **Not a gate for this packet**: `tests/test_weekly_summary_routes.py` — green
  either way (**F2**). `tests/test_session_summary*.py` — `session_summary.py:9`
  imports only `EFFECTIVE_STATUS_MAP`, which is untouched (**F19**).
- **e2e**: `e2e/summary-pages.spec.ts`, required via the fan-in branch-protection
  context named exactly **`E2E Functional (Chromium)`** (`ci.yml:232,:261`).
  Per-shard contexts are **not** required. Under D5 option (a) this is a
  regression check, not a change-verifying gate — stated plainly so no one reads
  it as covering criterion 10.
- **Not required**: `/build-css` (no `scss/**`); `visual.spec.ts` as a status
  check — deep-gate / `workflow_dispatch` only, never a required context
  (**F18**).
- **Other**: `product-risk-reviewer` before merge; the reviewed intentional
  golden diff (step 7 artifact); PR migration notes.

**Risks and tripwires**

- **R1 — golden regenerated to make a red test green.** Step 7 strictly precedes
  step 8; the diff is text-based and read against a pre-written expectation; a
  `Forearms` row is an explicit reject signal (**D1**).
- **R2 — `GENERATE_GOLDEN` destroys the fatigue golden silently** (**F6**). Two
  protected zones, both reporting `skipped`, suite still green. Step 8's
  `Remove-Item` + `git status` check is the only barrier.
- **R3 — a gate that cannot fail.** Three of Plan v1's four gates were in this
  class. Every gate in Plan v2 must be demonstrated to fail without the step-4
  edit; steps 3 and 5 build that in.
- **R4 — improvised seeding relaxes `exercise_manager.py:36`** (**F4**). Named as
  a stop-and-report condition, not a judgment call.
- **R5 — scope creep into `_tally_patterns` or `fatigue_data.py`.** Both frozen;
  the seam narrows from three conventions to two on purpose.
- **R6 — port-5000 contention.** One Playwright run at a time on this machine.
- **R7 — merging while the governance docs still say "DO NOT CHANGE"** (**F12**).
  Mitigated by step 15, subject to the F12 caveat below.

**Amendments to Gate-0-signed Section 0** *(Section 0 itself is preserved
byte-for-byte; these are the deltas the council produced, listed so the owner can
acknowledge them at Gate 1 rather than discover them in the diff)*

| Signed text | Amendment | Source |
|---|---|---|
| **Problem** — reads as a live defect | Restated as a legacy / restored / externally-edited-data defect | F1 |
| **Criterion 5** — mentions `frequency` only | Also pins `max_sets_per_session` moving `0.0 →` bucket value while `frequency` stays `0` (strengthens, never weakens) | F8 |
| **Criterion 8** — "never a new muscle row in the output" | Restated as "no muscle key added or removed **relative to the pre-change run on the same DB**", because `Unassigned` is already a real muscle value | F11 |
| **Assumptions** (six, all accepted) | A **7th**: a routine literally named `Unassigned` merges with the synthetic bucket — accepted, inherited from `session_summary.py:90` | F10 |
| **Calculation surface** — "measured by a read-only harness" | Re-warranted from the committed golden + `weekly_summary.py:171-193` (reproducible); the conclusion is unchanged and was independently re-derived twice | F14 |
| **Out of scope** — "`docs/REFACTOR_PLAN.md:1601` … its own separate docs-only PR" | **Reversed**: folded into this PR along with four further stale locations. **This reverses a signed exclusion and needs explicit owner acknowledgment** — or the separate docs PR lands first | F12 |
| **D2** — "the export pytest family joins the required gate" | The family does not exist; restated as net-new coverage, Effort M → L | F3 |
| **D3** — "asserted at the route-JSON layer" | Venue changes to a DB-backed unmocked test; **substance unchanged**, no owner re-decision needed | F2 |

**Open Gate 1 decisions** *(surfaced by this council — **not decided here**)*

**D4 — Does the "Routines" column need renaming?** (**F7**, product-risk B1)
After this change that column counts a bucket with no name, while `CLAUDE.md` §1
defines Routine as a *named* exercise group. A user could read "Routines: 1" for
Calves and find no such routine on `/workout_plan`. Criterion 10 plus its E2E
would enshrine the mislabel in a test.
- **(a) Accept and document** — record in the migration notes that "Routines"
  counts unnamed sessions. **Manager's recommendation.** Reason: renaming pulls
  `static/js/modules/weekly-summary.js:221`, the template header and **both**
  visual baseline sets into a packet that explicitly froze UI scope.
- **(b) Rename to "Sessions"** — matches `calculate_weekly_summary`'s own
  docstring (`weekly_summary.py:229`, "Number of **sessions** where…"), but
  re-opens UI scope and the visual gate.
- *Unsigned. The owner decides.*

**D5 — Amend the risk-mitigation gate's E2E requirement, or authorize seeding?**
(**F1**) Criterion 10's E2E is required by `docs/REFACTOR_PLAN.md:493-494`, not
by `QUALITY_GATE.md` (no `templates/**` or `static/js/**` file is in the write
set, so QUALITY_GATE derives no E2E at all). Dropping or substituting it is
therefore an **owner amendment to that gate**, not something a reviewer can
waive.
- **(a) Drop the DOM assertion; assert at the route-JSON layer with a documented
  waiver.** `test-strategist`'s recommendation — the DOM path is one `||` away
  (`weekly-summary.js:211`) from JSON that pytest asserts directly. Cost:
  criterion 10 is never observed in a browser.
- **(b) Authorize a shared-seed change** in `e2e/scripts/prepare_e2e_db.py`.
  Cost: ripple into `empty-states.spec.ts` and **both** `linux/` and `win32/`
  visual baseline sets.
- **(c) Spec-local seeding by shelling out to Python** — *added by this
  `product-manager`, not by the council; flagged as such.* Playwright specs run
  in Node, and the repo already invokes `e2e/scripts/*.py` via
  `.venv/Scripts/python.exe`, so a spec could insert one `routine=''` row and
  delete exactly that row in teardown. This is the only option that both avoids
  the shared-seed ripple and gives a real DOM assertion. Cost and caveat: it
  mutates the shared E2E database mid-run (`fullyParallel: false`, one server,
  one DB), so teardown must delete precisely the seeded row or later specs
  inherit it. **Unverified** — no such spec-local Python invocation exists today;
  treat as a spike before committing to it.
- *Unsigned. The owner decides. A `page.route()` mock is forbidden under all
  three.*

**D2 re-put — confirm the true cost.** (**F3**) D2 was signed on the premise that
an export pytest family existed to extend. It does not: no test under `tests/`
imports `utils/export_service.py`, and `tests/test_exports.py` never references
weekly summary. Discharging D2 means authoring `build_summary_sheets` coverage
from zero, which is what moves this packet from **M to L**. Confirm D2 at the
true cost, or re-scope it.

---

## Sign-off

- [x] Gate 0 complete — signed by the owner 2026-08-01 (Section 0).
- [x] Every finding has a disposition — 19 of 19 (F1–F19), proposed by the
      manager at council step 3, recorded verbatim-faithful in the response
      matrix with this `product-manager`'s caveats stated inline.
- [x] Agent provenance complete — both `product-manager` IDs, same-PM-resumed
      `yes`, the three reviewer IDs, and evidence gap `none`.
- [x] **User approved Plan v2** — signed by the owner 2026-08-01, together with
      all 19 council dispositions, D4, D5 and the D2 re-put.
- [x] Ready to implement — `main` is green at `bb4858e`; implementation runs on
      branch `wt/wpb4-unassigned-bucket` in the dedicated worktree
      `D:/development/Hypertrophy-Toolbox-v3-wpb4`.

## GATE 1 ✅ APPROVED 2026-08-01 — owner decisions D4, D5, D2 re-put, F12

| # | Decision | Resolution |
|---|---|---|
| **D4** | Does the "Routines" column need renaming? | **Option (a) — accept and document.** Keep the "Routines" label; document in the migration notes that it includes the synthetic unnamed bucket. **Do not expand UI or visual-baseline scope.** `static/js/**` and `templates/**` stay out of the write set. |
| **D5** | Amend the risk-mitigation gate's E2E requirement, or authorize seeding? | **Option (a) — drop criterion 10's DOM assertion.** Replace it with the DB-backed, unmocked route-JSON assertion and document the waiver. `e2e/summary-pages.spec.ts` is **regression coverage only — run, not modified**. Explicitly rejected: any `page.route()` mock, any `e2e/scripts/prepare_e2e_db.py` shared-seed change, and the spec-local Python seeder (option c). |
| **D2 re-put** | Confirm the true cost | **Confirmed.** Revised **L** effort accepted. Author exact-value export coverage **from zero** against `build_summary_sheets('Total')` (`utils/export_service.py:376`), cross-checked against the route JSON for the same seed. |
| **F12** | Reversal of a Gate-0-signed scope exclusion | **Acknowledged and approved.** The Gate-0 "Out of scope" line assigning `docs/REFACTOR_PLAN.md:1601` to a separate docs-only PR is **reversed**. All identified `REFACTOR_PLAN.md` locations, the `DUPLICATION_REGISTRY.md` row-4 corrections, and the coordinated `MASTER_HANDOVER.md` corrections fold into **this** PR. |

**Consequences carried into implementation**

- Criterion 10 is **amended**: the observable moves from the rendered DOM to the
  `/weekly_summary` JSON payload, asserted by a DB-backed unmocked test. The
  waiver is recorded in the PR migration notes, since the DOM path is one `||`
  away (`static/js/modules/weekly-summary.js:211`) from the asserted JSON.
- The write set gains `docs/MASTER_HANDOVER.md`, `docs/DUPLICATION_REGISTRY.md`
  and `docs/REFACTOR_PLAN.md`; it does **not** gain `static/js/**`,
  `templates/**`, `e2e/**`, or `e2e/scripts/prepare_e2e_db.py`.
- `docs/test_inventory/TEST_INVENTORY.{json,md}` must be regenerated in this PR —
  the `Test Inventory Drift` job fails on any test add or removal.

> **Gate 1 is signed. Implementation is authorized** on branch
> `wt/wpb4-unassigned-bucket` only. Every constraint in Plan v2 remains binding —
> in particular the D1 `Forearms` tripwire, the one-shot reviewed golden
> regeneration, and the `GENERATE_GOLDEN` disarm protecting
> `tests/goldens/fatigue_golden.json`.

---

## ✅ EXECUTED AND CLOSED — 2026-08-01

**The authorization above was discharged.** WPB.4 merged as **PR #256, squash
`9fe5dbd`**, 18/18 checks green.

| | |
|---|---|
| Production change | `utils/weekly_summary.py` only — the two sites named in Plan v2 |
| Tests added | `tests/test_weekly_summary_unassigned.py`, `tests/test_export_weekly_summary_sheet.py` (D2 re-put, from zero) |
| Golden | `tests/goldens/weekly_summary_golden.json` regenerated **once**, `Calves` only — the D1 `Forearms` tripwire held |
| Docs folded in per F12 | `MASTER_HANDOVER.md`, `DUPLICATION_REGISTRY.md`, `REFACTOR_PLAN.md` |
| Write set | **D4 (a) / D5 (a) honoured** — no `static/js/**`, `templates/**`, or `e2e/**` |

**Nothing in this document remains to be done.** The Sequence, the write-set
table and every "must / apply / regenerate" instruction are a record of completed
work. Verified post-merge against `origin/main`; see the banner at the top of this
file for why re-executing step 8 would be actively harmful.
