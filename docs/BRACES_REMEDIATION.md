# Braces depth exhaustion remediation

The remediation for [issue #513](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/513)
replaces every transitive `braces` resolution with the exact patched fork
`npm:@zklogic/braces@3.0.7` and removes the accepted-debt entry in the same commit.
It follows the existing [E-6 retirement rule](NPM_AUDIT_SEVERITY_POLICY_DECISION.md#63-owner-renewal-ruling-for-braces-2026-10-17)
and the owner's 2026-10-18 request to continue #513 through closure. It grants no
new waiver and does not amend the severity floor or whole-graph audit policy.

## Scope and alternatives

Fresh `origin/main` was `a81b3685` when measured on 2026-10-18. The official
[advisory](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) remained high,
unwithdrawn, affected through `3.0.3`, with no patched official release. Registry
latest was `braces 3.0.3`, `micromatch 4.0.8` and `stylelint 17.16.0`.

The committed graph reached `braces` through four paths:

- `stylelint 16.11.0 -> micromatch 4.0.8`;
- `stylelint -> fast-glob 3.3.3 -> micromatch`;
- `stylelint -> globby 11.1.0 -> fast-glob -> micromatch`;
- `sass 1.105.1 -> @parcel/watcher 2.5.1` (optional) `-> micromatch`.

An override at their common `braces` dependency repairs all four paths. Stylelint
stays at the frozen `16.11.0` measurement pin, and the deliberately skipped watcher
bump stays skipped. Other package resolutions remain unchanged.

Latest Stylelint still reaches the affected package; its proposed downgrade to
`7.7.0` violates the frozen instrument. A programmatic Stylelint entrypoint cannot
clear a whole-graph audit while the declared dependencies remain installed.
Picomatch is not a compatible micromatch substitution: fast-glob uses micromatch's
`.braces()` API. A postinstall patch leaves the affected official lockfile identity
and audit finding intact. Vendoring would require the same patch review plus local
maintenance of the copied source. The selected fork changes less runtime code than
the other reviewed fork, `@franciscosolis/braces@3.1.1`.

## Patch and provenance

The published artifact's ten files byte-match immutable
[commit `77ed7dda9f3f6c9aa22798a36acfc5b544506717`](https://github.com/ArfanKhalilMughal/braces/tree/77ed7dda9f3f6c9aa22798a36acfc5b544506717).
Compared with official `braces 3.0.3`, runtime changes are confined to
`lib/constants.js` and `lib/parse.js`. Parsing caps combined brace/parenthesis
nesting at 256 and preserves excessive nesting as literal text. The patch also
includes upstream quote/range parser corrections. `index.js`, the recursive
walkers, and the MIT license remain byte-identical. There are no new runtime
dependencies or install lifecycle scripts.

The lockfile pins the published tarball integrity:

```text
sha512-+MYCuqCdcYsZCVkG7BkHXWrkXklBDq+cTxrSMrCI8o1BQg6iAEPhkNuWrfwSt0LladX0XSx3V1HYV7RzMsKEWQ==
```

The downloaded artifact matches that integrity and its SLSA subject. Provenance
binds it to the same immutable source commit and
[publication run](https://github.com/ArfanKhalilMughal/braces/actions/runs/37463847658).
[CI at that commit](https://github.com/ArfanKhalilMughal/braces/actions/runs/37463847630)
passed nine Node-version jobs. Local `npm audit signatures` verified 206 registry
signatures and 56 attestations.

This is a recent, single-maintainer fork with a short maintenance history. The
repository now owns the decision to retain or replace this exact override. Revisit
it when official braces publishes a verified fix, or when every upstream path
stops requiring braces. An upstream release alone does not change the committed
graph; validate the replacement and remove the override in a reviewed change.

## Security and compatibility evidence

A clean audit is insufficient evidence for a renamed package. Independent source
review and executable positive controls established the actual depth bound:

- With a 512 KB Node stack, original `3.0.3` overflows in nine deeply nested
  brace/parenthesis/mixed compile, expand and stringify probes; the fork completes.
- The fork completes 24 adversarial string cases, including unbalanced or
  mismatched delimiters, escapes, quotes and square brackets.
- One thousand deterministic parser probes remain bounded even with excessive or
  infinite `maxDepth`. Seven hundred sixty-eight ordinary pattern/option
  comparisons match the original output.
- The full Stylelint reports are byte-identical: 21 files, 5,467 warnings,
  zero parse or configuration errors. The seven shared surfaces retain 2,767
  warnings. Historical committed baseline counts are not regenerated.
- Baseline and patched Sass builds are byte-identical. On Windows, the checkout's
  terminal CRLF differs from Sass's generated LF; the Git drift check, rather than
  a raw working-copy hash comparison, verifies the committed artifact.

The relevant micromatch and fast-glob callers pass strings, so their ASTs pass
through the bounded parser. Direct callers can still construct unbounded ASTs for
the unchanged walkers; this change does not claim to guard that unused API path
or every other form of resource exhaustion.

The actual audit changes from six high package entries carrying this advisory
to **zero high/critical findings**. The two existing moderate findings remain
below D-1's floor. The real gate passes with `allow: []`, including on
`2026-11-14`. Keeping the old entry correctly fails D-5 as stale.

## Reproduction and closure gates

From the remediation checkout:

```powershell
npm ci
npm audit --package-lock-only --json > artifacts/npm-audit.json
# Capture npm's exit status (1 while the two moderate findings remain).
node scripts/npm_audit_gate.mjs --audit artifacts/npm-audit.json --allowlist docs/npm_audit_allowlist.json --audit-exit-status 1
node scripts/npm_audit_gate.mjs --audit artifacts/npm-audit.json --allowlist docs/npm_audit_allowlist.json --audit-exit-status 1 --today 2026-11-14
npm audit signatures
npm run lint:css
npm run build:css
git diff --exit-code -- static/css/bootstrap.custom.min.css static/css/bootstrap.custom.min.css.map
.venv/Scripts/python.exe -m pytest tests/test_braces_override_contracts.py tests/test_npm_audit_gate_contracts.py -q
```

The new contracts pin the reviewed resolution and exercise hostile string inputs
when Node dependencies are installed. The existing committed-allowlist contract
uses synthetic audit input against the real gate and committed allowlist; it is
not a live-registry audit despite its historical test name. The separate commands
above provide the real-audit evidence.

Before merge, run full pytest, Chromium verification with the correct functional
and visual seeds, JS unit tests, type checking, generated-inventory drift, and the
required CI checks. Do not rebaseline CSS, visual captures, or policy to clear a
failure. Record final results in the remediation PR and close #513 only after the
fix lands.
