# Operation A owner review and Windows acceptance

Status, 2026-09-05: disposable interactive Windows acceptance **PASSED**, as verified
in the [planning continuation](PLANNING.md#2026-09-05--verified-interactive-acceptance-and-local-integration-continuation).
The procedure below remains available for future reruns. External installation,
publication, merge and active lifecycle monitoring remain unverified. Gate 1 and
the bounded local integration authorization do not complete Gate A;
PREVENTION_COMPLETE remains undeclared.

## Repository behavior and migration

`new-worktree.ps1` now requires an owner, future review date, retention condition,
approved baseline and reconciled lifecycle annotations. Missing/unreadable suppression
scopes or unresolved/ownerless/overdue/unacknowledged rows refuse before Git mutation.
Tracked/existing target collisions refuse without modifying bytes or index flags.
`copy-current` uses online SQLite backup plus disposable-copy integrity/schema/version/
readability validation and no-overwrite publication; unavailable sources/helpers fail.
`visual` uses the same validation; `empty` requires an absent DB. No app is launched.

Source selection order is explicit `-SourceDatabase`, process `DB_FILE`, process
`HT_RUNTIME_DIR/data/database.db`, then source checkout `data/database.db`. The selected
absolute source identity is displayed. Target launch always overrides DB/runtime,
temp/cache/bytecode settings with target paths. Dot-source the emitted launch script;
an arbitrary new shell is not already isolated. Source process or persistent settings
are never modified. Provision private dependencies before installation/tests.

Final annotation follows seed publication and target runtime verification. An earlier
post-Git failure reports INCOMPLETE and retains the registered worktree, branch and
owned temporary evidence. A later audit reports OWNERLESS. An interruption after
durable annotation retains complete prerequisite-backed annotation. No automatic
remove/prune/ref retirement or scratch disposal occurs.

Application calculations, schema, response contracts, initialization and backup
rotation are unchanged. Preserve every discovered snapshot for this operation.

## Exact external deltas, not applied

The private review packet is
`artifacts/worktree-cleanup-planning/council-20260905/operation-a-owner-deltas.private.json`.
Each proposal names one exact path, the SHA-256 of its current bytes (null means
creation only), full proposed UTF-8 text, operation and rationale. The packet contains:

- A proposed `C:/Users/aviha/.claude/hooks/guard-destructive-command.ps1` and one
  `Bash|PowerShell` PreToolUse registration in the existing user settings, using
  `-GuardProfile main`. Preserve the guard's UTF-8 BOM and ASCII body. Project
  shell-agent registrations retain the stricter default `agent` profile.
- Exact corrections to active project memory index/reference and local handover
  advice. Historical incident commands remain visibly non-prescriptive evidence.
- Exact proposed current guidance for the measured retained checkouts. These are
  review proposals only; the owner must inspect each full replacement against its
  existing version and any private/local changes before application.

The bounded scan covers registered checkout status/worktree/parallel guidance and
local handovers plus the known Claude project memory directory and user settings.
The owner must declare any additional active memory, IDE, wrapper or retained-root
guidance before claiming the active-guidance gate complete. This packet is private;
do not publish user settings, full paths, memory or its plaintext hashes.

Before applying a row, recompute its exact source SHA-256 and require equality, or
require its creation target absent. Any mismatch requires a fresh reviewed delta.
Apply only approved rows, retain the prior bytes privately, use UTF-8 BOM for the
guard, and validate the resulting JSON/guard syntax. Do not overwrite unrelated
settings. No agent installs these changes or executes the proposed replacements.

The guard inspects bounded raw command text. It cannot inspect opaque script files,
aliases/functions, fully expanded argv, final executable identity or every child.
The Codex tool transport does not attest Claude hook interception. A direct harness
tests the guard, not installation; capture a real fresh Claude session's hook denial
and inert allow result separately after installation. Never execute historical
incident payloads; only submit them as serialized hook input.

## Proposed lifecycle/baseline installation choices

Proposed canonical annotations: the Git main checkout's existing gitignored
`docs/ai_workflow/WORKSTREAM_OWNERSHIP.local.md`, preserving its claim/history prose,
with exactly one fenced JSON block. Schema and strict fields are in
[WORKSTREAM_OWNERSHIP.md](../ai_workflow/WORKSTREAM_OWNERSHIP.md).

```json
{
  "schemaVersion": 1,
  "records": [{
    "identity": "<measured volume serial:file ID>",
    "path": "<exact ordinary registered worktree path>",
    "owner": "<owner>", "task": "<development>", "branch": "<short branch>",
    "createdAt": "<ISO-8601 with timezone>", "expectedPr": null,
    "teardownCondition": "Retain until separately approved operation",
    "nextReviewDate": "<future ISO-8601 with timezone>",
    "disposition": "KEEP", "rationale": "<owner-reviewed reason>",
    "activity": "UNKNOWN", "activityObservedAt": "<observation timestamp>"
  }]
}
```

Proposed private baseline location:
`D:/development/Hypertrophy-Toolbox-v3-main/artifacts/worktree-lifecycle/drive-baseline.json`.
Proposed development parent: `D:/development`. Proposed drive roots: `C:/` and `D:/`.
These are choices for owner approval; no live baseline is generated by this packet.
Enumerate direct entries without following reparses; classify unresolved entries
explicitly. Do not adopt unexpected content merely to obtain a green report.

```json
{
  "schemaVersion": 1, "approvedBy": "<owner>",
  "approvedAt": "<dated owner approval>", "developmentParent": "D:/development",
  "roots": [{"path": "D:/", "children": [
    {"path": "D:/development", "identity": "<measured volume serial:file ID>"}
  ]}]
}
```

The sample omits real children and the second root intentionally: it is a schema
example, never an approved baseline. Every actual direct child requires a row.
`Get-WorktreePathIdentity -Path <path>` reads volume/file identity through a Windows
handle after ordinary-ancestor checks; unsupported or reparse topology is unresolved.
This detects accidental replacement and is not an adversarial race-proof boundary.

Proposed monitoring: run read-only audit on every session start, before creator
mutation (already enforced), and once per day through an owner-installed Windows
scheduled task. Pin the merged checkout/script and use a fresh PowerShell process,
process-only scratch TEMP/TMP/cache settings and explicit arguments. Capture JSON,
stderr, exit code, timestamp and script hash in the private lifecycle artifacts
directory. Keep all reports; add no automatic rotation/deletion task during this hold.
The owner reviews nonzero/UNKNOWN/review rows before opening new developments.

```powershell
& 'C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe' -NoProfile -NonInteractive -File 'D:\development\Hypertrophy-Toolbox-v3-main\scripts\audit-worktrees.ps1' -RepoRoot 'D:\development\Hypertrophy-Toolbox-v3-main' -DevelopmentParent 'D:\development' -AnnotationPath 'D:\development\Hypertrophy-Toolbox-v3-main\docs\ai_workflow\WORKSTREAM_OWNERSHIP.local.md' -BaselinePath 'D:\development\Hypertrophy-Toolbox-v3-main\artifacts\worktree-lifecycle\drive-baseline.json'
```

This is the proposed audit command, not a task registration or execution instruction
for the current agent. Approve/install the task and wrapper after merge. Record the
task XML/action, exact paths/hashes, last result and a fresh emitted report. Optional
PR metadata expires after 24 hours and requires one exact PR-number/HEAD match;
unavailable/stale metadata stays UNKNOWN. PR state never grants removal authority.

## Owner-run disposable interactive Windows acceptance

Run after reviewing the final diff in a direct interactive PowerShell console. Use
the approved standalone checkout below and its existing private dependencies. No
live database, source checkout mutation, user-level setter or B–E launcher appears
in this procedure. Keep every created disposable root for inspection.

```powershell
Set-Location -LiteralPath 'D:\development\Hypertrophy-Toolbox-worktree-cleanup-plan'
. .\artifacts\worktree-cleanup-planning\council-20260905\isolated-env.ps1
$acceptanceRoot = Join-Path $env:TEST_ARTIFACTS_DIR ('owner-acceptance-' + [guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($acceptanceRoot) | Out-Null
$env:OPERATION_A_ACCEPTANCE_ROOT = $acceptanceRoot
& .\tests\worktree_cleanup\guard-contract.ps1
if ($LASTEXITCODE -ne 0) { throw 'Standalone guard acceptance failed' }
```

The harness enumerates installed Windows PowerShell 5.1/PowerShell 7, both profiles
and default/bypassPermissions. Unavailable hosts are named, never marked passed.
It serializes deny/allow payloads and never launches their named children.

Create an explicitly synthetic SQLite/Git fixture using the checked-in QA setup:

```powershell
$fixtureCode = @'
import json, os
from pathlib import Path
from tests.worktree_cleanup.support import fixture_repo
from tests.test_worktree_snapshot import database
root = Path(os.environ['OPERATION_A_ACCEPTANCE_ROOT'])
repo, annotations, baseline = fixture_repo(root, 'powershell')
database(repo / 'data' / 'database.db').close()
(root / 'fixture.json').write_text(json.dumps({'repo': str(repo), 'annotations': str(annotations), 'baseline': str(baseline)}), encoding='utf-8')
'@
& .\.venv\Scripts\python.exe -B -c $fixtureCode
if ($LASTEXITCODE -ne 0) { throw 'Synthetic fixture setup failed' }
$fixture = Get-Content -LiteralPath (Join-Path $acceptanceRoot 'fixture.json') -Raw | ConvertFrom-Json
$before = git -C $fixture.repo worktree list --porcelain -z
& .\scripts\preflight-worktree-environment.ps1 -ApprovedRoot $acceptanceRoot -RuntimeRoot $fixture.repo -DatabasePath (Join-Path $fixture.repo 'data\database.db')
if ($LASTEXITCODE -ne 0) { throw 'Fresh-scope preflight failed; owner must resolve it before proceeding' }
& .\scripts\new-worktree.ps1 -RepoRoot $fixture.repo -DevelopmentParent (Split-Path -Parent $fixture.repo) -AnnotationPath $fixture.annotations -BaselinePath $fixture.baseline -Task interactive -Seed copy-current -SourceDatabase (Join-Path $fixture.repo 'data\database.db') -PythonExecutable (Join-Path $PWD '.venv\Scripts\python.exe') -Owner 'owner-acceptance' -NextReviewDate ([DateTimeOffset]::UtcNow.AddDays(1).ToString('o')) -TeardownCondition 'Retain disposable acceptance until separate approval' -OpenTerminal
if ($LASTEXITCODE -ne 0) { throw 'Creation incomplete: retain every registered root and inspect the report' }
git -C $fixture.repo worktree list --porcelain -z
```

If Windows Terminal is unavailable, record that limitation and retain the prior
acceptance root. In the same source console (where `$fixtureCode` is defined above),
build a fresh fixture and invoke the explicit manual alternative:

```powershell
$acceptanceRoot = Join-Path $env:TEST_ARTIFACTS_DIR ('owner-acceptance-manual-' + [guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($acceptanceRoot) | Out-Null
$env:OPERATION_A_ACCEPTANCE_ROOT = $acceptanceRoot
& .\.venv\Scripts\python.exe -B -c $fixtureCode
if ($LASTEXITCODE -ne 0) { throw 'Fresh synthetic fixture setup failed' }
$fixture = Get-Content -LiteralPath (Join-Path $acceptanceRoot 'fixture.json') -Raw | ConvertFrom-Json
& .\scripts\new-worktree.ps1 -RepoRoot $fixture.repo -DevelopmentParent (Split-Path -Parent $fixture.repo) -AnnotationPath $fixture.annotations -BaselinePath $fixture.baseline -Task interactive -Seed copy-current -SourceDatabase (Join-Path $fixture.repo 'data\database.db') -PythonExecutable (Join-Path $PWD '.venv\Scripts\python.exe') -Owner 'owner-acceptance' -NextReviewDate ([DateTimeOffset]::UtcNow.AddDays(1).ToString('o')) -TeardownCondition 'Retain disposable acceptance until separate approval'
if ($LASTEXITCODE -ne 0) { throw 'Creation incomplete; retain this fixture and inspect the error' }
$target = Join-Path (Split-Path -Parent $fixture.repo) 'fixture-interactive'
$launchPath = Join-Path $target 'artifacts\worktree\launch-worktree.ps1'
Write-Output ("Open a separate PowerShell console and run: . '" + $launchPath.Replace("'", "''") + "'")
```

Run that exact emitted dot-source command in the separate console. Do not dot-source
it in the source console, which retains the fixture variables for the audit below.
In the opened target terminal, inspect `$env:DB_FILE`, `$env:HT_RUNTIME_DIR`,
`$env:TEMP`, `$env:npm_config_cache` and `$env:PYTHONDONTWRITEBYTECODE`. All paths must
point into `fixture-interactive`, and bytecode is `1`. Open no application. The
source console's original DB/runtime variables must remain unchanged.

Run this exact read-only audit from the source console and inspect its final
annotation. Because
this deliberately small fixture baseline watches the development directory itself,
the newly created child is reported UNEXPECTED until the owner explicitly reviews
its identity and updates that disposable baseline. The final registered annotation
must exist regardless; baseline drift is not permission to remove anything.

```powershell
$auditText = & powershell -NoProfile -NonInteractive -ExecutionPolicy Bypass -File .\scripts\audit-worktrees.ps1 -RepoRoot $fixture.repo -DevelopmentParent (Split-Path -Parent $fixture.repo) -AnnotationPath $fixture.annotations -BaselinePath $fixture.baseline
$auditExit = $LASTEXITCODE
$audit = $auditText | ConvertFrom-Json
$target = Join-Path (Split-Path -Parent $fixture.repo) 'fixture-interactive'
$targetRow = @($audit.rows | Where-Object { $_.path -eq $target -and $_.registered })
if ($targetRow.Count -ne 1 -or $targetRow[0].status -ne 'ANNOTATED' -or $targetRow[0].annotation.owner -ne 'owner-acceptance') { throw 'Final annotation missing or inconsistent' }
if ($auditExit -ne 1 -or @($audit.driveRoots | Where-Object { $_.path -eq $target -and $_.status -eq 'UNEXPECTED' }).Count -ne 1) { throw 'Expected disposable baseline drift was not reported' }
$auditText
Write-Output 'Expected audit exit 1: retained new child is UNEXPECTED to the old disposable baseline; creation and final annotation succeeded.'
```

Keep this audit result as evidence. Do not treat its intentional baseline-drift exit
as failed creation or auto-update the baseline merely to obtain a zero exit.

Finally run the five-module behavioral suite in the isolated checkout. It proves
active WAL rows, coherent concurrent transactions, timeouts/corruption/collisions,
interruption before/after publication and annotation, concurrent writers, unknown
metadata, no-follow discovery, scope inheritance and actual launch resolution:

```powershell
& .\.venv\Scripts\python.exe -B -m pytest tests/test_guard_destructive_command.py tests/test_agent_workflow_contracts.py tests/test_worktree_environment_preflight.py tests/test_worktree_snapshot.py tests/test_worktree_lifecycle.py -q
if ($LASTEXITCODE -ne 0) { throw 'Behavioral acceptance failed' }
```

After owner installation, open a fresh direct PowerShell session and run the
self-contained installed-guard/scope check below; it requires no variables from
the acceptance console and opens no database:

```powershell
Set-Location -LiteralPath 'D:\development\Hypertrophy-Toolbox-worktree-cleanup-plan'
. .\artifacts\worktree-cleanup-planning\council-20260905\isolated-env.ps1
$freshRoot = Join-Path $env:TEST_ARTIFACTS_DIR ('installed-scope-check-' + [guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($freshRoot) | Out-Null
& powershell -NoProfile -NonInteractive -ExecutionPolicy Bypass -File .\scripts\preflight-worktree-environment.ps1 -ApprovedRoot $freshRoot -RuntimeRoot $freshRoot -DatabasePath (Join-Path $freshRoot 'database.db')
if ($LASTEXITCODE -ne 0) { throw 'Installed fresh-session Process/User/Machine scope check failed' }
& .\tests\worktree_cleanup\guard-contract.ps1 -GuardPath 'C:\Users\aviha\.claude\hooks\guard-destructive-command.ps1'
if ($LASTEXITCODE -ne 0) { throw 'Installed user guard failed its direct contract' }
```

The isolation setup does not clear either suppression variable. The preflight reads
their fresh inherited Process values and both persistent scopes independently.
Verify installed settings/agent registrations, guard BOM/hash and actual hook
interception. Record live lifecycle reporting/task evidence separately. Repository
tests cannot attest those external facts. Merge and owner Gate 2/publication approval
remain separate; do not push the standalone clone's source-pointing origin.
