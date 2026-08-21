/* ============================================================
   Site behaviour: language, nav, reveal, filters, FAQ, forms
   ============================================================ */
(function () {
  "use strict";

  /* ---------- Language ---------- */
  var STORE = "slw-lang";
  var lang = localStorage.getItem(STORE) ||
    ((navigator.language || "en").toLowerCase().indexOf("th") === 0 ? "th" : "en");
  if (lang !== "th" && lang !== "en") lang = "en";

  function t(key) {
    var dict = window.I18N[lang] || window.I18N.en;
    return dict[key] !== undefined ? dict[key] : (window.I18N.en[key] !== undefined ? window.I18N.en[key] : key);
  }

  function applyLang(next) {
    lang = next;
    localStorage.setItem(STORE, lang);
    document.documentElement.setAttribute("lang", lang);

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      el.textContent = t(el.getAttribute("data-i18n"));
    });
    document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      el.innerHTML = t(el.getAttribute("data-i18n-html"));
    });
    document.querySelectorAll("[data-i18n-ph]").forEach(function (el) {
      el.setAttribute("placeholder", t(el.getAttribute("data-i18n-ph")));
    });
    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
      el.setAttribute("aria-label", t(el.getAttribute("data-i18n-aria")));
    });
    // content that came from the database carries its own two languages
    document.querySelectorAll("[data-txt-en]").forEach(function (el) {
      var v = el.getAttribute("data-txt-" + lang);
      el.textContent = v === null ? el.getAttribute("data-txt-en") : v;
    });

    // page <title>
    var b = document.body;
    var title = b.getAttribute("data-title-" + lang);
    if (title) document.title = title;

    // language buttons
    document.querySelectorAll("[data-lang]").forEach(function (btn) {
      btn.classList.toggle("is-active", btn.getAttribute("data-lang") === lang);
      btn.setAttribute("aria-pressed", btn.getAttribute("data-lang") === lang);
    });

    // re-measure any open accordion
    document.querySelectorAll(".faq__item.is-open .faq__a").forEach(function (a) {
      a.style.maxHeight = a.scrollHeight + "px";
    });
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-lang]");
    if (btn) applyLang(btn.getAttribute("data-lang"));
  });

  /* ---------- Header: sticky state + mobile menu ---------- */
  var header = document.querySelector(".header");
  var menu = document.querySelector(".menu");
  var burger = document.querySelector(".burger");

  function onScroll() {
    if (header) header.classList.toggle("is-stuck", window.scrollY > 24);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (burger && menu) {
    burger.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      burger.classList.toggle("is-open", open);
      burger.setAttribute("aria-expanded", open);
      document.body.style.overflow = open ? "hidden" : "";
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        menu.classList.remove("is-open");
        burger.classList.remove("is-open");
        document.body.style.overflow = "";
      });
    });
  }

  // mark active nav item
  var page = document.body.getAttribute("data-page");
  document.querySelectorAll(".menu a[data-nav]").forEach(function (a) {
    if (a.getAttribute("data-nav") === page) a.classList.add("is-active");
  });

  /* ---------- Reveal on scroll ---------- */
  var reveals = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("is-in");
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -60px" });
    reveals.forEach(function (el, i) {
      el.style.transitionDelay = (Math.min(i % 4, 3) * 90) + "ms";
      io.observe(el);
    });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- Counters ---------- */
  var counters = document.querySelectorAll("[data-count]");
  if (counters.length && "IntersectionObserver" in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        co.unobserve(el);
        var target = parseFloat(el.getAttribute("data-count"));
        var suffix = el.getAttribute("data-suffix") || "";
        var start = performance.now(), dur = 1400;
        (function step(now) {
          var p = Math.min((now - start) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * eased).toLocaleString() + (p === 1 ? suffix : "");
          if (p < 1) requestAnimationFrame(step);
        })(start);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { co.observe(el); });
  }

  /* ---------- Lesson filters ---------- */
  var chips = document.querySelectorAll(".chip[data-filter]");
  if (chips.length) {
    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        chips.forEach(function (c) { c.classList.remove("is-active"); });
        chip.classList.add("is-active");
        var f = chip.getAttribute("data-filter");
        document.querySelectorAll("[data-tags]").forEach(function (card) {
          var show = f === "all" || card.getAttribute("data-tags").split(" ").indexOf(f) > -1;
          card.style.display = show ? "" : "none";
        });
      });
    });
  }

  /* ---------- FAQ accordion (delegated: works for rows added later) ---------- */
  document.addEventListener("click", function (e) {
    var q = e.target.closest(".faq__q");
    if (!q) return;
    var item = q.closest(".faq__item");
    var panel = item.querySelector(".faq__a");
    var open = item.classList.toggle("is-open");
    q.setAttribute("aria-expanded", open);
    panel.style.maxHeight = open ? panel.scrollHeight + "px" : 0;
  });

  /* ---------- Demo forms ---------- */
  document.querySelectorAll("form[data-demo]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = form.querySelector(".form-msg");
      if (msg) {
        msg.classList.add("is-on");
        msg.textContent = t(msg.getAttribute("data-i18n"));
        msg.scrollIntoView({ behavior: "smooth", block: "center" });
      }
      form.reset();
    });
  });

  /* ---------- Login / register tabs ---------- */
  var tabs = document.querySelectorAll("[data-tab]");
  if (tabs.length) {
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        var name = tab.getAttribute("data-tab");
        tabs.forEach(function (x) { x.classList.toggle("is-active", x === tab); });
        document.querySelectorAll("[data-pane]").forEach(function (p) {
          p.hidden = p.getAttribute("data-pane") !== name;
        });
      });
    });
    document.querySelectorAll("[data-goto-tab]").forEach(function (link) {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        var target = document.querySelector('[data-tab="' + link.getAttribute("data-goto-tab") + '"]');
        if (target) target.click();
      });
    });
  }

  /* ---------- Boot ---------- */
  window.applyLang = function (next) { applyLang(next || lang); };
  applyLang(lang);
})();
