/* Service worker (Phase 4, item 20): offline support + app installability.
   Cache-first for same-origin GET requests; navigation falls back to the cached
   home page when offline. Safe by design: cross-origin requests are untouched. */
"use strict";

var CACHE = "mama-fua-v1";
var CORE = [
  "./",
  "./index.html",
  "./css/tailwind.css",
  "./js/main.js",
  "./sw.js",
  "./favicon.svg",
  "./apple-touch-icon.png",
  "./manifest.json",
  "./images/icon-192.png",
  "./images/icon-512.png"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return cache.addAll(CORE);
    }).then(function () {
      return self.skipWaiting();
    }).catch(function () {
      // individual core items may fail (e.g. missing page); activation can still proceed
      return self.skipWaiting();
    })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.filter(function (k) { return k !== CACHE; })
            .map(function (k) { return caches.delete(k); })
      );
    }).then(function () {
      return self.clients.claim();
    })
  );
});

self.addEventListener("fetch", function (event) {
  var req = event.request;
  if (req.method !== "GET") return;
  var url = new URL(req.url);
  if (url.origin !== location.origin) return; // never intercept cross-origin

  event.respondWith(
    caches.match(req).then(function (hit) {
      if (hit) return hit;
      return fetch(req).then(function (res) {
        if (res && res.status === 200 && res.type === "basic") {
          var copy = res.clone();
          caches.open(CACHE).then(function (cache) { cache.put(req, copy); });
        }
        return res;
      }).catch(function () {
        // offline: serve cached home page for navigations
        if (req.mode === "navigate") return caches.match("./index.html");
        return Response.error();
      });
    })
  );
});
