#!/usr/bin/env python3
"""Phase 1 (items 1-4): broken links, shared <head> tags, mobile hamburger menu,
auto-updating copyright year, main.js include. Additive only - nothing removed."""
import re

CLEANING_OG_IMG = "https://storage.googleapis.com/a1aa/image/f778d151-bc04-47f7-9327-93d117397242.jpg"
MUSIC_OG_IMG = "https://storage.googleapis.com/a1aa/image/d9ee8944-dee4-4dc9-3558-77e48386c4b2.jpg"
THEME_COLOR = "#0d9488"

# file -> (meta description, og image, site name, mobile nav links [(href,label),...])
PAGES = {
    "index.html": (
        "Nairobi Cleaning - professional, trustworthy and affordable cleaning services in "
        "Nairobi. House, office, carpet, window and deep cleaning. Book on WhatsApp.",
        CLEANING_OG_IMG, "Nairobi Cleaning",
        [("index.html", "Home"), ("services.html", "Services"), ("about us.html", "About Us"),
         ("contact.html", "Contact"), ("blog.html", "Blog")],
    ),
    "about us.html": (
        "Learn about Nairobi Cleaning - a trusted provider of professional cleaning services "
        "in Nairobi. Eco-friendly products, experienced cleaners, residential and commercial cleaning.",
        CLEANING_OG_IMG, "Nairobi Cleaning",
        [("index.html", "Home"), ("services.html", "Services"), ("#", "About Us"),
         ("contact.html", "Contact"), ("blog.html", "Blog")],
    ),
    "blog.html": (
        "Expert cleaning tips and guides from Nairobi Cleaning. Keep your home spotless "
        "with eco-friendly products and professional service advice.",
        CLEANING_OG_IMG, "Nairobi Cleaning",
        [("index.html", "Home"), ("services.html", "Services"), ("about us.html", "About Us"),
         ("contact.html", "Contact"), ("#", "Blog")],
    ),
    "contact.html": (
        "Contact Nairobi Cleaning to book professional cleaning services in Nairobi. "
        "Call, WhatsApp or email us today for a free quote.",
        CLEANING_OG_IMG, "Nairobi Cleaning",
        [("index.html", "Home"), ("services.html", "Services"), ("about us.html", "About Us"),
         ("#", "Contact"), ("blog.html", "Blog")],
    ),
    "gallery.html": (
        "Browse the Reliable Cleaning Services Nairobi gallery - meet our trusted cleaners and "
        "see the house, office, carpet and window cleaning services we offer.",
        CLEANING_OG_IMG, "Nairobi Cleaning",
        [("index.html", "Home"), ("#categories", "Categories"), ("#gallery", "Gallery"),
         ("contact.html", "Contact")],
    ),
    "more blog.html": (
        "Latest cleaning tips and news from Cleaning Services Nairobi - kitchen cleaning, "
        "carpet care and more expert advice for a sparkling home.",
        CLEANING_OG_IMG, "Nairobi Cleaning",
        [("index.html", "Home"), ("blog.html", "Blog"), ("contact.html", "Contact")],
    ),
    "nairobi.html": (
        "Nairobi Cleaning - professional cleaning services across Nairobi: house cleaning, "
        "office cleaning, carpet cleaning and more. Book now via WhatsApp.",
        CLEANING_OG_IMG, "Nairobi Cleaning",
        [("index.html", "Home"), ("services.html", "Services"), ("about us.html", "About Us"),
         ("contact.html", "Contact"), ("blog.html", "Blog")],
    ),
    "privacy.html": (
        "Read the Nairobi Cleaning privacy policy to understand how we collect, use and "
        "protect your personal information.",
        CLEANING_OG_IMG, "Nairobi Cleaning",
        [("index.html", "Home"), ("services.html", "Services"), ("about us.html", "About Us"),
         ("contact.html", "Contact"), ("blog.html", "Blog")],
    ),
    "services.html": (
        "Explore Nairobi Cleaning services - house, office, carpet, window and deep cleaning. "
        "Affordable, eco-friendly and professional cleaning in Nairobi.",
        CLEANING_OG_IMG, "Nairobi Cleaning",
        [("index.html", "Home"), ("services.html", "Services"), ("about us.html", "About Us"),
         ("contact.html", "Contact"), ("blog.html", "Blog")],
    ),
    "terms of services.html": (
        "Read the terms of service for Nairobi Cleaning - booking terms, payments and "
        "customer care guidelines.",
        CLEANING_OG_IMG, "Nairobi Cleaning",
        [("index.html", "Home"), ("services.html", "Services"), ("about us.html", "About Us"),
         ("contact.html", "Contact"), ("blog.html", "Blog")],
    ),
    "tx.html": (
        "Reliable Cleaning Services Nairobi - meet our professional cleaners and book "
        "trusted house, office and commercial cleaning services.",
        CLEANING_OG_IMG, "Nairobi Cleaning", None,  # no nav on this page
    ),
}


def extract_title(html):
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if not m:
        return "Nairobi Cleaning"
    return " ".join(m.group(1).split())


def head_block(desc, og_image, site_name, title):
    return (
        '  <meta content="%s" name="description"/>\n'
        '  <meta content="%s" property="og:title"/>\n'
        '  <meta content="%s" property="og:description"/>\n'
        '  <meta content="website" property="og:type"/>\n'
        '  <meta content="%s" property="og:site_name"/>\n'
        '  <meta content="%s" property="og:image"/>\n'
        '  <meta content="summary_large_image" name="twitter:card"/>\n'
        '  <meta content="%s" name="twitter:title"/>\n'
        '  <meta content="%s" name="twitter:description"/>\n'
        '  <meta content="%s" name="twitter:image"/>\n'
        '  <meta content="%s" name="theme-color"/>\n'
        '  <link href="favicon.svg" rel="icon" type="image/svg+xml"/>\n'
        '  <link href="apple-touch-icon.png" rel="apple-touch-icon"/>\n'
    ) % (desc, title, desc, site_name, og_image, title, desc, og_image, THEME_COLOR)


def hamburger_button():
    return (
        '   <button aria-expanded="false" aria-label="Toggle navigation menu" '
        'class="md:hidden text-white text-xl focus:outline-none" data-nav-toggle="#mobileMenu" type="button">\n'
        '    <i class="fas fa-bars"></i>\n'
        '    <i class="fas fa-times hidden"></i>\n'
        '   </button>\n'
    )


def hamburger_button_dark():
    return hamburger_button().replace('class="md:hidden text-white', 'class="md:hidden text-gray-900')


def mobile_menu(links):
    items = "\n".join(
        '    <a class="block py-2 text-sm font-semibold hover:underline" href="%s">%s</a>' % (h, t)
        for h, t in links
    )
    return '   <div class="hidden md:hidden w-full pt-3 pb-1" data-nav-menu id="mobileMenu">\n%s\n   </div>\n' % items


def main():
    for fname, (desc, og_image, site_name, links) in PAGES.items():
        with open(fname, encoding="utf-8") as f:
            html = f.read()
        title = extract_title(html)
        already_has_head = 'name="description"' in html
        already_has_menu = "data-nav-toggle" in html
        already_has_year = "data-year" in html
        already_has_js = 'src="js/main.js"' in html

        # ---- 1. head block after </title> (idempotent) ----
        if not already_has_head:
            assert "</title>" in html, fname
            html = html.replace("</title>", "</title>\n" + head_block(desc, og_image, site_name, title), 1)

        # ---- 3. hamburger + mobile menu (idempotent) ----
        if already_has_menu:
            pass
        elif fname in ("gallery.html", "more blog.html"):
            # header-style: hide desktop nav on mobile, add button + menu
            html = html.replace(
                '<div class="max-w-7xl mx-auto px-6 py-4 flex flex-col md:flex-row md:items-center md:justify-between">',
                '<div class="max-w-7xl mx-auto px-6 py-4 flex flex-wrap items-center justify-between gap-3">', 1)
            html = html.replace(
                '<div class="max-w-7xl mx-auto px-6 py-4 flex flex-col sm:flex-row items-center justify-between">',
                '<div class="max-w-7xl mx-auto px-6 py-4 flex flex-wrap items-center justify-between gap-3">', 1)
            html = html.replace('<nav class="space-x-4 text-sm font-semibold">',
                                '<nav class="hidden md:block space-x-4 text-sm font-semibold">', 1)
            btn = hamburger_button_dark()
            menu = mobile_menu(links)
            # button + menu must be siblings of the (hidden-on-mobile) nav,
            # i.e. children of the flex-wrap container div that wraps them.
            html = html.replace("</nav>", "</nav>\n" + btn + menu, 1)
        elif links is not None:
            # classic dark navbar
            html = html.replace(
                '<nav class="flex items-center justify-between px-6 py-3 bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white">',
                '<nav class="flex flex-wrap items-center justify-between px-6 py-3 bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white">', 1)
            btn = hamburger_button()
            menu = mobile_menu(links)
            html = html.replace("</nav>", btn + menu + "\n  </nav>", 1)

        # ---- 4. auto-updating year (idempotent) ----
        if not already_has_year:
            html = re.sub(r"© (\d{4})", r"© <span data-year>\1</span>", html)

        # ---- main.js include (idempotent) ----
        if not already_has_js:
            html = html.replace("</body>", '  <script src="js/main.js"></script>\n </body>', 1)

        with open(fname, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"updated {fname} (title: {title})")


# ---- 1. broken link fixes (after the generic pass so nothing re-breaks) ----
def fix_links():
    fix = [
        ("contact.html", 'href="teams of services.html"', 'href="terms of services.html"'),
        ("services.html", 'href="services.htnl"', 'href="services.html"'),
        ("privacy.html", 'href="about.html"', 'href="about us.html"'),
        ("more blog.html", 'href="/index.html"', 'href="index.html"'),
        ("more blog.html", 'href="/blog"', 'href="blog.html"'),
    ]
    for fname, old, new in fix:
        with open(fname, encoding="utf-8") as f:
            html = f.read()
        if old not in html:
            continue  # already fixed
        html = html.replace(old, new)
        with open(fname, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"fixed link in {fname}: {old} -> {new}")


if __name__ == "__main__":
    main()
    fix_links()
