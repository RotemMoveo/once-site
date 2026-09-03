# -*- coding: utf-8 -*-
"""Build  ONCE site/spec.html  — the technical-specification page.

Layout follows the client's own spec section (asaf-collection.com/eisenberg-4038):
a row of category tabs on a hairline rail, one panel of items at a time, and the
legal line underneath.  Everything is drawn in ONCE's own components: the tab is
`chrome.css`'s `.tab` (bold-width reservation and all), the item ledger is the
one on `project.html` (`#n170` — a 0.5px rule above every 17px/23px line), and
the hero stat pills are `project.html`'s (`#n131`).
"""
import os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))

src = open(os.path.join(SITE, 'accessibility.html'), encoding='utf-8').read()
# NB: the menu drawer holds a <nav class="menu-links"> of its own, so the
# header's closing tag has to be looked for after the header's opening one
top  = src[src.index('<body data-nav="light">'):
           src.index('</nav>', src.index('<nav class="nav">')) + 6]
foot = src[src.index('<footer'):]

PILL = open(os.path.join(HERE, 'pill.svg'), encoding='utf-8').read().strip()
# the eight-point star as a URL-encoded background — one element per item, so a
# wrapped line indents under its own mark instead of starting a new one
STAR_URI = open(os.path.join(HERE, 'star.uri'), encoding='utf-8').read().strip()

CHEV_BACK = ('<svg width="5" height="9" viewBox="0 0 5 9" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
             '<path d="M0.5 0.5L4.5 4.5L0.5 8.5" stroke="#00416C" stroke-linecap="round" stroke-linejoin="round"/></svg>')

ARROW = ('<svg width="16" height="11" viewBox="0 0 16 11" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
         '<g clip-path="url(#sp_arrow)">'
         '<path d="M15.334 5.20703H2.29688" stroke="#00416C" stroke-width="1.22222" stroke-linecap="round" stroke-linejoin="round"/>'
         '<path d="M5.5549 10.3872L0.666016 5.49826L5.5549 0.609375" stroke="#00416C" stroke-width="1.22222" stroke-linecap="round" stroke-linejoin="round"/>'
         '</g><defs><clipPath id="sp_arrow"><rect width="16" height="11" fill="white"/></clipPath></defs></svg>')

# (tab label, short label for the mobile rail, items)
# Two labels are deliberately trimmed — 'ריצופים ואביזרים סניטריים' and
# 'תוכנית חשמל עשירה' fall to a third line in the display face and swell the rail.
SECTIONS = [
 ("הבניין", "הבניין", [
   "עיצוב בניין חדשני",
   "חללי עבודה משותפים",
   "חדרי ישיבות מעוצבים",
   "מטבחון ושירותים בלובי הראשי",
   "לאונג׳ יוקרתי",
   "2 מעליות יוקרתיות ומהירות",
   "מערכת מצלמות אבטחה בקומת הכניסה",
   "חניון תת קרקעי כולל שער ומחסום בכניסה",
   "תאורת גן ותאורה היקפית",
   "לובי ראשי וקומתי: מצלמות וגלאי נפח (תנועה)",
   "שער חשמלי, כולל מחסום כניסה",
   "פטיו מעוצב בין שני הבניינים",
   "פיתוח וגינון בתכנון אדריכלת נוף",
 ]),
 ("ריצופים ואביזרים", "ריצופים", [
   "קולקציה עשירה של אריחים וחיפויים",
   "חיפויי הדירה בגרניט פורצלן במידות 100/100 או 120/60, למעט חללים רטובים ומרפסות",
   "ריצוף מרפסות שמש באריחים דמויי דק במידות משתנות",
   "אינטרפוץ 4 דרך בחללי הרחצה",
   "אמבטיה אקרילית הכוללת אביק מילוי אוטומטי",
   "ברזים מעוצבים בגוונים ייחודיים, כולל שחור, מושחר, פליז ועוד",
   "מכסי אלומיניום למקלחונים ותעלת ניקוז",
   "ארונות אמבטיה עם כיור מובנה ומראה בחדרי הרחצה",
   "אסלות תלויות בעלות מנגנון הדחה נסתר",
   "לחצני הדחה במספר גוונים",
   "חיפויים במגוון מידות ודגמים",
 ]),
 ("מטבח משודרג", "מטבח", [
   "ארונות תחתונים ועליונים כולל בילט-אין גבוה",
   "מגירות בעלות מנגנון טריקה שקטה",
   "מטבח דגם במה במספר גוונים",
 ]),
 ("מיזוג אוויר", "מיזוג", [
   "מיזוג מיני מרכזי Super Quiet בכל הדירות",
   "בפנטהאוז מערכת מיזוג מיני VRF",
   "הנמכות גבס הכוללות דמפרים בחדרים",
 ]),
 ("אלומיניום ונגרות", "אלומיניום", [
   "חלונות ותריסים של חברת קליל או שו״ע",
   "ויטרינות גדולות לחלל המגורים למיקסום החשיפה לנוף ולאור טבעי",
   "תריסים חשמליים בכל הדירה, למעט חדרי רחצה וממ״ד",
   "זכוכית בידודית ליצירת בידוד אקוסטי מרעשי חוץ",
   "דלתות פנים משודרגות פנדור במבחר גוונים",
   "מנגנוני תפוס־פנוי וצוהר אור בחללים רטובים",
 ]),
 ("תוכנית חשמל", "חשמל", [
   "חיבור חשמל דירתי תלת־פאזי",
   "אביזרי חשמל איכותיים מחברת ניסקו או גביס",
   "הכנה למערכת קולנוע ביתי",
   "הכנה לטוחן אשפה",
   "הכנה לתנורי חימום בחללי הרחצה",
   "אינטרקום TV צבעוני במעגל סגור",
   "נקודת חשמל וטלוויזיה במרפסת",
   "שקעים ממוגני מים במקלחת",
   "נקודת מים וגז במרפסת השמש",
 ]),
 ("מרפסת", "מרפסת", [
   "מרפסת שמש מרווחת הכוללת מעקה מסגרות",
   "טעינה חשמלית לרכבים חשמליים",
   "שקעים להטענה עבור אופניים חשמליים",
 ]),
 ("מרתף חניה", "חניה", [
   "גלאי נפח בחדרי מדרגות ובחניונים",
   "קודן בדלתות כניסה לבניין",
 ]),
]

PILLS = ["3-4, דירת גן, פנטהאוז", "72 יחידות דיור", "פרויקט בשיווק וביצוע"]

H = {
 'title'   : 'ONCE | מפרט טכני — אייזנברג 38-40',
 'desc'    : 'עיקרי המפרט הטכני של פרויקט אייזנברג 38-40 ברחובות — הבניין, הדירה וכל מה שביניהם.',
 'back'    : 'אייזנברג 38-40',
 'h1'      : 'מפרט טכני',
 'tabsnav' : 'קטגוריות המפרט',
 'legal'   : 'התכנית והפרטים באתר/דף/עמוד זה הינם לצורך המחשה והדמיה בלבד וכפופים לשינויים, לרבות על פי היתרי בנייה והנחיות גורמי התכנון. המפרטים ותוכניות המכר שיצורפו להסכם המכר הם בלבד יחייבו את החברה.',
 'ctah'    : 'רוצים את המפרט המלא?',
 'ctap'    : 'נשמח לשלוח לכם את המפרט הטכני המלא ואת תוכניות הדירות, או לתאם פגישה במשרדי המכירות.',
 'ctabtn'  : 'ליצירת קשר',
 'phone'   : 'טלפון',
 'mail'    : 'דוא״ל',
 'addr'    : 'כתובת',
 'addrv'   : 'יעקב 26, רחובות',
 'skip'    : 'דלגו לתוכן העמוד',
}

CSS = """
/* ============ מפרט טכני =========================================== */
:root{--nav-h:93px;--pad:100px;--sp-tab-off:#86939c;--sp-rule:rgba(0,65,108,.16);--sp-rule-soft:rgba(0,65,108,.10)}
.sp-skip{position:absolute;inset-inline-start:-9999px;top:0;z-index:60;background:#fff;color:var(--marine);padding:12px 20px;font:500 16px/1 'GoogleSans'}
.sp-skip:focus{inset-inline-start:0}
.sp{max-width:1440px;margin-inline:auto;background:#fff}
.sp a:focus-visible,.sp button:focus-visible{outline:2px solid var(--marine);outline-offset:4px}

/* ---- hero ---- */
.sp-hero{padding:calc(var(--nav-h) + 88px) var(--pad) 64px;border-bottom:.5px solid rgba(0,65,108,.25);text-align:center}
.sp-back{display:inline-flex;align-items:center;gap:10px;font:500 16px/1 'GoogleSans';color:var(--marine);margin-bottom:26px}
.sp-back svg{flex:0 0 auto;transition:transform .3s ease}
.sp-back:hover svg{transform:translateX(4px)}
.sp-hero h1{font:400 80px/80px 'Almoni',sans-serif;letter-spacing:-3px;color:var(--night-sky)}
/* the stat pills from project.html's hero — text, then the ONCE glyph */
.sp-pills{display:flex;flex-wrap:wrap;justify-content:center;gap:20px;margin-top:34px}
.sp-pill{display:flex;align-items:center;gap:16px;padding:6px 10px;font:400 16px/1.4 'GoogleSans';color:var(--marine)}
.sp-pill svg{flex:0 0 auto;color:var(--marine)}

/* ---- the tabbed specification ---- */
.sp-spec{padding:80px var(--pad) var(--pad)}
.sp-rail{position:relative;border-bottom:.5px solid rgba(0,65,108,.25)}
/* eight equal columns rather than a scrolling row: the two long labels wrap onto
   a second line instead of pushing the last tab off the rail, and the bar under
   the picked tab is then a whole column wide */
.sp-tabs{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:0 16px;align-items:start}
.sp-tabs::-webkit-scrollbar{display:none}
/* Almoni, the face every heading on the site is set in — so a tab and an item
   differ by KIND of type, not by a step of weight. Nothing bolds when a tab is
   picked, so the label cannot re-wrap and needs no width reservation.
   --sp-tab-off is the lightest grey that still clears 3:1 on white at this size. */
.sp-tab{padding:0 0 18px;font:400 26px/30px 'Almoni',sans-serif;letter-spacing:-.6px;color:var(--sp-tab-off);cursor:pointer;background:none;border:0;text-align:center;transition:color .25s ease}
.sp-tab .tlab{display:flex;flex-direction:column;align-items:center}
.sp-tab .tshort{display:none}
.sp-tab:hover{color:var(--marine)}
.sp-tab[aria-selected="true"]{color:var(--night-sky)}
/* one bar that slides between tabs, rather than a border that blinks on and off */
.sp-ink{position:absolute;bottom:-.5px;height:2px;background:var(--night-sky);inset-inline-start:0;width:0;transform:translateX(0);transition:width .42s cubic-bezier(.22,.61,.36,1),transform .42s cubic-bezier(.22,.61,.36,1)}

.sp-panels{padding-top:64px;transition:height .42s cubic-bezier(.22,.61,.36,1)}
.sp-panels.moving{overflow:hidden}
.sp-panel[hidden]{display:none}
/* the item ledger from project.html: a hairline above every line, 17px/23px */
.sp-panel{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:56px;row-gap:24px;border-top:.5px solid var(--sp-rule);padding-top:24px}
/* The star heads each line and the rule drops to a whisper behind it. Without a
   mark, an item that wraps reads as two items — its second line sits 27px under
   the first, barely less than the 40px to the next item. The mark settles that:
   the wrap indents past it, a new item starts at it. */
.sp-panel li{list-style:none;padding-bottom:24px;padding-inline-start:26px;border-bottom:.5px solid var(--sp-rule-soft);font:400 16px/27px 'GoogleSans';color:var(--marine);background:url("data:image/svg+xml,%%STAR%%") no-repeat;background-position:right 0 top 8px;background-size:11px 11px}
/* …arriving line by line when the panel is switched */
.sp-panel.in li{animation:spIn .5s cubic-bezier(.22,.61,.36,1) both;animation-delay:var(--d,0ms)}
@keyframes spIn{from{opacity:0;transform:translateY(12px);filter:blur(3px)}to{opacity:1;transform:none;filter:none}}
.sp-legal{margin-top:44px;max-width:840px;font:400 13px/22px 'GoogleSans';color:var(--gray-txt)}

/* ---- closing contact band ---- */
.sp-cta{padding:var(--pad);border-top:.5px solid rgba(0,65,108,.25)}
.sp-cta-in{display:flex;justify-content:space-between;align-items:flex-end;gap:56px}
.sp-cta-txt{display:flex;flex-direction:column;align-items:flex-start;gap:36px}
.sp-cta-txt h2{font:400 48px/48px 'Almoni',sans-serif;letter-spacing:-2px;color:var(--night-sky)}
.sp-cta-txt p{max-width:530px;font:400 17px/30px 'GoogleSans';color:var(--marine)}
.sp-info{display:flex;flex-direction:column;gap:22px}
.sp-info>div{display:flex;flex-direction:column;gap:6px}
.sp-info dt{font:400 12px/17px 'GoogleSans';color:var(--gray-txt)}
.sp-info dd{font:400 20px/26px 'GoogleSans';color:var(--night-sky)}
.sp-info a:hover{text-decoration:underline}

@media (max-width:1280px){
  :root{--pad:72px}
  .sp-hero h1{font-size:64px;line-height:64px;letter-spacing:-2.4px}
  .sp-panel{column-gap:40px}
}
@media (max-width:1024px){
  .sp-panel{grid-template-columns:repeat(2,minmax(0,1fr))}
  .sp-spec{padding-top:64px}
}
@media (max-width:768px){
  :root{--nav-h:64px;--pad:24px}
  .sp-hero{padding-top:calc(var(--nav-h) + 56px);padding-bottom:40px}
  .sp-hero h1{font-size:38px;line-height:1.05;letter-spacing:-1.43px}
  .sp-pills{gap:8px 12px;margin-top:26px}
  .sp-pill{gap:10px;padding:4px 0;font-size:14px}
  .sp-pill svg{width:13px;height:13px}
  .sp-spec{padding:48px 24px 56px}
  /* the rail scrolls sideways on a phone, like .tabs in chrome.css */
  .sp-tabs{display:flex;gap:22px;overflow-x:auto;scrollbar-width:none;-ms-overflow-style:none}
  .sp-tab{flex:0 0 auto;font-size:21px;line-height:26px;padding-bottom:14px;white-space:nowrap}
  .sp-tab .tfull{display:none}
  .sp-tab .tshort{display:inline}
  .sp-panels{padding-top:40px}
  .sp-panel{grid-template-columns:minmax(0,1fr);row-gap:18px;padding-top:18px}
  .sp-panel li{padding-bottom:18px;padding-inline-start:24px;line-height:26px;background-size:10px 10px;background-position:right 0 top 8px}
  .sp-legal{margin-top:32px;font-size:12px;line-height:21px}
  .sp-cta{padding:56px 24px}
  .sp-cta-txt h2{font-size:30px;line-height:1.15;letter-spacing:-1.25px}
  .sp-cta-in{flex-direction:column;align-items:flex-start;gap:40px}
  .sp-cta-txt{gap:28px}
  .sp-cta-txt p{font-size:16px;line-height:27px}
}
@media (prefers-reduced-motion:reduce){
  .sp-back svg,.sp-ink{transition:none}
  .sp-panel.in li{animation:none}
}
"""


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


tabs, panels = [], []
for i, (label, short, items) in enumerate(SECTIONS):
    pid = 'sp-p%d' % (i + 1)
    tabs.append(
        '<button class="sp-tab" type="button" role="tab" id="sp-t%d" aria-controls="%s" '
        'aria-selected="%s" tabindex="%s">'
        '<span class="tlab">'
        '<span class="tfull">%s</span><span class="tshort">%s</span></span></button>'
        % (i + 1, pid, 'true' if i == 0 else 'false', '0' if i == 0 else '-1',
           esc(label), esc(short)))
    lis = ''.join('<li style="--d:%dms">%s</li>' % (28 * k, esc(x)) for k, x in enumerate(items))
    panels.append('<ul class="sp-panel%s" id="%s" role="tabpanel" aria-labelledby="sp-t%d"%s>%s</ul>'
                  % (' in' if i == 0 else '', pid, i + 1, '' if i == 0 else ' hidden', lis))

pills = ''.join('<span class="sp-pill">%s%s</span>' % (esc(p), PILL) for p in PILLS)

body = """<div class="sp">
<section class="sp-hero">
  <a class="sp-back" href="project.html">%(chev)s<span>%(back)s</span></a>
  <h1 data-rv>%(h1)s</h1>
  <div class="sp-pills">%(pills)s</div>
</section>

<section class="sp-spec" id="sp-main" tabindex="-1">
  <div class="sp-rail">
    <div class="sp-tabs" role="tablist" aria-label="%(tabsnav)s">%(tabs)s</div>
    <span class="sp-ink" aria-hidden="true"></span>
  </div>
  <div class="sp-panels">%(panels)s</div>
  <p class="sp-legal">%(legal)s</p>
</section>

<section class="sp-cta">
  <div class="sp-cta-in">
    <div class="sp-cta-txt">
      <div style="display:flex;flex-direction:column;gap:20px;align-items:flex-start">
        <h2 data-rv>%(ctah)s</h2>
        <p>%(ctap)s</p>
      </div>
      <a class="btn" href="contact.html">%(arrow)s<span>%(ctabtn)s</span></a>
    </div>
    <dl class="sp-info">
      <div><dt>%(phone)s</dt><dd><a href="tel:*9240" dir="ltr">*9240</a></dd></div>
      <div><dt>%(mail)s</dt><dd><a href="mailto:info@once-estate.com">info@once-estate.com</a></dd></div>
      <div><dt>%(addr)s</dt><dd>%(addrv)s</dd></div>
    </dl>
  </div>
</section>
</div>""" % dict(H, chev=CHEV_BACK, arrow=ARROW, pills=pills,
                 tabs=''.join(tabs), panels=''.join(panels))

JS = """
/* the specification tabs: one panel at a time, the bar slides to the tab that
   was picked, and the lines of the new panel arrive one after another */
(function () {
  var rail = document.querySelector('.sp-rail');
  if (!rail) return;
  var strip = rail.querySelector('.sp-tabs');
  var ink = rail.querySelector('.sp-ink');
  var tabs = [].slice.call(rail.querySelectorAll('.sp-tab'));
  var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });
  var cur = 0;

  // The bar is anchored with inset-inline-start, so its offset is measured from
  // the rail's own start edge — right in Hebrew, left in English — and pushed
  // inward. Reading both rects keeps it right while the strip scrolls sideways.
  function moveInk(animate) {
    var rtl = getComputedStyle(rail).direction === 'rtl';
    var rr = rail.getBoundingClientRect();
    var tr = tabs[cur].getBoundingClientRect();
    var x = rtl ? rr.right - tr.right : tr.left - rr.left;
    if (!animate) ink.style.transition = 'none';
    ink.style.width = tr.width + 'px';
    ink.style.transform = 'translateX(' + (rtl ? -x : x) + 'px)';
    if (!animate) { void ink.offsetWidth; ink.style.transition = ''; }
  }

  // A short panel following a tall one would otherwise snap the page up by a few
  // hundred pixels; the box is tweened from the old height to the new one.
  var box = document.querySelector('.sp-panels');
  var done = null;
  function tween(from) {
    if (done) { clearTimeout(done); box.classList.remove('moving'); }
    var to = box.scrollHeight;
    if (from === to) return;
    box.classList.add('moving');
    box.style.height = from + 'px';
    void box.offsetWidth;
    box.style.height = to + 'px';
    done = setTimeout(function () {
      box.style.height = '';
      box.classList.remove('moving');
      done = null;
    }, 460);
  }

  function select(i, focus) {
    if (i === cur) return;
    var from = box.offsetHeight;
    tabs[cur].setAttribute('aria-selected', 'false');
    tabs[cur].tabIndex = -1;
    panels[cur].hidden = true;
    panels[cur].classList.remove('in');
    cur = i;
    tabs[i].setAttribute('aria-selected', 'true');
    tabs[i].tabIndex = 0;
    panels[i].hidden = false;
    // restart the line-by-line reveal
    void panels[i].offsetWidth;
    panels[i].classList.add('in');
    tween(from);
    moveInk(true);
    tabs[i].scrollIntoView({ block: 'nearest', inline: 'nearest' });
    if (focus) tabs[i].focus();
  }

  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(i); });
  });
  strip.addEventListener('keydown', function (e) {
    var d = e.key === 'ArrowRight' ? -1 : e.key === 'ArrowLeft' ? 1 : 0;   // RTL rail
    if (document.dir === 'ltr') d = -d;
    if (e.key === 'Home') { e.preventDefault(); return select(0, true); }
    if (e.key === 'End') { e.preventDefault(); return select(tabs.length - 1, true); }
    if (!d) return;
    e.preventDefault();
    select((cur + d + tabs.length) % tabs.length, true);
  });
  strip.addEventListener('scroll', function () { moveInk(false); }, { passive: true });
  addEventListener('resize', function () { box.style.height = ''; moveInk(false); });
  // web fonts land after this runs and change every tab's width
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { moveInk(false); });
  moveInk(false);
})();
"""

head = ('<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">'
        '<meta http-equiv="Cache-Control" content="no-cache, must-revalidate">'
        '<title>%s</title><meta name="description" content="%s">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<link rel="stylesheet" href="css/site.css?v=17">'
        '<link rel="stylesheet" href="css/chrome.css?v=22">'
        '<style>%s</style></head>' % (H['title'], H['desc'], CSS.replace('%%STAR%%', STAR_URI)))

out = (head + top.replace('<body data-nav="light">',
       '<body data-nav="light">\n<a class="sp-skip" href="#sp-main">%s</a>' % H['skip'])
       + body + foot.replace('</body></html>', '<script>%s</script></body></html>' % JS))

open(os.path.join(SITE, 'spec.html'), 'w', encoding='utf-8').write(out)
print('wrote spec.html  %d chars  |  %d tabs, %d items'
      % (len(out), len(SECTIONS), sum(len(x[2]) for x in SECTIONS)))
