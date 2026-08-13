# Inter — Attribution

The UI typeface is [Inter](https://github.com/rsms/inter) by Rasmus Andersson
and the Inter Project Authors, used under the SIL Open Font License 1.1 (see
`LICENSE.txt`). The vendored `.woff2` payloads are the Google Fonts builds of
that family — the exact files `templates/base.html` used to fetch from
`fonts.gstatic.com` — so vendoring them changes the *origin* of the bytes and
nothing about the rendered glyphs.

The pinned release, upstream URLs, and per-file SHA-256 digests are in
`VERSION`.

## Deviations from upstream

1. **`inter.css` is the upstream CSS2 response with rewritten `url()`s.**
   Every `https://fonts.gstatic.com/...` reference became a relative
   `fonts/<subset>.woff2`. `font-family`, `font-style`, `font-weight`,
   `font-display: swap`, and every `unicode-range` are byte-for-byte the
   upstream values, so subset selection and the swap behavior are unchanged.

2. **Files are renamed by subset.** Google serves opaque hashed filenames
   (`UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2`); the vendored copies are named
   `inter-<subset>.woff2` so the tree is readable. `VERSION` maps every local
   name back to the URL it came from.

3. **Nothing is subset out.** All seven unicode subsets Google serves for
   `wght@400;500;600;700` are vendored.

## How to refresh

1. Re-request the CSS2 URL in `VERSION` with a current Chrome `User-Agent`
   (the response is UA-negotiated; an unrecognized UA returns `.ttf`, not
   `.woff2`).
2. Download every `url()` it names, store them under `fonts/` using the
   `inter-<subset>.woff2` convention, and rewrite the CSS `url()`s to match.
3. Update `VERSION` — URLs, import date, and every SHA-256.
4. Run `tests/test_local_first_assets.py`, then the visual matrix in **compare**
   mode. A refreshed font release can move text pixels; that is a deliberate
   rebaseline decision and never an incidental one.

## License

The SIL Open Font License 1.1 terms in `LICENSE.txt` cover the font software.
This `NOTICE.md` is part of our repo and follows our project license.
