# code-reviewer (agent `a2a2781864144fd32`) - diff-time review of 3d85fd9f, round 1, verbatim final message

I found no high-severity defects, no way for the guard to exit non-2 on a refused-class command, and no way for the monitor to write anywhere except its own snapshot file. I could not execute anything (no shell in this session), so every finding below comes from reading the code and tests. Each should be confirmed with a one-line payload through `outcome_with_stderr` before you act on it.

What I checked and found sound:
- **Guard exit paths.** `Invoke-DriveTokenScan` runs inside the existing `try` (`guard-destructive-command.ps1:1608-1692`), and `$ErrorActionPreference='Stop'` turns any non-terminating error into the `exit 2` catch. The new code only adds to `$script:denials`. Test P8 proves the first-statement throw case.
- **Existing rules.** The diff to the guard is purely additive, so I saw no regression to them.
- **ASCII and BOM.** The existing `HOOK_SCRIPTS` pin covers both hooks (`tests/test_guard_destructive_command.py:948`, `:1037`).
- **Monitor exit codes.** `exit` only ever returns 0, 10 or 11, never 2, so a Stop hook cannot be blocked.
- **Monitor locking.** `FileShare.None` with in-place rewrite and no temp or lock file is consistent between the hook modes and the tests (H1-held, H6).

## Findings, by severity

**1. Low-medium: PowerShell colon-bound parameters are not refused.**
- Evidence: `guard-destructive-command.ps1:918-919`. The boundary excludes `:` (kept so `D:/x` stays allowed), and the attached-option alternative `(?<=...-[A-Za-z]+)` requires the `/` to follow the option letters directly.
- Result: `Set-Content -Path:/d/x -Value hi` in the PowerShell tool matches neither alternative and is allowed. PowerShell binds `Path` to `/d/x`, which resolves to `D:\d\x`, the exact fault this rule exists to stop.
- I found no mention of this in PLANNING.md and no L-row pins it.
- Fix: extend the second lookbehind to `-[A-Za-z]+:?`. Add an R-row (`Set-Content -Path:/d/x hi`, PowerShell, refuse) and a pinned allow for `-Path:D:/x`.

**2. Low: a doubled slash escapes the token pattern.**
- Evidence: `:919`. The segment class `[^/\\...]+` cannot start with `/`, so `/d//x/y` never matches. The later `/x/y` is skipped because it follows `/`.
- Result: in the PowerShell tool, `Set-Content /d//x` is allowed, and Windows normalises it to `D:\d\x`.
- Fix: allow repeated slashes after the letter, for example `(/[A-Za-z]/+[^/\\...]+)`. Add one refuse row.

**3. Low: the directory-change hedge is clobbered by nested scans.**
- Evidence: `:1159` sets `$script:driveTokenHedge` whenever `$depth -eq 0`. The heredoc-body scan (`:1173`) and the interpreter-body scan (`:1225`) call the function at the same `$depth`, so they recompute the flag from the body text alone.
- Result: `cd C:\ && python -c "...'/d/x'..."` refuses without "A directory change in this command may alter this." The message then claims a resolved path it was designed not to claim. This affects the message only, not the decision.
- Test gap: the P1b-cd and P1b-setlocation rows cover only direct PowerShell commands, so nothing pins the heredoc or interpreter case.
- Fix: compute the hedge once per command in the entry loop (`:1655-1658`), or guard it with a parameter instead of `$depth -eq 0`.

**4. Nit: `$` in the converted-prefix regex also matches before a trailing newline.**
- Evidence: `:922`, `^(?:...)?$`. A quoted word whose prefix is only a line feed (`"<LF>/d/x"`) matches `^$` and is treated as offset 0, so it is allowed.
- Practical impact is near zero, but `$sessionIdPattern` in the monitor already uses `\z`.
- Fix: change the trailing `$` to `\z`.

**5. Low (monitor): a stuck "invalid snapshot" notice after a failed baseline write.**
- Evidence: `drive-root-monitor.ps1` HookStop baseline path, diff lines 806-821. If the write throws after `CreateNew` succeeds, a zero-length file remains.
- Result: every later Stop reports "invalid snapshot" and never overwrites it (the rule at diff lines 824-828). Only a `startup` SessionStart clears it.
- Fix: when the exclusively held file has `Length -eq 0`, take the baseline branch instead of the invalid branch. No test pins this.

**6. Informational (monitor): the "ALWAYS exit 0" claim for hook modes has a gap.**
- Evidence: header diff line 64 versus `Invoke-Standalone` (diff lines 615-619) and `exit` (diff line 877).
- A missing or misspelled `-Mode`, or a `-Mode:HookStop` that PowerShell splits into two tokens, falls to the standalone path. It exits 11 and prints a status report, not a `systemMessage`.
- This is non-blocking, because only exit 2 blocks, but it contradicts the header wording.
- Fix: soften the header to "recognised hook modes", or exit 0 silently when `-Mode` starts with `Hook`.

## Test false-green review
I found nothing that could pass vacuously. The allow rows assert `decision == "allow"`, and the refuse rows tie the deny to the drive-token prefix and exclude "failing closed". The one weak spot is the P7 allow-clean sweep: it discards the decision, but only to scan stderr for the two refusal prefixes. The matching allow assertions live in the case-table test.

## Files
- `C:\ht\MSYS\.claude\hooks\guard-destructive-command.ps1`
- `C:\ht\MSYS\.claude\hooks\drive-root-monitor.ps1`
- `C:\ht\MSYS\tests\test_guard_destructive_command.py`
- `C:\ht\MSYS\tests\test_drive_root_monitor.py`