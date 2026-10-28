# unslop-reviewer (agent `a280ec8cb8a9dddbc`) - delta review of a7aa5163, round 2, verbatim final message

Delta review of `a7aa5163`: findings 1, 3, 4 and 5 are resolved, 2 and 6 are partial, and there is new comment slop and stale evidence in the delta. I only read `fix1.diff` and grepped the working tree. I ran no tests, and the inventory was not regenerated.

**Round-1 findings**

1. **Hedge clobber: resolved.** The flag is no longer set inside `Invoke-DriveTokenScan`. It is set once per command at the entry point in `guard-destructive-command.ps1` (`fix1.diff` line 347). Tests `P1b-cd-heredoc` and `P1b-cd-interp` cover it.

2. **Plan and finding IDs in comments: partial.**
   - Both hooks are clean: a grep for `D\d`, `AC\d`, `M-\d`, `Q3`, `AR-`, `TS-` and `Plan v2` in `.claude/hooks/*.ps1` finds nothing.
   - `tests/test_guard_destructive_command.py` is clean of those IDs.
   - `C:\ht\MSYS\tests\test_drive_root_monitor.py` still carries them:
     - `:118` `(D20)`
     - `:373`, `:374`, `:384`, `:386`, `:406` `(D13)`
     - `:414` `"the D12 JSON report"`
     - `:502`, `:503` `(D14)`
   - Fix: delete the parenthetical IDs. Two of them are inside assertion messages.

3. **Duplicate default snapshot directory: resolved.** `Get-SnapshotDirectory` (`drive-root-monitor.ps1`, `fix1.diff` lines 81–84) is the single source. `Get-SnapshotPath` no longer defaults, and both callers use the helper.

4. **`Get-ProtectedList` wrapper: resolved.** It is inlined at its one caller. The line is still repeated verbatim where `Invoke-Standalone` builds the report, but that is now a single use.

5. **Restating comments: resolved.** Both are removed (`fix1.diff` lines 70 and 111).

6. **PLANNING.md prose contradicting the code: partial.**
   - The D7 contradiction is gone now that finding 1 is fixed.
   - The AC7 evidence sentence is corrected, at `PLANNING.md:1653-1657`.
   - The PM's open flag at `PLANNING.md:1744-1751` is not resolved. The `G-message-always` arm is listed as must-fail for `P1b-*` (table line 1319), which now includes `P1b-cd-heredoc` and `P1b-cd-interp`. The manager's own note says that arm does not affect the hedge. The table and the patch must agree, or the merge gate trips.

**New issues in the delta**

- **Review-process prose in code (charter item 9).** These comments describe the review that produced the change, not the code:
  - `tests/test_drive_root_monitor.py`, new `H13-zero-length` test: `# ... (diff-time review addition).`
  - `tests/test_guard_destructive_command.py`: the `# --- diff-time review additions ...` row banners (`fix1.diff` lines 661 and 700) and `(diff-time review)` in the `P1b-cd-*` comment (line 761).
  - Fix: describe the behaviour the rows pin, and drop the review attribution. The measured-conversion note on `A24-A26` is worth keeping.
- **Stale evidence figures in `PLANNING.md`.**
  - Lines 1620, 1626, 1628 and 1637 still say guard "+350 / −0 (1692 lines)", monitor "871 lines", "4127 → 4175" nodes, and "2229 passed".
  - Lines 1620 and 1624 also still say "No pre-existing line edited", but the delta rewrites header, regex and comment lines the first commit added.
  - The delta adds `A24-A26`, `R23`, `R24`, `P1b-cd-*`, `P3-refuse-newline`, `P4i` plus its companion, and `H13`. Fix: re-run the gates and update the numbers, or mark them as measured at `3d85fd9f`.
- **Residual "always exits 0" prose.** `PLANNING.md:970` ("The hook modes always exit 0 (D13)") was not softened to match the header change in the monitor.
- **Header wrap.**
  - The reflowed monitor header has an over-long line, "baseline). A snapshot held by another instance is skipped".
  - The guard header has two over-long lines: the one beginning "boundary, or attached to a short option (-D/d/x, -Path:/d/x)." and the one beginning "attached -X or -X: convert)".
  - Fix: rewrap them to the surrounding width.
- **Misleading helper name.** `d7_sentences` in the guard test keeps a plan ID in its name, although `D7` no longer appears in any comment. Rename it to something like `refusal_sentences`.

**Verified, no slop:**
- The `\z` comment ("`$` also matches before a trailing line feed") records a real constraint.
- The new zero-length comment in `Invoke-HookStop` is a justified invariant note.
- The updated monitor header correctly documents the zero-length baseline and the "recognised hook modes" wording.
- The guard header accurately documents `/d//x`, `-Path:/d/x` and the `-X:` convert prefix.