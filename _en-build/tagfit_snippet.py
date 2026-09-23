# -*- coding: utf-8 -*-
"""The one piece of behaviour the English site needs and the Hebrew does not:
a status label long enough to wrap leaves the pill wider than its own text."""

TAG_FIT_JS = u'''
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
  var SEL = '.ptag,[data-name="tag"],[data-name="\\u05ea\\u05d2\\u05d9\\u05ea"]';

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
'''
