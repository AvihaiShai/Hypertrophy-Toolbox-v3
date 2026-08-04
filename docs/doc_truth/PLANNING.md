# Plan Review — Documentation truth and compaction pass (LEFTOVERS P1.1)

**Source item:** [`LEFTOVERS_BY_PRIORITY.md`](../LEFTOVERS_BY_PRIORITY.md) row **P1.1**, deep-scan revision v23.

**Evidence snapshot:** 2026-08-04, `origin/main` @ **`db1bc5d`** (verified not advanced at execution time). Supersedes the original snapshot (`4e9b7d0` / `4a24773`, 2026-08-03), which predated **#291** (P1.4), **#293** (P2.6) and **#292** (P1.8+P1.3).

**Planning size:** Large / cross-cutting under [QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) — 13+ documents across two gate rows (`Product docs only` and `AI workflow / agent config`), so Gate 0 applies.

> **Anchor policy — this revision's main structural change.** The original brief
> addressed targets by `file:line`. Three merges have since moved those lines, and
> the brief itself already carried drifted pointers. **Every criterion below now
> cites a verbatim anchor string** — a heading or a quoted phrase — that can be
> re-found with `grep` regardless of line movement. Line numbers appear only as
> *observed at `db1bc5d`* conveniences and are never the addressing mechanism.

---

## Section 0 — Requirements Brief

**Raw request** (verbatim)

> regarding this item:
> P1.1 doc truth	~30%	#265/#270/#271 landed; named residue remains	Agent	2–4 h
>
> --
>
> create a goal to complete it

**Problem**

The repository's status-claiming documents disagree with the repository. A reader
who trusts them re-implements shipped work (WP2.6), waits on discharged gates
(WPB.4, Fatigue Stage 0), quotes test counts that no longer hold, or treats a
required CI context as optional.

---

## §0.1 — Rebase log: what three merges changed about this packet

| Merge | Effect on this packet |
|---|---|
| **#291** `ed14bb3` (P1.4 debug scaffolding) | No criterion target touched. |
| **#293** `592ab6b` (P2.6 LF normalization) | Rewrote the **P2.6 row** of `LEFTOVERS_BY_PRIORITY.md` and added `tests/test_css_audit_digest_normalization_contracts.py`, moving the generated inventory totals criterion 11 compares against. |
| **#292** `db1bc5d` (P1.8 + P1.3) | **Largest impact.** Added a multi-line blockquote to `ai_workflow/INDEX.md`'s Spine, shifting every line below it (`## Active feature plans` moved **11 → 21**). Reworded `QUALITY_GATE.md`'s identity line and two other phrases. Added goal-doc pointers to the **P1.3** and **P1.8** rows of `LEFTOVERS_BY_PRIORITY.md`. Added `tests/test_agent_workflow_contracts.py`, which **guards `docs/ai_workflow/` against any `Tier <digit>` or `Appendix A<digit>` string**. |

### Four premise corrections found while rebasing

**(a) Criterion 4's Linux premise expired.** The brief said the Linux baselines
were stale and produced "at least 11 failures". **#281** (`864043f`, merged
2026-08-03) regenerated and owner-accepted them, so that state no longer holds.
Re-derived instead: #281 changed 95 files but **did not update**
[`CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json`](../CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json),
whose `sourceCommit` is still `46e340e` and `revisedOn` still `2026-08-01`. That
ledger is the reconciliation baseline `QUALITY_GATE.md`'s `static/css/` row
names, so the *live* defect is no longer "the baselines are stale" — it is that
**the ledger predates the regeneration that replaced the baselines it describes**.

**(b) Criterion 14's inbound counts are inverted.** The brief claims
`CSS_PHASE4_WP4_3I_D/_E/_F` "each carry 6 inbound references" while `_B`, `_G`,
`_H` carry 0. Re-derived at `db1bc5d`, **every `WP4_3I_*` candidate carries 0
genuine inbound references**; the only hits are the P1.1 row of
`LEFTOVERS_BY_PRIORITY.md` listing them *as* orphan candidates, which is not an
index link. The 5–7 inbound counts belong to the **`WP4_4_*`** family
(`_D2_A11Y_`=5, `_E_LAYOUT_`=5, `_H_COMPONENTS_DEAD_`=7) — the pytest-pinned set
that Leftovers **N7** places explicitly out of scope. The brief conflated two
document families. The corrected reading matches what `LEFTOVERS_BY_PRIORITY.md`'s
own P3 bullet already says.

**(c) Criterion 9's shape is wrong.** `E2E_TESTING.md` does not carry
*per-spec counts*; its spec table is name → purpose with no numbers. It carries
exactly **one** hand-maintained aggregate — "There are currently **28**
Playwright spec files in `e2e/`" — against a generated truth of **31**. The
criterion still holds; its description of the defect does not.

**(d) Criterion 11's comparison numbers moved.** The brief compares against
"2100 collected nodes across 101 files". At `db1bc5d` the generated inventory
reports **2203 nodes across 105 deterministic files / 106 total**, Playwright
**589 across 31 specs**, required functional gate **474 across 25**, hard waits
**92**. Criterion 11's targets are also broader than the brief's four lines.

---

## §0.2 — Acceptance criteria, re-anchored

"Verified" means re-derived at execution time from git, `gh`, or a generated
inventory — never copied from this brief.

| # | File | Anchor (verbatim, grep-able) | Required end state |
|---|---|---|---|
| 1 | `DUPLICATION_REGISTRY.md` | heading `### ⚠️ Known stale rows — audited 2026-08-01, NOT yet corrected`; summary cell `DO NOT CHANGE (owner-gated behavior)` | Stale-rows block removed (its content is discharged); rows 3/11/14 pointers re-derived; row 14 states WP2.6 **shipped** via `utils/schema_registry.py` / `run_all_initializers()`; the summary/row-4 contradiction resolved |
| 2 | `ai_workflow/INDEX.md` | heading `## Active feature plans`; string `calibration window open 2026-05-24, earliest close 2026-06-07` | The four missing workstreams linked; the expired Fatigue window no longer advertised as open. **The Spine blockquote added by #292 is load-bearing and must survive in substance** — it is the anti-recreation control for the retired shared-plan tiers |
| 3 | `UI_SCENARIOS_GAP_ANALYSIS.md` | row prefixes `KI-003`, `KI-007` | KI-003 reflects resolution by the isolated required context; KI-007 states a re-derived status for `exercise_isolated_muscles` |
| 4 | `ai_workflow/QUALITY_GATE.md` | string `Windows matrix still carries one inherited red` | Visual-red state **links the single producer** rather than restating it, and records that the inherited-reds ledger predates #281's regeneration. **No `Tier <digit>` string may be introduced** — `tests/test_agent_workflow_contracts.py` reds on it |
| 5 | `fatigue_meter/PLANNING.md` | string `draft plan, awaiting human sign-off on Stage 0` | Status reflects Phase 1, Phase 2 Path 1 (#35) and the Stage 3 gate as shipped; Stage 4 state taken from `PHASE2_PLANNING.md`, not inferred |
| 6 | `REFACTOR_PLAN.md` | string `WPB.4 remains prerequisite-gated (needs WP2.3 golden fixtures)` | Marked historical **in place**; the same file's Track B row already records WPB.4 **Done** |
| 7 | `MASTER_HANDOVER.md` | string `Branch protection is now 10 required contexts` | Corrected to the verified count; every *current* test total links the generated inventory or is framed as dated per-packet evidence |
| 8 | `CHANGELOG.md` | heading `## Unreleased - July 29, 2026` | Extended with the August ships: #256, #262/#266, #248/#267, and #278, #280, #282, #283, #284, #285 |
| 9 | `E2E_TESTING.md` | string `There are currently **28** Playwright spec files` | The single hand-maintained count removed in favour of a link to `TEST_INVENTORY.md`; run commands and setup prose stay |
| 10 | `docs/README.md` | string `Current Playwright inventory and run commands` | No longer sells `E2E_TESTING.md` as the current inventory. The "punch list" wording on the LEFTOVERS line is already correct — **verify, do not re-edit** |
| 11 | `TESTING_STRATEGY_PLANNING.md` | strings `2,288 currently collected nodes`, `**1,994** across 92 files`, `**541** across 30 specs`, `**426** across 24 specs`, `**93** across 15 files` | Each is date-stamped as historical evidence or replaced with a link to the single producer |
| 12 | `ai_workflow/QUALITY_GATE.md` | string `it is not a required context, so the rename was free` | Corrected: branch protection returns **11** contexts including `Test Inventory Drift` (re-derived live). The `(non-required)` **job names stay byte-for-byte identical** |
| 13 | `LEFTOVERS_BY_PRIORITY.md` | strings `N1 — this plan is not reachable by anyone else`, `N9 — a duplicate of the orchestration plan is still loose` | P1.0 recorded done (#278 merged 2026-08-02); N1 marked historical; N9 re-checked. **The P1.3/P1.8 goal-doc pointers and #293's rewritten P2.6 row are preserved untouched** |
| 14 | orphan candidates | — | Written archive disposition using the **corrected** counts from §0.1(b). No file is moved |
| 15 | whole change | — | `git diff --name-only` shows `docs/` only — no `routes/`, `utils/`, `templates/`, `static/`, `scss/`, `tests/`, `e2e/` or `.github/` path |

**Calculation surface:** `none`. Several targets *describe* protected calculation
zones, but correcting a description is not a calculation change. **No file under
`utils/` is edited.** If any edit would require touching `utils/` to make a doc
true, that edit is out of scope and returns to the owner.

---

## §0.3 — Out of scope

- **Any archival move.** [`DOC_RETENTION.md`](../ai_workflow/DOC_RETENTION.md) requires *no meaningful edits for 6 months*; every candidate fails it. Dispositions are **written down**, not executed.
- **Moving the six pytest-pinned CSS evidence artifacts** (Leftovers **N7**) — moving one reds the required `Run Tests`.
- **Reopening any closed workstream.** P3 terminated at `a0`; WPB.4, WP2.6 and the app.py review are closed.
- **Renaming any CI job**, especially the two `(non-required)`-suffixed required contexts.
- **Regenerating `TEST_INVENTORY.json`/`.md`** — this packet adds no tests, so the artifacts must not move. Verified with `--check`, not rewritten.
- **Rewriting or compacting the #292 Spine blockquote in `INDEX.md`** — it is a control, not prose.
- The other P1 items and everything in P2/P3.

---

## §0.4 — Gate 0 sign-off

Gate 0 is signed by the owner's execution instruction, which directed this packet
to be rebased and then run through its gates and review. The five open questions
are resolved as follows; each is the brief's own recommendation except where noted.

| Q | Resolution | Basis |
|---|---|---|
| **Q1** — edit `LEFTOVERS_BY_PRIORITY.md` itself? | **Yes**, confined to P1.0 status plus N1/N9. No other row touched, nothing renumbered. | Brief's recommendation; owner named this file for careful reconciliation |
| **Q2** — gut or retire `E2E_TESTING.md`? | **Gut it**, keep run commands. | Criterion 9 already specifies gutting; deletion is the larger, less reversible option and was never the criterion |
| **Q3** — KI-003 wording | **"Resolved by CI isolation"**, with the historical flake retained in one clause. | Satisfies both readings; retaining context loses nothing |
| **Q4** — one PR or a series? | **One PR.** | Brief's recommendation; the change type requires no tests and no reviewers, so review cost is the only variable |
| **Q5** — drift found during execution | **Fix it when it lives in a file already being edited; otherwise record it.** | Brief's recommendation. Applied to §0.1(a), which lands in `QUALITY_GATE.md` — a file criterion 4 already opens |

---

## Plan v1

Single docs-only commit on `wt/doc-truth-p1-1`, cut from `db1bc5d`.

1. **Status corrections** — criteria 1, 3, 5, 6, 7, 12, 13.
2. **Single-producer cleanup** — criteria 9, 11, and the count half of 7.
3. **Index and disposition** — criteria 2, 8, 10, 14.
4. **Visual-red producer link** — criterion 4, including the §0.1(a) ledger-staleness note.

**Gates** (from the two change-type rows plus what this packet actually touches):

| Gate | Why | Required |
|---|---|---|
| `pytest tests/test_agent_workflow_contracts.py` | This packet edits `docs/ai_workflow/`, which #292's guard contracts cover. A stray retired-tier string reds it | yes |
| Full `pytest` | Cheap, and several tests assert doc artifacts | yes |
| `generate_test_inventory.py --check` | Must prove the artifacts did **not** move | yes |
| Docs-only path assertion | Criterion 15 | yes |
| Chromium E2E | No template, JS, CSS, route or util change | **no** |
| `code-reviewer` + `unslop-reviewer` | The `AI workflow / agent config` row names a reviewer; owner asked for independent review | yes |

**Definition of done:** criteria 1–15 observably met at the final tree, gates
green, review findings dispositioned, and one docs-only PR opened. The P1.1 row
is retired from `LEFTOVERS_BY_PRIORITY.md` only after that PR merges — per
[LEFTOVERS §6](../LEFTOVERS_BY_PRIORITY.md) item 1, not inside this packet.

---

## §5 — Execution record

Executed 2026-08-04 on `wt/doc-truth-p1-1` from `db1bc5d`. **13 documents changed,
docs-only.** Criteria 1–15 met.

### Gates

| Gate | Result |
|---|---|
| Docs-only path assertion (criterion 15) | **pass** — no non-`docs/` path in the diff |
| `pytest tests/test_agent_workflow_contracts.py` | **75 passed** — no retired-tier string introduced into `docs/ai_workflow/` |
| Full `pytest tests/` | **2523 passed, 2 skipped** — identical to the `db1bc5d` baseline |
| `generate_test_inventory.py --check` | **"Test inventory is up to date"** — the artifacts correctly did **not** move |
| Chromium E2E | not required; no template, JS, CSS, route or util change |

### Independent review — six factual defects found in this packet's own edits

An adversarial fact-check was run against the staged diff. It refuted four claims
this sweep had asserted, and a slop review found one case of the sweep committing
the exact defect it exists to remove. **All were verified independently before
correction** — none was accepted on the reviewer's word.

| # | Defect this sweep introduced | Correction |
|---|---|---|
| 1 | Registry row 14 claimed **all four** e2e scripts route through the schema registry. `build_visual_seed.py` does not — it copies the prebuilt fixture and still owns a raw `ALTER TABLE exercises ADD COLUMN media_path` (`:65-68`, called `:166`). | Row 14 now names the three real callers and records that ALTER as the one residual seam |
| 2 | The new registry preamble claimed **every** `file:line` was re-derived. Only rows 3/11/14 were. Row 13's `conftest.py:280` is a column dict (the INSERT is `:334`); row 9's `volume-splitter.js:179` is `slider.value = 0` (the catch is `:135-136`). | Preamble scoped to rows 3/11/14, with the two known-stale rows named |
| 3 | The orphan table claimed **zero** inbound refs for all eight candidates. `MASTER_HANDOVER.md:1144` cites the family in **shorthand** (`` `_B`/`_C`/`_D`/`_E`/`_F`/`_G` ``), which a whole-filename grep misses. Six are not orphans. | Counts corrected to 1; only `_H` and `WP3_5_FETCH_INVENTORY.md` are genuine candidates, and the shorthand trap is documented |
| 4 | Claimed the `WP4_4_*` **`.md`** files are pytest-pinned and moving one reds `Run Tests`. They appear only in docstrings and one assertion *message*; no test reads them. The real pins are the **JSON** siblings (`test_css_wp4_4_a_baseline_contracts.py:34`, `test_css_cascade_contracts.py:161`). | Corrected to name the JSON pins. Leftovers **N7** carries the same imprecision; recorded for the next audit rather than edited here, since Q1 confines this packet's LEFTOVERS edits to P1.0/N1/N9 |
| 5 | The CHANGELOG credited **#267** with adding `Test Inventory Drift` to branch protection. #267 touched only `ci.yml` and `QUALITY_GATE.md`; branch protection is API-side config that ships in no PR. | Split into the blocking flip (#267) and the separate protection change |
| 6 | The `TESTING_STRATEGY_PLANNING.md` "do not quote counts as current" note **transcribed five fresh counts** — precisely the rot this criterion removes. | Numbers cut; the note links the generated producer and nothing else |

Also fixed from the slop review: `docs/README.md`'s hand-maintained "Last updated:
2026-06-12" stamp, which this packet's own edit falsified; the LEFTOVERS
classification line still listing **P1.0** as READY after the row was marked done;
three specs (`erase-flow`, `listener-cleanup`, `visual-field-separator`) missing
from the `E2E_TESTING.md` table whose purpose this packet restated; and duplicated
statements of the 11-context fact, the `(non-required)` rule, and the fatigue
Stage-4 status across files.

### Deferred, recorded rather than fixed

- **Leftovers N7's pin attribution** — see defect 4. Out of the Q1-signed scope.
- **Registry rows 9 and 13 pointers** — named as stale in the preamble. Re-deriving
  every row is a larger pass than criterion 1 authorises.
- **The Linux inherited-reds ledger** predates #281's regeneration; `QUALITY_GATE.md`
  now warns against reconciling against it, but re-pinning it belongs to a packet
  that owns that file.

---

*Rebased 2026-08-04 against `origin/main` @ `db1bc5d`. Anchors are verbatim
strings verified at that commit; re-grep before acting.*
