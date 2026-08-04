# `.d-none` visibility defect — evidence

Fixes the defect recorded as **OD-2 / FU-2** during the table-helper re-audit
([PR #300](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/pull/300)): the
`/volume_splitter` Distribution and AI Suggestions cards rendered on first paint despite
carrying `d-none`.

Base commit `f8988f9`. Branch `wt/dnone-visibility`, isolated worktree, probe server on
port **5301** — verified by command line to be this checkout, never port 5000.

---

## 1. Root cause

`scss/custom-bootstrap.scss:34` imported `bootstrap/scss/utilities`, which only **defines**
the `$utilities` map. The classes are emitted by `bootstrap/scss/utilities/api`, which the
build never imported. **Every `d-*` class in the application has been inert for the app's
whole history** — not a `/volume_splitter` bug, a build-configuration bug with a
`/volume_splitter` symptom.

Measured before the change, on this worktree:

| Utility | Rules setting `display` | Consequence |
|---|---|---|
| `.d-none` | **1**, and it is ID-scoped — `#error-message-container.d-none` (`a11y.css:565`) | every other consumer unaffected by the class |
| `.d-flex` | **0** — the nine `.action-frame .d-flex` rules set only `gap` | 15 call sites computed `block` |
| `.d-inline-block` | **0** | `/fatigue` period `<select>` computed `block`, stretching to **1331px** at 1440 |
| `.d-lg-inline` | **0** | the `d-none d-lg-inline` pair at `base.html:213,219` did nothing |

The two reported cards, measured at four widths before the fix:

| Width | `.results-section` | `.ai-suggestions-section` |
|---|---|---|
| 375 | `block`, 343×142 | `block`, 343×70 |
| 991 | `block`, 460×141 | `block`, 460×141 |
| 992 | `block`, 460×141 | `block`, 460×141 |
| 1440 | `block`, 461×144 | `block`, 461×70 |

The Distribution card carries live **Export Volume Plan** and **Save & Activate** buttons
and an empty table; both were reachable before any split had been calculated.

`#error-message-container` was the one consumer that behaved correctly — and only because
`base.html:271` also carries an inline `style="display: none !important;"`. Someone had
already patched around the missing utility.

---

## 2. Why no gate saw it

- `e2e/volume-splitter.spec.ts:148` asserts `toHaveClass(/d-none/)` — **class-token
  presence**. It stayed green for the entire life of the defect, because the class *was*
  on the element; it simply did nothing.
- `tests/test_css_cascade_contracts.py:494` pins the same literal markup as a hook.

A class token is not a style. Both assertions are true of a class that does not exist.

---

## 3. The fix, and why it is scoped the way it is

```scss
$utilities: (
  "display": map-merge(
    map-get($utilities, "display"),
    (values: none inline)
  )
);

@import "bootstrap/scss/utilities/api";
```

Two narrowings, each measured rather than argued.

**Only the `display` utility.** The full API also emits spacing, colour, border, flex,
sizing and text utilities — hundreds of `!important` selectors this app never asked for,
each a chance to collide with the hand-written bundles.

**Only the `none` and `inline` values.** These are exactly what the defect needs:
`d-none` (12 call sites) and `d-lg-inline`, which is the other half of
`class="d-none d-lg-inline"` at `base.html:213,219`. **The pair is indivisible** —
emitting `d-none` alone would hide those two labels at every width, trading one defect for
another.

### What the wider fix would have cost, measured

The full value list was built and measured first, against a same-machine baseline
generated from the pre-change bundle through a scratch config resolving snapshots under
gitignored `artifacts/`:

| Scope | Rule heads added | Bundle | Visual captures moved |
|---|---:|---:|---|
| whole `display` utility | +83 | +3,369 B | **18 of 66** — volume-splitter ×6, **session-summary ×6, weekly-summary ×6** at 120k–564k px |
| `values: none inline` *(shipped)* | **+20** | **+665 B** | **6 of 66** — volume-splitter only |

The extra twelve come from `d-flex` activating on pages whose JS builds `d-flex` rows
(`session-summary.js:102`, `weekly-summary.js:75,91,120`). Those pages have rendered that
way for the app's entire history; changing them is an owner-reviewed visual decision with
its own baseline regeneration, not something a `.d-none` fix should carry silently.

**Both diffs are pure additions**: 0 rule heads removed, and every added head is a `.d-*`
selector — verified by parsing the built artifact before and after, not by reading the
SCSS.

Emitted by the shipped fix: `.d-none`, `.d-inline`, and their `sm/md/lg/xl/xxl/print`
variants — 20 heads.

---

## 4. Verification

`.d-none` is now a real declaration, read back from the browser's own CSSOM:

```
.d-none  ->  display: none !important   [bootstrap.custom.min.css]
.d-lg-inline -> display: inline !important  [bootstrap.custom.min.css @ (min-width: 992px)]
```

Consumer-by-consumer, before → after:

| Width | Route | Selector | Before | After |
|---|---|---|---|---|
| 375–1440 | `/volume_splitter` | `.results-section` | `block`, up to 461×144 | **`none`, 0×0** |
| 375–1440 | `/volume_splitter` | `.ai-suggestions-section` | `block`, up to 461×70 | **`none`, 0×0** |
| 375 / 991 | `/` | `.navbar .d-none.d-lg-inline` | `inline` | `none` — correct: hidden below `lg` |
| 992 | `/` | same | `inline` | `inline` — correct: shown from `lg` |
| all | `/` | `#error-message-container` | `none` | `none` — unchanged |
| all | any | `.d-flex`, `.d-inline-block` | inert | **inert, deliberately** |

The navbar rows are a behaviour change and are listed as one: those labels were visible
below `lg` only because `d-none` did nothing. Hiding them is what the markup asks for.
`nav-dropdown.spec.ts` — no longer a known red, so a failure there blocks — **passed**.

---

## 5. Regression coverage

**`tests/test_css_display_utilities_contracts.py` — 7 nodes.** The important one is
`test_no_template_uses_a_display_utility_the_build_does_not_emit`: every `d-*` token used
in `templates/**` or `static/js/**` must be emitted by a loaded stylesheet or listed in
`KNOWN_INERT` with a reason. **That contract would have caught the original defect**, and
it catches the next one.

`KNOWN_INERT` is an exact set, asserted in both directions, so it cannot rot into a
blanket exemption: a name that stops being used must be removed, and a name that starts
being emitted must be removed.

**`e2e/volume-splitter.spec.ts` — 3 new tests**, asserting visibility rather than class
tokens: both cards are `toBeHidden()` with computed `display: none` and a null bounding
box on first load; results become visible **only** after Calculate, with content; and
`.d-none` resolves to `display: none !important` in the browser's own CSSOM. The existing
`toHaveClass` test is left in place — not weakened, just no longer the only coverage.

### Red paths — 6 / 6 executed

| Violation | Contract | Result |
|---|---|---|
| remove the `utilities/api` import — the defect itself | `test_the_build_emits_the_display_utility_api` | RED |
| restore the pre-fix bundle | `test_d_none_resolves_to_display_none_important` | RED |
| drop `d-lg-inline` from the emitted set | `test_the_responsive_partner_of_d_none_is_emitted` | RED |
| add `class="d-md-flex"` to a template | `test_no_template_uses_a_display_utility...` | RED |
| add an unused name to `KNOWN_INERT` | `test_the_known_inert_list_has_no_stale_entries` | RED |
| emit `d-flex` after all | `test_the_deliberately_withheld_utilities_stay_withheld` | RED |

Tree byte-identical after every case; contracts 7 passed on restoration.

**A defect in the harness, recorded.** Its first version snapshotted only the production
files, but one red path mutates `KNOWN_INERT` inside the contracts file itself — so the
injected stale entry survived the run and left the suite red. Anything a case writes must
be snapshotted. Restores are from byte snapshots, never `git checkout --`, because this
packet's change is uncommitted and a git restore would revert the fix mid-run.

---

## 6. Gates

| Gate | Result |
|---|---|
| `tests/test_css_display_utilities_contracts.py` | **7 passed** |
| Red paths | **6 / 6** |
| `e2e/volume-splitter.spec.ts` | **30 passed** (27 existing + 3 new) |
| Chromium: `smoke-navigation`, `nav-dropdown`, `dark-mode`, `accessibility`, `summary-pages`, `volume-progress`, `ui-hardening` | **115 passed, 5 failed** — all five pre-existing, see below |
| Seven-surface Stylelint | **2,759 → 2,759 (+0)** — the seven surfaces exclude the generated Bootstrap artifact by design |
| `tsc --noEmit` | clean |
| Test inventory | regenerated, `--check` clean |
| Visual differential (same-machine, scratch snapshot path) | **6 of 66 moved, all `volume-splitter`** — the fix itself |

### The five failures are pre-existing, proven by control

All five are `summary-pages.spec.ts` "Pattern Coverage Analysis" API-structure tests.
Every packet change was stashed and the same five were re-run against the pristine base:
**5 failed, 1 passed** — identical. They are unrelated to this change and are not
introduced by it.

### The `/volume_splitter` baselines will need regeneration

This fix changes what `/volume_splitter` renders, so its six committed captures per
platform no longer match — **that is the fix working**, not a regression. Regenerating and
reviewing them is an owner action; CI never pushes pixels. No snapshot, tolerance, mask or
retry was changed here, and `git status --porcelain e2e/__screenshots__` is empty.

---

## 7. Follow-up, measured and scoped

**`d-flex` (15 call sites) and `d-inline-block` (1) remain inert**, recorded in
`KNOWN_INERT` and pinned by
`test_the_deliberately_withheld_utilities_stay_withheld` so the narrowing cannot widen by
accident. Activating them is a one-line SCSS change — add the values back — but it moves
**session-summary ×6 and weekly-summary ×6** at 120k–564k pixels each, plus the `/fatigue`
period select from `block` to `inline-block`. It needs its own packet, its own visual
review and its own baseline regeneration.

---

## 8. Reproducing this

```bash
# probe server on an isolated port (never 5000 -- a concurrent worktree owns it)
env HT_PORT=5301 FLASK_DEBUG=0 FLASK_USE_RELOADER=0 .venv/Scripts/python.exe app.py
# and confirm the listener is THIS checkout:
#   (Get-CimInstance Win32_Process -Filter "ProcessId=$owner").CommandLine

node artifacts/dnone/probe_d_utilities.mjs --port 5301 --out artifacts/dnone/after.json

# visual differential, snapshots under gitignored artifacts/
PW_SCRATCH_PORT=5302 PW_VISUAL_SEED=1 npx playwright test \
  -c artifacts/dnone/pw-scratch.config.ts --project=chromium e2e/visual.spec.ts

.venv/Scripts/python.exe artifacts/dnone/redpath.py
npm run build:css
```
