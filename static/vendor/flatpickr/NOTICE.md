# flatpickr — Attribution

The goal-date picker on `/progression` uses
[flatpickr](https://github.com/flatpickr/flatpickr) 4.6.13 by Gregory
Petrosyan and contributors, used under the MIT License (see `LICENSE`).

`templates/progression_plan.html` loads both files; the consumer is
`flatpickr(goalDateInput, …)` in `static/js/modules/progression-plan.js`, which
guards on `typeof flatpickr !== 'undefined'`.

## Deviations from upstream

**None in content.** Both files are the upstream 4.6.13 `dist` artifacts.

**One deviation in resolution, and it is the point of the change.** The two URLs
this replaced carried no version at all, so a future upstream release used to
arrive unannounced — on a library that parses a persisted date field. The
resolution pin is recorded in `VERSION`.

Only the default light theme (`flatpickr.min.css`) is vendored, which is the
only stylesheet the page ever loaded. Locale bundles and alternative themes are
not used.

## How to refresh

1. Download `dist/flatpickr.min.js` and `dist/flatpickr.min.css` at the new
   pinned version.
2. Update `VERSION` (version, URLs, import date, both digests).
3. Run `tests/test_local_first_assets.py` and the `progression` Chromium spec —
   date entry, the DD-MM-YYYY display format, and the four-weeks-out default
   are the behaviors at risk.

## License

The MIT License terms in `LICENSE` cover the upstream source. This `NOTICE.md`
is part of our repo and follows our project license.
