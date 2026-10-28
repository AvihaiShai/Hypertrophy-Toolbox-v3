# Final acceptance evidence — 2026-10-28

Candidate `68d52ba74a53a8ba4807842e512719b12e0a94fb`; base
`c29ddf0740ecd9dd90e65424c37050c764504431`. Accepted under the owner's task-specific
delegation. [Closeout and installed-copy evidence](../CLOSEOUT.md).

## Exact-candidate CI and AC7

All 34 native checks succeeded, including the 12 protected context/app pairs (GitHub Actions
app 15368). Protection was read, not changed; strict mode was false. Runs:
[CI 40706628332](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/40706628332),
[CodeQL 40706617549](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/40706617549).

Full AC7 run: `C:\ht\MSYS-AC7\runs\68d52ba7-sol-full\`. The single invocation ran all
34 mutated arms and `restored`; overall PASS. Each literal edit matched exactly once and
changed the disposable archive. Patches, complete hashes, argfiles, pytest logs and junit
files are retained per arm. `SUMMARY.md`, `summary.json` and `host-audit.json` are retained.

| Scope | Result |
|---|---|
| 15 guard arms | All 244 designated must-fail node/host identities failed |
| 19 monitor arms | All 33 designated nodes failed; failure messages independently confirm both hosts failed (66 host outcomes) |
| Restored guard file | 2,249 passed, both PowerShell hosts |
| Restored monitor file | 48 passed, 1 skipped (H8b is non-Windows-only); tests loop through both hosts |
| Restored effective registration probe | 4 passed |
| Restored total | 2,301 passed, 1 skipped; exit 0, 1 harness-related config warning |

Restored runtime was 1,354.41 seconds. The two-arm pilot is retained separately at
`C:\ht\MSYS-AC7\runs\68d52ba7-sol-pilot`; it is not substituted for the full run.
Earlier incomplete runs from the handover remain retained and are not credited.

### Message arm resolution

`G-message-always` forces a plain resolved-path clause, substitutes `D` when cwd is invalid,
and omits the directory-change hedge. Its designated must-fail labels are `P1b-cd`,
`P1b-conservative-interp`, `P1b-conservative-ps`, `P1b-emptycwd`, `P1b-garbage`, `P1b-nocwd`,
`P1b-setlocation` and `P1b-unc`, each under `powershell` and `pwsh`: all 16 failed.

The arm produced 20 failures / 194 passes. The four additional failures are the two hosts
for `P1b-cd-heredoc` and `P1b-cd-interp`; those remain restored-only requirements and are
not part of the arm's gate. This supersedes the earlier claim that this patch leaves the
hedge unaffected. `G-nonoption-anywhere` includes both edits and fails A22/A23 on both hosts.

### Blob binding and final counts

Git archive/checkout applies CRLF for these PowerShell files; the stored blobs use LF.
The restored archive guard and candidate blob were verified identical after CRLF-to-LF
normalization (`archive-blob-binding.json`). Installed copies instead match the merged blob
bytes exactly. BOM is preserved in both forms.

The final source has a 1,694-line guard (+352 / -0 against base) and an 872-line monitor.
The `a7aa5163` to `68d52ba7` diff changes headers/comments, docs, assertion wording and the
`refusal_sentences` helper name; it adds no test cases. The retained earlier fix1 guard log
records 2,245 passes on the pre-P4i working tree. The exact final candidate run above records
2,249, including P4i and its escaped companion on both hosts. The earlier log is not used
as proof of the final committed collection.

## Final corpus gate

[Final reconciliation](CORPUS_PASS_3d85fd9f.md): 69 refusals among 12,612 qualifying commands;
all previous 60 hits retained, 9 additions reconciled, no new false-positive class and no
unexpected exit code. Raw command text remains outside git at
`C:\ht\MSYS-AC7\corpus\run-68d52ba7-sol\`.

## Installation and operational receipts

- Expanded installer fake-profile execute/rollback: `C:\ht\MSYS-INSTALL\sol-rehearsal\`.
- Real dry-run transcript: `C:\ht\MSYS-INSTALL\transcript-20261028T155711Z.json`.
- Real install transcript and backup: `C:\ht\MSYS-INSTALL\transcript-20261028T155730Z.json`
  and `backup-20261028T155730Z\`.
- Installation verification exited 0. Guard and monitor match their merged OIDs and SHA-256;
  settings are a pure insertion preserving LF and the original absence of a BOM.
- Accepted operational run: `C:\ht\MSYS-OPS\run-sol-20261028T155934Z\`; prior incomplete
  attempt: `run-sol-20261028T155803Z\`. Both fixture mappings were removed.
- Manager verification records, native check evidence, before/after hashes and acceptance
  facts: `C:\ht\MSYS\artifacts\sol-closeout\`.

The shared checkout guard/settings hashes and H4 creation times were unchanged. The monitor
registration is user-level only. Panel rendering remains unmeasured. `PREVENTION_COMPLETE`
is not claimed.
