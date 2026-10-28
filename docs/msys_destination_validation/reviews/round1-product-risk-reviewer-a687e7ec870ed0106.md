# product-risk-reviewer (agent `a687e7ec870ed0106`) — Plan v1 review, round 1, verbatim final message

# Product-risk review of MSYS destination validation Plan v1

**Verdict: Needs revision.** There is one blocking finding on owner-facing copy, and several should-fix findings. I read only the plan and the guard's structure. I did not open the measurements file. My checks are noted per finding.

**Calculation surface claim confirmed.** `PLANNING.md:203-206` says `none`. The artifact table (`:424-434`) touches only `.claude/hooks/*`, two test files, `docs/test_inventory/`, this plan and user-level `~/.claude` files. Nothing under `utils/`, `routes/`, the DB schema or the API is touched. The local-first invariants hold:
- Both controls are local file or text operations with no network path.
- Remediation is out of scope (`:221`).
- The monitor is report-only (Q7, D10).

## Blocking

**B1. D6 / D5 / D3 (`:397-398`): the refusal text claims a resolved path that is false or unknowable in several accepted cases.**
- Invariant at risk: the owner's requirement that copy never claim a guessed resolved path or an unknowable cause.
- Risk, three variants:
  1. D5 (`:397`) concedes that unquoted `powershell -Command New-Item /d/x` is converted by MSYS and refused anyway. D6 would still print "resolves to `D:\d\x`", which is wrong for that case.
  2. D6 takes the payload `cwd` as the resolution drive. A `cd C:\` or `Set-Location` earlier in the same command line, or the nested `bash -c` form that R10 marks unmeasured, changes the real drive.
  3. R3 (`:295`) is a read-only `GetFullPath`. Copy that says it "would create" something would be false.
- Fix: use one fixed, hedged template. Example: `Refused: '<token as written>' is an unconverted POSIX drive path. If the working directory is <X:>, a native Windows program resolves it to <X:\...>; a cd earlier in the command can change that. This is a textual check; it does not know what the command would do.`
  - Omit the resolved path when the command contains `cd`, `Set-Location` or `pushd`.
  - Omit it when MSYS conversion would apply, and say "refused conservatively".
  - Add a P1 test that asserts the hedge text and the absence of "creates" or "would create".

## Should-fix

**S1. D3 token boundary (`:395`): false positives on ordinary agent commands.**
- The boundary excludes only `[\w./:\\]` as a preceding character. These common forms would be refused:
  - globs and pathspecs: `find -path "*/d/*"`, `rg -g '!*/c/*'`, `**/d/**`
  - env and shell expansions: `%USERPROFILE%/a/b`, `${HOME}/c/x`, `(Get-Location)/d/x`, `$(...)/d/x`
  - JS regex literals inside `node -e`: `/a/g` is `/<letter>/<segment>`, with `(` before it
  - `sed 's|/a/b|x|'` in Bash
- Fix: also exclude a preceding `*`, `%`, `}`, `)` and `]`. Add a regex-literal exclusion, such as a flags-only segment `/[A-Za-z]/[a-z]{1,3}\b` after `(` or `,` when the segment is flags-like. Add A-rows for each form. Add a measured corpus pass, described next.
  - Run the final regex over this repo's recent Bash and PowerShell command history, if a transcript source exists. Otherwise run it over the commands quoted in `docs/` and the memory notes. Record the hit count and every false positive in Plan v2.

**S2. Q3b / P4 (`:267`, `:494`): prose in this repo triggers refusals with no recovery path.**
- This repo's docs, PR bodies and commit messages routinely quote `/d/development/...`. For example, `git commit -m "...see /d/x..."`, or `gh pr create --body ...` in either tool, is refused.
- The stated remedy ("write `D:/…`") rewrites the meaning of the text.
- Fix: put the recovery text in the refusal: "if this is prose, put it in a file and pass `-F` / `--body-file`, or write the path drive-qualified". That route works because Write is off the matcher (M-2). Add a test that pins this text.

**S3. D12 (`:404`): a missing snapshot is announced on every Stop.**
- Stop fires at the end of each turn, not at session end. Any session that started before installation, or whose TEMP file was cleaned, would show an UNKNOWN notice every turn. That trains the owner to ignore the channel.
- Fix: in hook mode only, a missing snapshot at Stop creates one now (`CreateNew`). It announces once: "monitoring started mid-session; children created earlier are not covered". Standalone `Compare` keeps AC5's UNKNOWN. Add this as H-row coverage.

**S4. D9 / D10 / D14 notice wording (`:401-406`): the monitor must not imply causation.**
- Several sessions run concurrently on this machine, and each has its own snapshot. A child created by the owner, by another session or by Windows (Q5 admits `C:\` OS children) would be reported by every session as "new".
- Fix: fix the notice wording: `New direct child(ren) of <root> since this session started: <paths>. Cause unknown; not necessarily created by this session.`
  - For `faultShapedPresent`, say "single-letter child exists; this matches the MSYS fault shape but its origin is not known".
  - Add H2 assertions on those exact phrases.

**S5. Installation (`:536-548`): a live user-level guard swap affects every concurrent session and every repo.**
- The user-level guard and `settings.json` take effect immediately in all running sessions across all projects. Any guard that fails closed (exit 2) on a payload shape peculiar to another project would block every Bash and PowerShell call, including the ones needed to roll back. Rollback step 4 is only usable if the tools still work.
- Fix:
  - (a) Before the swap, run the merged blob from a staging path with synthetic payloads: Bash and PowerShell, with and without `cwd`, and a benign command. Assert exit 0.
  - (b) Replace atomically: write `*.new`, verify the hash, then `Move-Item -Force`.
  - (c) Write the exact rollback commands in the plan and confirm they contain no drive token, so they cannot be refused. State that they are runnable from the owner's own terminal.
  - (d) Order the work: copy the monitor file first with no registration; edit `settings.json` last, and only after the guard smoke test passes.
  - (e) The `settings.json` edit touches only the `hooks` object. The plan already says "append" (`:545`); also assert that `permissions`, `env` and every unrelated key are structurally unchanged.

**S6. Operational probe (`:556-559`): `subst Q:` is global to the logon session.**
- A new Fixed drive is mapped for every concurrent session. D13 would make all of them report UNKNOWN for a newly mounted root during the window. The plan does not check whether Q: is free.
- Fix:
  - Pick a letter proven unused, and keep the mapping window to seconds.
  - Record in the evidence that other sessions may show a one-off UNKNOWN notice.
  - Alternatively, drive the probe with a test-only `--settings` file whose hook passes `-Root C:\ht\MSYS-OPS\qroot`. That covers the logic but not the production registration, so label it "registration proven separately".

**S7. AC10 operational claim (`:200-201`, `:560`): the wording is stronger than the evidence.**
- Evidence is a headless CLI 2.1.302 session (M-1). The owner works in the VS Code panel, and notice rendering there is unmeasured. A notice the owner cannot see means the monitor is functionally silent.
- Also, no real drive-root child is ever detected in production. The probe uses `subst`. The guard probe uses one row.
- Fix: record the operational level as "headless; owner-visible notice not demonstrated; detection exercised on a substitute root; one guard row". If feasible, add a VS Code panel check to Step 9, or leave that explicitly open.
- Also record installation as "performed by the manager under delegation". Section 0 AC10 (`:196`) wrote "the owner copies".

## Notes

**N1. Q3a strict plus the tool-name probe (`:266`, `:334`).**
- `tool_name` and `cwd` were measured only on the headless CLI. If the VS Code extension omits or renames either, R12 refuses every command that has a drive-like token, with no guard change at fault.
- Fix: measure one payload from the VS Code panel before Step 7. Alternatively, accept that failure mode explicitly in Plan v2.

**N2. D1 / D6 and AC3 (`:393`).**
- State that the `Invoke-DriveTokenScan` call sits inside the existing try/catch, so an internal error exits 2. Add a P-test that forces an exception inside the scan.

**N3. D11 (`:403`).**
- Snapshot files `claude-drive-root-<id>.json` accumulate in TEMP and are never cleaned. Say so in the header. Do not add deletion; it is out of scope under AC6.

**N4. D10 / D4 hook timing (`:402`, timeout 30).**
- Enumerating fixed-volume roots on every turn can stall on a sleeping or locked volume.
- Fix: record the measured Stop-hook latency in the operational evidence.

**N5. D13 (`:405`).**
- Document that any newly mounted drive during a session yields a one-time UNKNOWN for that root in every open session.

## Confirmed good

- `PREVENTION_COMPLETE` is never claimed (`:227`, `:463-464`, Q6).
- Delegated acceptance is recorded as delegated (`:612`).
- Installation backs up byte-for-byte, with hash records and a read-only hash record of the shared checkout (`:537-540`). The shared checkout's locally modified settings and guard stay untouched (`:418-419`).
- The H4 tree creation-time check is retained (`:171-172`, S0-d).
- D8 rejects an environment-variable root override.

Relevant file: `C:\ht\MSYS\docs\msys_destination_validation\PLANNING.md`