# -*- coding: utf-8 -*-
"""Assembles the static HTML pages for the drum site (shared header/footer)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{desc}">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@300;400;500;600&family=Noto+Serif+Thai:wght@400;500;600&family=IBM+Plex+Sans+Thai:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='14' fill='none' stroke='%23c9a961' stroke-width='2'/%3E%3Ccircle cx='16' cy='16' r='5' fill='%23c9a961'/%3E%3C/svg%3E">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body data-page="{page}" data-title-en="{title_en}" data-title-th="{title_th}">

<!-- ===== Header ===== -->
<header class="header">
  <div class="wrap nav">
    <a class="brand" href="/">
      <span class="brand__mark">SL</span>
      <span class="brand__name"><span data-i18n="brand.name">Suttipoj&nbsp;Liang&nbsp;W.</span>
        <span class="brand__sub" data-i18n="brand.sub">Drum Academy</span>
      </span>
    </a>

    <nav class="menu" id="menu">
      <a href="/"   data-nav="home"    data-i18n="nav.home">Home</a>
      <a href="/profile" data-nav="profile" data-i18n="nav.profile">Profile</a>
      <a href="/lesson"  data-nav="lesson"  data-i18n="nav.lesson">Lesson</a>
      <a href="/contact" data-nav="contact" data-i18n="nav.contact">Contact</a>
      <a href="/login"   data-nav="login"   data-i18n="nav.login">Log in</a>
    </nav>

    <div class="nav__right">
      <div class="lang" role="group" aria-label="Language / ภาษา">
        <button type="button" data-lang="en">EN</button>
        <button type="button" data-lang="th">ไทย</button>
      </div>
      <a href="/contact" class="btn btn--gold btn--sm" data-i18n="nav.cta">Book a trial</a>
      <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu">
        <span></span><span></span>
      </button>
    </div>
  </div>
</header>
"""

FOOTER = """
<!-- ===== Footer ===== -->
<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <a class="brand" href="/">
          <span class="brand__mark">SL</span>
          <span class="brand__name"><span data-i18n="brand.name">Suttipoj&nbsp;Liang&nbsp;W.</span>
            <span class="brand__sub" data-i18n="brand.sub">Drum Academy</span>
          </span>
        </a>
        <p class="footer__about" data-i18n="ft.about"></p>
        <div class="socials">
          <a href="#" aria-label="YouTube">YT</a>
          <a href="#" aria-label="Instagram">IG</a>
          <a href="#" aria-label="Facebook">FB</a>
          <a href="#" aria-label="TikTok">TT</a>
        </div>
      </div>

      <div>
        <h5 data-i18n="ft.menu">Menu</h5>
        <ul>
          <li><a href="/"   data-i18n="nav.home">Home</a></li>
          <li><a href="/profile" data-i18n="nav.profile">Profile</a></li>
          <li><a href="/lesson"  data-i18n="nav.lesson">Lesson</a></li>
          <li><a href="/contact" data-i18n="nav.contact">Contact</a></li>
          <li><a href="/login"   data-i18n="nav.login">Log in</a></li>
        </ul>
      </div>

      <div>
        <h5 data-i18n="ft.lessons">Lessons</h5>
        <ul>
          <li><a href="/lesson" data-i18n="ft.l1">Beginner path</a></li>
          <li><a href="/lesson" data-i18n="ft.l2">Groove library</a></li>
          <li><a href="/lesson" data-i18n="ft.l3">Rudiments</a></li>
          <li><a href="/lesson" data-i18n="ft.l4">Odd time</a></li>
          <li><a href="/lesson" data-i18n="ft.l5">Play-alongs</a></li>
        </ul>
      </div>

      <div>
        <h5 data-i18n="ft.reach">Get in touch</h5>
        <ul>
          <li><a href="mailto:hello@suttipojdrums.com" data-setting="contact_email">hello@suttipojdrums.com</a></li>
          <li><a href="tel:+6620000000" data-setting="contact_phone">+66 2 000 0000</a></li>
          <li><a href="/contact" data-i18n="ct.i2v">Bangkok, Thailand</a></li>
        </ul>
      </div>
    </div>

    <div class="footer__bar">
      <span>&copy; 2026 <span data-i18n="brand.name">Suttipoj Liang W.</span> <span data-i18n="ft.rights">All rights reserved.</span></span>
      <span style="display:flex;gap:22px">
        <a href="#" data-i18n="ft.privacy">Privacy</a>
        <a href="#" data-i18n="ft.terms">Terms</a>
      </span>
    </div>
  </div>
</footer>

<script src="assets/js/supabase-config.js"></script>
<script src="assets/js/db.js"></script>
<script src="assets/js/i18n.js"></script>
<script src="assets/js/main.js"></script>
<script src="assets/js/content.js"></script>
</body>
</html>
"""

def page(name, meta, body, footer=True):
    html = HEAD.format(**meta) + body + (FOOTER if footer else
        '\n<script src="assets/js/supabase-config.js"></script>\n<script src="assets/js/db.js"></script>'
        '\n<script src="assets/js/i18n.js"></script>\n<script src="assets/js/main.js"></script>'
        '\n<script src="assets/js/content.js"></script>\n</body>\n</html>\n')
    with open(os.path.join(ROOT, name), "w") as f:
        f.write(html)
    print("wrote", name, len(html), "bytes")

PLAY = ('<span class="vcard__play"><svg width="15" height="17" viewBox="0 0 15 17" fill="currentColor" '
        'aria-hidden="true"><path d="M14 7.63a1 1 0 0 1 0 1.74l-12 6.8A1 1 0 0 1 .5 15.3V1.7A1 1 0 0 1 2 .83l12 6.8Z"/></svg></span>')

def vcard(key_t, key_d, lvl_key, length, tags, cat_key, reveal=True):
    return f"""        <article class="vcard" data-tags="{tags}"{' data-reveal' if reveal else ''}>
          <div class="vcard__thumb">
            <span class="vcard__lvl" data-i18n="{lvl_key}"></span>
            {PLAY}
            <span class="vcard__len">{length}</span>
          </div>
          <div class="vcard__body">
            <h3 data-i18n="{key_t}"></h3>
            <p data-i18n="{key_d}"></p>
            <div class="vcard__meta"><span data-i18n="{cat_key}"></span><span>HD · 4K</span></div>
          </div>
        </article>
"""

# ============================== HOME ==============================
home = """
<!-- ===== Hero ===== -->
<section class="hero">
  <div class="hero__bg">
    <div class="hero__photo"></div>
    <div class="hero__rings"><i></i><i></i><i></i><i></i></div>
  </div>
  <div class="wrap hero__inner">
    <span class="eyebrow" data-i18n="hero.eyebrow" data-setting="hero_eyebrow"></span>
    <h1 class="hero__name">
      <span data-i18n="hero.n1">Suttipoj</span>
      <span><em data-i18n="hero.n2">Liang W.</em></span>
    </h1>
    <p class="hero__role" data-i18n="hero.role" data-setting="hero_role"></p>
    <p class="hero__text" data-i18n="hero.text" data-setting="hero_text"></p>
    <div class="hero__cta">
      <a href="/lesson" class="btn btn--gold" data-i18n="hero.cta1">Start learning</a>
      <a href="/lesson" class="btn btn--ghost" data-i18n="hero.cta2">Watch a free lesson</a>
    </div>
  </div>
  <span class="hero__scroll" data-i18n="hero.scroll">Scroll</span>
</section>

<!-- ===== Marquee ===== -->
<div class="marquee" aria-hidden="true">
  <div class="marquee__track">
    <span data-i18n="mq.1"></span><span data-i18n="mq.2"></span><span data-i18n="mq.3"></span>
    <span data-i18n="mq.4"></span><span data-i18n="mq.5"></span><span data-i18n="mq.6"></span>
    <span data-i18n="mq.1"></span><span data-i18n="mq.2"></span><span data-i18n="mq.3"></span>
    <span data-i18n="mq.4"></span><span data-i18n="mq.5"></span><span data-i18n="mq.6"></span>
  </div>
</div>

<!-- ===== Stats ===== -->
<section class="section">
  <div class="wrap">
    <div class="stats" data-reveal>
      <div class="stat"><b data-count="20" data-suffix="+">20+</b><small data-i18n="st.1"></small></div>
      <div class="stat"><b data-count="850" data-suffix="+">850+</b><small data-i18n="st.2"></small></div>
      <div class="stat"><b data-count="180" data-suffix="+">180+</b><small data-i18n="st.3"></small></div>
      <div class="stat"><b data-count="14" data-suffix="">14</b><small data-i18n="st.4"></small></div>
    </div>
  </div>
</section>

<!-- ===== Method ===== -->
<section class="section section--alt">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow" data-i18n="m.eyebrow"></span>
      <h2 class="section-title" data-i18n="m.title"></h2>
      <p class="lead" data-i18n="m.lead"></p>
    </div>
    <div class="grid grid--4">
      <article class="card" data-reveal><span class="card__num">01</span><h3 data-i18n="m.1t"></h3><p data-i18n="m.1d"></p></article>
      <article class="card" data-reveal><span class="card__num">02</span><h3 data-i18n="m.2t"></h3><p data-i18n="m.2d"></p></article>
      <article class="card" data-reveal><span class="card__num">03</span><h3 data-i18n="m.3t"></h3><p data-i18n="m.3d"></p></article>
      <article class="card" data-reveal><span class="card__num">04</span><h3 data-i18n="m.4t"></h3><p data-i18n="m.4d"></p></article>
    </div>
  </div>
</section>

<!-- ===== Latest videos ===== -->
<section class="section">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow" data-i18n="fl.eyebrow"></span>
      <h2 class="section-title" data-i18n="fl.title"></h2>
      <p class="lead" data-i18n="fl.lead"></p>
    </div>
    <div class="grid grid--3" id="db-featured">
""" + vcard("fl.1t","fl.1d","ls.lv2","18:24","groove intermediate","ls.f4") \
    + vcard("fl.2t","fl.2d","ls.lv2","12:40","technique intermediate","ls.f5") \
    + vcard("fl.3t","fl.3d","ls.lv3","24:05","groove advanced","ls.f4") + """    </div>
    <div class="center" style="margin-top:48px" data-reveal>
      <a href="/lesson" class="btn btn--ghost" data-i18n="fl.all">Browse all lessons</a>
    </div>
  </div>
</section>

<!-- ===== About preview ===== -->
<section class="section section--alt">
  <div class="wrap split">
    <div class="portrait" data-reveal>
      <!-- Drop a photo at assets/img/portrait.jpg and it replaces the monogram automatically -->
      <img class="portrait__img" src="assets/img/portrait.jpg" alt="Suttipoj Liang W." onerror="this.remove()">
      <span class="portrait__mono">SL</span>
      <span class="portrait__tag" data-i18n="ap.tag">Est. 2006</span>
    </div>
    <div data-reveal>
      <span class="eyebrow" data-i18n="ap.eyebrow"></span>
      <h2 class="section-title" data-i18n="ap.title"></h2>
      <p class="lead" style="margin-bottom:18px" data-i18n="ap.p1" data-setting="about_p1"></p>
      <p class="lead" style="margin-bottom:34px" data-i18n="ap.p2" data-setting="about_p2"></p>
      <a href="/profile" class="btn btn--ghost" data-i18n="ap.cta">Read the full profile</a>
    </div>
  </div>
</section>

<!-- ===== Testimonials ===== -->
<section class="section">
  <div class="wrap">
    <div class="head center" data-reveal>
      <span class="eyebrow" data-i18n="tm.eyebrow"></span>
      <h2 class="section-title" data-i18n="tm.title"></h2>
    </div>
    <div class="grid grid--3" id="db-quotes">
      <figure class="quote" data-reveal>
        <div class="quote__mark">&ldquo;</div><p data-i18n="tm.1"></p>
        <figcaption class="quote__by"><span class="quote__av">N</span>
          <span><b data-i18n="tm.1n"></b><small data-i18n="tm.1r"></small></span></figcaption>
      </figure>
      <figure class="quote" data-reveal>
        <div class="quote__mark">&ldquo;</div><p data-i18n="tm.2"></p>
        <figcaption class="quote__by"><span class="quote__av">M</span>
          <span><b data-i18n="tm.2n"></b><small data-i18n="tm.2r"></small></span></figcaption>
      </figure>
      <figure class="quote" data-reveal>
        <div class="quote__mark">&ldquo;</div><p data-i18n="tm.3"></p>
        <figcaption class="quote__by"><span class="quote__av">D</span>
          <span><b data-i18n="tm.3n"></b><small data-i18n="tm.3r"></small></span></figcaption>
      </figure>
    </div>
  </div>
</section>

<!-- ===== CTA ===== -->
<section class="section section--alt">
  <div class="wrap">
    <div class="cta" data-reveal>
      <span class="eyebrow" style="justify-content:center" data-i18n="cta.eyebrow"></span>
      <h2 data-i18n="cta.title"></h2>
      <p data-i18n="cta.text"></p>
      <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
        <a href="/contact" class="btn btn--gold" data-i18n="cta.btn1"></a>
        <a href="/lesson" class="btn btn--ghost" data-i18n="cta.btn2"></a>
      </div>
    </div>
  </div>
</section>
"""

page("index.html", dict(
    page="home",
    title="Suttipoj Liang W. — Drum Academy",
    title_en="Suttipoj Liang W. — Drum Academy",
    title_th="ครูเลี้ยง — โรงเรียนสอนกลอง",
    desc="Online drum lessons with Suttipoj Liang W. — structured paths, play-along tracks and personal video feedback. Bangkok, Thailand."
), home)

def phead(eyebrow, title, lead, crumb):
    return f"""
<section class="phead">
  <div class="wrap phead__in">
    <p class="crumb" data-i18n="{crumb}"></p>
    <span class="eyebrow" style="margin-top:16px" data-i18n="{eyebrow}"></span>
    <h1 data-i18n="{title}"></h1>
    <p class="lead" data-i18n="{lead}"></p>
  </div>
</section>
"""

# ============================== PROFILE ==============================
profile = phead("pf.eyebrow","pf.title","pf.lead","pf.crumb") + """
<section class="section">
  <div class="wrap split">
    <div class="portrait" data-reveal>
      <!-- Drop a photo at assets/img/portrait.jpg and it replaces the monogram automatically -->
      <img class="portrait__img" src="assets/img/portrait.jpg" alt="Suttipoj Liang W." onerror="this.remove()">
      <span class="portrait__mono">SL</span>
      <span class="portrait__tag" data-i18n="ap.tag">Est. 2006</span>
    </div>
    <div data-reveal>
      <span class="eyebrow" data-i18n="pf.eyebrow"></span>
      <h2 class="section-title" data-i18n="pf.b1t"></h2>
      <p class="lead" style="margin-bottom:18px" data-i18n="pf.b1" data-setting="profile_bio_1"></p>
      <p class="lead" style="margin-bottom:18px" data-i18n="pf.b2" data-setting="profile_bio_2"></p>
      <p class="lead" data-i18n="pf.b3" data-setting="profile_bio_3"></p>
    </div>
  </div>
</section>

<!-- ===== Timeline ===== -->
<section class="section section--alt">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow" data-i18n="pf.tl"></span>
      <h2 class="section-title" data-i18n="ap.title"></h2>
    </div>
    <div class="split" style="align-items:start">
      <div class="timeline" id="db-timeline" data-reveal>
        <div class="tl"><span class="tl__year" data-i18n="pf.t1y"></span><h4 data-i18n="pf.t1t"></h4><p data-i18n="pf.t1d"></p></div>
        <div class="tl"><span class="tl__year" data-i18n="pf.t2y"></span><h4 data-i18n="pf.t2t"></h4><p data-i18n="pf.t2d"></p></div>
        <div class="tl"><span class="tl__year" data-i18n="pf.t3y"></span><h4 data-i18n="pf.t3t"></h4><p data-i18n="pf.t3d"></p></div>
        <div class="tl"><span class="tl__year" data-i18n="pf.t4y"></span><h4 data-i18n="pf.t4t"></h4><p data-i18n="pf.t4d"></p></div>
        <div class="tl"><span class="tl__year" data-i18n="pf.t5y"></span><h4 data-i18n="pf.t5t"></h4><p data-i18n="pf.t5d"></p></div>
      </div>
      <div class="card" data-reveal>
        <span class="card__num" data-i18n="pf.gr"></span>
        <ul style="margin-top:18px;display:grid;gap:14px;color:var(--muted);font-size:15px">
          <li data-i18n="pf.g1"></li><li data-i18n="pf.g2"></li>
          <li data-i18n="pf.g3"></li><li data-i18n="pf.g4"></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- ===== Skills ===== -->
<section class="section">
  <div class="wrap">
    <div class="head center" data-reveal>
      <span class="eyebrow" data-i18n="pf.sk"></span>
      <h2 class="section-title" data-i18n="m.title"></h2>
    </div>
    <div class="grid grid--4">
      <article class="card" data-reveal><div class="card__icon">&#9834;</div><h3 data-i18n="pf.s1t"></h3><p data-i18n="pf.s1d"></p></article>
      <article class="card" data-reveal><div class="card__icon">&#9995;</div><h3 data-i18n="pf.s2t"></h3><p data-i18n="pf.s2d"></p></article>
      <article class="card" data-reveal><div class="card__icon">&#9836;</div><h3 data-i18n="pf.s3t"></h3><p data-i18n="pf.s3d"></p></article>
      <article class="card" data-reveal><div class="card__icon">&#9679;</div><h3 data-i18n="pf.s4t"></h3><p data-i18n="pf.s4d"></p></article>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="cta" data-reveal>
      <span class="eyebrow" style="justify-content:center" data-i18n="cta.eyebrow"></span>
      <h2 data-i18n="cta.title"></h2>
      <p data-i18n="cta.text"></p>
      <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
        <a href="/contact" class="btn btn--gold" data-i18n="cta.btn1"></a>
        <a href="/contact" class="btn btn--ghost" data-i18n="nav.cta"></a>
      </div>
    </div>
  </div>
</section>
"""

page("profile.html", dict(
    page="profile",
    title="Profile — Suttipoj Liang W.",
    title_en="Profile — Suttipoj Liang W.",
    title_th="ประวัติ — ครูเลี้ยง",
    desc="Suttipoj Liang W. — session drummer and educator in Bangkok. Twenty years of stages, studios and students."
), profile)

# ============================== LESSON ==============================
lesson = phead("ls.eyebrow","ls.title","ls.lead","ls.crumb") + """
<section class="section">
  <div class="wrap">
    <div class="filters" data-reveal>
      <button class="chip is-active" data-filter="all"          data-i18n="ls.f0"></button>
      <button class="chip" data-filter="beginner"     data-i18n="ls.f1"></button>
      <button class="chip" data-filter="intermediate" data-i18n="ls.f2"></button>
      <button class="chip" data-filter="advanced"     data-i18n="ls.f3"></button>
      <button class="chip" data-filter="groove"       data-i18n="ls.f4"></button>
      <button class="chip" data-filter="technique"    data-i18n="ls.f5"></button>
      <button class="chip" data-filter="reading"      data-i18n="ls.f6"></button>
    </div>
    <div class="grid grid--3" id="db-lessons">
""" + vcard("ls.v1t","ls.v1d","ls.lv1","14:52","beginner groove","ls.f4") \
    + vcard("ls.v2t","ls.v2d","ls.lv1","11:08","beginner technique","ls.f5") \
    + vcard("ls.v3t","ls.v3d","ls.lv1","16:30","beginner reading","ls.f6") \
    + vcard("ls.v4t","ls.v4d","ls.lv2","18:24","intermediate groove","ls.f4") \
    + vcard("ls.v5t","ls.v5d","ls.lv2","12:40","intermediate technique","ls.f5") \
    + vcard("ls.v6t","ls.v6d","ls.lv2","21:15","intermediate technique","ls.f5") \
    + vcard("ls.v7t","ls.v7d","ls.lv3","24:05","advanced groove","ls.f4") \
    + vcard("ls.v8t","ls.v8d","ls.lv3","19:47","advanced reading","ls.f6") \
    + vcard("ls.v9t","ls.v9d","ls.lv3","27:12","advanced groove","ls.f4") + """    </div>
  </div>
</section>

<!-- ===== The path ===== -->
<section class="section section--alt">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow" data-i18n="ls.path"></span>
      <h2 class="section-title" data-i18n="ls.pathlead"></h2>
    </div>
    <div class="grid grid--4">
      <article class="card" data-reveal><span class="card__num">STAGE 01</span><h3 data-i18n="ls.p1t"></h3><p data-i18n="ls.p1d"></p></article>
      <article class="card" data-reveal><span class="card__num">STAGE 02</span><h3 data-i18n="ls.p2t"></h3><p data-i18n="ls.p2d"></p></article>
      <article class="card" data-reveal><span class="card__num">STAGE 03</span><h3 data-i18n="ls.p3t"></h3><p data-i18n="ls.p3d"></p></article>
      <article class="card" data-reveal><span class="card__num">STAGE 04</span><h3 data-i18n="ls.p4t"></h3><p data-i18n="ls.p4d"></p></article>
    </div>
  </div>
</section>

<!-- ===== Private lesson promo ===== -->
<section class="section">
  <div class="wrap">
    <div class="head center" data-reveal>
      <span class="eyebrow" data-i18n="pm.eyebrow"></span>
      <h2 class="section-title" data-i18n="pm.title"></h2>
      <p class="lead" style="margin-inline:auto" data-i18n="pm.lead" data-setting="promo_lead"></p>
    </div>

    <div class="promo" id="db-packages" data-reveal>
      <div class="promo__row">
        <div class="promo__left">
          <b data-i18n="pm.r1n"></b>
          <small data-i18n="pm.r1s"></small>
        </div>
        <div class="promo__right">
          <span class="promo__price">1,000฿</span>
        </div>
      </div>

      <div class="promo__row">
        <div class="promo__left">
          <b data-i18n="pm.r2n"></b>
          <small data-i18n="pm.r2s"></small>
        </div>
        <div class="promo__right">
          <s class="promo__was">8,000฿</s>
          <span class="promo__price">7,600฿</span>
          <span class="promo__save" data-i18n="pm.save400"></span>
        </div>
      </div>

      <div class="promo__row promo__row--best">
        <span class="promo__badge" data-i18n="pm.best"></span>
        <div class="promo__left">
          <b data-i18n="pm.r3n"></b>
          <small data-i18n="pm.r3s"></small>
        </div>
        <div class="promo__right">
          <s class="promo__was">10,000฿</s>
          <span class="promo__price">9,000฿</span>
          <span class="promo__save" data-i18n="pm.save1000"></span>
        </div>
      </div>
    </div>

    <div class="center" style="margin-top:40px" data-reveal>
      <a href="/contact" class="btn btn--gold" data-i18n="pm.cta"></a>
      <p class="form-note" style="margin-top:18px" data-i18n="pm.note" data-setting="promo_note"></p>
    </div>
  </div>
</section>
"""

page("lesson.html", dict(
    page="lesson",
    title="Lessons — Suttipoj Liang W.",
    title_en="Lessons — Suttipoj Liang W.",
    title_th="บทเรียน — ครูเลี้ยง",
    desc="Over 180 online drum lessons organised into four structured stages, with play-along tracks and PDFs in Thai and English."
), lesson)

def faq(q, a):
    return f"""      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false"><span data-i18n="{q}"></span><i>+</i></button>
        <div class="faq__a"><p data-i18n="{a}"></p></div>
      </div>
"""

# ============================== CONTACT ==============================
contact = phead("ct.eyebrow","ct.title","ct.lead","ct.crumb") + """
<section class="section">
  <div class="wrap split" style="align-items:start">

    <form class="card" data-demo novalidate data-reveal style="padding:38px 34px">
      <span class="eyebrow" data-i18n="ct.eyebrow"></span>
      <h2 style="font-size:26px;margin:16px 0 28px" data-i18n="ct.send"></h2>

      <div class="field">
        <label for="c-name" data-i18n="ct.fname"></label>
        <input id="c-name" name="name" type="text" required data-i18n-ph="ct.ph.name">
      </div>
      <div class="field">
        <label for="c-mail" data-i18n="ct.femail"></label>
        <input id="c-mail" name="email" type="email" required data-i18n-ph="ct.ph.email">
      </div>
      <div class="field">
        <label for="c-topic" data-i18n="ct.ftopic"></label>
        <select id="c-topic" name="topic">
          <option data-i18n="ct.o1"></option><option data-i18n="ct.o2"></option>
          <option data-i18n="ct.o3"></option><option data-i18n="ct.o4"></option>
        </select>
      </div>
      <div class="field">
        <label for="c-level" data-i18n="ct.flevel"></label>
        <select id="c-level" name="level">
          <option data-i18n="ct.l1"></option><option data-i18n="ct.l2"></option>
          <option data-i18n="ct.l3"></option><option data-i18n="ct.l4"></option>
        </select>
      </div>
      <div class="field">
        <label for="c-msg" data-i18n="ct.fmsg"></label>
        <textarea id="c-msg" name="message" required data-i18n-ph="ct.ph.msg"></textarea>
      </div>

      <button type="submit" class="btn btn--gold btn--block" data-i18n="ct.send"></button>
      <p class="form-note" data-i18n="ct.note"></p>
      <p class="form-msg" data-i18n="ct.ok" role="status"></p>
    </form>

    <div data-reveal>
      <div class="info">
        <div class="info__row"><span class="info__ic">&#9993;</span>
          <span><small data-i18n="ct.i1"></small><b data-setting="contact_email">hello@suttipojdrums.com</b>
          <p data-setting="contact_phone">+66 2 000 0000</p></span></div>
        <div class="info__row"><span class="info__ic">&#9673;</span>
          <span><small data-i18n="ct.i2"></small><b data-i18n="ct.i2v" data-setting="contact_place"></b>
          <p data-i18n="ct.i2s"></p></span></div>
        <div class="info__row"><span class="info__ic">&#9200;</span>
          <span><small data-i18n="ct.i3"></small><b data-i18n="ct.i3v" data-setting="contact_hours"></b>
          <p data-i18n="ct.i3s"></p></span></div>
        <div class="info__row"><span class="info__ic">&#8618;</span>
          <span><small data-i18n="ct.i4"></small><b data-i18n="ct.i4v"></b>
          <p data-i18n="ct.i4s"></p></span></div>
      </div>

      <h3 style="font-size:24px;margin:52px 0 14px" data-i18n="ct.faq"></h3>
      <div class="faq" id="db-faq">
""" + faq("ct.q1","ct.a1") + faq("ct.q2","ct.a2") + faq("ct.q3","ct.a3") \
    + faq("ct.q4","ct.a4") + faq("ct.q5","ct.a5") + """      </div>
    </div>

  </div>
</section>
"""

page("contact.html", dict(
    page="contact",
    title="Contact — Suttipoj Liang W.",
    title_en="Contact — Suttipoj Liang W.",
    title_th="ติดต่อ — ครูเลี้ยง",
    desc="Contact Suttipoj Liang W. about drum memberships, private coaching or session work in Bangkok."
), contact)

# ============================== LOGIN ==============================
login = """
<section class="auth">
  <div class="wrap" style="display:grid;place-items:center">
    <div class="auth__card" data-reveal>

      <div class="auth__tabs" role="tablist">
        <button type="button" class="is-active" data-tab="login" data-i18n="lg.tab1"></button>
        <button type="button" data-tab="register" data-i18n="lg.tab2"></button>
      </div>

      <!-- ---- Sign in ---- -->
      <div data-pane="login">
        <h1 style="font-size:30px;margin-bottom:8px" data-i18n="lg.title"></h1>
        <p style="color:var(--muted);font-size:15px;margin-bottom:30px" data-i18n="lg.sub"></p>

        <form data-demo novalidate>
          <div class="field">
            <label for="l-mail" data-i18n="lg.email"></label>
            <input id="l-mail" type="email" autocomplete="email" data-i18n-ph="ct.ph.email">
          </div>
          <div class="field">
            <label for="l-pass" data-i18n="lg.pass"></label>
            <input id="l-pass" type="password" autocomplete="current-password" placeholder="••••••••">
          </div>
          <div class="auth__row">
            <label><input type="checkbox"> <span data-i18n="lg.remember"></span></label>
            <a href="#" data-i18n="lg.forgot"></a>
          </div>
          <button type="submit" class="btn btn--gold btn--block" data-i18n="lg.btn"></button>
          <p class="form-msg" data-i18n="lg.demo" role="status"></p>
        </form>

        <div class="auth__or"><span data-i18n="lg.or"></span></div>
        <div class="social">
          <button type="button"><span class="gold">G</span> <span data-i18n="lg.g"></span></button>
          <button type="button"><span class="gold">f</span> <span data-i18n="lg.f"></span></button>
        </div>
        <p class="auth__foot"><span data-i18n="lg.no"></span>
          <a href="#" class="gold" data-goto-tab="register" data-i18n="lg.sign"></a></p>
      </div>

      <!-- ---- Register ---- -->
      <div data-pane="register" hidden>
        <h1 style="font-size:30px;margin-bottom:8px" data-i18n="lg.title2"></h1>
        <p style="color:var(--muted);font-size:15px;margin-bottom:30px" data-i18n="lg.sub2"></p>

        <form data-demo novalidate>
          <div class="field">
            <label for="r-name" data-i18n="lg.name"></label>
            <input id="r-name" type="text" autocomplete="name" data-i18n-ph="ct.ph.name">
          </div>
          <div class="field">
            <label for="r-mail" data-i18n="lg.email"></label>
            <input id="r-mail" type="email" autocomplete="email" data-i18n-ph="ct.ph.email">
          </div>
          <div class="field">
            <label for="r-pass" data-i18n="lg.pass"></label>
            <input id="r-pass" type="password" autocomplete="new-password" placeholder="••••••••">
          </div>
          <div class="field">
            <label for="r-pass2" data-i18n="lg.pass2"></label>
            <input id="r-pass2" type="password" autocomplete="new-password" placeholder="••••••••">
          </div>
          <button type="submit" class="btn btn--gold btn--block" data-i18n="lg.btn2"></button>
          <p class="form-note" data-i18n="lg.terms"></p>
          <p class="form-msg" data-i18n="lg.demo" role="status"></p>
        </form>

        <p class="auth__foot"><span data-i18n="lg.yes"></span>
          <a href="#" class="gold" data-goto-tab="login" data-i18n="lg.in"></a></p>
      </div>

      <p class="auth__foot" style="margin-top:18px">
        <a href="/" style="color:var(--muted-2)" data-i18n="lg.back"></a></p>
    </div>
  </div>
</section>
"""

page("login.html", dict(
    page="login",
    title="Log in — Suttipoj Liang W.",
    title_en="Log in — Suttipoj Liang W.",
    title_th="เข้าสู่ระบบ — ครูเลี้ยง",
    desc="Log in to your Suttipoj Liang W. drum academy account, or create a free account."
), login, footer=False)

# ============================== 404 ==============================
notfound = """
<section class="hero" style="min-height:78svh">
  <div class="hero__bg"><div class="hero__rings"><i></i><i></i><i></i><i></i></div></div>
  <div class="wrap hero__inner" style="text-align:center;max-width:640px;margin-inline:auto">
    <span class="eyebrow" style="justify-content:center" data-i18n="nf.code"></span>
    <h1 class="hero__name" style="font-size:clamp(34px,6vw,72px);margin:20px 0 22px">
      <em data-i18n="nf.title"></em>
    </h1>
    <p class="lead" style="margin:0 auto 36px" data-i18n="nf.text"></p>
    <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
      <a href="/" class="btn btn--gold" data-i18n="nf.home"></a>
      <a href="/lesson" class="btn btn--ghost" data-i18n="nf.lessons"></a>
    </div>
  </div>
</section>
"""

page("404.html", dict(
    page="404",
    title="404 — Suttipoj Liang W.",
    title_en="404 — Suttipoj Liang W.",
    title_th="ไม่พบหน้านี้ — ครูเลี้ยง",
    desc="Page not found."
), notfound)
