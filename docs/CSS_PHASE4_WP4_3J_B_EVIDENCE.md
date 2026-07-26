# WP4.3j-b — Workout Log responsive-ladder audit

**Branch:** `wt/wp4-3j-b-media-ladders` · **Base:** `origin/main` @ `99dfee1`
**Production diff:** none · **Outcome:** audit-only, no-op packet

---

## Original hypothesis

WP4.3j-a recorded 17 media queries in two late regions of
`static/css/pages-workout-log.css` as a possible duplicated responsive ladder:

- the first region begins with the `max-width: 992px` table overflow rule and
  continues through the table's 1280 / 1366 / 1536 / 1600 / 1920 / 2560
  breakpoints;
- the second region contains the `RESPONSIVE FRAME ADJUSTMENTS` block over the
  1200 / 1280 / 1366 / 1536 / 1600 / 1920 / 2560 breakpoints, followed by a
  separate `max-width: 1200px` legend rule.

The candidate packet was to consolidate the two regions without changing
responsive behavior. The audit rejected that premise before any CSS changed:
the regions are not duplicate owners, and the overlapping table/frame
declarations do not render.

## Why the regions are not duplicates

The table rules in the first region use:

```css
.workout-log-table thead th { ... }
.workout-log-table td { ... }
```

The table rules in the frame-adjustment region use:

```css
.workout-log-frame .workout-log-table thead th { ... }
```

The second region additionally assigns `.workout-log-frame` padding. The first
region additionally owns table overflow, page padding, delete-button sizing,
routine-cell widths, and routine typography at selected breakpoints. Combining
the media-query shells merely because their boundaries coincide would obscure
these different selector and property families.

## Actual table-cell owner

The rendered Workout Log table has both `table` and `table-calm` classes inside
`.workout-log-page`, so this shared `components.css` rule matches every header
and body cell:

```css
:is(
  #workout[data-page="workout-plan"],
  .workout-log-page,
  .summary-frame.frame-calm-glass,
  .progression-plan-container
) .table.table-calm > :not(caption) > * > * {
  font-size: var(--wp-table-fs, 0.88rem) !important;
  letter-spacing: 0 !important;
  padding: var(--wp-table-cell-padding, 0.75rem 1rem) !important;
}
```

This is an `:is()` specificity trap. The specificity of `:is()` is that of its
most specific argument, even when a less-specific argument is the branch that
matches the current element. Here:

| Selector part | Specificity |
|---|---:|
| `#workout[data-page="workout-plan"]` (most specific `:is()` argument) | `(1,1,0)` |
| `.table.table-calm` | `(0,2,0)` |
| `:not(caption)` | `(0,0,1)` |
| **Full shared selector** | **`(1,3,1)`** |

The first ladder's `.workout-log-table thead th` is `(0,1,2)` and its
`.workout-log-table td` is `(0,1,1)`. The second ladder's
`.workout-log-frame .workout-log-table thead th` is `(0,2,2)`. None of those
responsive declarations carries `!important`; the shared declarations do.
The shared rule therefore wins on both importance and specificity.

The same shared rule also beats the earlier page-local header and cell groups,
which do carry `!important`: their most specific live selector arms still have
no ID component. This explains why adding progressively more specific
page-local responsive selectors did not change the rendered padding or type
scale.

## Actual frame-padding owner

The base frame block and the responsive frame-adjustment block propose nine
`.workout-log-frame` padding values in total: one base value and eight
responsive values. They all lose to the file's opening rule:

```css
html body .workout-log-frame {
  padding: 0 !important;
}
```

The winner is `(0,1,2)` and important. The base and responsive proposals use
the lone `.workout-log-frame` class, `(0,1,0)`, without `!important`. Computed
frame padding is therefore `0px` throughout the measured width range.

## Browser ownership matrix

The browser walk inspected the winning declaration for each measured property
across every loaded stylesheet, rather than considering source order inside
`pages-workout-log.css` alone.

| Region | Selector/property family | Audit result | Winning owner |
|---|---|---|---|
| First ladder | `thead th` padding, font size, letter spacing | **Proven dead** | Shared `components.css` cell rule |
| First ladder | `td` padding, font size | **Proven dead** | Shared `components.css` cell rule |
| First ladder | `max-width: 992px` table display/overflow | **Not measured** | No claim |
| First ladder | page padding, delete-button sizing, icon sizing, routine-cell width/type | **Not measured** | No claim |
| Frame-adjustment block | eight responsive frame-padding declarations | **Proven dead** | `html body .workout-log-frame` in the same page bundle |
| Frame-adjustment block | seven header padding/font-size pairs | **Proven dead** | Shared `components.css` cell rule |
| Base frame block | base frame-padding declaration | **Proven dead** | `html body .workout-log-frame` in the same page bundle |
| Late legend query | `.legend-item` minimum width | **Not measured** | No claim |

The conclusion is deliberately narrower than "both ladders are dead." Every
declaration in the eight-query `RESPONSIVE FRAME ADJUSTMENTS` block was measured
and found inert. Only the table-cell property families in the first ladder were
measured; its other responsive families remain unclassified. The separate
legend query also remains unclassified.

## Fourteen breakpoint probes

The audit sampled both sides of every transition shared by the measured
1200–2561px property families:

| Transition | Probe widths |
|---|---|
| 1200 / 1201 | `1200`, `1201` |
| 1280 / 1281 | `1280`, `1281` |
| 1366 / 1367 | `1366`, `1367` |
| 1536 / 1537 | `1536`, `1537` |
| 1600 / 1601 | `1600`, `1601` |
| 1920 / 1921 | `1920`, `1921` |
| 2560 / 2561 | `2560`, `2561` |

At all 14 widths, representative header and body cells computed to:

| Property | Computed value | Source expression |
|---|---:|---|
| `padding` | `12px 16px` | `var(--wp-table-cell-padding, 0.75rem 1rem)` |
| `font-size` | `14.08px` | `var(--wp-table-fs, 0.88rem)` |

The frame computed to `padding: 0px` at every probe. None of the measured media
padding or font-size values became a winning computed value; source ownership
also assigns the first ladder's header letter spacing to the shared important
`letter-spacing: 0` declaration. The `992px` overflow rule was outside this
14-probe property audit and is not classified.

## Packet decision

Consolidation was rejected because it would not preserve two live responsive
systems; it would disguise dead-CSS deletion as structural deduplication.
WP4.3j-b therefore closes as an audit-only packet:

- no production CSS changed;
- no test, snapshot, generated Bootstrap, SCSS, JavaScript, template, or
  database file changed;
- no commit or branch may claim a responsive behavior change.

## Owner-gated follow-ups

### Separate Workout Log dead-CSS packet

A later, explicitly authorized deletion packet may remove only the families
proven dead above: the eight-query `RESPONSIVE FRAME ADJUSTMENTS` block and the
dead header/body-cell rule blocks from the first ladder. The base frame-padding
declaration is also proven dead but should be named explicitly if included.
The `992px` table overflow rule, page/button/routine responsive families, and
legend query must remain unless separately audited.

Such a packet needs its own before/after pixel oracle, same-CSS control, cascade
contracts, functional checks, and owner approval. This audit does not authorize
the deletion.

### WP4.4 shared-selector review

The shared `components.css` selector is intentionally left unchanged here. Its
ID-bearing `:is()` arm exports ID-level specificity to the Workout Log, Workout
Plan, summary-frame, and Progression branches, making page-local table-cell
padding and type-scale overrides unexpectedly difficult or impossible.
Ownership repair belongs to WP4.4 shared-bundle work and requires a cross-page
cascade and visual review; this audit records the finding without proposing the
replacement selector or desired responsive behavior.
