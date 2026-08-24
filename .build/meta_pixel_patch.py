#!/usr/bin/env python3
"""meta_pixel_patch.py - install the Meta (Facebook) Pixel across the Radiant Rides site.

Pixel ID 987419320779913, supplied by Dylan Tanner 2026-08-24 so he can run Meta ads.

Two snippets, per Meta's install instructions:

  1. BASE CODE on every page. Injected into <head> directly after the GA4 gtag
     block, so all tracking lives in one cluster. Fires PageView.

  2. EVENT CODE on the conversion page only. The Formspree form carries
     `_next=https://www.radiantridesautocare.com.au/thank-you`, so a successful
     submission always lands on /thank-you. Firing `Lead` there (rather than on
     the submit handler) means Meta only counts submissions Formspree actually
     accepted, and it does not race the page unload that a form POST triggers.
     thank-you.html is noindex and carries no form, so it cannot self-trigger.

Deliberately NOT mirroring the GA4 `generate_lead` submit beacon: that one fires
on any submit attempt including ones Formspree rejects, which is tolerable for
analytics but pollutes an ad-optimisation signal.

NOTE ON THE GENERATOR: new Car Detailing x suburb LPs are cloned from
car-detailing-pakenham.html by gen_car_detailing_suburbs.py, so patching the
committed pages here means future suburb LPs inherit the pixel for free. No
generator change needed. (_build_suburb_lps.py stays retired - it predates both
the GA4 events and the SEO-100 pass.)

Idempotent. Safe to re-run. Usage: python3 .build/meta_pixel_patch.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIXEL_ID = "987419320779913"

BASE_MARKER = "SUTERA_META_PIXEL"
LEAD_MARKER = "SUTERA_META_LEAD"

# The base code exactly as Meta supplies it, with the noscript URL rejoined onto
# one line (Meta's copy box wraps it mid-attribute) and the stray leading space
# on the init call removed. Behaviour is unchanged.
BASE_SNIPPET = """
<!-- Meta Pixel Code -->
<script>/* {marker} */
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window,document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{pixel}');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none" alt=""
src="https://www.facebook.com/tr?id={pixel}&ev=PageView&noscript=1" /></noscript>
<!-- End Meta Pixel Code -->
""".format(marker=BASE_MARKER, pixel=PIXEL_ID)

# Conversion page only. Sits after the base code so fbq() is already stubbed.
LEAD_SNIPPET = """
<!-- Meta Pixel Event Code -->
<script>/* {marker} */
fbq('track', 'Lead');
</script>
<!-- End Meta Pixel Event Code -->
""".format(marker=LEAD_MARKER)

# Anchor: the closing </script> of the GA4 config block. Every page has exactly
# one gtag('config', ...) call; not every page has the "<!-- Google tag -->"
# comment above it, so anchor on the config call itself.
GA4_CONFIG = "gtag('config', 'G-C62DXBY0EC');"

LEAD_PAGE = "thank-you.html"


def patch(path):
    """Return (changed, note) after injecting whatever this page is missing."""
    name = os.path.basename(path)
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    original = html
    notes = []

    if BASE_MARKER not in html:
        idx = html.find(GA4_CONFIG)
        if idx == -1:
            return False, "SKIPPED - no GA4 config block to anchor to"
        close = html.find("</script>", idx)
        if close == -1:
            return False, "SKIPPED - unterminated GA4 script block"
        cut = close + len("</script>")
        html = html[:cut] + BASE_SNIPPET + html[cut:]
        notes.append("base code")

    if name == LEAD_PAGE and LEAD_MARKER not in html:
        end = html.find("<!-- End Meta Pixel Code -->")
        if end == -1:
            return False, "SKIPPED - base code missing, cannot anchor Lead event"
        cut = end + len("<!-- End Meta Pixel Code -->")
        html = html[:cut] + LEAD_SNIPPET + html[cut:]
        notes.append("Lead event")

    if html == original:
        return False, "already installed"

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return True, " + ".join(notes)


def main():
    pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    if not pages:
        sys.exit("no HTML pages found in %s" % ROOT)

    changed = skipped = 0
    for name in pages:
        did, note = patch(os.path.join(ROOT, name))
        if did:
            changed += 1
        if note.startswith("SKIPPED"):
            skipped += 1
        print("%-38s %s" % (name, note))

    print("\n%d page(s) patched, %d unchanged, %d skipped." %
          (changed, len(pages) - changed - skipped, skipped))
    if skipped:
        sys.exit(1)


if __name__ == "__main__":
    main()
