# Documentation Retention

*Rules for keeping the docs surface useful without losing historical context.*

## Purpose

Keep active docs focused on current project truth. Archive completed plans when they stop helping daily work, and delete local/debug artifacts that should never become project memory.

> **`docs/product/**` is Always active and is not a feature workstream.** The product reference
> suite ([`../product/README.md`](../product/README.md)) describes the shipped application rather
> than a piece of work in flight, so it never becomes archivable when a feature closes.
>
> Do not run the Archive Criteria against it. Two of them will always appear satisfied for the
> wrong reason: the suite deliberately carries no status, so no handover follow-up will ever point
> at it (criterion 3), and a correct document needs no edits, so it can sit untouched for years
> (criterion 2). Neither is evidence of staleness here. Do not nominate it as an orphan candidate.
>
> No file inside it may be named `PLANNING.md` or `EXECUTION_LOG.md`; those names belong to the
> Active workstream class below and to the `/status` sweep, and would contradict this
> classification.

## Retention Classes

| Class | Examples | Rule |
|---|---|---|
| Always active | `CLAUDE.md`, `docs/MASTER_HANDOVER.md`, `docs/ai_workflow/**`, `docs/product/**`, `docs/DECISIONS.md`, `docs/CHANGELOG.md` | Keep in the active tree. Update when the workflow or durable project truth changes. |
| Active workstream | `docs/<feature>/PLANNING.md`, `docs/<feature>/EXECUTION_LOG.md`, feature research notes | Keep while the workstream is active, paused, or referenced from `docs/MASTER_HANDOVER.md`. |
| Archive | Completed feature plans, old audits, superseded implementation notes | Move to `docs/archive/<year>/<feature>/` after all archive criteria are met. |
| Delete | `debug/*`, `*.local.md`, generated scratch notes, local command output | Do not archive. These are local-only or transient artifacts. |

## Archive Criteria

Archive a document only when all of these are true:

1. The feature, audit, or migration shipped or was explicitly abandoned.
2. The document has had no meaningful edits for at least 6 months.
3. No open follow-up in `docs/MASTER_HANDOVER.md` points at it.
4. The active docs index or feature folder has a better current source of truth.

## Recorded dispositions — orphan candidates (assessed 2026-08-04 at `db1bc5d`)

These were nominated as orphans by the v21/v22 audits. Each is assessed here rather
than moved: **every one fails archive criterion 2** (no meaningful edits for 6 months),
so none is archivable yet. Re-assess after the stated date.

Search for the **shorthand** form too. `MASTER_HANDOVER.md` cites this family as
`` `_B`/`_C`/`_D`/`_E`/`_F`/`_G` `` after naming one file in full, so a grep for whole
filenames alone reports a false zero.

| Document | Genuine inbound refs | Last meaningful edit | Disposition |
|---|---:|---|---|
| `CSS_PHASE4_WP4_3I_B_EVIDENCE.md` | 1 (`MASTER_HANDOVER.md`, shorthand) | 2026-07-22 | **Not an orphan.** Keep; revisit only if the handover entry is archived |
| `CSS_PHASE4_WP4_3I_C_EVIDENCE.md` | 1 (same) | 2026-07-22 | as above |
| `CSS_PHASE4_WP4_3I_D_EVIDENCE.md` | 1 (same) | 2026-07-23 | as above |
| `CSS_PHASE4_WP4_3I_E_EVIDENCE.md` | 1 (same) | 2026-07-24 | as above |
| `CSS_PHASE4_WP4_3I_F_EVIDENCE.md` | 1 (same) | 2026-07-24 | as above |
| `CSS_PHASE4_WP4_3I_G_EVIDENCE.md` | 1 (same) | 2026-07-24 | as above |
| `CSS_PHASE4_WP4_3I_H_EVIDENCE.md` | 0 | 2026-07-25 | **Archive candidate — hold until 2027-01-25** (fails criterion 2 today) |
| `WP3_5_FETCH_INVENTORY.md` | 0 | 2026-07-12 | **Archive candidate — hold until 2027-01-12** |
| `archive/CLEANUP_V2_DEAD_CODE_AUDIT.md` | 1 | 2026-06-12 | **Already in `archive/`.** No further action |
| `user_profile/DUMBBELL_LOAD_BASIS_FIX.md` | 0 genuine | 2026-06-04 | **Archive candidate — hold until 2026-12-04.** Its only hit is the orphan-candidate list itself, which is not an index link |

> **Two corrections to the v22 candidate list.**
>
> 1. It recorded `CSS_PHASE4_WP4_3I_D/_E/_F` as carrying **6 inbound references each**
>    and `_B`/`_G`/`_H` as none. Re-derived: six of the seven carry exactly **one**
>    (the shorthand handover citation above); only `_H` is unreferenced.
> 2. The 5–7 reference counts it quoted belong to the similarly named
>    **`CSS_PHASE4_WP4_4_*`** family — one character apart in the filename. Check which
>    family you have before acting.
>
> **What is actually pytest-pinned, precisely.** The `WP4_4_*` **`.md`** files are only
> *mentioned* in test docstrings and one assertion message; no test reads them, so moving
> one does **not** red `Run Tests`. The real pins are the **JSON** siblings, which are
> `read_text()` at `tests/test_css_wp4_4_a_baseline_contracts.py:34`
> (`CSS_PHASE4_WP4_4_A_BASELINE.json`) and `tests/test_css_cascade_contracts.py:161`
> (`CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json`). Those two must not move. Leftovers **N7**
> states this pin against the `.md` files; that phrasing is imprecise and is recorded here
> for the next audit revision rather than edited inside this packet.

## Archive Procedure

1. Create `docs/archive/<year>/<feature>/` if it does not already exist.
2. Move the stale document there with its filename preserved unless the old name is misleading.
3. Grep the **whole repo** for the filename, not just docs — `*.py`/`*.ts`/`*.json`/`.github/workflows/*.yml` can hardcode a doc path (e.g. a test asserting an audit doc exists, or a CI step reading a baseline file). A doc-only link sweep misses these and the move reds CI. Fix every code/workflow reference, or keep the file in place if a build/test depends on its path.
4. Update links in `docs/README.md`, `docs/ai_workflow/INDEX.md`, and any affected feature docs.
5. Add a short changelog or handover note if the archived document was previously part of an active workstream.

## Keep Active Procedure

When a document stays active after a milestone, trim it to what future work needs:

- Replace completed checklist noise with a short shipped summary.
- Move durable choices into `docs/DECISIONS.md` as an ADR when they affect future implementation.
- Keep command names, file paths, and current verification status concrete.
- Remove stale speculation once the source code, changelog, or tests carry the truth.

## Delete Procedure

Delete transient artifacts instead of archiving them:

- Files under `debug/`, which are gitignored session scratch.
- `*.local.md`, including `MASTER_HANDOVER.local.md`.
- Generated command output, screenshots, or test logs unless a committed doc explicitly needs a small excerpt.
- Duplicated plans whose useful decisions have already moved into active docs.
