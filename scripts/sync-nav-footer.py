#!/usr/bin/env python3
"""Phase 2 (item 8): sync shared nav + footer templates into every page.

The templates in templates/ are the single source of truth for the site's
navigation bars and footers. This script replaces each page's <nav>/<header>
and <footer> regions with the rendered template, so a future edit happens in
one place (the template) and one command (this script) updates every page.

Additive only: markup is replaced with identical content (plus two small
upgrades: real hrefs instead of "#" for the current page, and aria-current
markers). Nothing is deleted. Idempotent: safe to re-run.
"""
import os
import re

TPL = "templates"

# template key -> filename
NAV_FILES = {
    "cleaning": "cleaning-nav.html",
    "music": "music-nav.html",
    "gallery": "gallery-nav.html",
    "blog": "blog-nav.html",
}
FOOT_FILES = {
    "cleaning": "cleaning-footer.html",
    "simple": "simple-footer.html",
}

# page -> config
#   nav:      NAV_FILES key or None (page has no navbar)
#   footer:   FOOT_FILES key
#   params:   substitutions for {{PLACEHOLDERS}}
#   current:  for classic navs - the page's own filename, gets aria-current="page"
PAGES = {
    "about us.html":        {"nav": "cleaning", "footer": "cleaning", "current": "about us.html",
                             "params": {"BRAND": "Nairobi Cleaning", "MARGIN": " mt-auto"}},
    "blog.html":            {"nav": "cleaning", "footer": "cleaning", "current": "blog.html",
                             "params": {"BRAND": "Nairobi Cleaning", "MARGIN": " mt-auto"}},
    "contact.html":         {"nav": "cleaning", "footer": "cleaning", "current": "contact.html",
                             "params": {"BRAND": "Nairobi Cleaning", "MARGIN": " mt-auto"}},
    "nairobi.html":         {"nav": "cleaning", "footer": "cleaning", "current": "nairobi.html",
                             "params": {"BRAND": "Nairobi Cleaning", "MARGIN": ""}},
    "privacy.html":         {"nav": "cleaning", "footer": "cleaning", "current": "privacy.html",
                             "params": {"BRAND": "Nairobi Cleaning", "MARGIN": " mt-auto"}},
    "services.html":        {"nav": "cleaning", "footer": "cleaning", "current": "services.html",
                             "params": {"BRAND": "Nairobi Cleaning", "MARGIN": " mt-auto"}},
    "terms of services.html": {"nav": "cleaning", "footer": "cleaning", "current": "terms of services.html",
                               "params": {"BRAND": "Nairobi Cleaning", "MARGIN": " mt-auto"}},
    "index.html":           {"nav": "music", "footer": "cleaning",
                             "params": {"BRAND": "U&I", "MARGIN": ""}},
    "gallery.html":         {"nav": "gallery", "footer": "simple",
                             "params": {"TITLE": "Reliable Cleaning Services Nairobi", "BRAND": "Reliable Cleaning Services Nairobi", "MARGIN": "mt-12"}},
    "more blog.html":       {"nav": "blog", "footer": "simple",
                             "params": {"TITLE": "Cleaning Services Nairobi Blog", "BRAND": "Reliable Cleaning Services Nairobi", "MARGIN": "mt-auto"}},
    "tx.html":              {"nav": None, "footer": "simple",
                             "params": {"BRAND": "Reliable Cleaning Services Nairobi", "MARGIN": "mt-auto"}},
}


def load(path):
    with open(os.path.join(TPL, path), encoding="utf-8") as f:
        return f.read()


def render(template, params, current_page=None):
    out = template
    for k, v in params.items():
        out = out.replace("{{" + k + "}}", v)
    if current_page:
        # mark the current page in the desktop nav (classic anchor format only)
        needle = f'<a class="hover:underline" href="{current_page}">'
        if needle in out:
            out = out.replace(needle, f'<a aria-current="page" class="hover:underline" href="{current_page}">', 1)
    return out


def main():
    navs = {k: load(v) for k, v in NAV_FILES.items()}
    foots = {k: load(v) for k, v in FOOT_FILES.items()}

    for fname, cfg in PAGES.items():
        with open(fname, encoding="utf-8") as f:
            html = f.read()
        orig = html

        if cfg["nav"]:
            nav_html = render(navs[cfg["nav"]], cfg["params"], cfg.get("current"))
            if cfg["nav"] in ("gallery", "blog"):
                pat = re.compile(r"<header\b.*?</header>", re.S)
            else:
                pat = re.compile(r"<nav\b.*?</nav>", re.S)
            assert pat.search(html), f"{fname}: no nav region found"
            html = pat.sub(lambda m: nav_html.strip(), html, count=1)

        foot_html = render(foots[cfg["footer"]], cfg["params"])
        pat = re.compile(r"<footer\b.*?</footer>", re.S)
        assert pat.search(html), f"{fname}: no footer region found"
        html = pat.sub(lambda m: foot_html.strip(), html, count=1)

        # sanity: exactly one nav/header and one footer afterwards
        nav_count = len(re.findall(r"<nav\b", html))
        head_count = len(re.findall(r"<header\b", html))
        foot_count = len(re.findall(r"<footer\b", html))
        if cfg["nav"] in ("gallery", "blog"):
            assert head_count == 1 and nav_count == 1, f"{fname}: header/nav counts wrong ({head_count}/{nav_count})"
        elif cfg["nav"]:
            assert nav_count == 1, f"{fname}: nav count {nav_count}"
        assert foot_count == 1, f"{fname}: footer count {foot_count}"

        if html != orig:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"synced {fname}")
        else:
            print(f"unchanged {fname}")


if __name__ == "__main__":
    main()
