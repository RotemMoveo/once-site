(function () {
  var nav = document.querySelector('.nav');
  if (nav) {
    var light = document.body.getAttribute('data-nav') === 'light';
    var onScroll = function () {
      if (light || window.scrollY > 40) nav.classList.add('scrolled');
      else nav.classList.remove('scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }
  var overlay = document.querySelector('.menu-overlay');
  var menu = document.querySelector('.menu');
  var burger = document.querySelector('.burger');
  var closeBtn = document.querySelector('.menu-close');
  function open()  { if (overlay) overlay.classList.add('open'); if (menu) menu.classList.add('open'); }
  function close() { if (overlay) overlay.classList.remove('open'); if (menu) menu.classList.remove('open'); }
  if (burger) burger.addEventListener('click', open);
  if (closeBtn) closeBtn.addEventListener('click', close);
  if (overlay) overlay.addEventListener('click', close);
})();

// ---------- clickable cards + working tabs ----------
(function () {
  var page = location.pathname.split('/').pop() || 'index.html';

  function clickable(sel, href) {
    document.querySelectorAll(sel).forEach(function (el) {
      el.style.cursor = 'pointer';
      el.addEventListener('click', function (e) {
        if (e.target.closest('a')) return;
        location.href = href;
      });
    });
  }

  clickable('[data-name^="כרטיס כתבה"]', 'article.html');
  clickable('[data-name^="כרטיס — "]', 'project.html');
  // the same card, drawn by the same export, on project.html and urban-renewal:
  // it was the only project card on the site that was not clickable.
  clickable('[data-name="project card"]', 'project.html');
  clickable('.pcard', 'project.html');
  clickable('.ncard', 'article.html');

  if (page !== 'projects.html') return;

  // --- reassign some statuses so filtering has real content ---
  var overrides = { 'הרא״ז 13': 'Occupied', 'ברוק 5, תל אביב': 'Occupied', 'האימהות 7-9': 'In permitting' };
  var cards = [].slice.call(document.querySelectorAll('[data-name^="כרטיס — "]'));
  cards.forEach(function (card) {
    var name = card.getAttribute('data-name').replace('כרטיס — ', '');
    var tagEl = [].slice.call(card.querySelectorAll('div,a')).find(function (e) {
      return !e.children.length && e.textContent.trim() === 'In marketing & construction';
    });
    var status = 'In marketing & construction';
    if (overrides[name]) { status = overrides[name]; if (tagEl) tagEl.textContent = status; }
    card.setAttribute('data-status', status);
  });

  // --- order: marketing & construction first, then permitting, then occupied ---
  // That is the order the "all" view has to read in. Each filtered view holds a
  // single status, so it keeps the order the cards already had inside its group
  // (Array#sort is stable).
  var ORDER = ['In marketing & construction', 'In permitting', 'Occupied'];
  function rank(c) {
    var i = ORDER.indexOf(c.getAttribute('data-status'));
    return i === -1 ? ORDER.length : i;
  }
  var ordered = cards.slice().sort(function (a, b) { return rank(a) - rank(b); });

  // --- reflow rows into one wrapping grid so filtering collapses gaps ---
  var firstRow = cards.length ? cards[0].parentElement : null;
  if (firstRow) {
    var gridParent = firstRow.parentElement;
    var wrap = document.createElement('div');
    wrap.style.cssText = 'display:flex;flex-wrap:wrap;justify-content:flex-start;gap:80px 40px;width:1188px;max-width:100%;flex-shrink:0';
    // a plain row: the English page reads left-to-right, so DOM order is already
    // reading order and a leftover odd card stays on the left, where it belongs.
    wrap.className = 'cards-grid';
    gridParent.insertBefore(wrap, firstRow);
    ordered.forEach(function (c) { wrap.appendChild(c); });
    [].slice.call(gridParent.children).forEach(function (ch) {
      if (ch !== wrap && ch.getAttribute('data-name') && ch.getAttribute('data-name').indexOf('שורה') === 0) ch.remove();
    });
  }

  // --- tabs ---
  var tabs = [].slice.call(document.querySelectorAll('[data-name="active tab"],[data-name="non-active tab"]'));
  // המונה של הרשימה המקופלת (.mfx-c) נוסף לתוך הטאב עצמו, ולכן הוא חייב
  // לרדת מכאן — אחרת התווית של "הכל" הופכת ל"הכל6" ואף טאב אינו מזוהה.
  function labelOf(t) {
    var c = t.cloneNode(true), n = c.querySelector('.mfx-c');
    if (n) n.remove();
    return c.textContent.trim();
  }
  function applyFilter(label) {
    cards.forEach(function (c) {
      var st = c.getAttribute('data-status');
      var show = label === 'All' || label.indexOf(st) !== -1;
      c.style.display = show ? '' : 'none';
    });
    tabs.forEach(function (t) {
      var on = labelOf(t) === label;
      t.classList.toggle('tab-on', on);
      [].slice.call(t.querySelectorAll('div,a')).forEach(function (e) {
        // ‎!children.length לבדו החמיץ בדיוק את שלוש הקטגוריות: התווית שלהן
        // עוטפת את "פרויקטים " ב-span.mw (שמוסתר במובייל), ולכן הצבע והמשקל
        // של הטאב הפעיל מעולם לא הוחלפו שם — רק "הכל" הגיב. הקו התחתון
        // הסתיר את זה בדסקטופ; ברשימה המקופלת אין קו, ולכן זה נדרש.
        var only = [].slice.call(e.children).every(function (k) {
          return k.classList.contains('mw') || k.classList.contains('tab-pre');
        });
        if (only && e.textContent.trim()) {
          e.style.color = on ? '#003A5E' : '#777777';
          e.style.fontWeight = on ? '700' : '400';
        }
      });
    });
  }
  // --- מונה לכל קטגוריה, לרשימה המקופלת של המובייל (.mfx) ---
  // נמדד דרך applyFilter עצמו ולא בחישוב מקביל, כדי שהמספר יהיה תמיד בדיוק
  // מה שהסינון יראה. רץ לפני שהמאזינים מחוברים, וה-applyFilter האחרון מנקה
  // אחריו את מצב הטאבים.
  tabs.forEach(function (t) {
    applyFilter(labelOf(t));
    var n = document.createElement('span');
    n.className = 'mfx-c';
    n.textContent = cards.filter(function (c) { return c.style.display !== 'none'; }).length;
    t.appendChild(n);
  });
  // ל"הכל" אין אייקון סטטוס. ברשימה המקופלת כל שורה מסתיימת באייקון בקצה,
  // ובלעדיו השורה הזו לבדה נצמדת לקצה הפנים — עיגול ריק שומר על אותו טור.
  // ה-CSS של העמוד מסתיר אותו מעל 768px.
  tabs.forEach(function (t) {
    if (t.querySelector('svg')) return;
    var ns = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', '0 0 14 14');
    svg.setAttribute('class', 'mfx-dot');
    svg.setAttribute('aria-hidden', 'true');
    var ci = document.createElementNS(ns, 'circle');
    ci.setAttribute('cx', '7'); ci.setAttribute('cy', '7'); ci.setAttribute('r', '6.1');
    ci.setAttribute('fill', 'none');
    ci.setAttribute('stroke', 'currentColor');
    ci.setAttribute('stroke-width', '1.3');
    svg.appendChild(ci);
    t.appendChild(svg);
  });

  // --- בחירת קטגוריה מביאה את הפרויקטים שלה אל מול העין ---
  // הסינון לבדו מחליף תוכן שיושב הרחק מעל לנקודת המבט: מי שבחר קטגוריה
  // אחרי גלילה נשאר מול שארית הרשת הקודמת או מול הפוטר, ולא רואה אף כרטיס
  // מהקבוצה שביקש. הגלילה מצמידה את סרגל הסינון אל מתחת לניווט הקבוע,
  // כך שהטאב שנבחר נשאר גלוי והכרטיסים מתחילים מיד מתחתיו.
  // העוגן הוא ראש הסרגל ולא ראש הרשת, ולכן הוא אינו זז כשהרשימה המקופלת
  // של המובייל נסגרת אחרי הבחירה (chrome.js, בלוק ‎.mfx).
  var bar = document.querySelector('[data-name="סרגל סינון"]');
  var still = window.matchMedia('(prefers-reduced-motion:reduce)');
  function bringIntoView() {
    if (!bar) return;
    var navEl = document.querySelector('.nav');
    var y = bar.getBoundingClientRect().top + window.pageYOffset -
            (navEl ? navEl.getBoundingClientRect().height : 0);
    window.scrollTo({ top: Math.max(0, y), behavior: still.matches ? 'auto' : 'smooth' });
  }

  tabs.forEach(function (t) {
    t.style.cursor = 'pointer';
    t.addEventListener('click', function () { applyFilter(labelOf(t)); bringIntoView(); });
  });
  applyFilter('All');
})();

// ---------- artboard sizing (no scaling) ----------
// היה כאן transform:scale(clientWidth/1440) על ‎.fig-page. הוא הוסר: הקטנה
// פרופורציונלית הקטינה גם את הטיפוגרפיה (16px ירדו ל-9px ב-800px) והגדילה
// אותה מעל 1440, ומכיוון שהניווט והפוטר יושבים מחוץ ל-‎.fig-page הם נשארו
// ב-1:1 ויצרו פער גדלים בולט. במקום זאת: עד 1439px חלים כללי המובייל
// (‎@media max-width:1439px), ומ-1440 ומעלה הלוח נשאר בגודלו — גדל עד 1660
// דרך המרווחים בלבד, ומעבר לכך רק השוליים גדלים. ראו css/chrome.css.
(function () {
  var pg = document.querySelector('.fig-page');
  if (!pg) return;
  pg.style.transform = '';
  pg.style.transformOrigin = '';
})();

// ---------- hover: tag the Figma-exported buttons and links ----------
// The export draws every button and every chevron link the same way — a flex
// wrapper holding [icon, <a>] — but gives them no class and an inline style
// that beats any rule coming from chrome.css.  So none of the .btn / .plink
// hover rules ever reached them: the same button reacted on the home page and
// sat dead on every inner page.  Tag them once here; chrome.css does the rest.
//
// Guards, each for a real false positive on this site:
//   * font-size <= 22px  — the page H1s are <a> too (contact / kablanit /
//     accessibility / privacy), one of them even next to the ✦ star.
//   * an icon sibling    — a bare <a> in a paragraph is not a button.
//   * [data-name="tag"]  — the status pill is also "icon + text in a padded,
//     coloured box", and it is not interactive.
(function () {
  function isBoxed(el) {
    var st = el.getAttribute('style') || '';
    return /padding:/.test(st) && /(border:|background-color:)/.test(st);
  }
  function light(el, a) {
    var st = el.getAttribute('style') || '';
    return /border:[^;]*rgb\(255,\s*255,\s*255\)/.test(st) ||
           /color:\s*rgb\(255,\s*255,\s*255\)/.test(a.getAttribute('style') || '');
  }
  function tag(wrap, textEl) {
    if (!wrap || wrap.classList.contains('fx-btn') || wrap.classList.contains('fx-link')) return;
    if (wrap.closest('[data-name="tag"]')) return;
    if (isBoxed(wrap)) {
      wrap.classList.add('fx-btn');
      if (light(wrap, textEl)) wrap.classList.add('fx-btn-light');
    } else {
      wrap.classList.add('fx-link');
    }
  }

  function iconish(el) {
    if (!el || !el.querySelector || !el.querySelector('svg')) return false;
    var r = el.getBoundingClientRect();            // an icon, not a column that
    return r.width <= 40 && r.height <= 40;        // merely contains svgs
  }

  document.querySelectorAll('.fig-page a[href]').forEach(function (a) {
    if (parseFloat(getComputedStyle(a).fontSize) > 22) return;
    // (a) the export's usual shape: a wrapper holding [icon, <a>]
    var wrap = a.parentElement;
    if (wrap && wrap.children.length === 2) {
      var icon = wrap.firstElementChild === a ? wrap.lastElementChild : wrap.firstElementChild;
      if (iconish(icon)) { tag(wrap, a); return; }
    }
    // (b) sometimes the <a> IS the wrapper and holds [icon, text] itself
    if (a.children.length === 2 && (iconish(a.firstElementChild) || iconish(a.lastElementChild))) {
      tag(a, a);
    }
  });

  // the send buttons are the boxes the export left without an <a> inside.
  // Structural, not by name: a padded box WITH A BORDER holding [icon, label].
  // The status pill is padded too but has no border, so it stays out.
  document.querySelectorAll('.fig-page [style*="border:"]').forEach(function (w) {
    if (w.children.length !== 2 || w.querySelector('a[href]')) return;
    if (!/padding:/.test(w.getAttribute('style') || '')) return;
    if ((w.textContent || '').trim().length > 40) return;
    var a = w.firstElementChild, b = w.lastElementChild;
    var icon = iconish(a) ? a : (iconish(b) ? b : null);
    if (!icon) return;
    tag(w, icon === a ? b : a);
  });
})();

// ---------- lobby: fill active tab icon + normalize icon sizes ----------
(function () {
  if ((location.pathname.split('/').pop() || '') !== 'projects.html') return;
  var tabs = [].slice.call(document.querySelectorAll('[data-name="active tab"],[data-name="non-active tab"]'));
  tabs.forEach(function (t) {
    var svg = t.querySelector('svg');
    if (!svg) return;
    var sz = '16';
    svg.setAttribute('width', sz); svg.setAttribute('height', sz);
    svg.style.width = sz + 'px'; svg.style.height = sz + 'px';
    svg.style.flexShrink = '0';
    var wrap = svg.parentElement;
    if (wrap && wrap !== t) { wrap.style.width = sz + 'px'; wrap.style.height = sz + 'px'; wrap.style.flexShrink = '0'; }
  });
  function paintIcons() {
    tabs.forEach(function (t) {
      var label = t.textContent.trim();
      var active = t.__isActive;
      [].slice.call(t.querySelectorAll('svg path, svg circle, svg rect, svg g')).forEach(function (p) {
        if (active) { p.style.fill = '#003A5E'; p.style.stroke = '#003A5E'; }
        else { p.style.fill = 'none'; p.style.stroke = '#777777'; }
      });
    });
  }
  function mark(label) {
    tabs.forEach(function (t) { t.__isActive = t.textContent.trim() === label; });
    paintIcons();
  }
  tabs.forEach(function (t) {
    t.addEventListener('click', function () { mark(t.textContent.trim()); });
  });
  mark('All');
})();

// ---------- project page: apartment tabs + gallery arrows ----------
(function () {
  if ((location.pathname.split('/').pop() || '') !== 'project.html') return;

  // apartment tabs (3/4/5 rooms) — clickable active toggle, no filtering
  var aptTabs = [].slice.call(document.querySelectorAll('div,a')).filter(function (e) {
    var onlySpan = !e.children.length || (e.children.length === 1 && e.children[0].tagName === 'SPAN');
    return onlySpan && /^[345] rooms$/.test(e.textContent.trim().replace(/\s+/g, ' '));
  });
  function setApt(el) {
    aptTabs.forEach(function (t) {
      var on = t === el;
      t.style.color = on ? '#003A5E' : '#777777';
      t.style.fontWeight = on ? '700' : '400';
    });
  }
  aptTabs.forEach(function (t) {
    var box = t.closest('[data-name]') || t;
    box.style.cursor = 'pointer';
    box.addEventListener('click', function () { setApt(t); });
  });
  var active3 = aptTabs.find(function (t) { return t.textContent.trim() === '3 rooms'; });
  if (active3) setApt(active3);

  // --- the pager arrows next to the "N/M" counter ---
  // They came out of the export as decoration: they carry .pgal-arrow, so they
  // had a pointer cursor and an opacity hover, but nothing listened to them —
  // a control that lights up and then does nothing.  And the prev arrow kept a
  // hard-coded inline opacity:.4, so it looked permanently disabled.
  // They page through the apartment tabs, and the counter follows the real
  // number of tabs instead of the artboard's hard-coded "4".
  var next = document.querySelector('.pgal-arrow.pgal-next');
  var prev = document.querySelector('.pgal-arrow.pgal-prev');
  var counter = [].slice.call(document.querySelectorAll('div')).find(function (e) {
    return !e.children.length && /^\d+\s*\/\s*\d+$/.test(e.textContent.trim());
  });
  if (next && prev && aptTabs.length > 1) {
    // reading order, right to left: the export lists the tabs left to right
    aptTabs.sort(function (x, y) {
      return y.getBoundingClientRect().right - x.getBoundingClientRect().right;
    });
    var i = aptTabs.indexOf(active3 || aptTabs[0]);
    if (i < 0) i = 0;
    function paint() {
      setApt(aptTabs[i]);
      if (counter) counter.textContent = (i + 1) + '/' + aptTabs.length;
      // the inline opacity from the export would win over [disabled]
      prev.style.opacity = '';
      next.style.opacity = '';
      prev.toggleAttribute('disabled', i === 0);
      next.toggleAttribute('disabled', i === aptTabs.length - 1);
    }
    next.addEventListener('click', function () { if (i < aptTabs.length - 1) { i++; paint(); } });
    prev.addEventListener('click', function () { if (i > 0) { i--; paint(); } });
    // clicking a tab directly keeps the pager in step
    aptTabs.forEach(function (t, k) {
      var box = t.closest('[data-name]') || t;
      box.addEventListener('click', function () { i = k; paint(); });
    });
    paint();
  }
})();

// ---------- kablanit gallery lightbox ----------
(function () {
  if ((location.pathname.split('/').pop() || '') !== 'kablanit.html') return;
  var tiles = [].slice.call(document.querySelectorAll('[data-name="תמונה"]')).filter(function (el) {
    var bg = getComputedStyle(el).backgroundImage;
    var r = el.getBoundingClientRect();
    return bg && bg.indexOf('url(') !== -1 && r.width > 300 && r.width < 700;
  });
  if (!tiles.length) return;
  var urls = tiles.map(function (el) {
    var m = getComputedStyle(el).backgroundImage.match(/url\(["']?([^"')]+)["']?\)/);
    return m ? m[1] : null;
  }).filter(Boolean);

  var box = document.createElement('div');
  box.style.cssText = 'display:none;position:fixed;inset:0;z-index:999;background:rgba(6,40,64,.94);align-items:center;justify-content:center';
  box.innerHTML =
    '<img style="max-width:84vw;max-height:86vh;object-fit:contain;display:block">' +
    '<button data-lb="close" style="position:absolute;top:28px;right:28px;background:none;border:none;cursor:pointer;padding:8px"><svg width="26" height="26" viewBox="0 0 22 22" fill="none"><path d="M2 2L20 20M20 2L2 20" stroke="white" stroke-width="1.5" stroke-linecap="round"/></svg></button>' +
    '<button data-lb="next" style="position:absolute;right:36px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;padding:12px"><svg width="36" height="36" viewBox="0 0 32 32" fill="none"><path d="M12 6L22 16L12 26" stroke="white" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>' +
    '<button data-lb="prev" style="position:absolute;left:36px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;padding:12px"><svg width="36" height="36" viewBox="0 0 32 32" fill="none"><path d="M20 6L10 16L20 26" stroke="white" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>';
  document.body.appendChild(box);
  var imgEl = box.querySelector('img');
  var cur = 0;
  function show(i) {
    cur = (i + urls.length) % urls.length;
    imgEl.src = urls[cur];
    box.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
  function close() { box.style.display = 'none'; document.body.style.overflow = ''; }
  box.addEventListener('click', function (e) {
    var b = e.target.closest('[data-lb]');
    if (b) {
      var a = b.getAttribute('data-lb');
      if (a === 'close') close();
      if (a === 'next') show(cur + 1);
      if (a === 'prev') show(cur - 1);
    } else if (e.target === box) close();
  });
  document.addEventListener('keydown', function (e) {
    if (box.style.display === 'none') return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowRight') show(cur + 1);
    if (e.key === 'ArrowLeft') show(cur - 1);
  });
  tiles.forEach(function (el, i) {
    el.style.cursor = 'zoom-in';
    el.addEventListener('click', function () { show(i); });
  });
})();

// ---------- image gallery (.pgal): dots + 4s autoplay + finger swipe ----------
// Navigation is dots-only by design — no arrows. (The .pgal-arrow CSS is still
// used by the apartments gallery on project.html, so it stays in chrome.css.)
(function () {
  var gals = [].slice.call(document.querySelectorAll('.pgal'));
  if (!gals.length) return;

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  gals.forEach(function (gal) {
    var track = gal.querySelector('.pgal-track');
    if (!track) return;
    var slides = [].slice.call(track.children);
    var n = slides.length;
    if (!n) return;

    var dots = document.createElement('div');
    dots.className = 'pgal-dots';
    var dotEls = slides.map(function (_, i) {
      var d = document.createElement('button');
      d.className = 'pgal-dot' + (i === 0 ? ' on' : '');
      d.type = 'button';
      d.setAttribute('aria-label', 'Image ' + (i + 1));
      dots.appendChild(d);
      return d;
    });
    gal.appendChild(dots);

    // single image: one inert dot, no autoplay
    if (n < 2) { gal.setAttribute('data-single', '1'); return; }

    var cur = 0, timer = null;
    function go(i) {
      cur = (i + n) % n;
      track.style.transform = 'translateX(' + (-cur * 100) + '%)';
      dotEls.forEach(function (d, k) { d.classList.toggle('on', k === cur); });
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function start() { if (reduce) return; stop(); timer = setInterval(function () { go(cur + 1); }, 4000); }

    dotEls.forEach(function (d, i) {
      d.addEventListener('click', function () { go(i); start(); });  // manual pick restarts the 4s clock
    });

    gal.addEventListener('mouseenter', stop);
    gal.addEventListener('mouseleave', start);

    /* ---- finger swipe (touch): the track follows the finger, snaps on lift ----
       .pgal is touch-action:pan-y, so a vertical drag still scrolls the page;
       we lock to the axis of the first 8px so a scroll never nudges the track. */
    var sx = 0, sy = 0, dx = 0, gw = 0, drag = 0;   /* drag: 0 idle, 1 undecided, 2 swiping */

    gal.addEventListener('touchstart', function (e) {
      if (e.touches.length !== 1) return;
      drag = 1; dx = 0; gw = gal.clientWidth || 1;
      sx = e.touches[0].clientX; sy = e.touches[0].clientY;
    }, { passive: true });

    gal.addEventListener('touchmove', function (e) {
      if (!drag) return;
      var mx = e.touches[0].clientX - sx, my = e.touches[0].clientY - sy;
      if (drag === 1) {
        if (Math.abs(mx) < 8 && Math.abs(my) < 8) return;
        if (Math.abs(my) >= Math.abs(mx)) { drag = 0; return; }   /* the page is scrolling */
        drag = 2; stop(); track.style.transition = 'none';
      }
      dx = mx;
      /* nothing sits past either end — pull back there instead of dragging blank in */
      if ((cur === 0 && dx > 0) || (cur === n - 1 && dx < 0)) dx *= 0.35;
      track.style.transform = 'translateX(' + (-cur * gw + dx) + 'px)';
    }, { passive: true });

    function drop() {
      if (drag !== 2) { drag = 0; return; }
      drag = 0;
      track.style.transition = '';
      var step = Math.max(40, gw * 0.15);
      go(dx <= -step ? cur + 1 : dx >= step ? cur - 1 : cur);
      start();                                    /* a swipe restarts the 4s clock */
    }
    gal.addEventListener('touchend', drop);
    gal.addEventListener('touchcancel', drop);

    go(0);
    start();
  });
})();

/* ---------- nav search panel ---------- */
(function () {
  var nsx = document.getElementById('nsx');
  if (!nsx) return;
  var scrim = document.getElementById('nsx-scrim');
  var field = nsx.querySelector('.nsx-field');
  var input = nsx.querySelector('#nsx-q');
  var nav   = document.querySelector('.nav');

  /* on the results page the panel opens holding the query that is already
     showing, pre-selected, so a second search is one keystroke away */
  var prev = (location.search.match(/[?&]q=([^&]*)/) || [])[1];
  if (prev) {
    try { input.value = decodeURIComponent(prev.replace(/\+/g, ' ')); } catch (e) {}
    field.classList.toggle('has', input.value.trim() !== '');
  }

  function open() {
    var menu = document.querySelector('.menu'), ov = document.querySelector('.menu-overlay');
    if (menu) menu.classList.remove('open');
    if (ov) ov.classList.remove('open');
    nsx.classList.add('open');
    scrim.classList.add('open');
    nsx.setAttribute('aria-hidden', 'false');
    /* the panel is white — a transparent nav over a hero would leave white-on-white icons */
    if (nav) nav.classList.add('scrolled');
    setTimeout(function () { input.focus(); input.select(); }, 80);
  }
  function close() {
    if (!nsx.classList.contains('open')) return;
    nsx.classList.remove('open');
    scrim.classList.remove('open');
    nsx.setAttribute('aria-hidden', 'true');
    /* hand the nav back to its own scroll rule */
    window.dispatchEvent(new Event('scroll'));
  }

  [].slice.call(document.querySelectorAll('.nav-search,.menu-search')).forEach(function (b) {
    b.addEventListener('click', function (e) { e.preventDefault(); open(); });
  });
  nsx.querySelector('.nsx-close').addEventListener('click', close);
  scrim.addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

  input.addEventListener('input', function () {
    field.classList.toggle('has', input.value.trim() !== '');
  });
  nsx.querySelector('.nsx-clear').addEventListener('click', function () {
    input.value = '';
    field.classList.remove('has');
    input.focus();
  });
  [].slice.call(nsx.querySelectorAll('.nsx-chip')).forEach(function (c) {
    c.addEventListener('click', function () {
      location.href = 'search.html?q=' + encodeURIComponent(c.textContent.trim());
    });
  });
})();

/* ---------- entrance reveal: a heading arrives word by word ----------
   The same animation index.html and about.html run inline, moved here so every
   other page gets it too. Targets are marked [data-rv] in the markup rather
   than picked by font size at runtime, because the Figma exports have no
   headings to select — only divs — and the sizes change at the mobile
   breakpoint, which would silently change which lines animate. */
(function () {
  var targets = [].slice.call(document.querySelectorAll('[data-rv]'));
  if (!targets.length) return;

  // Split text into words, leaving <br> and any inline wrapper in place — some
  // of the export's headings break their own line, and .wsplit .w is a
  // descendant selector, so nested words still animate.
  function split(el) {
    var i = 0;
    (function walk(node) {
      [].slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.nodeValue.split(/(\s+)/).forEach(function (tok) {
            if (!tok) return;
            if (/^\s+$/.test(tok)) {
              frag.appendChild(document.createTextNode(tok.indexOf('\n') > -1 ? '\n' : ' '));
              return;
            }
            var sp = document.createElement('span');
            sp.className = 'w';
            sp.textContent = tok;
            sp.style.setProperty('--d', (i * 45) + 'ms');
            i++;
            frag.appendChild(sp);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') {
          // an element with no text of its own — the ONCE wordmark some
          // headings end on — arrives as one more word, in its turn
          if (!n.textContent.trim()) {
            n.classList.add('w');
            n.style.setProperty('--d', (i * 45) + 'ms');
            i++;
          } else {
            walk(n);
          }
        }
      });
    })(el);
    el.classList.add('wsplit');
  }
  targets.forEach(split);

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: .5, rootMargin: '0px 0px -14% 0px' });

  // With threshold .5 and that bottom margin the trigger line sits at 86% of the
  // window height, so a heading already on screen at load would wait for a
  // scroll that may never come — every page here opens on one. Those reveal on
  // load instead; see the same fix on index.html's hero.
  var line = window.innerHeight * .86;
  var onLoad = [];
  targets.forEach(function (el) {
    if (el.getBoundingClientRect().top < line) onLoad.push(el);
    else io.observe(el);
  });

  if (onLoad.length) {
    var reveal = function () { onLoad.forEach(function (el) { el.classList.add('in'); }); };
    // Two frames, so the opacity:0 start state paints before the class flips —
    // flipping it in the same tick would just show the finished state.
    requestAnimationFrame(function () { requestAnimationFrame(reveal); });
    // Frames are suspended in a background tab, so rAF alone could leave the
    // heading invisible. These make sure it always resolves, and still animates
    // the first time the page is actually looked at.
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden) reveal();
    }, { once: true });
    setTimeout(function () { if (!document.hidden) reveal(); }, 1200);
  }
})();

/* ---------- סינון מקופל במובייל (.mfx) ---------- */
/* הרכיב אינו יודע דבר על העמוד שהוא יושב בו: הוא עוטף את סרגל הטאבים הקיים,
   קורא ממנו את הקטגוריה הפעילה אל תוך השורה הסגורה, ונסגר אחרי בחירה. מעל
   768px הוא שקוף לגמרי — הכותרת מוסתרת ב-CSS והפאנל פתוח תמיד, כך שאותו DOM
   משרת גם את הדסקטופ בלי כפילות תוויות. ראו css/chrome.css. */
(function () {
  var mq = window.matchMedia('(max-width:768px)');
  var ROWS = '.tab,.stab,[data-name="active tab"],[data-name="non-active tab"]';
  var ON   = '.tab.active,.stab.on,.tab-on';

  /* התווית הקצרה: data-short הוא מה שהטאב מציג ממילא במסך צר, ואחריו
     data-text. בלעדיהם נלקח הטקסט עצמו בלי הקידומת שמוסתרת במובייל
     (.mw/.tab-pre) ובלי המונה. */
  function labelOf(el) {
    var d = el.querySelector('[data-short]');
    if (d && d.getAttribute('data-short')) return d.getAttribute('data-short');
    d = el.querySelector('[data-text]');
    if (d && d.getAttribute('data-text')) return d.getAttribute('data-text');
    var c = el.cloneNode(true);
    [].slice.call(c.querySelectorAll('.mw,.tab-pre,.stab-n,.mfx-c')).forEach(function (x) { x.remove(); });
    return c.textContent.trim();
  }
  function countOf(el) {
    var n = el.querySelector('.stab-n,.mfx-c');
    return n ? n.textContent.trim() : '';
  }

  [].slice.call(document.querySelectorAll('.mfx')).forEach(function (mfx) {
    /* search.html טוען את chrome.js פעמיים (בלוק ההדגמה שאחרי </html>);
       בלי השמירה הזו כל לחיצה הייתה פותחת וסוגרת מיד. */
    if (mfx.getAttribute('data-mfx') === 'on') return;
    mfx.setAttribute('data-mfx', 'on');
    var head  = mfx.querySelector('.mfx-head');
    var val   = mfx.querySelector('.mfx-val');
    var panel = mfx.querySelector('.mfx-panel');
    if (!head || !val || !panel) return;

    function sync() {
      var on = panel.querySelector(ON);
      if (!on) return;
      var n = countOf(on);
      val.textContent = labelOf(on);
      if (n) {
        var chip = document.createElement('span');
        chip.className = 'mfx-n';
        chip.textContent = n;
        val.appendChild(chip);
      }
    }
    function setOpen(open) {
      mfx.classList.toggle('open', open);
      head.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    head.addEventListener('click', function () { setOpen(!mfx.classList.contains('open')); });

    /* המאזין של העמוד עצמו הוא שמסמן את הטאב הפעיל, ולכן הקריאה נדחית
       בתור אחריו; ההשהיה הקצרה נותנת לשורה הנבחרת להיראות לפני הסגירה. */
    panel.addEventListener('click', function (e) {
      if (!mq.matches || !e.target.closest || !e.target.closest(ROWS)) return;
      setTimeout(sync, 0);
      setTimeout(function () { setOpen(false); }, 180);
    });

    /* חזרה לדסקטופ באמצע מצב פתוח משאירה .open על רכיב שאין לו כותרת */
    var onMQ = function () { if (!mq.matches) setOpen(false); };
    if (mq.addEventListener) mq.addEventListener('change', onMQ);
    else if (mq.addListener) mq.addListener(onMQ);

    setOpen(false);
    sync();
  });
})();

/* אקורדיון הפוטר במובייל. הקיפול נבנה כאן ולא ב-CSS בלבד: מחלקת .acc
   וכפתורי הפתיחה נוספים רק כשהסקריפט רץ, כך שבלי ג׳אווהסקריפט הרשימות
   נשארות פרושות וכל הקישורים נגישים. מעל 768 האקורדיון מפורק לגמרי —
   ה-h4 חוזר להיות כותרת בלבד, כדי שקורא מסך לא יכריז על כפתור שאינו
   עושה דבר. */
(function () {
  var cols = document.querySelector('.f-cols');
  if (!cols) return;
  var mq = window.matchMedia('(max-width:768px)');
  var NS = 'http://www.w3.org/2000/svg';
  var rows = [];

  [].slice.call(cols.querySelectorAll('.f-col h4')).forEach(function (h, i) {
    var col = h.parentNode, list = col.querySelector('ul');
    if (!list) return;
    if (!list.id) list.id = 'f-acc-' + i;

    /* החץ נבנה כאן ולא כפינה מסובבת של border: border-right/left מתהפך
       בבניית האנגלית ו-border-inline-* מתהפך לפי dir, ובשני המקרים החץ
       היה מצביע הצידה ב-en. SVG סימטרי חסין לשניהם. */
    var svg = document.createElementNS(NS, 'svg'), p = document.createElementNS(NS, 'path');
    svg.setAttribute('class', 'acc-ch'); svg.setAttribute('width', '11');
    svg.setAttribute('height', '7'); svg.setAttribute('viewBox', '0 0 11 7');
    svg.setAttribute('fill', 'none'); svg.setAttribute('aria-hidden', 'true');
    p.setAttribute('d', 'M1 1L5.5 5.5L10 1'); p.setAttribute('stroke', '#76c9ff');
    p.setAttribute('stroke-width', '1.3'); p.setAttribute('stroke-linecap', 'round');
    p.setAttribute('stroke-linejoin', 'round');
    svg.appendChild(p);

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'acc-btn';
    btn.addEventListener('click', function () {
      var open = !col.classList.contains('open');
      col.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
    rows.push({ h: h, col: col, list: list, btn: btn, svg: svg });
  });
  if (!rows.length) return;

  function mount(r) {
    if (r.btn.parentNode) return;
    while (r.h.firstChild) r.btn.appendChild(r.h.firstChild);
    r.btn.appendChild(r.svg);
    r.h.appendChild(r.btn);
    r.btn.setAttribute('aria-controls', r.list.id);
    r.btn.setAttribute('aria-expanded', String(r.col.classList.contains('open')));
  }
  function unmount(r) {
    if (!r.btn.parentNode) return;
    if (r.svg.parentNode) r.svg.parentNode.removeChild(r.svg);
    while (r.btn.firstChild) r.h.appendChild(r.btn.firstChild);
    r.h.removeChild(r.btn);
    r.col.classList.remove('open');
  }
  function sync() {
    var on = mq.matches;
    rows.forEach(on ? mount : unmount);
    cols.classList.toggle('acc', on);
  }
  sync();
  if (mq.addEventListener) mq.addEventListener('change', sync);
  else if (mq.addListener) mq.addListener(sync);
})();

/* ---------- status tag: hug the wrapped text ---------- */
/* When a long label breaks over two lines the pill keeps the width the row
   handed it, so the panel runs on past the shorter line. There is no CSS length
   for "as wide as the longest line once it has wrapped", so the lines are
   measured and the text is pinned to the widest of them; the pill hugs its
   content, so it follows. Pinning to a line that already fits cannot move the
   break — and if it somehow does, or if the box will not take a width, the
   guard puts it back. Measurement is over the text NODES: a range over an
   element returns a rect per nested box, which is not a line count. */
(function () {
  var SEL = '.ptag,[data-name="tag"],[data-name="\u05ea\u05d2\u05d9\u05ea"]';

  function textNodes(root) {
    var out = [], w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false), n;
    while ((n = w.nextNode())) {
      if (n.nodeValue.trim() && !(n.parentNode.closest && n.parentNode.closest('svg'))) out.push(n);
    }
    return out;
  }

  /* the deepest element holding all of the text — that is the box to size */
  function holderOf(nodes) {
    var h = nodes[0].parentNode;
    for (var i = 1; i < nodes.length; i++) {
      while (!h.contains(nodes[i])) h = h.parentNode;
    }
    if (h.nodeType !== 1) h = h.parentNode;
    return h;
  }

  function lineRects(nodes) {
    var r = document.createRange();
    r.setStart(nodes[0], 0);
    var last = nodes[nodes.length - 1];
    r.setEnd(last, last.nodeValue.length);
    return r.getClientRects();
  }

  function fit() {
    [].slice.call(document.querySelectorAll(SEL)).forEach(function (p) {
      var nodes = textNodes(p);
      if (!nodes.length) return;
      var box = holderOf(nodes);
      if (box === p) return;                       /* nothing of our own to size */
      box.style.width = '';
      var rects = lineRects(nodes);
      if (rects.length < 2) return;                /* one line: already tight */
      var w = 0, i;
      for (i = 0; i < rects.length; i++) w = Math.max(w, rects[i].width);
      var was = box.getBoundingClientRect().width;
      box.style.width = Math.ceil(w) + 'px';
      var now = lineRects(nodes);
      if (now.length !== rects.length || box.getBoundingClientRect().width >= was) {
        box.style.width = '';                      /* no better: leave it alone */
      }
    });
  }

  function refit() { requestAnimationFrame(fit); } /* measure after the reflow */
  fit();
  window.addEventListener('resize', refit);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
})();
