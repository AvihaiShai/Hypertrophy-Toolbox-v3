# CSS `theme-dark.css` inertia arc — **P3-a0** audit evidence

*Packet **P3-a0** of the WP4.4 closeout proposal **P3**. Plan:
[`docs/css_theme_dark_p3/PLANNING.md`](css_theme_dark_p3/PLANNING.md). Naming per **Q4**
(flat `docs/CSS_THEME_DARK_P3_<PACKET>_EVIDENCE.md`).*

**Authority.** Gate 0 and Gate 1 were both signed by the owner on 2026-08-02, and execution
is authorized for **P3-a0 only**. `P3-a1` onward needs a separate dispatch decision. This
packet stops at its own boundary.

**Nature.** Read-only. **Zero deleted lines by construction.** It writes three paths and
nothing else:

| Path | What it is |
|---|---|
| `scripts/css_audit/p3_ceiling.py` | the P3-owned ceiling emitter |
| `tests/test_css_theme_dark_p3_audit_contracts.py` | contracts over this packet's own outputs |
| `docs/CSS_THEME_DARK_P3_A0_AUDIT_EVIDENCE.md` | this document |

**What this packet deliberately did NOT do**, each because the plan or the dispatch forbids it:

- No production CSS was written. `static/css/**` is byte-identical, **asserted** (§2).
- No existing apparatus was repaired. `scripts/css_audit/measure.py`,
  `measure.BLIND_SPOT_REGISTER`, `measure.CONTRACT_FILES` and
  `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` are untouched — that is P3-a1's question, and
  putting it here would rebuild the self-certification loop the a0/a1 split exists to break.
- The **N8 Linux deep gate was not dispatched**. The reconciliation in §8 is a desk exercise.
- The **Q1 `occurrences <= 1` → `== 1` repair was not performed.** The owner granted it
  unconditionally at Gate 0; that is scope approval, not authorization to do unrelated work
  during this dispatch. `tests/test_css_wp4_4_theme_dark_contracts.py` is unmodified. §6.4
  records the repair as available and proves, by execution, that it is still needed.
- No snapshot was regenerated; `--update-snapshots` was not run.
- `docs/MASTER_HANDOVER.md`, `docs/ACTIVE_DEVELOPMENT.md` and `docs/REFACTOR_PLAN.md` were
  **not** written. **D3 makes P3-e the sole writer.** This packet does not terminate the arc,
  so the D3 interim escalation rule is not triggered; §12 records what would need to change
  if the owner ends the arc here.

---

## 1. The arc base — measured, not inherited

The plan pins the arc base at `4b0670b` (P2 / PR #222). `main` has since advanced. Per
product-risk #6, this packet records **the SHA it actually measured** rather than inheriting
one.

| Item | Value |
|---|---|
| Branch | `wt/p3-a0-audit` |
| **Commit measured (HEAD at measurement)** | `2332242` — `docs(p3): narrow D3 to plain sole-writer, record the abandonment hole` |
| Merge base with `origin/main` | **`ac16e4c`** — `ci: correct the Test Inventory job summary to say blocking (#267 follow-up) (#271)` |
| Plan-pinned base | `4b0670b` — an ancestor of HEAD, verified |
| Base drift | **YES** — 22 commits between `4b0670b` and `ac16e4c` |

### The drift is real and, for every input this packet measures, immaterial

Verified rather than assumed:

| Input | `4b0670b` → `ac16e4c` |
|---|---|
| `static/css/**` | **no change at all** (`git diff --stat` empty) |
| `static/css/theme-dark.css` blob | `dffaa5824ed51b7c438092692286afb5685cf7f9` at `4b0670b`, at `ac16e4c` **and** in the working tree |
| `tests/test_css_wp4_4_theme_dark_contracts.py` | unchanged |
| `tests/test_css_cascade_contracts.py` | unchanged |
| `tests/test_css_wp4_4_a_baseline_contracts.py` | unchanged |
| `e2e/visual-helpers.ts` | unchanged |
| `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` | unchanged |
| `scripts/css_audit/**` | unchanged |
| `.github/workflows/deep-gate.yml` | **changed — 19 lines**, and it is one of the three N8 inputs |

The `deep-gate.yml` change is **only** `actions/checkout@v4→v7` (×7),
`actions/setup-python@v5→v7` (×7), `actions/upload-artifact@v4→v7` (×3),
`actions/setup-node@v4→v7` (×2). The `visual-linux` job's `if: inputs.run_visual` gate, its
`visual_mode` handling and its
`npx playwright test --project=chromium e2e/visual.spec.ts e2e/visual-baseline-thumbnails.spec.ts`
invocation are byte-identical. The N8 reconciliation in §8 is therefore unaffected by the
drift.

**Consequence for later packets:** the 14-row ceiling table and every file figure below hold
at `4b0670b` and at `ac16e4c` identically. P3-a1 may re-pin to `ac16e4c` without re-measuring
the CSS; it may **not** inherit the `deep-gate.yml` line numbers.

---

## 2. Gates — the P3-a0 column only

Derived from the **P3-a0** column of *Expected gates per packet — the v2 table*, and from
the `static/css/**` row of [`QUALITY_GATE.md`](ai_workflow/QUALITY_GATE.md).

| Gate | Required at a0 | Result |
|---|---|---|
| Full `pytest` (cascade contracts inside the total) | ✔ | **2,415 passed / 2 skipped** — see below |
| Seven-surface Stylelint | anchor only | **recorded as the arc anchor** — §3.3 |
| Production CSS diff empty | ✔ **asserted** | **empty**, asserted by contract |
| No snapshot regenerated | ✔ | `git status e2e/__screenshots__/` empty; the committed digest assertion (`a_baseline_contracts.py:234-255`) passed inside the full run |
| Required nine Chromium specs | — | **not run** |
| `visual.spec.ts` 66/platform | — | **not run** |
| `visual-baseline-thumbnails.spec.ts` 18/platform | — | **not run** |
| Linux N8 deep gate | — | **not dispatched** |
| N8 denominator reconciled (documentary) | ✔ **a0 produces it** | §8 |
| Whole-page computed differential | — | not applicable (no capture at a0) |

The four "not run" rows are not omissions. The plan is explicit: *"Read-only packets do not
run the E2E or visual gates. Nothing changed, so a pass would carry no information — and a
gate that cannot fail is worse than no gate."*

**One gate outside the a0 column was run anyway, and it caught something.** `ci.yml`'s
`Type Check` job runs `pyright baseline diff (blocking)`, which fails on **net-new**
diagnostics against `docs/ci_cd_phase3/pyright-baseline.json`. It is not in the plan's a0
column, but it is blocking on every PR and this packet adds two Python files. First run over
the two new files: **7 net-new errors**, all `dict[str, object]` indexing and `int()`
narrowing. Fixed; re-run is **0 errors, 0 warnings**. Invocation:

```
npx pyright@1.1.410 --pythonpath <main checkout>/.venv/Scripts/python.exe \
  scripts/css_audit/p3_ceiling.py tests/test_css_theme_dark_p3_audit_contracts.py
```

*(`--pythonpath` is needed because `pyrightconfig.json` pins `venv: ".venv"` and this worktree
has none — see §12.)*

### 2.1 Full pytest

```
D:/development/Hypertrophy-Toolbox-v3-main/.venv/Scripts/python.exe -m pytest tests/ -q
```

| Measurement | Value |
|---|---|
| Collected **without** this packet's contract file | **2,380** |
| Tests this packet adds | **37** |
| Total collected | **2,417** |
| Result | **2,415 passed, 2 skipped, 0 failed** |

The delta is exactly this packet's own file. No pre-existing test changed state. *(The
recorded run of 2,413 passed / 2 skipped was taken at 35 contract tests; two further red-path
contracts were added afterwards and the file re-ran green. The final full-suite figure above
is the one to cite.)*

### 2.2 Production CSS byte-identity — asserted, not assumed

`test_this_packet_wrote_no_production_css` runs `git status --porcelain -- static/css` plus
the staged and unstaged diffs, and fails if any is non-empty. It is **scoped to the working
tree rather than to a base SHA on purpose**: a base-SHA pin in a permanently-collected
per-packet file would red the moment P3-c makes its authorized cut, and no packet may be made
to weaken another packet's assertion in order to ship. Its red path builds a throwaway git
repository, dirties `static/css/theme-dark.css` in it, and shows the same function reports
`clean: False`.

`git status --porcelain` for the whole worktree at the end of this packet:

```
?? scripts/css_audit/p3_ceiling.py
?? tests/test_css_theme_dark_p3_audit_contracts.py
```

### 2.3 Stylelint invocation note

This worktree has **no `node_modules`** (the symlink that would have shared the main
checkout's failed). The anchor was measured by running the committed
`scripts/css_audit/stylelint_surfaces.mjs` logic verbatim from a scratchpad copy that
resolves the `stylelint` package from the main checkout by absolute path. Config, surface
list, and aggregation are identical; the main checkout was read and not written; output went
to the scratchpad only. **P3-a1 needs `npm ci` in its worktree** — this is a genuine
precondition, recorded in §12.

---

## 3. The file's own figures, re-measured with a tool

The plan flags all of these as counted **by reading** and explicitly un-inheritable. Every
figure below comes from `scripts/css_audit/p3_ceiling.py::measure_theme_dark()`.

### 3.1 Structure

| Figure | Measured | Plan's claim | Agrees |
|---|---|---|---|
| Lines | **574** | 574 | yes |
| Bytes on disk (CRLF) | **22,592** | — | — |
| Bytes newline-normalized (LF) | **22,018** | — | — |
| Line ending | **CRLF** | — | — |
| `sha256` of the bytes on disk | **`e54818bf790eb2c11474f68ecddc25d66304d9edf650cf698853276e419f2fca`** | — | — |
| Brace-opening blocks | **74** | 74 | yes |
| Top-level **style** rules | **72** | 72 | yes |
| Top-level at-rules | **1** | 1 (`@media`) | yes |
| Nested blocks | **1** | 1 | yes |
| Custom-property declarations | **34** | 34 | yes |
| — in `:where([data-theme="dark"])` `:2-22` | **16** | 16 | yes |
| — in `[data-theme="dark"]` `:550-574` | **18** | 18 | yes |
| `!important` declarations (comments excluded) | **124** | 124 | yes |
| `!important` lines | **125** | — | — |
| `!important` raw occurrences | **125** | — | — |
| `.value-changed` (comment-stripped) | **7** | 7 | yes |
| `@media` (comment-stripped) | **1** | 1 | yes |
| `:where(` tokens | **152** | — | — |
| Declares `@layer` | **no** | no | yes |
| Mentions `superset` | **no** | no | yes |

**Every one of the plan's six flagged figures is correct.** They were counted by reading and
they are right; they are now also mechanically reproducible.

Two figures the plan did not carry, both load-bearing for later packets:

- **The three `!important` units disagree by exactly one**, and the reason is the literal
  `Zero !important.` inside the comment at `:548`. This is already reconciled by
  `test_important_is_counted_in_reconcilable_units`.
- **`measure.surface_counts()`'s `bytes` figure is NOT the on-disk byte count.** It reads
  with `read_text()`, which normalizes CRLF to LF, so it reports **22,018** against the file's
  actual **22,592** — a difference of exactly 574, one CR per line. This is the *live* form of
  the offset hazard **O10** describes. Any P3-a1 tool that takes a postcss character offset
  and treats it as a byte offset into the on-disk file will cut in the wrong place, and the
  diff will still look plausible. The emitter reports both units side by side and flags the
  disagreement.

### 3.2 The F1 shadow — a nomination, emitted as one

Measured: **every one of the 16 names** declared in the `:where([data-theme="dark"])` block at
`:2-22` is redeclared in the unwrapped `[data-theme="dark"]` block at `:550-574`, which
additionally declares `--bs-body-bg` and `--bs-body-color`.

The emitter labels this `tokenBlockShadowNomination` and carries the warrant text inline:
**structural redeclaration is not deletion authority.** P-2 requires a `var()`-consumer
dependency graph *and* a removal-oracle result *and* a per-token split control. Nothing here
supplies any of the three.

### 3.3 Stylelint — the arc anchor

Anchored to **this arc's own base** (CSS byte-identical at `4b0670b`, `ac16e4c` and the
working tree), never to the pinned WP4.1 baseline.

| Surface | Warnings |
|---|---|
| `motion.css` | 10 |
| `base.css` | 13 |
| `layout.css` | 84 |
| `components.css` | 1,930 |
| `navbar.css` | 356 |
| **`theme-dark.css`** | **230** |
| `a11y.css` | 128 |
| **Seven-surface total** | **2,751** |

`theme-dark.css` breakdown: `declaration-no-important` **124**,
`declaration-property-value-disallowed-list` **82**, `selector-max-id` **24**.

**Why the two committed baselines are the wrong anchor, with numbers:**

| Candidate anchor | Total | `theme-dark.css` | Why it is wrong |
|---|---|---|---|
| **This arc's base** (`ac16e4c`) | **2,751** | **230** | correct — use this |
| `CSS_PHASE4_WP4_4_A_BASELINE.json` (`46e340e`) | 2,883 | 264 | predates WP4.4-b…k; quoting it would book **−132** of someone else's reduction to P3 |
| `CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json` (`9ee7638`) | 7,202 | — | different **scope entirely** — 21 files including `scss/**`; two arcs old |

`declaration-no-important` on `theme-dark.css` is **124**, which equals the emitter's
independent `importantDeclarations` count. Two tools, two methods, same number.

### 3.4 Two plan assumptions discharged

- **⚠️ "Assumed j's committed controls still run against the current tree."**
  `scripts/css_audit/j_known_live_mutation.mjs:39` pins
  `EXPECTED_INPUT = e54818bf790eb2c11474f68ecddc25d66304d9edf650cf698853276e419f2fca`. The
  working-tree file hashes to **exactly that**. **j's known-live control still runs at this
  base**, and no `--expect-sha` override is needed. It will need a deliberate re-pin after
  P3-c's first cut — silencing it with `--expect-sha` is the thing the tool's own docstring
  forbids.
- **⚠️ "Assumed `selector-max-id: 24` measures syntax, not cascade weight."** Measured
  stronger than assumed: the file's selectors contain **82 ID tokens**, and **all 82 are
  inside a `:where()` argument**, contributing zero specificity. Stylelint's 24 is a *warning*
  count (one per offending selector), not a token count. No packet may read either number as
  "heavy selectors", and a packet that deletes ID-bearing rules moves the Stylelint count
  without moving any specificity at all.

---

## 4. The emitted ceiling table

### 4.1 Why the emitter exists, verified rather than argued

`measure.contract_anchors()` and `measure.pinned_declarations()` iterate
`measure.CONTRACT_FILES` (`measure.py:34-37`), which is exactly
`tests/test_css_cascade_contracts.py` and `tests/test_visual_selector_contracts.py`.

Measured by `shared_register_reach()`:

- Ceiling rows reachable from `CONTRACT_FILES`: **2** — `cascade_contracts.py:1006` and
  `:1007`. **This is exactly the "Ceiling 3 and nothing else" that re-review N1 predicted.**
- Ceiling rows **unreachable**: **12**, all in per-packet contract files the tuple does not
  list.
- `CONTRACT_FILES` covers `tests/test_css_wp4_4_theme_dark_contracts.py`: **no**.

One correction to how the register's coverage claim should be read.
`tests/test_css_wp4_4_a_baseline_contracts.py:301` asserts `theme-dark.css` is among the
register's bound surfaces, and it **is** — but `contract_anchors()` records a surface as
`touched` when the test's *source text* mentions the filename, and **9** of the anchor entries
bind `theme-dark.css` only through a `base.index("css/theme-dark.css")` link-order assertion.
The claim is true and it does **not** mean the register enumerates this file's content
ceiling. `pinned_declarations()` is likewise not surface-resolved: filtered to strings that
also occur in `theme-dark.css` it returns `background:` and `border-color:` as noise
alongside the two real `.frame-header` pins.

**The double lock is confirmed.** `tests/test_css_wp4_4_a_baseline_contracts.py:297-298`
asserts both registers equal the committed `CSS_PHASE4_WP4_4_A_BASELINE.json` exactly, so
editing `tests/test_css_cascade_contracts.py` **at all** — including to strengthen a pin —
moves `startLine` / `endLine` / `assertionLines` and reds that contract too.

### 4.2 The table — regenerated mechanically

Content class = constrains the file's bytes. Link class = constrains the `<link>` (R4).
Headroom = how much may be removed before the assertion reds.

| # | Row | Class | Shape | Current | Bound | Headroom | Ceiling |
|---|---|---|---|---|---|---|---|
| 1 | `theme_dark_contracts.py:32` | link | substring-presence | — | — | — | R4: the file stays linked. **Not a deletion ceiling.** |
| 2 | `theme_dark_contracts.py:34` | content | truthy | — | — | — | the comment-stripped file may not be emptied |
| 3 | `theme_dark_contracts.py:35` | content | count-floor | **74** | 50 | **24** | **at most 24 brace-blocks removable, arc-wide** |
| 4 | `theme_dark_contracts.py:45` | content | count-exact | **34** | 34 | **0** | blocks P3-d entirely without Q1 |
| 5 | `theme_dark_contracts.py:52` | content | count-exact | **1** | 1 | **0** | F6 may be neither removed nor duplicated |
| 6 | `theme_dark_contracts.py:53` | content | substring-presence | — | — | — | F6 preserved |
| 7 | `theme_dark_contracts.py:55` | content | substring-presence | — | — | — | the `@media` block must keep covering `.value-changed` |
| 8 | `theme_dark_contracts.py:62` | content | count-floor | **7** | 7 | **0** | **zero headroom** — deleting any one reds it |
| 9 | `theme_dark_contracts.py:68` | content | substring-absence | — | — | — | G4 back-door half; satisfied by deletion |
| 10 | `theme_dark_contracts.py:88` | content | count-ceiling | — | 1 | — | **passes at zero — O14** |
| 11 | `theme_dark_contracts.py:98` | content | substring-absence | — | — | — | N2 premise; forbids the "make it win" shape |
| 12 | `a_baseline_contracts.py:128` | content | substring-presence | — | — | — | the literal `Zero !important. */` stays; occurs **once** |
| 13 | `cascade_contracts.py:1006` | content | substring-presence | — | — | — | the `.frame-header` rule head may not be deleted or reformatted; occurs **once** |
| 14 | `cascade_contracts.py:1007` | content | substring-presence | — | — | — | **satisfied by 4 lines, not 2 — O14, worse than recorded.** §5.1 |

### 4.3 The three adjacent buckets — counted, not omitted

| Bucket | Count | Effect on deletion |
|---|---|---|
| **Link-class assertions** (whole repository) | **10** | none. Forbid unlinking or reordering. `theme_dark_contracts.py:32`; `test_version.py:89`; `cascade_contracts.py:264, 301, 351, 431, 515, 583, 646, 730` (link-order guards). |
| **Parametrized surface readers** | **2** | none — additive, satisfied by deletion. `a11y_contracts.py:426`, `layout_contracts.py:292`. |
| **Arc-owned contract files, excluded** | **1 file** | excluded from the table and **counted**. This packet's own file reads the CSS to build fixtures; folding it in would make the arc's output an input to its own ceiling. |

### 4.4 How the walk decides what is a reader

The distinction that makes the table 14 rows instead of ~130: a *path expression reaching the
file that is then read*, versus a *mention of the filename*.
`tests/test_css_cascade_contracts.py` has a module-level `GLOBAL_BUNDLES` tuple containing
`"theme-dark.css"`; a name-mention walk turns every test that touches that tuple into a
ceiling row. The emitter resolves module-level **path handles** and **text handles** to a
fixpoint, then tracks intra-function assignments that carry the file's text, and admits an
assertion only when the assertion itself references one. `test_the_walk_does_not_mistake_a_
bundle_name_list_for_a_file_read` pins that `cascade_contracts.py` contributes exactly
`{1006, 1007}`, with a synthetic-module red path in both directions.

---

## 5. Discrepancies against the plan's copy of the table

Regenerated mechanically. The plan's copy is Gate-0 material and was used only as the
comparison target.

| Item | Plan | Measured | Agrees |
|---|---|---|---|
| Lines | 574 | 574 | yes |
| Top-level rules | 72 | 72 | yes |
| Brace-opening blocks | 74 | 74 | yes |
| Custom-property declarations | 34 | 34 | yes |
| Custom-property split | 16 / 18 | 16 / 18 | yes |
| `!important` declarations | 124 | 124 | yes |
| `.value-changed` occurrences | 7 | 7 | yes |
| Whole-block budget (braces − 50) | 24 | 24 | yes |
| Ceiling row set (14) | 14 named rows | **identical set** | yes |
| Rows reachable from `CONTRACT_FILES` | 2 | 2 | yes |
| `theme_dark_contracts.py:88` passes at zero | true | **true, measured** | yes |
| Parametrized surface readers recorded | 2 | 2 | yes |
| **Occurrences of the pinned `backdrop-filter: blur(8px) !important;` literal** | **2** | **4** | **NO** |
| **Link-class assertions carried** | **1** | **10** | **NO** |

**Everything the plan measured is correct. Two things it recorded are wrong, and one of them
matters.**

### 5.1 DISCREPANCY 1 — Ceiling 3 is materially worse than recorded

The plan states that `backdrop-filter: blur(8px) !important;` *"occurs **twice** — at `:102`
inside `.frame-header`, and at `:144`"*, and concludes *"at most one of `:102` / `:144` may
lose it — and the check cannot tell which."*

**Measured: the pinned literal is satisfied by four lines, not two.**

```
:102     backdrop-filter: blur(8px) !important;
:103     -webkit-backdrop-filter: blur(8px) !important;
:144     backdrop-filter: blur(8px) !important;
:145     -webkit-backdrop-filter: blur(8px) !important;
```

`tests/test_css_cascade_contracts.py:1007` is a bare substring check, and
`-webkit-backdrop-filter: blur(8px) !important;` **contains**
`backdrop-filter: blur(8px) !important;` as a substring. So the correct ceiling is not "at
most one of two may go" — it is:

> **Both `:102` and `:144` may be deleted and the assertion stays green**, as long as either
> `-webkit-` prefixed line survives. The pin protects nothing it claims to protect.

The comment at `tests/test_css_cascade_contracts.py:993-995` says the assertion exists because
*"the late dark theme is why the route retains one explicit dark frame-header blur override."*
The assertion cannot detect the loss of that override. This strengthens the Q8 ruling rather
than weakening it: the owner excluded `.frame-header` from candidacy and noted that *"the
exclusion rests on this plan's discipline, not on the contract's protection."* That is now
measured, and the gap is twice as wide as the note assumed.

`test_the_backdrop_filter_pin_is_detected_as_satisfiable_by_absence` pins the detection, with
a red path that reduces the literal to a single occurrence and shows the flag clear.

### 5.2 DISCREPANCY 2 — the link class is 10 assertions, not 1

The plan's table carries one link-class row (`theme_dark_contracts.py:32`) and omits nine
others. None imposes a deletion ceiling, so **no conclusion in the plan changes** — but the
set matters to a packet that might reformat the `<link>` block, and R4 is enforced by ten
assertions across three files, not one. Recorded so no later packet re-derives it.

### 5.3 A third finding, in the shared apparatus rather than in the plan

The same substring-containment defect exists **inside `measure.py`**.
`BLIND_SPOT_REGISTER`'s backdrop-filter entry cites
`helperEvidence: "backdrop-filter: none !important;"`, and `e2e/visual-helpers.ts:49-50`
declares both the unprefixed and the `-webkit-` prefixed neutralizer. The evidence string
occurs **twice**, so deleting the neutralizer the entry describes leaves
`verify_blind_spots()` clean. The one direction that verifier *does* check is itself
satisfiable by absence.

Recorded, not repaired — `measure.py` is outside this packet's owned paths.
`test_the_blind_spot_evidence_string_for_backdrop_filter_is_substring_shadowed` executes the
demonstration.

---

## 6. The nineteen committed tools — the re-scoped list that prices P3-a1

All nineteen assessed. Coverage is checked **mechanically** against the directory listing
(`test_every_committed_css_audit_tool_is_assessed`, red path: an unassessed tool in a
synthetic directory), so a tool added later cannot quietly widen a1's scope. Judgement is
curated; coverage is not.

### 6.1 Reuse unmodified — 9

| Tool | Why |
|---|---|
| `specificity.py` | the only committed component that already models `:where()` contributing zero — the exact construct this arc turns on. Unit-checked. No P3 variant warranted. |
| `resolution_check.py` | M4. Replays CDP cascade data against the model and reports every ownership disagreement. Directly reusable as **O3**'s "name the winner" check. |
| `measure.py` | read-only, for independent recount cross-checks. Its registers cannot enumerate this ceiling (§4.1) and its blind-spot register is one-way verified (§9). Repairing either is a1's question. |
| `i_seed_probe_db.py` | reuse **and do not modify** — its scoped raw-`sqlite3` exception is conditioned on not being modified. a1's superset seeding must land in a new `p3_seed_probe_db.py`. |
| `runtime_probe.mjs` | the capture layer, its M5 same-CSS control, its M6 sentinel-effect check and its CDP dump. **Not a removal oracle** — see 6.3. |
| `j_theme_differential.mjs` | already whole-document, both themes, four fatal controls. This is the instrument that returned j's uninformative zero, and reusing it is correct *because* the fix is O1′ bracketing, not a different differ. |
| `j_diff_theme.mjs` | already implements every **O6** refusal: same-root pair, equal served digests, failed half-control, empty comparison. |
| `stylelint_surfaces.mjs` | the arc anchor runs through it. |
| `j_known_live_mutation.mjs` | still runs at this base (§3.4). **Not** a per-family control: it re-points *every* `--bg-primary` line, so it cannot separate the two token blocks (P-2 obligation (d)) and it fires nowhere near F2/F3. |

### 6.2 Conditionally reusable — 3

| Tool | Condition |
|---|---|
| `i_element_pixel_diff.mjs` | **the only committed answer to O12.** The one tool that measures *rendered* pixels at element scope without the visual-helpers neutralizers — exactly what the superset alpha-compositing hazard needs, because a differential keyed on the row's own `background-color` reports zero while the composite moves. Its scope constant is `.table-calm`; retargeting is a parameter change, not a rewrite. |
| `j_shadow_certification.mjs` | F1 **nomination** only. Statically decidable and conservative, and it excludes custom properties by design — which is the whole of F1. Answers a strictly narrower question than M-h3. |
| `j_theme_dark_inventory.mjs` | census input to P3-b's partition. Already separates custom properties and the reduced-motion block; does not emit a disjoint per-declaration partition under an ordered predicate chain, which is P3-b's delta. |

### 6.3 Not reusable — 7, with the reason

| Tool | Why not |
|---|---|
| `emit_baseline.py` | **build-path input, and the finding is adverse — see §9.2.** A fresh `build()` at HEAD differs from the committed baseline in `sourceCommit`, `surfaces`, `totals` **and** `isFamily`, and the `isFamily` delta reds `test_is_family_enumeration_is_complete_and_classified`. Q10's "regenerate the baseline" cannot be a whole-file re-emit. |
| `i_five_route_computed.mjs` | build-path input. Subtree-scoped to the `:is()` family's five routes; `theme-dark.css` reaches tables, forms, cards, the navbar, headings and the welcome hero, so that scope is a guess here. `j_theme_differential.mjs` is the whole-document successor. Its **control catalogue** is worth copying; its scope is not. |
| `i_known_live_mutation.mjs` | build-path input. Mutates `components.css`, which **C8** freezes and this arc writes no byte of. Reusable only as the design pattern for a committed, digest-pinned, re-executable mutation. |
| `i_diff_computed.mjs` | pairs with a capture format this arc does not produce. Its `--expect-same-css` inversion is the right pattern; `j_diff_theme.mjs` already carries it for j's shape. |
| `i_diff_g3.mjs` | G3 is a WP4.4-i gate on `pages-workout-log.css`. Nothing here touches that surface. |
| `n4_regions_abc.mjs` | region-scoped and structurally keyed to `pages-workout-log.css`. **But it is the single most valuable reference for a1's census**: its wins/loses-with-named-owner record shape is precisely **O3**, and its structural (never line-keyed) anchor resolution is precisely **O11**. 1,101 lines — the largest committed tool. |
| `visual_helper_band_proof.mjs` | the named band-reconciliation tool, and **not an evidence source**: it compares two variants of the *helper*, not two variants of the product CSS, so it cannot certify a deletion. |

### 6.4 What this means for pricing P3-a1

- **No removal oracle exists.** No `h_*` file is present under `scripts/css_audit/`, and no
  committed tool removes a declaration and re-reads computed values. Every instrument is a
  differential, a census, a static certifier or a lint wrapper.
  `test_no_committed_tool_is_claimed_to_be_a_removal_oracle` asserts this against the
  directory, with a red path that restores an `h_certify.mjs` and shows AB-1's premise fail —
  so a recovered harness forces the claim to be re-made rather than passing unnoticed.
- **The nineteen-tool assessment reduces the new-tool count below Plan v1's seven.** Plan v1
  proposed `p3_census.mjs`, `p3_removal_oracle.mjs`, `p3_zero_winner_check.mjs`,
  `p3_ranges.mjs`, `p3_build_manifest.mjs`, `p3_apply.mjs`, `p3_family_controls.mjs`. On this
  assessment:

  | Proposed tool | Disposition after the assessment |
  |---|---|
  | `p3_removal_oracle.mjs` | **genuinely new.** Nothing committed does this. The single largest unit in a1. |
  | `p3_census.mjs` | **new, but heavily derived** from `n4_regions_abc.mjs`'s record shape + `j_theme_dark_inventory.mjs`'s structural census. |
  | `p3_zero_winner_check.mjs` | **new** — must be independent of the census by construction, which is the point. |
  | `p3_ranges.mjs` | **new**, and it carries the CRLF/character-offset hazard measured in §3.1. |
  | `p3_build_manifest.mjs` | **new**, and must implement **O10b** (contract-pinned literals derived from the contract files' ASTs). `p3_ceiling.py` already emits those literals with their occurrence counts, so a1 consumes them rather than re-deriving. |
  | `p3_apply.mjs` | **new**; digest-asserting, pristine re-encode before it cuts. |
  | `p3_family_controls.mjs` | **new**; `j_known_live_mutation.mjs` is the pattern but not the tool (it fires in neither F2 nor F3). |
  | *(added at re-review)* `p3_blind_spots.mjs` | **new**; §9 gives it its target list. |
  | *(added at re-review)* `p3_seed_probe_db.py` | **new**; `i_seed_probe_db.py` may not be modified. |

  So the assessment does **not** shrink the build. It confirms nine new tools rather than
  seven, and it removes ambiguity about which four committed instruments a1 may lean on
  (`j_theme_differential.mjs`, `j_diff_theme.mjs`, `runtime_probe.mjs`, `resolution_check.py`)
  and which one answers O12 (`i_element_pixel_diff.mjs`). **P3-a1 remains L, and the effort
  note in Plan v2 that "the nineteen-tool assessment may reduce the number of new tools" is
  not borne out.** That is the honest read and it is recorded rather than smoothed.

---

## 7. C7 — the uncertifiable set, recovered by reading

Read from `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` →
`uncertifiableElements.elements[]`. Not re-derived. The retracted architecture-reviewer #11
finding is confirmed retracted: the set was never lost with the gitignored `artifacts/` tree.

| Declared count | Recovered | `domPath` on all | `selector` on all |
|---|---|---|---|
| 8 | **8** | **yes** | **yes** |

| # | Selector | Animation | Duration |
|---|---|---|---|
| 1 | `i.fas.fa-heart.credit-heart` | `heartbeat` | 1.5s |
| 2 | `div.hero-center-icon` | `pulse-glow` | 3s |
| 3–8 | `div.hero-card.hero-card-1` … `-6` | `float` | 6s |

Route `/` (welcome), **both themes**. Ledger rule, carried verbatim:

> *"NO downstream packet may classify a declaration affecting these elements as dead on the
> authority of the rest-state harness. Certifying them requires a different instrument,
> proposed and approved separately."*

**The adjacency, which is the part a packet loses first:**
`div.developer-credit-banner` is **not** in the element list, because the infinite animation
belongs to its `::before` pseudo-element and the host's own `animation-name` computes to
`none`. A packet touching that banner's pseudo-element paint must treat it as uncertifiable
too. `test_the_c7_uncertifiable_set_is_recoverable_from_the_committed_ledger` pins the
recovery including the adjacency note, with a red path that strips one `domPath`.

---

## 8. N8 denominator — the reconciliation, and it closes exactly

**No deep gate was dispatched.** This is a desk exercise over `.github/workflows/deep-gate.yml`,
the ledger's `scopeNote` (`:177`) and the 66 + 18 baseline pins at
`tests/test_css_wp4_4_a_baseline_contracts.py:39-44`.

### 8.1 The gap

| | |
|---|---|
| Committed baselines, `visual.spec.ts` | **66** per platform |
| Committed baselines, `visual-baseline-thumbnails.spec.ts` | **18** per platform |
| Expected N8 total | **84** |
| Reported in all three recorded runs | **68** |
| Unaccounted | **16** |

The workflow does run both specs together — confirmed in `deep-gate.yml`, and the
`scopeNote` says so.

### 8.2 The 16 are serial-mode collateral, and the arithmetic is exact

`e2e/visual-baseline-thumbnails.spec.ts:45` sets
`test.describe.configure({ mode: 'serial' })` **at file scope**. In serial mode the first
failure stops the remainder of the group from running.

The spec's own generation order is `viewport × theme × mode` with
`VIEWPORTS = [desktop, tablet, mobile]`, `THEMES = [light, dark]`,
`PLAN_VIEW_MODES = [simple, advanced]`, so:

```
 1  plan-desktop-light-simple      passes
 2  plan-desktop-light-advanced    <- the ledgered red
 3..18                             never run
```

`plan-desktop-light-advanced` is the **only** thumbnail entry in the ledger, and it is test
**2 of 18**. Everything follows:

| | `visual.spec.ts` | thumbnails | total |
|---|---|---|---|
| Tests | 11 × 3 × 2 = **66** | 12 + 6 = **18** | **84** |
| Failed | 10 | 1 | **11** |
| Passed | 56 | 1 | **57** |
| Did not run | 0 | **16** | **16** |
| | | | **84 ✔** |

**11 + 57 + 16 = 84.** The denominator closes.

### 8.3 The falsifiable half

The sum closing is not evidence — it closes for any inputs, because `passed` is derived. The
claim that can be wrong is that the derivation **reproduces the run results the ledger itself
records**. It does, for all three:

| Run | Ref | Ledger records | Derived | Matches |
|---|---|---|---|---|
| `30665129779` | `1019d34` (pre-i) | 11 failed / 57 passed | 11 / 57 | ✔ |
| `30663355864` | i + corrective | 11 failed / 56 passed + 1 flaky | 11 / 57 | ✔ |
| `30671022691` | j | 11 failed / 57 passed | 11 / 57 | ✔ |

`test_the_n8_denominator_reconciles_against_the_recorded_runs` asserts this. Its red path
moves the ledgered thumbnail red to the **last** test in the file — nothing then gets skipped,
the derivation predicts `11 failed / 73 passed`, and the recorded `57 passed` stops matching.

### 8.4 Prior art in the repository, and why the gap stood anyway

The explanation already exists in two places and neither is cited by the plan or the ledger:

- `docs/MASTER_HANDOVER.md:173-178` — *"A failure inside `visual-baseline-thumbnails.spec.ts`
  skips the remainder of that spec … The resulting 'N did not run' is serial-mode collateral,
  never a documented tail."*
- `docs/MASTER_HANDOVER.md:187` — *"**11 failed, 57 passed, 16 did not run**"* on deep-gate run
  `30722690389` (`44fe838`), reproduced on `30721970863` (`d49cc80`).
- `docs/TESTING_STRATEGY_PLANNING.md` §8.7.

What was missing is that **the ledger itself records only `11 failed / 57 passed`** and its
own `totalCountNote` presents 11 as the inherited-red set. Nothing inside the ledger carries
the third number, so a packet reconciling against the ledger alone cannot close the
denominator. That is the defect, and it is a documentation defect, not a measurement one.

### 8.5 The consequence P3-c must carry — this is the part that is not merely bookkeeping

> **`totalCount: 11` is a FLOOR, not the inherited-red count.**

Sixteen thumbnail tests have **never executed** on any recorded N8 run. The ledger cannot
certify them as inherited **or** as clean, and the ledger's own rule — *"A red on a file NOT
in this ledger is a real finding and a rollback trigger"* — cannot be applied to a test that
never ran. `MASTER_HANDOVER.md:189` says exactly this: *"Because the suite is serial, **11 is
a floor, not the count**."*

**Precondition on P3-c** (not on this packet):

1. Either land a green `plan-desktop-light-simple` **and** `plan-desktop-light-advanced` so the
   remaining 16 execute and the ledger can describe the whole matrix, **or**
2. record the 16 unmeasured tests explicitly as an exclusion bucket with its count, and state
   that the arc's N8 reconciliation covers 68 of 84.

Option 1 is what the owner's in-flight Linux baseline regeneration produces. Under the **Q5**
amendment, the replacement ledger is post-regeneration **and** post-#274 by construction, so
P3-c reconciles against that ledger and not against today's. §8.2's derivation is
ledger-driven and re-runs against the replacement without modification.

---

## 9. Q10 — sizing the shared blind-spot-register repair

**Deferred to P3-a0 for SIZING with an obligation that it could ship standalone if the arc is
abandoned. It is sized here and NOT implemented.** `measure.py` is untouched;
`docs/CSS_PHASE4_WP4_4_A_BASELINE.json` is untouched.

### 9.1 The gap, measured by the converse derivation

`measure.verify_blind_spots()` checks one direction only: each register entry's
`helperEvidence` is still present in `e2e/visual-helpers.ts`. Nothing checks the converse, and
`tests/test_css_wp4_4_a_baseline_contracts.py:224` then pins
`len(register) == len(measure.BLIND_SPOT_REGISTER)` against the committed baseline. So a
neutralizer *added* to the helper is invisible, and adding the missing entries moves that
length.

`blind_spot_repair_sizing()` runs the converse read-only. Every rule block in
`prepareForScreenshot()`'s injected stylesheet is classified:

| Bucket | Blocks |
|---|---|
| Fully mapped to a register entry | **6** |
| Token-definition blocks (`--visual-surface-*`; inputs to registered flatteners, not neutralizers) | **2** |
| **Unmapped — no register entry's evidence occurs in the block** | **9** |
| **Partially mapped — matched only by a non-selective declaration evidence string** | **1** |
| Total | **18** |

**Unmapped neutralizing declarations: 19.**

| `visual-helpers.ts` | Selector | Unregistered declarations |
|---|---|---|
| `:53` | `html` | `scroll-behavior` |
| `:62` | `html[data-theme] body, body` | `background`, `background-attachment` |
| `:100` | `… [data-visual-header]::before` | `background` |
| `:103` | `… [data-visual-accent]` | `background`, `transform`, `transition` *(partial — see below)* |
| `:111` | `input, textarea` | `caret-color` |
| `:112` | `select` | `appearance`, `-webkit-appearance`, `background-image` |
| `:126` | `[data-testid="navbar"] a::before, … button::before` | `background-color`, `border-radius`, `transform`, `transition` |
| `:133` | `[data-visual-dropdown-toggle]::after` | `border-color` |
| `:144` | `input[type="number"]::-webkit-{outer,inner}-spin-button` | `-webkit-appearance`, `margin` |
| `:149` | `::-webkit-scrollbar` | `display` |

The `:103` block matches the register's form-controls entry **only because that entry's
evidence string is `box-shadow: none !important;`**, a declaration that also appears here. The
match is coincidental; `background`, `transform` and `transition` are genuinely unregistered.

### 9.2 Sizing against test-strategist #5's figure

Q10 says *"the eight unregistered neutralizers."* Measured, **the number depends on the
boundary and eight is a floor**:

| Boundary | Count |
|---|---|
| test-strategist #5's list (paint-relevant blocks) | 8 |
| **Unregistered rule blocks, mechanically** | **9** (+1 partial = **10** blocks with a gap) |
| **Unregistered neutralizing declarations** | **19** |

The two the reviewer's list omits are `:53` `scroll-behavior` (a scrolling neutralizer, not a
paint one) and `:144` the spin-button `-webkit-appearance` / `margin` (removes the spinner
rendering — paint-affecting). Neither changes the reviewer's conclusion; both change the size
of the edit.

The headline case is unchanged and it is the important one: **`:62-66` neutralizes
`background` and `background-attachment` on `body` in both themes**, which blinds the pixel
matrix to `theme-dark.css:26-33` — the multi-gradient
`:where([data-theme="dark"] body)` background, a headline F2/F3 candidate.

### 9.3 The standalone shape, and what does NOT work

Q10 asks whether the repair could ship as a standalone change if the arc is abandoned. It can,
but **not in the obvious form.**

**What does not work — a whole-file regeneration via `emit_baseline.py`.** Measured by running
`emit_baseline.build()` in memory at HEAD against the committed baseline, feeding the
committed baseline's own `stylelintSevenSurfaces` back in so the Stylelint input is held
constant. Four top-level keys move:

| Key | Moves? | Consequence |
|---|---|---|
| `sourceCommit` | yes | `46e340e` → HEAD |
| `surfaces` | yes | correct and consistent — the pin test re-derives at `sourceCommit` |
| `totals` | yes | follows `surfaces` |
| **`isFamily`** | **yes** | **`fourBranchTokens` 13 → 0, `fourBranchRules` 12 → 0, `threeBranchRules` 1 → 12** |
| everything else (`layers`, `contractAnchors`, `pinnedDeclarations`, `snapshotManifest`, `fatigueBaselines`, `screenshotTolerances`, `specificityModel`, `oracleBlindSpots`) | no | — |

The `isFamily` movement is **WP4.4-i's own `:is()` repair**: the committed baseline describes
the tree at `46e340e`, before i split the family. A regeneration at HEAD therefore **reds**
`test_is_family_enumeration_is_complete_and_classified`
(`a_baseline_contracts.py:157-198`), which pins `fourBranchTokens == 13`,
`fourBranchRules == 12`, `threeBranchRules == 1`, `len(leaking) == 14` and the
`ruleLine == 4433` reduced-motion record. Closing that would require editing
`a_baseline_contracts.py` — a "run always, edited never" file — which Q10 does not authorize
and Q1 does not cover.

**What does work — a scoped patch.** Standalone, no arc dependency:

| Step | Cost |
|---|---|
| 1. Add the missing entries to `measure.BLIND_SPOT_REGISTER` | ~9–10 entries × ~10 lines ≈ **90–110 lines** in `measure.py` |
| 2. Replace `verify_blind_spots()` with a bidirectional derivation | ~**40–60 lines**; must still return `[]` at the repaired state so `a_baseline_contracts.py:223` stays green. `blind_spot_repair_sizing()` in `p3_ceiling.py` is a working prototype of the converse half |
| 3. Fix the substring-shadowed evidence string (§5.3) | ~**1 line** — the backdrop-filter entry's evidence must not be satisfiable by the `-webkit-` line |
| 4. Patch **only** `oracleBlindSpots` in `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` | array replacement; leaves `sourceCommit` and every other key alone, so `test_wp4_4_baseline_is_pinned_and_matches_its_source_commit` and `test_is_family_enumeration_is_complete_and_classified` both stay green |
| 5. A red-path test: add a neutralizer to the helper, pytest goes red | ~**30 lines** |
| 6. Gates | full pytest only. `e2e/visual-helpers.ts` is **read, never written**, so no snapshot moves and no visual gate is engaged |

**Total ≈ 170–200 lines across two files plus one JSON array, gated by full pytest alone.**
Small, self-contained, and it ships without any part of this arc. Step 4 is the load-bearing
decision: a scoped array patch rather than a re-emit is what keeps it standalone.

**Recommendation, for the owner's decision and not taken here:** grant it, and ship it
independently of P3. `QUALITY_GATE.md:39` routes **every future CSS packet** into the register,
and `CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md:181`'s claim that *"the register cannot drift
from the file it describes"* is false in the only direction that matters. The arc is safe
either way — P3-a1 owns P3-local registers regardless.

---

## 10. Recorded, unacted — things this arc is not authorized to change

Per the plan's in-scope clause: *"Recording, unacted, anything the classification surfaces
that this arc is not authorized to change."*

| # | Finding | Where | Status |
|---|---|---|---|
| 1 | `cascade_contracts.py:1007` is satisfied by **4** lines, so `.frame-header`'s blur override can be deleted entirely with the pin green | §5.1 | **recorded.** Q8 defers the repair to its own decision; the exclusion of `.frame-header` from candidacy stands and now rests on measured discipline |
| 2 | `measure.BLIND_SPOT_REGISTER`'s backdrop-filter `helperEvidence` is substring-shadowed by the `-webkit-` line | §5.3 | **recorded.** Outside owned paths. Folded into the Q10 sizing as step 3 |
| 3 | `measure.py:81` still cites `theme-dark.css:595` for the `Zero !important.` comment, which now sits at **`:548`** | `measure.py:81` | **recorded.** The plan already routes this to P3-a1 "only if Q10 is granted; otherwise record it". Recorded. |
| 4 | `measure.surface_counts()` reports LF-normalized bytes (22,018) for a CRLF file that is 22,592 bytes on disk | §3.1 | **recorded.** Not a defect in `measure.py` — a unit that a1's offset math must not inherit |
| 5 | `contract_anchors()` binds a surface on a source-text mention, so 9 of its `theme-dark.css` entries are link-order tests | §4.1 | **recorded.** `a_baseline_contracts.py:301` is true and does not mean what a reader may take it to mean |
| 6 | `pinned_declarations()` is not surface-resolved; `background:` and `border-color:` appear as noise | §4.1 | **recorded.** O10b's manifest builder must resolve pins to surfaces, not just to literals |
| 7 | The committed A-baseline cannot be regenerated in place; `isFamily` reds | §9.3 | **recorded.** Constrains Q10's implementation shape |
| 8 | 16 thumbnail tests have never executed on any recorded N8 run; `totalCount: 11` is a floor | §8.5 | **recorded as a precondition on P3-c**, not on this packet |
| 9 | `docs/test_inventory/TEST_INVENTORY.{json,md}` will drift — this packet adds 37 tests and `Test Inventory Drift` is blocking as of #267 | §12 | **recorded, not fixed** — outside this packet's three owned paths, and regenerating it requires `npx playwright test --list`, which is outside the skill guard |
| 10 | The plan's gate table for read-only packets omits `pyright baseline diff`, which is blocking on every PR and did catch 7 net-new diagnostics here | §2 | **recorded.** Not a defect in the plan's reasoning — the a0 column derives from the `static/css/**` row, and pyright is a repository-wide gate. A future packet adding Python should run it regardless of its column. |

---

## 11. Contracts — the O14 / O15 discipline

`tests/test_css_theme_dark_p3_audit_contracts.py`, **37 tests**, all green.

**O15 — red paths are committed, executed fixtures.** Every red path is a synthetic tree the
test writes and feeds to the same function under test: a copied `tests/` directory with one
anchored edit, a copied CSS file with one anchored edit, a throwaway `git init` repository, a
mutated ledger JSON, a mutated helper file, or a synthetic `scripts/css_audit/` directory.
Every fixture edit asserts its anchor is present before applying, so a stale fixture cannot
pass by doing nothing. Nothing is described in markdown and asserted nowhere.

**O14 — every contract is shown to fail when the thing it protects is removed.**

| Contract | Red path — the input that makes it fail |
|---|---|
| reader coverage | a reader module whose file read is replaced by `""` |
| walk precision | a module that only *names* the file → zero rows; then the same module reading it → one row |
| self-exclusion is counted | a synthetic `test_css_theme_dark_p3_*` file → lands in the bucket, and an empty bucket fails |
| block budget | a whole rule deleted → 74 → 73 |
| token blocks / F1 nomination | one redeclaration removed from the later block |
| `.value-changed` zero headroom | an eighth `.value-changed` rule added |
| backdrop-filter O14 flag | the literal reduced to a single occurrence → flag clears |
| sliced-haystack discrimination | the slice replaced by the whole file → flag fires |
| Q1 defect probe | a pinned longhand duplicated → "exactly once today" fails |
| production CSS clean | a throwaway repo with a dirty `static/css` |
| arc base is measured | a throwaway repo → different HEAD reported |
| tool coverage | an unassessed tool added to a synthetic directory |
| no removal oracle | `h_certify.mjs` restored → AB-1's premise fails |
| C7 recovery | one `domPath` stripped from the ledger |
| N8 reconciliation | the ledgered red moved to the last test → derivation predicts 73 passed, recorded says 57 |
| Q10 sizing partition | a bucket count reduced by one → the partition drops a block |
| shared registers reach 2 | `CONTRACT_FILES` extended **via `monkeypatch`** → reach exceeds 2 |
| plan comparison runs | a fully-agreeing row list → "no disagreement at all" fails |

Two notes on that table.

- The `CONTRACT_FILES` red path uses `monkeypatch` **precisely so the demonstration cannot
  become the change**: the shared tuple is restored at teardown, the committed baseline is
  never regenerated, and `a_baseline_contracts.py` never sees a moved register.
- The green side was verified too. A mutation exercise replaced each emitter function with a
  broken version — `theme_dark_readers()` returning `[]`, `q1_occurrences()` reporting 2,
  `n8_denominator()` reporting a mismatch, `tool_assessment()` reporting incomplete coverage,
  `production_css_status()` reporting dirty, `plan_discrepancies()` reporting universal
  agreement, and four others — and **all 16 green contracts fired**. None is vacuous. The
  committed red-path pairs are the durable form of that check and run on every pytest
  invocation.

**One contract shape deliberately avoided.** Nothing here pins the current *shape* of
`theme-dark.css` — not its digest, not its rule count, not the backdrop-filter occurrence
count as a value. Per-packet contract files are permanently collected (P-4 / N1), so a
contract of that shape would red on P3-c's authorized cut and force a later packet to weaken
an earlier packet's assertion. The live figures are reported in this document; what is pinned
is that the emitter derives them correctly from whatever it is given.

---

## 12. Unresolved blockers and preconditions

**Blocking a merge of this packet:**

1. **`docs/test_inventory/TEST_INVENTORY.json` / `.md` are stale.** This packet adds 37 tests,
   and `Test Inventory Drift` became **blocking** on 2026-08-01 (#267 / `5b7a4f1`). The
   regeneration command is `python scripts/generate_test_inventory.py`, and it requires
   `npx playwright test --list` and therefore `npm ci` in the worktree. **Not done here:**
   `docs/test_inventory/**` is outside this packet's three owned paths, and the Playwright
   invocation is outside the dispatch's skill guard. **This is an owner or follow-up action
   before the PR.** It is a pure regeneration; no judgement is involved.

**Blocking P3-a1 (not this packet):**

2. **The a1 worktree needs `npm ci` and a `.venv`.** This worktree has neither, so
   `scripts/css_audit/stylelint_surfaces.mjs` and every `.mjs` harness cannot run in it
   directly, and `pyright` needs an explicit `--pythonpath` because `pyrightconfig.json` pins
   `venv: ".venv"`. a1 builds `.mjs` tools and needs a working environment, not a workaround.
3. **Q10 needs an answer** — §9. a1 is safe either way (it owns P3-local registers
   regardless), but the shared defect stays standing for every future CSS packet if the answer
   is no.
4. **The dispatch decision itself.** a1 is not authorized by the Gate 0/Gate 1 sign-off.

**Blocking P3-b:**

5. **PR #274 (Bootstrap 5.1.3 → 5.3.8) lands first** — the Q11 ruling. Unchanged by anything
   measured here; nothing in a0's inputs is touched by #274, and the 14-row ceiling table
   survives it.

**Blocking P3-c:**

6. **The N8 denominator's 16 unmeasured thumbnail tests** — §8.5. Either the regeneration
   makes the thumbnail head green so all 18 execute, or the 16 are recorded as a counted
   exclusion.
7. **The replacement ledger.** Per the Q5 amendment, no packet may reconcile against today's
   schema-v2 11-red ledger.

**If the owner ends the arc at P3-a0** — under **D3** this packet would then be the packet
that terminates the arc, and the interim rule is *stop and escalate, naming the three paths
and the exact lines*. Not triggered here, because a0 completed its scope and did not meet an
abandonment criterion. Recorded so the boundary is explicit: the three paths are
`docs/MASTER_HANDOVER.md`, `docs/ACTIVE_DEVELOPMENT.md` and `docs/REFACTOR_PLAN.md`, and the
lines are each file's lead block and its `## Next Safe Step` section. **This packet wrote none
of them.**

---

## 13. What P3-a0 does not answer

Stated plainly, because the owner's recorded reasoning for funding a0 alone depends on it.

- **a0 deletes nothing and certifies nothing.** It cannot say how much of `theme-dark.css` can
  never win. That question needs the removal oracle a1 would build, and §6.4 confirms no
  committed tool answers it.
- **a0 measures no computed value and renders no page.** Every figure here is static: file
  bytes, test ASTs, committed JSON, and one Stylelint pass.
- **The standing risk is unchanged.** Deletion authority still reduces to instruments P3-a1
  would both write and certify. a0 narrows it only in the sense that the apparatus assessment
  and the ceiling now exist *before* any instrument does, so a1's tools can be measured
  against something it did not produce.

**Three outputs survive total abandonment of the arc**, exactly as the owner's authorization
anticipated:

1. **The N8 denominator reconciliation** (§8) — it closes exactly, it reproduces all three
   recorded runs, and it feeds the in-flight Linux baseline regeneration directly with a
   consequence the ledger does not currently state: 11 is a floor.
2. **The ceiling emitter** (`scripts/css_audit/p3_ceiling.py`) — 14 prose assertions converted
   into a mechanical enumeration, independent of the shared registers that cannot reach them,
   plus a measured correction to the sharpest of them.
3. **The nineteen-tool assessment** (§6) — the only thing that can price a1, and it prices it
   honestly upward rather than down.

---

## See also

- [`docs/css_theme_dark_p3/PLANNING.md`](css_theme_dark_p3/PLANNING.md) — Section 0, Gate 0
  rulings Q1/Q3/Q4/Q5/Q6/Q8/Q9/Q10/Q11, Plan v2, the v2 gate table, O1′–O15, P-1…P-8
- [`docs/CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md`](CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md) §8
  (blind-spot register), §12 (gates)
- [`docs/CSS_PHASE4_WP4_4_J_THEME_DARK_EVIDENCE.md`](CSS_PHASE4_WP4_4_J_THEME_DARK_EVIDENCE.md)
  — the packet that measured the inertia
- [`docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json`](CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json)
  — schema v2; `uncertifiableElements` is the C7 source
- [`docs/ai_workflow/QUALITY_GATE.md`](ai_workflow/QUALITY_GATE.md) — the `static/css/**` row
- [`.claude/rules/verification.md`](../.claude/rules/verification.md) — the durable
  oracle-validation method
