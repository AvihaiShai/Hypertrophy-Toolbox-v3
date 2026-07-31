# WP4.4 N4 continuation authority — packets i, j and k

**Owner ruling date:** 2026-07-31  
**Authority:** fresh N4 approval and execution authority for the remainder of WP4.4  
**Sequence:** `i` (narrow or abandon) → `j` → `k`, one writer/worktree/PR/merge at a time

This document supersedes every current-status sentence saying that N4 approval has not
been given, that no packet is next, or that `i`, `j` and `k` are unauthorized. Historical
descriptions of the earlier hard stop remain historical. Plan v2's technical gates still
bind except where an explicit ruling below narrows or replaces one.

## 1. Current integrated state

- `origin/main` includes the N4 inventories at `89523ed` and the visual-harness
  correction at `1019d34` (PR #211).
- PR #211 added the inert `data-visual-preserve-border` hook and corrected the dark
  determinism rule without changing snapshots or effective rendering. Do not reopen it
  during i–k unless a fresh regression is proven against current `main`.
- WP4.4-i is active in `wt/wp4-4-i-is-repair`. Its WIP evidence and test results are not
  final until every capture is rerun from the post-#211 tree and labeled by the checkout
  root and **served** CSS digest.
- The main checkout's local `CLAUDE.md` modification belongs to the owner. Never stash,
  discard, stage, commit, overwrite or copy it into a packet.

## 2. Binding owner rulings

| ID | Decision | Binding execution consequence |
|---|---|---|
| C1 | **N4 is approved.** | Start/continue i; do not request N4 approval again. |
| C2 | **i uses the CSS-local split-selector-list shape only.** | Split only branches proven safe. No `:where()` repair, page-bundle deletion, template/JS solution, or layer move. |
| C3 | **N3 narrow-or-abandon is automatic.** | Unsafe/inconclusive branches remain grouped with the ID donor. If no branch survives, merge evidence-only abandonment and continue to j. |
| C4 | **The Progression branch and exact thirteen-rule shape are authorized if the fresh post-#211 gates remain neutral.** | The prior owner-approved re-expression of h's over-broad `:where`/`:hover` counts is allowed only with structural preservation and red-path proof. Do not weaken h or N6. |
| C5 | **The i Stylelint exception is narrow.** | `no-descending-specificity` may rise only for warnings mapped one-for-one to the approved split selectors. `selector-max-id`, `selector-max-specificity`, `!important`, duplicates and every other category may not increase. Record unchanged maxima as honest under-delivery, not a pass of the old projection. |
| C6 | **G3 before/after identity is semantic, not a folder label.** | “Before” must be served from pristine current main; “after” from the final i tree. Record checkout root, commit, served `components.css` SHA and DB SHA. Relabel or discard any artifact whose path name contradicts its metadata. |
| C7 | **i resolution unblocks j and k.** | Whether i merges a narrowed repair or an evidence-only abandonment, proceed directly to j and then k without another routine owner checkpoint. |
| C8 | **The Packet-a layer-span pin stays closed for this goal.** | Do not re-pin it or touch h's 235 withheld declarations. Record a separate future removal-certification packet at closeout. |
| C9 | **No snapshot rebaseline.** | Never use `--update-snapshots`. A real packet-caused visual/computed change is rolled back or narrowed. A red proven on pristine main is inherited and recorded against its existing identity/band. |
| C10 | **Small or zero yield is acceptable.** | Projections and line counts are not acceptance criteria. A fully proven no-op/audit outcome may merge and the sequence continues. |
| C11 | **j is preservation-only.** | Keep `theme-dark.css` linked and nonempty; retain custom properties by default, retain `.value-changed`, preserve reduced-motion behavior, and do not add the deferred superset tint. Delete only removal-certified declarations. A no-op j is valid. |
| C12 | **k may close documentation without another owner review.** | Update the three canonical status files and responsibility-only `CSS_OWNERSHIP_MAP.md`. Put the N10 `QUALITY_GATE.md` row in k evidence as a proposal only; do not edit `QUALITY_GATE.md`. |
| C13 | **In-scope corrective subpackets are pre-authorized.** | If i/j/k finds a defect, the manager may create a narrowly named corrective PR inside the original packet's paths that restores an invariant or strengthens its oracle/contract. No scope expansion or visible behavior change. Rebase and rerun downstream gates afterward. |
| C14 | **Reproducible audit tooling is authorized; generated state is not.** | Commit scripts and contracts needed to reproduce evidence. Generated DBs, screenshots, logs and reports stay under gitignored `artifacts/`; never commit `data/**` or a probe DB. |
| C15 | **Routine repository operations are authorized.** | The manager may commit packet paths, push, open/update PRs, monitor/retry CI, merge when required gates pass and refresh main. Arrange each next isolated checkout through the repository's external worktree workflow; neither manager nor subagents create/remove/move worktrees. This is a workflow boundary, not a new owner decision. |
| C16 | **Land this authority/status sync before i; docs-only ancestry does not automatically invalidate content-addressed gates.** | Create a docs-only PR containing the seven authority/status/handoff files, explicitly excluding `CLAUDE.md`, and merge it before i. After rebasing i, a fresh result may be retained only if all production CSS, test, harness, audit-script and DB digests used by that result are identical and the ancestry/source metadata is corrected. Rerun any gate whose inputs changed or whose provenance is incomplete. |

## 3. Work that must not stop for owner input

The manager decides and continues when the issue is one of these:

- agent allocation, branch naming, evidence formatting, command ordering or retries;
- an unsafe selector branch (exclude it) or no safe branch (abandon i under N3);
- low/no deletion yield in j;
- a stale/misnamed artifact whose root/digest reveals its real side (relabel or rerun);
- a test failure fixable inside the active packet's authorized paths;
- an inherited red/flake reproduced on pristine main with a clean same-state control;
- exact contract strengthening or oracle repair that preserves the same premise;
- CI infrastructure/transient failure: diagnose, retry and keep the PR open;
- an in-scope corrective subpacket under C13;
- reconciliation of packet evidence and the canonical status documents.
- a docs-only rebase under C16 with identical measured inputs.

## 4. Genuine hard stops

Stop and ask the owner only if progress requires one of the following:

1. accepting an intentional visible, computed-value, token, behavior, API or response-contract change;
2. changing or regenerating a committed screenshot baseline;
3. weakening, deleting, bypassing, `xfail`-ing or broadly relaxing a protected contract;
4. changing `@layer` membership, `templates/base.html`, page bundles, JavaScript or templates beyond the already merged PR #211 hook;
5. changing DB schema/data, committing a DB/probe artifact, or touching the owner's dirty `CLAUDE.md`;
6. reopening the 235 layer-pin declarations, superset tint, WPB.4, deferred Workout Plan/Log cleanup or another parked workstream;
7. accepting a new unexplained visual/functional red that cannot be reproduced on main, narrowed away or rolled back inside the packet;
8. expanding a corrective packet beyond i/j/k's original production and test-support scope.
9. a persistent external permission, CI, worktree or infrastructure failure that remains
   after diagnosis and bounded retries and prevents the required proof or merge.

An encountered hard stop does not authorize rebaseline or scope expansion. Preserve the
branch, report the exact evidence, and wait.

## 5. Multi-agent execution model

Use up to three subagents beside the manager, but keep a single writer.

- **Packet i:** one read-only route/cascade auditor; one contracts/oracle reviewer; one
  adversarial evidence and gate reviewer. The manager alone edits and commits.
- **Packet j:** agents classify disjoint rule ranges read-only and independently challenge
  removal evidence; the manager alone applies dispositions to `theme-dark.css`.
- **Packet k:** agents independently audit contract collection, Windows/Linux ledgers and
  cumulative metrics/docs; the manager alone writes integration artifacts.
- Static reading/review may run concurrently. DB, Flask, browser, Playwright, visual and
  shared-port jobs run serially unless separately isolated by both worktree, DB and port.
- Packets never overlap: j starts after i merges/resolves; k starts after j merges. Arrange
  new checkouts through the external workflow in `PARALLEL_WORKFLOW.md`.

## 6. Remaining completion gates

### Packet i

- Prove the final branch set from the post-#211 tree.
- Run true G3 before from current main and true G3 after from i; compare all 45
  declarations and published totals.
- Fresh computed/owner/DOM/scoped-pixel differential, same-CSS and known-live controls.
- Packet contracts and red paths; full pytest; required Chromium suites; Stylelint under
  C5; Windows visual reconciliation; N8 Linux deep gate.
- Evidence must replace stale base hashes, paths and pre-#211 results.

### Packet j

- Classify all 81 rules against final post-i ownership.
- Apply M1–M12, especially M9 custom properties, M10 JS-applied state and M11 media.
- Full pytest/contracts, required light/dark/reduced-motion Chromium coverage, Stylelint,
  computed/owner/visual differential and N8 Linux deep gate.

### Packet k

- No production CSS change.
- Full integration suite, all per-packet contracts, full Chromium, Windows/Linux ledger
  reconciliation, final ownership differential and cumulative Stylelint/line/importance/
  duplicate/Phase-4 contribution report.
- Reconcile `MASTER_HANDOVER.md`, `ACTIVE_DEVELOPMENT.md` and `REFACTOR_PLAN.md` together.

## 7. Definition of done

The goal is complete only when i is merged or formally abandoned, j and k are merged, all
required gates are reconciled, origin/main contains the WP4.4 closeout, all canonical
status documents agree, the 235 declarations remain deferred, and the owner's local
`CLAUDE.md` change is untouched.
