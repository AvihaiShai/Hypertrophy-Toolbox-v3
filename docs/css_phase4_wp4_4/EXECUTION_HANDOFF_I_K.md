# WP4.4 i–k execution handoff

This is the volatile restart ledger for
[`N4_CONTINUATION_AUTHORITY.md`](N4_CONTINUATION_AUTHORITY.md). Update it after every
material gate result, PR transition, merge/rebase and before ending a session. Evidence
filenames never establish provenance; the served checkout, commit and content digest do.

## Snapshot — 2026-07-31 23:30 +03:00

| Field | Current value |
|---|---|
| Active packet | WP4.4-i **corrective** (C13, in-scope); packet i itself is merged |
| Main / origin/main | `09bf9a0` — contains PR #212 (packet i, merged by the owner) and PR #213 (authority/status sync) |
| Main dirty paths | owner `CLAUDE.md` only — never stage, stash, discard or copy it |
| Branch | `wt/wp4-4-i-oracle-provenance` |
| Worktree | `D:/development/Hypertrophy-Toolbox-v3-main-wp4-4-i-is-repair` |
| HEAD / parent | `09bf9a0` (tracking `origin/main`); corrective uncommitted |
| Worktree status | dirty by intent: 4 audit scripts, 2 test files, 1 evidence doc, this file, + 2 new scripts |
| Remote / PR | no remote branch; corrective PR not yet opened |
| i CSS SHA (unchanged by the corrective) | `0702558b…c6f0e5` |
| Pristine pre-i CSS SHA | `883e6aa8…107964` (available at `1019d34`) |
| Second checkout used for before-halves | `D:/development/Hypertrophy-Toolbox-v3-main-wp4-4-j` @ `1019d34`, restored clean after each use |
| True blocker | none |

**No production CSS changes in this corrective.** `static/css/components.css` is untouched at
`0702558b…`; the corrective repairs oracles, contracts and evidence only.

## Corrective gate results — all from the post-#212 tree

| Gate | Result | Artifact under `artifacts/wp4_4/i/` |
|---|---|---|
| Full pytest | **2289 passed, 1 skipped** (was 2,287; corrective adds 2 contracts) | `r3-pytest-full.txt` |
| Cascade + components + packet contracts | **47 passed** | — |
| Computed differential `883e6aa8` → `0702558b` | **0 differences / 758,400 values** | `r3-diff-computed/diff.json` |
| Cross-run same-CSS control | **0 differences** | `r3-diff-samecss/diff.json` |
| Known-live control | **8,856** (session 4,578 · weekly 4,278; dark 5,688 · light 3,168) | `r3-knownlive-diff/diff.json` |
| G3 regions A–C, two different roots | **0 resurrections, 0 drift, 0 provenance failures** | `r3-g3-diff/diff.json` |
| Element-scoped pixel differential | 29/30 byte-identical; the 30th differs **identically** in the same-CSS control → 0 packet pixels | `r3-pixel/`, `r3-pixel-control/` |
| Stylelint, matched 21-source glob | `no-descending-specificity` 194→204 (+10), all on approved lines; every other category flat | `r3-stylelint-{before,after}.json` |
| Windows visual matrix | **36 failed / 30 passed on both halves, identities exactly equal**; 0 new, 0 cleared, no snapshot changed | `r3-visual-{before,after}.json` |

### What the corrective actually fixes

1. **G3 was unfalsifiable.** `n4_regions_abc.mjs` recorded only `pages-workout-log.css`,
   which no admissible repair touches, so both halves were byte-indistinguishable and
   `i_diff_g3.mjs` printed a full PASS when handed the same summary twice. Both now carry
   identity and refusal logic, and `--root` lets the before half come from a real second
   checkout instead of an in-place swap.
2. **The known-live control was unreproducible.** 8,856 was a real number from a scratch hand
   edit that exists nowhere in git. `i_known_live_mutation.mjs` now regenerates it
   deterministically (`883e6aa8…` → `9326fc63…`) and reproduces **8,856 exactly**.
3. **The evidence quoted two different mutations as one.** §3's table was the unguarded
   8,784 run; §9 quoted the guarded 8,856 run. Now a single reproducible run throughout.
4. **Stylelint's halves were run over different file sets** (21 sources vs 19), which
   inflated run-wide `no-descending-specificity` to 473→638. Matched, it is 473→483.
5. **The pixel differential belonged to PR #211.** `i_element_pixel_diff.mjs` is i's own,
   with a same-CSS determinism control.

## Checkpoint contents

The WIP snapshot `8dc358b` was superseded in place by the real packet commit
`232d6b5` (`git reset HEAD~1` then a scoped recommit; the reflog retains both).
The two trees differ only in `docs/CSS_PHASE4_WP4_4_I_IS_REPAIR_EVIDENCE.md`
(+61/−57) — no production, script or test content was lost.

`232d6b5` changes exactly these nine paths relative to current main:

- `static/css/components.css`
- `docs/CSS_PHASE4_WP4_4_I_IS_REPAIR_EVIDENCE.md`
- `scripts/css_audit/i_diff_computed.mjs`
- `scripts/css_audit/i_diff_g3.mjs`
- `scripts/css_audit/i_five_route_computed.mjs`
- `scripts/css_audit/i_seed_probe_db.py`
- `tests/test_css_cascade_contracts.py`
- `tests/test_css_wp4_4_components_contracts.py`
- `tests/test_css_wp4_4_i_is_repair_contracts.py`

Do not reset or discard it. The obsolete visual-helper worktree/branch must not be
resumed; PR #211 is already squash-merged on main.

## Fresh post-#211 evidence already observed

- Computed differential `r2-before` (main `883e6aa8…`) versus `r2-after` (i
  `0702558b…`): same DB `5bc6d34…`, 60 contexts, 15,168 elements, 758,400 values,
  **0 computed differences and 0 structural drift**.
- G3 runs currently named `r2-g3-before` and `r2-g3-after` report 56,304 records,
  45 declarations and 0 resurrection/ownership drift. The former contains the pristine
  four-branch owner selectors; the latter contains the i split selector. The current
  `n4_regions_abc.mjs` output does not itself record checkout root or served components
  digest, so final evidence must record the invocation/root and a distinguishing served
  identity; names alone are insufficient.
- Post-merge summary known-live control: **8,856 changes** (Session 4,578; Weekly
  4,278). This supersedes the stale 8,784 figure in the WIP evidence.

## Known stale WIP evidence

Before presenting Packet i as complete, correct
`docs/CSS_PHASE4_WP4_4_I_IS_REPAIR_EVIDENCE.md`:

- base `89523ed` is stale; the effective base is `1019d34`;
- “verification complete” is premature until the fresh gates finish;
- 8,784 known-live changes is stale; the post-#211 run measured 8,856;
- the old class-based `.table-calm` harness-exclusion narrative is superseded by PR #211's
  inert `data-visual-preserve-border` hook and property-level Rule A/Rule B split;
- all final commands/results must cite post-#211 roots, served digests and DB digest;
- any pre-#211 or misleadingly labeled artifacts are historical diagnostics only.

## Exact resume sequence

1. Read the authority and this handoff, fetch origin, and re-audit process/port state.
2. Inspect the prepared main-checkout diff. Stage **only** these seven paths and create/
   merge the docs-only authority/status PR; never stage `CLAUDE.md`:
   `docs/ACTIVE_DEVELOPMENT.md`, `docs/MASTER_HANDOVER.md`,
   `docs/REFACTOR_PLAN.md`, `docs/css_phase4_wp4_4/PLANNING.md`, this file,
   `N4_CONTINUATION_AUTHORITY.md`, and `OPUS_CONTINUATION_PROMPT.md`.
3. Rebase i onto that docs-only merge. Apply C16: retain fresh results only when every
   measured code/test/harness/script/DB digest is unchanged and provenance is complete.
4. Check processes again. Recover the completed pytest result if it is durably available;
   otherwise rerun it serially. Do not overlap DB/server/Playwright/oracle jobs or kill one
   blindly.
5. Verify i has HEAD `232d6b5` or a documented descendant, the authority merge as its
   base or ancestor, clean status, intended nine-path scope, the PR #211 hook, and served
   CSS `0702558b…`.
6. Establish true G3 before from pristine current main and true after from final i. Enhance
   metadata or record the commands/root/digests so provenance is machine-checkable.
7. Finish the remaining serialized i gates from the stable post-#211 tree.
8. Reconcile the evidence and contracts, commit intentionally, push/open i PR, monitor CI
   and merge only under the authority gates.
9. Update this file after i's PR/merge; arrange j from newly merged main through the
   external worktree workflow. Managers/subagents do not create or move worktrees.

## Update template

```markdown
### <timestamp> — <packet/milestone>
- main / packet base / head / served CSS:
- branch / worktree / PR / CI:
- dirty paths and running jobs:
- commands and exact results:
- inherited reds/bands and same-state controls:
- artifact roots + DB/CSS digests:
- next exact action:
- genuine blocker (or `none`):
```
