# WP4.4 i–k execution handoff

This is the volatile restart ledger for
[`N4_CONTINUATION_AUTHORITY.md`](N4_CONTINUATION_AUTHORITY.md). Update it after every
material gate result, PR transition, merge/rebase and before ending a session. Evidence
filenames never establish provenance; the served checkout, commit and content digest do.

## Snapshot — 2026-07-31 17:57 +03:00

| Field | Current value |
|---|---|
| Active packet | WP4.4-i |
| Main / origin/main | `1019d34` — PR #211 merged; authority/status sync is prepared locally but not committed |
| Main dirty paths | owner `CLAUDE.md` plus seven intentional authority/status docs; never stage `CLAUDE.md` |
| Branch | `wt/wp4-4-i-is-repair` |
| Worktree | `D:/development/Hypertrophy-Toolbox-v3-main-wp4-4-i-is-repair` |
| HEAD / parent | `232d6b5` / `1019d34` |
| Worktree status | clean; one packet commit ahead of main |
| Remote / PR | no remote branch; no i PR yet |
| Intended i CSS SHA | `0702558b…` |
| Pristine post-h CSS SHA | `883e6aa8…` |
| Running job at snapshot | none as of 18:03; the full pytest started at 17:55 finished, but this read-only audit did not capture its result |
| True blocker | none; first land the docs-only authority/status PR, then resume i under C16 |

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
