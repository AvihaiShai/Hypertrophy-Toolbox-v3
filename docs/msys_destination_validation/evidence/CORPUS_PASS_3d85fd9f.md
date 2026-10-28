# Corpus false-positive pass — candidate 3d85fd9f (2026-10-28)

Read-only. Source: Bash/PowerShell `tool_use` commands in `%USERPROFILE%\.claude\projects\**\*.jsonl`,
deduplicated, prefiltered to commands containing a `/<letter>/<char>` sequence: **12,442** unique
commands (all Bash; no PowerShell-tool command in the corpus matched the prefilter). Each was
classified by the candidate guard (blob `7597b828`) and, when refused with the drive-token reason, by
the base guard (blob `2d8a5a55`). Nothing was executed. Raw rows (`corpus.jsonl`) stay here, outside git.

- Candidate refused with the drive-token reason where base allowed: **60** (0.48% of the prefiltered set).
- Converted shapes spot-checked against the candidate (all allowed): `A=/d/d/x`, `env -i A=1 PATH=/usr/bin
  /d/x/python.exe`, `for t in /d/c /d/d; ...`, `cd /d/x && ls`, `source /d/x/env.sh`, `echo | cd /d/x`.

Classification (heuristic pass `classes.json`, then manual reconciliation of its 21 "OTHER" rows):

| Class | Count | Status |
|---|---|---|
| True positive: path inside a `python -c` / `node -e` / `powershell -Command` body, `"/d/x,/c/y"` second token, or a deliberate resolver probe | 20 | correct refusal |
| Drive path embedded inside a quoted word (command stored in a variable, prose in echo/printf/prompt strings, JSON test payloads, `grep " /d/x"`) | 19 | accepted Q3b class (pinned P4b) |
| `sed`/regex script argument (`s#/d/...#`, `s|/d/...||`, `/N/g`) | 13 | NEW class — accepted by manager under delegation as a Q3b sub-case; remedy: escape the slash (`s#\/d/...#`); pinned as P4i |
| Heredoc body text | 6 | accepted (pinned P4h) |
| Attached redirect target `2>/d/x` | 2 | accepted (pinned P3-refuse) |

Corpus rule (Plan v2 step 6): the only unpinned class seen more than once is the sed/regex class; it is
pinned (P4i) and accepted with the class named, so the rule is satisfied. No rule adjustment was made.

## Final candidate `68d52ba7` — 2026-10-28

Re-run against exact guard blob `427ae4c5ff28f23a41d765ae1e40928237d064fb`, with the same base
guard blob `2d8a5a559f6a9383549a280e09c3748f4213d63a`: **12,612** qualifying commands,
**69** refusals where the base allowed (0.55%). All commands were Bash; no PowerShell-tool
command matched this corpus's prefilter. Command text was classified, never executed.

All previous 12,442 commands and all previous 60 hits remain. Of 170 additional commands,
9 are new hits: one deliberate nested Windows resolver probe, seven heredoc bodies containing
path examples/code, and one quoted JSON guard-test payload. These fall into already accepted
or pinned classes. The manager accepts the reconciliation under the owner's task-specific
delegation; no new false-positive class or rule adjustment is needed.

| Reconciled final class | Count | Disposition |
|---|---|---|
| Correct refusal: interpreter/Windows-shell body or deliberate resolver probe | 21 | correct refusal |
| Path text embedded in a quoted word, including JSON guard-test payloads | 20 | accepted Q3b; P4b |
| `sed`/regex script argument | 13 | accepted Q3b sub-case; P4i and escaped companion |
| Heredoc body text | 13 | accepted; P4h |
| Attached redirect target | 2 | accepted; P3-refuse |

Thus 21 hits are correct refusals/probes and 48 are accepted textual false positives. No new
class occurs more than once without a pin or named acceptance. Candidate exit codes were
12,375 zero / 237 two; all 128 base probes returned zero or two (69 / 59). No unexpected
exit code occurred.

Raw rows, automated classes, comparison and manual reconciliation are retained outside git:
`C:\ht\MSYS-AC7\corpus\run-68d52ba7-sol\{corpus.jsonl,summary.json,classes.json,comparison.json,manual-reconciliation.json}`.
The heuristic labels are not the final disposition: the manual reconciliation carries forward
the original 60 reviewed hits and individually classifies the nine additions. Private command
text has not been copied into this repository.
