# Bootstrap — Attribution

The runtime JavaScript bundle (`js/bootstrap.bundle.min.js`) is
[Bootstrap](https://github.com/twbs/bootstrap) 5.3.8 by The Bootstrap Authors,
used under the MIT License (see `LICENSE`).

`templates/base.html` loads it. It powers the navbar collapse and Analyze
dropdown, the toast container, and the exercise-video modal.

## Second copyright holder: Popper, bundled

The `.bundle.` build embeds
[`@popperjs/core`](https://github.com/floating-ui/floating-ui) — that is what
distinguishes it from plain `bootstrap.min.js` — and **Popper's copyright
notice does not survive upstream's minification**: the only `Copyright` string
in the file is Bootstrap's own banner. While this was fetched from a CDN the
repository distributed nothing; vendoring makes it a redistributed work in git
and in the frozen build, so the notice is restored here:

> MIT License. Copyright (c) 2019 Federico Zivolo and contributors.

The full text is the same MIT license reproduced at
`static/vendor/popperjs/LICENSE`, which this repository also ships for the
standalone Popper that `/volume_splitter` loads.

## Deviations from upstream

**None.** Both files are copied verbatim from the `bootstrap@5.3.8` package
already pinned in `package.json`, and the bundle's SHA-256 was verified equal
to the jsdelivr response for the same version — the URL this replaced. See
`VERSION`.

Only the two `dist/js` artifacts the application loads are vendored; the rest
of the package (SCSS sources, the non-bundled builds, the ESM variants) stays
in `node_modules` where the SCSS build already reaches it.

The source map is vendored so devtools keeps resolving the minified bundle as
it did from the CDN. It embeds the readable Bootstrap and Popper sources, so the
frozen build ships them too — a size and disclosure consequence that is
accepted deliberately rather than incurred silently.

## How to refresh

1. Bump `bootstrap` in `package.json` and reinstall.
2. Copy `node_modules/bootstrap/dist/js/bootstrap.bundle.min.js` and its `.map`
   over these files; update `VERSION` (version, import date, both digests).
3. Re-run `npm run build:css` — `static/css/bootstrap.custom.min.css` is
   compiled from the same package and must not drift from the runtime bundle.
4. Run `tests/test_local_first_assets.py` and the visual matrix in **compare**
   mode.

## License

The MIT License terms in `LICENSE` cover the upstream source. This `NOTICE.md`
is part of our repo and follows our project license.
