# B1 adopted action and permission inventory

Measured 2026-10-19 against base `7ac1af2d2dc10be6bf6a5016c09bc5244cf37ed7`.
Execution authority and commit/run/review evidence live in [PLANNING.md §13](PLANNING.md#13-b1-execution--2026-10-19).
This is the B1 inventory, not activation of the C3 repository policy.

## Adopted remote actions

Each original `@v7` resolved to the full commit below in its official `actions/`
repository. The exact release tag resolves to the same commit, its `package.json`
version agrees, and GitHub reports the commit signature verified. Workflow comments
retain the exact version for review and Dependabot. No version family is upgraded.

| Repository | Release | Pinned commit | Calls: CI / Deep Gate / Release / reusable |
|---|---|---|---|
| `actions/checkout` | v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` | 16 / 6 / 5 / 1 |
| `actions/setup-python` | v7.0.0 | `5fda3b95a4ea91299a34e894583c3862153e4b97` | 12 / 6 / 5 / 1 |
| `actions/setup-node` | v7.1.0 | `949feb2413d6458794dcd2491c4babbbce0c15c1` | 13 / 2 / 0 / 0 |
| `actions/upload-artifact` | v7.0.2 | `cf430e030ddbb5b0abf93d22962f4752f3646cd9` | 15 / 3 / 0 / 0 |

There are **85 remote `uses:` occurrences**, four repositories and four distinct
commits. These are all adopted remote actions, including the actions inside the
local reusable workflow. No remote reusable workflow, Docker action or local
composite action is adopted. The orphan workflow absent from `main` remains C5's
separate owner action; this inventory does not authorize changing it.

## Metadata and nested dependency proof

Fetched and parsed the **exact pinned commit's** `action.yml` for every repository,
including all `runs` entries, rather than inferring nested dependencies from the
callers. All four run `node24` with checked-in JavaScript entrypoints. None declares
`runs.steps`, a nested `uses:` or a container image; the action traversal terminates
at these four metadata files. There are no tracked `action.yml`/`action.yaml` files
in this repository to add to that traversal.

| Immutable metadata source | Main / post entrypoints | Metadata Git blob |
|---|---|---|
| [checkout](https://github.com/actions/checkout/blob/3d3c42e5aac5ba805825da76410c181273ba90b1/action.yml) | `dist/index.js` / `dist/index.js` | `5b0524f730db83f9513c18ab31a6c086c7239076` |
| [setup-python](https://github.com/actions/setup-python/blob/5fda3b95a4ea91299a34e894583c3862153e4b97/action.yml) | `dist/setup/index.js` / `dist/cache-save/index.js`, post on success | `df6c8235b476652b6402d31d92a2a89cdea74bb9` |
| [setup-node](https://github.com/actions/setup-node/blob/949feb2413d6458794dcd2491c4babbbce0c15c1/action.yml) | `dist/setup/index.js` / `dist/cache-save/index.js`, post on success | `31057efa69b67281683c7b601a1d202329eaa3c1` |
| [upload-artifact](https://github.com/actions/upload-artifact/blob/cf430e030ddbb5b0abf93d22962f4752f3646cd9/action.yml) | `dist/upload/index.js` / none | `7cb4d1e81db55320b41217e1a78a1a46e3d2baef` |

The pin includes the bundled action code and its libraries. Runtime tool downloads
(Python, Node, pip and npm packages) are not nested Actions `uses:`; their existing
version/cache behavior is unchanged. B1 does not claim hermetic dependency locking.
The local evidence directory `artifacts/ci_cd_expansion/b1/upstream/` retains the
metadata bytes, commit responses and SHA256 digests in `summary.json`.

## Reusable workflow contracts

All three calls remain `./.github/workflows/_packaged-windows.yml`, resolved from
the caller's commit. A local reusable call does not take an `@ref`. No inputs,
outputs, secrets forwarding or additional caller is introduced. The child remains
`build-and-smoke` / `Build and smoke`, on Windows with its existing timeout,
build and bootloader-smoke steps.

| Caller workflow / job | Unchanged composite check name |
|---|---|
| `ci.yml` / `packaged-smoke-windows` | `Packaged Smoke (Windows bootloader, non-required) / Build and smoke` |
| `deep-gate.yml` / `frozen-windows` | `Frozen executable (real bootloader, Windows) / Build and smoke` |
| `release.yml` / `packaged-windows` | `Frozen Windows executable / Build and smoke` |

## Effective token permissions

| Scope | Explicit permissions | Reason |
|---|---|---|
| All four workflow defaults | `contents: read` | Checkout and existing repository reads; unspecified scopes are disabled. CI and Deep Gate gain this declaration; Release and the reusable build retain theirs. |
| `ci.yml` / `e2e-functional` | `{}` | The shell fan-in reads only `needs.e2e-functional-shard.result`; it uses no repository API or checkout. |
| `release.yml` / `ci-provenance` | `contents: read`, `checks: read` | Preserved exception: inspect check-runs for the exact commit through the existing provenance gate. |
| Every other job, including reusable callers and child | `contents: read` | Inherited explicit default or existing job declaration. No write scope is required. |

Artifact and cache uploads use runner runtime credentials; they do not require
`actions: write` on `GITHUB_TOKEN`. No publication, PR commenting, repository write,
OIDC or attestation scope is added. Permission maps and reusable-call narrowing
follow [GitHub's workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions)
and [reuse permissions rules](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations#access-and-permissions-for-nested-workflows).

## Verification and future updates

Parsed all four workflows and the four pinned metadata files. Every remote action
reference matches its recorded 40-character commit. Effective permissions were
checked for every job. A structural comparison to the base, normalizing only the
85 pin replacements and the three new permission declarations, is identical:
triggers, names, matrices, steps, conditions, enforcement, timeouts, inputs and
reusable calls are preserved. There are 18 CI job definitions (19 jobs when the
two-leg shard matrix expands), seven Deep Gate jobs, six Release jobs and one
reusable child. Local result: `artifacts/ci_cd_expansion/b1/verification.json`.

The required full pytest run and independent code-reviewer result are recorded in
the execution ledger. No test identities or functional spec sets changed, so the
generated test inventory is not regenerated. No existing test is weakened.

Dependabot's weekly `github-actions` version updates remain enabled and unchanged.
For a future pin update or new action, verify the official commit/release, read
that commit's metadata, traverse any composite/local/remote dependencies, and
update this inventory and affected workflows before adoption. Keep full SHA pins
and version comments; do not infer nested safety from a tag-text search.

The C3 candidate repository set is exactly `actions/checkout`,
`actions/setup-python`, `actions/setup-node`, and `actions/upload-artifact`.
No wildcard or future integration is pre-approved. C3 activation, its owner
readback/proof and any future inventory expansion remain separate work.
