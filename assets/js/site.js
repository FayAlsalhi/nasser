/* ملاحظة: يعمل بلا أي مكتبة خارجية */
/* ==========================================================================
   SITE — تفاعلات الواجهة: القائمة، المؤشر المخصص، الحالة النشطة، النموذج
   ========================================================================== */
(function () {
  'use strict';
  var root = document.documentElement;

  /* ---------- 1. طبقة التنقّل ------------------------------------------- */
  var nav = document.querySelector('.nav');
  var burger = document.querySelector('.burger');
  if (nav && burger) {
    var links = nav.querySelectorAll('.nav__link');
    Array.prototype.forEach.call(links, function (l, i) { l.style.transitionDelay = (i * 60 + 90) + 'ms'; });

    function setNav(open) {
      nav.classList.toggle('is-open', open);
      burger.classList.toggle('is-open', open);
      burger.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('is-locked', open);
      if (!open) Array.prototype.forEach.call(links, function (l, i) {
        l.style.transitionDelay = (i * 30) + 'ms';
      });
      else Array.prototype.forEach.call(links, function (l, i) {
        l.style.transitionDelay = (i * 60 + 90) + 'ms';
      });
    }
    burger.addEventListener('click', function () { setNav(!nav.classList.contains('is-open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setNav(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setNav(false); });
  }

  /* ---------- 2. الحالة النشطة في التنقّل -------------------------------- */
  var here = location.pathname.split('/').pop() || 'index.html';
  Array.prototype.forEach.call(document.querySelectorAll('[data-nav]'), function (a) {
    if (a.getAttribute('href') === here) { a.classList.add('is-current'); a.setAttribute('aria-current', 'page'); }
  });

  /* ---------- 3. المؤشر المخصص ------------------------------------------ */
  var cursor = document.querySelector('.cursor');
  if (cursor && window.matchMedia('(hover:hover) and (pointer:fine)').matches) {
    var label = cursor.querySelector('.cursor__label');
    var tx = 0, ty = 0, cx = 0, cy = 0, on = false;

    document.addEventListener('pointermove', function (e) { tx = e.clientX; ty = e.clientY; }, { passive: true });
    (function loop() {
      cx += (tx - cx) * 0.18; cy += (ty - cy) * 0.18;
      cursor.style.transform = 'translate3d(' + cx.toFixed(1) + 'px,' + cy.toFixed(1) + 'px,0)' + (on ? ' scale(1)' : ' scale(.6)');
      requestAnimationFrame(loop);
    })();

    Array.prototype.forEach.call(document.querySelectorAll('[data-cursor]'), function (el) {
      el.addEventListener('pointerenter', function () {
        on = true; cursor.classList.add('is-on');
        if (label) label.textContent = el.getAttribute('data-cursor') || '';
      });
      el.addEventListener('pointerleave', function () { on = false; cursor.classList.remove('is-on'); });
    });
  }

  /* ---------- 4. أزرار مغناطيسية خفيفة ---------------------------------- */
  if (window.matchMedia('(hover:hover) and (pointer:fine)').matches &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    Array.prototype.forEach.call(document.querySelectorAll('[data-magnet]'), function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var dx = (e.clientX - (r.left + r.width / 2)) * 0.18;
        var dy = (e.clientY - (r.top + r.height / 2)) * 0.28;
        el.style.transform = 'translate3d(' + dx.toFixed(1) + 'px,' + dy.toFixed(1) + 'px,0)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
  }

  /* ---------- 4.5 معاينة صورة الخدمة تتبع المؤشر ---------------------- */
  /* سطح المكتب فقط: على اللمس لا يوجد hover فالمعاينة تصبح ضوضاء.
     نستعمل حلقة تنعيم واحدة بدل تحديث الموضع في كل حدث حركة. */
  var peek = document.querySelector('.peek');
  if (peek && window.matchMedia('(hover:hover) and (pointer:fine)').matches &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var pImg = peek.querySelector('img');
    var px = 0, py = 0, pcx = 0, pcy = 0, pOn = false, started = false;

    document.addEventListener('pointermove', function (e) {
      px = e.clientX; py = e.clientY;
      if (!started) { pcx = px; pcy = py; started = true; }
    }, { passive: true });

    (function pLoop() {
      pcx += (px - pcx) * 0.14;
      pcy += (py - pcy) * 0.14;
      peek.style.translate = pcx.toFixed(1) + 'px ' + pcy.toFixed(1) + 'px';
      requestAnimationFrame(pLoop);
    })();

    Array.prototype.forEach.call(document.querySelectorAll('[data-peek]'), function (el) {
      el.addEventListener('pointerenter', function () {
        var src = el.getAttribute('data-peek');
        if (src && pImg.getAttribute('src') !== src) pImg.setAttribute('src', src);
        pOn = true; peek.classList.add('is-on');
      });
      el.addEventListener('pointerleave', function () {
        pOn = false; peek.classList.remove('is-on');
      });
    });
  }

  /* ---------- 5. سنة الفوتر --------------------------------------------- */
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();

  root.classList.add('js-ready');
})();
