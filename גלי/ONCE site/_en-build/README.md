# ONCE — English (LTR) build

`en/` is generated from the Hebrew site one directory up. Regenerate it after
any change to the Hebrew pages:

```bash
python3 "_en-build/build.py"
```

Or let it decide for itself — `_en-build/sync.sh` rebuilds only when a Hebrew
source is newer than the last build (~50ms when there is nothing to do), so it
is cheap to call constantly:

```bash
"_en-build/sync.sh"
```

`deploy.sh` runs it before publishing, so a deploy can never ship an `en/` that
lags the Hebrew site, and it aborts if the build fails. It also backs the
PostToolUse hook in `.claude/settings.json`, which re-syncs `en/` after every
edit Claude makes.

The build reads `../*.html`, `../css/*.css` and `../js/chrome.js`, and writes
`../en/`. Images and videos are not copied — the pages point at `../images/`
and `../videos/`.

| file          | what it does                                                       |
|---------------|--------------------------------------------------------------------|
| `mirror.py`   | RTL → LTR. Mirrors inline styles and stylesheets (padding/margin, left/right, text-align, direction, transforms, border sides), turns Figma's `flex-direction:row` into `row-reverse` inside `.fig-page`, and mirrors the arrow and chevron SVGs. Also relaxes the `white-space:nowrap` the export pins on every text node, because English runs longer than the Hebrew it replaces. |
| `dict_en.py`  | The translation table: every visible string, keyed by its exact Hebrew source. |
| `fixups.py`   | The handful of things a generic pass cannot know — labels that had to be re-split around the responsive `<span>`s, three scripts whose maths assumed an RTL scroller, and the few frames whose fixed width English outgrows. |
| `make_js.py`  | Derives `en/js/chrome.js` from `js/chrome.js`: the strings it compares against visible labels, and the three places the logic assumed RTL. |
| `build.py`    | Runs the above over every page. It **fails loudly** if a fixup no longer matches, and prints any Hebrew string missing from the dictionary — so a change to the Hebrew site surfaces here instead of silently shipping. |

Two deliberate choices worth knowing:

* `data-name` attributes stay in Hebrew. They are Figma layer names, and both
  `chrome.js` and the responsive CSS select on them.
* `.fig-page` keeps `dir="ltr"` (it always had it). The RTL look was built out
  of physical flex values, which is why they are mirrored explicitly rather
  than left to the `dir` attribute.
