# B1 adopted action and permission inventory

Measured 2026-10-19 against base `7ac1af2d2dc10be6bf6a5016c09bc5244cf37ed7`.
Execution authority and commit/run/review evidence live in [PLANNING.md §13](PLANNING.md#13-b1-execution--2026-10-19).
This is the B1 inventory, not activation of the C3 repository policy.
Later additions (A1, B2, E1/D3, B3) are appended below without rewriting this measurement;
the current C3 candidate set and remote `uses:` count are in the latest addition (B3: six
repositories, 95).

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
`actions/setup-python`, `actions/setup-node`, and `actions/upload-artifact`
(B1-time; see the additions below).
No wildcard or future integration is pre-approved. C3 activation, its owner
readback/proof and any future inventory expansion remain separate work.

## A1 addition — 2026-10-19

Packet A1 ([PLANNING.md §14](PLANNING.md#14-a1-execution--2026-10-19)) adopts one
more GitHub-owned action. It follows the same procedure as above, and the sections
above are left at their B1 measurement.

| Repository | Release | Pinned commit | Metadata Git blob | Calls: CI |
|---|---|---|---|---|
| `actions/download-artifact` | v8.0.2 | `9000827ccba6bdab643e8b6fd33ac0654aef8333` | `8b8c65029ccad20750a29fecb438eca5a607fc57` | 1 |

The `v8.0.2` and `v8` tags both resolve to that commit. GitHub reports its signature
`verified` (`valid`). Its `package.json` version is `8.0.2`, and the commit is 5 ahead
of and 0 behind `v8.0.1`. The pinned
[`action.yml`](https://github.com/actions/download-artifact/blob/9000827ccba6bdab643e8b6fd33ac0654aef8333/action.yml)
runs `node24` from `dist/index.js` with no post entrypoint. It declares no
`runs.steps`, nested `uses:` or container, so the traversal ends there. It runs in the
`guard-hook-tests` job, inheriting `contents: read`, and downloads only this run's
own `guard-hook-junit-*` artifacts (no `github-token`, `repository` or `run-id`
input), so no permission is added.

A1 also adds three `checkout`, one `setup-python` and one `upload-artifact` call to
`ci.yml`, all at the pins above. `ci.yml` now holds 62 remote `uses:` (was 56), and the
repository holds 91 (was 85) across five repositories. The C3 candidate set therefore
becomes `actions/checkout`, `actions/setup-python`, `actions/setup-node`,
`actions/upload-artifact` and `actions/download-artifact`. That set is still a
proposal; it activates nothing.

## Non-Action tool binaries (B2)

The `workflow-lint` job downloads three release assets pinned by version and SHA-256
in its `env` block, and verifies them with `sha256sum --check --strict` before
anything is unpacked. The record and rationale are in
[PLANNING.md §15](PLANNING.md#15-b2-execution--2026-10-20).

| Tool | Version | Asset | SHA-256 |
|---|---|---|---|
| actionlint | 1.7.12 | `actionlint_1.7.12_linux_amd64.tar.gz` | `8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8` |
| zizmor | 1.30.1 | `zizmor-x86_64-unknown-linux-gnu.tar.gz` | `e65324f4430c2717591937edcec90ccbefaf14c174f8ec9415e03ca875b46e1a` |
| shellcheck | v0.11.0 | `shellcheck-v0.11.0.linux.x86_64.tar.gz` | `b7af85e41cc99489dcc21d66c6d5f3685138f06d34651e6d34b42ec6d54fe6f6` |

These are tool binaries, not Actions, so the C3 allowlist and candidate set are
unchanged. The job's only `uses:` is the existing pinned `actions/checkout`. That one
call brings `ci.yml` to 63 remote `uses:` (was 62) and the repository to 92 (was 91),
all at the pins above.

## E1/D3 (2026-10-20)

E1 moves the `visual-linux` job's five calls (`checkout`, `setup-python`, `setup-node`
and two `upload-artifact`) out of `deep-gate.yml` (17 → 12) into the new
`deep-gate-visual.yml` (5). D3's new `deep-gate-watch.yml` adds one `actions/checkout`
and one `actions/setup-python` (2). Every call uses the pins above; no new action
repository is adopted, and the C3 candidate set is unchanged.

Remote `uses:` per file, by
`grep -cE '^\s*(- )?uses: [A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@'`: `ci.yml` 63,
`deep-gate.yml` 12, `deep-gate-visual.yml` 5, `deep-gate-watch.yml` 2,
`release.yml` 10, `_packaged-windows.yml` 2. The repository holds **94** (was 92)
across the same five repositories. The three local `uses: ./.github/workflows/_packaged-windows.yml`
calls are not remote and are not counted.

## B3 addition — 2026-10-20

Packet B3 ([PLANNING.md §17](PLANNING.md#17-b3-execution--2026-10-20)) adopts one more
GitHub-owned action for the PR-only `dependency-review` / `Dependency Review` job. It
follows the same procedure as above, and the sections above are left at their own
measurements.

| Repository | Release | Pinned commit | Metadata Git blob | Calls: CI |
|---|---|---|---|---|
| `actions/dependency-review-action` | v5.0.0 | `a1d282b36b6f3519aa1f3fc636f609c47dddb294` | `5f6cf73d694f70892899c2768fa9814a9218dd0d` | 1 |

`v5.0.0` is a lightweight tag on that commit; no moving `v5` tag exists. GitHub reports
the commit signature `verified` (`valid`). Its `package.json` version is `5.0.0`, the
commit is 19 ahead of and 0 behind `v4.9.0`, and the release was published 2026-05-08.
The pinned
[`action.yml`](https://github.com/actions/dependency-review-action/blob/a1d282b36b6f3519aa1f3fc636f609c47dddb294/action.yml)
runs `node24` from `dist/index.js` with no post entrypoint. It declares no
`runs.steps`, nested `uses:` or container, so the traversal ends there.

The only API the action calls is the dependency-graph compare endpoint
(`GET /repos/{owner}/{repo}/dependency-graph/compare/{base}...{head}`) on the default
job token, so the job's `contents: read` suffices and no permission is added. There is
no checkout. The job sets `show-openssf-scorecard: false`, which disables the action's
outbound calls to third-party scorecard services.

Remote `uses:` per file, by the same
`grep -cE '^\s*(- )?uses: [A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@'`: `ci.yml` 64 (was 63);
`deep-gate.yml` 12, `deep-gate-visual.yml` 5, `deep-gate-watch.yml` 2, `release.yml` 10
and `_packaged-windows.yml` 2 are unchanged. The repository holds **95** (was 94) across
six repositories. The C3 candidate set therefore becomes `actions/checkout`,
`actions/setup-python`, `actions/setup-node`, `actions/upload-artifact`,
`actions/download-artifact` and `actions/dependency-review-action`. That set is still a
proposal; it activates nothing.
