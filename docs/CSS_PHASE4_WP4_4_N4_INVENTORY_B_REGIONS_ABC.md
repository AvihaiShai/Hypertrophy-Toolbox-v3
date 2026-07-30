# WP4.4 N4 checkpoint — Inventory B: G3 Workout Log regions A, B and C pre-change measurement

**Status:** pre-change inventory for the N4 owner checkpoint. **Read-only — no production
CSS, template, JavaScript or Python file changed.** This document authorizes nothing.

**Measured commit:** `a895cb043ebfa050429c66ae8749acf65cf0315d` (`main` after PR #209).
**`static/css/pages-workout-log.css`:** SHA-256
`d07e2c07ebe9585df2779ad078a3d5335247a4427cf41420af2497630173c8c6`, 1,621 lines.
**Frozen database:** SHA-256
`7cef8e0acb9106534ba9ff8a935d825d94f913211191f43e46dba830b4da1d47` — the same frozen
probe database WP4.4-h used, so the two measurements are directly comparable.

---

## 1. What G3 asks for

Grounding obligation **G3** ([PLANNING.md](css_phase4_wp4_4/PLANNING.md) §2): *"Workout Log
regions A, B and C remain page-local and ID-free. Any packet that changes shared selector
ownership MUST re-measure A–C before and after. This is a hard gate on packet WP4.4-i, not
advice."* This is the **before** half. The after half is the identical command re-run on
i's branch, diffed on `wins` / `loses`.

**This is not Region H evidence and does not substitute for it.** G9 locks Region H
byte-for-byte by `REGION_H_SHA256` (`tests/test_css_cascade_contracts.py:43`); that is a
*different* constraint with a *different* instrument, and WP4.4-h's "Region H unchanged"
finding discharges G9, not G3. Regions A–C carry no sha256 lock at all — the thing that
protects them is precisely this before/after ownership measurement.

---

## 2. Region identity, resolved structurally

The WP4.3j-c audit named regions A–C by line span in a **2,180-line** file. Two deletion
packets have shipped since (j-b-dead −155, j-c-dead −404), so those spans are stale. A
line-keyed scope already swept up 26 rules including Region H once
(`CSS_PHASE4_WP4_3J_C_DEAD_EVIDENCE.md`). Every region here is therefore anchored on its
**complete normalized selector list**, and an anchor that does not resolve to exactly one
rule is a fatal error.

| Region | Title | Rule lines | Selector arms | Declarations |
|---|---|---|---:|---:|
| **A** | Base light header block | 208–239 | 5 | **20** |
| **B** | Dark-mode header counterpart | 242–260 | 5 | **7** |
| **C** | Base light cell block | 263–284 | 5 | 14 |
| **C** | …alternating-row block | 287–293 | 3 | 1 |
| **C** | …hover block | 295–303 | 3 | 3 |
| | | | **C total: 11** | **18** |
| | | | **A+B+C: 21 arms** | **45** |

**A first-line anchor is not sufficient, and this bit during authoring.**
`.workout-log-table tbody tr:hover td` opens **two different rules**: region C's three-arm
hover block at `:295`, and the standalone `filter: brightness()` hover rule at `:403` that
the j-c arc deliberately left in place. Anchoring on the first selector line conflated them.

### 2.1 G3's own claim, measured

**Every one of the 21 selector arms across regions A, B and C has specificity `a = 0`.**
The ID-free assertion is a fatal precondition of the run, not a conclusion drawn from it.
Range: `(0,1,1)` – `(0,4,2)`. This is the property G3 protects and it currently holds.

That range is the whole problem in one line: the heaviest page-local arm in these regions
is `(0,4,2)`, and the lightest arm of the shared `:is()` family is `(1,2,0)`. No amount of
class stacking crosses `a = 0 → 1`, which is why `!important` on **26** of these 45
declarations buys nothing.

---

## 3. Result

| Verdict | Declarations |
|---|---:|
| **always wins** — owns every longhand it declares, in every context | **9** |
| **mixed** — wins some contexts/elements, loses others | **6** |
| **never wins** — suppressed everywhere measured | **30** |
| no record | **0** |
| **Total** | **45** |

| Region | always-wins | mixed | never-wins |
|---|---:|---:|---:|
| A (20) | 7 | 3 | 10 |
| B (7) | 0 | 1 | 6 |
| C (18) | 2 | 2 | 14 |

**56,304 ownership records** over 12 contexts (`/workout_log` × light/dark × 375/768/1440 px
× rest/hover). Of those: **8,028 wins**, **30,618 losses to the shared `components.css`
`:is()` family**, **17,658 losses to some other owner**.

### 3.1 The number that matters for WP4.4-i

| Blocking owner | Declarations | Resurrection risk if i lowers the family's weight |
|---|---:|---|
| loses **only** to the `components.css` `:is()` family | **16** | **direct** — nothing else is above them |
| loses to the `:is()` family **and** to something else | **13** | **partial** — i changes which rule wins, not whether a page-local rule wins |
| loses only to **non-`:is()`** owners (page-local, or other `components.css` rules) | 7 | none from i |
| never loses | 9 | none |

**29 of the 45 region A/B/C declarations are currently suppressed, at least in part, by the
selector WP4.4-i exists to repair.** Sixteen of those have *no other* rule above them: if
the `:is()` arm stops out-weighing them, they become winners and Workout Log's header and
cell paint changes. That is precisely the "uncontrolled resurrection of suppressed rules"
R3 forbids accepting.

Directly at risk (the 16):

| Region | Declaration IDs | Properties |
|---|---|---|
| A | A6, A9, A11, A18, A19, A20 | `padding`, `font-size`, `letter-spacing`, `font-weight`, `box-shadow`, `text-shadow` |
| B | B25, B26, B27 | `border-top`, `box-shadow`, `text-shadow` |
| C | C28, C30, C31, C39, C40, C41, C44 | `padding`, `border-bottom`, `font-size`, `color`, `transition`, `box-shadow` ×2 |

Partially at risk (the 13): A3, A4, A7, A8, A17, B21, B22, B23, B24, C37, C38, C42, C43 —
mostly `background` / `background-color` / `color` / `border-bottom`, which also contend
with the page's own `#workout-log-table … .metric-lane` rules (those carry an ID and are
unaffected by i).

### 3.2 Region B is the sharpest case

Region B has **zero** always-wins declarations. Six of its seven never win anywhere, and
three of those (`border-top`, `box-shadow`, `text-shadow`) lose *only* to the `:is()`
family. The dark-mode Workout Log header is painted almost entirely by `components.css`
today. A repair that de-weights the family flips the majority of this block live in one
step, in dark mode, on a route the visual matrix covers — the highest-signal red i can
produce, and the one most worth predicting before writing anything.

### 3.3 The full per-declaration table

Machine-readable, with the complete losing-owner set for every declaration:
`artifacts/wp4_4/n4-regions-abc/summary.json` (`perDeclaration`) and
`artifacts/wp4_4/n4-regions-abc/records.json` (all 56,304 records). Generated output stays
gitignored under A11; §5 reproduces it.

---

## 4. Controls — all clean, all fatal

| Control | Rule | Result |
|---|---|---|
| Specificity model unit checks | M4 | **10 / 10 pass**, asserted before use |
| ID-free assertion (G3's own claim) | G3 | **passed** — all 26 arms have `a = 0` |
| DOM presence | — | 1 table, **17** header cells, **102** body cells in all 12 contexts |
| Dark-theme presence | — | `data-theme="dark"` and **17** dark-matched header cells in all 6 dark contexts |
| **Same-CSS control** | M5 | every context captured twice — **56,304 records, 0 differing** |
| **Known-live control** | M5 | live winners found in **A (10), B (1), C (4)** — no region reports zero |
| **Resolution self-check** | M4 | **4,800 checked, 0 mismatches** |
| Transition settling | M6a | transitions finished via the Web Animations API before any computed read |

### 4.1 Three oracle defects the controls caught, every one pointing "dead"

The known-live control existed because a sweep that reports everything dead is
indistinguishable from a broken sweep. It fired three times during authoring, and each
failure would have shipped a confident false verdict:

1. **`!important` declarations returned zero records.** Matching an authored declaration to
   its CDP candidate by *value equality* fails because CDP re-serializes, and `!important`
   moves between `value` and `text` depending on the property. Every important declaration
   in all three regions — most of the file — read as "not present in the cascade". Fixed by
   matching on **source range** (`CSSProperty.range.startLine`), which is exact.
2. **Region B returned zero records entirely.** Chrome re-serializes `[data-theme='dark']`
   with double quotes, so an exact selector-string comparison never matched the dark header
   rule. Region B would have been reported as having no cascade presence at all.
3. **The alternating-row rule returned zero records.** Chrome re-serializes
   `:nth-child(even)` as `:nth-child(2n)` — the same defect WP4.3j-c-dead documented, hit
   again from a different direction. Separately, `white-space` is now a *shorthand* over
   `white-space-collapse` / `text-wrap-mode`, so a static longhand table missed it in both
   A and C.

All three are the same root cause: **comparing what the browser gives back to what the
author wrote.** The fix was to stop comparing strings and key membership off source line
identity, which no re-serialization can move. Method note worth carrying: *a selector or
property name that survives a round trip through the CSSOM is not the string you wrote.*

---

## 5. Reproduction

The harness is committed at
[`scripts/css_audit/n4_regions_abc.mjs`](../scripts/css_audit/n4_regions_abc.mjs) rather
than left under `artifacts/` — G3 requires the *identical* run again after any repair, and
a gitignored one-off cannot satisfy a before/after gate (A11).

```bash
# from a checkout at a895cb0, with artifacts/wp4_4/probe-frozen.db in place
node scripts/css_audit/n4_regions_abc.mjs \
  --frozen-db artifacts/wp4_4/probe-frozen.db \
  --expect-db-sha  7cef8e0acb9106534ba9ff8a935d825d94f913211191f43e46dba830b4da1d47 \
  --expect-css-sha d07e2c07ebe9585df2779ad078a3d5335247a4427cf41420af2497630173c8c6 \
  --out artifacts/wp4_4/n4-regions-abc
# → "PASS — all controls clean"
```

The script boots the app itself against an isolated copy of the frozen database
(`DB_FILE`, `FLASK_DEBUG=0`, `FLASK_USE_RELOADER=0`), deletes the `-wal` / `-shm` sidecars
before copying — a stale WAL silently reverted a freshly seeded database during WP4.4-h and
produced `td = 0` — and asserts both file digests before measuring. It writes nothing to
the repository outside `--out`.

For the **after** run, pass the repaired `--expect-css-sha` and diff `perDeclaration`:
any declaration whose `wins` rises from 0 is a resurrection and must be accounted for
explicitly.

---

## 6. What this inventory does *not* establish

- **It is not a safety proof for any repair shape.** It says what is currently suppressed
  and by whom. N3 requires proving, per branch, that no page-local rule *would become* a
  winner — that is a different measurement, and on this evidence 29 declarations are
  candidates to fail it.
- **It covers Workout Log only.** G3 names A–C specifically, but the `:is()` family reaches
  **five** routes. Workout Plan, Weekly Summary, Session Summary and Progression have not
  been swept for would-become-winners. Workout Plan additionally carries the ten frozen
  WP4.3i interaction-state declarations (G6) and `tr.superset-group-1..4` (PR#6), both of
  which sit under the same branch.
- **Interaction coverage is hover only.** Focus, focus-visible, focus-within and active were
  not driven. M12 excludes them from the deletion packets; it does not exclude them from i.
- **`filter: saturate(1.02) brightness(0.99)`** (C45) loses to the region-G hover `filter`
  rules WP4.3j-d retained, not to the `:is()` family. It is unaffected by i and is recorded
  here so a future reader does not re-litigate it.
