# -*- coding: utf-8 -*-
"""Build the English (LTR) copy of the ONCE site into  ONCE site/en."""
import os
import re
import sys
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mirror                                   # noqa: E402
from dict_en import T                           # noqa: E402
import fixups                                   # noqa: E402
import make_js                                  # noqa: E402
from tagfit_snippet import TAG_FIT_JS            # noqa: E402

SRC = os.path.dirname(HERE)          # the Hebrew site, one level up
DST = os.path.join(SRC, 'en')

HEB = re.compile(r'[֐-׿]')
ATTRS = ('aria-label', 'placeholder', 'title', 'alt', 'data-text', 'data-short', 'value',
         'content')

missing = {}
global_hits = set()      # which fixups.GLOBAL entries actually matched somewhere


def apply_global(s):
    for i, (a, b) in enumerate(fixups.GLOBAL):
        if a in s:
            global_hits.add(i)
            s = s.replace(a, b)
    return s

AMP = re.compile(r'&(?![A-Za-z]+;|#\d+;)')


def esc(s):
    """A bare & in a translation has to be written as an entity."""
    return AMP.sub('&amp;', s)


def tr(text):
    """Translate one text run, keeping its surrounding whitespace."""
    core = text.strip()
    if not core or not HEB.search(core):
        return text
    if core in T:
        lead = text[:len(text) - len(text.lstrip())]
        trail = text[len(text.rstrip()):]
        return lead + esc(T[core]) + trail
    missing[core] = missing.get(core, 0) + 1
    return text


def tr_attrs(tag):
    def one(m):
        name, val = m.group(1), m.group(2)
        if name.lower() not in ATTRS or not HEB.search(val):
            return m.group(0)
        core = val.strip()
        if core in T:
            return '%s="%s"' % (name, esc(T[core]))
        missing[core] = missing.get(core, 0) + 1
        return m.group(0)
    return re.sub(r'\b([a-zA-Z-]+)="([^"]*)"', one, tag)


def translate(html):
    out, pos = [], 0
    for m in mirror.TOKEN.finditer(html):
        out.append(tr(html[pos:m.start()]))
        pos = m.end()
        tok = m.group(0)
        if m.group('comment') is not None:
            out.append(tok)
        elif m.group('script') is not None:
            out.append(tok)
        elif m.group('style') is not None:
            out.append(tok)
        elif m.group('close') is not None:
            out.append(tok)
        else:
            out.append(tr_attrs(tok))
    out.append(tr(html[pos:]))
    return ''.join(out)


MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')


def english_dates(s):
    """d.m.yyyy is day-first in Hebrew and month-first to an English reader,
    so spell the month out."""
    def one(m):
        d, mo, y = int(m.group(1)), int(m.group(2)), m.group(3)
        if not 1 <= mo <= 12:
            return m.group(0)
        return '>%d %s %s<' % (d, MONTHS[mo - 1], y)
    return re.sub(r'>(\d{1,2})\.(\d{1,2})\.(\d{4})<', one, s)


ROW_NAME = '\u05e9\u05d5\u05e8\u05ea \u05db\u05d5\u05ea\u05e8\u05ea'      # the export's name for a card's title row
TAG_NAMES = ('tag', '\u05ea\u05d2\u05d9\u05ea')


def title_row_css(html):
    """Keep a card's status tag on the title's line, by id.

    chrome.css already says this for the row as a whole, but projects.html
    forces flex-wrap back on by id inside its own media query, and an id beats
    an attribute selector however many !importants it carries. So the rule is
    restated here against the same ids, in a block that comes after the page's
    own <style>.
    """
    ids = set(re.findall(r'<[^>]*\bid="(n\d+)"[^>]*data-name="%s"' % ROW_NAME, html))
    ids |= set(re.findall(r'<[^>]*data-name="%s"[^>]*\bid="(n\d+)"' % ROW_NAME, html))
    if not ids:
        return ''
    ids = sorted(ids, key=lambda x: int(x[1:]))
    rows = ','.join('#' + i for i in ids)
    kids = ','.join('#%s>*' % i for i in ids)
    tags = ','.join('#%s>[data-name="%s"]' % (i, n) for i in ids for n in TAG_NAMES)
    return ('\n/* a long status label breaks over two lines beside the title, rather than\n'
            '   lifting onto a line of its own — see chrome.css */\n'
            '%s{flex-wrap:nowrap !important}\n'
            '%s{flex-shrink:0 !important}\n'
            '%s{flex-shrink:1 !important;min-width:0 !important}\n' % (rows, kids, tags))


def retarget_assets(s):
    for folder in ('images', 'videos'):
        s = s.replace('"%s/' % folder, '"../%s/' % folder)
        s = s.replace("'%s/" % folder, "'../%s/" % folder)
        s = s.replace('(%s/' % folder, '(../%s/' % folder)
    return s


LD_NAME = re.compile(r'("name":")([^"]+)(")')


def translate_ld(s):
    """The breadcrumb's JSON-LD sits inside a <script>, which `translate` passes
    through untouched — but its names are dictionary labels like any other.
    Written straight from T, without esc(): a bare & is legal inside a script,
    and &amp; would land in the name itself."""
    i = s.find('application/ld+json')
    if i < 0:
        return s
    j = s.index('</script>', i)

    def one(m):
        core = m.group(2)
        if not HEB.search(core):
            return m.group(0)
        if core in T:
            return m.group(1) + T[core] + m.group(3)
        missing[core] = missing.get(core, 0) + 1
        return m.group(0)

    return s[:i] + LD_NAME.sub(one, s[i:j]) + s[j:]


def build_page(name):
    src = open(os.path.join(SRC, name), encoding='utf-8').read()
    s = mirror.mirror_svgs(src)
    s = mirror.mirror_html(s)
    s = s.replace('<html lang="he" dir="rtl">', '<html lang="en" dir="ltr">')
    s = retarget_assets(s)
    s = translate(s)
    s = translate_ld(s)
    s = english_dates(s)
    # שומרים על מספר הגרסה של המקור העברי (עם קידומת en) כדי שכל שינוי
    # ב-chrome.css/js ישבור את המטמון גם באתר האנגלי. גרסה קבועה כמו
    # 'en1' גרמה לדפדפן להמשיך להגיש את הקבצים הישנים אחרי כל תיקון.
    s = re.sub(r'\?v=(\d+)', lambda m: '?v=en' + m.group(1), s)
    for a, b in fixups.PAGES.get(name, []):
        if a not in s:
            raise SystemExit('fixup missed in %s:\n%s' % (name, a[:140]))
        s = s.replace(a, b)
    s = apply_global(s)
    extra = (fixups.EXTRA_CSS.get(name) or '') + title_row_css(s)
    if extra:
        s = s.replace('</head>', '<style>' + extra + '</style></head>', 1)
    # index.html and about.html carry their scripts inline; everything else
    # gets this from chrome.js
    if 'js/chrome.js' not in s and re.search(r'class="[^"]*\bptag\b|data-name="tag"', s):
        s = s.replace('</body>', '<script>' + TAG_FIT_JS + '</script></body>', 1)
    open(os.path.join(DST, name), 'w', encoding='utf-8').write(s)


def build_css(name, physical=False):
    src = open(os.path.join(SRC, 'css', name), encoding='utf-8').read()
    if name == 'site.css':                       # fonts + reset only
        out = src
    else:
        out = mirror.mirror_stylesheet(src, force_physical=physical)
        out = out.replace('url(images/', 'url(../../images/')
        out = apply_global(out)
    open(os.path.join(DST, 'css', name), 'w', encoding='utf-8').write(out)


if __name__ == '__main__':
    os.makedirs(os.path.join(DST, 'css'), exist_ok=True)
    os.makedirs(os.path.join(DST, 'js'), exist_ok=True)
    pages = sorted(f for f in os.listdir(SRC) if f.endswith('.html'))
    for p in pages:
        build_page(p)
        print('page', p)
    for c in ('site.css', 'chrome.css', 'form-states.css'):
        build_css(c)
        print('css', c)
    js = open(os.path.join(SRC, 'js', 'chrome.js'), encoding='utf-8').read()
    open(os.path.join(DST, 'js', 'chrome.js'), 'w', encoding='utf-8').write(make_js.convert(js))
    print('js  chrome.js')
    stale = [a for i, (a, b) in enumerate(fixups.GLOBAL) if i not in global_hits]
    if stale:
        raise SystemExit('GLOBAL fixup no longer matches anything:\n' +
                         '\n'.join(a[:120] for a in stale))
    if missing:
        print('\n--- UNTRANSLATED (%d) ---' % len(missing))
        for k, v in sorted(missing.items(), key=lambda x: -x[1]):
            print(v, repr(k)[:160])
