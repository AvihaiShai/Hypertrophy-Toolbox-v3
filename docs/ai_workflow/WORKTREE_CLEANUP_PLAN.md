# Worktree Cleanup, Preservation, and Recurrence-Prevention Plan

*Status: fourth-pass rewrite after independent Codex, Astra, and Opus review.*
*Authority: planning only. This document authorizes no unlink, move, worktree
removal, prune, ref change, branch change, archive deletion, or main reconciliation.*
*Approval state: Gate 0 and Operation A Plan v2 Gate 1 are signed, and the approved
planning record records the approved implementation and verified disposable
interactive Windows acceptance. Operation A's reviewed guard and test source is
merged. Section 5.4, Section 11, and the dated operation evidence govern installation,
verification, monitoring, post-merge required-check disposition, and successor-artifact
reconciliation obligations; this amendment discharges none. Operation-specific owner
approval and Windows-filesystem review remain requirements under the contracts below.
Actual approvals, waivers, execution results, and the remaining prevention acceptance
are recorded in the dated [closeout record](../worktree_cleanup/CLOSEOUT.md) and
[state evidence](../worktree_cleanup/evidence/2026-10-29-amendment-readiness.md).
E requires its own separate plan and approval. Section 14 defines F and G under
their own separate plans and approvals; neither is approved here. This amendment
does not reopen completed operations or declare PREVENTION_COMPLETE.*

## 1. Purpose, authority, and independent outcomes

This plan retires only positively identified, owner-approved obsolete worktrees,
quarantines the malformed drive-root paths, preserves the complete recovery surface,
and introduces controls that address both MSYS path mistakes and worktree
accumulation.

The repository's existing authorities remain canonical:

- [QUALITY_GATE.md](QUALITY_GATE.md) controls planning, tests, and required
  reviewers.
- [AUTONOMY.md](AUTONOMY.md) controls agent roles and approval boundaries.
- [PARALLEL_WORKFLOW.md](PARALLEL_WORKFLOW.md) controls checkout and database
  isolation.
- [WORKSTREAM_OWNERSHIP.md](WORKSTREAM_OWNERSHIP.md) controls active-claim and
  lifecycle evidence.

This plan adds operation-specific safety requirements. It does not redefine those
documents or create permanent new agent roles.

### 1.1 Stable policy versus live evidence

This file contains stable predicates and procedures only. Counts, SHAs, branch
names, worktree paths, database counts, file counts, process lists, free-space
measurements, and remote advertisements belong in dated operation evidence outside
this document.

A semantic change to this plan requires Gate 1 review, or renewed Gate 1 review after
approval. Ordinary live-state drift invalidates only the affected assessment,
preservation manifest, or removal slice; it does not invalidate unrelated completed
operations or require editing this file.

Empty directory skeletons below .git/refs are not refs. Every ref inventory must use
Git's ref enumeration. Transient agent-created refs, including refs/codex entries,
must be recorded dynamically rather than assumed from a prior count.

### 1.2 Independently completable operations

#### Approved rollout order

The Gate 0 requirements impose this program order:

    Gate 0 signed
      -> Plan v1 -> council review -> Plan v2 -> Gate 1 owner approval
      -> A. Prevention -> PREVENTION_COMPLETE
      -> finish or explicitly disposition open development; retain its worktrees
      -> owner-accepted stabilization checkpoint
      -> regenerate fresh read-only evidence
      -> separately approve and schedule B, C, and D
      -> consider E only under its separate plan and approval

Operations F and G, added by a later amendment under Section 1.1, are considered only
under their own separate plans and approvals (Section 14). The Gate 0 requirements
above neither order nor authorize them.

No technical independence below permits B-G to bypass that sequence. During the
open-development phase, merged-PR and exact-head evidence may pre-classify completed
work mechanically; only ambiguous or genuinely unmerged residue requires substantive
owner judgment. Every row still receives the disposition and preservation checks in
this plan, and no worktree is removed during that phase.

#### Technical dependencies after stabilization

After the stabilization checkpoint and fresh evidence, the dependencies are:

    A. Prevention
    |
    +--> B. Malformed-root archive and quarantine
    |
    +--> C. Whole-tree and derived preservation
          |
          +--> D1...Dn. Independently approved worktree-removal slices
          |
          +--> E. Main reconciliation under a separate approval
    |
    +--> F. Separately approved additional-source preservation (Section 14.1)
          |
          +--> G. Separately approved drive-root child retirement (Section 14.2)

The shared Windows-filesystem proof in Section 4 is required before B, C, D, F, or G
uses its filesystem mutation/copy primitives.

- B does not depend on C, D, or E.
- Each D slice is approved, executed, verified, and closed independently. Normal
  development may resume between slices.
- E is source-control maintenance, not part of worktree-cleanup completion. It may
  proceed only after PRESERVATION_COMPLETE under its own plan and approval,
  regardless of whether every D slice has run.
- A triage result with no approved candidates is
  TRIAGE_COMPLETE_NO_REMOVAL_AUTHORIZED, not successful worktree retirement.
- F and G each require PREVENTION_COMPLETE and their own approvals. Beyond that they
  are independent: F does not depend on B, C, D, or E; no D slice, no E operation, and
  no PRESERVATION_COMPLETE waits on it; and an F failure blocks only G, and only for
  the source identities it failed to preserve. G depends only on its own approval and
  on ADDITIONAL_SOURCE_PRESERVED(source) already proved for its exact root identity.
  Neither is part of worktree-cleanup completion.

Section 14.0 defines when an unexpected drive-root child is outside approved operation
scope; that definition is stated only there, and such a child is retained and recorded
only. No proximity to a named root, generated-output classification, filesystem
creation time, previous campaign completion receipt, aggregate, receipt, approval
record, manifest, or baseline entry in this plan confers preservation, relocation,
quarantine, or removal authority over any unexpected drive-root child. Authority
exists only where this plan names it explicitly, as Operation B's two named roots are
named, or under a dated Section 4.3 owner approval record created separately from and
after this plan text. Section 14 defines the shape of two separately approved
operations, F and G, and approves neither: this plan names no source and no target for
either. Completing either changes no Operation B aggregate, no Operation C
PRESERVATION_COMPLETE, no Operation D worktree-slice outcome, and no
PREVENTION_COMPLETE declaration, and permits neither an edit to the owner-approved
drive-root baseline nor a zero exit from the Section 5.2 audit.

### 1.3 Planning-artifact landing gate

This file is the technical design, not a substitute for the repository's council
artifact. Before implementing A, the product-manager must create
docs/worktree_cleanup/PLANNING.md from PLAN_REVIEW_TEMPLATE.md. It must contain the
verbatim request, Section 0 requirements and Gate 0 sign-off, Plan v1, complete agent
provenance, the three required reviewers' verbatim findings, a response matrix, Plan
v2, and owner Gate 1 sign-off. The Astra/Opus/Codex reviews are additional evidence,
not replacements for architecture-reviewer, test-strategist, or
product-risk-reviewer.
Each later semantic amendment to this design records its own Gate 0 and Gate 1 in its
own council artifact rather than in the artifact named above, which is the Operation A
council artifact. The amendment that added Section 14 records its gates in
docs/worktree_cleanup_amendment/PLANNING.md.

The first Gate 1 implementation decision is for Operation A only. Sections B-G retain
their safety contracts and dependencies, but their production launchers and
operation-specific recovery details do not need to be built or approved before A can
land. Refine each later operation after stabilization and fresh evidence, then review
any semantic change under Section 1.1 before that operation is approved.

Adding this workflow document changes the repository's parametrized test-inventory
surface. Before its PR:

1. Place the plan and its INDEX entry in an owner-created standalone clone, never a
   linked worktree, so Git's tracked/staged view includes the new file. Create that
   clone from a non-local source or with a reviewed no-local/no-hardlink method.
2. Redirect TEMP, TMP, HT_RUNTIME_DIR, DB_FILE, caches, and bytecode to scratch.
3. Run scripts/generate_test_inventory.py --check. Regenerate only after that command
   proves real drift, then run --check again; never hand-edit the inventory.
4. Prove the checkout has no alternates/hardlinks to the live object store and its
   runtime paths cannot resolve to the live database or log tree.

This isolated planning/CI lane is permitted before C because it cannot touch the
live runtime. Normal collection against the live checkout/runtime remains forbidden
during a preservation or destructive freeze.

This is an operation-specific stronger isolation lane, not a replacement for
PARALLEL_WORKFLOW.md's normal DB-isolated linked-worktree flow. When the canonical
PLANNING.md is opened, add its current-state pointer to MASTER_HANDOVER.md through the
normal shared-path coordination process.

## 2. Threat model and non-negotiable safety rules

### 2.1 Threat model

This is a single-owner Windows repository with concurrent IDE, agent, terminal, app,
test, and maintenance processes. The controls in this plan address:

- accidental path conversion, shell interpolation, wildcard/prefix selection, path
  aliasing, reparse traversal, or selection of the wrong worktree;
- concurrent sessions or background processes mutating shared Git, filesystem, or
  SQLite state;
- interruption, process crash, power loss, partial copy/move/unlink/removal, or a
  journal write that does not complete;
- inconsistent SQLite copies, including WAL-mode databases and a writer starting
  during a naive file copy;
- stale registrations, unregistered directories, squash-merge ancestry gaps,
  detached or reflog-only history, and local-only content; and
- incomplete, corrupt, unavailable, or undecryptable preservation.

The plan does not claim protection against a malicious administrator, compromised
OS/kernel, hostile replacement of all local evidence and executables, or a fully
compromised off-machine storage account and both recovery-secret copies. Adding any
of those adversaries requires a separate threat-model decision and controls designed
for it.

Every mechanism below must name one of the in-scope threats it mitigates. When two
controls provide the same protection, prefer the simpler control with fewer
interruption states. Detached signatures, external manifest anchors, coordination-
register prefix hashes, and custom cryptographic protocols are not required by this
threat model. Authenticated encryption and off-machine restore testing remain
required for confidentiality and recoverability.

### 2.2 Non-negotiable safety rules

1. Never use git worktree remove --force.
2. During A-D, F, and G, never run a mutating worktree prune, manually delete
   .git/worktrees
   entries, delete or rename a branch/ref/tag/stash, reset, rebase, force-push,
   expire reflogs, or run Git object cleanup. The only prune command permitted is a
   reviewed worktree prune --dry-run for evidence. E has one narrow exception: its
   independently approved main-to-rescue rename must preserve the exact OID and
   reflog under a new collision-free name before a new main is created; it is not
   history deletion.
3. Disable automatic Git maintenance for every cleanup Git child. During each C/D
   live freeze, any Operation F live freeze whose approved source contains a live Git
   repository (Section 14), and any future E live-mutation window, suspend
   scheduled/background
   Git maintenance through an explicitly
   reviewed reversible mechanism, record its original state, and restore it only at
   a verified clean closeout. A failure before restoration leaves it suspended for
   recovery; a failed or ambiguous restoration records the actual/unknown state and
   blocks development resume. A later offline C restore failure blocks D and E but
   does not resuspend maintenance after a verified capture-phase closeout. Because
   archive-only OIDs need not remain live after C, do not impose a retention-wide
   maintenance ban.
4. Worktree removal deletes that worktree's administrative directory and reflog.
   Before removal, every commit whose only durable live root is that admin directory
   must receive a collision-free archive ref and must be present in verified private
   preservation.
5. A successful fsck is necessary but not proof that a previously present object was
   preserved. Freeze all three Section 3.3 protected OID sets and test every member
   and type explicitly after preservation and after every removal slice.
6. For every B-G preservation/cleanup command that invokes Git against live or
   restored operation state, invoke a pinned absolute git.exe directly with an
   argument array through the final reviewed safe Git runner. Use a freshly
   constructed minimal child environment, disabled hooks/fsmonitor/helpers/pagers/
   external diff/textconv, GIT_OPTIONAL_LOCKS=0 for reads, and gc.auto=0 plus
   maintenance.auto=false for mutations. No shell-interpolated Git command is
   permitted. Ordinary implementation/version-control work for A remains under the
   repository's normal Git workflow and cannot invoke a cleanup launcher.
7. Never fetch with pruning and never treat a locally named refs/remotes/pr entry as
   advertised remote durability. Remote evidence comes from a fresh independent
   advertisement or fetch into an isolated audit repository.
8. Resolve every mutation target from an exact manifest. Require a drive-qualified
   canonical/final path, expected NTFS volume serial and file ID, an ordinary
   non-reparse parent, no wildcard or prefix matching, and immediate-child
   containment where the operation requires it. Reject UNC, device, volume-GUID,
   ADS, DOS-device, 8.3-alias, trailing-dot/space, control-character, and unresolved
   forms.
9. Filesystem enumeration must be no-follow and explicit-stack. Record reparse
   points as entries; never traverse them.
10. A worktree link may be unlinked only when it is an approved .venv or
    node_modules junction whose tag, final target, volume, and file identity exactly
    match one of the two approved shared targets in the main checkout. Unlink the
    junction nonrecursively. Main's separate ordinary venv is protected but is not a
    permitted shared-junction target.
11. A worktree containing an ordinary private .venv, venv, or node_modules is KEEP
    for this cleanup. Preserve it separately; do not call it rebuildable.
12. Git refusal is not data discovery. Inventory and disposition tracked,
    untracked, ignored, special-index, nested-repository, database, and environment
    state before removal.
13. Before opening any database copy, capture the complete raw SQLite family:
    database, WAL, SHM, rollback/statement journal, super-journal, and any unresolved
    same-directory temporary family member. Integrity and logical checks run only on
    disposable copies or completed online backups.
14. Once an operation's live-runtime preservation freeze begins, preserve every
    manifest-enumerated startup snapshot before starting the app, pytest, Playwright,
    Vitest, a release build, or code that can initialize runtime paths. Never call
    create_startup_backup during preservation. Pre-C planning and implementation
    gates are permitted only through the isolated lane in Sections 1.3 and 4.5.
15. Do not install or update packages in the shared Python, Node, release, or browser
    environments during cleanup.
16. Public source control, encrypted private preservation, and local quarantine are
    distinct:

    - Public: reviewed code/docs and redacted receipts only.
    - Private: full Git state, bundles, local-only history, databases, settings,
      evidence, environments, and private manifests.
    - Quarantine: exact local payload retained for recovery; it is not the
      off-machine backup.

17. Unreviewed history is private by default. A public push requires explicit
    content/privacy approval and acknowledgement that deleting a public ref cannot
    retract already disclosed objects.
18. No LLM may invoke a live destructive execution mode. The owner launches the
    reviewed production entry point from a direct interactive PowerShell console
    while agent, IDE, app, test, and background writers are stopped.
19. Keep a durably flushed append-only journal for each mutation. REMOVE_INVOKED is
    the boundary after which no automatic retry or rollback is permitted.
20. Retain every preservation object and quarantine payload for at least 30 days
    after the relevant operation, including each Operation F source capture and each
    Operation G quarantine payload (Section 14), and a successful
    normal-development observation.
    Later deletion requires a separate manifest and owner approval; no automatic
    expiry is permitted.

## 3. Evidence, disposition, and candidate model

### 3.1 Generated evidence

Each operation has a unique ID and private evidence root outside every source,
candidate, Git directory, quarantine source, and archive source. The owner records
the root's canonical/final path, physical identity, no-reparse ancestry, capacity,
and access boundary.

The generated private evidence contains:

- exact command/tool/package versions and hashes;
- process, CWD/handle, port, scheduled-task, and runtime-source maps;
- source and destination member manifests with files, empty directories, sizes,
  hashes, attributes, ACL/stream dispositions, reparse metadata, and read failures;
- Git refs, reflogs, pseudorefs, worktree admin state, object/OID sets, status/index
  state, config hazards, remotes, and advertised refs;
- database-family and logical-validation records;
- environment member/hash and reconstruction records;
- candidate decisions, approvals, journal, recovery state, and retention date; and
- encrypted-object IDs plus upload/download/restore receipts.

The redacted public receipt contains only non-sensitive row IDs, approved outcome,
package/manifest identifiers, ciphertext hashes, and verification status. It must
not contain private paths, plaintext-content hashes, database contents, settings,
credentials, recovery secrets, or unreviewed ref names.

### 3.2 Reproducible discovery predicates

The inventory must state its predicates. At minimum:

- refs are rows returned by for-each-ref, not directories;
- advertised remote refs are recorded separately from local remote-tracking and
  handmade PR refs;
- Git operation markers are all discovered entries plus a separate reviewed
  live/stale/unknown disposition;
- SQLite discovery has three non-overlapping categories: header-confirmed database
  files, filename/extension candidates lacking a confirmed header, and sidecar/
  journal-family members mapped to an owning candidate;
- local operational files are selected by an explicit path/name rule, never by an
  unexplained total;
- main snapshots and linked-worktree snapshots have distinct path identities and
  are not double-counted; and
- current database contents are described by measured schema/table results, not by
  assumptions such as "has user state."

Unreadable, malformed, or corrupt inputs remain preservation inputs. They are
recorded and archived rather than silently excluded.

### 3.3 Protected Git OID sets

Every Git inventory defines three exact sets:

- LIVE_REQUIRED_OIDS: every object reachable from a durable named ref after the
  approved archive refs are created. This includes every commit that would otherwise
  lose its only root when a worktree admin directory is removed.
- COLD_ARCHIVE_REQUIRED_OIDS: every object present in the frozen live object store,
  enumerated by OID and type, including objects named only by common/worktree
  reflogs, stash history, admin pseudorefs, and the complete unreachable-object set.
- HISTORICAL_BUNDLE_REQUIRED_OIDS: every head and reachable object in each preserved
  pre-existing bundle that is absent from the frozen live store.

LIVE_REQUIRED_OIDS must remain present in the evolving live repository and in
restored preservation. COLD_ARCHIVE_REQUIRED_OIDS need not remain live after
development resumes, but every member must exist in the exact restored cold archive.
HISTORICAL_BUNDLE_REQUIRED_OIDS must exist in a verified restoration of its owning
historical bundle. Representative semantic restore drills are additional evidence;
they never replace complete batch OID/type checks.

### 3.4 Independent disposition fields

Do not overload one classification with activity, content, and execution state.
Every worktree row records:

| Field | Allowed values |
|---|---|
| Activity signals (set) | OPEN_PR, ACTIVE_CLAIM, ACTIVE_PROCESS, ACTIVE_CWD_OR_HANDLE, LIVE_GIT_OPERATION, PREEXISTING_LOCK, UNKNOWN; empty means CLEAR |
| Source issues (set) | DIRTY, SPECIAL_INDEX, ADMIN_OID_UNANCHORED, GIT_MARKER_UNRESOLVED, UNRESOLVED; empty means ACCOUNTED |
| Data issues (set) | UNPRESERVED, QUARANTINE_NOT_READY, UNRESOLVED; empty means NONE_OR_PRESERVED |
| Environment entries (set) | APPROVED_SHARED_LINK, ORDINARY_PRIVATE; empty means ABSENT |
| Lifecycle basis | INTEGRATED, SQUASH_ACCOUNTED, DUPLICATE, SUPERSEDED, EXPLICITLY_ABANDONED, UNRESOLVED |
| Eligibility | REVIEW_REQUIRED, INELIGIBLE, ELIGIBLE |
| Owner disposition | UNDECIDED, KEEP, DEFERRED, TARGETED_PENDING_SLICE, APPROVED_FOR_SLICE |
| Aggregate row status | NOT_REMOVED, VERIFIED_REMOVED, BLOCKED_NEEDS_RECOVERY |

Eligibility transitions are evidence-driven:

    REVIEW_REQUIRED -> INELIGIBLE
    REVIEW_REQUIRED -> ELIGIBLE
    any relevant state drift -> REVIEW_REQUIRED

An INELIGIBLE row cannot be approved for removal and must be assigned KEEP before
triage closes. For an ELIGIBLE row, the owner independently records KEEP, DEFERRED,
or TARGETED_PENDING_SLICE. An owner-approved slice manifest advances only its
included rows to APPROVED_FOR_SLICE. Journal state is separate, uses the exact
Section 8.2 transition
graph, and begins only for an ELIGIBLE row with APPROVED_FOR_SLICE disposition. Every
attempt retains its immutable terminal journal state. VERIFIED derives aggregate
status VERIFIED_REMOVED; ABORTED_NO_MUTATION or ROLLED_BACK leaves it NOT_REMOVED;
FAILED_NEEDS_RECOVERY derives BLOCKED_NEEDS_RECOVERY. A later attempt never overwrites
an earlier attempt's evidence.

Every tracked/untracked path and every local-only tip receives one content
disposition:

- PUBLIC_SOURCE_REVIEWED
- PRIVATE_SOURCE_PRESERVED
- GENERATED_EVIDENCE_PRESERVED
- SENSITIVE_DATA_PRESERVED
- DISPOSABLE_OWNER_CONFIRMED

Unknown content cannot be blanket-labeled nonmeaningful or disposable.

### 3.5 Positive lifecycle basis

A worktree is obsolete only when the owner confirms that no current workflow needs
the checkout and at least one positive basis is proved:

- INTEGRATED: HEAD is reachable from a freshly advertised target ref, or its complete
  tree exactly matches a named commit reachable from that ref.
- SQUASH_ACCOUNTED: a reviewed tree/range/patch comparison identifies the squash
  result and shows no unexplained source content. Ancestry and git cherry alone are
  insufficient.
- DUPLICATE: a named retained checkout/ref contains the same source state.
- SUPERSEDED: a named replacement ref/worktree accounts for every unique change.
- EXPLICITLY_ABANDONED: the owner reviewed and intentionally abandoned the checkout;
  its branch/ref, admin-only commits, and private preservation remain retained.

Age, branch name, clean status, ignored status, or a closed PR is evidence to
investigate, never a positive lifecycle basis by itself.

Use the hosting provider's fresh merged-PR data to accelerate, not replace, this
classification. For each attached branch, record every matching PR's number, state,
base, merge OID, and recorded head OID. An exact match between the current worktree
HEAD and a merged PR head, together with a clean and fully dispositioned checkout,
is a high-confidence SQUASH_ACCOUNTED candidate. Before assigning that basis, prove
the PR's merge is present in the freshly advertised target and compare the relevant
tree/range/patch so merge-time conflict resolution or later base drift leaves no
unexplained source content. A branch that advanced after the PR, a detached HEAD,
multiple ambiguous PRs, or local-only content remains REVIEW_REQUIRED. A merged PR
never authorizes removal by itself.

### 3.6 Eligibility rule

A row becomes ELIGIBLE only if every condition below is true:

1. It is a registered immediate child of the approved development parent and is not
   main or the active control checkout.
2. The activity-signal set is empty: no open PR, active claim, process, CWD/handle,
   live Git operation, preexisting lock, or uncertainty.
3. The source-issue set is empty: tracked status is clean and no special-index
   flag/stage, unanchored admin OID, or unresolved marker remains. A dirty/special
   row becomes eligible only after a separately reviewed normal source-resolution
   workflow preserves its state and leaves it clean; the cleanup executor never
   cleans or normalizes a candidate.
4. Every valid commit OID named by its admin HEAD, ORIG_HEAD, reflogs, or pseudorefs
   is reachable from a durable named ref; any formerly admin-only commit has a
   collision-free archive ref.
5. Its attached branch ref or detached archive ref remains present and is included
   in verified private preservation. A public remote copy is not mandatory.
6. Every untracked, ignored, database, local-setting, evidence, and nested-repository
   member has a verified preservation/quarantine mapping and an owner disposition;
   the data-issue set is empty.
7. The environment-entry set is empty or contains only APPROVED_SHARED_LINK entries;
   any ORDINARY_PRIVATE entry is KEEP.
8. Path, registration, Git-admin relationship, reparse topology, and physical
   identity pass the reviewed validator.
9. A positive lifecycle basis and owner rationale are recorded.

The triage report must show every worktree, the fields above, proposed disposition,
reason, and owner decision. Before any D execution, it must also state the exact
candidate count, slice count, estimated duration, storage requirement, and
maintenance window.

### 3.7 Immutable cleanup target set

After triage and before the first D slice approval, the owner approves a scope-only
target-set manifest under Section 4.3, with a unique campaign ID, exact non-empty
ELIGIBLE row IDs, baseline path/admin identities, and evidence hashes. This
establishes the denominator for WORKTREE_CLEANUP_COMPLETE but authorizes no mutation.
Included rows become TARGETED_PENDING_SLICE.

Once the first slice is approved, that campaign's target set is immutable. Every D
slice manifest binds its campaign ID and target-set hash and contains only a subset of
those rows that are not already VERIFIED_REMOVED. A targeted row may become blocked
or require renewed evidence, but cannot be removed from the denominator or
reclassified KEEP/DEFERRED to manufacture completion. Added candidates require a new
campaign ID. Receipts identify the exact target-set version and report every
superseded/incomplete campaign; no narrower later set can support an unqualified
estate-wide cleanup claim.

## 4. Shared tooling, integrity, and test gates

### 4.1 Keep the mutation surface small

Build tooling in explicit stages:

1. Before B, C, or F, approve an early shared package containing the no-follow
   inventory/manifest compiler, final safe Git runner, path/identity validator,
   append-only journal primitives, strict versioned schemas, and scratch tests. C
   uses this final runner; it is not deferred until worktree triage.
2. Before B, add and review the thin root-quarantine launcher against B's exact
   manifest and crash states.
3. C uses established copy/archive/encryption tools through reviewed wrappers; it
   does not require the worktree-removal transaction core.
4. Only after C produces the real candidate model and triage table, add the D
   transaction core and thin owner-only worktree-removal launcher. Do not build that
   removal surface speculatively.
5. Operation F (Section 14.1) uses the same established copy/archive/encryption tools
   through the same reviewed wrappers as C and requires no new mutation primitive.
   Only after an approved Operation G target manifest exists for one exact root, add
   the thin root-quarantine launcher for Operation G (Section 14.2), built from the
   same reviewed template as item 2 but bound to its own manifest, journal and outcome
   name. Do not build that mutation surface speculatively. Neither F nor G may use D's
   worktree-removal transaction core.

The resulting packages contain no unrelated orchestration. Scratch-only
tests/adapters are not reachable from any production launcher.

There is no separate bootstrap launcher that later becomes ambiguous. If a
preliminary safe Git runner is needed before the final package exists, it is
versioned, independently reviewed, explicitly retired, and forbidden after the final
runner hash is approved.

Each production launcher accepts no caller-supplied target/path/action, pipeline
input, environment authorization, or permissive fallback. It loads one adjacent
approved immutable manifest and verifies its recorded digest. B handles exactly one
root, C one live capture phase, F one approved closed source set, G exactly one root,
and E one live maintenance window. One D launcher
invocation owns exactly one slice: it holds the same process, coordination handle,
and freeze through ordered row processing and
Section 8.3 closeout, pausing for fresh owner confirmation before each row. It never
skips/reorders a row or re-enters through a second process.

### 4.2 Mandatory human and Windows-filesystem review

Before any live copy, move, junction unlink, or worktree removal, a non-LLM reviewer
must inspect the actual mutation surface:

- canonical/final-path and immediate-child comparison;
- volume serial/file-ID acquisition and revalidation;
- reparse-point enumeration and link-only junction deletion using
  [IO.Directory]::Delete(path, false), or an equivalently proven primitive;
- same-volume, non-overwriting directory/file move;
- long-path behavior and limits;
- ADS enumeration and preservation;
- case-folding, trailing-dot/space, DOS-device, UNC/device, 8.3, prefix, and
  traversal rejection;
- PowerShell 5.1 and PowerShell 7 behavior; and
- the exact native git.exe spawn site and argument array.

Run scratch proofs for every item. If the selected API cannot safely handle a
measured live path, classify that path KEEP/BLOCKED; do not improvise a fallback.
File-ID revalidation reduces accidental target substitution but is not described as
an adversarial race-proof sandbox.
This review is required for an Operation F source capture and an Operation G root move
exactly as it is for B, C, and D (Section 14), and it must add fresh scratch proofs
for every path form a drive-root source or quarantine destination introduces. A prior
review of a different operation's mutation surface never satisfies it.

### 4.3 Manifest integrity and owner approval

Each B root operation, C preservation run, D slice, future E operation, Operation F
source capture, and Operation G root operation (Section 14) uses an
exact immutable manifest produced by reviewed tooling. The owner approval records the
operation ID and SHA-256 digest of the manifest and production package in the
operation's durable approval record outside every source and candidate. At launch,
the executor recomputes both digests, rejects any mismatch, and revalidates live
state. This guards against accidental drift between approval and execution without
introducing a detached-signature or external-anchor protocol outside the Section 2.1
threat model.

Every B root-operation, D slice, Operation F source-capture, and Operation G
root-operation approval binds these common fields:

- operation/root/slice ID;
- exact manifest hash;
- exact production-package hash;
- exact external-executable paths and versions, with a hash when the executable is an
  operation-supplied artifact rather than an installed owner-selected tool;
- required preservation object IDs/hashes;
- exact source, destination, evidence, and quarantine identities as applicable;
- expected pre/post Git and filesystem state;
- the SHA-256 digest of the Section 14.3 known-unexpected register as frozen at this
  operation's start, recorded again in the operation's closeout receipt; and
- owner, date, and retention deadline.

A B approval additionally binds exactly one malformed-root identity, one nonexistent
same-volume destination, and its single ordered move. A D approval additionally
binds its immutable cleanup-campaign ID/target-set hash, candidate row IDs and ordered
actions, plus the control-checkout identity. Fields that do not apply to that
operation are absent, never populated with dummy values.
An Operation F approval additionally binds the exact closed set of source identities,
the digest of that same set's retained outside-scope eligibility assessment taken
immediately before manifest approval, each Git-bearing source's retained empty
archive-ref-need set and protected ref/OID inventory, each source's extraction root,
the destination identity, the freeze budget with the owner-approved maximum freeze
duration approved for that Operation F operation, its safe-abort boundary, and its
expected capture and restore results. The approval enrolls only the assessed set;
it changes no source's unexpected classification and no owner-approved baseline.
An Operation G approval additionally binds exactly one drive-root child identity,
one nonexistent same-volume quarantine destination, its single ordered move, the
ADDITIONAL_SOURCE_PRESERVED(source) evidence for that exact identity, and its
retention start and per-object retention period. An Operation G approval is never an
Operation B approval, and no Operation B approval may bind an Operation G root.

Each C manifest binds the exact source/destination scopes, copy/archive/encryption
executables, archive-ref creation set, protected OID inputs, storage objects,
key-handling procedure, freeze budget, safe-abort boundary, and expected
capture/restore results. Its approval authorizes only those preservation writes and
new collision-free archive refs; it never authorizes D.

No single-use nonce or nonce verifier is used. Human presence comes from the direct
interactive console, the durable approval record, digest verification, and an exact
final confirmation after every live-target no-mutation validation has passed.

### 4.4 Journal model

The journal is append-only JSONL outside all source/candidate trees. Each record has
the operation, slice and row ID, monotonic sequence, state, timestamp, tool/package
hash, and evidence hash. Flush each record durably. Hash the completed journal for
the closeout receipt, but do not require a custom per-record hash chain, prefix hash,
or external anchor.

All B-G live launchers, including the Section 14 operations F and G, use one fixed
owner-approved coordination-file path
outside every operation evidence root, source, and candidate. Its parent must be an
ordinary non-reparse directory at the expected canonical path. The lock is an
exclusive OS handle on the pre-created file; file existence alone is not a lock.
Failure to acquire the handle or uncertainty about a holder blocks the operation. The
executor never deletes, replaces, steals, or forcibly breaks the coordination file or
handle.

A shared append-only attempt register at the same owner-approved root records every
B-G live attempt and closeout. Every read, append, and flush occurs while holding the
exclusive handle. The production launcher acquires that handle once and keeps the
same hold from initial state verification through final durable closeout. On entry it:

1. validates that the register parses completely and has monotonic unique attempt
   identifiers;
2. rejects an incomplete, failed, or otherwise unresolved prior live attempt;
3. verifies the approved manifest/package digests and current live preconditions; and
4. appends and flushes ATTEMPT_OPEN before any live action.

A separately owner-approved recovery launcher may instead bind exactly one unresolved
attempt and append RECOVERY_ATTEMPT_OPEN. It may perform only that approved repair.
It does not clear or waive any other unresolved attempt.

Every clean live closeout uses this single-hold protocol:

1. While retaining the original handle, finish all terminal and global verification.
2. Restore and verify saved Git-maintenance state when the operation suspended it.
3. Append and durably flush VERIFIED_CLEAN_CLOSEOUT to the operation journal and
   shared register, then write and durably flush the final receipt.
4. Release the handle exactly once as the process's final shared-state action. Write
   no register or receipt state after release.

The next launcher's successful exclusive acquisition is the proof that the prior OS
hold ended; there is no reacquire-to-prove-release finalizer and no
LOCK_RELEASE_CONFIRMED state. If the process terminates after the clean-closeout flush
but before an explicit release returns, the OS releases its handle and the next
launcher still validates the complete register and live state before acting.

If any mutation, verification, maintenance restoration, journal flush, or receipt
write fails, record and flush FAILED_NEEDS_RECOVERY or BLOCKED_RECOVERY plus the
actual/unknown maintenance state when the original handle remains available. Then
release once without VERIFIED_CLEAN_CLOSEOUT. If interruption prevents that record,
ATTEMPT_OPEN without VERIFIED_CLEAN_CLOSEOUT is itself a persistent block. Handle
release never authorizes development resume or retry. A verified
ABORTED_NO_MUTATION or ROLLED_BACK may receive a clean closeout for its own attempt,
never another attempt. An offline C restore-gate failure after a verified live capture
closeout blocks D and E through Gate C; it does not falsely poison B's live lock.
An offline Operation F restore failure at Gate F, after that operation's verified live
capture closeout, blocks only Operation G and only for the source identities it failed
to preserve; it does not poison B's, C's, or another Operation F operation's live
lock.

A successful approved recovery verifies the exact bound repair and all global/live
postconditions, restores maintenance when applicable, and appends
RECOVERY_VERIFIED, BLOCKED_RECOVERY_CLEARED with the original attempt ID, and
VERIFIED_CLEAN_CLOSEOUT for the recovery attempt before the one final release. It can
clear only its bound block. A failed recovery attempt creates its own
BLOCKED_RECOVERY and never clears the original.

Within a stage containing multiple filesystem entries, flush an ordered child intent
and result record for each native mutation, with exact before/after identities. Append
the aggregate stage-result state only after every child result is verified; the
aggregate state never substitutes for per-mutation recovery evidence.

### 4.5 Recovery readiness and test isolation

Before the first live mutation in B, the first preservation write or ref creation in
C, the first removal slice in D, the first preservation write in an Operation F source
capture, the first live mutation in an Operation G root operation (Section 14), or any
future E mutation, approve the common recovery
playbook for that operation and pass its scratch drills. Do not wait for a blocked
live repository to design known recovery procedures.

Each playbook must cover every reachable interruption boundary in its state machine,
including lock acquisition, intent/result journal flushes, copy/archive, ref creation,
move, link unlink, Git child execution, receipt writing, and maintenance restoration
as applicable. For every state, specify read-only diagnosis, artifacts that must be
retained, allowed recovery primitives, prohibited guesses, and the exact evidence
needed for ABORTED_NO_MUTATION, ROLLED_BACK, verified recovery, or continued block.
Fault-injection tests must exercise failures immediately before and after each
irreversible boundary. The owner runs one representative recovery drill against a
disposable Windows scratch repository and scratch database family.

An actual live repair still requires an incident-specific owner approval that binds
the blocked attempt and observed state. Pre-approved recovery design authorizes no
automatic repair and no live mutation by an agent.

#### Test isolation

Outside a live preservation/destructive freeze, required planning and implementation
gates may run before C only in remote CI or a standalone checkout with no
alternates/hardlinks to the live object store and every runtime/cache path redirected
to scratch. During a live freeze, no test or collector runs.

The pre-C guard/cleanup fast lane must not load tests/conftest.py, import application
modules, or open the live repository log/database. Use a standalone PowerShell
harness for the immediate guard contract. When a canonical gate requires pytest,
Playwright, Vitest, or generate_test_inventory.py collection before C, run it only in
the isolated planning/implementation checkout described above. Redirect TEMP, TMP,
HT_RUNTIME_DIR, DB_FILE, caches, and bytecode, and verify the live protected roots
are unchanged.

The transaction core uses injected scratch filesystem/Git/fault adapters. Automated
tests never invoke the owner-only production execution entry point. The owner runs
one interactive end-to-end acceptance against a disposable scratch repository.
There is no production test-bypass switch.

Use this gate matrix:

| Changed surface | Required gate |
|---|---|
| This plan plus INDEX | AI-workflow manual review; generate_test_inventory.py --check and regenerate only on proved drift |
| .claude files, root CLAUDE.md, workflow docs | Manual dry-run plus focused guard/config contract tests and code-reviewer or careful self-review |
| scripts at repository root | Stem/directory-token test union; verify-suite if genuine coverage is absent; code-reviewer |
| Any Python implementation | Repository-wide pyright baseline diff in addition to its path-derived gate |
| Added/removed/renamed test or parametrized config | Run inventory --check; regenerate after proved drift; never hand-edit |
| B/C/D/E/F/G operation with no source change | Manifest, restore, and receipt gates only; no invented browser gate |

After C, normal path-derived gates may run in an isolated checkout/runtime. Always
run generate_test_inventory.py --check for a relevant surface; regeneration is
permitted only after the check proves real drift and never while local untracked
configuration files would contaminate it.

### 4.6 Canonical role routing

- The manager remains read-only and coordinates the approved workflow.
- The product-manager owns the canonical Gate 0/Gate 1 planning artifact.
- Automation-QA owns tests under tests and e2e.
- The senior-developer owns hook, script, and repository-config implementation.
- The owner creates/removes any checkout and performs every external, user-level,
  recovery-key, remote, and live destructive mutation.

Root CLAUDE.md and every .claude path are never-claimed shared paths; coordinate each
edit under WORKSTREAM_OWNERSHIP.md. If implementation and test authors work in
parallel, the owner first creates one isolated manager checkout and both roles stay
within that checkout and its isolated runtime.

## 5. Operation A - prevention and lifecycle compliance

### 5.1 Root cause and bounded guard contract

The causal conjunction was:

1. MSYS argument conversion was suppressed at native-process spawn, whether by a
   command-scoped assignment, export, inherited process state, or persistent state;
2. a native Windows child received a slash-rooted path; and
3. Windows resolved that path from the current drive, creating an unintended
   drive-root child.

The project-level and owner-approved user-level guard must reliably deny every
observable attempt to set or export MSYS_NO_PATHCONV or MSYS2_ARG_CONV_EXCL,
including direct assignments, env/cmd/PowerShell/.NET/setx forms, chaining,
multiline and nested command strings, and bypassPermissions. A separate fresh-session
preflight checks Process, User, and Machine inherited state.

The guard may add tested literal heuristics for known native-output commands, but it
must not claim to infer fully expanded argv, aliases/functions, opaque scripts,
native-versus-MSYS executable identity, arbitrary destination options, or all child
processes from raw command text.

All cleanup writes use PowerShell end to end, direct argument arrays, and
drive-qualified native paths. For Git revision/path reads, resolve exactly one blob
OID with ls-tree, validate the full OID, then pass it separately to cat-file blob
instead of suppressing path conversion.

### 5.2 Required prevention changes

The prevention change must:

- update root CLAUDE.md without exceeding its size constraint;
- replace unsafe status guidance in .claude/commands/status.md;
- correct PARALLEL_WORKFLOW.md, AUTONOMY.md, WORKSTREAM_OWNERSHIP.md, and
  .claude/commands/worktree.md;
- update project settings and all shell-capable agent registrations so the new
  denial is profile-invariant;
- update every active user/project memory, local handover, and retained-worktree
  guidance that prescribes either suppression variable or POSIX paths for native
  Windows output;
- remove unsafe branch -D and mutating-prune teardown advice from active workflow
  documentation;
- update scripts/new-worktree.ps1 and add a read-only
  scripts/audit-worktrees.ps1 lifecycle report under the Section 4.5 tooling gates;
- replace new-worktree.ps1's copy-current byte copy with a consistent SQLite snapshot
  procedure. Create the seed at a new temporary destination with SQLite's online
  backup API or an equivalently reviewed SQLite-native operation, validate the
  completed copy, and install it as the target only after success. If the procedure
  or validation is unavailable, refuse copy-current without overwriting the target;
  never copy database.db alone, and never infer safety merely from the current
  absence of a -wal file;
- add the bounded guard regression contract; and
- add a read-only drive-root audit that compares configured drive roots with an
  owner-approved baseline and reports unexpected new children without deleting them.

Never execute the historical npx or gh incident commands in tests; serialize them as
hook payloads and prove denial before child launch.

The one-time rule to preserve every discovered backup/snapshot overrides ordinary
rotation/cleanup guidance only for this operation. Do not silently turn it into a
universal ban on normal post-operation backup rotation.

### 5.3 Worktree-sprawl prevention

Repeating teardown prose is insufficient, but a gitignored Markdown file must not
become a second worktree registry. The lifecycle view is a projection reconciled on
every read from:

- `git worktree list --porcelain -z` for registered worktrees;
- Git's reported common/admin relationships plus a no-follow scan of the approved
  development parent for missing paths, unregistered directories, and reparse
  anomalies; and
- owner/task/disposition annotations from the main checkout's gitignored
docs/ai_workflow/WORKSTREAM_OWNERSHIP.local.md.

Extend WORKSTREAM_OWNERSHIP.md with the annotation schema. Missing annotations do not
hide a registered or discovered worktree; the projection reports it as OWNERLESS and
sets its activity signal to UNKNOWN. Stale annotations remain visible as
ORPHANED_ANNOTATION until dispositioned. Git's registry is authoritative for
registration, not for physical presence, so any registry/filesystem disagreement sets
the source issue to UNRESOLVED and blocks action rather than being silently copied
into the annotations.

- after `git worktree add` succeeds, creation atomically adds or updates owner, task,
  branch, creation time, expected PR, teardown condition, and next review date;
- concurrent annotation updates use a short local lock plus atomic replacement, or
  independent atomically renamed per-worktree records; there is no transaction that
  pretends to commit Git creation and annotations together;
- if Git succeeds but annotation writing fails or the creator is interrupted, do not
  auto-remove the worktree. Return an incomplete-creation result; the next audit
  derives the registered row and flags it OWNERLESS for repair;
- creation preflight reads a freshly reconciled projection. It fails closed on an
  ownerless row, a registry/filesystem anomaly, or an unacknowledged merged/closed/
  overdue row until the owner records a KEEP/close disposition or time-bounded
  deferral;
- status/handover reports merged, closed, ownerless, orphaned-annotation, or overdue
  rows for review. Fresh merged-PR metadata and exact PR-head OID matching provide
  triage evidence under Section 3.5, never automatic teardown authority;
- a workstream is not closed until the owner either performs verified non-force
  teardown or records KEEP with a reason and next review date; and
- no audit or lifecycle tool auto-removes, prunes, deletes a branch, or treats age or
  PR state alone as permission.

### 5.4 Gate A

Operation A completes only when:

- exact deny/allow cases pass on every installed PowerShell 5.1/7 host;
- the existing UTF-8-BOM-plus-ASCII and fail-closed exit-code contract remains;
- all effective guard registrations and both profiles are tested;
- the two variables are absent at Process/User/Machine scope in a fresh session;
- the active guidance scan contains no prescriptive unsafe advice;
- drive-qualified native commands and the safe Git blob workflow remain allowed;
- the lifecycle audit works read-only against a scratch inventory;
- WAL-active and concurrent-write fixtures prove copy-current produces a consistent
  validated SQLite snapshot, while injected backup/validation failures prove no
  partial seed replaces the target;
- concurrent and interrupted creation fixtures prove the reconciled projection
  reports post-Git annotation failures as ownerless without automatic removal;
- A implements the already Gate-0/Gate-1-approved subplan, passes every Section 4.5
  implementation gate including Test Inventory Drift --check, and is merged; and
- the owner-approved user-level guard/memory updates are installed and verified.

## 6. Operation B - malformed-root archive and quarantine

B may start after A and the relevant Section 4 Windows/filesystem proofs. It does not
wait for worktree classification or Git preservation.

Each attempt retains its immutable terminal journal state. Each named root separately
derives NOT_QUARANTINED, VERIFIED_QUARANTINED, or BLOCKED_NEEDS_RECOVERY; a later
attempt never overwrites prior evidence. VERIFIED_QUARANTINED derives only after the
root's VERIFIED attempt, complete Section 4.4 clean-closeout protocol, and final root
receipt. A missing/failed closeout derives BLOCKED_NEEDS_RECOVERY instead.

For D:\c and D:\d independently:

1. Stop only processes that can write the selected root and confirm no CWD/handle
   remains there.
2. Inventory the exact canonical/final path, physical identity, files, empty
   directories, hashes, metadata/streams, and reparse topology without following a
   link.
3. Create an exact archive with a standard reviewed tool. Prove:

       frozen source manifest
       == local archive member/content manifest
       == freshly downloaded and decrypted extraction manifest

4. Preserve encrypted copies locally and off-machine under Section 7.5's key
   controls.
5. Create the Section 4.3 immutable manifest and owner approval for one root only.
   Acquire and retain the shared Section 4.4 operation lock, then revalidate every
   live-target no-mutation precondition and append PREFLIGHTED.
6. Append AUTHORIZED after direct owner confirmation. Immediately revalidate source,
   parent, destination, file IDs, volume, and reparse topology.
7. Append and flush QUARANTINE_MOVE_INTENT, then move the exact root to a nonexistent
   operation-specific same-volume quarantine destination without overwrite. Never
   copy-delete or recursively delete it. Append and durably flush MOVE_RESULT with
   the native call's success/failure, source/destination observations, and error.
8. Append QUARANTINED only after source absence, destination identity, and exact
   member/hash equality are proved; then run the full postcondition and append
   VERIFIED. Complete the Section 4.4 clean-closeout protocol and final root receipt.
   Only then may the aggregate root status become VERIFIED_QUARANTINED.

B's exact forward states are:

    NOT_STARTED -> PREFLIGHTED -> AUTHORIZED -> QUARANTINE_MOVE_INTENT
    -> MOVE_RESULT -> QUARANTINED -> VERIFIED

Terminal attempt branches are:

    NOT_STARTED | PREFLIGHTED | AUTHORIZED
      -> ABORTED_NO_MUTATION

    MOVE_RESULT
      -> ABORTED_NO_MUTATION       # only with exact proof of no mutation

    QUARANTINE_MOVE_INTENT | MOVE_RESULT | QUARANTINED
      -> FAILED_NEEDS_RECOVERY      # interruption, partial/ambiguous state, or
                                    # failure without exact no-mutation proof

Before QUARANTINE_MOVE_INTENT, a failed attempt records ABORTED_NO_MUTATION. After
intent, a completed move call may end in ABORTED_NO_MUTATION only when exact evidence
proves the original source and identity wholly unchanged and the destination absent.
An interruption, missing result, partial move, or source/destination ambiguity at or
after intent records FAILED_NEEDS_RECOVERY. Inspect both exact identities; never
blindly retry, overwrite, or guess. A new attempt after ABORTED_NO_MUTATION is allowed
only when the approved manifest is unchanged, the owner reviews the completed result,
reconfirms, and journals a new attempt ID.

A failure for one root does not invalidate the other's completed operation. Keep
each quarantine object for the retention period. Post-operation observation checks
both original paths and the configured drive-root allowlist so a future D:\tmp,
C:\c, or other unexpected root is detected rather than limiting recurrence checks to
the two historical names.

## 7. Operation C - whole-tree and derived preservation

### 7.1 Runtime map and bounded freeze

Before terminating any process, the owner captures the effective runtime-source map
for every app, server, test, IDE, launcher, task, or service that could reach Git or
runtime data. Record the effective source/precedence of DB_FILE, HT_RUNTIME_DIR,
LOCALAPPDATA, APPDATA, PLAYWRIGHT_BROWSERS_PATH, TEMP, TMP, relevant caches, .env
files, IDE settings, wrappers, and scheduled/service configuration. Resolve all
resulting roots privately. An unresolved root blocks C.

From a read-only pre-inventory, prepare the exact C manifest required by Section 4.3.
It names every proposed new archive ref and OID, records the measured freeze budget,
and identifies the last ordinary safe-abort boundary. The owner's explicit C approval
authorizes only that capture and those append-only, collision-free ref creations.
Revalidate the complete manifest after the freeze is established; drift aborts before
any preservation write or ref creation.

Then acquire and retain the shared Section 4.4 operation lock and establish one
bounded preservation freeze: stop Git/app/database writers, automatic
restart sources, IDE integrations, agents, tests, and maintenance. Record ports,
processes, CWDs/handles, Git markers/locks, environment hazards, and any unsupported
topology. Do not delete a stale marker or lock merely to pass the gate.

### 7.2 Whole-tree cold copy first

Before creating refs or other Git metadata:

1. Select a non-overlapping destination, preferably another physical volume/failure
   domain.
2. Before approval, measure source bytes and file counts, benchmark the selected
   no-follow enumeration/copy/hash tools against the selected destination, and record
   a conservative lower-bound throughput. Estimate the complete in-freeze duration,
   including writer shutdown, both source manifests, copy, immediate source-to-local
   comparison, final Git/raw-database/environment capture, and clean closeout.
3. The C manifest records an owner-approved maximum freeze duration, the measured
   estimate plus contingency, and checkpoint deadlines. Do not begin the freeze when
   the conservative estimate exceeds the maximum. Recheck source bytes, bytes still
   to be written, destination capacity, and archive overhead immediately before
   writing. Require that amount plus the larger of 25 percent or 1 GiB.
4. Create a no-follow cold copy/archive of the complete approved D:\development
   scope, including immediate loose files, registered and unregistered directories,
   the main .git, local settings/evidence, and reparse entries as inert metadata.
5. Generate live-source manifests immediately before and after capture and require
   them to be identical. Compare both directly with the cold-copy extraction.
   Archive-to-itself or upload-to-download equality alone is insufficient.

Before any archive ref or other live metadata mutation, a failed checkpoint or
projected overrun may cleanly abort C: stop writing, retain and label partial outputs
INVALID_INCOMPLETE, restore maintenance, record ABORTED_NO_MUTATION, close out under
Section 4.4, and leave later disposal to a separate approved action. Once the first
archive ref is created, a deadline overrun no longer authorizes ordinary abort. Finish
the minimum manifest-enumerated Git/raw-database capture and clean closeout, or enter
BLOCKED_RECOVERY under the pre-drilled Section 4.5 playbook. Tooling should hash while
copying where the reviewed tool supports it, without weakening direct
source-to-restoration equality.

### 7.3 Git roots and OID preservation

Using the final safe Git runner and no-follow filesystem inventory, record:

- every actual named/symbolic ref and target OID;
- advertised remote refs separately from local remote-tracking and handmade PR refs;
- every stash entry and older stash reflog OID;
- every common reflog OID;
- each worktree admin HEAD, ORIG_HEAD, log, index, and pseudoref OID;
- worktree-private refs/config;
- detached tips;
- every object readable from the frozen live repository, enumerated by OID and type
  and mapped to its physical primary, pack, alternate, or other object source;
- fsck missing/corrupt and unreachable OIDs by object type; and
- nested repository and existing bundle inventories.

Any alternate, symlinked object path, object/common directory outside the approved
scope, or promisor/partial-clone dependency blocks C until every required object is
available locally, the dependency is captured explicitly, and a sanitized isolated
restore proves that the repository is standalone.

Type-check every extracted OID. Compute archive-ref need from durable named refs
only; a common reflog is recovery evidence, not a durable named root. For every valid
commit named by a worktree admin directory that is not reachable from a durable named
ref, prepare a collision-free refs/archive/worktree-cleanup/<operation>/<row>/...
ref. The owner creates those refs with the final safe Git runner. Re-inventory twice
and freeze exact final ref, reflog, admin-root, stash, LIVE_REQUIRED_OIDS,
COLD_ARCHIVE_REQUIRED_OIDS, and unreachable-object sets.

Do not encode a previously reported count. The manifest-enumerated set is the gate.

### 7.4 Derived Git preservation

After the archive refs exist:

1. Create an exact full .git archive containing objects, refs, packed refs, reflogs,
   config, indexes, worktree admin directories/logs/HEADs, custom files, empty
   directories, and reviewed metadata/streams.
2. Require identical live .git manifests immediately before and after capture, then
   compare every member/hash in both directly with the local archive extraction.
3. Create a portable bundle of every bundle-eligible named ref. Verify it and require
   exact bundled-ref/OID equality; the bundle supplements the full archive.
4. Locate every pre-existing bundle in approved backup roots, including the
   historical all-refs backup identified during review. For each one, run bundle
   verify, record/list its exact heads, and restore-test all tips absent from the live
   store. A corrupt historical bundle is preserved as evidence but does not satisfy a
   recovery claim.
5. Preserve and restore-test every nested Git repository separately.
6. Prove every member of LIVE_REQUIRED_OIDS and COLD_ARCHIVE_REQUIRED_OIDS has the
   expected type in the frozen source and restored cold archive. Prove every member
   of HISTORICAL_BUNDLE_REQUIRED_OIDS in its restored historical bundle. Do not
   substitute fsck alone for complete OID/type comparison.

### 7.5 Databases, ignored state, and environments

Inventory every root discovered in the pre-stop runtime map plus the repository,
artifacts, recovery/backup directories, local application-data roots, and the owner
paths enumerated in C's approved immutable source manifest. A path is an inventory
target only because one of those categories covers it; being named by the owner
somewhere outside the approved manifest does not make it one.

This inventory is a discovery obligation, not a source grant. When it observes a
drive-root directory outside C's approved source scope, that directory is recorded and
retained only: discovery never adds it to an immutable source manifest, and discovery
alone obliges no capture. Adding any such directory to a source manifest requires the
separate Operation F approval of Section 14.1, which this plan does not give.

- Capture every raw SQLite family first; never open the original after capture.
- Create completed online backups from disposable family copies, then run integrity,
  foreign-key, schema, and logical-count checks on disposable/online copies only.
- Preserve every manifest-enumerated startup snapshot before any app/test launch.
- Preserve, within C's approved immutable source manifest, ignored/untracked/local
  settings, handovers/claims, evidence, loose files, recovery/salvage directories, and
  unique local payload. This bullet adds nothing to that manifest, and a drive-root
  directory outside C's approved source scope is recorded and retained only, per the
  discovery paragraph above and Section 14.
- Preserve main .venv, venv, node_modules, browser stores, and every ordinary private
  environment as separate exact no-follow archives/manifests. Record reconstruction
  versions and health output without installing or repairing anything.
- Record volatile cache/log paths separately so expected later drift does not weaken
  the nonvolatile equality gate.

Keep the capture freeze only until the whole-tree copy, final Git capture, raw
database families, environment/local payload captures, and their immediate
source-to-local comparisons are complete. Mark those local artifacts immutable,
record the capture receipt, and complete the Section 4.4 clean-closeout protocol for
the live capture phase, including maintenance restoration under the original lock. Only
then allow writers to resume. Encryption, upload, download, disposable database
checks, and restore drills operate only on those immutable copies. Later live drift
is handled by D's slice refresh; it does not alter the captured C snapshot.

Use an established authenticated-encryption tool; do not invent crypto. Before a B
quarantine move, a D removal, or an Operation G retirement move (Section 14), the
owner must approve:

- the tool and its AEAD/KDF or equivalent security properties;
- a tool-generated high-entropy secret or approved strong recovery phrase;
- two independent offline custody copies, such as an established password manager
  plus a separate offline recovery record; and
- bounded secret handling: no command arguments, logs, shell history, transcripts,
  source files, or unencrypted temporary files; isolate and terminate the key-bearing
  process after use rather than claiming memory can be proven erased.

Upload every required encrypted object to private off-machine versioned storage,
download it into a fresh root, verify ciphertext hashes, decrypt/extract, and compare
exact member/hash sets. Prove recovery with the stored secret before any removal and
before any Operation G retirement move, and again at retention exit.

### 7.6 Gate C and isolated restore

Treat the first decrypted extraction as immutable evidence and never run Git or
project code against it. Make a second disposable copy with no hardlinks to the
evidence or live store. Before invoking Git, use a reviewed no-execution sanitizer to
rewrite or disable every absolute gitdir/worktree path, include, alternate, hook,
fsmonitor, filter, external-diff/textconv, pager, credential/askpass helper, and
remote. Disable network and prove no restored path resolves to a live source or
executable. Extraction itself must reject traversal, absolute/device/ADS entries,
case collisions, and external link materialization.

Restore into a fresh isolated root and verify at minimum:

- whole-tree source-to-restoration equality;
- full Git archive state and portable bundled refs;
- complete LIVE_REQUIRED_OIDS, COLD_ARCHIVE_REQUIRED_OIDS, and
  HISTORICAL_BUNDLE_REQUIRED_OIDS membership/type equality, plus representative
  semantic recovery of reflog-only and unreachable objects;
- every manifest-present historical bundle's unique tips;
- every manifest-present detached, dirty, staged, unstaged, and special-index
  worktree state;
- nested Git state;
- every manifest-present main/user-bearing database family plus snapshots;
- ignored/untracked payload; and
- main and ordinary-private environment manifests.

When any listed state class is absent from the live manifest, its production restore
gate is not applicable; exercise that parser/restorer path with a representative
disposable scratch fixture instead. Never invent live data merely to satisfy a gate.

Missing/corrupt objects, skipped members, source/archive mismatch, incomplete
database families, unexpected link traversal, live-source resolution, secret
exposure, or failed recovery blocks D and E.

C reaches PRESERVATION_COMPLETE only when its live capture phase has
VERIFIED_CLEAN_CLOSEOUT in the shared register, maintenance is restored, no C-caused
BLOCKED_RECOVERY remains, the final capture receipt passes, and every offline
encryption/upload/download/restore gate above passes. Anything less blocks D and E.
Operation F is outside PRESERVATION_COMPLETE. Operation F still performs every Section
7.6 restore verification for its own sources, under Operation F's own gate; no
Operation F source, receipt, or failure contributes to or blocks
PRESERVATION_COMPLETE, and no Operation C receipt covers an Operation F source, so
PRESERVATION_COMPLETE keeps exactly the meaning it had before Section 14 existed and
pre-amendment and post-amendment C receipts remain comparable.

## 8. Operation D - resumable worktree-removal slices

### 8.1 Slice preparation

Before the first slice, require PRESERVATION_COMPLETE, complete the triage table and
Section 3 eligibility checks, and freeze the Section 3.7 target-set manifest. Create
the small production package only after its real candidate profiles are known.
Obtain the mandatory non-LLM mutation-surface review and scratch proofs.

The control checkout must use the same common Git directory, be a retained
noncandidate for the entire slice, and have manifest-pinned path/file identity, HEAD,
status, and admin relationship. The owner console and production-package CWD remain
outside every candidate. Acquire and retain the single shared Section 4.4 operation
lock before validation and record owner/PID/start time. Failure to acquire the lock,
an incomplete prior attempt, or an ambiguous journal blocks execution; the launcher
never clears it.

Each slice:

- has its own immutable manifest/digest, owner approval, journal, freeze budget, and
  closeout receipt;
- binds the immutable cleanup-campaign ID/target-set hash and contains only targeted
  rows;
- contains at most three candidates for the first slice and at most five thereafter;
- runs the first approved candidate of each unseen shared-link profile alone;
- uses one short console-only freeze for the whole slice, not a campaign-long freeze
  or a reboot between every candidate;
- does not Git-lock the worktree estate or candidates; manifest containment and the
  console-only freeze protect KEEP rows without adding an unmodelled unlock step; and
- ends with the full Section 8.3 closeout and explicit development resume. A verified
  full or partial closeout is a safe pause; only Section 11's exact named outcome may
  be claimed.

Before slice approval, time the complete scratch preflight, one representative
candidate transaction for each applicable profile, global verification, maintenance
restoration, and closeout. The manifest records a conservative estimate, contingency,
and owner-approved maximum freeze. Do not start when the estimate exceeds the maximum.
Before a candidate's first mutation intent, a projected overrun cleanly ends the slice
under Section 8.3. After that intent, the state machine and Section 4.5 recovery
playbook control; a deadline never authorizes an unsafe shortcut.

At slice entry, repeat activity, identity, status, ref/admin-OID, database/payload,
environment, process, and advertised-remote checks. Compare against the most recent
verified expected state: C plus journalled prior slices and every approved
post-development preservation refresh. C's artifacts may be reused only when their
protected inputs still match. Any changed candidate or Git control-plane state
requires an approved preservation refresh and restore proof for the affected scope;
it does not reopen completed B or earlier D slices.

### 8.2 Per-candidate state machine

Allowed forward states are:

    NOT_STARTED
    PREFLIGHTED
    AUTHORIZED
    PAYLOAD_MOVE_INTENT
    PAYLOAD_MOVED
    LINK_UNLINK_INTENT
    LINKS_UNLINKED
    REMOVE_INVOKED
    REMOVE_RESULT
    REMOVED
    VERIFIED

Terminal alternatives are:

    ABORTED_NO_MUTATION
    ROLLED_BACK
    FAILED_NEEDS_RECOVERY

Legal branches are:

    NOT_STARTED -> PREFLIGHTED -> AUTHORIZED
      -> PAYLOAD_MOVE_INTENT -> PAYLOAD_MOVED
      -> LINK_UNLINK_INTENT -> LINKS_UNLINKED
      -> REMOVE_INVOKED -> REMOVE_RESULT -> REMOVED -> VERIFIED

    any state before REMOVE_INVOKED
      -> ABORTED_NO_MUTATION       # only when exact evidence proves this attempt
                                  # made no live-target mutation

    any state after a live-target mutation but before REMOVE_INVOKED
      -> ROLLED_BACK               # only after deterministic reverse verification

    any ambiguous state, or any failure at/after REMOVE_INVOKED
      -> FAILED_NEEDS_RECOVERY

Rules:

1. After acquiring the shared Section 4.4 coordination lock, complete all live-target
   no-mutation validation before PREFLIGHTED, including package/signing-key/manifest
   trust, freeze, receipts, control/candidate identity, activity, status, refs,
   admin/protected OIDs, preservation availability, payload, environment, and
   reparse topology.
2. The slice launcher has one invocation ID, and every candidate attempt within it has
   a distinct attempt ID. A failed preflight records ABORTED_NO_MUTATION and consumes
   no special authorization token. An unchanged approved row may be attempted again
   after the non-manifest precondition is fixed, the owner reviews the prior journal,
   reconfirms, and a new attempt ID is recorded. Manifest or expected-state drift
   requires a new owner approval for the changed manifest. There are no nonces.
3. After successful preflight, the owner reviews the exact row and confirms in the
   direct console. Flush AUTHORIZED immediately before the first mutation intent.
4. Revalidate critical path/file identities immediately after authorization. Drift
   records ABORTED_NO_MUTATION.
5. Immediately revalidate payload source/destination identities and reparse topology.
   Move only manifest-approved untracked/ignored payload to a nonexistent
   same-volume quarantine destination; flush intent first and verify before
   PAYLOAD_MOVED.
6. Immediately revalidate each junction and target, then unlink only manifest-
   approved shared junctions with [IO.Directory]::Delete(path, false), or the
   equivalently proven primitive. Flush intent first. Verify both approved shared
   targets and all three protected main environment trees remain unchanged before
   LINKS_UNLINKED.
7. Immediately before removal, revalidate candidate/control path identities,
   registration, admin relation, and reparse topology. Require exact expected
   NUL-safe status, branch/ref/admin-root state, and residual member-set equality. An
   undispositioned residual blocks removal.
8. Flush REMOVE_INVOKED, then spawn the pinned Git child exactly once:

       git.exe --no-pager --no-optional-locks
         -c core.hooksPath=<approved-empty-directory>
         -c core.fsmonitor=false
         -c gc.auto=0
         -c maintenance.auto=false
         -C <verified-control-worktree>
         worktree remove -- <exact-manifest-path>

9. Capture child PID, argument fields, stdout, stderr, and exit code; flush
   REMOVE_RESULT.
10. Append REMOVED only when the registered entry, admin directory, and intended
    worktree path are absent with no unexpected residual.
11. Before VERIFIED, prove branch/ref OIDs are unchanged and every member of
    LIVE_REQUIRED_OIDS still exists with its expected type live and in restored
    preservation,
    COLD_ARCHIVE_REQUIRED_OIDS remain complete in the restored cold archive, and
    HISTORICAL_BUNDLE_REQUIRED_OIDS remain complete in restored historical bundles.
    Also prove quarantine exact, shared environments unchanged, and every
    noncandidate worktree, including KEEP and DEFERRED rows, registered at its
    expected HEAD/status. VERIFIED sets aggregate row status to VERIFIED_REMOVED.

When a payload or link stage does not apply, append both of that stage's intent and
result states with applicability=not_applicable, an expected empty set, and unchanged
before/after evidence. Do not silently skip states.

Before REMOVE_INVOKED, an exact deterministic completed move/unlink may be reversed
without overwrite, then journaled ROLLED_BACK. At or after REMOVE_INVOKED, an
interruption, nonzero exit, missing result, partial state, or ambiguity goes directly
to FAILED_NEEDS_RECOVERY. Never retry automatically, prune, manually edit Git admin
state, or guess. Recovery uses the journal, archive refs, and cold preservation under
a separately reviewed repair/re-add procedure. A ROLLED_BACK attempt may be followed
by a new attempt only with a new attempt ID after owner review; any manifest/state
change requires a new approval for the changed manifest.

### 8.3 Slice closeout

Whenever the launcher stops after attempting any row, run the same closeout; never
leave a verified removal behind an open slice. Verify:

- compare expected and actual registration/path sets;
- compare every ref and LIVE_REQUIRED_OIDS member with the live slice state; verify
  every COLD_ARCHIVE_REQUIRED_OIDS and HISTORICAL_BUNDLE_REQUIRED_OIDS member in its
  restored preservation object;
- run fsck in addition to, not instead of, OID checks;
- verify quarantine and required private preservation objects;
- verify both shared junction targets and all protected main/ordinary environments;
- verify every noncandidate worktree's expected identity, registration, HEAD/status,
  and content/preservation disposition, including KEEP and DEFERRED rows;
- verify the manifest-enumerated live database/snapshot families without opening the
  originals;
- confirm that no unexpected drive-root child was created during the operation, by
  comparing a no-follow explicit-stack enumeration of the configured drive roots
  (Section 5.2) against the owner-approved baseline union the Section 14.3
  known-unexpected register as frozen at this operation's start; a pre-existing
  registered child is not a failure and a newly created child is, whether or not it
  resembles a registered entry;
- hash and review the complete journal; and
- complete the Section 4.4 single-hold clean-closeout protocol, including maintenance
  restoration and the final slice receipt, end the freeze, and record
  development resume.

If every manifest row is VERIFIED_REMOVED, the slice can reach
WORKTREE_SLICE_COMPLETE. If a non-empty ordered prefix is VERIFIED_REMOVED and the
remaining suffix is NOT_STARTED, except that its first row may instead be
ABORTED_NO_MUTATION or ROLLED_BACK, the same successful global closeout yields
WORKTREE_SLICE_PARTIAL_CLOSED. The verified prefix remains valid; every unfinished
target remains in the immutable campaign denominator and may appear in a later approved
slice. A zero-removal clean abort records SLICE_ABORTED_NO_REMOVAL.
FAILED_NEEDS_RECOVERY cannot receive any clean slice outcome until its separately
approved recovery succeeds.

Publish only a privacy-reviewed redacted receipt after the shared Git state has
settled. No branch/ref retirement occurs in D.

## 9. Operation E - separate main reconciliation

The divergent-main repair is not a prerequisite for B, C, or D and is not included
in worktree-cleanup completion. It requires its own source-control-maintenance
manifest and owner approval.

Its eventual live executor must acquire and retain the same Section 4.4 coordination
lock, cannot overlap a D slice, and must suspend/restore Git maintenance around its
live mutation window. It must complete Section 4.4's exact clean-closeout protocol
before MAIN_RECONCILIATION_COMPLETE. Its separate review adds any Windows-filesystem
proofs required by the chosen checkout/switch procedure and a Section 4.3 immutable,
digest-bound owner-approved manifest tailored to E's exact refs, target OID,
working-tree paths, preservation objects, and expected pre/post state.

That separate plan must:

1. preserve and restore-test main's tracked, staged, unstaged, untracked, ignored,
   and special-index state;
2. preserve and restore-test main's complete reflog/OID set, anchor every required
   reflog-only commit under a collision-free archive ref, and select a distinct
   collision-free rescue branch name that is proved absent but not yet created;
3. disposition remaining working content without reset, rebase, or force;
4. query a fresh stable advertised origin/main and review all intervening content,
   dependency, and lockfile differences;
5. choose either preservation/compatibility validation for existing shared
   environments or a separate environment migration; never install into shared
   environments during reconciliation;
6. before switching/creating the new main, compare its target tree against every
   tracked, staged, unstaged, untracked, ignored, special-index, ordinary, and
   reparse path in the checkout; any overwrite, hidden byte, or type collision
   blocks reconciliation;
7. rename the divergent local main to the still-absent approved rescue branch name
   only after its archive refs are durable and the checkout is clean, then create a
   new local main at the exact approved advertised SHA;
8. verify HEAD/upstream equality, rescue durability, clean status, unchanged live
   database/snapshot/environment families, and receipt history; and
9. run one isolated-runtime smoke only after PRESERVATION_COMPLETE, with all runtime/
   cache paths directed to a fresh temporary root and the live database untouched.

E may proceed after PRESERVATION_COMPLETE even if later D slices are deferred. Its
receipt and any public source changes follow the repository's normal PR and quality
gates.

## 10. Common abort and recovery rules

Stop the affected operation or slice without improvising when:

- plan, manifest digest, production-package digest, or executable identity is wrong;
- an unknown process, CWD/handle, writer, restart source, Git marker, or lock remains;
- a target path, file ID, volume, registration, admin relationship, ref, status,
  special-index state, payload, database family, environment, or reparse target
  differs from the manifest;
- source-to-preservation or download-to-restoration equality fails;
- a required Git OID is absent, corrupt, unanchored, or missing from restored
  preservation;
- an archive follows/skips a member, warns, escapes containment, or cannot be
  decrypted with the approved recovery copy;
- a database family is incomplete or was opened before raw capture;
- a public action would disclose unreviewed/private content;
- the executor receives a caller-supplied path/action or an LLM attempts live
  execution;
- git worktree remove requests force, returns nonzero, is interrupted, or leaves
  ambiguous disk/registration/admin state; or
- recovery would require pruning, manual admin deletion, overwrite, reset/rebase, or
  destructive guessing.

Record the terminal state and preserve every relevant backup, journal,
coordination lock-state record, source, and quarantine object. For a failed/incomplete
live attempt, follow the already drilled Section 4.5 playbook and Section 4.4's
single-hold blocked-recovery protocol. Never write the shared register after releasing
the handle. Handle release does not authorize development resume or retry. If the
failure occurred while a C/D freeze, an Operation F live freeze, or an E
live-mutation window was active and
restoration was not attempted, keep Git maintenance suspended; if restoration failed
or is ambiguous, record its actual/unknown state and keep development paused. The
separately reviewed recovery must verify a clean closeout. An offline C restore
failure after the verified capture-phase closeout blocks D and E without resuspending
maintenance. Return only to the earliest affected operation or slice; a later success
cannot waive its failed gate.
These rules apply unchanged to Operation F and Operation G (Section 14). An Operation
F or Operation G failure returns only to that operation's own earliest affected source
or root; it neither reopens nor waives a completed B, C, or D result, and no later F
or G success waives a failed gate of any operation.

## 11. Completion and retention

The outcomes are intentionally distinct:

- PREVENTION_COMPLETE: A is merged/installed/tested and lifecycle monitoring is
  active.
- MALFORMED_ROOT_QUARANTINED(root): that one approved B root has aggregate status
  VERIFIED_QUARANTINED, is absent from its original path, is exact in quarantine,
  and is independently recoverable off-machine.
- MALFORMED_ROOTS_QUARANTINED: both specifically named roots, D:\c and D:\d, meet
  MALFORMED_ROOT_QUARANTINED; approving or completing only one cannot produce this
  plural aggregate.
- PRESERVATION_COMPLETE: C's live capture has VERIFIED_CLEAN_CLOSEOUT with maintenance
  restored, no C-caused BLOCKED_RECOVERY remains, its final capture receipt passes,
  and all whole-tree, derived, encryption, off-machine, and isolated-restore gates
  pass.
- TRIAGE_COMPLETE_NO_REMOVAL_AUTHORIZED: the owner approved no D candidates; no
  worktree-retirement claim is made.
- WORKTREE_SLICE_COMPLETE: every row in one non-empty D slice has aggregate status
  VERIFIED_REMOVED and the complete Section 8.3 closeout passes, including global
  checks, maintenance restoration, Section 4.4 VERIFIED_CLEAN_CLOSEOUT, and the final
  closeout receipt.
- WORKTREE_SLICE_PARTIAL_CLOSED: one non-empty ordered prefix is VERIFIED_REMOVED,
  every unfinished row was NOT_REMOVED and retained in the immutable target set at
  that slice's closeout, and the same complete Section 8.3 global/lock/maintenance
  closeout passes. A later verified removal does not invalidate this historical
  receipt. It is a safe pause, not campaign completion.
- WORKTREE_CLEANUP_COMPLETE(campaign-id, target-set-hash): every immutable target
  row has aggregate status VERIFIED_REMOVED, and each removal is covered by a
  WORKTREE_SLICE_COMPLETE or WORKTREE_SLICE_PARTIAL_CLOSED final receipt; every
  non-target row has an explicit KEEP or DEFERRED owner disposition and remains exact
  at its approved identity, registration, HEAD/status, content, and preservation
  state. No removed, deferred, or superseded target row may disappear from the
  approved denominator.
- MAIN_RECONCILIATION_COMPLETE: E's independent plan passes.
- ADDITIONAL_SOURCE_PRESERVED(source): that one Operation F source, bound by exact
  canonical/final path and physical identity in F's approved immutable source
  manifest, has an Operation F live capture with VERIFIED_CLEAN_CLOSEOUT in the shared
  register, maintenance restored where F suspended it, no F-caused BLOCKED_RECOVERY
  remaining, a passing final capture receipt, and every Section 14.1 Gate F
  whole-tree, encryption, off-machine, and isolated-restore check passing for that
  exact source. The outcome is defined per source. This plan defines no aggregate over
  an Operation F source set; an aggregate claim would require a later amendment naming
  an exact closed set and reviewed under Section 1.1.
  ADDITIONAL_SOURCE_PRESERVED(source) is not an input to PRESERVATION_COMPLETE,
  neither contributes to nor blocks it, and authorizes no Operation B, D, or E step.
- DRIVE_ROOT_CHILD_RETIRED(root): that one Operation G root, bound by exact
  canonical/final path and physical identity in G's approved immutable target
  manifest, has ADDITIONAL_SOURCE_PRESERVED(source) already proved for an Operation F
  source whose exact identity is that same root, has a VERIFIED Operation G attempt
  under Section 14.2's adopted Section 6 state machine with the complete Section 4.4
  clean-closeout protocol and final root receipt, is absent from its original path, is
  exact in its operation-specific nonexistent same-volume quarantine destination, and
  is independently recoverable off-machine from the stored secret. The outcome is
  defined per root. This plan defines no aggregate over Operation G roots. It does not
  alter, satisfy, or contribute to MALFORMED_ROOT_QUARANTINED(root),
  MALFORMED_ROOTS_QUARANTINED, PRESERVATION_COMPLETE, PREVENTION_COMPLETE,
  TRIAGE_COMPLETE_NO_REMOVAL_AUTHORIZED, WORKTREE_SLICE_COMPLETE,
  WORKTREE_SLICE_PARTIAL_CLOSED, or WORKTREE_CLEANUP_COMPLETE, and is not part of any
  of them.

After each operation/slice, perform a normal guarded development observation
appropriate to its scope. Database bytes may legitimately change during normal app
use; capture a new closeout family and inspect only disposable copies rather than
claiming it still equals the pre-resume snapshot. Protected environment members,
Git/ref relationships, guard installation, quarantines, and unexpected drive-root
children must remain consistent with their closeout manifest. For an unexpected
drive-root child that belongs to no operation's manifest, that requirement is met when
its Section 14.3 register entry is unchanged at its recorded identity at closeout.
Every operation and slice also performs the Section 14.3 delta comparison: a no-follow
explicit-stack enumeration of the configured drive roots (Section 5.2) against the
owner-approved baseline union the Section 14.3 register as frozen at that operation's
start, failing on any child newly created during the operation.

At retention exit, reverify off-machine access, ciphertext hashes, both recovery
custody copies, decryption, protected Git OIDs, and representative data restoration.
Permanent archive/quarantine deletion and any branch/ref retirement are separate
operations with new exact manifests. Nothing expires automatically.
Preserving a source under Operation F grants no quarantine, relocation, or removal
authority for it. No Operation F receipt, Operation B receipt, Operation C receipt,
Operation D receipt or campaign target set, approval record, or baseline entry in this
plan authorizes an Operation G step; Operation G authority exists only under its own
dated Section 4.3 owner approval, created separately from and after this plan text.
Operation G's route is archive plus non-overwriting same-volume quarantine and never
recursive deletion, so completing it deletes nothing. Permanent deletion of an
Operation F preservation object or an Operation G quarantine payload remains a
separate later operation with its own exact manifest and owner approval, exactly as
for B and C above.

## 12. Open owner decisions before execution

- [x] Approve Gate 0 requirements (requirements only; signed 2026-09-05).
- [ ] Approve the Gate 1 council-reviewed version of this plan.
- [x] Approve Operation A Plan v2 at Gate 1 (signed 2026-09-05); this approved neither
      B-G execution nor any later semantic amendment to this design.
- [ ] Approve the renewed plan-level Gate 1 that Section 1.1 requires after each later
      semantic amendment to this design.
- [ ] Complete Section 5.4's outstanding conditions as that section states them,
      including installation and verification of the owner-approved user-level
      guard/memory updates; satisfy Section 11's PREVENTION_COMPLETE requirement that
      lifecycle monitoring is active; complete the outstanding post-merge
      required-check disposition recorded in the dated operation evidence; and
      reconcile any successor of the reviewed guard and test artifact against the
      reviewed bytes before the deployment decision.
- [ ] Select the human Windows-filesystem/mutation-surface reviewer.
- [ ] Select the no-follow copy/archive tools and prove their exact Windows behavior.
- [ ] Select authenticated encryption, private off-machine versioned storage, and
      two independent recovery-secret custody locations.
- [ ] Select the durable owner-approval record and SHA-256 manifest/package-digest
      procedure described in Section 4.3.
- [ ] Select operation evidence, restore, and same-volume quarantine roots.
- [ ] Select the single shared B-G coordination lock/register root and verify its
      canonical path, non-reparse parent, and access boundary.
- [ ] Approve user-level guard/memory changes and the worktree lifecycle mechanism.
- [ ] Approve C's exact preservation/ref-creation manifest and digest, including every
      append-only archive ref, OID, freeze budget, and safe-abort boundary; this is
      distinct from Gate 1 and from D.
- [ ] Approve and scratch-drill the Section 4.5 common recovery playbooks before each
      operation's first applicable live mutation.
- [ ] Resolve active PR, ownership claim, process, dirty-source, database, local-file,
      nested-repository, and ordinary-environment dispositions.
- [ ] Approve the complete KEEP/DEFERRED table and a digest-bound, positive, non-empty,
      immutable D campaign target set, or explicitly record
      TRIAGE_COMPLETE_NO_REMOVAL_AUTHORIZED.
- [ ] Approve each slice's candidate order, duration, maintenance window, storage
      estimate, preservation objects, retention date, and human executor.
- [ ] Decide whether and when to commission the separate E main-reconciliation plan.
- [ ] Decide whether to commission an Operation F additional-source preservation
      (Section 14.1) for an exact, closed set of unexpected drive-root children
      outside approved operation scope, and approve its Section 4.3 manifest, capacity
      requirement, freeze budget, and Operation-F-specific maximum freeze duration. No
      source is proposed or approved by this plan.
- [ ] Decide separately and later whether to commission an Operation G retirement
      (Section 14.2) for any such child whose ADDITIONAL_SOURCE_PRESERVED(source) is
      already proved, and approve its Section 4.3 target manifest, retention start,
      and per-object retention period. No root is proposed or approved by this plan.
- [ ] Maintain the Section 14.3 known-unexpected register. Each entry is recorded,
      amended, or removed by owner decision only, and the register is frozen for the
      duration of each operation.

Operation A's reviewed guard and test source is merged. Section 5.4's merge condition
is a conjunction: it additionally requires that Operation A implement the approved
subplan and pass every Section 4.5 implementation gate.

## 13. Review dispositions

### 13.1 Third-pass dispositions

The third pass incorporated the independent review by:

- separating prevention, malformed-root quarantine, preservation, removal slices,
  and main reconciliation;
- removing volatile counts and SHAs from the approval contract;
- defining a positive, squash-aware obsolete/eligibility rule;
- separating evidence-driven eligibility, owner disposition, immutable attempt
  results, and aggregate completion state;
- explicitly anchoring every per-worktree-admin-only commit and comparing protected
  OID sets;
- requiring direct frozen-source-to-restoration equality and verification of
  pre-existing bundles;
- replacing the universal native-argv hook claim with a bounded enforceable guard;
- replacing campaign-wide locks/freezes with short independent slices;
- using one shared B-E coordination lock/register that remains blocked after any
  unresolved live attempt;
- removing nonce verifiers, per-record hash chaining, and per-candidate external
  anchoring while retaining the then-required signed-manifest/external-trust model,
  durable journal, and REMOVE_INVOKED boundary;
- defining an isolated fault-injection architecture and deferring normal repository
  collection until runtime data is preserved;
- adding recovery-secret acceptance criteria and private-by-default source handling;
- requiring the then-separate signed authorization for C's append-only archive refs
  and a collision-safe, independently locked E plan; and
- requiring the previously missing human Windows-filesystem review before execution.

The disputed review counts are deliberately not repeated. Execution relies only on
fresh manifest-enumerated state.

### 13.2 Fourth-pass Astra and Opus dispositions

The fourth pass accepts the preservation recommendations and reduces the number of
mechanisms the owner must operate correctly:

- adds the Gate 0 rollout order prominently without changing the later technical
  independence of B, C, D, and E;
- adds an explicit single-owner/concurrent-session threat model and removes detached
  signatures, external manifest anchors, coordination-prefix hashes, and the
  reacquire-to-prove-release finalizer that did not mitigate an in-scope threat;
- retains immutable digest-bound manifests, direct owner approval, one exclusive OS
  lock, durable journals, exact path checks, authenticated encryption, off-machine
  preservation, and source-to-restoration equality;
- makes the worktree lifecycle view a projection of Git registration, no-follow
  filesystem discovery, and fallible owner annotations, with self-reporting recovery
  when Git creation succeeds before annotation writing;
- requires new-worktree.ps1 copy-current to create and validate a SQLite-native
  consistent snapshot instead of copying database.db without its active WAL state;
- gives C and D measured, owner-approved maximum freeze budgets and explicit safe-
  abort boundaries;
- requires common recovery playbooks and scratch fault-injection drills before the
  first related live mutation, while retaining incident-specific approval for an
  actual repair; and
- uses fresh merged-PR metadata and exact PR-head OID matching to accelerate squash-
  aware disposition without treating PR state as removal authority.
## 14. Drive-root children outside Operations B and C

### 14.0 Scope, terminology, authority, and receipts

**The term.** Sections 8.3 and 11 use the noun unexpected drive-root child, and this
section uses it in exactly that sense: a drive root's child that the owner-approved
drive-root baseline does not list. Two adjacent terms elsewhere are deliberately left
unrenamed because their senses differ: Section 5.1's "unintended drive-root child" is a
causal description of how path conversion creates one, and Section 6's "other
unexpected root" is discriminated against the configured drive-root allowlist rather
than against the baseline. No second noun is minted here.

**The scope qualifier, defined once.** An unexpected drive-root child is outside
approved operation scope when, evaluated by exact canonical/final path and physical
identity rather than by name, prefix, proximity, or any alias form Section 2.2 rule 8
rejects, it is neither of Operation B's two named roots nor enumerated in an approved
operation source or target manifest. This is the only place the qualifier is defined.
The noun is fixed by the owner-approved baseline; only the qualifier depends on
manifest approval, and it is the qualifier - never the noun - that stops applying when
a manifest is approved, because no manifest approval edits that baseline. The term
"unapproved drive-root child" is deliberately not used: it would go false at the moment
of manifest approval while "unexpected" must stay true, splitting the Section 8.3 and
Section 11 checks from the Section 5.2 audit.

**No implicit authority over any unexpected drive-root child.** Proximity to a named
root, a generated-output classification, a filesystem creation time, a previous
campaign's completion receipt, and every existing aggregate, receipt, approval record,
manifest, and baseline entry in this plan confer no preservation, relocation,
quarantine, or removal authority over any unexpected drive-root child, whether or not
it is outside approved operation scope. Authority exists only where this plan names it
explicitly - Operation B for its two named roots - or under a dated Section 4.3 owner
approval record for an operation of this section, created separately from and after
this text. This section approves nothing, names no source and no target, and widens no
existing approval. Completing either operation of this section changes no
PREVENTION_COMPLETE declaration, permits no edit to the owner-approved drive-root
baseline, and permits no zero exit from the Section 5.2 audit.

**Prevention first.** Operations F and G each require PREVENTION_COMPLETE in addition
to their own approvals. Operation A is the prevention operation for the very defect
that creates unexpected drive-root children, and an operation freeze that ran before
prevention was complete could itself create one, which the Section 8.3 and Section 11
delta checks would then correctly fail. Beyond that precondition, F and G may be
commissioned at any point after the owner-accepted stabilization checkpoint and fresh
evidence, independently of whether B, C, or D has been approved or scheduled.

**Operation B is unchanged.** MALFORMED_ROOT_QUARANTINED(root) and
MALFORMED_ROOTS_QUARANTINED continue to mean exactly Operation B's two named roots and
nothing else; Section 4.3's binding of exactly one malformed-root identity to a B
approval is unchanged; and no Operation B receipt, approval record, or quarantine
destination may cover any other root. An Operation G approval is never an Operation B
approval, and an Operation G launcher may not emit an Operation B outcome name.

**Operation D is unchanged, and the structural seal is stated rather than relied on.**
A drive-root directory can never satisfy Section 3.6 condition 1, which requires a
registered immediate child of the approved development parent; it can therefore never
be an ELIGIBLE row, can never record a Section 3.5 positive lifecycle basis, and can
never enter a Section 3.7 immutable cleanup target set. No drive-root directory can
affect WORKTREE_SLICE_COMPLETE, WORKTREE_SLICE_PARTIAL_CLOSED,
TRIAGE_COMPLETE_NO_REMOVAL_AUTHORIZED, or WORKTREE_CLEANUP_COMPLETE, in either
direction.

**Receipts are private by default.** An Operation F or Operation G manifest, journal,
and receipt necessarily bind an exact canonical/final path, a physical identity, and,
for F, an off-machine storage object. Those are private under Section 2.2 rules 16 and
17. Publish only a privacy-reviewed redacted receipt; no public receipt names a
drive-root child's exact path, physical identity, or off-machine storage object.

### 14.1 Operation F - separately approved additional-source preservation

No Operation F preservation authority exists for any source until every one of the
conditions below is true. Operation F preserves an approved closed set of exactly
identified unexpected drive-root children. Immediately before approval of that
Operation F manifest, an exact, retained eligibility assessment must establish that
every source in the set is outside approved operation scope under Section 14.0.
The ensuing approval enrolls only that same closed set by exact path and physical
identity. The scope qualifier then stops applying as Section 14.0 describes; neither
the sources' unexpected classification nor the owner-approved baseline changes.
Operation F is not a general route for arbitrary sources outside Operation C's scope,
and it is not an extension of Operation C's immutable source manifest: no Operation
C manifest, approval, receipt, freeze budget, or capacity approval is altered, reused,
or extended by it.

One Operation F operation binds one approved closed set. Its outcome is per source:
Section 11 defines ADDITIONAL_SOURCE_PRESERVED(source) and defines no aggregate over
the set, so no claim may be made over the set as a whole.

1. A Section 4.3 immutable, digest-bound manifest enumerates the exact, closed set of
   sources by canonical/final path and physical identity. Immediately before its
   approval, retain a digest-bound assessment of that exact set's Section 14.0
   outside-scope eligibility. A dated Section 4.3 owner approval record binds that
   assessment's digest and the same manifest, created separately from and after
   this plan text. It enrolls only the assessed identities and changes neither the
   owner-approved baseline nor the sources' unexpected classification. Wildcard or
   prefix expansion, source-to-source overlap, source-to-destination overlap,
   overlap with Operation C's approved scope, overlap with a previously approved
   Operation F source, a missing source, and a changed identity are each a rejection,
   not a warning.
2. Every obligation of Section 7.5 applies to each source in the set, unchanged, with
   only these two scope-specific deviations: Section 7.5's opening inventory paragraph
   governs Operation C's pre-stop runtime map, and Operation F substitutes its own
   approved source set; and Section 7.5's live-capture freeze release governs
   Operation C's capture phase, and Operation F releases its own. Nothing else in
   Section 7.5 is narrowed - including raw SQLite-family capture before any open,
   completed online backups and logical checks on disposable copies only, preservation
   of every manifest-enumerated startup snapshot before any app or test launch,
   preservation of ignored/untracked/local settings, handovers/claims, evidence, loose
   files, recovery/salvage directories and unique local payload, separate exact
   no-follow archives for every ordinary private environment with reconstruction
   versions and health output recorded without installing or repairing anything, the
   separate recording of volatile cache and log paths, and the authenticated
   encryption, two independent offline custody copies, and off-machine
   upload/download/verify/decrypt/compare regime.
3. Section 7.2 items 4 and 5 apply to each source as obligations: a no-follow cold
   copy or archive of the complete approved source, including loose files, directories
   and reparse entries recorded as inert metadata; and live-source manifests generated
   immediately before and after capture, required identical, and compared directly
   with the extraction - archive-to-itself or upload-to-download equality alone is
   insufficient.
4. Section 7.6 applies to each source: the first decrypted extraction is immutable
   evidence, a second disposable copy with no hardlinks is sanitized before any Git
   invocation, extraction rejects traversal and absolute/device/ADS entries, and
   whole-tree source-to-restoration equality is proved in a fresh isolated root. Each
   source is proved separately against its own extraction root; no union or aggregate
   comparison substitutes for a per-source proof. This section's restore gate over the
   complete approved set is named Gate F.
5. Any Git repository inside a source carries Section 7.3's OID enumeration and
   type-checking and Section 7.4's separate preservation and restore-test. Before
   approving the Operation F manifest, compute Section 7.3's archive-ref-need set
   read-only from durable named refs and retain the exact result with the approval.
   The set must be empty; a nonempty or unresolved set rejects the source under
   Operation F. Recompute it read-only against the frozen source immediately before
   capture; any nonempty result, unresolved result, or changed protected ref/OID set
   stops the capture under its approved safe-abort or recovery protocol. Operation F
   creates no archive ref or other live Git metadata. A source needing ref creation
   requires a separately reviewed plan and its own approval; this paragraph grants
   no such authority and never treats a reflog as a durable named ref.
6. Section 7.1's runtime map and writer-shutdown set are extended to each source, or
   the absence of a writer is positively recorded for it. An unresolved writer or an
   unresolved root blocks Operation F for that source exactly as it blocks Operation
   C.
7. Every member class present in each source - SQLite family, nested repository,
   reparse point, alternate data stream, long path - has been enumerated and
   characterized before approval, and the absence of each unlisted class is positively
   recorded. An uncharacterized member class makes the source unapprovable.
8. The capacity requirement and the freeze budget are calculated for the complete
   approved set, not per source in isolation, and re-measured immediately before
   writing under Section 7.2 item 3's margin. The owner re-approves the maximum freeze
   duration for this Operation F operation. A maximum approved for Operation C, or for
   an earlier Operation F operation, never carries over.
9. The Section 4.5 recovery playbook for Operation F is approved and its scratch
   drills pass before the first preservation write, and the Section 4.2 non-LLM human
   and Windows-filesystem review has been performed against the actual mutation
   surface with fresh scratch proofs for every path form a drive-root source
   introduces.

**States and abort branches.** Operation F adopts Operation C's safe-abort model. Its
safe-abort boundary is the first preservation write: before it, a failed checkpoint or
projected overrun cleanly aborts under Section 7.2's abort paragraph, retaining and
labelling partial outputs INVALID_INCOMPLETE, restoring maintenance, recording
ABORTED_NO_MUTATION, and closing out under Section 4.4. After it, the operation
finishes the minimum manifest-enumerated capture and clean closeout or enters
BLOCKED_RECOVERY under its pre-drilled Section 4.5 playbook. Operation F creates no
archive ref and no live Git metadata in the live repository.

**Closeout.** An Operation F closeout runs the complete Section 4.4 single-hold
clean-closeout protocol and, in addition, the Section 14.3 drive-root delta
comparison: a no-follow explicit-stack enumeration of the configured drive roots of
Section 5.2, compared against the owner-approved baseline union the Section 14.3
register as frozen at this operation's start, failing on any child newly created
during the operation.

**Failure isolation.** A defect, overrun, or unresolved identity on an Operation F
source aborts or blocks only that Operation F operation, under its own safe-abort
boundary and its own recovery playbook. It never aborts, blocks, delays, or alters
Operation C's D:\development capture; Section 7.2's abort branches govern Operation C
on its own scope. PRESERVATION_COMPLETE is unchanged by this section: it remains
Operation C's outcome, computed from Operation C's gates over Operation C's approved
scope only, so a pre-amendment and a post-amendment Operation C receipt remain
directly comparable. An Operation F failure does not block Operation D or Operation E;
it blocks only Operation G, and only for the source identities it failed to preserve.

### 14.2 Operation G - separately approved drive-root child retirement

Operation G is built on Operation B's per-root template: archive, then a single
ordered non-overwriting move of one exact root to a nonexistent operation-specific
same-volume quarantine destination. It never uses recursive deletion, never
copy-deletes, and never uses Operation D's worktree-removal transaction core.
Permanent deletion of a quarantine payload remains Section 11's separate later
operation.

Operation G adopts Section 6's forward states and terminal branches unchanged -
NOT_STARTED, PREFLIGHTED, AUTHORIZED, QUARANTINE_MOVE_INTENT, MOVE_RESULT,
QUARANTINED, VERIFIED, with ABORTED_NO_MUTATION and FAILED_NEEDS_RECOVERY on the same
branches and the same QUARANTINE_MOVE_INTENT boundary - reading "root" as the
Operation G root. It derives its own aggregate per root and never derives an Operation
B aggregate.

No Operation G retirement authority exists for a root until every one of the following
is true for that exact identity:

1. ADDITIONAL_SOURCE_PRESERVED(source) is proved for an Operation F source whose exact
   canonical/final path and physical identity are the same identity as this Operation
   G root. That equality is required; resemblance, adjacency, and a matching name are
   not sufficient.
2. Recovery has been proved with the stored secret for that exact source before the
   move - the proof Section 7.5 requires before a B quarantine move, a D removal, or
   an Operation G retirement move - by downloading the encrypted object into a fresh
   root off this machine, verifying ciphertext hashes, decrypting, extracting, and
   comparing exact member and hash sets.
3. An exact immutable, digest-bound, positive, non-empty target manifest names that
   one root and its single nonexistent same-volume quarantine destination.
4. Section 4.2's non-LLM human and Windows-filesystem review has been performed
   against that actual mutation surface, with fresh scratch proofs for every path form
   a drive-root source or quarantine destination introduces. A prior review of another
   operation's mutation surface does not satisfy it.
5. Section 4.3 manifest and production-package digest integrity are verified and the
   owner's approval is recorded in a durable approval record outside every source and
   candidate.
6. A Section 4.4 journal is kept, and the shared Section 4.4 coordination lock and
   shared attempt register are used on the same single-hold protocol as every other
   live launcher.
7. The Section 4.5 recovery playbook for Operation G is approved and its scratch
   drills pass before the first live mutation.
8. A retention start and a per-object retention period are stated, and Section 11's
   named retention-exit checks apply to the resulting quarantine payload.

Operation G uses its own thin root-quarantine launcher built from the same reviewed
template as Section 4.1 item 2, bound to its own approved single-root manifest, its
own journal, and Operation G's own outcome name. It is not Operation B's launcher and
cannot emit an Operation B outcome. A failure for one Operation G root does not
invalidate another root's completed operation, and no Operation G attempt overwrites a
prior attempt's evidence.

**Closeout.** An Operation G closeout runs the complete Section 4.4 single-hold
clean-closeout protocol, the final root receipt, and, in addition, the Section 14.3
drive-root delta comparison described for Operation F above. Because a completed
Operation G changes the drive-root enumeration, that comparison also reports the
retired root as absent at its recorded identity, and the owner dispositions its
Section 14.3 register entry at that closeout.

### 14.3 The owner-dispositioned known-unexpected register

The register is a durable owner record of unexpected drive-root children that are
already known and dispositioned as retained. It is an owner-approved artifact: each
version carries a SHA-256 digest, lives in an evidence root meeting Section 3.1's
conditions, and is bound by digest into the Section 4.3 approval of every operation
that will consume it and again into that operation's closeout receipt.

**What it changes.** Section 8.3's closeout check is "confirm no unexpected drive-root
child was created" - a delta over the operation window, not a census. The register
pins, by exact canonical/final path and physical identity, the set of unexpected
drive-root children already recorded before an operation began. A closeout therefore
compares a no-follow explicit-stack enumeration of the configured drive roots of
Section 5.2 against the owner-approved baseline union the register as frozen at that
operation's start, and fails on a child newly created during the operation. A
pre-existing registered child is not a closeout failure. A newly created child is a
closeout failure whether or not it resembles a registered entry. This comparison is
performed at every Operation B, C, D, F and G closeout: Section 8.3 states it for a D
slice, Sections 14.1 and 14.2 state it for F and G, and Section 11's post-operation
observation states it for every operation and slice. The register also gives Section
11's requirement that unexpected drive-root children "remain consistent with their
closeout manifest" a determinate meaning for a child that belongs to no operation's
manifest: each registered entry must be unchanged at its recorded identity at that
closeout.

**What it does not change.** The register does not clear, suppress, alter, or
reinterpret the Section 5.2 read-only drive-root audit, which continues to compare
configured drive roots against the owner-approved baseline and to report every
unexpected child. That audit's non-zero exit is unchanged and expected. A registered
entry is neither a reason to suppress that report nor a reason to ignore it. A
register entry is not a baseline entry: it is not added to the baseline, and it alters
none of the baseline's bytes, approver, approval timestamp, or RESOLVED meanings. It
is not a source-manifest entry and not a target-manifest entry. It confers no
preservation, relocation, quarantine, or removal authority, and it is not a
disposition any operation may act on. Section 6's post-operation observation of the
configured drive-root allowlist is likewise unaffected: detection is never suppressed.

**Its own integrity.** Each entry carries an exact canonical/final path and physical
identity, the owner's disposition, and the fact that the child is retained. An entry
is added, amended, or removed only by owner decision - never by an executor, an audit
run, a closeout, or an agent. The register is frozen for the duration of an operation,
from that operation's start through its closeout; the frozen version's digest is
recorded in that operation's Section 4.3 approval and again in its closeout receipt,
so the delta above is computable and an after-the-fact addition is detectable. When a
completed Operation G retires a registered child, the owner dispositions that entry at
that operation's closeout; until the owner does so, the entry stands and its recorded
identity is expected absent.
