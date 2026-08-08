# Windows visual baseline regeneration — evidence

Closes the Windows half of **#304** ("Windows visual baselines are broadly stale: 58 of 66
`visual.spec.ts` tests fail on unmodified `main`"). Linux was regenerated separately in #281.

**Scope of this packet:** regenerate the `win32` baseline corpus, review every changed capture by
eye, and move the two contracts that pinned the pre-regeneration state. **No application code, CSS,
template or test-logic change.** The only non-PNG edits are the two contract constants and the
snapshot manifest.

---

## 1. Why CI could not do this

`deep-gate.yml`'s visual job is **Linux-only** — `name: Visual regression (Linux baselines)`,
`runs-on: ubuntu-24.04`, artifact `visual-baselines-linux`. The only `windows-latest` job in that
workflow is `frozen-windows` (packaged smoke). There is no Windows visual job anywhere in CI, so
`gh workflow run deep-gate.yml -f run_visual=true -f visual_mode=generate` regenerates **Linux
only**.

The win32 corpus therefore had to be generated locally, with `PW_VISUAL_SEED=1`. #304's unblock
steps were corrected on 2026-08-05 to say so.

---

## 2. What changed

Generated locally on Windows, 2026-08-05 00:25–00:29.

| Path | Before | After |
|---|---:|---:|
| `win32/visual.spec.ts-snapshots` | 64 | **66** |
| `win32/visual-baseline-thumbnails.spec.ts-snapshots` | 15 | 15 |
| `linux/visual.spec.ts-snapshots` | 66 | 66 (untouched) |
| `linux/visual-baseline-thumbnails.spec.ts-snapshots` | 15 | 15 (untouched) |
| **tracked total** | **160** | **162** |

Working-tree status: **71 modified, 2 deleted, 4 untracked** PNGs.

The 64 → 66 delta is exactly `−2 +4`:

- deleted `user-profile-mobile-{dark,light}.png` (375×19785 / 375×19742 — both above Chromium's
  16,384 px capture surface, so their tails were unpainted)
- added `user-profile-mobile-{dark,light}-segment-{1,2}.png`

This brings win32 to parity with the linux corpus, which was segmented the same way in #281.

### Contract moves

| Constant | File | Change |
|---|---|---|
| `EXPECTED_SNAPSHOT_COUNTS["win32/visual.spec.ts-snapshots"]` | `tests/test_css_wp4_4_a_baseline_contracts.py` | 64 → 66 |
| `AWAITING_SEGMENTED_REGENERATION` | `tests/test_visual_capture_contracts.py` | two win32 paths → empty set |

`AWAITING_SEGMENTED_REGENERATION` is **kept, not deleted**. Two tests consume it. The first,
`test_no_committed_visual_baseline_exceeds_the_chromium_surface_limit`, is a strict equality against
the measured oversized set, so an empty constant is still a live guard: it now reads "no committed
baseline may exceed the capture surface", and a newly oversized capture reds it immediately. The
second, `test_the_retired_oversized_baselines_are_real_platform_relative_files`, iterates the set and
is therefore **vacuous while it is empty** — it is a meta-guard on the carve-out's honesty, and an
empty carve-out has nothing to be dishonest about.

Measured heights confirm the carve-out is genuinely empty — tallest committed captures:

| Capture | Height |
|---|---:|
| `weekly-summary-mobile-{dark,light}` | 11,559 |
| `session-summary-mobile-{dark,light}` | 10,401 |
| `user-profile-mobile-*-segment-1` | 10,000 |
| `user-profile-mobile-dark-segment-2` | 9,836 |
| `user-profile-mobile-light-segment-2` | 9,793 |

Ceiling is `MAX_CAPTURE_HEIGHT_PX = 16_384`. Nothing is close.

---

## 3. Manifest digest

`test_snapshot_manifest_makes_an_accidental_rebaseline_a_pytest_red` failed after regeneration
(23 passed / 1 failed). Count and file-list assertions passed; only `nameAndSizeSha256` did not.

Cause, isolated by brute-forcing the recorded size rather than assumed:

| | `volume-splitter-mobile-dark.png` |
|---|---:|
| size recorded in manifest (written 00:40:29) | **133,993 B** |
| size on disk (rewritten 00:50:13) | **134,456 B** |
| other 65 files | **all matched** |

A single capture was re-taken *after* the manifest was emitted. Both versions are 375×3144 and
structurally identical; run-to-run pixel variation is expected and absorbed by the gate
(`maxDiffPixels: 800, threshold: 0` in `e2e/visual-helpers.ts`). The stale digest was the whole
failure.

**Fix: the recorded digest only** — one line of the *local* edit sequence, `745726f2… →
5779f353…`. Contracts then pass **24/24**.

That "one line" describes the corrective edit, not the reviewable diff. `745726f2…` was an
intermediate working-tree value and was never committed, so it appears nowhere in git. **Against
`HEAD` the manifest diff is 7 insertions and 5 deletions**, all inside the two `win32` blocks, and
every one of them is mechanical:

| Line(s) | Change | Why |
|---|---|---|
| `count` | 64 → 66 | the −2 +4 segmentation |
| file list | 2 names → 4 names | same |
| `nameAndSizeSha256` (visual) | `ec36cb53…` → `5779f353…` | names and sizes both moved |
| `nameAndSizeSha256` (thumbnails) | `48e9f28e…` → `5a1c69a8…` | **all 15 thumbnails were re-captured**; the count and file list are unchanged, so only the size component moved |

The thumbnails digest is the one to check deliberately: its block looks untouched apart from the
hash. Six of those 15 captures moved −2 px (§4.2a), which changes their byte sizes, which changes
the digest. Nothing else in the file moved — `stylelintSevenSurfaces`, `surfaces`,
`screenshotTolerances` and `sourceCommit` are all byte-identical to `HEAD`, which is the positive
proof that `emit_baseline` was not used.

> ⚠️ **Do not fix this with `python -m scripts.css_audit.emit_baseline`.** That command rebuilds the
> whole baseline file: it re-pins `sourceCommit` from `46e340e5` (WP4.4-a, #187 — deliberately
> pinned, not HEAD-tracking) to the current HEAD, re-derives all seven surface metrics, and — unless
> `--stylelint artifacts/wp4_4/stylelint_surfaces.json` is passed, and that file does not exist here
> — silently drops the entire `stylelintSevenSurfaces` block. It changed **170 leaf values to fix
> one**. It was run once during this packet, reverted byte-identically from a pre-run snapshot, and
> replaced with the surgical edit.
>
> *(Reconciled 2026-08-08: this line previously read 171. The measured figure is 170, as recorded
> in `CHECKPOINT.md` §6 and in the commit message; 171 was a transcription slip here and nowhere
> else.)*

---

## 4. By-eye review

All **26 contact sheets** reviewed — 22 `visual.spec.ts` (11 pages × 2 themes) and 4
`visual-baseline-thumbnails.spec.ts`. Sheets generated by `scripts/baseline_contact_sheet.mjs`
into `artifacts/review/{win32-visual,win32-thumbs}`.

A matching **pre-regeneration** set now sits beside it in
`artifacts/review/{win32-visual-OLD,win32-thumbs-OLD}`, built by the same tool from the **79
committed** baselines at that `HEAD` — read out of the git object store, so no working copy was
involved. (79 is the *committed* count before this packet; the *working tree* during the run held
**81** = 79 + 4 new segments − 2 retired, which is the figure §6 quotes. Both are correct; they
count different sets.) 52
sheets in total, same grouping and same band geometry on both sides, which is what makes them
comparable page-by-page rather than one at a time.

**Open `artifacts/review/INDEX.html` to run the review.** It pairs all 26 before/after sheets
side by side and badges each one with the per-capture dimension delta, so a sheet that should not
have moved is visible without cross-referencing a table.

| Page | dark | light | Result |
|---|:--:|:--:|---|
| welcome | ✅ | ✅ | full render, icons present, both themes correct |
| workout-plan | ✅ | ✅ | mobile column-crush (pre-existing, see §5) |
| workout-log | ✅ | ✅ | mobile column-crush (pre-existing, see §5) |
| weekly-summary | ✅ | ✅ | incl. Movement Pattern Coverage warnings |
| session-summary | ✅ | ✅ | incl. Advanced Isolated Muscles Statistics |
| body-composition | ✅ | ✅ | **large height delta — explained, §4.1** |
| volume-splitter | ✅ | ✅ | pre-#303 state, §4.2 |
| backup | ✅ | ✅ | counts, library and detail all render |
| fatigue | ✅ | ✅ | per-muscle bars, SFR cards |
| user-profile | ✅ | ✅ | segmentation verified, §2 |
| progression | ✅ | ✅ | unchanged — the 6 that already passed in #304 |
| thumbnails: plan | ✅ | ✅ | 4 dark + 5 light; only `plan-desktop-light-simple` survives #298 |
| thumbnails: log | ✅ | ✅ | 6 captures |

**No hidden regression found.**

To separate real change from inherited staleness, every capture's dimensions were compared against
the committed version. The full per-file table is
[`DIMENSION_DELTA.md`](DIMENSION_DELTA.md); the counts are:

| `win32/visual.spec.ts-snapshots` (64 committed) | n |
|---|---:|
| dimensions changed | **18** |
| retired and replaced by segments | 2 |
| same dimensions, bytes changed | 38 |
| **byte-identical** (the 6 `progression` captures that already passed in #304) | **6** |

Of the 18 that changed dimensions, **12 moved by 2–6 px** — font/layout drift over a long-stale
corpus. The other six are the two outlier classes below.

> Withdrawn: this section previously read *"20 of 64 changed size. Sixteen moved by 2–6 px."* 20
> counted the 2 retired captures as size changes, and the 2–6 px band is 12, not 16.

The outliers:

### 4.1 body-composition (+760 px mobile) — legitimate

| Capture | Before | After | Δ |
|---|---:|---:|---:|
| `body-composition-mobile-dark` | 375×2056 | 375×2816 | **+760** |
| `body-composition-mobile-light` | 375×2054 | 375×2814 | **+760** |
| `body-composition-tablet-dark` | 768×1481 | 768×1641 | +160 |
| `body-composition-tablet-light` | 768×1479 | 768×1639 | +160 |

Cause: the page renders a **Snapshot History** section with three seeded records (2026-03-03,
2026-02-03, 2026-01-06). On mobile each record stacks as a full card; on tablet it is a 3-row table;
on desktop it already fit — and **desktop did not change size at all**, which is exactly the
signature of "same data, narrower viewport" rather than a layout regression.

The win32 baselines for this page were last committed in **#48**
(`728fb65 test(visual): add {platform} segment to snapshotPathTemplate`). They simply predate this
content. This is the inherited staleness #304 describes, not a defect.

### 4.1a user-profile grew too — the second outlier class, same signature

`user-profile` grew on every viewport narrower than desktop.

| Capture | Before | After | Δ |
|---|---:|---:|---:|
| `user-profile-mobile-dark` (retired) → `segment-1` + `segment-2` | 375×19785 | 375×(10000+9836) = 19,836 | **+51** |
| `user-profile-mobile-light` (retired) → `segment-1` + `segment-2` | 375×19742 | 375×(10000+9793) = 19,793 | **+51** |
| `user-profile-tablet-dark` | 768×9602 | 768×9636 | +34 |
| `user-profile-tablet-light` | 768×9590 | 768×9624 | +34 |
| `user-profile-desktop-{dark,light}` | 1440×6160 / 1440×6150 | **same dimensions** | 0 |

Desktop bytes did move (+72 KB each) — it is the *dimensions* that are unchanged, which is the part
that carries the reflow signal.

Segment heights sum to the whole document height — the last segment is the remainder, not a padded
band — so `10000 + 9836` is directly comparable to the retired 19,785.

Same signature as §4.1: **desktop is unmoved, narrower viewports grow, and the growth is
proportionate to the reflow**, which is content that predates the baseline rather than a layout
regression. The user-profile contact sheets show no truncation, no unpainted tail and no collapsed
section in either theme.

### 4.2a thumbnails — 6 of 15 moved −2 px

`visual-baseline-thumbnails.spec.ts-snapshots` was outside the "of 64" accounting entirely. Six
captures moved −2 px (`log-mobile-{dark,light}`, `plan-mobile-{dark,light}-{advanced,simple}`); the
other nine kept their dimensions. This is the same 2-px drift as §4's 12, and it is the reason the
thumbnails `nameAndSizeSha256` moved despite an unchanged count and file list (§3).

### 4.2 volume-splitter is captured in its pre-#303 state — deliberately

> **SUPERSEDED 2026-08-08 — these six captures are NOT in the integrated corpus.** The reasoning
> below was correct for `main` as it stood when written. #303 has since merged (`42e8a4d`) and
> shipped its own post-fix win32 captures, so keeping these would have re-blessed the OD-2 defect
> as the baseline. At integration the six were resolved to `main`'s post-fix versions and the six
> described here were discarded. See §8.

Both `Distribution` (with live **Export Volume Plan** / **Save & Activate**) and **AI Suggestions**
are visible on first paint with no split calculated. That is the **OD-2 defect PR #303 fixes**, and
capturing it here is correct: `static/css/bootstrap.custom.min.css` is byte-identical to
`origin/main` and still contains no `utilities/api` import, so these six captures record current
`main`.

> The only render source that differs from `origin/main` at all is `static/css/layout.css`, which
> still carries the 47 `.tbl-show-*`/`.tbl-hide-*` lines #300 deleted. Those classes appear in no
> template, module, route or util — only in CSS and two contract-test docstrings — so they cannot
> move a pixel. The corpus is valid for current `main`; see [`CHECKPOINT.md`](CHECKPOINT.md) §7.

> **MEASURED 2026-08-08 — the prediction below does not hold; the blast radius is exactly six.**
> The demand for measurement was right, and the measurement was taken: whole-corpus differentials
> moved **exactly six** captures on win32 and **exactly six of 81** on linux, and a computed-style
> probe found **0 differences across 5,179 elements** at 1440 px. The two navbar spans do change
> computed `display` below 992 px, but they measure `0x0 at (0,0)` in **either** state because
> `nav.navbar-collapse:not(.show)` is `display: none` (`static/css/navbar.css:704`). Full figures
> in §8. Retained below as the dated prediction it was.

**#303's blast radius is wider than these six, and must be measured rather than assumed.** It emits
the `display` utility for the values `none inline`, which activates **both** halves of the
`class="d-none d-lg-inline"` pair at `templates/base.html:213,219` — a navbar element on *every*
page. Below the `lg` breakpoint those two labels start hiding, so mobile and tablet captures across
all 11 pages are candidates, not just volume-splitter's six. #303's own scss note measures the
*wider* variant (adding `d-flex`/`d-inline-block`) at 18 of 66 captures and deliberately excludes
it; it does not measure the `none inline` set that ships.

What still holds is the sequencing argument: landing this packet first means #303's delta lands on a
corpus that is no longer stale, so whatever it moves is reviewable as its own change.

---

## 5. Pre-existing characteristics accepted, not fixed

Recorded so a future reader does not mistake them for regressions introduced here:

- **Mobile column-crush** on `/workout_plan` and `/workout_log` at 375 px — wide tables force
  one-character-per-line cells and some label/button overlap. Those captures moved by **−2 px**,
  so this is unchanged from the previous baseline.
- **`workout-plan` tablet captures are 835 px wide, not 768** — horizontal overflow from the same
  wide table. Also pre-existing.
- **Blank-looking rows** in the mobile "Exercise Categories Summary" on both summary pages. The data
  renders correctly at tablet/desktop; those captures moved −6 px, so unchanged.
- **`/fatigue` period `<select>` spans the full width** — the inert `.d-inline-block` recorded in
  #303's `KNOWN_INERT`, still inert by design.
- **No `workout-plan` desktop capture in the dark thumbnail sheet** — #298 took five plan-desktop
  captures off the byte gate; `plan-desktop-light-simple` is the only survivor.

None of these were "fixed" here. Changing them is a rendering decision with its own baseline review.

---

## 6. What this does NOT cover

- **Windows only.** The linux corpus is untouched.
- **No tolerance was raised**, and no snapshot was resolved with `--update-snapshots`.
- The `58 failed / 8 passed` figure in #304 was measured at `02e73c7`. This packet does not re-run
  that measurement; it replaces the corpus that produced it. The **post**-regeneration counterpart
  has now been measured — see §7.
- **The two WP4.0 "known Windows reds" are not fixed here.** Both suites are fully green (§7), but
  `workout-plan desktop dark` and `plan-desktop-light-advanced` pass because #298 put them in
  `BYTE_GATE_EXEMPT` (`e2e/visual-helpers.ts:49`) — they are still rendered and asserted, but no
  longer byte-compared. Green here is silence on those two defects, not a claim about them.

---

## 7. Gate results

| Gate | Result |
|---|---|
| `e2e/visual.spec.ts` win32, `PW_VISUAL_SEED=1` | **66 passed** (was 58 failed / 8 passed) |
| `e2e/visual-baseline-thumbnails.spec.ts` win32 | **18 passed**, zero serial-mode skips |
| `tests/test_visual_capture_contracts.py` + `tests/test_css_wp4_4_a_baseline_contracts.py` | **24 passed** |
| Full `pytest tests/` | **2527 passed, 2 skipped** (the two reds in §7.2 were the tool's path, now resolved) |
| Oversized-baseline carve-out | empty and verified against measured heights |
| Contact-sheet review | **52 sheets** — 26 new + 26 pre-regeneration, no hidden regression |
| Dimension diff vs committed | 18 changed + 2 retired of 64; all explained (§4, `DIMENSION_DELTA.md`) |
| On disk vs contract | **162 = 162** |
| Baselines written by the verification run | **none** — status stayed 71 M / 2 D / 4 ?? across both suites |

### 7.1 The suite result, stated carefully

`e2e/visual.spec.ts` was run against this corpus with `PW_VISUAL_SEED=1`, no
`--update-snapshots`, no `PW_REUSE_SERVER`, on a Playwright-started server bound to this worktree's
own database: **66 passed**. The same 66 tests on the same tree with the previous corpus were
**58 failed / 8 passed** (#304).

Contact sheets establish that the new pixels are *correct*; they cannot establish that the committed
corpus is *self-consistent* with what the app renders. Only the suite does, and a stale corpus is
precisely the failure mode that a by-eye review of the new pixels alone would not catch.

Two properties were checked immediately afterwards, because a passing visual run is not by itself
proof that nothing was written:

- `git status --porcelain e2e/__screenshots__` was **byte-for-byte the same before and after** —
  71 modified, 2 deleted, 4 untracked. Playwright auto-creates a missing baseline instead of
  failing, so an unnoticed addition would show up only here.
- A SHA-256 manifest of all 81 win32 PNGs, taken before the run, re-verified **clean afterwards**.

**Tracked = on disk = contract-expected = 162**, all three, once this packet is committed. Before
the commit only 160 were tracked — the 4 segment files untracked and the 2 deletions unstaged — so a
"162 = 162" measured against the working tree is not evidence about what a fresh clone would get.

### 7.2 The contact-sheet tool lives in `scripts/`, not `scripts/css_audit/`

The first draft of this tool was written to `scripts/css_audit/`, which red two tests that the
narrow contract run never touches:

```
FAILED tests/test_css_theme_dark_p3_audit_contracts.py::test_every_committed_css_audit_tool_is_assessed
FAILED tests/test_css_theme_dark_p3_audit_contracts.py::test_every_committed_css_audit_tool_is_assessed_red_path
```

`scripts/css_audit/p3_ceiling.py::TOOL_ASSESSMENT` carries a curated verdict for each tool in that
directory and the contract asserts the listing and the list agree. The new file was the 20th against
19 verdicts. The check scans the **directory**, not the index, so it red while the file was still
untracked — it did not wait for a commit.

**Resolved by moving the tool to `scripts/baseline_contact_sheet.mjs`**, which is where it belonged:
it composes PNGs for a human to look at and has nothing to do with cascade auditing, the same
reasoning that already puts `scripts/stylelint-report.mjs` at the `scripts/` root. The alternative —
adding a `TOOL_ASSESSMENT` entry — would have written a verdict into the theme-dark P3 arc's curated
ledger and formally added this tool to what P3-a1 is priced off, which is the scope-widening that
gate exists to prevent.

After the move: `coverageComplete: True`, `unassessed: []`, and the full suite is **2527 passed**.

**Lesson for the next packet: run the full suite, not just the contracts you edited.** A narrow run
of the two files this packet touches reports 24/24 and hides a red caused by a file the packet
added.

---

## 8. Integration onto current `origin/main` (2026-08-08)

Everything above describes the corpus as generated on 2026-08-05 against `001b166`.
This section records how it was integrated onto `origin/main` at `99e172d`, what
changed in the process, and the results measured on the **final resolved tree**.
Where the two disagree, this section is current.

### 8.1 What changed relative to the packet as committed at `b990412`

| | |
|---|---|
| Base | fresh branch from `origin/main` @ `99e172d` |
| Method | **merge** of `b990412` (not rebase), as CHECKPOINT §4 prescribed |
| Conflicts | **7 files** — the manifest plus the six `volume-splitter-*` win32 captures |
| Resolution | the six resolved to **`main`'s post-#303 captures**; this packet's pre-#303 six **discarded** (§4.2 is superseded) |
| Net changed files vs `99e172d` | **78** — 71 PNGs + 7 text files |

The 15 win32 thumbnail baselines regenerated by this packet **are** included; the
linux corpora are **untouched**, byte-for-byte, on both entries.

### 8.2 The compare-mode run — the check that makes this safe

Run on the merged tree **before** anything was committed, and **without**
`--update-snapshots`:

```
PW_VISUAL_SEED=1 npx playwright test e2e/visual.spec.ts e2e/visual-baseline-thumbnails.spec.ts --project=chromium --reporter=line
```

| | |
|---|---|
| Result | **84 passed** (66 + 18) in 2.0 min |
| Port | 5000, verified free; no `PW_REUSE_SERVER` |
| Baselines written | **zero** — SHA-256 of all 81 win32 PNGs byte-identical before and after |
| Untracked afterwards | none |

This is what converts "71 of these captures were generated two CSS commits behind"
from an inference into a measurement. Had any been stale for the current tree, the
comparison would have red and named the capture.

For contrast, issue #304 measured **58 failed / 8 passed** of the same 66 on the
pre-regeneration corpus.

### 8.3 Final counts and manifest

Tracked = on disk = contract = **162** (win32 66 + 15, linux 66 + 15).

| manifest entry | count | `nameAndSizeSha256` |
|---|---:|---|
| `win32/visual.spec.ts-snapshots` | 64 -> **66** | `64fc91cb...` -> `830bcdd5...` |
| `win32/visual-baseline-thumbnails.spec.ts-snapshots` | 15 | `48e9f28e...` -> `5a1c69a8...` |
| `linux/visual.spec.ts-snapshots` | 66 | `e509191c...` **unchanged** |
| `linux/visual-baseline-thumbnails.spec.ts-snapshots` | 15 | `25a67f05...` **unchanged** |

Recomputed by hand from the final tree. **`emit_baseline` was not run** — see the
warning in §3, which still stands.

The win32 visual digest is **not** this packet's `5779f353...`. That value described
a corpus containing the pre-#303 volume-splitter six, which are no longer in it.

### 8.4 Contact sheets regenerated for owner review

The by-eye pass recorded in §4 was performed by the authoring agent, against the
2026-08-05 corpus, and is **explicitly not owner sign-off**. Fresh sheets were
generated from the final resolved tree:

| set | sheets | baselines |
|---|---:|---:|
| `artifacts/review_final/win32-visual/` | 22 | 66 |
| `artifacts/review_final/win32-thumbnails/` | 4 | 15 |

26 sheets over 81 baselines. `artifacts/` is gitignored, so these are review
material and are not committed.

**Owner by-eye approval of the regenerated pixels remains the open gate.** Note in
particular that the largest byte deltas in this corpus sit on captures whose
*dimensions did not change* — `user-profile-desktop-{dark,light}` at roughly +72 KB
each and `user-profile-tablet-*` at roughly +171 KB each. Nothing accounts for what
moved inside those frames except the sheets, so they deserve the closest look.
