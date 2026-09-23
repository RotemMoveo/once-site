# -*- coding: utf-8 -*-
"""
_hero-mobile/build.py — מייצר את קובצי ההשוואה של פתרונות ראש-העמוד במובייל.

    python3 _hero-mobile/build.py        # מתוך תיקיית האתר
    ואז לפתוח את _hero-mobile/compare.html

הבעיה: בעמודים שנפתחים בכותרת ולא בתמונה (projects, news — וגם accessibility,
privacy, spec, search) הקצב האנכי של לוח ה-1440 ממשיך לחול גם ב-375px. התוצאה
היא קיפול ראשון של ~480px לובן ובתוכו שלוש שורות טקסט, לפני שנראה תוכן אחד.

כל וריאנט כאן הוא *טלאי*: גיליון ‎@media (max-width:768px)‎ ולפעמים כמה שורות JS,
שמוזרקים לעותק של העמוד המקורי. כלומר מה שייבחר עובר כמעט כמו שהוא אל העמוד
עצמו (או אל css/chrome.css אם הוא גנרי), ואין כאן עמוד מקביל לתחזק.

הדסקטופ אינו נוגע: כל כלל יושב מתחת ל-768px, בעוד שכללי ה-1439 של העמוד
ממשיכים לשלוט מעליו.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent

# כוכב ONCE. מרכאות כפולות בלבד — ה-SVG נדחף לתוך מחרוזת JS במרכאות יחידות.
STAR = ('<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">'
        '<path d="M48 23.7922L31.5809 25.4544C28.3738 25.774 25.8486 28.3418 25.5822 31.5596L24.2078 48L22.5456 '
        '31.5809C22.2153 28.3738 19.6582 25.8486 16.4404 25.5822L0 24.2078L16.4191 22.5456C19.6262 22.226 22.1407 '
        '19.6582 22.4178 16.4404L23.7922 0L25.4544 16.4191C25.7847 19.6262 28.3418 22.1514 31.5596 22.4178L48 '
        '23.7922Z" fill="{c}"/><path d="M33.905 33.7305L26.4999 27.6893C25.0508 26.5066 22.9731 26.5278 21.556 '
        '27.7318L14.2681 33.9011L20.3094 26.5065C21.4921 25.0575 21.4708 22.9798 20.2668 21.552L14.0977 '
        '14.2642L21.4921 20.3055C22.9412 21.4882 25.0189 21.4668 26.4466 20.2628L33.7345 14.0938L27.6932 '
        '21.4881C26.5105 22.9372 26.5318 25.0148 27.7358 26.4426L33.905 33.7305Z" fill="{c}"/></svg>')

# ---------------------------------------------------------------------- עמודים
PAGES = {
    'projects': dict(
        file='projects.html', title='הפרויקטים שלנו',
        root='#n1', head='#n3', headin='#n4', startitle='#n5', star='#n6', h1='#n7',
        bar='#n9',        # סרגל הסינון
        below='#n30',     # גריד הפרויקטים
        lead='#n33',      # הכרטיס הראשון — הרא״ז 13
        leadimg='#n34',
        align='end',
        band='images/3465d5c6c01d7b36.jpg',
        cap='שישה פרויקטים ברחובות',
    ),
    'news': dict(
        file='news.html', title='חדשות ועדכונים',
        root='#n326', head='#n328', headin='#n329', startitle='#n330', star='#n331', h1='#n332',
        bar='#n334',      # שורת החיפוש
        below='#n349',    # רשת הכתבות
        lead='#n338',     # הכתבה הראשית
        leadimg='#n340',
        align='center',
        band='images/28323d6fc880a2ba.jpg',
        cap='מהשטח, מהפרויקטים ומהחברה',
    ),
}

M = '@media (max-width:768px){'


def lead_pad(p, v):
    """רק ב-news הפריט הראשון הוא צומת עליון עם ריפוד משלו; ב-projects הוא
    כרטיס בתוך הגריד ואסור לתת לו ריפוד עליון."""
    return '' if p['file'] != 'news.html' else '  %s{padding-top:%dpx !important}\n' % (p['lead'], v)


# ------------------------------------------------------------------ גיליונות
def css_base(p):
    return M + '.bcr-wrap{padding-top:26px !important}}'


def css_compact(p):
    """1 · כיווץ — אותם אלמנטים בדיוק, קצב אנכי של טלפון."""
    return M + f"""
  {p['head']}{{padding-top:20px !important;padding-bottom:22px !important}}
  {p['startitle']}{{gap:10px !important}}
  {p['star']},{p['star']} svg{{width:28px !important;height:28px !important}}
  {p['bar']}{{padding-top:4px !important}}
  {p['below']}{{padding-top:28px !important}}
{lead_pad(p, 28)}}}"""


def css_rail(p):
    """2 · שורת כותרת — הכוכב עולה לשורת הכותרת, קו שיער סוגר."""
    just = 'center' if p['align'] == 'center' else 'flex-start'
    return css_compact(p) + M + f"""
  {p['startitle']}{{flex-direction:row-reverse !important;align-items:center !important;
                    justify-content:{just} !important;gap:11px !important;width:100% !important}}
  {p['headin']}{{width:100% !important;gap:0 !important}}
  {p['star']},{p['star']} svg{{width:23px !important;height:23px !important}}
  {p['h1']}{{font-size:30px !important;line-height:1.1 !important;letter-spacing:-1.15px !important}}
  {p['head']}{{padding-top:14px !important;padding-bottom:14px !important;
               border-bottom:.5px solid rgba(0,65,108,.25) !important}}
  {p['bar']}{{padding-top:0 !important}}
  {p['below']}{{padding-top:24px !important}}
{lead_pad(p, 24)}}}"""


def css_band(p):
    """3 · רצועת תמונה מקצה לקצה מתחת לשורת הכותרת."""
    return css_rail(p) + M + """
  .hv-band{align-self:stretch !important;flex-shrink:0 !important;position:relative;
           height:31vh !important;min-height:200px !important;max-height:260px !important;
           background-position:center !important;background-size:cover !important;
           background-repeat:no-repeat !important}
  .hv-band .hv-cap{position:absolute;inset-inline-start:20px;bottom:13px;direction:rtl;
                   font:400 13px/18px 'GoogleSans',Arial,sans-serif;color:#fff;
                   text-shadow:0 1px 12px rgba(6,40,64,.65)}
}"""


def css_hero(p):
    """4 · הירו מצולם — שפת ההירו של kablanit / urban-renewal, במובייל בלבד."""
    return M + """
  .nav-gap{display:none !important}
  .hv-hero{align-self:stretch !important;flex-shrink:0 !important;position:relative;
           display:flex !important;flex-direction:column !important;justify-content:flex-end !important;
           height:43vh !important;min-height:300px !important;max-height:380px !important;
           padding:0 20px 26px 20px !important;
           background:linear-gradient(0deg,rgba(6,40,64,.62),rgba(6,40,64,0) 58%),
                      linear-gradient(rgba(0,0,0,.18),rgba(0,0,0,.18)),
                      var(--hv-img) center/cover no-repeat !important}
  .hv-hero .hv-in{display:flex;flex-direction:column;align-items:flex-end;gap:9px;direction:rtl}
  .hv-hero svg{width:26px;height:26px;display:block}
  .hv-hero h1{margin:0;font:400 34px/1.08 'Almoni',Arial,sans-serif;letter-spacing:-1.3px;color:#fff}
  .hv-hero .hv-k{font:400 14px/18px 'GoogleSans',Arial,sans-serif;color:rgba(255,255,255,.85)}
  .bcr-wrap{padding-top:22px !important;padding-bottom:0 !important}
}""" + M + f"""
  {p['bar']}{{padding-top:18px !important}}
  {p['below']}{{padding-top:26px !important}}
{lead_pad(p, 26)}}}"""


def css_lead(p):
    """5 · הפריט הראשון פותח — התמונה בורחת לשולי המסך."""
    if p['file'] == 'news.html':
        extra = """
  #n339{flex-direction:column !important;gap:18px !important;align-items:stretch !important}
  #n341{align-items:flex-end !important}
  #n344{font-size:27px !important;line-height:1.12 !important;letter-spacing:-1px !important}
  #n338{padding-top:0 !important}
  #n334{padding-top:30px !important}
  #n349{padding-top:44px !important}
"""
    else:
        extra = """
  #n33{align-self:stretch !important;width:100% !important;padding-top:0 !important}
  #n35{padding-inline:20px !important}
  #n41{font-size:24px !important;letter-spacing:-.9px !important}
  #n9{padding-top:30px !important}
  #n30{padding-top:26px !important}
"""
    return css_rail(p) + M + f"""
  {p['leadimg']}{{width:100vw !important;max-width:none !important;
                  margin-inline:calc((100% - 100vw)/2) !important;
                  aspect-ratio:375/248 !important;height:auto !important}}
{extra}}}"""


def css_star(p):
    """6 · כוכב ענק — הלובן הופך לשדה מעוצב, בלי תמונה חדשה."""
    return css_compact(p) + M + f"""
  {p['head']}{{position:relative !important;overflow:hidden !important;
               padding-top:32px !important;padding-bottom:32px !important}}
  .hv-star{{position:absolute;top:50%;inset-inline-end:-80px;width:250px;height:250px;
            transform:translateY(-50%);opacity:.075;pointer-events:none;z-index:0;
            display:flex;align-items:center;justify-content:center}}
  .hv-star svg{{width:100%;height:100%}}
  {p['headin']}{{position:relative;z-index:1}}
}}"""


# ------------------------------------------------------------------------- JS
def js_band(p):
    return f"""
    var band = document.createElement('div');
    band.className = 'hv-band';
    band.style.backgroundImage = "url('{p['band']}')";
    band.innerHTML = '<span class="hv-cap">{p['cap']}</span>';
    root.insertBefore(band, head.nextSibling);
"""


def js_hero(p):
    star = STAR.format(c='white')
    return f"""
    var hero = document.createElement('div');
    hero.className = 'hv-hero';
    hero.style.setProperty('--hv-img', "url('{p['band']}')");
    hero.innerHTML = '<div class="hv-in">{star}<h1>{p['title']}</h1>'
                   + '<span class="hv-k">{p['cap']}</span></div>';
    root.insertBefore(hero, root.firstChild);
    head.style.display = 'none';
    var bcr = document.querySelector('.bcr-wrap');
    if (bcr) root.insertBefore(bcr, hero.nextSibling);
    // העמודים האלה מכריזים data-nav="light" ולכן התפריט נצבע לבן מיד; מעל הירו
    // מצולם הוא צריך להתחיל שקוף ולהתמלא בגלילה — בדיוק כמו ב-kablanit.
    var nav = document.querySelector('.nav');
    if (nav) {{
      var on = function () {{
        if (scrollY > 40) nav.classList.add('scrolled');
        else nav.classList.remove('scrolled');
      }};
      on();
      addEventListener('scroll', on, {{ passive: true }});
    }}
"""


def js_lead(p):
    # הפריט הראשון עולה אל מתחת לשורת הכותרת, לפני סרגל הסינון / החיפוש.
    return f"""
    var lead = document.querySelector('{p['lead']}');
    var bar  = document.querySelector('{p['bar']}');
    if (lead && bar) root.insertBefore(lead, bar);
"""


def js_star(p):
    star = STAR.format(c='#003a5e')
    return f"""
    var s = document.createElement('span');
    s.className = 'hv-star';
    s.innerHTML = '{star}';
    head.insertBefore(s, head.firstChild);
"""


VARIANTS = [
    ('v0', 'המצב היום',         'הקצב של לוח 1440 ממשיך לחול ב-375',           None,        None),
    ('v1', 'כיווץ מרווחים',     'אותו עיצוב בדיוק, קצב אנכי של טלפון',          css_compact, None),
    ('v2', 'שורת כותרת',        'הכוכב עולה לשורה, קו שיער סוגר את הראש',       css_rail,    None),
    ('v3', 'רצועת תמונה',       'שורת כותרת ומתחתיה רצועה מקצה לקצה',           css_band,    js_band),
    ('v4', 'הירו מצולם',        'ההירו של קבלנית / התחדשות — במובייל בלבד',     css_hero,    js_hero),
    ('v5', 'הפריט הראשון פותח', 'הפריט הראשון עולה מעל הסרגל ובורח לשוליים',    css_lead,    js_lead),
    ('v6', 'כוכב ענק',          'הלובן הופך לשדה מעוצב, בלי תמונה חדשה',        css_star,    js_star),
]


def build_variant(page_key, vkey, css_fn, js_fn):
    p = PAGES[page_key]
    html = (SITE / p['file']).read_text(encoding='utf-8')

    # הקובץ יושב תיקייה אחת פנימה, וכל הנכסים בעמוד יחסיים לשורש האתר.
    html = html.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../">', 1)

    css = '' if css_fn is None else (css_base(p) + css_fn(p))
    js = '' if js_fn is None else js_fn(p)

    patch = f"""
<style id="hv-patch">{css}</style>
<script>
(function () {{
  function go() {{
    if (innerWidth > 768) return;
    var root = document.querySelector('{p['root']}');
    var head = document.querySelector('{p['head']}');
    if (!root || !head) return;
{js}
  }}
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go);
  else go();
  // הגילוי המדורג לא נורה בתוך iframe נטול-גלילה — פותחים אותו ידנית לתצוגה.
  setTimeout(function () {{
    document.querySelectorAll('.wsplit').forEach(function (e) {{ e.classList.add('in'); }});
  }}, 150);
}})();
</script>
"""
    html = html.replace('</body>', patch + '</body>', 1)
    out = HERE / f'{page_key}-{vkey}.html'
    out.write_text(html, encoding='utf-8')
    return out.name


def main():
    n = 0
    for key in PAGES:
        for vkey, _lab, _sub, css_fn, js_fn in VARIANTS:
            build_variant(key, vkey, css_fn, js_fn)
            n += 1
    print('נכתבו %d קבצים ב-%s' % (n, HERE.name))


if __name__ == '__main__':
    main()
