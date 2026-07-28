#!/usr/bin/env python3
"""seo_100_patch.py - idempotent on-page SEO patcher for the Radiant Rides site.

Brings every page to a clean pass on the machine-checkable checks in
Apps/sutera-seo/checklist.py (the engine behind SEO HQ). Safe to re-run.

NOTE ON THE GENERATOR: the 6 suburb LPs come from _build_suburb_lps.py, but the
committed HTML has already drifted from it (GA4 events were injected after the
last generator run), so the committed files are the source of truth - we edit
them directly and do NOT regenerate (same call as the Select Civil LPs).

Fixes:
  - twitter:image (all pages have twitter:card but no image) - derived from og:image, absolutised
  - JSON-LD: the 4 pages with none (about/packages/our-work/contact) get an
    AutoBodyShop+LocalBusiness + BreadcrumbList @graph; the pages that already
    carry an AutoBodyShop node get "LocalBusiness" added to @type so the audit's
    business-schema check recognises it (AutoBodyShop alone doesn't qualify)
  - visible breadcrumb nav on the 5 interior core pages that lack one
    (homepage deliberately omitted - pointless UX on the root)
  - skip-to-content link + <main id="main"> landmark on every page
  - footer + nav headings h4 -> h3 (kills the H2->H4 / H1->H3 skips). Heading
    sizing is driven by Tailwind utility classes + normalised by preflight, so
    the level change is visually invisible
  - packages: a visually-hidden <h2> between the H1 and the pricing H3s
  - trimmed 4 long/short titles + 2 long meta descriptions into band
  - explicit width/height on every <img> from the real asset (both logo classes
    already set width:auto in CSS, so the attrs are a pure CLS/aspect hint)
"""

import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.radiantridesautocare.com.au"

# clean-URL slug per file (for breadcrumb + canonical parity)
SLUG = {
    "index.html": "/", "about.html": "/about", "packages.html": "/packages",
    "our-work.html": "/our-work", "contact.html": "/contact", "privacy.html": "/privacy",
    "ceramic-coating.html": "/ceramic-coating", "paint-correction.html": "/paint-correction",
    "pre-sale-detail.html": "/pre-sale-detail", "headlight-restoration.html": "/headlight-restoration",
    "engine-bay-clean.html": "/engine-bay-clean", "leather-reconditioning.html": "/leather-reconditioning",
    "advanced-odor-elimination.html": "/advanced-odor-elimination",
    "ceramic-coating-berwick.html": "/ceramic-coating-berwick",
    "ceramic-coating-narre-warren.html": "/ceramic-coating-narre-warren",
    "paint-correction-berwick.html": "/paint-correction-berwick",
    "paint-correction-clyde-north.html": "/paint-correction-clyde-north",
    "car-detailing-cranbourne.html": "/car-detailing-cranbourne",
    "car-detailing-pakenham.html": "/car-detailing-pakenham",
}
ALL_FILES = list(SLUG) + ["thank-you.html"]

# pages with NO JSON-LD at all -> inject a full business + breadcrumb graph
INJECT_JSONLD = ["about.html", "packages.html", "our-work.html", "contact.html"]

# visible breadcrumb trails for the interior core pages (homepage omitted)
CRUMBS = {
    "about.html": [("Home", "/"), ("About", None)],
    "packages.html": [("Home", "/"), ("Packages", None)],
    "our-work.html": [("Home", "/"), ("Our Work", None)],
    "contact.html": [("Home", "/"), ("Contact", None)],
    "privacy.html": [("Home", "/"), ("Privacy", None)],
}

# title rewrites -> 50-60 band (were 71/39/66/73)
TITLES = {
    "index.html": "Car Detailing Cranbourne North | Radiant Rides AutoCare",
    "privacy.html": "Privacy Policy | Radiant Rides AutoCare, Cranbourne North",
    "pre-sale-detail.html": "Pre-Sale Car Detail Melbourne | Radiant Rides AutoCare",
    "headlight-restoration.html": "Headlight Restoration Melbourne | Radiant Rides AutoCare",
}

# meta-description rewrites -> 150-160 band (were 175/192)
METAS = {
    "privacy.html": "How Radiant Rides AutoCare collects, uses and protects the personal information you share when you book or request a quote, under the Australian Privacy Act.",
    "ceramic-coating.html": "Professional ceramic coating in Melbourne. Multi-year paint protection at our Cranbourne North studio. Spray sealant from $50, full coating from $1,000.",
}

# Business entity, mirrored from index.html + LocalBusiness added so the audit
# recognises it, shared @id so it dedupes with the AutoBodyShop nodes elsewhere.
BUSINESS_NODE = {
    "@type": ["AutoBodyShop", "LocalBusiness"],
    "@id": BASE + "/#business",
    "name": "Radiant Rides AutoCare",
    "image": BASE + "/brand_assets/6993c810021c99eafe30839f_Radiant_Rides_logo_art.png",
    "url": BASE + "/",
    "telephone": "+61449801505",
    "email": "hello@radiantridesautocare.com.au",
    "address": {"@type": "PostalAddress", "streetAddress": "Crestway Dr",
                "addressLocality": "Cranbourne North", "addressRegion": "VIC",
                "addressCountry": "AU"},
    "areaServed": "Melbourne, Victoria",
    "priceRange": "$$",
}

_DIM_CACHE = {}


def img_dims(src):
    src = src.split("?")[0].split("#")[0]
    if src.startswith(("http://", "https://", "data:", "//")):
        return None
    if src in _DIM_CACHE:
        return _DIM_CACHE[src]
    path = os.path.normpath(os.path.join(ROOT, src.lstrip("/")))
    if not path.startswith(ROOT) or not os.path.isfile(path):
        _DIM_CACHE[src] = None
        return None
    try:
        out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
                             capture_output=True, text=True, timeout=20).stdout
        w = re.search(r"pixelWidth:\s*(\d+)", out)
        h = re.search(r"pixelHeight:\s*(\d+)", out)
        dims = (int(w.group(1)), int(h.group(1))) if w and h else None
    except Exception:
        dims = None
    _DIM_CACHE[src] = dims
    return dims


def meta_prop(html, prop):
    m = re.search(rf'<meta property="{re.escape(prop)}"[^>]*content="([^"]*)"', html)
    return m.group(1) if m else ""


def abs_url(u):
    if not u:
        return u
    return u if u.startswith("http") else BASE + "/" + u.lstrip("/")


def crumb_html(trail):
    parts = []
    for i, (name, slug) in enumerate(trail):
        if i:
            parts.append('      <li aria-hidden="true" class="text-neutral-600">/</li>')
        if slug is None:
            parts.append(f'      <li aria-current="page" class="text-white">{name}</li>')
        else:
            parts.append(f'      <li><a class="hover:text-white" href="{slug}">{name}</a></li>')
    return ('<nav aria-label="Breadcrumb" class="border-b border-white/10 bg-black">\n'
            '  <div class="container-x py-3">\n'
            '    <ol class="flex items-center gap-2 text-xs text-neutral-400">\n'
            + "\n".join(parts) + "\n    </ol>\n  </div>\n</nav>\n")


def crumb_node(trail):
    items = []
    for i, (name, slug) in enumerate(trail, 1):
        it = {"@type": "ListItem", "position": i, "name": name}
        if slug is not None:
            it["item"] = BASE + ("" if slug == "/" else slug) + ("/" if slug == "/" else "")
        items.append(it)
    return {"@type": "BreadcrumbList", "itemListElement": items}


def patch(fn):
    path = os.path.join(ROOT, fn)
    html = open(path, encoding="utf-8").read()
    orig = html
    did = []

    # --- title ---
    if fn in TITLES:
        html2 = re.sub(r"<title>.*?</title>", "<title>" + TITLES[fn] + "</title>", html, count=1, flags=re.S)
        if html2 != html:
            html = html2
            did.append(f"title({len(TITLES[fn])})")

    # --- meta description ---
    if fn in METAS:
        new = METAS[fn]
        html2 = re.sub(r'(<meta name="description" content=")[^"]*(")',
                       lambda m: m.group(1) + new + m.group(2), html, count=1)
        if html2 != html:
            html = html2
            did.append(f"desc({len(new)})")

    # --- twitter:image (all pages have card, none have image) ---
    if 'name="twitter:image"' not in html and 'name="twitter:card"' in html:
        img = abs_url(meta_prop(html, "og:image"))
        if img:
            tag = f'\n<meta name="twitter:image" content="{img}" />'
            html = re.sub(r'(<meta name="twitter:card"[^>]*>)', r'\1' + tag, html, count=1)
            did.append("twitter:image")

    # --- JSON-LD ---
    if "application/ld+json" not in html:
        if fn in INJECT_JSONLD:
            graph = {"@context": "https://schema.org",
                     "@graph": [BUSINESS_NODE, crumb_node(CRUMBS[fn])]}
            block = ('<script type="application/ld+json">\n'
                     + json.dumps(graph, indent=2, ensure_ascii=False) + "\n</script>\n")
            html = html.replace("</head>", block + "</head>", 1)
            did.append("jsonld-inject")
    elif '"@type": "AutoBodyShop"' in html:
        html = html.replace('"@type": "AutoBodyShop"',
                            '"@type": ["AutoBodyShop", "LocalBusiness"]', 1)
        did.append("localbusiness-type")

    # --- skip-to-content link ---
    if "skip-link" not in html:
        html = html.replace("<body>",
                            '<body>\n<a class="skip-link" href="#main">Skip to content</a>', 1)
        did.append("skip-link")

    # --- visible breadcrumb nav (interior core pages), after </header> ---
    if fn in CRUMBS and 'aria-label="Breadcrumb"' not in html:
        he = html.find("</header>")
        if he != -1:
            pt = he + len("</header>")
            html = html[:pt] + "\n" + crumb_html(CRUMBS[fn]) + html[pt:]
            did.append("breadcrumb-nav")

    # --- <main id="main"> wrapper: before first <section> after header, close before <footer> ---
    if not re.search(r"<main\b", html):
        he = html.find("</header>")
        start = he + len("</header>") if he != -1 else 0
        sm = re.search(r"<section\b", html[start:])
        fo = html.find("<footer", start)
        if sm and fo != -1:
            sec = start + sm.start()
            if sec < fo:
                html = html[:fo] + "</main>\n\n" + html[fo:]     # close first (higher index)
                html = html[:sec] + '<main id="main">\n' + html[sec:]
                did.append("main")

    # --- footer + nav headings h4 -> h3 (Tailwind normalises size; visually identical) ---
    if re.search(r"<h4\b", html):
        html = re.sub(r"<h4(\b[^>]*)>", r"<h3\1>", html)
        html = html.replace("</h4>", "</h3>")
        did.append("h4->h3")

    # --- packages: visually-hidden <h2> between the H1 and the pricing H3s ---
    if fn == "packages.html" and "sr-only" not in html.split("</h1>")[0][-200:]:
        html = html.replace("</h1>",
                            '</h1>\n<h2 class="sr-only">Detailing packages and pricing</h2>', 1)
        did.append("packages-h2")

    # --- explicit width/height on <img> ---
    def add_dims(m):
        tag = m.group(0)
        if re.search(r"\bwidth=", tag) and re.search(r"\bheight=", tag):
            return tag
        s = re.search(r'\bsrc="([^"]+)"', tag)
        if not s:
            return tag
        d = img_dims(s.group(1))
        if not d:
            return tag
        return re.sub(r"<img\b", f'<img width="{d[0]}" height="{d[1]}"', tag, count=1)

    new_html = re.sub(r"<img\b[^>]*?>", add_dims, html)
    if new_html != html:
        did.append("img-dims")
        html = new_html

    if html != orig:
        open(path, "w", encoding="utf-8").write(html)
    return did


def main():
    print(f"Patching {len(ALL_FILES)} pages under {ROOT}\n")
    for fn in ALL_FILES:
        changed = patch(fn)
        print(f"  {fn:34s} {', '.join(changed) if changed else 'no change'}")
    print("\nDone. Idempotent - safe to re-run.")


if __name__ == "__main__":
    main()
