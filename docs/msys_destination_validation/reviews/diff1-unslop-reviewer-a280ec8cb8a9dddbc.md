# unslop-reviewer (agent `a280ec8cb8a9dddbc`) - diff-time review of 3d85fd9f, round 1, verbatim final message

Findings below. Nothing needed changing in the guard header, which matches the new behaviour. I did not review `tests/test_drive_root_monitor.py` in detail.

**1. Stale hedge state on same-depth recursion (contradicts Plan v2 D7)**
`C:\ht\MSYS\.claude\hooks\guard-destructive-command.ps1:1159`
  > `if ($depth -eq 0) { $script:driveTokenHedge = ($text -match $driveTokenDirectoryChange) }`
  Heredoc bodies (line 1173) and interpreter code bodies (line 1225) recurse with the same `$depth`, so a depth-0 body overwrites the flag. D7 says the hedge keys on "the command" containing a directory change. With `cd /x; python -c "...'/d/y'"`, the body's own refusal is built after the flag is reset by the body text. Outer-word refusals afterwards also use the body's value.
  Fix: set the flag once at the entry point, next to `$script:driveTokenCwdLetter` (line 1248), and delete this line. A code-body or heredoc scan at the same depth then can't clobber it.

**2. Review-finding and plan IDs embedded as code comments (item 9)**
  These comments only make sense with `PLANNING.md` open, and they go stale when the plan is edited.
  - `C:\ht\MSYS\.claude\hooks\drive-root-monitor.ps1:316`, `:329`, `:397`, `:432`, `:729`, `:746`, `:806`, `:834`
    > `# D13: one object whose only key is systemMessage.`
    > `# AR-N4: print first, then record, still holding the handle.`
    The same pattern appears at lines 316 (D11), 397 (AC6), 432 (D17), 729 (D13), 746 (D15) and 806 (D14).
  - `C:\ht\MSYS\.claude\hooks\guard-destructive-command.ps1:915` to `:921` and `:1156`
    > `# D3: ...`, `# D4: ... (measured, M-6)`, `# D1: owns its own recursion`
    The same pattern appears at lines 933 (D2), 938 (D7), 949 (D7), 1070 (D5(iii)), 1171 (D6) and 1180 (Q3).
  - `C:\ht\MSYS\tests\test_guard_destructive_command.py:96`
    > `# M-1/M-10/M-11), and the drive-token rule reads it: ... (Q3a strict).`
  Fix: delete the ID prefixes and keep the invariant each comment states. The header-level pointer "Plan v2 D1-D8" / "D9-D18" is enough as the single cross-reference.

**3. Duplicate default-directory logic**
`C:\ht\MSYS\.claude\hooks\drive-root-monitor.ps1:719`
  > `$directory = $parsed.SnapshotDir; if ([string]::IsNullOrEmpty($directory)) { $directory = [IO.Path]::GetTempPath() }`
  `Get-SnapshotPath` (line 603) already applies the same default.
  Fix: resolve the default once in a small helper that both callers use, or drop the default branch from `Get-SnapshotPath` and have `Invoke-Standalone` resolve it too.

**4. Single-caller wrapper, applied inconsistently**
`C:\ht\MSYS\.claude\hooks\drive-root-monitor.ps1:607`
  > `function Get-ProtectedList($parsed) { return @(@($builtinProtected) + @($parsed.Protected.ToArray())) }`
  It has one caller (line 612), while `Get-SnapshotPathRefusal` is passed `$parsed.Protected.ToArray()` directly at lines 639 and 722.
  Fix: inline it at line 612.

**5. Comments that restate the code, in the comment-heavy style this file uses**
  - `C:\ht\MSYS\.claude\hooks\drive-root-monitor.ps1:664`
    > `# Compare: read-only, and ignores what the hooks have announced.`
    This repeats the header's Compare description. Drop it.
  - `C:\ht\MSYS\.claude\hooks\drive-root-monitor.ps1:490`
    > `# In place under the exclusive handle: truncate, write, flush.`
    This paraphrases the next three lines. Drop it.

**6. PLANNING.md prose that the implementation falsifies**
  - `C:\ht\MSYS\docs\msys_destination_validation\PLANNING.md:936` (D7): "If the command contains a ... directory change, the clause is followed by ..." is not what the code does. See finding 1.
  - `C:\ht\MSYS\docs\msys_destination_validation\PLANNING.md:1633` to `:1637`: it says the helper split gives "each AC7 arm one mutation point". The AC7 `neut-guard` arm at about line 1790 of the diff still neutralises only `Invoke-DriveTokenScan`.
  Fix: either update D7 to match the code, or fix the code as in finding 1. Reword the evidence sentence so it matches the arms actually run.

**Checked and not flagged:**
- The unreachable `return` after `while ($true)` (monitor lines 184, 200, 234) is needed for PowerShell class-method return analysis.
- `Get-DriveTokenRegion` and the other small drive-token helpers are single-caller, but the plan documents them as deliberate mutation points.
- The `tool_name` fixture edits in the guard test are the planned Q3a change, with no expected decision altered.
- The guard diff is purely additive, with no unrelated churn. I did not check the plan's "+350 / −0" figure beyond the hunk sizes.