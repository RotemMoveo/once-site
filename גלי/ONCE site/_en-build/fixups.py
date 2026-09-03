# -*- coding: utf-8 -*-
"""Per-file touch-ups applied after the mechanical mirror + translation.

Everything here is something a generic RTL->LTR pass cannot know:
label wording that has to be re-split around the responsive <span>s,
and the handful of scripts whose maths assumed an RTL scroller.
"""

# --- tab labels -------------------------------------------------------------
# The Hebrew markup puts the removable half of the label FIRST
# (<span class="mw">פרויקטים </span>ברישוי).  In English the removable half is
# the tail, so the two halves swap places.
INDEX = [
('<span class="tlab" data-text="Occupied projects" data-short="Occupied">'
 '<span class="ttxt"><span class="tab-pre">Projects </span>Occupied</span></span>',
 '<span class="tlab" data-text="Occupied projects" data-short="Occupied">'
 '<span class="ttxt">Occupied<span class="tab-pre"> projects</span></span></span>'),

('<span class="tlab" data-text="Projects in marketing &amp; construction" '
 'data-short="In marketing &amp; construction"><span class="ttxt">'
 '<span class="tab-pre">Projects </span>In marketing &amp; construction</span></span>',
 '<span class="tlab" data-text="In marketing &amp; construction" data-short="In marketing">'
 '<span class="ttxt">In marketing<span class="tab-pre"> &amp; construction</span>'
 '</span></span>'),

('<span class="tlab" data-text="Projects in permitting" data-short="In permitting">'
 '<span class="ttxt"><span class="tab-pre">Projects </span>In permitting</span></span>',
 '<span class="tlab" data-text="In permitting" data-short="In permitting">'
 '<span class="ttxt">In permitting<span class="tab-pre"></span></span></span>'),

# --- home slider: the track is an LTR scroller now --------------------------
('  // In RTL, scrollLeft is 0 at start and goes negative (Chrome/FF standard)\n'
 '  function pos(){ return Math.abs(slider.scrollLeft); }',
 '  // LTR scroller: scrollLeft runs 0 -> maxScroll()\n'
 '  function pos(){ return Math.abs(slider.scrollLeft); }'),
("    seg.style.right = (p * (track - segw)) + 'px';",
 "    seg.style.left = (p * (track - segw)) + 'px';"),
("  next.addEventListener('click', function(){ slider.scrollBy({left:-step(), behavior:'smooth'}); });\n"
 "  prev.addEventListener('click', function(){ slider.scrollBy({left:step(), behavior:'smooth'}); });",
 "  next.addEventListener('click', function(){ slider.scrollBy({left:step(), behavior:'smooth'}); });\n"
 "  prev.addEventListener('click', function(){ slider.scrollBy({left:-step(), behavior:'smooth'}); });"),
("  // quote: delay per word by horizontal position -> one RTL wave across all lines",
 "  // quote: delay per word by horizontal position -> one LTR wave across all lines"),
("      var frac = qr.width ? (qr.right - wr.right) / qr.width : 0;",
 "      var frac = qr.width ? (wr.left - qr.left) / qr.width : 0;"),
]

PROJECTS = [
('<span class="mw">Projects </span>In permitting',
 'In permitting<span class="mw"></span>'),
('<span class="mw">Projects </span>Occupied',
 'Occupied<span class="mw"> projects</span>'),
('<span class="mw">Projects </span>In marketing &amp; construction',
 'In marketing<span class="mw"> &amp; construction</span>'),
]

PROJECT = [
('<span class="mw"> </span>5 rooms', '<span class="mw"></span>5 rooms'),
('<span class="mw"> </span>4 rooms', '<span class="mw"></span>4 rooms'),
('<span class="mw"> </span>3 rooms', '<span class="mw"></span>3 rooms'),
]

SEARCH = [
("      count.innerHTML = 'נמצאו <strong>24</strong> תוצאות ב־4 קטגוריות';",
 "      count.innerHTML = 'Found <strong>24</strong> results in 4 categories';"),
("      input.value = none ? 'פנטהאוז ברמת אביב' : 'רחובות';",
 "      input.value = none ? 'penthouse in Ramat Aviv' : 'Rehovot';"),
]

KABLANIT = [
# the Hebrew broke this heading after "foundations"; English is longer, so it
# wraps on its own rather than at a hand-placed break
('Building responsibly — from the foundations<br>to the key.',
 'Building responsibly — from the foundations to the key.'),
]

PAGES = {
    'index.html': INDEX,
    'kablanit.html': KABLANIT,
    'projects.html': PROJECTS,
    'project.html': PROJECT,
    'search.html': SEARCH,
}

# --- rules the generic mirror gets wrong -------------------------------------
# index.html and about.html carry their own inline copy of the chrome CSS, so
# these run over every built file, not just chrome.css.
GLOBAL = [
    # the animated indicator is offset from the left now, so animate `left`
    ('background:var(--night-sky);transition:right .2s linear}',
     'background:var(--night-sky);transition:left .2s linear}'),
    # a tick mark is not mirrored — it has to stay centred on the 16px box.
    # left:2 puts the elbow on the square's vertical axis (2+6 = 8); top:-6.5
    # puts the middle of the drawn mark on its horizontal one.
    (".cbx svg{position:absolute;right:2px;top:calc(50% - 9px)",
     ".cbx svg{position:absolute;left:2px;top:calc(50% - 6.5px)"),
    ("carries only the check. Offsetting the SVG by left:2 / top:-1 puts the check's elbow\n"
     "   at (2+6, -1+12) = (8,11) — horizontally centred, and sitting 3px below the vertical\n"
     "   centre, which reads as balanced because the long arm carries the mark's weight\n"
     "   upward. The arm sweeps out past the top-right corner.",
     "carries only the check. Horizontally the mark is placed by its elbow — left:2 puts\n"
     "   the corner where the two arms meet at 2+6 = 8, the middle of the square. Vertically\n"
     "   it is placed by the mark itself: the drawn path runs from y 0.56 to 12.53 (ends\n"
     "   included), so top:-6.5 lands its middle, 6.54, on the square's middle. Centring the\n"
     "   elbow instead would hang the whole tick above the centre line, which is what it\n"
     "   looked like — the box read as empty at the bottom and the arm shot out of the top\n"
     "   corner. The 45 degree angles and both arm lengths are the original design's."),
    (".cbx::before{content:'';position:absolute;right:0;",
     ".cbx::before{content:'';position:absolute;left:0;"),
    # a long status label breaks over two lines beside the title, rather than
    # lifting onto a line of its own
    ("wrap-reverse is the escape hatch: when the\n   two labels cannot share a line (a narrow phone, or a long English status)\n   the tag lifts onto its own line ABOVE the title, still on the outer edge,\n   instead of shoving the name off the card. */\n.pcard-head{display:flex;flex-wrap:wrap-reverse;align-items:center;gap:6px 12px}",
     "when the two labels cannot share a line\n   (a narrow phone, or a long English status) the tag stays on the title's line\n   and breaks over two lines instead, panel and all: nowrap keeps it out of a\n   line of its own, the title does not shrink, so the tag is the one that gives.\n   The English labels are long enough that lifting the tag put a full-width band\n   above every card. */\n.pcard-head{display:flex;flex-wrap:nowrap;align-items:center;gap:6px 12px}\n.pcard-head h3{flex-shrink:0}\n.pcard-head .ptag{white-space:normal;min-width:0}\n.pcard-head .ptag>svg{flex:0 0 auto}\n/* The same row, as the Figma export builds it on the project and urban-renewal\n   cards: no class there, so it is addressed by its layer name. Same rule — the\n   row does not break, the title does not shrink, the tag does. */\n[data-name=\"\u05e9\u05d5\u05e8\u05ea \u05db\u05d5\u05ea\u05e8\u05ea\"]{flex-wrap:nowrap !important}\n[data-name=\"\u05e9\u05d5\u05e8\u05ea \u05db\u05d5\u05ea\u05e8\u05ea\"]>*{flex-shrink:0 !important}\n[data-name=\"\u05e9\u05d5\u05e8\u05ea \u05db\u05d5\u05ea\u05e8\u05ea\"]>[data-name=\"tag\"],\n[data-name=\"\u05e9\u05d5\u05e8\u05ea \u05db\u05d5\u05ea\u05e8\u05ea\"]>[data-name=\"\u05ea\u05d2\u05d9\u05ea\"]{flex-shrink:1 !important;min-width:0 !important}"),
    # the spec CTA is hand-written CSS but lives inside the export, where
    # flex-end means the right edge of the spec column — the left edge now
    (".spec-cta{align-self:flex-end;text-decoration:none}",
     ".spec-cta{align-self:flex-start;text-decoration:none}"),
    # the wordmark fills its span exactly; anchor it at the text start
    ('.once-mark svg{position:absolute;right:0;',
     '.once-mark svg{position:absolute;left:0;'),
    ('.pgal-prev{left:16px}   /* RTL: right arrow steps back */\n'
     '.pgal-next{right:16px}    /* RTL: left arrow steps forward */',
     '.pgal-prev{left:16px}   /* LTR: left arrow steps back */\n'
     '.pgal-next{right:16px}   /* LTR: right arrow steps forward */'),
    ('inside is aligned to the RIGHT, because the magnifier that opens it lives at\n'
     '   the right end of the nav',
     'inside is aligned to the LEFT, because the magnifier that opens it lives at\n'
     '   the left end of the nav'),
]


# --- frames drawn around Hebrew that English outgrows ------------------------
# The generic pass lets a long line wrap; these are the few boxes whose own
# width is fixed in the export, so the frame itself has to be allowed to give.
EXTRA_CSS = {
'accessibility.html': """
/* the tool chips are a plain row in the export — let them run onto a second line */
#n790,#n801{flex-wrap:wrap}
""",
'kablanit.html': """
/* the heading now wraps over two lines, so cap the text column
   and leave the photo beside it the width it was drawn at */
#n685{flex-shrink:1 !important;min-width:0;max-width:560px}
#n686{flex-shrink:1 !important;min-width:0;max-width:100%}
#n687{flex-shrink:1 !important;min-width:0}
""",
'project.html': """
/* the form column is sized off its heading; let it give way to the photo */
#n242{flex-shrink:1 !important;min-width:0}

/* Stage in the process. Two of the English labels wrap to a second line, and
   the row centres its steps, so those steps sat 12px higher than the rest —
   which broke the track, since each step draws its own half of the line from
   its own top edge. Anchoring the steps to the top puts every circle, and so
   every half-line, back on one axis. Only on desktop: below 769px the row is
   a column and align-items is what centres the stack. */
@media (min-width:769px){
  .pstep-row{align-items:flex-start !important}
}
/* a wrapped label reads as belonging to its circle only if both lines sit
   under it */
.pstep>div:last-child{text-align:center !important}
""",
'urban-renewal.html': """
/* step copy and the three advantage cards read wider in English — let them give */
#n531,#n538,#n545,#n552,#n559{flex-shrink:1 !important;min-width:0}
#n661,#n665,#n669{flex-shrink:1 !important;min-width:0}
""",
}
