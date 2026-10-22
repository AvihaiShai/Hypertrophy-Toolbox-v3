# Repository safeguards — S2 activation record

Prepared on 2026-10-22 (Asia/Jerusalem) from fetched `origin/main`
`155181d67a89fe72e86c75a1ff438caec250a9bd`. Definitions and prerequisites are
[PLANNING.md](PLANNING.md) §§4, 6 and 7. This packet records the bounded S2
execution and prepares the remaining settings for the owner.

## Authority and isolation

The owner's commission permits C5 and enabling secret scanning, followed by push
protection after the baseline alert triage is clean or every alert is dispositioned.
The shared claims announcement, full before/after API readbacks and a previously
tested rollback command are mandatory for each authorized change. CodeQL default
setup, alert rules, emergency bypass, C2 strict and C3 Actions policy remain
**prepare-only**. C4 is unchanged and belongs to S1 and the owner. No merge, release,
credential, visual-baseline change or public seeded proof is authorized here.

Work uses standalone clone `D:\development\Hypertrophy-Toolbox-v3-settings-20261022`
and branch `docs/s2-settings-activation-20261022`. Git common/admin storage is the
clone's own `.git`, with no alternates or linked worktrees. Dependencies, DB/runtime,
logs, caches, bytecode path and TEMP are private; TEMP is 81 characters. No app server
was launched. Live claims and applicable freezes were checked before writes; the
dirty shared checkout was used only for reads and S2's locked claim announcements.
Operation A/recovery holds continue. Retain clone, branch and private evidence until
separately approved; next review 2026-11-22.

## Baseline and execution receipts

Full API receipts at `2026-10-21T21:40:58Z–21:41:04Z` matched the supplied snapshot:
public repository; strict false; 12 required contexts/checks, each bound to app 15368;
admin enforcement false; secret scanning, push protection, validity checks,
non-provider patterns and Dependabot security updates disabled; CodeQL not configured;
no rulesets; Actions enabled/all/SHA false; orphan workflow 345538425 active with one
historical run. CodeQL already reported the target languages/default suite while
unconfigured. The current workflow census is 99 remote uses, superseding B1's dated95.

Before each executed mutation, the immediate full readback and rollback prerequisite
were captured again. Private `artifacts/settings-s2/execution/` retains full request
bodies, HTTP response headers/bodies, stderr, exit status and UTC timestamps.
`settings-author/before/` retains the initial full settings snapshots. No alert value
or credential is published in this record.

| Operation | Before | Executed UTC / result | Verified after |
|---|---|---|---|
| C1 secret scanning | disabled; push protection disabled | 2026-10-21T21:43:46Z; PATCH200 | scanning enabled; other four security fields unchanged |
| C5 orphan 345538425 | active; historical run33274031928 | 2026-10-21T21:43:49Z; PUT204 | disabled_manually; same run remains retrievable |
| C1 push protection | scanning enabled; protection disabled; clean refreshed alert inventory | 2026-10-21T21:50:09Z; PATCH200 | both enabled; other security fields unchanged |

Dependabot security updates stay **disabled** under D-6. Validity checks and
non-provider patterns stay disabled. Branch protection, C4, CodeQL and Actions policy
remain unchanged. C1 as a whole is **partial**, because CodeQL setup and its baseline triage,
native enforcement and seeded/bypass proof remain unexecuted.

### Secret-scanning triage and delegated disposition

Pre-enablement HTTP404 alert responses were unavailable baseline data, never zero.
After enablement, all/default-pattern, explicit open and explicit resolved alert lists
each returned HTTP200 with zero alerts and complete pagination (no next-page Link),
at `2026-10-21T21:44:25Z–21:44:27Z`. No returned alert required an individual disposition.
Raw responses with `hide_secret=true` remain private under
`c1-triage/after-enablement-01/`.

Scan history returned HTTP404 with Advanced Security unavailable. A fresh request with
API version2026-03-10 also returned404. This is **not historical-scan completion
evidence**; empty inventories and elapsed time do not prove a completed backfill or
historical absence of secrets. [GitHub scan-history API](https://docs.github.com/en/rest/secret-scanning/secret-scanning#get-secret-scanning-scan-history-for-a-repository).

**DELEGATED — proceed on the clean observed alert inventory.** Three independent
read-only advisers (architecture, testing, security/product risk) each recommended
that the user's alert-triage condition is satisfied by successful complete enumeration
of the available enabled-scope alerts. The parent adopts that reasoned classification;
it is not an owner signature. Initial historical completion is unverified and was not
added as a new prerequisite. No stated check was waived, no completion evidence was
invented and no prepare-only authority was expanded. Historical detection and incoming
push prevention remain distinct. [GitHub push-protection enablement](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/prevent-future-leaks/enable-push-protection).

The three reports are retained privately as `artifacts/settings-s2/advisers/`:
`architecture.md`, `testing.md`, `security-risk.md`; each quotes the owner's delegation
verbatim. `delegated-disposition.json` binds their hashes, rationale, rollback evidence
and announcement. The preparer's stronger historical-completion recommendation was
explicitly considered and not adopted as an unstated owner condition.

The shared locked claims announcement was published at `2026-10-21T21:49:35Z`, before
activation. A fresh all/open/resolved collection immediately before activation again
returned200, complete pagination and zero alerts (`c1-triage/before-push-protection/`).
The full immediate before/mutation/after repository objects confirm only the push
protection field changed. Any later surfaced finding still needs private triage;
this record certifies neither completed historical scanning nor absence of secrets.
Push protection's rejection behavior was not exercised with a seeded public push.

Full final readbacks at `2026-10-21T21:50Z` compare equal to the original
full objects for branch protection, required checks, Actions policy, CodeQL setup,
rulesets, effective main rules and Dependabot security updates. The repository security
object equals exactly the two authorized enablement deltas. `gh workflow list --all`
confirms C5 disabled_manually and the run-history API retains run33274031928.
Private comparison results are in `artifacts/settings-s2/final-readbacks/`.

### Rollback evidence recorded before execution

At `2026-10-21T21:42:34Z–21:42:37Z`, six invocations of the actual PowerShell
`settings-author/rollback.ps1` passed loopback transport tests through `gh`. The fixture
asserted each method, exact repository path, JSON body, Accept and API-version header,
using dummy tokens and an empty CLI configuration. No authorization header was logged.
The complete transcript predates the authorized mutations. Execution records bind
its SHA-256 and the rollback script's SHA-256.

Tested commands: C5 enable; separate push-protection disable and scanning disable;
C2 strict false; CodeQL not-configured; C3 effective all-actions/SHA-false restoration.
This proves command transport/payload construction. **No live GitHub restoration was
exercised**; fixture success does not establish live entitlement, API acceptance or
complete operational reversibility. Rule-disable rollback is documented but not
transport-tested. Standalone inline equivalents are provided below and their shell
form is distinguished from the tested helper.

## Exact request bodies, expected readbacks and rollbacks

The C1a/C5 commands below preserve the executed requests for audit; their receipt table
above governs actual state. Every other mutation is a proposal requiring separate
owner approval. Refresh the corresponding full readbacks immediately before any
future apply/rollback and reconcile drift. Preserve other sessions' settings.

To reproduce file-input commands, create the private directories below and save each
exact JSON block under its stated filename in `$Body`; do not assume ignored artifacts
exist in a fresh clone. Rollback helper invocations refer to retained private evidence;
the standalone equivalent commands at the end require no helper.

Use PowerShell in the standalone clone:

```powershell
$Repo = 'AvihaiShai/Hypertrophy-Toolbox-v3'
$Settings = 'artifacts/settings-s2/settings-author'
$Body = Join-Path $Settings 'request-bodies'
$Headers = @('-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: 2026-03-10')
New-Item -ItemType Directory -Path $Body -Force | Out-Null
```

### C1 secret scanning and push protection

Apply scanning first using `c1-secret-scanning-enabled.json`:

```json
{"security_and_analysis":{"secret_scanning":{"status":"enabled"}}}
```

```powershell
gh api --method PATCH "repos/$Repo" @Headers --input (Join-Path $Body 'c1-secret-scanning-enabled.json')
gh api "repos/$Repo" @Headers
gh api "repos/$Repo/automated-security-fixes" @Headers
```

The expected delta is scanning enabled. Keep Dependabot security updates disabled under D-6 and leave validity/non-provider features at their current values. After baseline alert triage is clean or every alert is dispositioned, announce push protection in the shared claims file before applying its separate body:

```json
{"security_and_analysis":{"secret_scanning_push_protection":{"status":"enabled"}}}
```

```powershell
gh api --method PATCH "repos/$Repo" @Headers --input (Join-Path $Body 'c1-push-protection-enabled.json')
gh api "repos/$Repo" @Headers
```

Expected scanning and push protection enabled, other features unchanged. Native API support for these independently scoped status fields is documented in [Update a repository](https://docs.github.com/en/rest/repos/repos?apiVersion=2026-03-10#update-a-repository). Alert contents and dispositions remain private.

Rollback commands already recorded and transport-tested before any root mutation:

```powershell
# Reverse dependency order if restoring both settings.
& (Join-Path $Settings 'rollback.ps1') -Action PushProtectionDisabled
& (Join-Path $Settings 'rollback.ps1') -Action SecretScanningDisabled
```

Each rollback is a PATCH of that single setting to disabled. Read the full repository object and Dependabot state afterward; retain the triage record. This does not retract prior notifications or alerts.

### C1 CodeQL and native alert rule — prepare only

The exact default-setup body is:

```json
{"state":"configured","query_suite":"default","languages":["python","javascript-typescript","actions"]}
```

```powershell
gh api --method PATCH "repos/$Repo/code-scanning/default-setup" @Headers --input (Join-Path $Body 'c1-codeql-default.json')
gh api "repos/$Repo/code-scanning/default-setup" @Headers
```

Expected configured state, default suite and exactly those languages. Wait for real analysis and baseline triage; an accepted asynchronous request is not proof of completed scanning. [Default setup REST API](https://docs.github.com/en/rest/code-scanning/code-scanning?apiVersion=2026-03-10#update-a-code-scanning-default-setup-configuration) supports these values. Rollback uses `rollback.ps1 -Action C1CodeQLNotConfigured`, then GET verifies `not-configured`; scan results and run history may remain.

*C1b/C1c completion addendum, 2026-10-22 (read-only lane; nothing activated).* The PATCH returns 200 `{}` or 202 with `run_id`/`run_url`; on 409 wait and re-read, never re-PATCH. GET default-setup has no progress field and cannot prove analysis: completion is one error-free CodeQL analysis per language category on `refs/heads/main` at a recorded SHA (`code-scanning/analyses`). The readback also asserts `threat_model: remote`, `runner_type: standard` and `runner_label: null`. **Rollback order:** while the C1c rule is active, disable it before setting default setup to `not-configured`; otherwise every PR into `main` is blocked ("A required tool is not configured for the repository"). Default setup is not subject to the allowed-actions policy ([changelog](https://github.blog/changelog/2025-11-25-code-scanning-default-setup-bypasses-github-actions-policy-blocks/)), so C1b and C3 are order-independent and need no CodeQL allowlist entry. Owner decision package: `artifacts/c1bc-codeql-prep-20261022/C1BC_APPROVAL_PACKAGE.md` (private, shared checkout).

The separate native main-branch ruleset request `c1-codeql-main-rule.json` is:

```json
{
  "name":"C1 CodeQL newly introduced High/Critical on main",
  "target":"branch",
  "enforcement":"active",
  "conditions":{"ref_name":{"include":["refs/heads/main"],"exclude":[]}},
  "bypass_actors":[{"actor_id":58347128,"actor_type":"User","bypass_mode":"pull_request"}],
  "rules":[{"type":"code_scanning","parameters":{"code_scanning_tools":[{"tool":"CodeQL","security_alerts_threshold":"high_or_higher","alerts_threshold":"none"}]}}]
}
```

The owner ID was observed in both repository metadata and `GET /users/AvihaiShai`. This is the only bypass actor. A 2026-10-22 collaborators readback shows a second account, `avihayshai1989` (211789243), with write access; it is deliberately not a bypass actor, and a `RepositoryRole` write or maintain bypass would include it. `User` is in the 2026-03-10 bypass-actor enum ([changelog](https://github.blog/changelog/2026-05-07-repository-rulesets-user-bypass-and-branch-renaming/)); live acceptance is proved only by the POST response and a readback showing `current_user_can_bypass: pull_requests_only` for the owner. If the POST is rejected, nothing is substituted without a new owner decision. After scans/baseline triage and the independently reviewed proof design, the separately authorized owner could run:

```powershell
gh api --method POST "repos/$Repo/rulesets" @Headers --input (Join-Path $Body 'c1-codeql-main-rule.json')
# Set $RulesetId only to the numeric ID returned by this POST; retain its full response.
gh api "repos/$Repo/rulesets/$RulesetId" @Headers
gh api "repos/$Repo/rules/branches/main" @Headers
```

The [rules API](https://docs.github.com/en/rest/repos/rules?apiVersion=2026-03-10#create-a-repository-ruleset) supports User bypass with a numeric ID and PR-only mode, CodeQL thresholds and a main-ref condition. The rule needs analysis for the relevant commit and reference. The branch-protection admin exception does not demonstrate this bypass. Prove that a newly introduced High/Critical result blocks and that the recorded owner emergency PR procedure works; configuration readback is insufficient. The C1 proof design below requires separate approval before publishing any seed.

Safe rollback preserves the newly created ruleset as disabled:

```powershell
gh api --method PUT "repos/$Repo/rulesets/$RulesetId" @Headers --input (Join-Path $Settings 'rollback-bodies/c1-rule-disabled.json')
gh api "repos/$Repo/rulesets/$RulesetId" @Headers
```

Before rollback verify this is the exact newly created ruleset and that another session has not changed it. The body is `{"enforcement":"disabled"}`. Compare other rulesets unchanged. This restores no active C1 rule while retaining configuration evidence; it does not make the literal ruleset list empty.

### C2 strict — prepare only

```powershell
gh api "repos/$Repo/branches/main/protection/required_status_checks" @Headers
gh api --method PATCH "repos/$Repo/branches/main/protection/required_status_checks" @Headers --input (Join-Path $Body 'c2-strict-only.json')
gh api "repos/$Repo/branches/main/protection/required_status_checks" @Headers
gh api "repos/$Repo/branches/main/protection" @Headers
```

The body is exactly `{"strict":true}`. Expected strict true and exact current checks/contexts/app bindings preserved; all unrelated protection unchanged. Rollback is `rollback.ps1 -Action C2StrictFalse`, using only `{"strict":false}`. The [status-check protection API](https://docs.github.com/en/rest/branches/branch-protection?apiVersion=2026-03-10#update-status-check-protection) supports this partial update.

Refreshed read-only at 2026-10-22T15:27–15:35Z (main `b77cb742`, then `295f2acd` after docs-only #558): strict false; the same 12 checks, each `app_id` 15368; `enforce_admins` false; no rulesets. Protection and ruleset objects equal the 21:50Z S2 readback. GitHub's documentation does not say that a strict-only PATCH keeps omitted `checks`, so the immediate full readback is the proof, and any other difference triggers rollback. With `enforce_admins: false` the owner can still merge a behind PR as admin, and `allow_update_branch: false` does not hide *Update branch* when strict applies. Strict also voids a named-head merge approval whenever `main` moves first: the updated branch has a new head and needs fresh CI.

Recommendation: apply C2 after the WS5 workflow PR (slot 3) merges, in a window with no PR in its final merge sequence. Strict requires the branch to be up to date before merge, so activating during serial merges creates additional refresh/CI work. Refreshed payloads, expected objects, a GET-only pre-flight and the runbook are private under `artifacts/c2c3-activation-prep-20261022/` (shared checkout, gitignored).

### C3 selected actions and full SHA — prepare only

The policy body `c3-policy.json` is exactly:

```json
{"enabled":true,"allowed_actions":"selected","sha_pinning_required":true}
```

The separate inventory supplies the copied `c3-selected-actions.json` below. Its reviewed corpus has 99 direct remote references and three local reusable calls across six workflows / 39 jobs. No broad `actions/*`, deferred Codex/signing or unreviewed dependency is pre-allowed. Re-inventoried on 2026-10-22 at `b77cb742`: totals unchanged and no new `owner/repo@sha`. WS5's staged workflows (102 remote uses, 40 jobs) add none. GitHub documents that CodeQL default setup ([changelog](https://github.blog/changelog/2025-11-25-code-scanning-default-setup-bypasses-github-actions-policy-blocks)) and Dependabot update jobs ([Dependabot on Actions](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/about-dependabot-on-github-actions-runners)) bypass the Actions policy, so neither needs a pattern. Neither was tested here. `dynamic/dependabot/update-graph` is not documented either way; check it after activation. Also observe one default-setup run after C3 as live evidence.

```json
{
  "github_owned_allowed": false,
  "verified_allowed": false,
  "patterns_allowed": [
    "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
    "actions/dependency-review-action@a1d282b36b6f3519aa1f3fc636f609c47dddb294",
    "actions/download-artifact@9000827ccba6bdab643e8b6fd33ac0654aef8333",
    "actions/setup-node@949feb2413d6458794dcd2491c4babbbce0c15c1",
    "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",
    "actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9"
  ]
}
```

PLANNING §3 CI-D8 and §6 C3 name allowed *repositories*. A repository-level variant uses `actions/<repo>@*` for the same six repositories, with SHA pinning still required. It matches that wording and needs no allowlist change when Dependabot bumps an action. The exact-SHA list above instead blocks each such bump's CI until the owner adds the new SHA. The next likely bump is `actions/setup-python` v7.1.0, released 2026-10-22 and eligible about 2026-11-02. The owner chooses; both keep the two broad flags false and add no repository.

The live selected-actions GET returns HTTP 409 because the current policy allows all actions. [GitHub's selected-actions API](https://docs.github.com/en/rest/actions/permissions?apiVersion=2026-03-10#set-allowed-actions-and-reusable-workflows-for-a-repository) requires selected mode for its PUT as well as its GET. Therefore the command-sheet staging order cannot be executed literally through these endpoints; preparing/reviewing the allowlist is possible first, persisting it is not documented while all actions are allowed.

After owner approval and inventory review, apply three writes back to back, with no workflow run unfinished. First switch to `selected` with SHA pinning still off. Then read the hidden selected list once, the only moment it can be read. Then PUT the reviewed allowlist, and finally turn SHA pinning on. Read back after each write. Between the first and second writes the hidden list governs. Coordinate the activation so it cannot surprise another lane. On any failure, restore the effective before policy immediately and capture all error responses. The status-filtered runs list returned `total_count: 0` while a main push run was in progress, so a quiet window is judged from the unfiltered list.

```powershell
'{"enabled":true,"allowed_actions":"selected","sha_pinning_required":false}' | gh api --method PUT "repos/$Repo/actions/permissions" @Headers --input -
gh api "repos/$Repo/actions/permissions/selected-actions" @Headers --include   # retain: hidden list before this change
gh api --method PUT "repos/$Repo/actions/permissions/selected-actions" @Headers --input (Join-Path $Body 'c3-selected-actions.json')
gh api "repos/$Repo/actions/permissions/selected-actions" @Headers
gh api --method PUT "repos/$Repo/actions/permissions" @Headers --input (Join-Path $Body 'c3-policy.json')
gh api "repos/$Repo/actions/permissions" @Headers
```

Expected selected/SHA true and both broad flags false with exactly reviewed patterns. Observed execution of every caller remains an activation gate. Rollback: `rollback.ps1 -Action C3AllActions`, then GET policy shows enabled/all/SHA false and selected-actions returns the original 409. Because its before policy is hidden by 409, exact restoration of latent selected settings cannot be claimed; this restores effective before behavior. If the hidden list was captured during activation, a later quiet window can restore it exactly: switch to `selected`, PUT the captured list, then return to `all`. Without that capture, the hidden list keeps the installed allowlist, which has no effect while the mode is `all`.

### C5 orphan — authorized root execution only

```powershell
gh api --method PUT "repos/$Repo/actions/workflows/345538425/disable" @Headers
gh api "repos/$Repo/actions/workflows/345538425" @Headers
gh workflow list --all -R $Repo
gh api "repos/$Repo/actions/workflows/345538425/runs?per_page=100" --paginate @Headers
```

Expected `disabled_manually` and historical run `33274031928` still present. Never delete the workflow history or its run. The [workflow API](https://docs.github.com/en/rest/actions/workflows?apiVersion=2026-03-10#disable-a-workflow) documents disable and enable state changes. Rollback is `rollback.ps1 -Action C5Enable`, then GET must show active and preserved history.

### Rollback test boundary

The following standalone commands need no private helper script. Retain the full response, inspect errors and GET the readback after each command. They are the same method, endpoint and exact JSON as the tested helper's requests. Their inline-stdin shell form has not separately been transport-tested.

```powershell
$Repo = 'AvihaiShai/Hypertrophy-Toolbox-v3'
$Headers = @('-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: 2026-03-10')

# C5: restore the previously active orphan, without touching its run history.
gh api --method PUT "repos/$Repo/actions/workflows/345538425/enable" @Headers
gh api "repos/$Repo/actions/workflows/345538425" @Headers

# C1a: reverse push protection first if restoring both settings.
'{"security_and_analysis":{"secret_scanning_push_protection":{"status":"disabled"}}}' | gh api --method PATCH "repos/$Repo" @Headers --input -
'{"security_and_analysis":{"secret_scanning":{"status":"disabled"}}}' | gh api --method PATCH "repos/$Repo" @Headers --input -
gh api "repos/$Repo" @Headers
gh api "repos/$Repo/automated-security-fixes" @Headers

# C1c first: an active code-scanning rule blocks every PR once CodeQL is unconfigured.
# $RulesetId must be the numeric ID retained from the create response.
'{"enforcement":"disabled"}' | gh api --method PUT "repos/$Repo/rulesets/$RulesetId" @Headers --input -
gh api "repos/$Repo/rulesets/$RulesetId" @Headers
gh api "repos/$Repo/rules/branches/main" @Headers

# C1b only after C1c is disabled: restore unconfigured default setup; retained analyses may remain.
'{"state":"not-configured"}' | gh api --method PATCH "repos/$Repo/code-scanning/default-setup" @Headers --input -
gh api "repos/$Repo/code-scanning/default-setup" @Headers

# C2: preserve all current required check/app bindings.
'{"strict":false}' | gh api --method PATCH "repos/$Repo/branches/main/protection/required_status_checks" @Headers --input -
gh api "repos/$Repo/branches/main/protection/required_status_checks" @Headers

# C3: restore effective before policy; its hidden selected list was unreadable.
'{"enabled":true,"allowed_actions":"all","sha_pinning_required":false}' | gh api --method PUT "repos/$Repo/actions/permissions" @Headers --input -
gh api "repos/$Repo/actions/permissions" @Headers
gh api "repos/$Repo/actions/permissions/selected-actions" @Headers
# The last GET is expected to return HTTP 409 again.
```

Before root mutation, `test_rollback_transport.py` invoked the actual `rollback.ps1` six ways against an HTTP loopback fixture with dummy tokens and an empty CLI configuration. It asserted method, exact repository path, JSON body, Accept and API-version header; the full private transcript predates activation. Authorization headers were not logged. No fixture call went to GitHub.

This proves transport and payload construction for C5 enable, separate scanning/push disable, C2 strict false, CodeQL not-configured and C3 effective before policy. It does not prove live authorization, plan entitlement, endpoint acceptance or operational restoration. C1 rule rollback has supported API documentation but no live test; no live rollback has been exercised. Retain this distinction in activation records.

## C3 complete caller and metadata inventory

### Adopted action metadata closure

Fetched each exact pinned repository tree, located its actual action metadata, fetched that Git blob through the connected GitHub API, recomputed the Git blob hash and byte count, then parsed the complete metadata. Every action uses `node24`; none has a `pre` entrypoint, `runs.steps`, any structural `uses:` key, or `image`. Thus every metadata traversal terminates at its inspected JavaScript action leaf, including all conditional metadata. No remote reusable workflow, composite action, Docker action or local action metadata exists in this tree.

| Action at exact pinned commit | Definitions | Main / post entrypoints | Metadata Git blob | Metadata SHA-256 |
|---|---:|---|---|---|
| [actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1](https://github.com/actions/checkout/blob/3d3c42e5aac5ba805825da76410c181273ba90b1/action.yml) | 34 | `dist/index.js` / dist/index.js | `5b0524f730db83f9513c18ab31a6c086c7239076` | `d59219cb79590abdb877deaa14e3b65a00c05318bf5a6f3b989b9162b5d08c35` |
| [actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97](https://github.com/actions/setup-python/blob/5fda3b95a4ea91299a34e894583c3862153e4b97/action.yml) | 27 | `dist/setup/index.js` / dist/cache-save/index.js (`success()`) | `df6c8235b476652b6402d31d92a2a89cdea74bb9` | `e6dc8046c02bd3c9f7bf2fea6ba2e59b4e83c7de2b26ec2149a1627f5d66f96c` |
| [actions/setup-node@949feb2413d6458794dcd2491c4babbbce0c15c1](https://github.com/actions/setup-node/blob/949feb2413d6458794dcd2491c4babbbce0c15c1/action.yml) | 15 | `dist/setup/index.js` / dist/cache-save/index.js (`success()`) | `31057efa69b67281683c7b601a1d202329eaa3c1` | `84cd55863dbadfb83ed786c0bb4336553c2f4ceb52e102fccec01848f1977387` |
| [actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9](https://github.com/actions/upload-artifact/blob/cf430e030ddbb5b0abf93d22962f4752f3646cd9/action.yml) | 21 | `dist/upload/index.js` / none | `7cb4d1e81db55320b41217e1a78a1a46e3d2baef` | `c5979822866a72362e609844b6ebe77d4b7e759af68cc1c2c425dcf51481fab4` |
| [actions/download-artifact@9000827ccba6bdab643e8b6fd33ac0654aef8333](https://github.com/actions/download-artifact/blob/9000827ccba6bdab643e8b6fd33ac0654aef8333/action.yml) | 1 | `dist/index.js` / none | `8b8c65029ccad20750a29fecb438eca5a607fc57` | `e98559b7a31ba31be4709f20d22102dc2737fa630f69a339eb89981151e505fe` |
| [actions/dependency-review-action@a1d282b36b6f3519aa1f3fc636f609c47dddb294](https://github.com/actions/dependency-review-action/blob/a1d282b36b6f3519aa1f3fc636f609c47dddb294/action.yml) | 1 | `dist/index.js` / none | `5f6cf73d694f70892899c2768fa9814a9218dd0d` | `582ebeb27ae108f3d8786b5f7b29ddebc5bee3a5446e7ef2b94a3ac984cf587b` |

The six exact metadata files, raw tree responses and hashes are retained privately under `artifacts/settings-s2/c3-inventory/`. Pinning covers the bundled action code; downloaded Python/Node runtimes, pip/npm packages and shell networking remain outside the `uses:` allowlist. This inventory is not a hermetic dependency lock.

### Every workflow and caller remains permitted

| Workflow | Job definitions | Remote uses | Local reusable calls | External action closure (all at the exact commits above) | Policy match |
|---|---:|---:|---:|---|---|
| `.github/workflows/_packaged-windows.yml` | 1 | 2 | 0 | `actions/checkout`, `actions/setup-python` | all permitted |
| `.github/workflows/ci.yml` | 24 | 68 | 1 | `actions/checkout`, `actions/dependency-review-action`, `actions/download-artifact`, `actions/setup-node`, `actions/setup-python`, `actions/upload-artifact` | all permitted |
| `.github/workflows/deep-gate-visual.yml` | 1 | 5 | 0 | `actions/checkout`, `actions/setup-node`, `actions/setup-python`, `actions/upload-artifact` | all permitted |
| `.github/workflows/deep-gate-watch.yml` | 1 | 2 | 0 | `actions/checkout`, `actions/setup-python` | all permitted |
| `.github/workflows/deep-gate.yml` | 6 | 12 | 1 | `actions/checkout`, `actions/setup-node`, `actions/setup-python`, `actions/upload-artifact` | all permitted |
| `.github/workflows/release.yml` | 6 | 10 | 1 | `actions/checkout`, `actions/setup-python` | all permitted |

All 39 jobs are checked individually in `inventory.json`, including jobs with no `uses:` and all conditional steps. Dependency Review is the pinned `actions/dependency-review-action` leaf in `ci.yml`; Workflow Lint uses only pinned checkout. Deep Gate Visual and Deep Gate Watch are included explicitly above.

| Local caller | Reusable workflow | Child action closure | Policy match |
|---|---|---|---|
| `.github/workflows/ci.yml` / `packaged-smoke-windows` | `./.github/workflows/_packaged-windows.yml` | `actions/checkout`, `actions/setup-python` at the pins above | local call inherently permitted; both child pins match |
| `.github/workflows/deep-gate.yml` / `frozen-windows` | `./.github/workflows/_packaged-windows.yml` | `actions/checkout`, `actions/setup-python` at the pins above | local call inherently permitted; both child pins match |
| `.github/workflows/release.yml` / `packaged-windows` | `./.github/workflows/_packaged-windows.yml` | `actions/checkout`, `actions/setup-python` at the pins above | local call inherently permitted; both child pins match |

Local `./` actions/reusable workflows remain permitted by selected-actions mode. The local reusable resolves from the same caller commit and takes no `@ref`; adding an external pattern for it is unnecessary. GitHub's repository settings page says local `./` actions and reusable workflows stay allowed. For other `AvihaiShai/*` repositories it uses organization wording only, so their automatic allowance for a personal-account owner is unverified. No such action is used. The SHA requirement applies to actions (including GitHub-owned actions); GitHub documents that reusable workflows may still use tags. This tree adopts no remote reusable workflow. [GitHub policy semantics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)

### Workflow Lint tool downloads

These shell-downloaded release binaries are not Actions `uses:` dependencies and receive no allowlist entry:

| Binary | Version | SHA-256 checked before unpack/execution |
|---|---|---|
| actionlint | `1.7.12` | `8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8` |
| zizmor | `1.30.1` | `e65324f4430c2717591937edcec90ccbefaf14c174f8ec9415e03ca875b46e1a` |
| shellcheck | `v0.11.0` | `b7af85e41cc99489dcc21d66c6d5f3685138f06d34651e6d34b42ec6d54fe6f6` |

The compatibility result is bound to the fetched main tree above. The live workflow
registry also retains branch-only rehearsal entries (16 registry entries versus six
workflow source files on main). Other refs were inventoried read-only at
2026-10-22T15:28Z: 36 branches and 2 tags, 47 unique workflow blobs. 30 are
compatible. 8 are blocked by SHA pinning under either allowlist variant, because they
pin tags (`@v4`–`@v7`, pre-B1):

- branches `docs/js-unit-ledger-rows-22-23`, `docs/model-guidance-efficiency-20260914`,
  `docs/r1-postmerge-reconcile`, `feat/d4-packet-a-role-weight-accumulation`,
  `fix/npm-audit-braces-exception-20261017` and `probe/v1-drop-compositing-hints`;
- tags `archive/pr-4-fatigue-planning-recovery` and `archive/probe-v1-drop-compositing-hints`.

A PR opened or reopened from one of those branches, or a dispatch of `deep-gate.yml`
or `release.yml` against one, would fail to start. They need an explicit owner
disposition before C3; their retention under Operation A is unchanged. The disabled
C5 orphan remains in the registry and its source is absent from main.


## C1 seeded enforcement and bypass proof design — prepare only

### Future seeded newly introduced High/Critical proof

No real credential is needed. Private `artifacts/settings-s2/c1-triage/seed-sql-injection.py.txt` is an unexecuted static
analysis candidate, outside tracked source and inventory collection. A later
owner-approved rehearsal would copy it into a new otherwise unused source path
such as `c1_proof/codeql_sql_injection.py`, without importing/registering it from
the production app or modifying workflows. Review that no app or test auto-loader
will execute/import it. The intended query is `py/sql-injection`, security score
8.8, present in the standard code-scanning suite; success must depend on the
actual engine returning High/Critical, not this expectation. [CodeQL query metadata](https://codeql.github.com/codeql-query-help/python/py-sql-injection/).

1. Obtain separate owner approval naming the future public seed PR plan and
   native ruleset activation/proof scope. Refresh current main/base analysis,
   existing checks, source inventories and all settings. Preserve unrelated
   lanes. Do not copy the stale clone base into a future PR.
2. Establish an analyzed clean-or-explicitly-triaged baseline at the exact base
   SHA with the intended three languages. Confirm the candidate path/query is
   absent in the base. Keep all source-to-sink locations in newly added diff
   lines, since native merge protection has this requirement.
3. Use a human same-repository PR targeting main, with an exact recorded head,
   not a Dependabot or fork carrier. Do not publish a secret fixture, manufacture
   an alert via hand-written SARIF, or represent a push-only scan as PR blocking.
4. Wait for actual native CodeQL PR analysis. Retain run/attempt/head/merge SHA,
   tool name/version, query/category and alert/instance data proving the seeded
   rule and a High/Critical security severity on that PR. Review any unexpected
   result before proceeding. Do not relax query/severity or ignore the missing
   finding to make the rehearsal pass.
5. With the reviewed native ruleset active, capture its full readback and main's
   effective rule. Retain GitHub's PR merge-box/rule evaluation showing this
   exact native rule prevents merging because of that finding. All unrelated
   required checks must pass, or show independent rule-specific blocking
   evidence; a generic BLOCKED state with unrelated red checks is insufficient.
   Do not attempt a merge unless a separately approved mechanism guarantees the
   target cannot be updated. There is no assumed dry-run merge API.
6. On the same PR, replace the concatenated SQL query with a parameterized one
   (or remove the isolated fixture) as a separate recorded head. Actual native
   CodeQL analysis must remove/fix that introduced alert and its native merge
   restriction. Record base drift and any required refresh. This recovery
   distinguishes a native High/Critical alert block from missing setup/results
   or unrelated checks. Do not merge this PR under present authority.

*Addendum, 2026-10-22.* A red `Code scanning results / CodeQL` check is not enforcement
evidence: it fails with or without the ruleset. Open the seed PR before C1c exists and
record its exact head with every required context green and `mergeStateStatus`
UNSTABLE or CLEAN; then create C1c and record the same head BLOCKED. Record the
distinct waiting-for-results state on the fix head before its analysis completes.
Any seed PR is public: code scanning on private repositories needs a paid licence,
so publication is an owner decision.

Code scanning rules also block while the configured tool's analysis is still in
progress or when the tool is not configured; failed-analysis behaviour is
undocumented. Their constraints exclude merge queue groups and Dependabot PRs
analyzed by default setup, and require identified lines in the PR diff. These
limitations belong in the receipt; one ordinary PR cannot prove excluded cases.
[Code scanning merge protection](https://docs.github.com/en/code-security/concepts/code-scanning/merge-protection).

### Future native sole-owner bypass proof

Static payload/readback can establish a single allowed actor and mode; it cannot
prove a bypass was executed. Merely showing a merge button or an admin identity
also falls short. A native executed-bypass receipt needs an owner-authorized
reference update plus GitHub's rule evaluation identifying the owner and rule.

The main-target seeded PR should stay unmerged. The least disruptive separate
rehearsal proposal is an isolated protected proof base branch and a second
ruleset with byte-identical tool/threshold/User/mode values but only that base
ref/name changed. Protecting this base is a separately approved settings action;
default setup scans PRs against default/protected branches. [Default setup triggers](https://docs.github.com/en/code-security/concepts/code-scanning/setup-types).

Under separate explicit approval for those temporary resources and a named
rehearsal merge, run the same newly introduced High/Critical PR analysis on
that proof branch; capture ordinary rule blocking; then let the owner explicitly
choose PR bypass and merge only into that isolated proof base. Capture before/
after ref SHAs, PR/actor IDs, timestamp, ruleset version and detailed native
rule-suite result `bypass`. Collect
`rulesets/rule-suites?ref=<proof-ref>&actor_name=AvihaiShai&rule_suite_result=bypass&time_period=month`
with pagination, then its detailed suite. The default `time_period` is `day` (24 h)
and `month` is the longest window, so capture immediately. The proof base needs
classic branch protection (ruleset-only triggering of default-setup PR scans is
undocumented) and its own completed analysis before the seed PR. Check that its `actor_id` is 58347128
and its code-scanning rule is the one bypassed. This demonstrates the matching
configuration on a rehearsal branch, not a bypass executed on main. If GitHub
does not emit the needed result, report the evidence gap. [Rule suites REST API](https://docs.github.com/en/rest/repos/rule-suites).

Do not add another bypass actor to generate a negative test or obtain/use another
person's credentials. Sole-owner exclusion is established from fresh full actor
readback plus the collaborators readback (a write collaborator exists and stays
outside the bypass list); whether the rule evaluates owner direct pushes
(`enforce_admins: false`) or clears a PR block after a write user's alert
dismissal is undocumented and remains a recorded residual; a negative native test would need a separately authorized existing
non-owner actor and remains unproved absent that evidence. Preserve all proof
refs/history/artifacts; cleanup needs its own authority. An actual main bypass
remains unproved until a separately authorized genuine emergency occurs.

Every emergency or separately approved rehearsal PR records: incident or rehearsal
reason; target/base/head; affected checks and alert rule; owner identity; why
ordinary recovery is unavailable; compensating evidence; exact approval;
bypass action/time; and a linked subsequent green result. Never put secret values
in the record. A rehearsal must identify itself explicitly and cannot be cited
as a real emergency incident.

## Validation and remaining owner actions

The independent cold security reviewer approved the technical packet at content commit
`bddfd740b4b36ebd53c403b6acfc6984e1b99497`, with no blocking findings. The private report
is `artifacts/settings-s2/review/SECURITY_REVIEW.md`; final receipt changes also require
a delta check. A reviewer pass is not an owner signature or a readiness waiver.

The initial full Windows run completed **5,798 passed / 2 skipped / 13 failed** in
1,462.02s. Twelve shell contracts selected the unconfigured Windows WSL bash launcher;
one default-DB assertion conflicted with the explicit DB_FILE environment override
while a test changed HT_RUNTIME_DIR. The original log/XML are retained privately as
`full-pytest.log` / `full-pytest.xml`. No source or test was changed to resolve these.

Using Git Bash first on process PATH and letting the private HT_RUNTIME_DIR determine
the default DB resolved the failures: all four affected modules passed, **583/583**
in72.72s (`affected-modules.log` / `.xml`). The resolved DB path was asserted beneath
this clone's private runtime before execution. No user/machine environment changed;
no MSYS suppression variable was set. The corrected full-suite command is:

```powershell
# From this standalone clone, with its private dependency environment:
. ./artifacts/settings-s2/enter-lane.ps1
$env:PATH = 'C:\Program Files\Git\bin;' + $env:PATH
Remove-Item -LiteralPath Env:DB_FILE -ErrorAction SilentlyContinue
.\.venv\Scripts\python.exe -m pytest tests/ -q -n 4 --dist loadfile --junitxml=artifacts/settings-s2/full-pytest-corrected.xml
```

Corrected full-suite stdout/XML are retained as `full-pytest-corrected.log` / `.xml`.
The final completed full-suite result, final full head and exact-head CI run/check
receipt are recorded in [PR #555](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/555).
The PR stays draft until the corrected full suite, final review delta and every
final-head CI check are successful. The initial content head had30/30 successful
native checks; that is historical evidence and cannot substitute for final-head CI.

`git diff --check` passes. All six JSON request-body blocks and all twelve PowerShell
example blocks pass parsing without executing a settings command. Full before/final
settings comparisons show only the authorized changes. No test set, workflow, source,
manifest or generated inventory changed; C4 and every other ledger row are preserved.

The remaining owner settings choices are CodeQL setup/rules/proof activation, C2 and
C3. Recommend reviewing/authorizing the CodeQL setup and bounded proof plan separately,
then applying the native rule only after its baseline is triaged. Recommend C2 after
the WS5 workflow PR merges. Recommend C3 in a later, separate quiet window, once WS5 has
merged and a post-WS5 inventory still matches, and after the 2026-10-26 scheduled slot
is read. C3 also needs explicit choices on the allowlist variant, the eight blocked refs
and latent-policy restoration. Default setup is not subject to the allowed-actions policy, so C1b and C3 are order-independent; observe one default-setup run once both are active. Do not pre-allow deferred tools or extra actors.

Every PR merge still requires the owner's approval naming the PR and full head SHA.
No settings proposal or delegated classification is an owner signature.

## C4 JS Unit preparation — owner handoff, 2026-10-22

This supplement records lane 07's bounded documentation integration after the
owner's explicit section handoff. It changes no repository setting. The original
S2 receipts above remain dated evidence; C5 and S2's executed settings are untouched.
C4 code/contracts implementation is **not approved**. Q4's rename and D2's
conditional ruling do not authorize that stage. Later settings activation needs
its own owner decision, readbacks and live merge-blocking proof.

### Qualification and native proof

Q4 [#554](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/554), reviewed
head `316d7f69930b11d80b089b8c7956d296949f08ac`, merged as
`73de866ecb22bc8472dafb85f1405a27caf6513b`. Its exact renamed merged-main
[job 119766292139](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39761432262/job/119766292139)
is `JS Unit (Vitest)`, successful with coverage, 14 files / 269 cases. The full
main run succeeded with 29 successful jobs and the expected PR-only Dependency
Review skip. This is current-suite evidence, separate from historical qualification.

Reuse [Q4_RENAME.md](../r23_js_unit_promotion/Q4_RENAME.md)'s native seeded proof:
[run 39683330072 / job 119511059749](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39683330072/job/119511059749),
rehearsal `dac825e79f2078ba2580895ff2755c6b43b61e28`. The 269 original tests
passed, the injected assertion alone failed, the actual coverage command exited 1,
the summary succeeded and the Actions job remained failed. Reuse depends on the
final execution/failure-propagation bytes remaining equivalent. No new failure
campaign or protection-enforcement credit is assigned by this record.

Lane 03's final fixed-cutoff handoff was received at SHA-256
`e077541e9471c074ef88a3b96c3dda560619257d4fbda7309fb7abda764f779a`.
It proposes rows 123–131, nine exact successful jobs, cumulative 131/0/0/0/0
across corpora, at cutoff `2026-10-22T15:24:52Z`. Its separately owned source
publication is [#559](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/559);
this record neither applies those rows nor claims them merged. Historical rows
26–75 remain the completed 245-case cycle, 50/0/0/0/0, and D2's recorded
condition stays met. The eight expanded-corpus successes span only 18 h 14 m 29 s.
The owner still determines whether #551 is the final expansion packet: candidate
T0 `2026-10-21T18:45:51Z`, conditional strict mark `2026-11-04T18:45:51Z`.
Neither is declared operative here; no new C4/window condition is imposed.
#558 is after the cutoff and remains later ledger debt. Lane 04's final preflight
handoff awards no scheduled qualification before the 2026-10-26 slot.

### Exact first-stage membership and implementation proposal

Let R0 be the exact twelve existing strings in
[`scripts/release_gate.py`](../../scripts/release_gate.py)'s `REQUIRED_CONTEXTS`;
preserve their historical suffixes. Let J = `JS Unit (Vitest)` and
V = `Visual Regression (Windows baselines)`.

| Stage | PR required contexts | Release expected contexts |
|---|---|---|
| Current | R0, 12 | R0 + V, 13 |
| First proposed C4 stage | R0 + J, 13 | R0 + V + J, 14 |
| Future full adoption | R0 + J + Operation A Windows Tests + packaged composite + V + Workflow Lint + Dependency Review, 18 | Same excluding PR-only Dependency Review, 17 |

The future packaged context is `Packaged Smoke (Windows bootloader, non-required) / Build and smoke`;
Workflow Lint is `Workflow Lint (actionlint + zizmor)`. Full adoption is a future
target, not this payload. Windows visual occurs once in release. Dependency Review
never becomes release evidence; Linux and all unrelated candidates are excluded
from this first promotion.

After explicit owner approval naming **JS Unit C4 code/contracts implementation**:

| Path | Proposed bounded delta |
|---|---|
| `scripts/release_gate.py` | Keep immutable baseline `BASE_PR_REQUIRED_CONTEXTS` (R0) and `BASE_RELEASE_EXPECTED_CONTEXTS` (R0+V). Add `JS_UNIT_CONTEXT`, `PR_REQUIRED_CONTEXTS` = R0+J and separately `RELEASE_EXPECTED_CONTEXTS` = baseline release+J. Default provenance to the release set; migrate consumers together, retaining compatibility aliases if needed. No arbitrary runtime switch to a weaker stage. |
| Same script, provenance | Retain exact commit endpoint, pagination, slug filter, newest `(started_at,id)` choice, missing-timestamp handling and deadline behavior. Thread requested SHA into `select_runs(runs, expected, *, sha)` and require result `head_sha == sha`, `app.slug == github-actions`, numeric `app.id == 15368` before credit. Missing/wrong bindings cannot counterfeit success. Preserve version, exact-tag/main-ancestry and release fan-in rules. |
| `tests/test_release_gate.py` | Realistic SHA/app-ID fixtures; independently specified baseline 12/13 and JS 13/14 floors, uniqueness and exact membership; real provenance decisions for both supported sets, retaining existing mirror, pagination, pending, version and fan-in tests. |
| `tests/test_release_workflow_contracts.py` | Migrate explicit set imports; replace JS exclusion with positive PR/release membership. Pin the stable direct `js-unit` job, exact name and `npm run test:js -- --coverage` invocation with unsuppressed test failure. Preserve composite-name resolution and unrelated negative assertions. |
| `docs/test_inventory/**` | Regenerate only on actual added/renamed-case drift from the final integrated tree; never hand-merge generated output. |

Current provenance scopes SHA through the API endpoint and filters app slug;
its selection/fixtures do **not** already validate per-result SHA and numeric
app ID. The paired implementation/tests above make that requirement explicit.
Stale means a superseded run on the requested SHA masking a newer result, not
a new wall-clock TTL. No executable workflow change, new threshold, suite change
or release-job change is needed merely to promote the existing context.

| Decision | Positive control | Negative control |
|---|---|---|
| Floors and membership | Exact R0 preserved; J in both first-stage sets; V once in release | Dropped/rebound/renamed floor, duplicate V, empty expected set, extra promotion or release Dependency Review rejected |
| JS outcome | Completed/success on requested SHA | Missing/old name; deadline-pending; failure, cancelled, skipped, neutral, timed_out or action_required rejected |
| Provenance | Requested URL/SHA, slug and numeric app ID agree | Missing/wrong SHA or app ID, foreign slug cannot fill a requirement; foreign failure does not poison genuine trusted success |
| Newest result | Newer success beats old failure; timestamp/ID order is deterministic | Newer failure/pending beats stale success regardless of array order, including page 2 |
| Wiring and settings | Real direct coverage exit propagates; exact 13-check object list preserves strict | Test failure suppression, conditional/detached execution, lost composite resolution, strict flip or unrelated candidate rejected |

Reuse existing acceptance tests first. The implementation gate union includes
full pytest per the owning R2.3 follow-through, targeted release/contracts/staged
behavior, JS coverage, inventory check/necessary regeneration, and pyright
baseline diff for Python edits. Run an independent code reviewer; adding/removing
jobs or converting to `uses:` also needs architecture review. Apply any stronger
matching `/verify-suite` gate for uncovered behavior, milestones or root configs.
G7's one-PR E2E exception grants C4 no waiver. Reserve host resources separately;
respect S3/WS5's workflow slot if any workflow change becomes necessary.

### Future owner activation and rollback sheet — not executed

The reviewed snapshot has 12 exact `(context, app_id)` pairs, all app 15368,
`strict: false`, and JS absent. The complete first-stage body is the existing
[`required-status-checks.proposed.json`](../r23_js_unit_promotion/required-status-checks.proposed.json):
the twelve pairs plus exactly `{"context":"JS Unit (Vitest)","app_id":15368}`.
It is a reviewed snapshot, never a blind replacement of concurrent settings.
For this JS-only stage, preserve fresh strict; C2 is a separate action. This
bounded instruction supersedes §6's generic C4 `strict: true` for this proposal.

Before activation: separately approved code/contracts implemented, derived gates
and independent reviews complete, named PR merged under separate merge authority,
and J succeeds on that exact merged-main SHA. Then obtain separate owner C4
settings/proof authority and serialize settings writers. Re-read full protection
and effective rules immediately; drift from the reviewed floor requires
reconciliation and a refreshed reviewed payload. No tag during a partial transition.

```powershell
# Future owner-run sheet; no command below was executed by lane 07.
$Repo = 'AvihaiShai/Hypertrophy-Toolbox-v3'
$Out = 'artifacts/ci07/activation'
$Headers = @('-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: 2026-03-10')
New-Item -ItemType Directory -Path $Out -Force | Out-Null
gh api "repos/$Repo/branches/main/protection" @Headers |
    Set-Content (Join-Path $Out 'full-before.json') -Encoding utf8
gh api "repos/$Repo/rules/branches/main" @Headers |
    Set-Content (Join-Path $Out 'effective-rules-before.json') -Encoding utf8
# Check exit codes and compare complete readbacks before considering any apply.
# Only with separate owner C4 settings/proof approval and a freshly reviewed body:
# gh api --method PATCH "repos/$Repo/branches/main/protection/required_status_checks" @Headers --input 'docs/r23_js_unit_promotion/required-status-checks.proposed.json'
# Then retain fresh full protection and effective-rule readbacks.
```

Expected after-state: exactly 13 unique check/app pairs, all twelve original pairs
unchanged, J bound to 15368, strict unchanged, unrelated protection/effective rules
unchanged. Retain UTC request/response status, complete snapshots and payload/hash.
A failed/ambiguous response requires readback before deciding what applied.

Actual blocking proof remains an owner action on an explicitly approved harmless
proof PR/head with all twelve old requirements green and the real J job failing.
Record GitHub's blocked state/reason attributable to J under the agreed non-bypass
actor. Admin enforcement is false; an administrative override is not this proof.
Any active merge-attempt method needs its own owner approval; an unrelated rejection
does not qualify. Restore the assertion on the retained proof branch and capture
the exact new head's J success and required-check recovery. No proof-branch merge
or deletion is authorized. A green job, fixture or YAML inspection alone cannot
close live enforcement.

Rollback is a separate owner action: re-read first; if the current full object
equals the expected post-apply state, a scoped PATCH restores the reviewed twelve
checks and same strict. If it drifted, reconcile a body removing only J while
preserving concurrent settings. Never drop or rebind another context. Retain full
readbacks and mark C4 reverted/unactivated, not completed. No mutation, rollback
transport test or live blocking proof ran in this preparation lane.
