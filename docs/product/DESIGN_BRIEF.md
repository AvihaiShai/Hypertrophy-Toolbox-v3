# Design Brief

*The visual system that actually ships — tokens, theming, typography, motion, and accessibility,
measured rather than assumed.*

**Derived from:** the CSS bundles at revision `d1efc93`, plus computed styles read from a running
application across **11 pages × 2 themes × 3 viewports** (66 page loads, all HTTP 200), a
reduced-motion pass, and a keyboard-focus pass. The Workout Plan and Navigation sections
reflect #736. The redesign checks cover the page frame, shared overlays and the rendered
navigation in both themes. [Plan frame](../../e2e/workout-plan-frame.check.ts) ·
[Overlays](../../e2e/overlay-style.check.ts) · [Navigation](../../e2e/nav-dropdown.spec.ts)
**On conflict, the code wins.**

This document describes what shipped. It introduces no design decision and proposes no change.
For how the CSS is structured and how to add to it, see
[`../../.claude/rules/frontend.md`](../../.claude/rules/frontend.md) and
[`../CSS_OWNERSHIP_MAP.md`](../CSS_OWNERSHIP_MAP.md).

## Workout Log pilot

The Workout Log uses a shared page frame with 16 px gutters on phones, 24 px from 768 px,
and 32 px from 1360 px. The empty state gives Import the indigo fill. Once exercises appear,
Import uses an outline and the exercise results take priority. Inter text uses weights 400,
500 and 600. Controls and thumbnails have an 8 px radius, cards use 12 px and status labels
use a pill. Fields have a 1 px `--ink-3` border on `--surface-2` in light and on `--surface-0`
in dark. Light and dark status colors and surfaces come from the same component tokens.

## Why this was measured and not grepped

A design token existing in `tokens.css` is **not** evidence that it owns anything on screen. A
declaration can exist and lose the cascade, or simply have no consumer at all. Every claim below
therefore comes from one of two sources: a **consumer census** counting real `var()` references
across the bundles, or **`getComputedStyle` output** from the running application. Where the two
disagree with the naive reading of the source, the measurement is reported.

That distinction found real things. Seventeen tokens are defined and never referenced. The body
font is not the font token. And one page's tables ignore the theme system entirely.

---

## The system in one paragraph

Neutral surfaces and a single indigo accent carry both themes. The shared navigation, Workout
Log and Workout Plan use opaque surfaces and thin borders. Older components also use translucent
panels, blur and soft shadows. The `[data-theme="dark"]` attribute switches the token values.
Spacing and type adapt across seven viewport bands. Components honor `prefers-reduced-motion`.

## Bundle structure and load order

Eighteen application bundles plus the Bootstrap build artifact. Verified from the live document:

```
vendor/inter/inter.css → tokens.css → bootstrap.custom.min.css → vendor/fontawesome/all.min.css
  → base.css → layout.css → components.css → navbar.css → a11y.css
  → {% block page_css %}      ← this route's page bundle, if it has one
  → motion.css → theme-dark.css
```

Every one of those is served from the application's own origin — the Inter `@font-face` sheet and
Font Awesome are vendored under `static/vendor/`, not fetched from a font service or a CDN. A page
load makes **zero** requests to any external host; verified by capturing every request the browser
issued across four pages, including the two that carry extra vendored libraries.

The `page_css` slot holds whatever that template declares, which is not always just its own
bundle: `/progression` loads the vendored `flatpickr.min.css` there ahead of
`pages-progression.css`.

There are **10 page bundles for 11 page routes**: `templates/fatigue.html` declares no `page_css`
block, so `/fatigue` loads only the global bundles — confirmed by reading the live document's
stylesheet list. Its page-specific styling, including the body heatmap, lives in `scss/_fatigue.scss`,
which is `@import`ed into `custom-bootstrap.scss` and therefore compiles into
`bootstrap.custom.min.css`. That is the one page whose look is carried by the Bootstrap build
artifact rather than by a route bundle, and it is why its local overrides — such as a 12px select
radius where every other page uses 8px — are not findable in `static/css/pages-*.css`.

The tail is load-bearing: **`motion.css` and `theme-dark.css` load after the page bundle**, which
is how reduced-motion overrides and dark theming win over page-specific rules without needing
`!important`. `tokens.css` loads first so everything downstream can consume it.

| Bundle | Lines | Role |
|---|---:|---|
| `tokens.css` | 514 | Design tokens and responsive bands |
| `base.css` | 79 | Body background and base typography |
| `layout.css` | 1,800 | Containers, grids, page scaffolding |
| `components.css` | 4,677 | Buttons, cards, tables, badges, fields and overlays |
| `navbar.css` | 248 | Navigation, its panels and utilities |
| `a11y.css` | 551 | Focus, scale capability, contrast and screen-reader affordances |
| `motion.css` | 91 | Transitions and the reduced-motion override |
| `theme-dark.css` | 471 | Shared dark-mode overrides |
| `pages-*.css` (10) | 7,389 total | Route-specific styling. The Plan bundle accounts for 1,999 lines |

---

## Color

Eleven color tokens carry the shared palette. The values are computed colors from the running
application. The reference counts cover application stylesheets and exclude comments and the
compiled Bootstrap bundle.

| Token | Light | Dark | Role | `var()` refs |
|---|---|---|---|---:|
| `--surface-0` | `#eef1f6` | `#101419` | Page background / inset dark controls | 12 |
| `--surface-1` | `#f4f6fa` | `#192028` | Recessed / secondary surface | 74 |
| `--surface-2` | `#ffffff` | `#26313d` | Raised surface for cards, panels and navigation | 79 |
| `--ink-1` | `#0f1220` | `#f3f6fa` | Primary text | 150 |
| `--ink-2` | `#4a5170` | `#c3ccd7` | Secondary text, table headers | 133 |
| `--ink-3` | `#8a90a8` | `#96a2b1` | Tertiary text, hints | 74 |
| `--accent` | `#4c6ef5` | `#4c6ef5` | Single accent — indigo | 164 |
| `--accent-ink` | `#ffffff` | `#ffffff` | Text on accent | 7 |
| `--success` | `#10b981` | `#10b981` | Positive state | 6 |
| `--warning` | `#f59e0b` | `#f59e0b` | Caution state | 4 |
| `--danger` | `#ef4444` | `#ef4444` | Destructive / error | 9 |

The accent and semantic colors keep their values across themes. Surfaces and inks swap to provide
the contrast each theme needs.

The dark ink ramp is intentionally brighter than the former blue-grey ramp. Tertiary copy remains
visibly subordinate while clearing the raised graphite surfaces without looking dim.

Dark-mode action buttons use a separate muted indigo/brick/forest ramp (`#5264ad`, `#a84f49`, and
`#3f6f5e`) rather than the brighter semantic accent colors. Hover colors remain WCAG-readable with
white text. **Light mode's action palette is unchanged**: light defines the `--action-*` tokens as
`var(--accent)` / `var(--danger)` and the same greens the Excel action already used, so every light
action button computes to the value it did before.

### Elevation and glass

| Token | Light | Dark | `var()` refs |
|---|---|---|---:|
| `--shadow-neu-out` | soft dual shadow, `rgba(167,175,200,.35)` + white highlight | compact black shadow + subtle top edge | 12 |
| `--shadow-neu-in` | inset variant of the above | compact inset black shadow + inner outline | 6 |
| `--shadow-elev-1` | `0 1px 2px / 0 2px 8px rgba(15,18,32,.06)` | `0 2px 8px rgba(0,0,0,.28)` | 8 |
| `--shadow-elev-2` | `0 8px 24px rgba(15,18,32,.10)` | `0 12px 32px rgba(0,0,0,.38)` | 12 |
| `--calm-glass-bg` | `rgba(255,255,255,.55)` | `rgba(25,32,40,.94)` | 10 |
| `--calm-glass-border` | `rgba(255,255,255,.65)` | `rgba(185,203,224,.16)` | 14 |
| `--calm-glass-blur` | `18px` | `18px` | 9 |
| `--calm-glass-sat` | `180%` | `180%` | 8 |

Both neumorphic and flat elevation shadows are theme-aware. Dark mode uses compact black shadows
and a subtle top edge instead of opposing light/dark neumorphic lobes, keeping boundaries visible
without creating additional apparent surface bands.

The fixed navbar and its panels use opaque `--surface-2` in both themes. A 1 px `--ui-hairline`
edge separates the header from the page. The header has zero shadow and backdrop blur.

---

## Typography

| Owner | Stack | Applies to |
|---|---|---|
| `base.css` — hardcoded on `body` | `'Inter', Arial, sans-serif` | Body text and anything inheriting from it |
| `--font-sans` token | `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif` | Shared components |
| `--wl-font` | `ui-sans-serif, system-ui, "Inter", …` | Welcome page |
| Shared header, page frames and `--wpdd-font` | `Inter, sans-serif` | Navigation, Workout Plan, Workout Log and the exercise picker |

`base.css` sets the body stack directly. On Home, `body` computes to `Inter, Arial, sans-serif`
and `h1` uses the Welcome token's system font stack. Navbar controls use Inter 500 at 14 / 20 px.
The brand uses 16 px at weight 600.

Every `var(--font-sans)` reference also carries the full stack as an inline fallback, so the token
failing to resolve changes nothing.

Inter is **vendored**, not fetched: `static/vendor/inter/inter.css` declares weights
400/500/600/700 at `font-display: swap`, pointing at seven `woff2` subsets — latin, latin-ext,
greek, greek-ext, cyrillic, cyrillic-ext, vietnamese — by relative path in the same directory. It
therefore resolves offline, so the fallback entries in the stacks above are a genuine fallback
rather than the normal offline state.

### Type scale

Seven steps, all viewport-responsive. Measured at three widths:

| Token | 390px | 1440px | 1920px |
|---|---|---|---|
| `--font-size-xs` | `0.6rem` | `0.65rem` | `0.7rem` |
| `--font-size-sm` | `0.65rem` | `0.7rem` | `0.75rem` |
| `--font-size-base` | `0.7rem` | `0.75rem` | `0.8rem` |
| `--font-size-lg` | `0.75rem` | `0.8rem` | `0.875rem` |
| `--font-size-xl` | `0.85rem` | `0.9rem` | `1rem` |
| `--font-size-2xl` | `0.95rem` | `1.05rem` | `1.125rem` |
| `--font-size-3xl` | `1.1rem` | `1.2rem` | `1.375rem` |

The base step is below `1rem` at every band. This is a deliberately dense, data-table-oriented
interface, not a reading interface.

`--font-size-xs` is **defined at all seven bands and referenced by nothing.**

---

## The responsive band system

This is the most distinctive thing about the system and the easiest to miss. `tokens.css` redefines
its sizing tokens inside **seven** width bands:

| Band | Range | Intent |
|---|---|---|
| HD | ≤ 1280px | Very compact |
| Laptop | 1281–1366px | Compact |
| Scaled laptop | 1367–1536px | Compact+ |
| HD+ | 1537–1600px | Medium compact |
| FHD | 1601–1920px | Standard compact |
| QHD | 1921–2560px | Standard |
| 4K | ≥ 2561px | Large |

Measured effect on the same page:

| Token | 390px | 1440px | 1920px |
|---|---|---|---|
| `--btn-height` | `24px` | `28px` | `30px` |
| `--layout-space-lg` | `0.5rem` | `0.65rem` | `0.75rem` |
| `--input-height-md` | `26px` | `30px` | `32px` |
| `--table-font-size` | `0.7rem` | `0.75rem` | `0.8rem` |

Two consequences worth knowing before changing anything:

- **There is no mobile band.** The narrowest band is `max-width: 1280px`, so a 390px phone gets
  the same tokens as a 1280px laptop. Mobile layout is handled by Bootstrap's grid and by
  component rules, not by the token scale.
- **A screenshot only ever proves one band.** Any pixel comparison is band-specific; the visual
  suite's viewport choice decides which of the seven is under test.

The navbar `−`/`+` buttons control **application scale** independently of the responsive bands
and browser zoom. They write a `ui-scale-level` cookie (1–8), which `app.py` maps to factors
from `0.75` to `1.2`. Invalid values fall back to level 6 (factor `1`). Browsers that support
CSS `zoom` show the control subject to the existing responsive visibility. Browsers without
CSS `zoom` support hide the control and its trailing divider.
Firefox validation covers version 160.0.1, tested on 2026-11-18.

### Spacing, radius, and container tokens

Two spacing scales coexist, on purpose:

- **`--s-1` … `--s-7`** (4, 8, 12, 16, 24, 32, 48px) — fixed component spacing, never responsive.
  This is the canonical scale.
- **`--layout-space-xs` … `--layout-space-2xl`** — responsive layout spacing. Only `xs`, `sm`,
  `md`, `lg`, and `xl` are actually redefined per band; **`--layout-space-2xl` is declared once at
  `2rem` and never varies**, so despite its name it behaves like a fixed token.
  A deprecated `--space-*` alias family points at these; the aliases still have 24 live references
  across five bundles, so they are not dead.

Radius: `--r-sm` 10px, `--r-md` 14px, `--r-lg` 20px, `--r-xl` 28px, `--r-pill` 999px — plus a
separate `--frame-border-radius` at 8px.

The measured radius on almost every surface is **8px**: cards, buttons, inputs, and tables all
compute to it, and none computes to an `--r-*` value. `--r-pill` (999px) is real and visible on
nav links.

Note what this does *not* establish. The bundles carry **45 literal `border-radius: 8px`
declarations against a single `var(--frame-border-radius)` reference** — so the shared radius is
a convention held by hand, not a token that owns it. Changing that token would move one rule, not
the system. This is the clearest case in the codebase of a visual constant that looks tokenized
and is not.

Containers: `--container-max-fhd` (1800px) and `--container-max-qhd` (2200px) are consumed; the
five Bootstrap-mirroring widths `--container-max-sm` through `--container-max-xxl` are not.

---

## Tokens that own nothing

Seventeen of the 79 tokens defined in `tokens.css` have **zero** `var()` references anywhere in
the bundles. They are inert: changing them changes no pixel.

`--space-xl` · `--space-2xl` · `--container-max-sm` · `--container-max-md` · `--container-max-lg`
· `--container-max-xl` · `--container-max-xxl` · `--input-height-sm` · `--input-height-lg` ·
`--input-min-width` · `--btn-padding-y` · `--btn-height` · `--frame-gap` · `--font-size-xs` ·
`--r-lg` · `--r-xl` · `--s-7`

Recorded, not removed — this document changes nothing. Two are worth flagging specifically because
they read as authoritative and are not: **`--btn-height` is unreferenced**, so the button height
you see comes from padding and line-height, not from that token; and the **top two radius steps**
`--r-lg` / `--r-xl` are unused, so the largest radius actually in play is `--r-md` at 14px.

---

## Components

### Plan Volume Summary and Session Summary

Both pages use the shared page frame, a 24 / 32 px title at every width and a secondary
workbook export action. The projected-fatigue panel precedes muscle group volume,
exercise categories and the conditional isolated-muscle panel. Movement pattern
coverage follows on Weekly. The contribution selector, visible four-band legend and
keyboard-operated definitions and formula disclosure sit with the volume table.

Below 768 px each table row becomes a labelled card with an 8 px corner and a 1 px
`--ink-3` boundary. From 768 px the same cells sit beneath column headers in a
focusable region, with a 1 px row divider. Numeric data uses right-aligned 14 px
tabular Inter. Headers and phone field labels use 12 px Inter. Status text accompanies
the danger, orange, success and purple swatches. Session warnings use a second pill
on the ordinary row surface. Weekly names each warning's priority and each routine's
position relative to its returned target range.

### Workout Plan redesign

The Plan uses the Workout Log frame and the same 16, 24 and 32 px gutters. The list comes
first, with the Add exercise panel below it. The page title uses Inter 600 at 20 / 28 px
below 768 px and 24 / 32 px from 768 px. Section headings use Inter 600 at 18 / 24 px.
Panels use opaque `--surface-2` with 12 px corners. Controls and exercise thumbnails use
8 px corners, and Add exercise uses white text on `--ui-primary` (`#4263eb` light,
`#5264ad` dark). Form fields use a 1 px `--ink-3` border on `--surface-2` in light
and on `--surface-0` in dark.

| Viewport | Plan list |
|---|---|
| Below 768 px | One column of exercise cards |
| 768 px to below 1360 px | Two columns of exercise cards |
| From 1360 px | One table inside a focusable, horizontally scrolling region. Cells have 6 px vertical and 8 px horizontal padding, and the numeric columns align to the end with tabular numerals |

Cards show the routine, exercise and prescription at a glance. Details reveals the
remaining row fields and actions. Cards and table rows share the same data and editing
controls. Linked exercises use a neutral rail and a Superset badge in both themes.

### Navigation and data entry

The fixed header aligns the brand glyph with `--ui-gutter` at 16 px below 768 px, 24 px from
768 px, and 32 px from 1360 px. At application scale 6 the regular header measures 56 px at
390 and 768 px, and 64 px at 1440 px. It compacts on scroll. The menu below 1360 px starts at
the header's bottom edge and scrolls independently to the final control. From 1360 px, the
destinations and utilities fit on one row at scales 6 and 8. The 45 px hamburger keeps its
three-stroke symbol and a pointer target above 44 px at scale 8.

Destinations use bundled Font Awesome Free 5 solid glyphs at `1em`, in the label color. The
server marks the current link with `aria-current="page"`. A 2 px edge in the current color
appears below the link on desktop and along its leading edge in the menu. Analyze also has an
edge when one of its destinations is current. Enabled controls use `--surface-1` on hover.
The glyph and the control hold their position while hovered. [Navigation checks](../../e2e/nav-dropdown.spec.ts)

On phones up to 576 px, each Workout Log label and its value share the full card width.
Desktop column percentages apply above that breakpoint.

The Backup save form uses the shared primary text color in dark mode. The Volume Splitter
paints its recommended interval on the native slider track in both themes. The input keeps
its larger pointer target and native keyboard controls. Template icons must have a glyph in
the bundled Font Awesome Free 5 solid font.

### Shared controls and overlays

The opt-in rules in `components.css` define these values. The starter-plan, execution-style,
Clear Plan, shared reference-video and Clear Log dialogs use the shared modal styles. The
Plan's Volume targets drawer uses the shared drawer surface and backdrop.

| Token | Light | Dark | Role | `var()` refs |
|---|---|---|---|---:|
| `--ui-modal-radius` | `16px` | `16px` | Modal and drawer corners, the exercise picker popover and the exercise image preview | 15 |
| `--ui-danger-fill` | `#c0362c` | `#a84f49` | Filled destructive confirmation with white text | 2 |
| `--ui-drawer-backdrop` | `rgba(10, 15, 30, 0.34)` | `rgba(10, 15, 30, 0.34)` | Backdrop behind the open drawer | 1 |

| Component | Style |
|---|---|
| Pressed button and neutral badge | The pressed button uses `--ink-1` text and an `--ink-3` border on `--surface-1`. The neutral badge uses `--ink-2` on `--surface-1`. |
| Filter chip | A 32 px pill button with 12 / 16 px type and an `--ink-3` border. Its minimum height is 44 px below 768 px. |
| Routine tabs | Tabs wrap. Each tab has an 8 px radius, 14 / 20 px type and a minimum height of 40 px, increasing to 44 px below 768 px. The selected tab uses `--ink-1` text and an `--ink-3` border on `--surface-1`. |
| Menu | The popover aligns with the right edge of the actions row. It uses a `--surface-2` fill, a 12 px radius, a hairline and `--shadow-elev-2`. It is at least 200 px wide when space permits. Items have a minimum height of 40 px, increasing to 44 px below 768 px. The destructive item uses `--ui-danger`. |
| Ruled table and record card | A 1 px `--ink-3` edge draws each card under 1360 px and each table body cell's bottom border from 1360 px. |
| Modal | An opaque `--surface-2` surface, a 16 px radius, a 1 px hairline and `--shadow-elev-2`. The surface, header and footer use `backdrop-filter: none`. The plain header title uses weight 600 and 18 / 24 px type. The body and footer have 16 px padding, with 8 px between footer actions. Dialogs leave a gutter on either side and cap at 480 px for confirmations, 800 px by default and 1120 px for the wide variant. |
| Drawer | The right-hand sheet fills the viewport height and is up to 360 px wide. It uses `--surface-2`, `--shadow-elev-2`, a hairline on the left and 16 px radii on the left corners. The body scrolls vertically and has 16 px padding. The transform transition takes 220 ms. |

Modal and drawer close buttons measure 40 × 40 px, increasing to 44 × 44 px below 768 px.

### Intentional exceptions

**The Backup Center's tables are outside the theme-token system.** Measured on `/backup`, dark
mode: table `rgb(33,37,41)`, header `rgb(52,58,64)`, body cell `rgb(42,42,42)` — Bootstrap's
neutral greys, not `--surface-*`. In light mode the header text is `rgb(80,80,80)` and body text
is pure `rgb(0,0,0)`, neither of which is `--ink-1` or `--ink-2`. Every other page's tables track
the tokens. Recorded as an observed divergence.

**The Fatigue page's select** computes to `rgba(255,255,255,.7)` light / `rgba(40,40,52,.7)` dark
with a **12px** radius, where every other page's select is 8px. Another local override.

**Semantic colors do not invert.** Already noted above and repeated here because it is the most
likely thing for someone to "fix": success, warning, danger, and accent are deliberately identical
in both themes.

---

## Theming mechanism

Dark mode is a `localStorage` toggle, not a media query — though it defaults to one.

1. A parser-blocking `static/js/theme-init.js` in the document head reads `localStorage.darkMode`
   and sets the `<html>` theme before the first stylesheet can paint.
2. `static/js/darkMode.js` initializes the navbar control from that already-applied theme.
3. If nothing is stored the scripts use `prefers-color-scheme` **and keep following system changes** until
   the user makes an explicit choice.
4. Clicking the navbar toggle writes `'true'` / `'false'` and stops following the system.
5. The theme is applied by setting `data-theme="light"` or `data-theme="dark"` on `<html>`.

`tokens.css` redefines six surface/ink tokens plus the neumorphic and elevation shadows and two
glass tokens under `[data-theme="dark"]`. `theme-dark.css` carries overrides for older components.
Navigation uses the shared tokens in `navbar.css`. Its current-location marker and keyboard
focus ring use an accent mixed with the primary ink in each theme.

Because the whole switch is a token swap on one attribute, **any component that hardcodes a color
instead of consuming a token silently opts out of dark mode.** That is the mechanism behind both
exceptions above.

---

## Motion

Four tokens, and they are genuinely uniform:

| Token | Value | `var()` refs |
|---|---|---:|
| `--dur-fast` | `150ms` | 12 |
| `--dur-base` | `240ms` | 2 |
| `--dur-slow` | `360ms` | 1 |
| `--ease-out` | `cubic-bezier(0.22, 1, 0.36, 1)` | 15 |

Common button and input transitions use `0.15s` with `cubic-bezier(0.22,1,0.36,1)`. The navbar's
container animates its minimum height for 150 ms when it compacts. Reduced-motion mode removes
that transition.

**Reduced motion is honored and total.** With `prefers-reduced-motion: reduce`, measured on the
Plan page: `transition-duration: 0s`, `animation-duration: 0s`, and `0s` on `body`. Not shortened
— removed.

---

## Accessibility

- **Skip link.** The first tabbable element on every page is a "Skip to main content" link
  targeting `#main-content`, which carries `tabindex="-1"` so it can receive programmatic focus.
  Verified live: one `Tab` from a fresh page load lands on `.nb-skip-link`.
- **Keyboard focus uses a 2 px outline.** Navbar controls draw it inside the target with
  `--nav-current`. Other controls retain the shared focus ring and offset.
- **Status is never carried by color alone.** Volume classes, fatigue bands, and warnings all
  render a text label beside the color.
- **Controls are labelled.** Theme and muscle naming have visible labels alongside their icons.
  The hamburger and scale buttons have accessible names. The scale indicator announces changes
  with `aria-live="polite"`.
- **The open navbar menu traps focus.** While the hamburger menu is open, Tab wraps inside it and
  page content is inert with scrolling locked. Escape and a click on empty panel space close it and
  return focus to the toggler. Widening the viewport to 1360px or wider releases the trap, the
  scroll lock and the inert state.
- **Modals trap focus.** `static/js/modules/modal-focus-trap.js` loads globally from `base.html`.
- **Toasts announce.** The toast element itself carries `role="alert"`, `aria-live="assertive"`,
  and `aria-atomic="true"` — the live region is the toast, not its positioning container.
- `a11y.css` loads after the component bundles and before the page bundle.

The browser matrix is Chromium-only by decision (`../DECISIONS.md` ADR-004), so these behaviors are
verified on Chromium only.

---

## Reproducing these measurements

Token definitions and their live consumers:

```bash
grep -oE -- "--[A-Za-z0-9-]+\s*:" static/css/tokens.css | sort -u
grep -roE -- "var\(\s*--[A-Za-z0-9-]+" static/css/*.css | sort | uniq -c | sort -rn
```

Match the `var(` pattern, not `var(--token)`. Most references carry an inline fallback —
`var(--font-sans, Inter, …)` — so a search for the closed form reports a false zero. That mistake
is what made `--font-sans` look unused on the first pass.

Computed styles need a running application; the capture used here walked 11 pages × 2 themes ×
3 viewports plus a reduced-motion and a focus pass, reading `getComputedStyle` for each probe.
Before trusting any such capture, hash a served bundle against the on-disk file — a relative
launch inside a worktree has previously served a different checkout's static assets.

**Every computed value in this document therefore has weaker provenance than the token counts**,
which anyone can reproduce from the two commands above. The raw capture is deliberately not
committed: a snapshot of rendered styles goes stale the moment a bundle changes, and a stale
snapshot presented as current is worse than no snapshot. Re-run the capture rather than trusting
these numbers indefinitely.
