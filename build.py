#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مولّد الصفحات الثابتة — يبني كل صفحات الموقع من مكوّنات مشتركة.
شغّله بعد أي تعديل على المحتوى:  python3 build.py
"""
import os, io, glob

def _asset_version():
    """بصمة من أحدث تعديل على الأصول — تتغيّر مع كل تعديل فقط."""
    root = os.path.dirname(os.path.abspath(__file__))
    files = glob.glob(os.path.join(root, "assets", "**", "*.*"), recursive=True)
    newest = max((os.path.getmtime(f) for f in files), default=0)
    return str(int(newest))

ASSET_V = _asset_version()

OUT = os.path.dirname(os.path.abspath(__file__))

SITE = {
    "name":  "ناصر الحنايا",
    "role":  "مصور فوتوغرافي",
    "phone": "+966553123193",
    "phone_display": "+966 55 312 3193",
    "wa":    "https://wa.me/966553123193",
    "ig":    "https://www.instagram.com/nasser_alhnay",
    "email": "Nasseralhnay@gmail.com",
    "credit_name": "عــجـلان",
    "credit_url":  "https://linktr.ee/ajlanms",
}

# الصور محلية بالكامل — لا اعتماد على استضافة خارجية.
# مصغّرة إلى 2000px وجودة 82 (23MB -> 2MB).
# نطاق الموقع بعد النشر — مطلوب لمعاينات المشاركة (og:image لا تقبل مساراً
# نسبياً). غيّره إلى نطاقك الحقيقي قبل النشر.
SITE_URL = "https://nasseralhanaya.com"

IMG = "assets/img/"
M = {
    "logo":        IMG + "logo.png",
    "hero":        IMG + "hero.jpg",
    "hero_alt":    IMG + "hero_alt.jpg",
    "about":       IMG + "about.jpg",
    "events":      IMG + "events.jpg",
    "weddings":    IMG + "weddings.jpg",
    "products":    IMG + "products.jpg",
    "portraits":   IMG + "portraits.jpg",
    "g1":          IMG + "g1.jpg",
    "g2":          IMG + "g2.jpg",
    "g3":          IMG + "g3.jpg",
    "g4":          IMG + "g4.jpg",
}

CATS = [
    {"slug": "album-events.html",    "title": "تغطيات احداث", "img": M["events"],
     "lead": "توثيق كل لحظة", "service": "تصوير تغطيات احداث"},
    {"slug": "album-weddings.html",  "title": "زواجات",       "img": M["weddings"],
     "lead": "ليلة لا تُنسى",  "service": "تصوير زواجات"},
    {"slug": "album-products.html",  "title": "منتجات",       "img": M["products"],
     "lead": "تفاصيل تبيع",    "service": "تصوير منتجات"},
    {"slug": "album-portraits.html", "title": "بورترية",      "img": M["portraits"],
     "lead": "وجه يحكي قصة",   "service": "تصوير بورترية"},
]

NAV = [
    ("index.html",   "الرئيسية"),
    ("about.html",   "من انا"),
    ("albums.html",  "اعمالي"),
    ("contact.html", "تواصل معي"),
]

ARROW = ('<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="1.5" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>')
ARROW_UP = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            'aria-hidden="true"><path d="M17 17V7H7M17 7L6 18"/></svg>')
WA_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" '
           'width="18" height="18" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20.5l1.7-5.2A8.5 8.5 0 1 1 21 11.5Z"/>'
           '<path d="M8.6 9.2c.2 2.6 3.6 6 6.2 6.2l1.3-1.3-2-1.2-1 .8c-1-.4-2.2-1.6-2.6-2.6l.8-1-1.2-2-1.5 1.1Z"/></svg>')
MAIL_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" '
             'width="18" height="18" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/>'
             '<path d="m3.5 7 8.5 6 8.5-6"/></svg>')
IG_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" '
           'width="18" height="18" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/>'
           '<circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/></svg>')


def head(title, desc, page):
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#000000">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE_URL}/{M['hero']}">
<meta property="og:type" content="website">
<script>document.documentElement.classList.add('js');</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&amp;family=IBM+Plex+Sans+Arabic:wght@300;400;500&amp;family=Rakkas&amp;family=Inter:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f%5B%5D=clash-display@400,500,600&amp;display=swap">
<link rel="stylesheet" href="assets/css/tokens.css?v={ASSET_V}">
<link rel="stylesheet" href="assets/css/typography.css?v={ASSET_V}">
<link rel="stylesheet" href="assets/css/base.css?v={ASSET_V}">
<link rel="stylesheet" href="assets/css/components.css?v={ASSET_V}">
<link rel="stylesheet" href="assets/css/pages.css?v={ASSET_V}">
<link rel="stylesheet" href="assets/css/motion.css?v={ASSET_V}">
</head>
<body data-page="{page}">
<a class="sr-only" href="#main">تخطَّ إلى المحتوى</a>
"""


def header():
    return f"""
<header class="header page-in">
  <div class="header__inner">
    <a class="logo" href="index.html" aria-label="{SITE['name']} — الرئيسية">
      <img src="{M['logo']}" alt="{SITE['name']}" width="97" height="25">
    </a>
    <button class="burger" type="button" aria-label="القائمة" aria-expanded="false" aria-controls="nav">
      <span class="burger__bar"></span><span class="burger__bar"></span><span class="burger__bar"></span>
    </button>
  </div>
</header>

<nav class="nav" id="nav" aria-label="التنقل الرئيسي">
  <ul class="nav__list">
""" + "\n".join(
        f'    <li class="nav__item"><a class="nav__link" data-nav href="{h}">{t}{ARROW}</a></li>'
        for h, t in NAV) + f"""
  </ul>
  <div class="nav__foot">
    <a class="t-label link-u" href="{SITE['ig']}" target="_blank" rel="noopener">INSTAGRAM</a>
    <a class="t-label link-u" href="{SITE['wa']}" target="_blank" rel="noopener">WHATSAPP</a>
    <a class="t-label link-u" href="mailto:{SITE['email']}">EMAIL</a>
  </div>
</nav>

<div class="peek" aria-hidden="true"><img alt="" decoding="async"></div>

<div class="cursor" aria-hidden="true">
  <span class="cursor__c"></span><span class="cursor__c"></span>
  <span class="cursor__c"></span><span class="cursor__c"></span>
  <span class="cursor__label"></span>
</div>
"""


# --------------------------------------------------------------------------- #
#  عدسة الكاميرا (SVG) — تُبنى هندسياً لا يدوياً حتى يسهل تغيير عدد الريشات
# --------------------------------------------------------------------------- #
import math as _math

APERTURE_BLADES = 6
_C = 110.0          # مركز الـviewBox
_R = 100.0          # نصف قطر البرميل
_IRIS = 46.0        # نصف قطر الحدقة وهي مغلقة


def _poly(radius, n=APERTURE_BLADES, rot=-_math.pi / 2):
    pts = []
    for i in range(n):
        a = 2 * _math.pi * i / n + rot
        pts.append("%.2f,%.2f" % (_C + radius * _math.cos(a), _C + radius * _math.sin(a)))
    return " ".join(pts)


def _knurl(n=54, r_in=90.0, r_out=99.0):
    """حزّ حلقة الضبط حول البرميل — يعطي إحساس العدسة الحقيقية."""
    out = []
    for i in range(n):
        a = 2 * _math.pi * i / n
        x1, y1 = _C + r_in * _math.cos(a), _C + r_in * _math.sin(a)
        x2, y2 = _C + r_out * _math.cos(a), _C + r_out * _math.sin(a)
        out.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (x1, y1, x2, y2))
    return "".join(out)


def _blade_edges(n=APERTURE_BLADES, r_out=88.0, rot=-_math.pi / 2):
    """خطوط فصل الريشات: من رؤوس الحدقة إلى حافة البرميل."""
    out = []
    for i in range(n):
        a = 2 * _math.pi * i / n + rot
        x1, y1 = _C + _IRIS * _math.cos(a), _C + _IRIS * _math.sin(a)
        x2, y2 = _C + r_out * _math.cos(a), _C + r_out * _math.sin(a)
        out.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (x1, y1, x2, y2))
    return "".join(out)


def aperture(label, href):
    return f"""      <a class="aperture" href="{href}" aria-label="{label}" data-magnet data-cursor="{label}">
        <svg class="aperture__svg" viewBox="0 0 220 220" width="220" height="220" aria-hidden="true">
          <circle class="aperture__barrel" cx="110" cy="110" r="{_R}"/>
          <g class="aperture__knurl">{_knurl()}</g>
          <circle class="aperture__ring" cx="110" cy="110" r="88"/>
          <polygon class="aperture__iris" points="{_poly(_IRIS)}"/>
          <g class="aperture__edges">{_blade_edges()}</g>
          <circle class="aperture__glint" cx="82" cy="80" r="13"/>
        </svg>
        <span class="aperture__label t-heavy-s">{label}</span>
      </a>"""


def cta():
    # بلا أيقونات وبلا لوقو: اللوقو موجود أصلاً في الهيدر، والأيقونات العامة
    # تضعف الإحساس التحريري. الاسم كبير والقيمة أكبر — نفس لغة قائمة الخدمات.
    channels = [
        ("واتساب",    SITE["phone_display"], SITE["wa"]),
        ("إنستقرام",  "@nasser_alhnay",      SITE["ig"]),
        ("البريد",    SITE["email"],         "mailto:" + SITE["email"]),
    ]
    rows = "\n".join(
        f"""      <a class="channel" href="{href}"{' target="_blank" rel="noopener"' if href.startswith('http') else ''}
         data-reveal="up" style="--i:{i+3}">
        <span class="channel__label t-label">{label}</span>
        <span class="channel__value" dir="ltr">{value}</span>
        <span class="channel__go" aria-hidden="true">{ARROW}</span>
      </a>""" for i, (label, value, href) in enumerate(channels))

    return f"""
<section class="cta brackets" data-theme="light">
  <div class="shell cta__inner">
    <p class="t-label cta__kicker" data-reveal="up">جاهز نبدأ مشروعك</p>

    <div data-reveal="up" style="--i:1">
{aperture("للتواصل", "contact.html")}
    </div>

    <div class="channels">
{rows}
    </div>
  </div>
</section>
"""


def footer(page):
    marquee_items = "".join(
        f'<span class="marquee__item t-display-xxl">{SITE["role"]}</span>' for _ in range(4))
    return f"""
<footer class="footer">
  <div class="shell stack">
    <hr class="rule" data-reveal="rule">
    <nav class="footer__nav" aria-label="روابط الفوتر">
""" + "\n".join(
        f'      <a class="t-heavy-s link-u{" is-current" if h == page else ""}" data-nav href="{h}">{t}</a>'
        for h, t in NAV) + f"""
    </nav>
  </div>
  <div class="marquee footer__mark" aria-hidden="true">
    <div class="marquee__track">{marquee_items}</div>
  </div>
</footer>

<script src="assets/js/motion.js?v={ASSET_V}" defer></script>
<script src="assets/js/site.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def work_card(cat, i, wide=True):
    ratio = "media--wide" if wide else "media--card"
    return f"""
      <a class="work" href="{cat['slug']}" data-cursor="VIEW" data-reveal="media" style="--i:{i}">
        <div class="media {ratio} work__media">
          <img src="{cat['img']}" alt="{cat['title']}" loading="lazy" decoding="async">
        </div>
        <span class="work__corner">{ARROW_UP}</span>
        <span class="work__meta">
          <span class="pill">اكتشف المزيد</span>
          <span class="t-display-s work__title">{cat['title']}</span>
        </span>
      </a>"""


# --------------------------------------------------------------------------- #
#  الصفحات
# --------------------------------------------------------------------------- #
def page_index():
    works_full = work_card(CATS[0], 0) + work_card(CATS[1], 1)
    works_pair = work_card(CATS[2], 0, wide=False) + work_card(CATS[3], 1, wide=False)
    services = "\n".join(
        f"""      <a class="service" href="{c['slug']}" data-reveal="up" style="--i:{i}"
         data-peek="{c['img']}" data-cursor="VIEW">
        <span class="service__num">{i+1:02d}</span>
        <span class="service__body">
          <span class="service__title">{c['service']}</span>
          <span class="service__lead t-label">{c['lead']}</span>
        </span>
        <span class="service__go" aria-hidden="true">{ARROW}</span>
      </a>""" for i, c in enumerate(CATS))

    return (head(f"{SITE['name']} — {SITE['role']}",
                 "ملف أعمال ناصر الحنايا، مصور فوتوغرافي: تغطيات أحداث، زواجات، منتجات، وبورترية.",
                 "index.html")
            + header() + f"""
<main id="main">

  <!-- ١. الهيرو المثبّت -->
  <section class="hero" data-theme="fog">
    <div class="hero__pin">
      <div class="hero__media"><img src="{M['hero']}" alt="{SITE['name']}" fetchpriority="high"></div>
      <div class="hero__overlay">
        <h1 class="t-display-xl hero__title" data-split="words">{SITE['name']}</h1>
      </div>
    </div>
    <div class="hero__scroll-space"></div>
  </section>

  <!-- ٢. شريط «اعمل منذ» — بطاقة زجاجية تتداخل مع حافة الصورة -->
  <section class="section section--tight" style="padding-block-start:0">
    <div class="shell">
      <div class="glass row row--between row--wrap" style="margin-block-start:calc(var(--block) * -1)"
           data-reveal="up">
        <p class="t-lead" style="font-family:var(--f-display)">اعمل منذ</p>
        <p class="t-num-xl odo" data-odometer>2018</p>
      </div>
    </div>
  </section>

  <!-- ٣. من انا -->
  <section class="section">
    <div class="shell stack">
      <h2 class="t-display-m t-display-m--airy t-accent" data-split="words">من انا</h2>
      <p class="t-lead" data-split="lines">مصور فوتوغرافي من <span class="num">2018</span> محب للأضاءة، اولويتي دائماً اخراج صوره <span class="t-accent">تحكي قصة</span>.</p>
      <div class="btn-group" data-reveal="up">
        <a class="btn" href="about.html">اعرف عني اكثر</a>
        <span class="arrow-dot">{ARROW}</span>
      </div>
    </div>
  </section>

  <!-- ٤. اعمالي — عنوان مثبّت خلف الصور -->
  <section class="section section--flush-top pinned">
    <div class="shell">
      <h2 class="t-display-l t-accent pinned__title" data-split="words">اعمالي</h2>
      <div class="pinned__body stack stack--block" style="margin-block-start:var(--block)">
        {works_full}
        <div class="grid grid--2">{works_pair}
        </div>
      </div>
    </div>
  </section>

  <!-- ٥. خدماتي -->
  <section class="section" data-theme="light">
    <div class="shell stack">
      <p class="t-label" data-reveal="up">04 — الخدمات</p>
      <h2 class="t-display-m" data-split="words">خدماتي</h2>
      <div class="stack" style="margin-block-start:var(--rhythm)">
{services}
      </div>
    </div>
  </section>

  <section class="section section--tight" aria-hidden="true"></section>

  {cta()}
</main>
""" + footer("index.html"))


def page_about():
    traits = ["الرؤية الإبداعية", "الاحترافية", "شغوف", "المرونة"]
    # زوايا الميلان تصنع شكل «المروحة» — مقاسة من المرجع.
    # الالتصاق على الغلاف والميلان على الكرت: transform على عنصر sticky يبطله.
    angles = [10, -5, 4, -6]
    trait_html = "\n".join(
        f'''        <div class="stackcards__item" style="z-index:{i+1}">
          <div class="stackcard" data-reveal="card"
               style="--rot:{angles[i % len(angles)]}deg; --i:{i}">
            <p class="stackcard__text">{t}</p>
          </div>
        </div>'''
        for i, t in enumerate(traits))
    return (head(f"عني — {SITE['name']}",
                 "من أنا: مصور فوتوغرافي يهتم بالإضاءة وبالصورة التي تحكي قصة.",
                 "about.html")
            + header() + f"""
<main id="main">

  <section class="section" style="padding-block-start:calc(var(--header-h) + var(--section))">
    <div class="shell">
      <div class="about-hero">
        <h1 class="t-display-l about-hero__a" data-split="words">ناصر</h1>
        <div class="media media--card about-hero__img" data-reveal="media" data-parallax="0.08">
          <img src="{M['about']}" alt="{SITE['name']}" fetchpriority="high">
        </div>
        <h1 class="t-display-l about-hero__b" data-split="words">الحنايا</h1>
      </div>
      <div class="row row--between row--wrap" style="margin-block-start:var(--rhythm)" data-stagger>
        <p class="t-label" data-reveal="up">فوتوجرافي</p>
        <p class="t-label t-label--muted" data-reveal="up">اسحب للأسفل</p>
        <a class="t-label link-u" href="{SITE['wa']}" target="_blank" rel="noopener" data-reveal="up">أتصل بي</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="shell">
      <p class="t-lead" data-split="lines">مصور فوتوغرافي من <span class="num">2018</span> محب للأضاءة، اولويتي دائماً اخراج صوره <span class="t-accent">تحكي قصة</span>.</p>
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="shell stack">
      <p class="t-label" data-reveal="up">02 — القيم</p>
      <h2 class="t-display-m stackcards__head" data-split="words">وش راح تحصل فيني</h2>
      <div class="stackcards">
{trait_html}
      </div>
    </div>
  </section>

  {cta()}
</main>
""" + footer("about.html"))


def page_albums():
    cards = "\n".join(work_card(c, i, wide=False) for i, c in enumerate(CATS))
    return (head(f"اعمالي — {SITE['name']}",
                 "ألبومات الأعمال: تغطيات أحداث، زواجات، منتجات، بورترية.",
                 "albums.html")
            + header() + f"""
<main id="main">

  <section class="section" style="padding-block-start:calc(var(--header-h) + var(--section))">
    <div class="shell section-head section-head--center">
      <h1 class="t-display-l" data-split="words">الاعمال</h1>
      <span class="pill pill--accent" data-reveal="up">الصور</span>
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="shell">
      <div class="grid grid--2">
{cards}
      </div>
    </div>
  </section>

  {cta()}
</main>
""" + footer("albums.html"))


def page_album(cat):
    others = [c for c in CATS if c["slug"] != cat["slug"]]
    other_html = "\n".join(work_card(c, i, wide=False) for i, c in enumerate(others))
    gallery = [M["g1"], M["g2"], M["g3"], M["g4"], cat["img"], M["hero_alt"]]
    gal_html = "\n".join(
        f"""        <figure class="media {'media--tall' if i % 3 == 1 else 'media--card'}" data-cursor="ZOOM" data-reveal="media" style="--i:{i%3}">
          <img src="{g}" alt="{cat['title']} — {i+1}" loading="lazy" decoding="async">
        </figure>""" for i, g in enumerate(gallery))
    return (head(f"{cat['title']} — {SITE['name']}",
                 f"ألبوم {cat['title']} — {SITE['name']}، {SITE['role']}.",
                 "albums.html")
            + header() + f"""
<main id="main">

  <section class="section section--tight" style="padding-block-start:calc(var(--header-h) + var(--rhythm))">
    <div class="shell">
      <div class="media media--wide" data-reveal="media">
        <img src="{cat['img']}" alt="{cat['title']}" fetchpriority="high">
      </div>
      <h1 class="t-display-l work__title album-title" data-split="words">{cat['title']}</h1>
    </div>
  </section>

  <section class="section">
    <div class="shell section-head section-head--center">
      <p class="t-label" data-reveal="up">وصف للخدمة</p>
      <h2 class="t-display-m" data-split="words">{cat['lead']}</h2>
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="shell">
      <div class="grid grid--3">
{gal_html}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="shell stack">
      <div class="row row--between row--wrap">
        <h2 class="t-display-m" data-split="words">المزيد من اعمالي</h2>
        <a class="btn" href="albums.html">كل الاعمال</a>
      </div>
      <div class="grid grid--3">
{other_html}
      </div>
    </div>
  </section>

  {cta()}
</main>
""" + footer("albums.html"))


def page_contact():
    return (head(f"بيانات التواصل — {SITE['name']}",
                 "تواصل مع ناصر الحنايا: البريد، الجوال، إنستقرام.",
                 "contact.html")
            + header() + f"""
<main id="main">

  <section class="section" style="padding-block-start:calc(var(--header-h) + var(--section))">
    <div class="shell section-head section-head--center">
      <h1 class="t-display-l" data-split="words">معلومات التواصل</h1>
    </div>
  </section>

  <section class="section section--flush-top">
    <div class="shell">
      <a class="panel" href="mailto:{SITE['email']}" data-reveal="up">
        <span class="t-label t-label--latin t-label--wide t-label--muted">EMAIL</span>
        <span class="t-heavy-m" dir="ltr">{SITE['email']}</span>
      </a>
      <a class="panel" href="{SITE['wa']}" target="_blank" rel="noopener" data-reveal="up" style="--i:1">
        <span class="t-label t-label--latin t-label--wide t-label--muted">PHONE</span>
        <span class="t-num-m" dir="ltr">{SITE['phone']}</span>
      </a>
      <a class="panel" href="{SITE['ig']}" target="_blank" rel="noopener" data-reveal="up" style="--i:2">
        <span class="t-label t-label--latin t-label--wide t-label--muted">INSTAGRAM</span>
        <span class="t-heavy-m" dir="ltr">@nasser_alhnay</span>
      </a>
    </div>
  </section>

  <section class="section">
    <div class="shell stack">
      <h2 class="t-display-m" data-split="words">ارسال رسالة</h2>
      <form class="stack stack--tight" action="mailto:{SITE['email']}" method="post" enctype="text/plain">
        <div class="field" data-reveal="up">
          <label class="t-label t-label--muted" for="f-name">الاسم</label>
          <input id="f-name" name="name" type="text" required autocomplete="name">
        </div>
        <div class="field" data-reveal="up" style="--i:1">
          <label class="t-label t-label--muted" for="f-email">البريد الإلكتروني</label>
          <input id="f-email" name="email" type="email" required autocomplete="email" dir="ltr">
        </div>
        <div class="field" data-reveal="up" style="--i:2">
          <label class="t-label t-label--muted" for="f-msg">الرسالة</label>
          <textarea id="f-msg" name="message" required></textarea>
        </div>
        <div class="btn-group" data-reveal="up" style="--i:3">
          <button class="btn btn--filled" type="submit">ارسال</button>
          <span class="arrow-dot">{ARROW}</span>
        </div>
      </form>
    </div>
  </section>
</main>
""" + footer("contact.html"))


# --------------------------------------------------------------------------- #
def write(name, html):
    with io.open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(html)
    print("built", name)


if __name__ == "__main__":
    write("index.html",   page_index())
    write("about.html",   page_about())
    write("albums.html",  page_albums())
    write("contact.html", page_contact())
    for c in CATS:
        write(c["slug"], page_album(c))
