# Documentation cutover

GitHub issues own current public task status. Repository documents retain current
guidance, technical contracts, decisions and historical evidence. A published issue
does not make its source document disposable. This cutover changes documentation;
it does not authorize implementation of the work described in it.

The owner approved the private-record handling, the keep/split/archive policy and
20–30-document batches on 2026-10-26. The current commission is **one public pilot**;
the private H1 review waits until after that pilot. Every merge requires a separate
approval naming the PR number and exact head SHA. See the [pilot record](PILOT_CSS.md).

## Decision rules

Privacy, holds and actual consumers take precedence. Apply these rules together
with [Documentation Retention](../ai_workflow/DOC_RETENTION.md):

| Action | Use when | Required result |
|---|---|---|
| KEEP | Current guidance, active or paused work, durable contracts, needed evidence, qualification ledgers or machine inputs | Stable home, explicit role and reason; current public task status points to its owning issue. Dated evidence and handoffs are identified as historical. |
| SPLIT | Durable reference or evidence is mixed with duplicated task status or closed history | Preserve technical conditions, decisions, evidence and anchors; replace duplicate public tracking with verified issue links. Extract history only if it independently qualifies for archive. |
| ARCHIVE | Shipped or explicitly abandoned, no live follow-up or hold, named current replacement, all references and consumers repairable in the same change | Complete historical content in `docs/archive/<year>/<workstream>/`, with repaired navigation and source/destination identities. Pure moves preserve bytes; link-only edits are declared separately. |

Always-active product and workflow references remain active. Machine inputs stay at
their consumed paths. A blocked move can become KEEP with a documented durable role;
an unreviewed or unresolved disposition cannot be marked complete. This cutover
proposes no deletion and releases no private hold.

## Completion criteria

The cutover counts as done only when **all** of the following can be demonstrated
against a named final `main` commit and an owner-accepted closeout record.

1. **The complete public scope is accounted for.** Refresh an inventory of every
   tracked file under `docs/`, plus repository documentation outside that directory
   (root guides, folder guides, workflow/agent documentation and other tracked
   Markdown, reStructuredText or text documentation). Record path, source blob,
   documentary role and coverage boundary. Generated inventories, baseline inputs,
   evidence assets and third-party notices receive explicit KEEP/supporting-input
   dispositions; they are not silently omitted. Reconcile new, renamed and changed
   documents through the final commit. No path is left pending or unclassified.
2. **Every public disposition has been actioned and verified on main.** KEEP has a
   recorded role, stable home and checked consumers; SPLIT has preserved its durable
   content and anchors and uses verified issue destinations; ARCHIVE meets every
   retention predicate and records the original and resulting identities. Related
   PRs are owner-approved and merged, with applicable checks passing. An open pilot
   PR or a proposed batch is not an action completed on main.
3. **Navigation and tracking agree.** Repair affected relative links, anchors,
   shorthand citations, indexes and actual code/workflow readers. Verify no new
   broken references or content loss. Resolve any pre-existing broken reference
   that prevents a disposition from being verified, or give it an owner-accepted
   exception with a permanent evidence destination. Current public task status
   lives in the owning issues; dated narratives cannot masquerade as a live queue.
   Technical, product and recovery work may remain open under its own gates.
4. **All 167 held private records have verified permanent homes.** In the existing
   private register, retain the ID, hold category, original provenance, owner,
   permanent source/evidence location outside the temporary backup, content identity
   and retrieval/integrity verification receipt. Preserve payloads, attachments and
   decision/evidence dependencies as well as metadata. A source pointer, public
   summary or issue alone is insufficient. The register itself and its receipts
   also need verified permanent homes. Record private-retained outcomes for the 26
   explicit holds, the 18 provenance/privacy candidates and the 123 reserved records;
   closure does not require publishing them or completing their underlying work.
   Any declassification still needs exact-payload owner approval. No private source
   locators or raw receipts belong in public documentation.
5. **The temporary copy is not a unique source.** Separately reconcile its manifest
   with retained destinations: every item must either match a verified retained
   copy outside it, or have an explicitly approved, evidenced successor that
   preserves its required information and history. This includes local/untracked
   documents, attachments, database snapshots and recovery material outside the
   public-doc/private-record counts. A GitHub merge does not preserve ignored files,
   databases, protected roots or private evidence. Do not discard old versions solely
   because a newer file exists. Record omissions or unverified items as blockers.
6. **The owner accepts the closeout.** Present public coverage and merged-PR evidence,
   a private coverage/verification summary without private payloads, remaining
   exceptions and the temporary-copy reconciliation. The owner decides whether the
   temporary copy can be deleted. Neither this document nor satisfying these
   criteria authorizes deletion or a recovery operation.

These are acceptance conditions, not claims that the cutover or preservation work
is complete. H1 and permanent-home verification have not started in this pilot.
The encrypted off-machine backup and verified-restore deliverable retains its own
scope and gates; documentation cutover does not establish that deliverable.

## Pilot boundary and next review

The [CSS pilot](PILOT_CSS.md) accounts for twenty related evidence documents, with
thirteen KEEP, one SPLIT and six ARCHIVE dispositions. Navigation repairs and this
acceptance record are included in the same PR. Original measurements, accepted
limitations, contracts and signed decisions are preserved.

Stop after that PR is ready for owner review. Do not prepare another public batch,
start H1, enable auto-merge or merge this PR under the pilot commission.
