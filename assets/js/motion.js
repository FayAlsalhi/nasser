/* ==========================================================================
   MOTION ENGINE
   - تقسيم النص إلى أسطر/كلمات داخل أقنعة
   - كشف عند التمرير (IntersectionObserver)
   - حركة مرتبطة بالتمرير (rAF واحد لكل الإطار)
   - شريط متحرك بسرعة ثابتة (px/s) واعٍ بالاتجاه
   لا مكتبات خارجية. كل التوقيتات من التوكنز.
   ========================================================================== */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;
  var dirFactor = getComputedStyle(root).direction === 'rtl' ? 1 : -1;

  /* ---------- أدوات ------------------------------------------------------ */
  function num(name, fallback) {
    var v = parseFloat(getComputedStyle(root).getPropertyValue(name));
    return isNaN(v) ? fallback : v;
  }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function debounce(fn, ms) {
    var t; return function () { clearTimeout(t); var a = arguments, s = this;
      t = setTimeout(function () { fn.apply(s, a); }, ms); };
  }

  /* ---------- 1. تقسيم النص --------------------------------------------- */
  function tokenize(el) {
    var out = [];
    Array.prototype.forEach.call(el.childNodes, function (n) {
      if (n.nodeType === 3) {
        n.textContent.split(/(\s+)/).forEach(function (t) {
          if (t.length) out.push({ t: t, cls: '', space: !t.trim() });
        });
      } else if (n.nodeType === 1) {
        var cls = n.getAttribute('class') || '';
        n.textContent.split(/(\s+)/).forEach(function (t) {
          if (t.length) out.push({ t: t, cls: cls, space: !t.trim() });
        });
      }
    });
    return out;
  }

  function splitWords(el) {
    var toks = tokenize(el), html = '', i = 0;
    toks.forEach(function (tk) {
      if (tk.space) { html += '<span class="word word--space"></span>'; return; }
      html += '<span class="word"><span class="word__inner ' + tk.cls +
              '" style="--i:' + (i++) + '">' + tk.t + '</span></span>';
    });
    el.innerHTML = html;
    el.style.setProperty('--n', i);
  }

  function splitLines(el) {
    var toks = tokenize(el), html = '';
    toks.forEach(function (tk) {
      if (tk.space) { html += ' '; return; }
      html += '<span class="w" ' + (tk.cls ? 'data-c="' + tk.cls + '"' : '') + '>' + tk.t + '</span>';
    });
    el.innerHTML = html;

    var words = el.querySelectorAll('.w'), lines = [], last = null;
    Array.prototype.forEach.call(words, function (w) {
      var top = Math.round(w.offsetTop);
      if (last === null || Math.abs(top - last) > 3) { lines.push([]); last = top; }
      lines[lines.length - 1].push(w);
    });

    var out = '';
    lines.forEach(function (line, i) {
      var inner = line.map(function (w) {
        var c = w.getAttribute('data-c');
        return c ? '<span class="' + c + '">' + w.textContent + '</span>' : w.textContent;
      }).join(' ');
      out += '<span class="line"><span class="line__inner" style="--i:' + i + '">' + inner + '</span></span>';
    });
    el.innerHTML = out;
    el.style.setProperty('--n', lines.length);
  }

  function applySplit(el) {
    if (!el.__raw) el.__raw = el.innerHTML;
    else el.innerHTML = el.__raw;
    if (el.getAttribute('data-split') === 'words') splitWords(el);
    else splitLines(el);
  }

  var splitTargets = document.querySelectorAll('[data-split]');
  Array.prototype.forEach.call(splitTargets, applySplit);

  var lastW = window.innerWidth;
  window.addEventListener('resize', debounce(function () {
    if (Math.abs(window.innerWidth - lastW) < 40) return;
    lastW = window.innerWidth;
    Array.prototype.forEach.call(splitTargets, function (el) {
      var wasIn = el.classList.contains('is-in');
      applySplit(el);
      if (wasIn) el.classList.add('is-in');
    });
  }, 220));

  /* ---------- 2. الكشف عند التمرير --------------------------------------- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting && e.intersectionRatio <= 0) return;
      var el = e.target;
      el.classList.add('is-in');
      // تتابع المجموعات: كل ابن يحمل --i تصاعدياً
      var group = el.getAttribute('data-stagger');
      if (group) {
        Array.prototype.forEach.call(el.children, function (c, i) {
          c.style.setProperty('--i', i);
          c.classList.add('is-in');
        });
      }
      io.unobserve(el);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

  /* ---------- 2.5 العدّاد الأسطواني ---------------------------------- */
  /* يحوّل نصاً رقمياً إلى خانات، كل خانة شريط 0..9 مكرّر ينتهي عند رقمها.
     الخانات اليمنى تدور دورات أكثر، فيبدو العدّ متصاعداً لا قفزة واحدة.
     مع تقليل الحركة لا نبني شيئاً: يبقى الرقم نصاً ثابتاً. */
  function buildOdometer(el) {
    var finalText = (el.textContent || '').trim();
    if (!/^\d+$/.test(finalText)) return;

    el.setAttribute('aria-label', finalText);
    var frag = document.createDocumentFragment();

    finalText.split('').forEach(function (ch, i) {
      var target = parseInt(ch, 10);
      var cycles = i + 1;                 // كل خانة إلى اليمين تدور أكثر
      var last = cycles * 10 + target;    // الموضع النهائي داخل الشريط

      var col = document.createElement('span');
      col.className = 'odo__col';
      col.setAttribute('aria-hidden', 'true');

      var strip = document.createElement('span');
      strip.className = 'odo__strip';
      strip.style.setProperty('--pos', last);
      strip.style.setProperty('--i', i);

      for (var n = 0; n <= last; n++) {
        var cell = document.createElement('span');
        cell.textContent = String(n % 10);
        strip.appendChild(cell);
      }

      col.appendChild(strip);
      frag.appendChild(col);
    });

    el.textContent = '';
    el.appendChild(frag);
    el.classList.add('odo--ready');
  }

  if (!reduced) {
    Array.prototype.forEach.call(
      document.querySelectorAll('[data-odometer]'), buildOdometer);
  }

  var revealables = document.querySelectorAll('[data-reveal],[data-split],[data-stagger],[data-odometer]');
  Array.prototype.forEach.call(revealables, function (el) { io.observe(el); });

  /* ---------- 3. الحركة المرتبطة بالتمرير -------------------------------- */
  var parallax = [].slice.call(document.querySelectorAll('[data-parallax]'));
  var pinnedTitles = [].slice.call(document.querySelectorAll('.pinned'));
  var heroPins = [].slice.call(document.querySelectorAll('.hero'));
  var blurMax = num('--blur-max', 5);
  var safety = [].slice.call(revealables);

  function frame() {
    var vh = window.innerHeight;

    parallax.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      var p = (vh - r.top) / (vh + r.height);      // 0 → 1 عبر النافذة
      var strength = parseFloat(el.getAttribute('data-parallax')) || 0.12;
      var y = (p - 0.5) * 2 * strength * r.height;
      el.style.transform = 'translate3d(0,' + (-y).toFixed(2) + 'px,0)';
    });

    heroPins.forEach(function (hero) {
      var media = hero.querySelector('.hero__media');
      if (!media) return;
      var r = hero.getBoundingClientRect();
      var total = r.height - vh;
      if (total <= 0) return;
      var p = clamp(-r.top / total, 0, 1);
      media.style.transform = 'translate3d(0,' + (p * 12).toFixed(2) + '%,0) scale(' + (1 + p * 0.10).toFixed(4) + ')';
      var ov = hero.querySelector('.hero__overlay');
      if (ov) ov.style.opacity = (1 - clamp(p * 1.35, 0, 1)).toFixed(3);
    });

    pinnedTitles.forEach(function (pin) {
      var title = pin.querySelector('.pinned__title');
      var body = pin.querySelector('.pinned__body');
      if (!title || !body) return;
      var br = body.getBoundingClientRect();
      var tr = title.getBoundingClientRect();
      // كم غطّى المحتوى العنوان
      var overlap = clamp((tr.bottom - br.top) / (tr.height + 40), 0, 1);
      title.style.filter = overlap > 0 ? 'blur(' + (overlap * blurMax).toFixed(2) + 'px)' : '';
      title.style.transform = 'scale(' + (1 - overlap * 0.03).toFixed(4) + ')';
      title.style.opacity = (1 - overlap * 0.25).toFixed(3);
    });

    // شبكة أمان: أي عنصر دخل النافذة ولم يُكشف بعد (قص/تحوّل يمنع المراقب) يُكشف هنا
    for (var i = safety.length - 1; i >= 0; i--) {
      var el = safety[i];
      var rr = el.getBoundingClientRect();
      if (rr.top < vh * 0.92 && rr.bottom > 0) {
        el.classList.add('is-in');
        if (el.hasAttribute('data-stagger')) {
          Array.prototype.forEach.call(el.children, function (c, k) {
            c.style.setProperty('--i', k); c.classList.add('is-in');
          });
        }
        safety.splice(i, 1);
      }
    }

    ticking = false;
  }

  var ticking = false;
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }

  if (reduced) {
    Array.prototype.forEach.call(revealables, function (el) { el.classList.add('is-in'); });
  }
  if (!reduced) {
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    onScroll();
  }

  /* ---------- 4. الشريط المتحرك ----------------------------------------- */
  var speed = num('--marquee-speed', 100);
  [].slice.call(document.querySelectorAll('.marquee')).forEach(function (m) {
    var track = m.querySelector('.marquee__track');
    if (!track) return;
    var base = track.innerHTML;
    // ضاعف المحتوى حتى يغطي ضعف عرض الشاشة على الأقل
    var guard = 0;
    while (track.scrollWidth < m.offsetWidth * 2 && guard++ < 12) track.innerHTML += base;
    var half = track.scrollWidth / 2;
    if (reduced) return;
    var x = 0, last = performance.now(), dir = (m.getAttribute('data-dir') === 'reverse' ? -1 : 1) * dirFactor;
    (function loop(now) {
      var dt = Math.min((now - last) / 1000, 0.05); last = now;
      x -= speed * dt * dir;
      if (x <= -half) x += half;
      if (x >= 0 && dir < 0) x -= half;
      track.style.transform = 'translate3d(' + x.toFixed(2) + 'px,0,0)';
      requestAnimationFrame(loop);
    })(last);
  });

  /* ---------- 5. جاهزية الصفحة ------------------------------------------ */
  requestAnimationFrame(function () {
    requestAnimationFrame(function () { root.classList.add('is-ready'); });
  });

  window.NM = { refresh: onScroll };
})();
