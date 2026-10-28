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
