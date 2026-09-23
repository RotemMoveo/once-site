`build_spec.py` writes `../spec.html` — the מפרט טכני page.

    python3 _spec-build/build_spec.py     # from the site folder
    python3 _en-build/build.py            # then regenerate en/

The page's copy lives in `SECTIONS` / `H` at the top of the script, and its CSS in `CSS`.
The shared chrome (nav, menu, search panel, footer) is sliced out of `accessibility.html`
at build time, so a global chrome change reaches this page by rebuilding, not by hand.

Write the CSS in logical properties only (`padding-inline-start`, `inset-inline-start`) —
`_en-build/mirror.py` swaps every physical `left`/`right` it finds in a `<style>` block, so
logical properties are what survive the LTR pass and simply re-read under `dir="ltr"`.
