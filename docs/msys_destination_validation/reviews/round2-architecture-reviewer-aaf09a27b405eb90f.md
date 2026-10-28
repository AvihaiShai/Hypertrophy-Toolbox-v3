# architecture-reviewer (agent `aaf09a27b405eb90f`) — Plan v2 delta review, round 2, verbatim final message

# Round 2 delta review: Plan v2 against my round-1 findings

I read Plan v2 (lines 770-1225) and M-10 cold. All round-1 findings are resolved except AR-S3, which is resolved with a caveat. There are no new blocking findings.

## Round-1 status

| ID | Status | Evidence |
|---|---|---|
| AR-B1 (P6 can never fail under G-noop) | Resolved | P6a is a 4-level drive-token deny, and P6b is a 5-level existing-reason pin (989-990). G-noop lists P6a as expected-fail and P6b as expected-pass (1063). |
| AR-B2 (D1 "once at entry" vs D5 recursion) | Resolved | D1 owns its recursion, uses `Split-Segments`/`Remove-Wrappers`/`Get-Delegation`/`Get-VerbCandidates` read-only, and never edits `Invoke-CommandScan` (787). D5(iii) mirrors the `$(...)` loop (791). |
| AR-S1 (M-6 vs D4 prefix) | Resolved | D4 prefix is `^(?:[A-Za-z0-9_.-]+=)*(?:-[A-Za-z]+)?$` (790). It accepts `a=b=` and `OUT2=--o=`, and S0-a is deleted (903). |
| AR-S2 (M-7 vs Q5) | Resolved | D10 states that fixed volumes include `subst` (796). The operational `subst` probe is unconditional (1120-1126). |
| AR-S3 (resume baseline, invalid file) | Resolved, with caveat | D14 is keyed on `source`. Invalid files are replaced at SessionStart and never at Stop, and the F1 ruling keeps a single self-locking file (800, 1188-1197). I accept the Stop-time `CreateNew` under the same handle (1198-1200) as still one file. Caveat: see N-2 below. |
| AR-S4 (stdout channels) | Resolved | D13 (799), H1 and H2 (1022-1026). |
| AR-S5 (prose false positives, remedy) | Resolved | D7 remedy text and P4b (793, 983). |
| AR-S6 (P4 rows name tool/region) | Resolved | D8 and P4a-g (794, 982-986). |
| AR-S7 (interpreter-body detection) | Resolved, with caveat | D5(i) covers `Get-VerbCandidates` path forms and `-Ic` clusters (791). Caveat: see S-3 below. |
| AR-S8 (non-atomic install) | Resolved | Installation steps 3-7 stage, parse and probe, then `.new` + hash + `Move-Item -Force`, with a re-probe and a rollback script (1095-1111). |
| AR-S9 (docs surface, handover) | Resolved | `CLOSEOUT.md` and hook headers are the surface, and `MASTER_HANDOVER.md` is out of scope (876, 892). |
| AR-S10 (enumeration semantics) | Resolved | D11 (797). |
| AR-N1 | Resolved | D19 (805). |
| AR-N2 | Resolved | D21 (807). |
| AR-N3 | Resolved | Accepted gaps (943-946). |
| AR-N4 | Resolved | D15 prints, then records (801). |
| AR-N5 | Resolved | Coverage limits (1135). |

## New findings

**Should-fix**

- **S-1. PLANNING.md:793, 1205-1207, 858-859 — D7 withholds the resolved path beyond the owner's must-address (5).**
  - AC1 literally says the refusal names "the path it resolves to on the drive of the payload's `cwd`". Must-address (5) grounds withholding only for a missing or invalid `cwd`. D7 also withholds it for any command containing `cd`/`Set-Location`/`sl`/etc., and for every conservative refusal. The manager records this as a "delegated interpretation of AC1", but it narrows an owner-approved AC on a ground the owner did not give.
  - Fix: keep the path in those cases as a conditional clause, for example `if unconverted from cwd <X:>: <X:\...>`. That satisfies AC1 literally and stays hedged. Otherwise record it as an AC1 amendment awaiting owner ratification, not as an interpretation.
  - Also require word-boundary matching for the `cd`/`sl` detection, since a bare substring test on `sl` would withhold the clause far too often.

- **S-2. PLANNING.md:967, 791, 1209 — R20 refuses a word that AC2 says must not be refused, while the plan claims "no narrowing".**
  - `python -c "x=/d/y"` has a `NAME=` prefix, which AC2 lists as measured-converted and "not refused". The F4 ruling states that "AC1(b) is literal, with no narrowing".
  - Fix: state the AC1(b)-over-AC2 precedence for interpreter code bodies explicitly as a delegated reconciliation, alongside the F3 note.

- **S-3. PLANNING.md:791 (D5(i)) — "`-c` anywhere in its arguments" mis-classifies tool arguments.**
  - `python -m pytest -c pytest.ini` and `python -m pip install -c constraints.txt` carry `-c` as a tool option after `-m`. The following token would be refused as a "code body".
  - Fix: scan only interpreter options that precede the first non-option token or `-m <module>`. Add a row for `python -m pytest -c /d/x/pytest.ini` showing the intended outcome.

- **S-4. PLANNING.md:788, 1138 — no subagent-originated payload has been measured.**
  - M-1 and M-10 measured main-thread PreToolUse payloads only. The guard also runs from charter frontmatter in subagents (the senior-developer and automation-qa charters, matcher `Bash|PowerShell`), and with `agent_id` set.
  - If `tool_name` were absent there, strict Q3a would refuse every `/d/...` command from subagents.
  - Fix: add a measurement (M-11) of a subagent PreToolUse payload before implementation, or add a subagent probe to operational acceptance.

- **S-5. PLANNING.md:759, 1131-1132, 1138-1139 — M-10 contradicts three plan statements.**
  - M-10 measured the VS Code extension's bundled `claude.exe` 2.1.310 headless. Both tools carried `tool_name` and `cwd`, and the Stop `systemMessage` notice appeared.
  - Plan v2 still says `tool_name` and `cwd` from VS Code are "not separately measured", and the PR-N1 row says "Not measured from VS Code".
  - Fix: update those texts to "measured for the bundled 2.1.310 binary in headless mode; panel rendering unmeasured". Consider running the operational guard probe with that binary as well.

**Notes**

- **N-1. D4 and A16-A21:** D4 does not say how a "drive-token occurrence" is found in a Bash word. A16-A21 and the G-boundary arm only work if it uses D3's token and boundary rules. State that.
- **N-2. Snapshot schema:** the schema is not specified (version field, roots map, `reported[]`). D16, D17 and the mid-session notice each need "announced once" state, and M4's "wrong-schema" test needs a version field to be well-defined. Specify the schema in D14.
- **N-3. M-lock discrimination is host-dependent:**
  - On Linux, .NET maps a share mode other than `None` to a shared flock. A test holding `LOCK_EX` would still block it, so H6 would not fail under the mutation there.
  - The AC7 arms run on Windows, so this does not affect AC7. Record that M-lock is proven on the Windows hosts only.
- **N-4. Heredoc prose (D6, D8):** heredoc bodies that mention `/d/x` (for example `git commit -F - <<EOF`) are refused, but they are not in the D8 pinned list. The D7 remedy ("put the text in a file") should name the Write tool, which is unhooked here and converts only `file_path`. Add a P4 row.
- **N-5. Corpus pass (step 6):** no decision rule is given for an unacceptable false-positive rate. State what outcome blocks the PR, for example any false-positive class not already in D8.
- **N-6. Hard-coded H4 paths:** `protected[]` embeds owner-specific `D:\` paths in a committed script. This is acceptable as print-only (D12). Keep the protection checks themselves testable only through `-ProtectedPath`, as R16 already states.

**Verdict: no blocking findings**

Files read: `C:\ht\MSYS\docs\msys_destination_validation\PLANNING.md` (704-1229) and `C:\ht\MSYS\artifacts\msys-gate0-20261028\MEASUREMENTS_20261028.md` (M-10, lines 81-88).