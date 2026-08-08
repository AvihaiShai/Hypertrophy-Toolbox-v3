# Preservation and sync plan — win32 visual baseline recovery (#304)

Read this first if you are picking the work up.

---

## 1. What is at risk, precisely

> **SUPERSEDED 2026-08-08.** This section described the packet before it was committed, and §3/§7
> already contradicted it. The work was committed on `fix/win32-visual-baseline-regen` as
> **`b990412`** (84 files), and has since been integrated onto current `origin/main` — see §8.
> Retained as the dated record of the at-risk window, **not** as current state.

*As written:* the packet existed **entirely as uncommitted working-tree state** in
`D:/development/HT-v3-winregen`; `git diff origin/main...HEAD` was empty, the branch had no commits
of its own, was not pushed, and its `HEAD` (`001b166`) was a plain ancestor of `origin/main`.

82 working-tree entries, plus 70 gitignored files under `artifacts/review/` that no git operation
can recover.

| Asset | Recoverable from git? | Cost to recreate |
|---|---|---|
| 71 modified + 2 deleted win32 PNGs — **old** bytes | **yes**, `git show HEAD:<path>` | free |
| 71 modified win32 PNGs — **new** bytes | **no** | a full local `PW_VISUAL_SEED=1` run |
| 4 untracked `-segment-N.png` | **no** | same run |
| `EVIDENCE.md`, `DIMENSION_DELTA.md`, this file | **no** | rewriting them |
| `scripts/baseline_contact_sheet.mjs` | **no** | re-authoring the tool |
| 3 tracked text edits (manifest + 2 contracts) | **no**, but trivially redone | minutes |
| `artifacts/review/**` — 52 contact sheets + `INDEX.html` | **no** (gitignored) | ~6 min of Chromium compositing |
| **the by-eye review itself** | **no** | **a human re-reviewing 52 sheets** |

Aggravating context: this repository currently has **~50 live worktrees** sharing one object store,
and concurrent sessions operate in the main checkout. A stray `git checkout -- .`, `git stash`,
`git clean -fdx` or `git add -A` from any of them, run in or against this directory, ends the packet.

## 2. The checkpoint that exists now

First taken 2026-08-08 **before** any sync, merge, or regeneration; refreshed as this packet's own
documents and review artifacts grew.

Durable copy, verified 158/158 and safe across a reboot — **use this one**:
`D:/development/_winregen-checkpoint-20260808/` (outside every repo, so no git operation in any
worktree can reach it). The session scratchpad holds an identical copy that Storage Sense may clear.

```
D:/development/_winregen-checkpoint-20260808/
  tree/              158 files, byte-exact copies, original relative paths
  SHA256SUMS.txt     158 lines, sha256 per file
  git-status.txt     the 82-entry porcelain status it was taken against
  head.txt           001b166
  diff-stat.txt      the working-tree diff stat
  text-diff.patch    the three tracked text edits, applyable standalone
```

Coverage — 158 = 81 + 70 + 3 + 4:

| | n |
|---|---:|
| win32 PNGs on disk (both snapshot dirs) | 81 |
| `artifacts/review/**` — 52 sheets, 4 `sheets.json`, `INDEX.html`, 13 legacy partial sheets | 70 |
| tracked text edits — manifest + 2 contracts | 3 |
| `EVIDENCE.md`, `CHECKPOINT.md`, `DIMENSION_DELTA.md`, `baseline_contact_sheet.mjs` | 4 |

`sha256sum -c SHA256SUMS.txt` against the live worktree returns **158/158 OK**.

Re-verify after anything that touches the tree. Two intermediate re-verifications already caught
what they should have: after both visual suites, all 81 PNGs were unchanged and only the two files
deliberately edited failed the check.

Restore is a plain copy back over the worktree — nothing to unwind, no git state involved:

```bash
cd D:/development/HT-v3-winregen
cp -a <checkpoint>/tree/. .
sha256sum -c <checkpoint>/SHA256SUMS.txt   # expect 158 OK
```

This checkpoint lives in a session scratchpad, which is **not durable storage**. It removes the
risk of losing the work to a stray command today; it does not replace a commit.

## 2a. Cleared: the contact-sheet tool's path

The contact-sheet tool started in `scripts/css_audit/`, where it was the 20th entry in a directory
whose 19 tools are enumerated by `scripts/css_audit/p3_ceiling.py::TOOL_ASSESSMENT`, and red two
tests in `test_css_theme_dark_p3_audit_contracts.py`. Moved to `scripts/baseline_contact_sheet.mjs`;
`coverageComplete` is `True` again. Detail in [`EVIDENCE.md`](EVIDENCE.md) §7.2.

**Run the full suite before committing, not just the contracts you edited** — the narrow run reports
24/24 and hides this class of red entirely.

## 3. Commit — DONE

The packet is committed. Recorded here because the staging is the part that goes wrong, and a
future regeneration on this branch has to repeat it.

**Commit before syncing** — a merge into a dirty tree carrying 73 binary changes is where things get
lost. The exact staging matters: `git add -u` and `git commit -a` stage tracked
modifications and deletions but **never** untracked files, so both take the 2 deletions and none of
the 4 additions. That commits a **62**-file corpus against a contract expecting 66: an instant red
on a fresh clone, and one that does not reproduce in the worktree where the files still exist.

```bash
cd D:/development/HT-v3-winregen
git add e2e/__screenshots__/win32                     # picks up M, D and the 4 untracked segments
git add docs/CSS_PHASE4_WP4_4_A_BASELINE.json \
        tests/test_css_wp4_4_a_baseline_contracts.py \
        tests/test_visual_capture_contracts.py \
        docs/visual_baseline_win32 \
        scripts/baseline_contact_sheet.mjs
git status --porcelain -uall                          # expect 84 staged, 0 unstaged, 0 untracked
git diff --cached --stat -- . ':(exclude)e2e/__screenshots__'   # expect exactly 7 text files
```

Never `git add -A` here — other worktrees share this checkout.

## 4. Sync plan, in order

**Do not start this while #303 is unfinished.** #303 rebuilds `static/css/bootstrap.custom.min.css`
so that `.d-none` actually hides; it will move pixels on every page carrying a `.d-none` element on
first paint. Regenerating before it lands means regenerating twice and reviewing twice.

1. ~~**Commit** (§3).~~ **Done.** Everything below assumes a clean tree.
2. **Merge, do not rebase.** `git merge origin/main`. The branch is unpushed today, but a merge
   keeps the packet reviewable as one reviewed corpus rather than replaying 73 binary changes onto a
   moving base. Expect **no conflicts**: `origin/main`'s three unmerged commits touch
   `docs/MASTER_HANDOVER.md`, `docs/css_table_helpers_cleanup/**`, `docs/test_inventory/**`,
   `static/css/layout.css` and `tests/test_css_wp4_4_layout_contracts.py` — **disjoint from every
   path this packet touches**.
3. **Re-verify the checkpoint after the merge** — `sha256sum -c` again. A merge must not have
   touched a single PNG. If any hash moved, stop.
4. **Scope the regeneration from the diff, not from a full re-run.** Re-derive which pages the
   merged source can actually move, and regenerate only those. Anything else stays as reviewed.
   For #303 specifically, do **not** take "the six volume-splitter captures" on faith: it emits the
   `display` utility for `none inline`, which activates both halves of `class="d-none d-lg-inline"`
   at `templates/base.html:213,219` — a navbar element on every page — so mobile and tablet across
   all 11 pages are candidates. Measure the moved set; do not predict it.
5. **Regenerate**, `PW_VISUAL_SEED=1`, worktree-private DB, serialized against other worktrees —
   see §5.
6. **Check `git status --porcelain e2e/__screenshots__` immediately afterwards.** Playwright
   *creates* a missing baseline instead of failing, so a silently added file shows up only here.
7. **Rebuild the contact sheets for the regenerated pages** and diff them against the `-OLD` sheets.
8. **Regenerate the manifest digest surgically** — see §6.
9. **Pause for owner by-eye approval.** Do not finalize on green contracts alone — open
   `artifacts/review/INDEX.html`, which pairs all 26 before/after sheets side by side with the
   per-capture dimension deltas badged on each.

## 5. Running the gate safely

- `PW_VISUAL_SEED=1` is mandatory. Without it the run seeds via `prepare_e2e_db.py` — the
  user-state-wiped functional seed — and reds dozens of tests for reasons that have nothing to do
  with the baselines.
- **Never `PW_REUSE_SERVER=1`.** It silently certifies against whichever worktree already holds the
  port, i.e. against another checkout's CSS. `runtime_probe.mjs` hard-codes port 5000, so this is a
  live hazard here, not a theoretical one.
- Use this worktree's own `data/database.db`. One DB per checkout; do not point `DB_FILE` at
  another worktree's file even read-only.
- If port 5000 is held, run through a scratch config overriding **only** the port.

## 6. Hard prohibitions

- **Never raise `maxDiffPixels` (800) or `threshold` (0)**, add a mask, raise `retries`, or add a
  name to `BYTE_GATE_EXEMPT`. If a capture reds, the answer is a reviewed rebaseline or a defect
  fix, never a wider gate.
- **Never resolve a red with `--update-snapshots`** as a reflex. Regeneration here is a deliberate,
  reviewed act on a corpus already established as stale by two identical control runs in #304.
- **Never fix a manifest-digest red with `python -m scripts.css_audit.emit_baseline`.** It re-pins
  `sourceCommit` off its deliberate `46e340e5` anchor, re-derives all seven surface metrics, and
  silently drops the entire `stylelintSevenSurfaces` block — its `--stylelint` default already
  points at `artifacts/wp4_4/stylelint_surfaces.json`, which does not exist here, so passing the flag
  explicitly changes nothing. Measured: **170 leaf values move to fix one**, and `snapshotManifest`
  — the only block you wanted — comes out identical. Edit the one digest by hand.
- **Never `git add -A`**, `git reset --hard`, `git clean`, `git stash` broadly, or force-push. Other
  worktrees share this checkout, and the guard hook blocks several of these for that reason.

## 7. State as of 2026-08-08

| | |
|---|---|
| Branch | `fix/win32-visual-baseline-regen`, **unpushed**, 1 commit — the packet |
| `HEAD` | the packet commit, on a base 3 commits behind `origin/main` (`b6550e6`, `88b634c`, `4025295`) |
| Working tree | **clean** — all 84 files committed (71 M + 2 D + 4 A PNGs, 3 text edits, 3 new docs, 1 moved tool) |
| Tracked corpus | win32 **66 + 15**, linux 66 + 15 — tracked = on disk = contract = **162** |
| Checkpoint | **158/158** verified, re-verified after the visual runs and after the commit |
| Contact sheets | **52** — 26 new + 26 `-OLD`, the old set rebuilt from `HEAD` blobs for side-by-side review |
| Visual suites | `visual.spec.ts` **66 passed**, `visual-baseline-thumbnails.spec.ts` **18 passed**, zero baselines written |
| Blocked on | *(resolved — #303 merged as `42e8a4d`; see §8)* |
| Full pytest | **2 failed / 2525 passed / 2 skipped as measured at this point**, both failures the §2a tool-path reds. After §2a was resolved by moving the tool the same suite read **2527 passed / 2 skipped** (EVIDENCE §7). The two rows are the same suite before and after that fix, not a disagreement. |
| Merge conflict risk | *(superseded — `origin/main` has moved well past those three commits; the realised conflict was 7 files, see §8)* |
| Pixel risk from the merge | *(superseded by measurement — see §8)* |

---

## 8. Integration onto current `origin/main` (2026-08-08)

The packet was integrated by **merge**, not rebase, onto a fresh branch from
`origin/main` at `99e172d`. Owner-authorised. The sequencing this document
anticipated — "do not start this while #303 is unfinished" — is resolved: #303
merged as `42e8a4d`, and its Linux counterpart as `99e172d` (#308).

**The realised conflict was 7 files**, not zero: `docs/CSS_PHASE4_WP4_4_A_BASELINE.json`
plus the six `volume-splitter-*` win32 captures.

**Resolution: main's six volume-splitter captures win.** This packet captured
`/volume_splitter` in its **pre-#303** state deliberately (EVIDENCE §4.2), which was
correct for `main` at the time. It is not correct now: #303 shipped, and its own
regenerated win32 captures are on `main`. Taking this packet's six would have
re-blessed the OD-2 defect as the baseline. They were resolved to `--ours` (main's,
post-fix) and this packet's six discarded.

**The EVIDENCE prediction about #303 is now measured, and it does not hold.** It
warned that "#303's blast radius is wider than these six, and must be measured
rather than assumed", reasoning that `class="d-none d-lg-inline"` is a navbar
element on every page, so mobile and tablet across all 11 pages were candidates.
Measured during #303, on both platforms:

- Computed `display` + geometry, pre-fix bundle vs shipped bundle: `/workout_plan`
  at 1440 px, **5,179 elements, 0 differences**; `/workout_log` 603, **0**;
  `/weekly_summary` 514, **0**.
- At 768 and 375 exactly **two** elements change computed `display` — the two label
  spans — and both measure **0x0 at (0,0) in either state**, because
  `nav.navbar-collapse:not(.show)` is `display: none` below the breakpoint
  (`static/css/navbar.css:704`). Bootstrap's `collapse` component is not compiled
  into this build, so that hand-written rule is what governs. They are unpainted
  either way.
- Whole-corpus hash differentials moved **exactly six** captures on win32 and
  **exactly six of 81** on linux.

So the blast radius is the six volume-splitter captures, and the other 71 win32
baselines in this packet are unaffected by #303. The warning was right to demand
measurement; the measurement returned a smaller number than it predicted.

**Self-validating check, and the reason this integration is safe.** The merged
corpus was run in **compare mode, without `--update-snapshots`**:

```
PW_VISUAL_SEED=1 npx playwright test e2e/visual.spec.ts e2e/visual-baseline-thumbnails.spec.ts --project=chromium --reporter=line
```

**84 passed** (66 + 18) in 2.0 minutes, on port 5000, with no `PW_REUSE_SERVER`. A
SHA-256 manifest of all 81 win32 PNGs taken before and after the run is
**byte-identical**, and `git status --porcelain e2e/__screenshots__` shows nothing
untracked, so the run wrote no baseline. That converts "these 71 captures were
generated two CSS commits behind" from an inference into a measurement: had any been
stale for the current tree, it would have red and named itself.

**Manifest.** Recomputed by hand from the final tree; `emit_baseline` was **not**
run. Two win32 entries move, both linux entries are byte-unchanged:

| entry | count | `nameAndSizeSha256` |
|---|---:|---|
| `win32/visual.spec.ts-snapshots` | 64 -> **66** | `64fc91cb...` -> `830bcdd5...` |
| `win32/visual-baseline-thumbnails.spec.ts-snapshots` | 15 | `48e9f28e...` -> `5a1c69a8...` |
| `linux/visual.spec.ts-snapshots` | 66 | `e509191c...` **unchanged** |
| `linux/visual-baseline-thumbnails.spec.ts-snapshots` | 15 | `25a67f05...` **unchanged** |

The win32 visual digest is **not** this packet's `5779f353...`: that value described
a corpus still holding the pre-#303 volume-splitter six.

**Contact sheets were regenerated from the final resolved tree** — 26 sheets, 22 for
`visual.spec.ts` and 4 for `visual-baseline-thumbnails.spec.ts`, under
`artifacts/review_final/`. The earlier by-eye pass recorded in §4 of EVIDENCE was
performed by the authoring agent and is **not** owner sign-off; owner approval of the
regenerated pixels remains the open gate.
