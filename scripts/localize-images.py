#!/usr/bin/env python3
"""Phase 2 (item 9): download external images into images/ and repoint references.

- Downloads every https://storage.googleapis.com/a1aa/image/... URL used on the site
  into images/ (filename = original basename).
- Writes images/manifest.json mapping original URL -> local file (the record, so the
  source URLs are never lost).
- Rewrites each HTML page so <img src>, JS strings, etc. use images/<basename>.
- Keeps og:image / twitter:image meta values as absolute URLs (social platforms
  require absolute URLs).
- Fixes src="/images/jane.jpg" -> src="images/jane.jpg" (relative, deploy-safe).
- Moves the accidental "images /12.jpg" (trailing-space folder) into images/12.jpg.

Additive only: no page content is removed, images are identical, just local.
Idempotent: safe to re-run.
"""
import glob
import json
import os
import re
import sys
import urllib.request

BASE = "https://storage.googleapis.com/a1aa/image/"
IMG_DIR = "images"
MANIFEST = os.path.join(IMG_DIR, "manifest.json")

URL_RE = re.compile(r"https://storage\.googleapis\.com/a1aa/image/[A-Za-z0-9._-]+")


def collect_urls():
    urls = set()
    for f in glob.glob("*.html"):
        for m in URL_RE.finditer(open(f, encoding="utf-8").read()):
            urls.add(m.group(0))
    return sorted(urls)


def download(url):
    name = url[len(BASE):]
    dest = os.path.join(IMG_DIR, name)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest, "cached"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (site-image-upgrade)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        with open(dest, "wb") as f:
            f.write(data)
        return dest, f"ok ({len(data)} bytes)"
    except Exception as e:
        return dest, f"FAILED: {e}"


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    urls = collect_urls()
    print(f"found {len(urls)} unique external image URLs")

    # 1. download
    manifest = {}
    failures = []
    for url in urls:
        dest, status = download(url)
        manifest[url] = dest
        if status.startswith("FAILED"):
            failures.append((url, status))
        print(f"  {status:>12}  {dest}")
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    print(f"manifest written: {MANIFEST}")
    if failures:
        print("WARNING: some downloads failed:")
        for u, s in failures:
            print("  ", u, s)
        sys.exit(1)

    # 2. rewrite pages (site pages + shared templates so they stay in sync)
    for fname in sorted(glob.glob("*.html") + glob.glob("templates/*.html")):
        with open(fname, encoding="utf-8") as f:
            html = f.read()

        # protect og:image / twitter:image values (must stay absolute)
        protected = {}
        def protect(m):
            key = f"__OG_URL_{len(protected)}__"
            protected[key] = m.group(0)
            return key
        html = re.sub(r'(content=")(https://storage\.googleapis\.com/a1aa/image/[A-Za-z0-9._-]+)(")',
                      lambda m: m.group(1) + protect(m.group(2)) + m.group(3), html)

        # localize every other occurrence
        html = URL_RE.sub(lambda m: "images/" + m.group(0)[len(BASE):], html)

        # restore protected absolute URLs
        for key, val in protected.items():
            html = html.replace(key, val)

        # absolute -> relative local path
        html = html.replace('src="/images/', 'src="images/')

        with open(fname, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"rewrote {fname} ({len(protected)} og/twitter URLs kept absolute)")

    # 3. consolidate the accidental trailing-space folder
    odd = IMG_DIR + " "
    odd_file = os.path.join(odd, "12.jpg")
    if os.path.exists(odd_file):
        dest12 = os.path.join(IMG_DIR, "12.jpg")
        if not os.path.exists(dest12):
            os.replace(odd_file, dest12)
            print(f"moved {odd_file} -> {dest12}")
        # remove now-empty accidental folder
        try:
            os.rmdir(odd)
            print(f"removed empty accidental folder {odd!r}")
        except OSError as e:
            print(f"note: could not remove {odd!r}: {e}")
    print("done.")


if __name__ == "__main__":
    main()
