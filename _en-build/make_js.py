# -*- coding: utf-8 -*-
"""Derive en/js/chrome.js from the Hebrew js/chrome.js.

Only two kinds of edit are needed: the strings the script compares against
visible labels (those are English now), and the three places where the logic
itself assumed an RTL reading order.  The data-name selectors stay in Hebrew —
they are Figma layer names, not content, and the markup still carries them.
"""
from tagfit_snippet import TAG_FIT_JS

REPLACEMENTS = [
    # ---- projects.html: status labels the script reads off the cards --------
    ("var overrides = { 'הרא״ז 13': 'מאוכלס', 'ברוק 5, תל אביב': 'מאוכלס', 'האימהות 7-9': 'ברישוי' };",
     "var overrides = { 'הרא״ז 13': 'Occupied', 'ברוק 5, תל אביב': 'Occupied', "
     "'האימהות 7-9': 'In permitting' };"),
    ("return !e.children.length && e.textContent.trim() === 'בשיווק וביצוע';",
     "return !e.children.length && e.textContent.trim() === 'In marketing & construction';"),
    ("var status = 'בשיווק וביצוע';",
     "var status = 'In marketing & construction';"),
    ("wrap.style.cssText = 'display:flex;flex-direction:row-reverse;flex-wrap:wrap;"
     "justify-content:flex-start;gap:80px 40px;width:1188px;max-width:100%;flex-shrink:0';\n"
     "    // row-reverse: the page is dir=ltr (Figma export), so without it the first card\n"
     "    // in the DOM lands on the LEFT and each row reads backwards against the Hebrew.\n"
     "    // With it, DOM order IS reading order — which is what the sort above assumes —\n"
     "    // and a leftover odd card stays on the right, where RTL reading expects it.",
     "wrap.style.cssText = 'display:flex;flex-wrap:wrap;justify-content:flex-start;"
     "gap:80px 40px;width:1188px;max-width:100%;flex-shrink:0';\n"
     "    // a plain row: the English page reads left-to-right, so DOM order is already\n"
     "    // reading order and a leftover odd card stays on the left, where it belongs."),
    ("      var show = label === 'הכל' || label.indexOf(st.replace('מאוכלס', 'מאוכלס')) "
     "!== -1 || label.indexOf(st) !== -1 ||\n"
     "                 (label.indexOf('מאוכלסים') !== -1 && st === 'מאוכלס');",
     "      var show = label === 'All' || label.indexOf(st) !== -1;"),
    ("  var ORDER = ['בשיווק וביצוע', 'ברישוי', 'מאוכלס'];",
     "  var ORDER = ['In marketing & construction', 'In permitting', 'Occupied'];"),
    ("  applyFilter('הכל');", "  applyFilter('All');"),
    ("  mark('הכל');", "  mark('All');"),
    # ---- project.html: apartment tabs --------------------------------------
    ("    return onlySpan && /^דירת [345] חדרים$/.test(e.textContent.trim().replace(/\\s+/g, ' '));",
     "    return onlySpan && /^[345] rooms$/.test(e.textContent.trim().replace(/\\s+/g, ' '));"),
    ("  var active3 = aptTabs.find(function (t) { return t.textContent.trim() === 'דירת 3 חדרים'; });",
     "  var active3 = aptTabs.find(function (t) { return t.textContent.trim() === '3 rooms'; });"),
    # ---- kablanit lightbox: close moves to the far side, arrow keys swap ----
    ('data-lb="close" style="position:absolute;top:28px;left:28px;',
     'data-lb="close" style="position:absolute;top:28px;right:28px;'),
    ("    if (e.key === 'ArrowLeft') show(cur + 1);\n"
     "    if (e.key === 'ArrowRight') show(cur - 1);",
     "    if (e.key === 'ArrowRight') show(cur + 1);\n"
     "    if (e.key === 'ArrowLeft') show(cur - 1);"),
    # ---- gallery dots ------------------------------------------------------
    ("d.setAttribute('aria-label', 'תמונה ' + (i + 1));",
     "d.setAttribute('aria-label', 'Image ' + (i + 1));"),
]


def convert(src):
    out = src
    for a, b in REPLACEMENTS:
        if a not in out:
            raise SystemExit('chrome.js replacement missed:\n' + a[:160])
        out = out.replace(a, b)
    return out + TAG_FIT_JS
