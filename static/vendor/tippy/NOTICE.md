# tippy.js — Attribution

Slider and training-day tooltips on `/volume_splitter` use
[tippy.js](https://github.com/atomiks/tippyjs) 6.3.7 by atomiks, used under the
MIT License (see `LICENSE`).

`templates/volume_splitter.html` loads it as a global after Popper, which it
requires. The consumers are the `tippy(...)` calls in
`static/js/modules/volume-splitter.js`, each guarded by
`typeof tippy !== 'function'` — which is why an unreachable CDN degraded the
page to "no tooltips" silently rather than erroring.

## Deviations from upstream

**None in content.** `tippy-bundle.umd.min.js` is the upstream 6.3.7 bundle
build — the artifact the unpkg URL resolved to.

**One deviation in resolution.** The URL this replaced was major-pinned
(`tippy.js@6`), so the application received the latest 6.x at request time. The
resolution pin is recorded in `VERSION`.

The **bundle** build is required, not incidental: it carries tippy's base CSS
and injects it at load. No template links a tippy stylesheet, so a plain UMD
build would leave every tooltip unstyled.

## How to refresh

1. Download `dist/tippy-bundle.umd.min.js` at the new pinned version — the
   bundle build specifically, for the CSS reason above.
2. Confirm the Popper version in `static/vendor/popperjs/` still satisfies the
   new release's peer requirement.
3. Update `VERSION` (version, URL, import date, digest).
4. Run `tests/test_local_first_assets.py` and the `volume-splitter` Chromium
   spec.

## License

The MIT License terms in `LICENSE` cover the upstream source. This `NOTICE.md`
is part of our repo and follows our project license.
