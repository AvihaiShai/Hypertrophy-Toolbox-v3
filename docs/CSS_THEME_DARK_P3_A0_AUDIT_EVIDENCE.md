# CSS `theme-dark.css` inertia arc — **P3-a0** audit evidence

*Packet **P3-a0** of the WP4.4 closeout proposal **P3**. Plan:
[`docs/css_theme_dark_p3/PLANNING.md`](css_theme_dark_p3/PLANNING.md). Naming per **Q4**
(flat `docs/CSS_THEME_DARK_P3_<PACKET>_EVIDENCE.md`).*

**Authority.** Gate 0 and Gate 1 were both signed by the owner on 2026-08-02, and execution
was authorized for **P3-a0 only**. **The owner then TERMINATED the arc at P3-a0 the same day**
— a0's tool assessment (§6) priced P3-a1 at *nine* new tools against the small deletion yield
accepted at Q6, and the owner ruled that does not clear the cost/risk bar. **`P3-a1` is not
funded; `P3-b` … `P3-e` are not authorized. P3 ends when this packet merges, and reopening it
requires a new owner decision.** **a0 is the owner-declared TERMINAL packet** and therefore
holds the narrow D3 status-doc exception — see §12.

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
- No snapshot was regenerated; `--update-snapshots` was not run, and `e2e/__screenshots__/**`
  is byte-identical to `main`. The stale Linux baselines are a **separate recovery packet**,
  explicitly not P3 work.

**One thing changed at finalization, and only because the owner changed it.** The audit ran
under *"`P3-e` is sole writer, and a terminating packet escalates rather than writes."* The
owner then **superseded that with the final D3 ruling and declared a0 terminal**, which grants
this packet a narrow, bounded exception:

> `P3-e` is the sole writer *while the arc continues*. A packet the owner has **explicitly
> declared TERMINAL** may update **the lead block and `## Next Safe Step` — and nothing else** —
> in `docs/MASTER_HANDOVER.md`, `docs/ACTIVE_DEVELOPMENT.md` and `docs/REFACTOR_PLAN.md`.

a0 exercised **exactly** that and no more: two locations in each of three files, recording that
P3 is terminated at a0. No other section of any status document was touched, nothing was
restructured, and no surrounding prose was tidied. §12 has the detail.

---

## 1. The arc base — measured, not inherited, and **re-pinned at finalization**

The plan pins the arc base at `4b0670b` (P2 / PR #222). `main` has since advanced. Per
product-risk #6, this packet records **the SHA it actually measured** rather than inheriting
one.

> **RE-PINNED 2026-08-02.** a0's audit ran against `2332242` / merge base `ac16e4c`. **Five
> pull requests landed on `main` while it ran and finalized** — `#274` Bootstrap 5.3.8
> (`4435b04`), `#275` Node 24 (`95f603f`), `#276` docs (`489a7ce`), `#277` the P3 sign-off +
> arc termination (`67280fb`) and `#279` the Node 24 engines floor (`4de6b62`) — so the branch
> was rebased **twice** and **every figure in this document was re-measured, not carried
> forward.** `#279` landed *during* finalization, after the first re-measurement; its figures
> were re-taken rather than shipped stale, which is the whole point of this section. The old
> pins are shown struck through rather than deleted, because the plan's Q11 event update names
> the first of them explicitly as stale.

| Item | Value |
|---|---|
| Branch | `wt/p3-a0-audit` |
| **Arc base — merge base with `origin/main`** | **`4de6b62`** — `chore(node): declare the Node 24 floor that CI already enforces (#279)` |
| Packet commit measured | `3760e3e` — the rebased `audit(css-p3): …` commit *(originally `9d06136`)* |
| ~~Superseded pins~~ | ~~`2332242` / merge base `ac16e4c`~~ (the audit run), then ~~merge base `67280fb`~~ (the first re-measurement) — both stale, both re-measured |
| Plan-pinned base | `4b0670b` — still an ancestor of HEAD, verified |
| Base drift vs the plan pin | **YES** — **50** commits between `4b0670b` and `4de6b62` (was 22 at `ac16e4c`) |

`arc_base()` reads HEAD live from `git rev-parse`; nothing in the emitter hard-codes a SHA, and
`test_the_arc_base_is_measured_from_the_repository_not_hardcoded` proves it against a synthetic
repository. The value above is the **merge base**, which is the stable thing to cite — the
branch tip advances with each finalization commit.

### The drift is real and, for every input this packet measures, immaterial

Verified rather than assumed, and **re-verified at every one of the six commits** between the
audit's base and the finalized base — `4435b04`, `95f603f`, `cc91c57`, `489a7ce`, `67280fb`,
`4de6b62` — not merely at the endpoints:

| Input | `4b0670b` → `ac16e4c` | `ac16e4c` → `4de6b62` (all six commits) |
|---|---|---|
| `static/css/theme-dark.css` blob | `dffaa58` | **`dffaa58` at every one of the six, and in the working tree** |
| `tests/test_css_wp4_4_theme_dark_contracts.py` | unchanged | **unchanged — blob `794597a` at every one** |
| `tests/test_css_cascade_contracts.py` | unchanged | **unchanged — blob `cd232f4` at every one** |
| `tests/test_css_wp4_4_a_baseline_contracts.py` | unchanged | **unchanged — blob `878ee98` at every one** |
| `scripts/css_audit/**` | unchanged | **unchanged — `git diff --stat` empty** |
| `e2e/visual-helpers.ts` | unchanged | **unchanged — blob `515db4e` at every one** |
| `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` | unchanged | **unchanged** |
| `static/css/**` (whole tree) | no change at all | **changed once, by `#274`** — it rewrote `bootstrap.custom.min.css` + `.map` and made a one-line comment change in `components.css`. **No file this packet measures moved**, and `components.css`'s Stylelint count is identical (§3.3). |
| `.github/workflows/deep-gate.yml` | **changed — 19 lines** | **changed — 4 lines**, `node-version: '20'→'24'` ×2 (`#275`); unchanged again through `#279` |

**Every input the ceiling table, the Ceiling-3 finding, the tool assessment, the N8
reconciliation and the Q10 sizing rest on is byte-identical across all five merged pull
requests.** The `4b0670b → ac16e4c` `deep-gate.yml` change is **only** `actions/checkout@v4→v7`
(×7), `actions/setup-python@v5→v7` (×7), `actions/upload-artifact@v4→v7` (×3),
`actions/setup-node@v4→v7` (×2); the `ac16e4c → 4de6b62` change is **only** the two
`node-version` pins. Across all three refs the `visual-linux` job's `if: ${{ inputs.run_visual }}`
gate (`:343`), its `visual_mode` / `--update-snapshots` handling (`:396–397`) and its

```
npx playwright test --project=chromium \
  e2e/visual.spec.ts e2e/visual-baseline-thumbnails.spec.ts $UPDATE
```

invocation (`:399–400`) are **byte-identical**, and the `visual-baselines-linux` artifact still
uploads `e2e/__screenshots__/linux/**` (`:409–410`). The N8 reconciliation in §8 is therefore
unaffected by either drift.

**Consequence, now that the arc is terminated:** the 14-row ceiling table and every file figure
below hold at `4b0670b`, at `ac16e4c` **and** at `4de6b62` identically. There is no P3-a1 to
inherit them. Any future packet that reopens this ground must re-measure the `deep-gate.yml`
line numbers rather than quote the ones above.

---

## 2. Gates — the P3-a0 column only

Derived from the **P3-a0** column of *Expected gates per packet — the v2 table*, and from
the `static/css/**` row of [`QUALITY_GATE.md`](ai_workflow/QUALITY_GATE.md).

**All figures below are the post-rebase re-run at arc base `4de6b62`.** Nothing is carried
forward from the audit run, and nothing from the intermediate `67280fb` re-measurement either.

| Gate | Required at a0 | Result |
|---|---|---|
| Full `pytest` (cascade contracts inside the total) | ✔ | **2,419 passed / 2 skipped, 0 failed** — see §2.1 |
| **Test-inventory drift `--check`** | ✔ blocking since #267 | **PASS — "Test inventory is up to date."** §2.4 |
| **`pyright` net-new (blocking in CI)** | ✔ | **PASS — 0 net-new** (baseline 175, current 175) |
| Seven-surface Stylelint | anchor only | **2,751 total / `theme-dark.css` 230 — unchanged** §3.3 |
| Production CSS diff empty | ✔ **asserted** | **empty**, asserted by contract **and** by `git diff origin/main HEAD -- static/css` §2.2 |
| No snapshot regenerated | ✔ | `git diff origin/main HEAD -- e2e/__screenshots__` empty; the committed digest assertion (`a_baseline_contracts.py:234-255`) passed inside the full run |
| Required nine Chromium specs | — | **not run** |
| `visual.spec.ts` 66/platform | — | **not run** |
| `visual-baseline-thumbnails.spec.ts` 18/platform | — | **not run** |
| Linux N8 deep gate | — | **not dispatched** |
| N8 denominator reconciled (documentary) | ✔ **a0 produces it** | §8 |
| Whole-page computed differential | — | not applicable (no capture at a0) |

The four "not run" rows are not omissions. The plan is explicit: *"Read-only packets do not
run the E2E or visual gates. Nothing changed, so a pass would carry no information — and a
gate that cannot fail is worse than no gate."* That reasoning is **strengthened** by the
rebase, not weakened: `static/css/**` is byte-identical to `origin/main` (§2.2), so a visual
run could only reproduce `main`'s own state.

**One gate outside the a0 column was run anyway, and it caught something.** `ci.yml`'s
`Type Check` job runs `pyright baseline diff (blocking)`, which fails on **net-new**
diagnostics against `docs/ci_cd_phase3/pyright-baseline.json`. It is not in the plan's a0
column, but it is blocking on every PR and this packet adds two Python files. The first
pre-rebase run over the two new files found **7 net-new errors**, all `dict[str, object]`
indexing and `int()` narrowing; they were fixed in the packet commit.

**Re-run post-rebase over the whole repository — the shape CI actually runs — and it is still
clean:**

```
npx pyright@1.1.410 --pythonpath D:/development/Hypertrophy-Toolbox-v3-main/.venv/Scripts/python.exe \
  --outputjson > artifacts/pyright.json
python scripts/pyright_baseline_diff.py \
  --current artifacts/pyright.json --baseline docs/ci_cd_phase3/pyright-baseline.json
```

```
pyright baseline gate: PASS - 0 net-new diagnostics (baseline 175, current 175).
```

208 files analyzed, 175 errors, 0 warnings — **exactly the committed backlog, and `0`
diagnostics of any severity in either of this packet's two Python files.** That the total
lands on the baseline's own 175 is itself the check that `--pythonpath` resolved third-party
imports the same way CI's `.venv` does. *(`--pythonpath` is needed because
`pyrightconfig.json` pins `venv: ".venv"` and this worktree has none.)*

### 2.1 Full pytest

```
D:/development/Hypertrophy-Toolbox-v3-main/.venv/Scripts/python.exe -m pytest tests/ -q
```

```
2419 passed, 2 skipped in 416.86s (0:06:56)
```

| Measurement | Audit run (`ac16e4c`) | **Final (`4de6b62`)** |
|---|---|---|
| Collected **without** this packet's contract file | 2,380 | **2,384** |
| Tests this packet adds | 37 | **37** |
| Total collected | 2,417 | **2,421** |
| Result | 2,415 passed / 2 skipped | **2,419 passed / 2 skipped / 0 failed** |

**The +4 reconciles exactly, and none of it is this packet's:**

| Landed | File | Tests |
|---|---|---|
| `#274` | `tests/test_bootstrap_version_contract.py` | **1** |
| `#275` | `tests/test_node_version_contract.py` | **2** |
| `#279` | *same file, one case added* — it extended `#275`'s contract rather than adding a second | **+1** (→ 3) |
| | | **4** |

2,380 + 4 = 2,384, and 2,384 + 37 = 2,421 = 2,419 passed + 2 skipped. **This packet's own
delta is unchanged at exactly +37, and no pre-existing test changed state in any run.**

*(The intermediate re-measurement at `67280fb`, before `#279` landed, read 2,418 passed /
2 skipped over 2,420 collected. It is superseded by the figures above and is recorded only so
the +1 is traceable.)*

### 2.2 Production CSS byte-identity — asserted, not assumed

`test_this_packet_wrote_no_production_css` runs `git status --porcelain -- static/css` plus
the staged and unstaged diffs, and fails if any is non-empty. It is **scoped to the working
tree rather than to a base SHA on purpose**: a base-SHA pin in a permanently-collected
per-packet file would red the moment P3-c makes its authorized cut, and no packet may be made
to weaken another packet's assertion in order to ship. Its red path builds a throwaway git
repository, dirties `static/css/theme-dark.css` in it, and shows the same function reports
`clean: False`.

The contract's own emitted record at finalization:

```json
"productionCss": { "statusPorcelain": [], "unstaged": [], "staged": [], "clean": true }
```

**The working-tree assertion is the contract; the base-SHA comparison is the stronger claim
this dispatch also requires, so both are shown.** Against `origin/main` (`4de6b62`):

```
$ git diff --stat origin/main HEAD -- static/css             # (empty)
$ git diff --stat origin/main HEAD -- e2e/__screenshots__    # (empty)
```

**`static/css/**` is byte-identical to `main` and no snapshot was touched.** The complete diff
this branch carries against `origin/main` is **eight files, none of them production CSS and
none of them a snapshot** — the five the packet owns plus the three status documents written
under the terminal-packet exception (§12.4):

```
 docs/ACTIVE_DEVELOPMENT.md                      | lead block only
 docs/CSS_THEME_DARK_P3_A0_AUDIT_EVIDENCE.md     | this document
 docs/MASTER_HANDOVER.md                         | lead block + Next Safe Step
 docs/REFACTOR_PLAN.md                           | lead block only
 docs/test_inventory/TEST_INVENTORY.json         | regenerated
 docs/test_inventory/TEST_INVENTORY.md           | regenerated
 scripts/css_audit/p3_ceiling.py                 | new, 1880
 tests/test_css_theme_dark_p3_audit_contracts.py | new, 1055
```

`--update-snapshots` was never run, and `e2e/__screenshots__/**` was never opened for writing.

### 2.3 Test-inventory drift — the blocking gate, regenerated

`Test Inventory Drift` has been blocking since #267 (`5b7a4f1`). The committed inventory
predated this packet's 37 tests, and a0 recorded that as its one merge blocker (§12). It is
now discharged with the canonical workflow:

```
python scripts/generate_test_inventory.py
  playwright: 541 tests / 30 specs (426 required-functional)
  pytest:     2099 collected / 100 files (deterministic subset; 1 env-dependent file(s) excluded)
  hard waits: 93 lines

python scripts/generate_test_inventory.py --check
Test inventory is up to date.
```

The whole committed diff is this packet's own file: `collected_deterministic` 2,062 → **2,099**
(+37), `deterministic_files` 99 → **100**, `total_files` 100 → **101**, and one new per-file
row at 37 tests. **Playwright is untouched** at 541 / 30 / 426, as are the 93 hard-wait lines.
`npx playwright test --list` is a collection-only listing — **no browser was launched and no
E2E test was executed at any point in this packet.**

*(The `2,062` base is `#279`'s own regenerated figure. The first re-measurement, taken at
`67280fb` before `#279` landed, produced 2,061 → 2,098; it was regenerated rather than
rebased forward.)*

### 2.4 Stylelint invocation note — the workaround is retired

At audit time this worktree had **no `node_modules`**, so the anchor was measured by running
the committed `scripts/css_audit/stylelint_surfaces.mjs` logic verbatim from a scratchpad copy
that resolved the `stylelint` package from the main checkout by absolute path.

**That workaround is no longer in use.** `npm ci` was run in this worktree at finalization,
and the anchor in §3.3 is now produced by invoking the committed script directly and unmodified:

```
node scripts/css_audit/stylelint_surfaces.mjs artifacts/stylelint_seven_surfaces.json
seven-surface stylelint warnings: 2751
```

**The two methods agree exactly**, on the total and on every per-surface and per-rule
sub-count — which retrospectively validates the scratchpad measurement as well as the current
one.

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

> **⚠️ The four byte-level figures above are checkout-dependent, and this is not pedantry —
> it broke CI.** The repository is `core.autocrlf=true` with **no `.gitattributes`**, so the
> committed blob is **LF** and a Windows worktree materializes it as **CRLF**. Both forms are
> the same file; only the bytes differ. **Re-confirmed after the line-ending repair, and both
> figures stand:**
>
> | Form | Bytes | `sha256` | Lines |
> |---|---|---|---|
> | Windows worktree (**CRLF**) — what this document measured | **22,592** | `e54818bf…` | 574 |
> | Committed blob / **Linux CI checkout** (LF) | **22,018** | `3ab06083c89eae0b5dd46d820dde4d2da1d59de1ffa6d825585aaca0ad17e14a` | 574 |
>
> The difference is exactly **574** — one `CR` per line — which is the same arithmetic as the
> `measure.surface_counts()` unit mismatch two paragraphs below, arriving from the other
> direction. **Every structural figure in the table (lines, blocks, rules, declarations,
> `!important`, `.value-changed`, `:where(` tokens) is line-ending-invariant and identical on
> both platforms.** Only bytes and digests move. A later reader on Linux should expect
> `bytesOnDisk: 22018` and `lineEnding: LF` from the emitter and treat that as agreement, not
> drift.
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

### 3.3 Stylelint — the arc anchor, **re-measured at `4de6b62`**

Anchored to **this arc's own base**, never to the pinned WP4.1 baseline.

> **Re-measured twice, carried forward neither time.** `#274` rewrote
> `bootstrap.custom.min.css` and touched `components.css`, so this anchor could not be
> inherited across the rebase; it was then re-taken again after `#279`. **It is unchanged at
> both — identical on the total, on every surface, and on every rule.**
> `bootstrap.custom.min.css` is not one of the seven surfaces, and `#274`'s `components.css`
> edit is a one-line comment change, which is exactly why its 1,930 does not move.

| Surface | Warnings | Audit run (`ac16e4c`) | Moved? |
|---|---|---|---|
| `motion.css` | 10 | 10 | no |
| `base.css` | 13 | 13 | no |
| `layout.css` | 84 | 84 | no |
| `components.css` | 1,930 | 1,930 | **no — despite `#274` editing the file** |
| `navbar.css` | 356 | 356 | no |
| **`theme-dark.css`** | **230** | 230 | no |
| `a11y.css` | 128 | 128 | no |
| **Seven-surface total** | **2,751** | 2,751 | **no** |

`theme-dark.css` breakdown: `declaration-no-important` **124**,
`declaration-property-value-disallowed-list` **82**, `selector-max-id` **24**.

**Why the two committed baselines are the wrong anchor, with numbers:**

| Candidate anchor | Total | `theme-dark.css` | Why it is wrong |
|---|---|---|---|
| **This arc's base** (`4de6b62`) | **2,751** | **230** | correct — use this |
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

  > **Qualified after the line-ending repair, because the original sentence was true on only
  > one platform.** The tool reads with `readFileSync(cssPath)` — a **Buffer**, no newline
  > translation — and hashes those raw bytes (`j_known_live_mutation.mjs:28,60,62`). So
  > `EXPECTED_INPUT` is the digest of the **CRLF** form. **The claim above holds on a Windows
  > checkout and does not hold on a Linux one**, where the file is LF and hashes to
  > `3ab06083…` (§3.1). On Linux the control refuses to run without `--expect-sha`, which is
  > precisely the override its docstring forbids using to silence it. **Recorded, not
  > repaired** — the tool is outside this packet's owned paths, and the arc is terminated. See
  > §10 row 11.
  >
  > **Repaired later, on 2026-08-04, as LEFTOVERS P2.6 — read this block as history, not as
  > live state.** The tool hashes the LF-normalized text now and pins `3ab06083…`, so the
  > claim holds on both platforms again. No measurement in this document moved:
  > `theme-dark.css` was not touched, and §3.1's CRLF figures are still what a Windows
  > worktree shows on disk. What changed is only *which representation the gate is defined
  > over*.
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
- **The hypothesis under test was that the nineteen-tool assessment would reduce the new-tool
  count below Plan v1's seven. Measured, it RAISES it to nine.** Plan v1
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
  seven, and it removes ambiguity about which four committed instruments a1 would have leaned on
  (`j_theme_differential.mjs`, `j_diff_theme.mjs`, `runtime_probe.mjs`, `resolution_check.py`)
  and which one answers O12 (`i_element_pixel_diff.mjs`). **P3-a1 remains L, and the effort
  note in Plan v2 that "the nineteen-tool assessment may reduce the number of new tools" is
  not borne out.** That is the honest read and it is recorded rather than smoothed.

  > **This is the finding that terminated the arc.** The owner weighed **nine new tools**
  > against the deletion yield already accepted at **Q6** — *"a small certified deletion plus a
  > reusable instrument, not a gutted file"* — and ruled on 2026-08-02 that it does not clear
  > the cost/risk bar. **P3-a1 is not funded and P3-b … P3-e are not authorized.** The
  > dispositions above are retained as the priced estimate a future owner decision would start
  > from; **none of them is an action item.**

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

- `docs/MASTER_HANDOVER.md` § *Known Windows visual reds — the WP4.0 pair, both OPEN and
  deferred* — *"A failure inside `visual-baseline-thumbnails.spec.ts` skips the remainder of
  that spec … The resulting 'N did not run' is serial-mode collateral, never a documented
  tail."*
- `docs/MASTER_HANDOVER.md` § *Known LINUX visual reds — stale baselines after the WP4.4 CSS
  arc* — *"**11 failed, 57 passed, 16 did not run**"* on deep-gate run `30722690389`
  (`44fe838`), reproduced on `30721970863` (`d49cc80`).
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
never ran. `MASTER_HANDOVER.md` § *Known LINUX visual reds — stale baselines after the WP4.4
CSS arc* says exactly this: *"Because the suite is serial, **11 is a floor, not the count**."*

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
from the file it describes"* is false in the only direction that matters.

**Now that the arc is terminated, the standalone route is the only route.** The original
hedge — *"the arc is safe either way, since P3-a1 owns P3-local registers regardless"* — no
longer applies: there is no a1 to own a P3-local register, so a refusal leaves the shared
defect standing for every future CSS packet with nothing else covering it. The sizing above
was commissioned for exactly this contingency and it holds unchanged.

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
| 9 | `docs/test_inventory/TEST_INVENTORY.{json,md}` drift — this packet adds 37 tests and `Test Inventory Drift` is blocking as of #267 | §2.3 | **✅ RESOLVED at finalization.** Regenerated under a dispatch that authorized the collection-only `npx playwright test --list`; `--check` reports up to date. The whole diff is this packet's own 37 tests. |
| 10 | The plan's gate table for read-only packets omits `pyright baseline diff`, which is blocking on every PR and did catch 7 net-new diagnostics here | §2 | **recorded.** Not a defect in the plan's reasoning — the a0 column derives from the `static/css/**` row, and pyright is a repository-wide gate. A future packet adding Python should run it regardless of its column. |
| 11 | `j_known_live_mutation.mjs`'s `EXPECTED_INPUT` is the digest of the **CRLF** bytes, so j's known-live control **cannot run unmodified on a Linux checkout** — the file is LF there and hashes to `3ab06083…` | §3.4 | **recorded, not repaired.** Outside owned paths and the arc is terminated. The repo has **no `.gitattributes`** under `core.autocrlf=true`, so every raw-byte digest pinned against a working-tree file has this property. Any future packet re-pinning that constant must say which form it pinned. **→ REPAIRED 2026-08-04 as LEFTOVERS P2.6**, outside this arc and without touching the audited CSS: the tool now hashes the LF-normalized text and pins `3ab06083…`, which is the committed blob's own digest, so both checkouts agree. `tests/test_css_audit_digest_normalization_contracts.py` holds the contract. This row's *finding* stands as recorded — only its disposition changed. |

---

## 11. Contracts — the O14 / O15 discipline

`tests/test_css_theme_dark_p3_audit_contracts.py`, **37 tests**, all green **on both line-ending
forms**.

### 11.0 A line-ending defect in this file, found by CI and repaired

**Five of the 37 passed on Windows and failed on the Linux runner.** The module embedded CSS
anchors with explicit `\r\n` escapes and matched them against
`THEME_DARK.read_text(encoding="utf-8", newline="")` — and `newline=""` performs no
translation, so it yields **CRLF on Windows and LF on Linux** (§3.1). The anchors matched on
exactly one platform.

**This is the arc's own named Tier-2 hazard — "CRLF and character-offset math" — arriving in
the test rather than in the finding.** The evidence had already recorded it against
`measure.surface_counts()` as a *byte-count* mismatch (§3.1, §10 row 4); the same root cause
produced a *substring-match* mismatch here. The audit flagged the hazard and then tripped over
it, which is worth stating plainly rather than quietly fixing.

**The repair normalizes the input, it does not flip the platform.** A single `_read_css()`
helper reads with `newline=""` and then normalizes to `\n`, every embedded CSS literal is
stored with `\n`, and `_synthetic_css()` writes its fixture back with `newline=""` so the
fixture is byte-for-byte LF on both platforms. Rewriting the literals to CRLF instead would
merely have moved the failure to Linux-only developers.

**All twelve escape sites were converted, not only the five that failed.** One of them —
the eighth `.value-changed` rule injected by the zero-headroom red path — was latent: its
*anchor* contained no newline so the test passed on Linux, while the text it *inserted*
carried a stray `CR` into an LF file.

**No contract changed what it asserts.** The Ceiling-3 substring finding, the block budget,
the F1 shadow nomination, the zero-headroom row and the Q1 defect probe all assert exactly
what they asserted before, with every red path intact.

**Verified on both forms rather than argued.** With the working tree converted to LF to
reproduce the Linux checkout, **36 of 37 pass**; the single failure is
`test_this_packet_wrote_no_production_css` correctly detecting the deliberately dirtied
`static/css/theme-dark.css` that the simulation itself created. Restored byte-identically
(`sha256 e54818bf…`), the file is **37 / 37**.

**`scripts/css_audit/p3_ceiling.py` does not share the defect**, checked rather than assumed —
see §11.0a.

### 11.0a Why the emitter was already platform-proof

Every `read_text()` in `p3_ceiling.py` omits `newline=`, so Python's **universal-newline mode**
translates CRLF to LF on the way in. Its CSS text is therefore LF on both platforms already,
and it embeds **no multi-line CSS literal** to match against file text. An AST walk over every
string constant in the module found only two containing a `CR`, and both are correct:

| Site | Construct | Why it is not the defect |
|---|---|---|
| `p3_ceiling.py:299` | `"lineEnding": "CRLF" if "\r\n" in text else "LF"` | A **detector**, not a matcher. It is *supposed* to report whichever form is on disk, and it is the figure §3.1 quotes. |
| `p3_ceiling.py:1214` | `blanked[selector_start] in " \t\r\n"` | A single-character whitespace-class test. `\r` simply never occurs in LF input; `\n` still matches. |

The one deliberate non-translating read is `raw_bytes = path.read_bytes()` in
`measure_theme_dark()` (`:224`), which produces `bytesOnDisk`, `sha256OfBytesOnDisk` and
`lineEnding`. **That must stay untranslated** — it is what makes the O10 offset hazard visible
at all, and those three values are *reported*, never asserted. No contract in this file pins a
byte count, a digest or a line ending, which is why the emitter's platform-dependent figures
never reached CI as a red.

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

## 12. Blockers — all merge blockers discharged; the rest are void or reassigned

### 12.1 Blocking a merge of this packet — **none remain**

1. ~~`docs/test_inventory/TEST_INVENTORY.json` / `.md` are stale.~~ **✅ DISCHARGED.**
   Regenerated and verified at finalization — §2.3. `npm ci` was run in this worktree, the
   canonical two-step workflow was used, and `--check` reports *"Test inventory is up to
   date."* The dispatch that finalized this packet explicitly authorized
   `npx playwright test --list` as a collection-only listing. It was a pure regeneration, as
   predicted; no judgement was involved.

**This packet has no remaining merge blockers and no known reds.**

### 12.2 Blocking P3-a1 — **VOID: a1 is not funded**

The arc is terminated at a0. These are retained as the record of what a1 *would* have needed,
should the owner ever reopen the ground with a new decision. **None of them is an action item.**

2. ~~The a1 worktree needs `npm ci` and a `.venv`.~~ Half-discharged incidentally: `npm ci`
   now works in this worktree and the Stylelint workaround is retired (§2.4). `pyright` still
   needs an explicit `--pythonpath` here because `pyrightconfig.json` pins `venv: ".venv"`.
3. **Q10 has not been answered, and the defect it names is now the arc's main survivor.**
   §9 sizes the repair at **≈170–200 lines across two files plus one JSON array, gated by full
   pytest alone**, and it ships **standalone** — it never depended on this arc. `QUALITY_GATE.md:39`
   routes *every future CSS packet* into that register, so the defect stands for all of them
   until someone fixes it. **This is the one thing in §12 that is still live, and it is now a
   standalone proposal for the owner rather than a precondition on anything.**
4. ~~The dispatch decision itself.~~ **Made, and it was NO.** a1 is not funded.

### 12.3 Blocking P3-b / P3-c / P3-d — **VOID: not authorized**

5. ~~PR #274 lands before P3-b.~~ Discharged by events — #274 merged as `4435b04`, and the
   packet it gated will not run. Its measured non-effect on a0 is re-verified in §1.
6. ~~The N8 denominator's 16 unmeasured thumbnail tests.~~ **Reassigned, not void.** No P3
   packet will consume it, but the finding itself is one of a0's three durable outputs (§13):
   `totalCount: 11` is a **floor**, and the 16 tests have never executed on any recorded run.
   **The owner's separate Linux-baseline recovery packet is the correct consumer** — it must
   verify all **84** expected baselines, not the 68 the ledger describes.
7. ~~The replacement ledger.~~ Void for P3; still true for the recovery packet.

### 12.4 The D3 status-doc boundary — exercised, and exactly to its limit

The audit ran under the interim rule (*a terminating packet escalates rather than writes*) and
wrote none of the three status documents. **The owner then superseded that rule, declared a0
TERMINAL, and granted the bounded exception.** a0 therefore wrote, in each of
`docs/MASTER_HANDOVER.md`, `docs/ACTIVE_DEVELOPMENT.md` and `docs/REFACTOR_PLAN.md`, **exactly
two locations**:

| Location | What was recorded |
|---|---|
| the lead block | P3 is terminated at a0; a0 is the only implemented packet |
| `## Next Safe Step` | a1 is not funded, b–e are not authorized, reopening needs a new owner decision, and what a0 delivered that outlives the arc |

**Nothing else in any of the three files was touched** — no other section, no restructuring, no
tidying of surrounding prose. The exception is owner-triggered by construction: a packet cannot
declare itself terminal and thereby grant itself write authority.

---

## 13. What P3-a0 does not answer — and why the arc stopped here

Stated plainly, because the owner's reasoning for funding a0 alone, and then for terminating
at it, depends on this being said without softening.

- **a0 deletes nothing and certifies nothing.** It cannot say how much of `theme-dark.css` can
  never win. That question needs a removal oracle, and §6.4 confirms **no committed tool
  answers it** — nine would have had to be written.
- **a0 measures no computed value and renders no page.** Every figure here is static: file
  bytes, test ASTs, committed JSON, and one Stylelint pass.
- **The standing risk was never narrowed, only made legible.** Deletion authority still reduces
  to instruments the arc would have both written and certified. a0's contribution is that the
  apparatus assessment and the ceiling now exist *before* any instrument does.

**That is precisely what ended the arc.** §6.4 was commissioned on the expectation that
assessing nineteen committed tools would let a1 lean on some of them and **shrink** the build.
Measured, it does the opposite: **nine new tools, not the seven Plan v1 proposed** — and the
assessment is recorded that way rather than smoothed, because a smoothed number would have
bought a1's funding on a false premise. Against the deletion yield the owner had already
accepted at **Q6** — *"a small certified deletion plus a reusable instrument, not a gutted
file"* — nine tools does not clear the cost/risk bar. **The owner terminated the arc at a0 on
2026-08-02.** The audit paying for itself by *stopping* the work is the outcome the a0/a1 split
was designed to make possible.

**Three outputs survive the termination**, exactly as the owner's authorization anticipated:

1. **The N8 denominator reconciliation** (§8) — it closes exactly, it reproduces all three
   recorded runs, and it feeds the owner's Linux baseline recovery packet directly with a
   consequence the ledger does not state: **11 is a floor**, and 16 thumbnail tests have never
   executed on any recorded run. That packet must verify **84** baselines, not 68.
2. **The ceiling emitter** (`scripts/css_audit/p3_ceiling.py`) — 14 prose assertions converted
   into a mechanical enumeration, independent of the shared registers that cannot reach them,
   plus a measured correction to the sharpest of them: **`cascade_contracts.py:1007` protects
   nothing it claims to protect** (§5.1). It runs on any future tree.
3. **The nineteen-tool assessment** (§6) — the only thing that could price a1, and it priced it
   honestly upward. **It is the artifact that terminated the arc.**

A fourth, sized but not implemented and not tied to P3: **the Q10 blind-spot-register repair**
(§9), ≈170–200 lines, standalone, gated by full pytest alone. It remains available and the
defect it fixes affects every future CSS packet.

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
