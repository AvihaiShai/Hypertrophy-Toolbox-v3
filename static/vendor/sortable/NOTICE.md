# SortableJS — Attribution

Drag-and-drop row reordering on `/workout_plan` uses
[SortableJS](https://github.com/SortableJS/Sortable) 1.14.0 by Lebedev
Konstantin and contributors, used under the MIT License (see `LICENSE`).

`templates/workout_plan.html` loads it as a global; the single consumer is
`Sortable.create(...)` in `static/js/modules/workout-plan-table.js`, which
persists the resulting order through the `exercise_order` column.

## Deviations from upstream

**None.** `Sortable.min.js` is the upstream 1.14.0 production build, verified
byte-identical across cdnjs and the npm distribution. See `VERSION`.

Only the minified UMD build is vendored — the module builds and source map are
not loaded by the application.

## How to refresh

1. Download the new version's `Sortable.min.js` from both cdnjs and npm and
   confirm the two agree before writing either.
2. Update `VERSION` (version, URLs, import date, digest) **and the version
   `e2e/workout-plan.spec.ts` asserts** — it pins `Sortable.version` so a
   silently swapped payload fails.
3. Run `tests/test_local_first_assets.py`, then the `workout-plan` and
   `exercise-interactions` Chromium specs — row reordering is the behavior at
   risk.

## License

The MIT License terms in `LICENSE` cover the upstream source. This `NOTICE.md`
is part of our repo and follows our project license.
