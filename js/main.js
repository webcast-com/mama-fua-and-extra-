/* Shared site behaviour (Phase 1 + Phase 3):
   1. Mobile hamburger menu toggle
   2. Auto-updating copyright year (elements with data-year)
   3. Floating WhatsApp button (all pages)
   4. Image lightbox (elements with data-lightbox)
   5. Dark mode toggle (data-dark-toggle) with localStorage + injected CSS
   6. Booking/contact form -> prefilled WhatsApp message (contact.html)
   7. Booking estimate calculator (contact.html)
   8. Blog search + category filter (more blog.html)
   No existing behaviour is modified — these only add functionality. */
(function () {
  "use strict";

  var WHATSAPP_NUMBER = "254700123456"; // site's WhatsApp number (digits only)

  function setMenuState(menu, open) {
    if (!menu) return;
    menu.classList.toggle("hidden", !open);
    var btn = document.querySelector('[data-nav-toggle="#' + menu.id + '"]');
    if (!btn) return;
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    var barsIcon = btn.querySelector(".fa-bars");
    var timesIcon = btn.querySelector(".fa-times");
    if (barsIcon) barsIcon.classList.toggle("hidden", open);
    if (timesIcon) timesIcon.classList.toggle("hidden", !open);
  }

  function initMobileMenu() {
    document.querySelectorAll("[data-nav-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var menu = document.querySelector(btn.getAttribute("data-nav-toggle"));
        setMenuState(menu, menu.classList.contains("hidden"));
      });
    });

    // Close the menu when any link inside it is tapped.
    document.querySelectorAll("[data-nav-menu] a").forEach(function (link) {
      link.addEventListener("click", function () {
        setMenuState(link.closest("[data-nav-menu]"), false);
      });
    });
  }

  function initYear() {
    var currentYear = String(new Date().getFullYear());
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = currentYear;
    });
  }

  /* ---------- 3. Floating WhatsApp button ---------- */
  function initWhatsAppFloat() {
    if (document.getElementById("whatsapp-float")) return;
    var a = document.createElement("a");
    a.id = "whatsapp-float";
    a.href = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" +
      encodeURIComponent("Hello Nairobi Cleaning! I'd like to book a cleaning service.");
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.setAttribute("aria-label", "Chat with us on WhatsApp");
    a.style.cssText =
      "position:fixed;bottom:20px;right:20px;z-index:9999;background:#25d366;color:#fff;" +
      "width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;" +
      "box-shadow:0 4px 12px rgba(0,0,0,.3);font-size:28px;transition:transform .15s;";
    a.onmouseenter = function () { a.style.transform = "scale(1.08)"; };
    a.onmouseleave = function () { a.style.transform = "scale(1)"; };
    a.innerHTML = '<i class="fab fa-whatsapp"></i>';
    document.body.appendChild(a);
  }

  /* ---------- 4. Lightbox ---------- */
  function initLightbox() {
    if (document.getElementById("lightbox-overlay")) return;
    var overlay = document.createElement("div");
    overlay.id = "lightbox-overlay";
    overlay.style.cssText =
      "position:fixed;inset:0;background:rgba(0,0,0,.88);z-index:10000;display:none;" +
      "align-items:center;justify-content:center;cursor:zoom-out;";
    var img = document.createElement("img");
    img.id = "lightbox-img";
    img.style.cssText =
      "max-width:92vw;max-height:88vh;border-radius:8px;box-shadow:0 10px 40px rgba(0,0,0,.6);";
    var closeBtn = document.createElement("button");
    closeBtn.setAttribute("aria-label", "Close image");
    closeBtn.style.cssText =
      "position:absolute;top:16px;right:24px;background:transparent;border:none;color:#fff;" +
      "font-size:36px;cursor:pointer;line-height:1;";
    closeBtn.innerHTML = "&times;";
    overlay.appendChild(img);
    overlay.appendChild(closeBtn);
    document.body.appendChild(overlay);

    function open(src, alt) {
      img.src = src;
      img.alt = alt || "";
      overlay.style.display = "flex";
    }
    function close() {
      overlay.style.display = "none";
      img.src = "";
    }
    document.addEventListener("click", function (e) {
      var target = e.target.closest ? e.target.closest("[data-lightbox]") : null;
      if (target) {
        e.preventDefault();
        open(target.src || target.getAttribute("src"), target.alt || "");
      } else if (overlay.style.display === "flex" && e.target !== img) {
        close();
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  /* ---------- 5. Dark mode ---------- */
  function darkModeCss() {
    return (
      "html.dark{color-scheme:dark}" +
      "html.dark body{background:#0f172a!important}" +
      "html.dark .bg-gradient-to-r.from-green-200.via-cyan-200.to-blue-300," +
      "html.dark .bg-gradient-to-tr.from-yellow-200.via-green-200.to-blue-300" +
      "{background:linear-gradient(to bottom right,#0f172a,#1e293b)!important}" +
      "html.dark main[style*='radial-gradient']{background:radial-gradient(circle at top left,#1e1b4b,#312e81 55%,#1e293b 90%)!important}" +
      "html.dark .bg-white{background-color:#1e293b!important}" +
      "html.dark .text-gray-900{color:#f1f5f9!important}" +
      "html.dark .text-gray-800{color:#e2e8f0!important}" +
      "html.dark .text-gray-700{color:#cbd5e1!important}" +
      "html.dark .text-gray-600{color:#94a3b8!important}" +
      "html.dark .border-gray-200{border-color:#334155!important}"
    );
  }

  function initDarkMode() {
    var style = document.createElement("style");
    style.id = "dark-mode-css";
    style.textContent = darkModeCss();
    document.head.appendChild(style);

    var root = document.documentElement;
    var stored = null;
    try { stored = localStorage.getItem("ui-theme"); } catch (e) { /* ignore */ }
    if (stored === "dark" ||
        (stored === null && window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
      root.classList.add("dark");
    }
    document.querySelectorAll("[data-dark-toggle]").forEach(function (btn) {
      function syncIcons() {
        var moon = btn.querySelector(".fa-moon");
        var sun = btn.querySelector(".fa-sun");
        if (moon) moon.classList.toggle("hidden", root.classList.contains("dark"));
        if (sun) sun.classList.toggle("hidden", !root.classList.contains("dark"));
      }
      syncIcons();
      btn.addEventListener("click", function () {
        root.classList.toggle("dark");
        try { localStorage.setItem("ui-theme", root.classList.contains("dark") ? "dark" : "light"); } catch (e) { /* ignore */ }
        syncIcons();
      });
    });
  }

  /* ---------- 6. Booking form -> WhatsApp ---------- */
  function initBookingForm() {
    var form = document.getElementById("bookingForm");
    if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = (document.getElementById("bkName").value || "").trim();
      var phone = (document.getElementById("bkPhone").value || "").trim();
      var service = document.getElementById("bkService").value;
      var date = document.getElementById("bkDate").value || "as soon as possible";
      var msg = document.getElementById("bkMessage").value.trim();
      var text = "Hello Nairobi Cleaning! I'd like to book a cleaning service.\n" +
        "Name: " + name + "\n" +
        "Phone: " + phone + "\n" +
        "Service: " + service + "\n" +
        "Preferred date: " + date;
      if (msg) text += "\nDetails: " + msg;
      window.open("https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(text), "_blank");
    });
  }

  /* ---------- 7. Estimate calculator ---------- */
  function initEstimator() {
    var form = document.getElementById("estimateForm");
    if (!form) return;
    var base = { studio: 1500, "1br": 2000, "2br": 3000, "3br": 4000, "4br": 5000 };
    var freqMultiplier = { once: 1, weekly: 3.0, biweekly: 2.0, monthly: 1.0 };
    var freqDiscount = { weekly: 0.25, biweekly: 0.15, monthly: 0.1 };
    var extras = { deep: 1500, carpet: 1000, windows: 800, fridge: 600 };
    var out = document.getElementById("estimateResult");
    var amount = document.getElementById("estimateAmount");

    function update() {
      var size = document.getElementById("estSize").value;
      var freq = document.getElementById("estFreq").value;
      var ksh = base[size] || 2000;
      ksh *= freqMultiplier[freq] || 1;
      if (freq !== "once") ksh *= (1 - (freqDiscount[freq] || 0));
      Object.keys(extras).forEach(function (k) {
        var cb = document.getElementById("est" + k.charAt(0).toUpperCase() + k.slice(1));
        if (cb && cb.checked) ksh += extras[k];
      });
      var rounded = Math.round(ksh / 100) * 100;
      amount.textContent = "KSh " + rounded.toLocaleString("en-KE");
      out.classList.remove("hidden");
    }
    form.addEventListener("input", update);
    form.addEventListener("change", update);

    var bookBtn = document.getElementById("estimateBook");
    if (bookBtn) {
      bookBtn.addEventListener("click", function () {
        var size = document.getElementById("estSize");
        var freq = document.getElementById("estFreq");
        var text = "Hello Nairobi Cleaning! I'd like an estimate for cleaning.\n" +
          "Home size: " + size.options[size.selectedIndex].text + "\n" +
          "Frequency: " + freq.options[freq.selectedIndex].text + "\n" +
          "Estimated price: " + amount.textContent;
        window.open("https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(text), "_blank");
      });
    }
  }

  /* ---------- 8. Blog search + filter ---------- */
  function initBlogFilter() {
    var search = document.getElementById("blogSearch");
    if (!search) return;
    var chips = document.querySelectorAll("[data-category-chip]");
    var items = document.querySelectorAll("[data-category]");
    var empty = document.getElementById("blogNoResults");
    var activeCat = "all";

    function apply() {
      var q = search.value.trim().toLowerCase();
      var visible = 0;
      items.forEach(function (item) {
        var cat = item.getAttribute("data-category") || "other";
        var text = (item.textContent || "").toLowerCase();
        var matchCat = activeCat === "all" || cat === activeCat;
        var matchQ = q === "" || text.indexOf(q) !== -1;
        var show = matchCat && matchQ;
        item.style.display = show ? "" : "none";
        if (show) visible++;
      });
      if (empty) empty.style.display = visible ? "none" : "block";
    }
    search.addEventListener("input", apply);
    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        activeCat = chip.getAttribute("data-category-chip");
        chips.forEach(function (c) {
          c.classList.toggle("bg-green-600", c === chip);
          c.classList.toggle("text-white", c === chip);
          c.classList.toggle("bg-white", c !== chip);
          c.classList.toggle("text-gray-700", c !== chip);
        });
        apply();
      });
    });
    apply();
  }

  /* ---------- init ---------- */
  function init() {
    initMobileMenu();
    initYear();
    initWhatsAppFloat();
    initLightbox();
    initDarkMode();
    initBookingForm();
    initEstimator();
    initBlogFilter();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
