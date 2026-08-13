# Design Brief

*The visual system that actually ships — tokens, theming, typography, motion, and accessibility,
measured rather than assumed.*

**Derived from:** the CSS bundles at revision `d1efc93`, plus computed styles read from a running
application across **11 pages × 2 themes × 3 viewports** (66 page loads, all HTTP 200), a
reduced-motion pass, and a keyboard-focus pass. **On conflict, the code wins.**

This document describes what shipped. It introduces no design decision and proposes no change.
For how the CSS is structured and how to add to it, see
[`../../.claude/rules/frontend.md`](../../.claude/rules/frontend.md) and
[`../CSS_OWNERSHIP_MAP.md`](../CSS_OWNERSHIP_MAP.md).

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

A light-first, low-contrast "calm glass" surface system: layered neutral surfaces, a single indigo
accent, generous corner radii, soft neumorphic shadows, and translucent blurred panels. Dark mode
is a token swap on `[data-theme="dark"]`, not a separate stylesheet. Sizing is not fixed — nearly
every dimension is a token that steps through **seven viewport bands**, so the same page is
materially denser on a laptop than on a 4K display. Motion is short and uniform, and fully
removed under `prefers-reduced-motion`.

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
| `tokens.css` | 445 | Every design token; the responsive band system |
| `base.css` | 79 | Body background and base typography |
| `layout.css` | 1,678 | Containers, grids, page scaffolding |
| `components.css` | 5,207 | Buttons, cards, tables, badges, inputs, modals |
| `navbar.css` | 1,533 | Navigation bar and its dropdowns |
| `a11y.css` | 664 | Focus, contrast, screen-reader affordances |
| `motion.css` | 73 | Transitions and the reduced-motion override |
| `theme-dark.css` | 574 | Dark-mode corrections beyond the token swap |
| `pages-*.css` (10) | 13,840 total | One per route except `/fatigue`; largest is `pages-workout-plan.css` at 5,808 |

`pages-workout-plan.css` (5,808) and `components.css` (5,207) are each larger than every other
bundle; together they are 11,015 of the 24,093 non-Bootstrap lines — just under half. That is
where the weight is, and the Plan page is where the complexity is.

---

## Color

Eleven color tokens carry the whole palette. Values below are the **computed** values read from
the running application, not the source text.

| Token | Light | Dark | Role | `var()` refs |
|---|---|---|---|---:|
| `--surface-0` | `#eef1f6` | `#0f1220` | Page background | 3 |
| `--surface-1` | `#f4f6fa` | `#161a2d` | Recessed / secondary surface | 57 |
| `--surface-2` | `#ffffff` | `#1d2238` | Raised surface — cards, panels | 101 |
| `--ink-1` | `#0f1220` | `#eef1f6` | Primary text | 129 |
| `--ink-2` | `#4a5170` | `#b4bad0` | Secondary text, table headers | 81 |
| `--ink-3` | `#8a90a8` | `#7a8099` | Tertiary text, hints | 49 |
| `--accent` | `#4c6ef5` | `#4c6ef5` | Single accent — indigo | **247** |
| `--accent-ink` | `#ffffff` | `#ffffff` | Text on accent | 6 |
| `--success` | `#10b981` | `#10b981` | Positive state | 6 |
| `--warning` | `#f59e0b` | `#f59e0b` | Caution state | 4 |
| `--danger` | `#ef4444` | `#ef4444` | Destructive / error | 12 |

Two observations the numbers make plain:

- **`--accent` is used 247 times**, more than the next two tokens combined. This is a
  single-accent system, not a multi-hue palette.
- **The five semantic colors do not change between themes.** Only surfaces and inks swap. Accent,
  success, warning, and danger keep the same hex in dark mode, which is why they read as brighter
  there — the surface moved, not the color.

`--ink-3` is the one exception to the clean light/dark inversion: it goes `#8a90a8` → `#7a8099`,
slightly *darker* rather than mirrored, so tertiary text does not glare on a dark surface.

### Elevation and glass

| Token | Light | Dark | `var()` refs |
|---|---|---|---:|
| `--shadow-neu-out` | soft dual shadow, `rgba(167,175,200,.35)` + white highlight | `rgba(0,0,0,.55)` + `rgba(255,255,255,.04)` | 15 |
| `--shadow-neu-in` | inset variant of the above | inset dark variant | 16 |
| `--shadow-elev-1` | `0 1px 2px / 0 2px 8px rgba(15,18,32,.06)` | **identical** | 9 |
| `--shadow-elev-2` | `0 8px 24px rgba(15,18,32,.10)` | **identical** | 8 |
| `--calm-glass-bg` | `rgba(255,255,255,.55)` | `rgba(29,34,56,.55)` | 12 |
| `--calm-glass-border` | `rgba(255,255,255,.65)` | `rgba(255,255,255,.08)` | 30 |
| `--calm-glass-blur` | `18px` | `18px` | 13 |
| `--calm-glass-sat` | `180%` | `180%` | 12 |

The neumorphic shadows are theme-aware; the flat elevation shadows are **not** — `--shadow-elev-1`
and `--shadow-elev-2` keep identical light-mode values in dark mode, where a shadow tuned for a
light ground has little visible effect. Recorded as measured, not judged.

Glass surfaces are real and live: the navbar computes to
`backdrop-filter: blur(20px) saturate(1.8)` in both themes, over `rgba(255,255,255,.75)` light and
`rgba(11,13,18,.85)` dark. Buttons carry a lighter `blur(4px)`.

---

## Typography

**Three different font stacks are live simultaneously**, which the source alone does not make
obvious.

| Owner | Stack | Applies to |
|---|---|---|
| `base.css` — hardcoded on `body` | `'Inter', Arial, sans-serif` | Body text and anything inheriting from it |
| `--font-sans` token | `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif` | 9 specific declarations in `components.css` and `navbar.css` |
| Four scoped `--*-font` tokens | `ui-sans-serif, system-ui, "Inter", …` | Welcome page, navbar container, workout-plan surfaces, plan dropdowns |

`body` does **not** consume `--font-sans`; `base.css` sets its own stack. And the four scoped
tokens (`--wl-font`, `--nav-font`, `--wp-font`, `--wpdd-font`) put the OS UI font *ahead* of Inter,
so those surfaces prefer the platform font while the rest of the application prefers Inter. Measured
on Home: `body` computes to `Inter, Arial, sans-serif` while `h1` computes to
`ui-sans-serif, system-ui, …`.

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

There is also a **user-controlled zoom** independent of the bands: the navbar `−`/`+` buttons
write a `ui-scale-level` cookie (1–8), which `app.py` maps to a zoom factor from `0.75` to `1.2`,
default level 6 = `1`. Invalid values fall back to 6.

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

## Components, as measured

Computed values on the Plan page at 1440px, both themes.

| Component | Light | Dark |
|---|---|---|
| Page body | bg `#eef1f6`, text `#0f1220` | bg `#0f1220`, text `#eef1f6` |
| Navbar | `rgba(255,255,255,.75)`, blur 20px + saturate 1.8, shadow `0 4px 24px rgba(0,0,0,.08)` | `rgba(11,13,18,.85)`, same blur, shadow `0 8px 32px rgba(0,0,0,.4)` |
| Nav link | translucent tint, pill radius `999px` | translucent dark tint, same radius |
| Primary button | bg `#4c6ef5`, text white, radius 8px, blur 4px | **identical** |
| Secondary button | translucent `--surface-1`, neumorphic shadow | translucent dark, dark neumorphic shadow |
| Table | `rgba(255,255,255,.55)` glass, radius 8px | `rgba(29,34,56,.55)` |
| Table header cell | bg `--surface-1`, text `--ink-2`, padding 10px | bg `#161a2d`, text `#b4bad0` |
| Table body cell | `rgba(255,255,255,.72)`, text `--ink-1` | `rgba(29,34,56,.74)`, text `--ink-1` |
| Text input | translucent `--surface-1` (.88 α), radius 8px | translucent dark, radius 8px |
| Card | `--calm-glass-bg`, radius 8px | dark glass, radius 8px |

The primary button is byte-identical across themes — accent on accent-ink, unaffected by the
surface swap. Table cells are translucent in both themes, which is what makes the glass effect
visible through the data grid.

Table cell padding is genuinely per-page, not per-component: 10px on the Plan page, 12px/16px on
Weekly Summary, 6.4px/8px on Profile — each page bundle tunes its own density.

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

1. `static/js/darkMode.js` reads `localStorage.darkMode`.
2. If nothing is stored it uses `prefers-color-scheme` **and keeps following system changes** until
   the user makes an explicit choice.
3. Clicking the navbar toggle writes `'true'` / `'false'` and stops following the system.
4. The theme is applied by setting `data-theme="light"` or `data-theme="dark"` on `<html>`.

`tokens.css` redefines six surface/ink tokens plus the two neumorphic shadows and two glass
tokens under `[data-theme="dark"]`; `theme-dark.css` (574 lines) carries the corrections the token
swap alone cannot express. Verified live: `data-theme` is `light` and `dark` respectively across
all 11 pages.

Because the whole switch is a token swap on one attribute, **any component that hardcodes a color
instead of consuming a token silently opts out of dark mode.** That is the mechanism behind both
exceptions above.

---

## Motion

Four tokens, and they are genuinely uniform:

| Token | Value | `var()` refs |
|---|---|---:|
| `--dur-fast` | `150ms` | 20 |
| `--dur-base` | `240ms` | 2 |
| `--dur-slow` | `360ms` | 1 |
| `--ease-out` | `cubic-bezier(0.22, 1, 0.36, 1)` | 24 |

Measured: buttons, nav links, and inputs all transition at `0.15s` with `cubic-bezier(0.22,1,0.36,1)`.
`--dur-fast` and `--ease-out` carry essentially the entire system; the slower two are near-unused.
The easing curve is a decelerating ease-out — fast start, soft landing.

**Reduced motion is honored and total.** With `prefers-reduced-motion: reduce`, measured on the
Plan page: `transition-duration: 0s`, `animation-duration: 0s`, and `0s` on `body`. Not shortened
— removed.

---

## Accessibility

- **Skip link.** The first tabbable element on every page is a "Skip to main content" link
  targeting `#main-content`, which carries `tabindex="-1"` so it can receive programmatic focus.
  Verified live: one `Tab` from a fresh page load lands on `.nb-skip-link`.
- **Focus is visible and not suppressed.** That first focused element computes to
  `outline: rgba(13,110,253,.5) solid 2px` with `outline-offset: 2px` — a real, offset ring.
- **Status is never carried by color alone.** Volume classes, fatigue bands, and warnings all
  render a text label beside the color.
- **Controls are labelled.** The icon-only navbar buttons — dark mode, muscle naming, scale −/+ —
  each carry an `aria-label` and a `title`; the scale indicator is `aria-live="polite"`.
- **Modals trap focus.** `static/js/modules/modal-focus-trap.js` loads globally from `base.html`.
- **Toasts announce.** The toast element itself carries `role="alert"`, `aria-live="assertive"`,
  and `aria-atomic="true"` — the live region is the toast, not its positioning container.
- `a11y.css` is 664 lines and loads before the page bundle but after the component bundles.

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
