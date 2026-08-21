/* ============================================================
   Hydrates the public pages from Supabase.
   If the database is unreachable or empty, the HTML that shipped
   with the page is left exactly as it is — the site never breaks.
   ============================================================ */
(function () {
  "use strict";
  if (!window.DB || !window.DB.ready) return;

  var EN = (window.I18N && window.I18N.en) || {};
  var TH = (window.I18N && window.I18N.th) || {};

  var LEVEL_KEY = { beginner: "ls.lv1", intermediate: "ls.lv2", advanced: "ls.lv3" };
  var CAT_KEY = { groove: "ls.f4", technique: "ls.f5", reading: "ls.f6" };

  /* ---------- tiny DOM helpers ---------- */
  function el(tag, cls, attrs) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    for (var k in attrs || {}) if (attrs[k] !== null && attrs[k] !== undefined) n.setAttribute(k, attrs[k]);
    return n;
  }
  /** element whose text follows the language switch */
  function bi(tag, cls, en, th) {
    var n = el(tag, cls, { "data-txt-en": en || "", "data-txt-th": th || en || "" });
    n.textContent = en || "";
    return n;
  }
  function dict(tag, cls, key) {
    return bi(tag, cls, EN[key] || "", TH[key] || "");
  }
  function txt(tag, cls, s) {
    var n = el(tag, cls);
    n.textContent = s == null ? "" : s;
    return n;
  }
  function relang() { if (typeof window.applyLang === "function") window.applyLang(); }

  var PLAY_SVG = '<svg width="15" height="17" viewBox="0 0 15 17" fill="currentColor" aria-hidden="true">' +
    '<path d="M14 7.63a1 1 0 0 1 0 1.74l-12 6.8A1 1 0 0 1 .5 15.3V1.7A1 1 0 0 1 2 .83l12 6.8Z"/></svg>';

  /* ---------- renderers ---------- */
  function lessonCard(row) {
    var card = el("article", "vcard", {
      "data-tags": (row.category || "") + " " + (row.level || ""),
      "data-reveal": ""
    });

    var playable = window.DB.isPlayable(row.video_url);
    var thumb;
    if (playable) {
      thumb = el("button", "vcard__thumb", { type: "button" });
      thumb.addEventListener("click", function () { openPlayer(row.video_url, row); });
    } else if (row.video_url) {
      thumb = el("a", "vcard__thumb", { href: row.video_url, target: "_blank", rel: "noopener" });
    } else {
      thumb = el("div", "vcard__thumb");
    }
    thumb.appendChild(dict("span", "vcard__lvl", LEVEL_KEY[row.level] || "ls.lv1"));
    var play = el("span", "vcard__play");
    play.innerHTML = PLAY_SVG;
    thumb.appendChild(play);
    if (row.duration) thumb.appendChild(txt("span", "vcard__len", row.duration));
    card.appendChild(thumb);

    var body = el("div", "vcard__body");
    body.appendChild(bi("h3", null, row.title_en, row.title_th));
    body.appendChild(bi("p", null, row.desc_en, row.desc_th));
    var meta = el("div", "vcard__meta");
    meta.appendChild(dict("span", null, CAT_KEY[row.category] || "ls.f4"));
    meta.appendChild(txt("span", null, "HD · 4K"));
    body.appendChild(meta);
    card.appendChild(body);

    card.classList.add("is-in");
    return card;
  }

  function packageRow(row) {
    var r = el("div", "promo__row" + (row.is_best ? " promo__row--best" : ""));
    if (row.is_best) r.appendChild(dict("span", "promo__badge", "pm.best"));

    var left = el("div", "promo__left");
    left.appendChild(txt("b", null, row.name));
    left.appendChild(bi("small", null, row.sub_en, row.sub_th));
    r.appendChild(left);

    var right = el("div", "promo__right");
    if (row.price_was) right.appendChild(txt("s", "promo__was", row.price_was));
    right.appendChild(txt("span", "promo__price", row.price));
    if (row.save_en || row.save_th) right.appendChild(bi("span", "promo__save", row.save_en, row.save_th));
    r.appendChild(right);
    return r;
  }

  function faqItem(row) {
    var item = el("div", "faq__item");
    var q = el("button", "faq__q", { type: "button", "aria-expanded": "false" });
    q.appendChild(bi("span", null, row.q_en, row.q_th));
    var plus = el("i"); plus.textContent = "+";
    q.appendChild(plus);
    item.appendChild(q);
    var a = el("div", "faq__a");
    a.appendChild(bi("p", null, row.a_en, row.a_th));
    item.appendChild(a);
    return item;
  }

  function quoteCard(row) {
    var fig = el("figure", "quote");
    var mark = el("div", "quote__mark"); mark.innerHTML = "&ldquo;";
    fig.appendChild(mark);
    fig.appendChild(bi("p", null, row.quote_en, row.quote_th));

    var cap = el("figcaption", "quote__by");
    cap.appendChild(txt("span", "quote__av", (row.person || "?").trim().charAt(0).toUpperCase()));
    var who = el("span");
    who.appendChild(txt("b", null, row.person));
    who.appendChild(bi("small", null, row.role_en, row.role_th));
    cap.appendChild(who);
    fig.appendChild(cap);
    fig.classList.add("is-in");
    return fig;
  }

  function timelineItem(row) {
    var d = el("div", "tl");
    d.appendChild(txt("span", "tl__year", row.year));
    d.appendChild(bi("h4", null, row.title_en, row.title_th));
    d.appendChild(bi("p", null, row.desc_en, row.desc_th));
    return d;
  }

  /* ---------- lightbox player for uploaded videos ---------- */
  var player = null;
  function openPlayer(src, row) {
    if (!player) {
      player = el("div", "player");
      var inner = el("div", "player__box");
      var close = el("button", "player__x", { type: "button", "aria-label": "ปิด" });
      close.textContent = "×";
      var vid = el("video", null, { controls: "", playsinline: "" });
      var cap = el("p", "player__cap");
      inner.appendChild(close);
      inner.appendChild(vid);
      inner.appendChild(cap);
      player.appendChild(inner);
      document.body.appendChild(player);

      function shut() {
        vid.pause();
        vid.removeAttribute("src");
        vid.load();
        player.classList.remove("is-on");
        document.body.style.overflow = "";
      }
      close.addEventListener("click", shut);
      player.addEventListener("click", function (e) { if (e.target === player) shut(); });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && player.classList.contains("is-on")) shut();
      });
      player._video = vid;
      player._cap = cap;
    }
    player._video.src = src;
    var title = row ? (document.documentElement.lang === "th" ? row.title_th : row.title_en) : "";
    player._cap.textContent = title || "";
    player.classList.add("is-on");
    document.body.style.overflow = "hidden";
    player._video.play().catch(function () {});
  }

  /* ---------- fill a container, only when there is something to show ---------- */
  function fill(id, rows, render, limit) {
    var box = document.getElementById(id);
    if (!box || !rows || !rows.length) return;
    var list = limit ? rows.slice(0, limit) : rows;
    box.textContent = "";
    list.forEach(function (row) { box.appendChild(render(row)); });
  }

  function applySettings(rows) {
    if (!rows || !rows.length) return;
    var map = {};
    rows.forEach(function (r) { map[r.key] = r; });
    document.querySelectorAll("[data-setting]").forEach(function (node) {
      var row = map[node.getAttribute("data-setting")];
      if (!row) return;
      node.removeAttribute("data-i18n");           // database wins over the dictionary
      node.setAttribute("data-txt-en", row.value_en || "");
      node.setAttribute("data-txt-th", row.value_th || row.value_en || "");
      if (node.tagName === "A") {
        var href = node.getAttribute("href") || "";
        if (href.indexOf("mailto:") === 0) node.setAttribute("href", "mailto:" + (row.value_en || ""));
        if (href.indexOf("tel:") === 0) node.setAttribute("href", "tel:" + (row.value_en || "").replace(/[^\d+]/g, ""));
      }
    });
  }

  /* ---------- boot ---------- */
  var need = {
    "db-lessons":  "site_lessons",
    "db-featured": "site_lessons",
    "db-packages": "site_packages",
    "db-faq":      "site_faq",
    "db-quotes":   "site_testimonials",
    "db-timeline": "site_timeline"
  };
  var tables = {};
  Object.keys(need).forEach(function (id) {
    if (document.getElementById(id)) tables[need[id]] = true;
  });
  var wantSettings = !!document.querySelector("[data-setting]");
  if (!Object.keys(tables).length && !wantSettings) return;

  var jobs = Object.keys(tables).map(function (t) {
    return window.DB.select(t, "select=*&published=eq.true&order=sort.asc")
      .then(function (rows) { return [t, rows]; })
      .catch(function () { return [t, null]; });
  });
  if (wantSettings) {
    jobs.push(window.DB.select("site_settings", "select=*")
      .then(function (rows) { return ["site_settings", rows]; })
      .catch(function () { return ["site_settings", null]; }));
  }

  Promise.all(jobs).then(function (pairs) {
    var data = {};
    pairs.forEach(function (p) { data[p[0]] = p[1]; });

    fill("db-lessons", data.site_lessons, lessonCard);
    fill("db-featured", data.site_lessons, lessonCard, 3);
    fill("db-packages", data.site_packages, packageRow);
    fill("db-faq", data.site_faq, faqItem);
    fill("db-quotes", data.site_testimonials, quoteCard);
    fill("db-timeline", data.site_timeline, timelineItem);
    applySettings(data.site_settings);
    relang();
  });
})();
