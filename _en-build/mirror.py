# -*- coding: utf-8 -*-
"""RTL -> LTR mirroring for the ONCE site.

Two contexts:
  * "physical"  — markup inside .fig-page, which is dir=ltr.  The RTL look is
                  built out of physical flex values, so every horizontal value
                  has to be mirrored by hand.
  * "logical"   — the hand-written chrome, which inherits dir from <html>.
                  flex-start/end and the *-inline-* properties flip on their
                  own once dir becomes ltr; only physical properties move.
"""
import re

VOID = {'area','base','br','col','embed','hr','img','input','link','meta',
        'param','source','track','wbr'}

# ---------------------------------------------------------------- declarations

def split_decls(s):
    """Split a declaration list on ';' that are not inside () or quotes."""
    out, buf, depth, q = [], [], 0, None
    for ch in s:
        if q:
            buf.append(ch)
            if ch == q:
                q = None
            continue
        if ch in '"\'':
            q = ch; buf.append(ch); continue
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if ch == ';' and depth == 0:
            out.append(''.join(buf)); buf = []
        else:
            buf.append(ch)
    out.append(''.join(buf))
    return out


def split_values(v):
    """Split a value on top-level whitespace."""
    out, buf, depth = [], [], 0
    for ch in v:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if ch.isspace() and depth == 0:
            if buf:
                out.append(''.join(buf)); buf = []
        else:
            buf.append(ch)
    if buf:
        out.append(''.join(buf))
    return out


def swap_box(val):
    """padding/margin/inset shorthand: swap the 2nd and 4th value."""
    imp = ''
    m = re.search(r'!\s*important\s*$', val)
    if m:
        imp = val[m.start():]; val = val[:m.start()]
    parts = split_values(val)
    if len(parts) == 4:
        parts[1], parts[3] = parts[3], parts[1]
        return ' '.join(parts) + imp
    return val + imp


def swap_radius(val):
    imp = ''
    m = re.search(r'!\s*important\s*$', val)
    if m:
        imp = val[m.start():]; val = val[:m.start()]
    if '/' in val:
        return val + imp
    parts = split_values(val)
    if len(parts) == 4:          # tl tr br bl -> tr tl bl br
        parts = [parts[1], parts[0], parts[3], parts[2]]
    elif len(parts) == 3:        # tl (tr bl) br -> tr (tl br) bl
        parts = [parts[1], parts[0], parts[1], parts[2]]
    else:
        return val + imp
    return ' '.join(parts) + imp


def neg(numstr):
    n = numstr.strip()
    if n.startswith('-'):
        return n[1:]
    if n.startswith('+'):
        n = n[1:]
    if re.match(r'^0(\D|$)', n) and not re.match(r'^0\.[1-9]', n):
        return n
    return '-' + n


def flip_transform(val):
    def tx(m):
        return m.group(1) + neg(m.group(2)) + ')'
    val = re.sub(r'(translateX\(\s*)([^)]+)\)', tx, val)
    val = re.sub(r'(translate3d\(\s*)([^,)]+)', lambda m: m.group(1) + neg(m.group(2)), val)

    def tr(m):
        args = m.group(2).split(',')
        args[0] = neg(args[0])
        return m.group(1) + ','.join(args) + ')'
    val = re.sub(r'(\btranslate\(\s*)([^)]+)\)', tr, val)
    return val


PROP_SWAP = {
    'padding-left': 'padding-right', 'padding-right': 'padding-left',
    'margin-left': 'margin-right', 'margin-right': 'margin-left',
    'left': 'right', 'right': 'left',
    'border-left': 'border-right', 'border-right': 'border-left',
    'border-left-width': 'border-right-width', 'border-right-width': 'border-left-width',
    'border-left-style': 'border-right-style', 'border-right-style': 'border-left-style',
    'border-left-color': 'border-right-color', 'border-right-color': 'border-left-color',
    'border-top-left-radius': 'border-top-right-radius',
    'border-top-right-radius': 'border-top-left-radius',
    'border-bottom-left-radius': 'border-bottom-right-radius',
    'border-bottom-right-radius': 'border-bottom-left-radius',
    'scroll-padding-left': 'scroll-padding-right', 'scroll-padding-right': 'scroll-padding-left',
    'scroll-margin-left': 'scroll-margin-right', 'scroll-margin-right': 'scroll-margin-left',
}

FLIP_KEYWORD = {'left': 'right', 'right': 'left'}


def parse_decl(d):
    i = d.find(':')
    if i < 0:
        return None
    return d[:i], d[i + 1:]


def own_direction(decls):
    """row / column / None, from a parsed declaration list."""
    fd = None
    for d in decls:
        p = parse_decl(d)
        if not p:
            continue
        name = p[0].strip().lower()
        val = p[1].strip().lower()
        if name == 'flex-direction':
            fd = val.replace('!important', '').strip()
        elif name == 'flex-flow':
            for tok in split_values(val):
                if tok in ('row', 'row-reverse', 'column', 'column-reverse'):
                    fd = tok
    if fd is None:
        for d in decls:
            p = parse_decl(d)
            if p and p[0].strip().lower() == 'display' and 'flex' in p[1]:
                return 'row'
        return None
    return 'column' if fd.startswith('column') else 'row'


def mirror_decls(css, physical, parent_dir=None, dir_hint=None):
    """Mirror one declaration list. `physical` = flex values are physical.

    A rule in a media query often sets align-items without saying which way the
    box runs, so the axis cannot be read off the declarations alone; `dir_hint`
    carries it in from the element the selector points at.
    """
    decls = split_decls(css)
    my_dir = own_direction(decls) or dir_hint
    is_flex = any((parse_decl(d) or ('', ''))[0].strip().lower() == 'display'
                  and 'flex' in (parse_decl(d) or ('', ''))[1] for d in decls)
    has_fd = any((parse_decl(d) or ('', ''))[0].strip().lower() in ('flex-direction', 'flex-flow')
                 for d in decls)

    out = []
    for d in decls:
        p = parse_decl(d)
        if not p:
            out.append(d); continue
        raw_name, raw_val = p
        name = raw_name.strip().lower()
        lead = raw_name[:len(raw_name) - len(raw_name.lstrip())]
        val = raw_val
        low = val.strip().lower()

        if name in PROP_SWAP:
            name_out = PROP_SWAP[name]
            out.append(lead + name_out + ':' + val)
            continue
        if name in ('padding', 'margin', 'inset', 'scroll-padding', 'scroll-margin'):
            out.append(lead + raw_name.strip() + ':' + swap_box(val))
            continue
        if name == 'border-radius':
            out.append(lead + raw_name.strip() + ':' + swap_radius(val))
            continue
        if name == 'text-align':
            v = low.replace('!important', '').strip()
            if v in FLIP_KEYWORD:
                out.append(lead + raw_name.strip() + ':' + val.lower().replace(v, FLIP_KEYWORD[v], 1))
            else:
                out.append(d)
            continue
        if name == 'direction':
            out.append(lead + raw_name.strip() + ':' + val.replace('rtl', 'ltr'))
            continue
        if name == 'float' or name == 'clear':
            v = low.replace('!important', '').strip()
            if v in FLIP_KEYWORD:
                out.append(lead + raw_name.strip() + ':' + val.lower().replace(v, FLIP_KEYWORD[v], 1))
            else:
                out.append(d)
            continue
        if name == 'transform':
            out.append(lead + raw_name.strip() + ':' + flip_transform(val))
            continue
        if name == 'transform-origin':
            v = val
            if '%' in v:
                v = re.sub(r'(^|\s)(\d+(?:\.\d+)?)%', lambda m: m.group(1) + str(100 - float(m.group(2))).rstrip('0').rstrip('.') + '%', v, count=1)
            out.append(lead + raw_name.strip() + ':' + v)
            continue
        if name == 'background-position':
            v = re.sub(r'\bleft\b', '\x00', val)
            v = re.sub(r'\bright\b', 'left', v).replace('\x00', 'right')
            out.append(lead + raw_name.strip() + ':' + v)
            continue

        if physical:
            if name == 'flex-direction':
                v = low
                if 'row-reverse' in v:
                    out.append(lead + raw_name.strip() + ':' + re.sub('row-reverse', 'row', val, flags=re.I))
                elif re.search(r'\brow\b', v):
                    out.append(lead + raw_name.strip() + ':' + re.sub(r'\brow\b', 'row-reverse', val, flags=re.I))
                else:
                    out.append(d)
                continue
            if name == 'flex-flow':
                if 'row-reverse' in low:
                    out.append(lead + raw_name.strip() + ':' + re.sub('row-reverse', 'row', val, flags=re.I))
                elif re.search(r'\brow\b', low):
                    out.append(lead + raw_name.strip() + ':' + re.sub(r'\brow\b', 'row-reverse', val, flags=re.I))
                else:
                    out.append(d)
                continue
            if name == 'align-items' and my_dir == 'column':
                out.append(lead + raw_name.strip() + ':' + flip_fx(val))
                continue
            if name == 'align-self' and parent_dir == 'column':
                out.append(lead + raw_name.strip() + ':' + flip_fx(val))
                continue
        out.append(d)

    res = ';'.join(out)
    if physical and is_flex and not has_fd:
        # display:flex with no flex-direction is a row -> mirror it
        res = res.rstrip()
        sep = '' if (not res or res.endswith(';')) else ';'
        res = res + sep + 'flex-direction:row-reverse'
    if physical and 'white-space:nowrap' in res.replace(' ', ''):
        # The export pins every text node to nowrap at a width measured off the
        # Hebrew string it used to hold.  English runs longer, so the line is
        # allowed to wrap - and, inside a row, to give way - which reflows a
        # long translation instead of spilling it out of its frame.
        res = re.sub(r'white-space\s*:\s*nowrap', 'white-space:normal', res)
        # Alignment on a line that could not wrap was invisible, and the export
        # set it either way. Now that the line can wrap, it shows — so a text
        # that isn't deliberately centred reads from the start of the line.
        if not re.search(r'text-align\s*:\s*(center|justify)', res):
            res = re.sub(r'text-align\s*:\s*right', 'text-align:left', res)
        if parent_dir == 'row':
            res = re.sub(r'flex-shrink\s*:\s*0\b', 'flex-shrink:1', res)
            if 'min-width' not in res:
                res = res.rstrip().rstrip(';') + ';min-width:0'
    return res


def flip_fx(val):
    if re.search(r'flex-start', val, re.I):
        return re.sub(r'flex-start', 'flex-end', val, flags=re.I)
    if re.search(r'flex-end', val, re.I):
        return re.sub(r'flex-end', 'flex-start', val, flags=re.I)
    return val


# ---------------------------------------------------------------- style sheets

FIGSEL = re.compile(r'#n\d+|\[data-name|\.fig-page|\.cards-grid')


ID_SEL = re.compile(r'#([A-Za-z][-\w]*)')


def sheet_directions(css):
    """id -> flex axis, for ids a rule in THIS sheet gives a direction to."""
    out = {}
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', css):
        d = own_direction(split_decls(m.group(2)))
        if d and 'flex-direction' in m.group(2) or (d and 'flex-flow' in m.group(2)):
            for i in ID_SEL.findall(m.group(1)):
                out[i] = d
    return out


def _hint(sel, prop, dirmap, sheetdirs):
    """The axis a bare align-items / align-self should be read against."""
    if not dirmap:
        return None
    ids = ID_SEL.findall(sel)
    if not ids:
        return None
    seen = set()
    for i in ids:
        if prop == 'align-items':
            seen.add(sheetdirs.get(i) or (dirmap.get(i) or (None, None))[0])
        else:
            seen.add((dirmap.get(i) or (None, None))[1])
    seen.discard(None)
    return seen.pop() if len(seen) == 1 else None


def mirror_stylesheet(css, force_physical=None, extra_physical=(), dirmap=None,
                      sheetdirs=None):
    """Walk a stylesheet, mirroring each rule body.

    A rule is treated as `physical` when its selector points into the Figma
    export (#nNNN / [data-name=...]) or is listed in extra_physical.
    """
    if sheetdirs is None:
        sheetdirs = sheet_directions(css)
    out = []
    i = 0
    n = len(css)
    while i < n:
        # comments
        if css.startswith('/*', i):
            j = css.find('*/', i + 2)
            j = n if j < 0 else j + 2
            out.append(css[i:j]); i = j; continue
        # at-rule with a block (media / supports / keyframes)
        m = re.match(r'@[\w-]+[^{;]*', css[i:])
        if m and i + m.end() < n and css[i + m.end()] == '{':
            head = m.group(0)
            start = i + m.end() + 1
            depth = 1
            j = start
            while j < n and depth:
                if css[j] == '{':
                    depth += 1
                elif css[j] == '}':
                    depth -= 1
                j += 1
            inner = css[start:j - 1]
            at = head.split()[0].lower()
            if at in ('@media', '@supports', '@layer', '@container'):
                out.append(head + '{' + mirror_stylesheet(inner, force_physical, extra_physical,
                                                          dirmap, sheetdirs) + '}')
            elif 'keyframes' in at:
                out.append(head + '{' + mirror_stylesheet(inner, force_physical, extra_physical,
                                                          dirmap, sheetdirs) + '}')
            else:
                out.append(head + '{' + inner + '}')
            i = j
            continue
        # plain rule
        k = css.find('{', i)
        if k < 0:
            out.append(css[i:]); break
        sel = css[i:k]
        j = css.find('}', k)
        if j < 0:
            out.append(css[i:]); break
        body = css[k + 1:j]
        # a comment sitting above a rule is part of this slice; an id mentioned
        # in prose must not decide how the rule is read
        bare = re.sub(r'/\*.*?\*/', '', sel, flags=re.S)
        if force_physical is None:
            phys = bool(FIGSEL.search(bare)) or any(e in bare for e in extra_physical)
        else:
            phys = force_physical
        hint = pdir = None
        if phys:
            hint = _hint(bare, 'align-items', dirmap, sheetdirs)
            pdir = _hint(bare, 'align-self', dirmap, sheetdirs)
        out.append(sel + '{' + mirror_decls(body, phys, pdir, hint) + '}')
        i = j + 1
    return ''.join(out)


# ---------------------------------------------------------------- html walking

TOKEN = re.compile(
    r'(?P<comment><!--.*?-->)'
    r'|(?P<script><script\b[^>]*>.*?</script\s*>)'
    r'|(?P<style><style\b[^>]*>.*?</style\s*>)'
    r'|(?P<close></\s*([A-Za-z][-\w:]*)\s*>)'
    r'|(?P<open><\s*([A-Za-z][-\w:]*)((?:"[^"]*"|\'[^\']*\'|[^>"\'])*?)(/?)>)',
    re.S)

STYLE_ATTR = re.compile(r'(\sstyle\s*=\s*")([^"]*)(")', re.S)
DIR_ATTR = re.compile(r'(\sdir\s*=\s*")([^"]*)(")')


def mirror_html(html, page_physical_root='fig-page', extra_physical=()):
    """Mirror inline styles.  Only markup inside .fig-page is treated as
    physical; everything else is dir-aware chrome."""
    dirmap = collect_dirs(html)
    out = []
    pos = 0
    stack = []            # list of dicts: tag, physical, dir
    in_svg = 0

    def cur_physical():
        for fr in reversed(stack):
            if fr['fig']:
                return True
        return False

    def parent_dir():
        return stack[-1]['dir'] if stack else None

    for m in TOKEN.finditer(html):
        out.append(html[pos:m.start()])
        pos = m.end()
        tok = m.group(0)

        if m.group('comment') is not None:
            out.append(tok); continue
        if m.group('script') is not None:
            out.append(tok); continue
        if m.group('style') is not None:
            head, inner, tail = re.match(r'(<style\b[^>]*>)(.*)(</style\s*>)', tok, re.S).groups()
            out.append(head + mirror_stylesheet(inner, None, extra_physical, dirmap) + tail)
            continue
        if m.group('close') is not None:
            name = m.group(5).lower()
            if name == 'svg':
                in_svg = max(0, in_svg - 1)
            for idx in range(len(stack) - 1, -1, -1):
                if stack[idx]['tag'] == name:
                    del stack[idx:]
                    break
            out.append(tok); continue

        # open tag
        name = m.group(7).lower()
        attrs = m.group(8)
        selfclose = m.group(9)
        newtok = tok

        if name == 'svg':
            in_svg += 1
            out.append(newtok)
            if not selfclose:
                stack.append({'tag': name, 'fig': False, 'dir': None})
            continue

        if in_svg:
            out.append(newtok)
            if not selfclose and name not in VOID:
                stack.append({'tag': name, 'fig': False, 'dir': None})
            continue

        fig = 'fig-page' in attrs
        phys = cur_physical() or fig
        mydir = None

        sm = STYLE_ATTR.search(attrs)
        if sm:
            newstyle = mirror_decls(sm.group(2), phys, parent_dir())
            mydir = own_direction(split_decls(sm.group(2)))
            if phys and mydir == 'row':
                mydir = 'row'
            newattrs = attrs[:sm.start()] + sm.group(1) + newstyle + sm.group(3) + attrs[sm.end():]
            newtok = '<' + m.group(7) + newattrs + selfclose + '>'

        out.append(newtok)
        if not selfclose and name not in VOID:
            stack.append({'tag': name, 'fig': fig, 'dir': mydir})

    out.append(html[pos:])
    return ''.join(out)


# ---------------------------------------------------------------- svg arrows

DIRECTIONAL_D = {
    'M12.5002 4.26172H1.8335', 'M12.5007 4.26172H1.83398', 'M12.5 4.26367H1.83333',
    'M12.5007 4.76172H1.83398', 'M15.334 5.20703H2.29688', 'M9.5 3.32227H1.5',
    'M8.5 1L1.5 5L8.5 9', 'M4.5 8.5L0.5 4.5L4.5 0.5', 'M3.5 6.5L0.5 3.5L3.5 0.5',
    'M0.5 0.5L4.5 4.5L0.5 8.5',
    'M5.5549 10.3872L0.666016 5.49826L5.5549 0.609375', 'M4.5 9L0.5 5L4.5 1',
    'M12.5007 4.26172H1.83398Z', 'M15 5.5H1M1 5.5L5.5 1M1 5.5L5.5 10',
    'M11.1631 12L22.4248 12',
    'M5 16L27 16', 'M27 16L5 16', 'M14 25L5 16L14 7', 'M18 7L27 16L18 25',
    'M12 6L22 16L12 26', 'M20 6L10 16L20 26',
}

NUM = r'-?\d*\.?\d+(?:[eE]-?\d+)?'


def _fmt(x):
    s = ('%.5f' % x).rstrip('0').rstrip('.')
    return s if s not in ('', '-0') else '0'


def mirror_path_d(d, W):
    out = []
    for m in re.finditer(r'([A-Za-z])([^A-Za-z]*)', d):
        cmd, args = m.group(1), m.group(2)
        nums = re.findall(NUM, args)
        if cmd in 'ML' and len(nums) >= 2 and len(nums) % 2 == 0:
            pts = []
            for i in range(0, len(nums), 2):
                pts.append('%s %s' % (_fmt(W - float(nums[i])), nums[i + 1]))
            out.append(cmd + ' '.join(pts))
        elif cmd == 'H' and nums:
            out.append('H' + ' '.join(_fmt(W - float(n)) for n in nums))
        elif cmd in 'Zz':
            out.append(cmd)
        else:
            out.append(cmd + args)
    return ''.join(out)


def collect_dirs(html):
    """id -> (its own flex axis, its parent's), read off the inline styles.

    The Figma export gives every box an id and an inline style, so the axis a
    media-query rule is silent about can be looked up here.
    """
    dirs = {}
    stack = []
    in_svg = 0
    for m in TOKEN.finditer(html):
        if (m.group('comment') is not None or m.group('script') is not None
                or m.group('style') is not None):
            continue
        if m.group('close') is not None:
            name = m.group(5).lower()
            if name == 'svg':
                in_svg = max(0, in_svg - 1)
            for idx in range(len(stack) - 1, -1, -1):
                if stack[idx][0] == name:
                    del stack[idx:]
                    break
            continue
        name = m.group(7).lower()
        attrs = m.group(8)
        selfclose = m.group(9)
        if name == 'svg':
            in_svg += 1
            if not selfclose:
                stack.append((name, None))
            continue
        if in_svg:
            if not selfclose and name not in VOID:
                stack.append((name, None))
            continue
        sm = STYLE_ATTR.search(attrs)
        mydir = own_direction(split_decls(sm.group(2))) if sm else None
        im = re.search(r'\sid="([^"]+)"', attrs)
        if im:
            dirs[im.group(1)] = (mydir, stack[-1][1] if stack else None)
        if not selfclose and name not in VOID:
            stack.append((name, mydir))
    return dirs


SVGISH = re.compile(r'<(svg|symbol)\b([^>]*)>(.*?)</\1\s*>', re.S)


def mirror_svgs(html):
    def one(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        ds = re.findall(r'\bd="([^"]*)"', inner)
        vb = re.search(r'viewBox="\s*([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)\s*"', attrs)
        if not any(d.strip() in DIRECTIONAL_D for d in ds) or not vb:
            # a sprite sheet: the arrows live in <symbol>s that carry their own
            # viewBox, so step inside instead of giving up on the wrapper
            if '<symbol' in inner or '<svg' in inner:
                return '<%s%s>%s</%s>' % (tag, attrs, mirror_svgs(inner), tag)
            return m.group(0)
        x0, W = float(vb.group(1)), float(vb.group(3))
        span = 2 * x0 + W

        def fixd(dm):
            return 'd="' + mirror_path_d(dm.group(1), span) + '"'
        inner = re.sub(r'\bd="([^"]*)"', fixd, inner)

        def fixrect(rm):
            body = rm.group(1)
            xm = re.search(r'\bx="(' + NUM + r')"', body)
            wm = re.search(r'\bwidth="(' + NUM + r')"', body)
            if xm and wm:
                nx = span - float(xm.group(1)) - float(wm.group(1))
                body = body[:xm.start(1)] + _fmt(nx) + body[xm.end(1):]
            return '<rect' + body + '>'
        inner = re.sub(r'<rect([^>]*)>', fixrect, inner)
        inner = re.sub(r'\bcx="(' + NUM + r')"',
                       lambda c: 'cx="%s"' % _fmt(span - float(c.group(1))), inner)
        for a in ('x1', 'x2'):
            inner = re.sub(r'\b%s="(%s)"' % (a, NUM),
                           lambda c, a=a: '%s="%s"' % (a, _fmt(span - float(c.group(1)))), inner)
        return '<%s%s>%s</%s>' % (tag, attrs, inner, tag)
    return SVGISH.sub(one, html)
