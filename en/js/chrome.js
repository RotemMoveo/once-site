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
  clickable('[data-name^="כרטיס — "]', page === 'urban-renewal.html' ? 'projects.html' : 'project.html');
  clickable('.pcard', 'projects.html');
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
    // flex-start: a full row (2 cards) exactly fills the width so it is unaffected;
    // only a leftover odd card gets pushed to the left, as LTR reading expects.
    wrap.className = 'cards-grid';
    gridParent.insertBefore(wrap, firstRow);
    ordered.forEach(function (c) { wrap.appendChild(c); });
    [].slice.call(gridParent.children).forEach(function (ch) {
      if (ch !== wrap && ch.getAttribute('data-name') && ch.getAttribute('data-name').indexOf('שורה') === 0) ch.remove();
    });
  }

  // --- tabs ---
  var tabs = [].slice.call(document.querySelectorAll('[data-name="active tab"],[data-name="non-active tab"]'));
  function labelOf(t) { return t.textContent.trim(); }
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
        if (!e.children.length && e.textContent.trim()) {
          e.style.color = on ? '#003A5E' : '#777777';
          e.style.fontWeight = on ? '700' : '400';
        }
      });
    });
  }
  tabs.forEach(function (t) {
    t.style.cursor = 'pointer';
    t.addEventListener('click', function () { applyFilter(labelOf(t)); });
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

// ---------- image gallery (.pgal): dots + 4s autoplay ----------
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

/* ---------- POPUP — the lead panel, on the project page ----------
   The generic corner panel: its markup sits at the end of project.html and its
   styles in chrome.css under POPUP. It belongs to the project page — that is
   where a visitor is already looking at one specific project — and not to the
   projects lobby, which is still a list to browse.
   It is not modal: it takes no focus, dims nothing, and closes only on the ×
   or Escape. Trigger: once the visitor has scrolled past the hero, i.e. has
   actually started reading, or after a dwell of 14s, whichever comes first.
   Once closed or sent it stays away for the rest of the session, so moving
   between project pages does not bring it back. */
(function () {
  if ((location.pathname.split('/').pop() || '') !== 'project.html') return;
  /* popup.html shows the panel over a live project page in an iframe; the
     page inside a decorative frame must not pop one of its own. */
  if (window.top !== window.self) return;
  var dock = document.getElementById('dock');
  if (!dock) return;
  var pop = document.getElementById('pop'),
      form = document.getElementById('popForm'),
      KEY = 'once-pop-seen',
      seen = false, timer = null;
  try { seen = sessionStorage.getItem(KEY) === '1'; } catch (e) {}

  function settle() {
    seen = true;
    try { sessionStorage.setItem(KEY, '1'); } catch (e) {}
  }
  function onScroll() {
    if (window.pageYOffset > window.innerHeight * .9) open();
  }
  function open() {
    if (seen || dock.classList.contains('open')) return;
    dock.classList.add('open');
    window.removeEventListener('scroll', onScroll);
    if (timer) { clearTimeout(timer); timer = null; }
  }
  /* closing is the visitor's answer, so it is remembered for the session */
  function close() { dock.classList.remove('open'); settle(); }

  if (!seen) {
    timer = setTimeout(open, 14000);
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  document.getElementById('popClose').addEventListener('click', close);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && dock.classList.contains('open')) close();
  });

  /* the underline sharpens on focus and stays sharp while the field holds text */
  [].slice.call(dock.querySelectorAll('.fld input')).forEach(function (i) {
    function sync() {
      i.closest('.fld').classList.toggle('on',
        document.activeElement === i || i.value.trim() !== '');
    }
    i.addEventListener('focus', sync);
    i.addEventListener('blur', sync);
    i.addEventListener('input', sync);
    sync();
  });

  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    pop.classList.add('done');
    pop.querySelector('.pop-body').scrollTop = 0;
    settle();
  });
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
