# -*- coding: utf-8 -*-
"""Latin typography for the English site.

The Hebrew pages set their type in two embedded families: Almoni for display
(headings, the hero, the big footer links) and Google Sans for everything
else. English has no reason to be set in a Hebrew face, so the build can swap
both for Geist — one family, the same three weights, from `fonts/`.

`PAGES` is the switch. It lists the pages the swap applies to, so the font can
be tried on one page before the site follows:

    PAGES = ()                  # off — Almoni + Google Sans, as now
    PAGES = ('index.html',)     # just the home page
    PAGES = ALL                 # the whole English site, site.css included

The faces are read from `fonts/*.woff2` and embedded as base64, exactly like
the fonts they replace — an English page stays self-contained, with no font
request of its own.
"""
import base64
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

FAMILY = 'Geist'
FACES = (('Geist-Regular.woff2', 400),
         ('Geist-Medium.woff2', 500),
         ('Geist-Bold.woff2', 700))

# the families the Hebrew pages embed, display first
REPLACED = ('Almoni', 'GoogleSans')

ALL = 'all'

# ──────────────────────────────────────────────────────────────────────────
# 2026-09-23: the trial is over — the whole site, Hebrew and English, keeps
# its original type (Almoni + Google Sans). The swap stays here, off.
PAGES = ()
# ──────────────────────────────────────────────────────────────────────────

# Geist sets the card title wider than Almoni did, and under 769px the status
# tag is an ordinary flex item beside it. With min-width:0 the tag shrank past
# its own longest word and the label ran out of the pill; the title yields the
# room instead. It wraps, and the row is as tall as the three-line tag either
# way. (The Figma-export pages name that row #nNNN rather than .pcard-head —
# see title_row_css in build.py — so they will want the same two lines keyed by
# id when Geist goes site-wide.)
GUARD_CSS = """
/* Geist is wider than the face this row was spaced for: the title gives up the
   room so the status tag keeps its own longest word — see fonts_en.py */
@media (max-width:768px){
  .pcard-head h3{flex-shrink:1;min-width:0}
  .pcard-head .ptag{min-width:auto}
}
"""

FACE_BLOCK = re.compile(r"@font-face\{[^}]*font-family:'(%s)'[^}]*\}" % '|'.join(REPLACED))
DUPES = re.compile(r"'%s'(?:\s*,\s*'%s')+" % (FAMILY, FAMILY))


def covers(name):
    return PAGES == ALL or name in PAGES


def _faces():
    out = []
    for fn, weight in FACES:
        with open(os.path.join(HERE, 'fonts', fn), 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('ascii')
        out.append("@font-face{font-family:'%s';src:url(data:font/woff2;base64,%s) "
                   "format('woff2');font-weight:%d;font-style:normal;font-display:swap}"
                   % (FAMILY, b64, weight))
    return '\n'.join(out)


def swap(s):
    """Point one page (or site.css) at Geist. Raises if it finds nothing to swap."""
    blocks = list(FACE_BLOCK.finditer(s))
    if not blocks:
        raise SystemExit('fonts_en: no Almoni/Google Sans @font-face to replace')
    # the Geist faces take the place of the first block; the rest go
    s = s[:blocks[0].start()] + _faces() + FACE_BLOCK.sub('', s[blocks[0].end():])
    for name in REPLACED:
        s = s.replace("'%s'" % name, "'%s'" % FAMILY)
    # '<display>','<text>',Arial,sans-serif collapses to one family
    return DUPES.sub("'%s'" % FAMILY, s)
