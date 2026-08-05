/* Shared site behaviour (Phase 1):
   1. Mobile hamburger menu toggle
   2. Auto-updating copyright year (elements with data-year)
   No existing behaviour is modified — this only adds functionality. */
(function () {
  "use strict";

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

  document.addEventListener("DOMContentLoaded", function () {
    initMobileMenu();
    initYear();
  });
})();
