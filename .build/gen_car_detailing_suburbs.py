#!/usr/bin/env python3
"""gen_car_detailing_suburbs.py - build the missing Car Detailing x suburb LPs.

Clones car-detailing-pakenham.html (the "away suburb" variant of the LP, as
opposed to the home-patch Cranbourne one) and localises it for the suburbs in
clients.yaml that have no Car Detailing page yet: Clyde North, Clyde, Narre
Warren, Berwick and Melbourne.

Why not _build_suburb_lps.py: that script has drifted from the committed pages
(it predates the GA4 SUTERA_LEAD_EVENTS block and the SEO-100 pass), so
re-running it would strip live tracking. Same lesson as Select Civil's
_build_city_lps.py - clone the committed page, do not regenerate from the old
builder.

What gets localised: title/meta/og/canonical/geo, the whole JSON-LD graph
(LocalBusiness areaServed, Service, BreadcrumbList, the two suburb-specific
FAQs), hero, the three-paragraph "why <suburb> drivers book" block, the drive
-time panel, the drop-off card, the "Around <suburb>" tile grid, the sibling
-LP pill row, both suburb FAQs in the body, and every form field / hidden field.
Drive times and coordinates match what the already-live LPs for the same suburb
say (Berwick 12 via M1, Narre Warren 15 via Princes Hwy, Clyde North 8 via
Berwick-Cranbourne Rd), so the site never contradicts itself.

Also patches sitemap.xml and the homepage "Areas We Service" band. Idempotent.

Usage: python3 .build/gen_car_detailing_suburbs.py
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "car-detailing-pakenham.html")
SITE = "https://www.radiantridesautocare.com.au"
SITEMAP = os.path.join(ROOT, "sitemap.xml")
INDEX = os.path.join(ROOT, "index.html")
LASTMOD = "2026-08-17"

WASH_VS_DETAIL = ("Detailing isn't a wash. A wash cleans the outside. A detail cleans the outside AND "
                  "resets the inside, with deeper attention to vents, carpet, upholstery, trim and the "
                  "surfaces a wash never touches. The result holds for weeks, not days, which is why most "
                  "of our {name} regulars run on a roughly six-week rotation.")

SUBURBS = [
    {
        "slug": "clyde-north", "name": "Clyde North", "mins": "8",
        "route": "Berwick-Cranbourne Rd", "geo": ("-38.0944", "145.3406"),
        "paras": [
            "Clyde North is one of the fastest-growing pockets in Casey, and it shows in the cars. New estates, driveways with no shade, and a lot of daily drivers doing the freeway run every morning. Fresh paint picks up swirl marks fast when it gets washed in a hurry, and a family car's interior collects more than anyone wants to think about.",
            None,
            "We're an 8 minute drive from Clyde North to our Cranbourne North studio straight down Berwick-Cranbourne Road, which makes this about the easiest suburb on our list to book from. Drop off in the morning, pick up clean, and most Basic and Interior Reset jobs are done the same day.",
        ],
        "dropoff": "8 minute drive from Clyde North via Berwick-Cranbourne Rd. Drop in the morning, we send updates through the day.",
        "cities": ["Clyde North", "Clyde", "Cranbourne East", "Berwick", "Narre Warren South"],
        "tiles": ["Clyde", "Cranbourne East", "Cranbourne North", "Berwick", "Officer",
                  "Narre Warren South", "Botanic Ridge", "Devon Meadows", "Hampton Park",
                  "Lyndhurst", "Lynbrook", "Junction Village"],
        "pills": [("/ceramic-coating-clyde-north", "Ceramic coating Clyde North"),
                  ("/paint-correction-clyde-north", "Paint correction Clyde North"),
                  ("/car-detailing-clyde", "Car detailing Clyde"),
                  ("/car-detailing-cranbourne", "Car detailing Cranbourne")],
    },
    {
        "slug": "clyde", "name": "Clyde", "mins": "12",
        "route": "Berwick-Cranbourne Rd", "geo": ("-38.1289", "145.3327"),
        "paras": [
            "Clyde has gone from farmland to new estates in a handful of years, and most cars here are doing an estate-to-freeway commute on roads that are still half construction site. That means fine dust, road grit and the film that settles on anything parked outside overnight, which is exactly the sort of build-up a quick wash smears around rather than removes.",
            None,
            "We're a 12 minute drive from Clyde to our Cranbourne North studio up Berwick-Cranbourne Road. Drop off in the morning, pick up clean, and we'll be straight about timing when we quote.",
        ],
        "dropoff": "12 minute drive from Clyde via Berwick-Cranbourne Rd. Drop in the morning, we send updates through the day.",
        "cities": ["Clyde", "Clyde North", "Cranbourne East", "Devon Meadows", "Botanic Ridge"],
        "tiles": ["Clyde North", "Cranbourne East", "Cranbourne South", "Botanic Ridge",
                  "Devon Meadows", "Junction Village", "Pearcedale", "Cranbourne",
                  "Officer", "Berwick", "Tooradin", "Cardinia"],
        "pills": [("/ceramic-coating-clyde", "Ceramic coating Clyde"),
                  ("/car-detailing-clyde-north", "Car detailing Clyde North"),
                  ("/car-detailing-cranbourne", "Car detailing Cranbourne"),
                  ("/paint-correction-clyde-north", "Paint correction Clyde North")],
    },
    {
        "slug": "narre-warren", "name": "Narre Warren", "mins": "15",
        "route": "Princes Hwy", "geo": ("-38.0269", "145.3036"),
        "paras": [
            "Narre Warren cars work hard. Between the Princes Highway run, the Fountain Gate car park and the school-run kilometres, a daily driver here picks up road film and car-park marks on the outside and a season's worth of dust, crumbs and spills on the inside. Most owners never find the Sunday to reset all of it properly.",
            None,
            "We're a 15 minute drive from Narre Warren to our Cranbourne North studio down the Princes Highway. Drop off in the morning, pick up clean. Most Basic and Interior Reset jobs are same day, and we'll always be straight about timing when we quote.",
        ],
        "dropoff": "15 minute drive from Narre Warren via Princes Hwy. Drop in the morning, we send updates through the day.",
        "cities": ["Narre Warren", "Narre Warren South", "Narre Warren North", "Berwick", "Hallam"],
        "tiles": ["Narre Warren South", "Narre Warren North", "Fountain Gate", "Berwick",
                  "Hallam", "Hampton Park", "Endeavour Hills", "Doveton", "Lynbrook",
                  "Lyndhurst", "Harkaway", "Clyde North"],
        "pills": [("/ceramic-coating-narre-warren", "Ceramic coating Narre Warren"),
                  ("/car-detailing-berwick", "Car detailing Berwick"),
                  ("/paint-correction-berwick", "Paint correction Berwick")],
    },
    {
        "slug": "berwick", "name": "Berwick", "mins": "12",
        "route": "M1", "geo": ("-38.0309", "145.3471"),
        "paras": [
            "Berwick is a long-haul commute suburb, and the leafy older streets that make it good to live in are hard on paint. Tree sap, bird droppings and pollen through spring, on top of the tar and grit that comes with a daily M1 run. Left alone, that lot etches into the clear coat rather than washing off.",
            None,
            "We're a 12 minute drive from Berwick to our Cranbourne North studio down the M1. Drop off in the morning, pick up clean. Most Basic and Interior Reset jobs are same day, and if the paint needs more than a detail we'll tell you rather than sell you the wrong package.",
        ],
        "dropoff": "12 minute drive from Berwick via the M1. Drop in the morning, we send updates through the day.",
        "cities": ["Berwick", "Beaconsfield", "Harkaway", "Narre Warren South", "Officer"],
        "tiles": ["Beaconsfield", "Harkaway", "Narre Warren South", "Narre Warren", "Officer",
                  "Clyde North", "Guys Hill", "Upper Beaconsfield", "Endeavour Hills",
                  "Hallam", "Pakenham", "Clyde"],
        "pills": [("/ceramic-coating-berwick", "Ceramic coating Berwick"),
                  ("/paint-correction-berwick", "Paint correction Berwick"),
                  ("/car-detailing-narre-warren", "Car detailing Narre Warren")],
    },
    {
        "slug": "melbourne", "name": "Melbourne", "mins": "45",
        "route": "EastLink / M1", "geo": ("-37.8136", "144.9631"),
        "meta": "Professional car detailing for Melbourne drivers. Fixed studio in Cranbourne North, Melbourne's south-east, about 45 minutes from the CBD. Enquire today.",
        "og_desc": "Car detailing for Melbourne drivers at our Cranbourne North studio in Melbourne's south-east, about 45 minutes from the CBD.",
        "hero_p": "Professional car detailing for Melbourne drivers. Booked in at our Cranbourne North studio in Melbourne's south-east, about 45 minutes from the CBD.",
        "paras": [
            "Melbourne is hard on cars in ways that creep up slowly. Bayside salt air, city car-park scrapes, tree sap through the leafy inner east, summer sun on a parked bonnet and the fine grit that comes off every freeway. Almost all of it is reversible, but only with a proper detail rather than another quick wash.",
            None,
            "One thing to be upfront about: we're a fixed studio, not a mobile service, and we sit in Melbourne's south-east at Cranbourne North. Most of our metro clients come from the south-east corridor, out through Casey, Dandenong and down towards Frankston. From the CBD and the inner suburbs it's about a 45 minute run down EastLink or the M1. Mobile headlight restoration is the one service we do bring to you.",
        ],
        "glance_route": "~45 min from the CBD via EastLink / M1",
        "dropoff": "About 45 minutes from the CBD via EastLink / M1, less from the south-east. Drop in the morning, we send updates through the day.",
        "mobile_faq": "We are not a mobile detailing service. All general detailing is carried out at our Cranbourne North studio in Melbourne's south-east, about 45 minutes from the CBD and a lot less from the south-east suburbs. We do offer mobile headlight restoration as a separate add-on.",
        "cities": ["Melbourne", "Dandenong", "Frankston", "Berwick", "Cranbourne"],
        "tiles": ["Melbourne CBD", "South Yarra", "Brighton", "Caulfield", "Glen Waverley",
                  "Mount Waverley", "Dandenong", "Springvale", "Mentone", "Mordialloc",
                  "Frankston", "Mornington"],
        "pills": [("/car-detailing-cranbourne", "Car detailing Cranbourne"),
                  ("/car-detailing-berwick", "Car detailing Berwick"),
                  ("/ceramic-coating-berwick", "Ceramic coating Berwick")],
    },
]


def rep(html, old, new, label, count=1):
    if html.count(old) < count:
        raise SystemExit(f"[{label}] anchor not found:\n  {old[:110]}")
    return html.replace(old, new, count)


def replace_block(html, start, end, inner, label):
    """Swap what sits between the first `start` marker and the next `end`."""
    i = html.find(start)
    if i == -1:
        raise SystemExit(f"[{label}] start marker not found: {start[:80]}")
    j = html.index(end, i + len(start))
    return html[:i + len(start)] + inner + html[j:]


def build_schema(sub, old_ld):
    """Rewrite the JSON-LD graph rather than string-patching six places in it."""
    doc = json.loads(old_ld)
    name, slug = sub["name"], sub["slug"]
    url = f"{SITE}/car-detailing-{slug}"
    cities = [{"@type": "City", "name": c} for c in sub["cities"]]
    for node in doc["@graph"]:
        t = node.get("@type")
        if isinstance(t, list) and "LocalBusiness" in t:
            node["areaServed"] = cities
        elif t == "Service":
            node["name"] = f"Car Detailing {name}"
            node["description"] = (f"Professional car detailing for {name} vehicles. "
                                   f"Carried out in-studio at our Cranbourne North location.")
            node["areaServed"] = [{"@type": "City", "name": name}]
            node["hasOfferCatalog"]["name"] = f"Car Detailing options for {name} drivers"
        elif t == "BreadcrumbList":
            last = node["itemListElement"][-1]
            last["name"] = f"Car Detailing {name}"
            last["item"] = url
        elif t == "FAQPage":
            qs = node["mainEntity"]
            for q in qs:
                if q["name"].startswith("Are you mobile"):
                    q["name"] = f"Are you mobile? Can you come to {name}?"
                    q["acceptedAnswer"]["text"] = sub["mobile_faq"]
            qs[-1]["name"] = sub["faq6"][0]
            qs[-1]["acceptedAnswer"]["text"] = sub["faq6"][1]
    return json.dumps(doc, indent=2, ensure_ascii=False)


def build_page(sub):
    name, slug, mins = sub["name"], sub["slug"], sub["mins"]
    url = f"{SITE}/car-detailing-{slug}"
    title = f"Car Detailing {name} | Radiant Rides AutoCare"
    meta = sub.get("meta", f"Professional car detailing for {name} drivers. Car Detailing at our "
                           f"Cranbourne North studio, {mins} minutes from {name}. Enquire today.")
    og_desc = sub.get("og_desc", f"Car Detailing for {name} drivers. Booked in at our Cranbourne "
                                 f"North studio, {mins} minutes from {name}.")
    hero_p = sub.get("hero_p", f"Professional car detailing for {name} drivers. Booked in at our "
                               f"Cranbourne North studio, {mins} minutes from {name}.")
    route_phrase = sub["route"] if sub["route"].startswith("M1") else "the " + sub["route"]
    sub.setdefault("mobile_faq", "We are not a mobile detailing service. All general detailing is "
                                 "carried out at our Cranbourne North studio, about " + mins + " minutes from "
                                 + name + " via " + route_phrase + ". "
                                 "We do offer mobile headlight restoration as a separate add-on.")
    sub.setdefault("faq6", (
        f"How much is car detailing in {name}?",
        "Pricing starts from $110 for our Basic Interior and Exterior package and $150 for Interior "
        "Reset and Protection. Paint Enhancement is from $300. Add-ons like odor elimination, leather "
        "reconditioning and engine bay clean are priced on top. We quote individually after knowing the vehicle."))
    paras = [p if p else WASH_VS_DETAIL.format(name=name) for p in sub["paras"]]

    # Audited head lengths (Apps/sutera-seo/checklist.py: title 40-65, desc 120-170).
    if not 40 <= len(title) <= 65:
        raise SystemExit(f"[{slug}] title {len(title)} chars: {title}")
    if not 120 <= len(meta) <= 170:
        raise SystemExit(f"[{slug}] meta description {len(meta)} chars")

    html = open(BASE, encoding="utf-8").read()

    # -- head (regex on the attribute so the surrounding markup is untouched) --
    html = re.sub(r"<title>.*?</title>", lambda m: f"<title>{title}</title>", html, count=1)
    html = re.sub(r'(<meta name="description" content=")[^"]*(")',
                  lambda m: m.group(1) + meta + m.group(2), html, count=1)
    html = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
                  lambda m: m.group(1) + title + m.group(2), html, count=1)
    html = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
                  lambda m: m.group(1) + og_desc + m.group(2), html, count=1)
    lat, lon = sub["geo"]
    html = rep(html, '<meta name="geo.position" content="-38.0719;145.4843" />',
               f'<meta name="geo.position" content="{lat};{lon}" />', "geo.position")
    html = rep(html, '<meta name="ICBM" content="-38.0719, 145.4843" />',
               f'<meta name="ICBM" content="{lat}, {lon}" />', "ICBM")

    # -- JSON-LD graph --
    s = html.index('<script type="application/ld+json">') + len('<script type="application/ld+json">')
    e = html.index("</script>", s)
    html = html[:s] + "\n" + build_schema(sub, html[s:e]) + "\n" + html[e:]

    # -- hero paragraph --
    html = rep(html,
        "        Professional car detailing for Pakenham drivers. Booked in at our Cranbourne North studio, 20 minutes from Pakenham.\n",
        f"        {hero_p}\n", "hero-p")

    # -- the three-paragraph "why <suburb> drivers book" block --
    body = "\n" + "\n".join(f"        <p>{p}</p>" for p in paras) + "\n      "
    html = replace_block(html, '<div class="space-y-5 text-neutral-300 text-lg leading-relaxed">',
                         "</div>", body, "why-block")

    # -- at-a-glance drive time + drop-off card --
    glance = sub.get("glance_route") or ("~" + mins + " min via " + sub["route"])
    html = rep(html, '<span class="font-semibold">~20 min via Princes Hwy / M1</span>',
               '<span class="font-semibold">' + glance + '</span>', "glance-drive-time")
    html = rep(html,
        "20 minute drive from Pakenham via Princes Hwy / M1. Drop in the morning, we send updates through the day.",
        sub["dropoff"], "dropoff-card")

    # -- "Around <suburb>" tiles + sibling-LP pills --
    tiles = "\n" + "\n".join(
        f'      <div class="border border-white/10 px-4 py-3 text-center">'
        f'<p class="text-neutral-300 text-sm font-semibold">{t}</p></div>' for t in sub["tiles"]) + "\n    "
    html = replace_block(html, '<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">',
                         "</div>\n    <div class=\"mt-8", tiles, "around-tiles")
    pills = "\n" + "\n".join(
        f'      <a href="{h}" class="pill border border-white/15 px-4 py-2 text-white hover:bg-white/5">{l}</a>'
        for h, l in sub["pills"]) + \
        '\n      <a href="/packages" class="pill border border-white/15 px-4 py-2 text-white hover:bg-white/5">All packages</a>\n    '
    html = replace_block(html, '<div class="mt-8 flex flex-wrap gap-3 text-sm">', "</div>", pills, "pills")

    # -- visible FAQ: the two suburb-specific entries --
    html = rep(html, "<summary>Are you mobile? Can you come to Pakenham?",
               f"<summary>Are you mobile? Can you come to {name}?", "faq-mobile-q")
    html = rep(html,
        "        <p>We are not a mobile detailing service. All general detailing is carried out at our Cranbourne North studio, about 20 minutes from Pakenham via the M1. We do offer <strong>mobile headlight restoration</strong> as a separate add-on, which may suit longer-distance bookings.</p>",
        "        <p>" + sub["mobile_faq"].replace("mobile headlight restoration",
                                                  "<strong>mobile headlight restoration</strong>") + "</p>",
        "faq-mobile-a")
    html = rep(html, "<summary>Is it worth the drive from Pakenham?",
               f"<summary>{sub['faq6'][0]}", "faq6-q")
    html = rep(html,
        "        <p>Most of our Pakenham regulars combine the drop-off with another errand in the Cranbourne or Berwick direction. A proper detail holds for weeks, not days, so the trip earns its keep on the back of a single booking.</p>",
        f"        <p>{sub['faq6'][1]}</p>", "faq6-a")

    # -- studio line in the contact card --
    html = rep(html, "Studio (20 min from Pakenham)",
               f"Studio ({mins} min from {name})" if slug != "melbourne" else "Studio (Cranbourne North)",
               "studio-line")

    # -- everything left is a plain suburb-name or slug swap --
    html = html.replace("car-detailing-pakenham", f"car-detailing-{slug}")
    expected = tiles.count("Pakenham") + pills.count("Pakenham") + body.count("Pakenham") \
        + sum(c == "Pakenham" for c in sub["cities"])
    html = html.replace("Pakenham", name)
    if expected:                      # put back the legitimate neighbour mentions
        html = replace_block(html, '<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">',
                             "</div>\n    <div class=\"mt-8", tiles, "around-tiles-restore")

    for stray in ("20 min", "Princes Hwy / M1" if sub["route"] != "Princes Hwy / M1" else None):
        if stray and stray in html:
            raise SystemExit(f"[{slug}] stray base-page text left in output: {stray}")

    out = os.path.join(ROOT, f"car-detailing-{slug}.html")
    open(out, "w", encoding="utf-8").write(html)
    return out


def patch_sitemap():
    xml = open(SITEMAP, encoding="utf-8").read()
    added = []
    block = ""
    for s in SUBURBS:
        loc = f"{SITE}/car-detailing-{s['slug']}"
        if f"<loc>{loc}</loc>" in xml:
            continue
        added.append(s["slug"])
        block += (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n"
                  f"    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n")
    if not block:
        return "sitemap: all URLs already listed"
    open(SITEMAP, "w", encoding="utf-8").write(xml.replace("</urlset>", block + "</urlset>", 1))
    return f"sitemap: added {len(added)} URLs"


def patch_home():
    """Add the new LPs to the homepage 'Areas We Service' link list."""
    html = open(INDEX, encoding="utf-8").read()
    anchor = '      <li><a href="/car-detailing-pakenham" class="hover:text-white">Car Detailing Pakenham</a></li>\n'
    if anchor not in html:
        raise SystemExit("home: Areas We Service anchor not found")
    add = "".join(
        f'      <li><a href="/car-detailing-{s["slug"]}" class="hover:text-white">Car Detailing {s["name"]}</a></li>\n'
        for s in SUBURBS if f'href="/car-detailing-{s["slug"]}"' not in html)
    if not add:
        return "home: all links already present"
    open(INDEX, "w", encoding="utf-8").write(html.replace(anchor, anchor + add, 1))
    return f"home: added {add.count('<li>')} links to the Areas We Service band"


def main():
    for sub in SUBURBS:
        print(f"  built {os.path.basename(build_page(sub))}")
    print(patch_sitemap())
    print(patch_home())
    print(f"\nDone. {len(SUBURBS)} pages. Idempotent.")


if __name__ == "__main__":
    main()
