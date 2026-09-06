---
description: Create a worktree with verified lifecycle, consistent SQLite seed and isolated launch setup.
---

Use the owner-created manager checkout for parallel work. Agents within one feature
stay in that checkout. Read [PARALLEL_WORKFLOW.md](../../docs/ai_workflow/PARALLEL_WORKFLOW.md)
and [WORKSTREAM_OWNERSHIP.md](../../docs/ai_workflow/WORKSTREAM_OWNERSHIP.md) first.

```powershell
.\scripts\new-worktree.ps1 -Task example -Seed empty -Owner '<owner>' -NextReviewDate '<future ISO-8601 date>' -TeardownCondition 'Retain until separately approved' -BaselinePath 'D:\approved\drive-baseline.json'
```

Supply the owner-approved baseline; the default annotation file is the Git main
checkout's `docs/ai_workflow/WORKSTREAM_OWNERSHIP.local.md`. Explicit `-RepoRoot`,
`-DevelopmentParent`, `-AnnotationPath`, `-PrMetadataPath` and `-PythonExecutable`
support approved layouts. Missing or inconsistent lifecycle/baseline information
blocks creation before registrations, refs or children change.

| Seed | Behavior |
|---|---|
| `visual` (default) | SQLite online backup of the visual fixture, validated and published without overwrite; missing fixture/helper fails. |
| `empty` | Requires absent target DB; the application's ordinary first launch bootstraps the catalog. No application is launched by the creator. |
| `copy-current` | Validated online SQLite backup, including committed WAL rows; never a base-file byte copy. |

`copy-current` source order is explicit `-SourceDatabase`, process `DB_FILE`, process
`HT_RUNTIME_DIR/data/database.db`, then the source checkout's `data/database.db`.
The selected absolute identity is verified and displayed; unavailable input never
falls through. Collision with a tracked or existing target refuses without changing
bytes or index flags. Synthetic acceptance never selects a live source.

Readiness follows Git creation, seed publication, target runtime verification, then
atomic final annotation. Failure after Git leaves the registered checkout and branch
in place and reports INCOMPLETE; the next audit exposes missing final annotation as
OWNERLESS. Review retained scratch; do not remove or prune it to conceal a failure.

Dot-source the exact emitted `artifacts/worktree/launch-worktree.ps1` before commands.
It sets process-only `HT_RUNTIME_DIR`, `DB_FILE`, temp, caches and bytecode paths to
the target. `-OpenTerminal` explicitly requests an interactive terminal with that
same setup. An unrelated new shell is not already isolated. Provision private
`.venv`/`node_modules`; do not install into shared environments.

Never set/export either MSYS suppression variable. Use PowerShell end to end,
separate argument arrays and drive-qualified native output paths. The bounded hook
does not inspect opaque script files or provide a native-process sandbox.

Completion, abandonment, KEEP and DEFERRED retain worktrees, branches/reflogs and
all recovery roots during the signed cleanup sequence. The owner records rationale
and a next review date; separate operation approval is required for retirement.
