# Popper — Attribution

Tooltip positioning on `/volume_splitter` uses
[Popper](https://github.com/floating-ui/floating-ui) 2.11.8, published as
`@popperjs/core` by Federico Zivolo and contributors, used under the MIT
License (see `LICENSE`).

`templates/volume_splitter.html` loads it as a global immediately before
tippy.js, which requires it. Nothing in this repository calls Popper directly.

## Deviations from upstream

**None in content.** `popper.min.js` is the upstream 2.11.8 UMD build.

**One deviation in resolution.** The URL this replaced was major-pinned
(`@popperjs/core@2`), so the application received the latest 2.x at request
time. The resolution pin is recorded in `VERSION`.

Only the UMD build is vendored; the ESM and development builds are not loaded
by the application.

## Why not reuse Bootstrap's bundled Popper

`static/vendor/bootstrap/js/bootstrap.bundle.min.js` contains its own Popper,
but it is enclosed in the bundle rather than published as the global tippy
resolves. Loading one copy for both would be a behavior change; this packet is
about the origin of bytes, not about consolidating dependencies.

## How to refresh

1. Download `dist/umd/popper.min.js` at the new pinned version and confirm it
   is still the version tippy's peer range accepts.
2. Update `VERSION` (version, URL, import date, digest).
3. Run `tests/test_local_first_assets.py` and the `volume-splitter` Chromium
   spec — slider and training-day tooltips are the behavior at risk.

## License

The MIT License terms in `LICENSE` cover the upstream source. This `NOTICE.md`
is part of our repo and follows our project license.
