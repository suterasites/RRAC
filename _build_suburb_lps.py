#!/usr/bin/env python3
"""Build suburb landing pages for Radiant Rides AutoCare.

Uses ceramic-coating-berwick.html (Phase B2) as the structural template.
Generates the remaining 5 suburb LPs (Phase B3-B7) with per-page config.

Run once. Idempotent (overwrites). Keep the script for adding more
suburbs in future Phase rollouts and for the SEO_brief pace target
of 2 sites/day.

Usage:
    python3 _build_suburb_lps.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://www.radiantridesautocare.com.au"

# ============================================================
# SHARED HEAD (Tailwind CDN, fonts, GA4, site verification)
# ============================================================

HEAD_COMMON = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-C62DXBY0EC"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-C62DXBY0EC');
</script>

<link rel="stylesheet" href="assets/tailwind.css" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&display=swap" onload="this.onload=null;this.rel='stylesheet'" />
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&display=swap" /></noscript>"""

# ============================================================
# SHARED HEADER (identical across all pages on the site)
# ============================================================

HEADER = """<header class="site-header">
  <div class="header-top">
    <div class="container-x flex items-center justify-between gap-6">
      <a href="/" aria-label="Radiant Rides AutoCare home" class="block flex-shrink-0">
        <img src="brand_assets/6993b18f5356d704752d6ff4_RR_Type_Only.png" alt="Radiant Rides AutoCare" class="wordmark" />
      </a>
      <div class="hidden md:flex items-center gap-5 lg:gap-7">
        <img src="brand_assets/6993c810021c99eafe30839f_Radiant_Rides_logo_art.png" alt="" class="header-logo" />
        <div class="flex flex-col gap-1.5">
          <a href="mailto:hello@radiantridesautocare.com.au" class="contact-row">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>
            <span>hello@radiantridesautocare.com.au</span>
          </a>
          <a href="tel:0449801505" class="contact-row">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <span>0449 801 505</span>
          </a>
          <a href="https://www.instagram.com/radiantrides_autocare/" target="_blank" rel="noopener" class="contact-row">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
            <span>@radiantrides_autocare</span>
          </a>
          <a href="https://www.facebook.com/profile.php?id=61579215043451" target="_blank" rel="noopener" class="contact-row">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5.02 3.66 9.18 8.44 9.94v-7.03H7.9v-2.91h2.54V9.85c0-2.52 1.49-3.92 3.78-3.92 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.78-1.63 1.57v1.89h2.77l-.44 2.91h-2.33V22c4.78-.76 8.43-4.92 8.43-9.94z"/></svg>
            <span>Radiant Rides AutoCare</span>
          </a>
        </div>
      </div>
      <button id="navToggle" class="md:hidden p-2" aria-label="Open menu">
        <svg class="w-7 h-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>

  <div class="header-nav hidden md:block">
    <div class="container-x grid grid-cols-3 items-center py-4">
      <div></div>
      <nav class="hidden md:flex items-center justify-center gap-10 lg:gap-14">
        <a href="/" class="nav-link">Home</a>
        <a href="/about" class="nav-link">About</a>
        <div class="mega-wrap" data-mega="packages">
          <a href="/packages" class="nav-link mega-trigger" aria-haspopup="true" aria-expanded="false">
            Packages
            <svg class="mega-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
          </a>
        </div>
        <a href="/our-work" class="nav-link">Our Work</a>
      </nav>
      <div class="hidden md:flex justify-end">
        <a href="/contact" class="enquire-btn">Enquire Now</a>
      </div>
    </div>
  </div>

  <div class="mega-panel" id="mega-packages" role="menu" aria-label="Packages menu">
    <div class="container-x py-8">
      <div class="text-xs uppercase tracking-[0.18em] text-neutral-400 mb-4">Our Most Popular Packages</div>
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-4">
        <a href="/packages#basic" class="mega-card featured">
          <div class="name">Basic Interior &amp; Exterior</div>
          <div class="price"><span class="from">From</span>$110</div>
          <p class="desc">Two-bucket wash, vacuum, microfibre dry. The everyday refresh.</p>
          <span class="more">Details <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg></span>
        </a>
        <a href="/packages#full-interior" class="mega-card featured">
          <div class="name">Interior Reset &amp; Protection</div>
          <div class="price"><span class="from">From</span>$150</div>
          <p class="desc">Vents, upholstery deep clean or leather reconditioning, dashboard protection.</p>
          <span class="more">Details <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg></span>
        </a>
        <a href="/packages#exterior" class="mega-card featured">
          <div class="name">Paint Enhancement</div>
          <div class="price"><span class="from">From</span>$300</div>
          <p class="desc">Clay bar, decontamination wash, single stage polish, ceramic sealant option.</p>
          <span class="more">Details <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg></span>
        </a>
        <a href="/packages#complete" class="mega-card featured">
          <div class="name">Correction &amp; Coating</div>
          <div class="price"><span class="from">From</span>$1,000</div>
          <p class="desc">Full paint correction, 2-stage cut and polish, ceramic coating.</p>
          <span class="more">Details <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg></span>
        </a>
        <div class="mega-aside">
          <h4>Subscription Detailing</h4>
          <p>Locked-in member rates and priority bookings. Keep your car radiant all month long.</p>
          <a href="/contact" class="text-xs uppercase tracking-[0.16em] font-semibold text-white inline-flex items-center gap-1 mb-3">Enquire <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg></a>
          <div class="border-t border-white/10 pt-3">
            <h4 class="text-sm">Mobile Headlight Restoration</h4>
            <p class="mb-0">Bookable add-on. We come to you. Call-out fee applies.</p>
          </div>
        </div>
      </div>
      <!-- Browse by service (Phase C service pages) -->
      <div class="border-t border-white/10 mt-6 pt-5">
        <div class="text-xs uppercase tracking-[0.18em] text-neutral-400 mb-4">Or browse by service</div>
        <div class="flex flex-wrap gap-2">
          <a href="/ceramic-coating" class="inline-flex items-center px-3.5 py-2 border border-white/15 text-white text-xs uppercase tracking-[0.14em] font-semibold hover:bg-white/5 hover:border-white/30 transition">Ceramic Coating</a>
          <a href="/paint-correction" class="inline-flex items-center px-3.5 py-2 border border-white/15 text-white text-xs uppercase tracking-[0.14em] font-semibold hover:bg-white/5 hover:border-white/30 transition">Paint Correction</a>
          <a href="/pre-sale-detail" class="inline-flex items-center px-3.5 py-2 border border-white/15 text-white text-xs uppercase tracking-[0.14em] font-semibold hover:bg-white/5 hover:border-white/30 transition">Pre-Sale Detail</a>
          <a href="/headlight-restoration" class="inline-flex items-center px-3.5 py-2 border border-white/15 text-white text-xs uppercase tracking-[0.14em] font-semibold hover:bg-white/5 hover:border-white/30 transition">Headlight Restoration</a>
          <a href="/leather-reconditioning" class="inline-flex items-center px-3.5 py-2 border border-white/15 text-white text-xs uppercase tracking-[0.14em] font-semibold hover:bg-white/5 hover:border-white/30 transition">Leather Reconditioning</a>
          <a href="/engine-bay-clean" class="inline-flex items-center px-3.5 py-2 border border-white/15 text-white text-xs uppercase tracking-[0.14em] font-semibold hover:bg-white/5 hover:border-white/30 transition">Engine Bay Clean</a>
          <a href="/advanced-odor-elimination" class="inline-flex items-center px-3.5 py-2 border border-white/15 text-white text-xs uppercase tracking-[0.14em] font-semibold hover:bg-white/5 hover:border-white/30 transition">Odor Elimination</a>
        </div>
      </div>
      <div class="mega-foot mt-5">
        <span class="text-neutral-400">Not sure which one? Tell us about your car and we'll recommend.</span>
        <div class="flex items-center gap-3">
          <a href="tel:0449801505" class="pill"><svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>0449 801 505</a>
          <a href="/packages" class="pill">View all packages <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg></a>
        </div>
      </div>
    </div>
  </div>

  <div id="mobileNav" class="hidden md:hidden border-t border-white/10 bg-black">
    <div class="container-x py-5 flex flex-col gap-3">
      <a href="/" class="nav-link py-2">Home</a>
      <a href="/about" class="nav-link py-2">About</a>
      <details>
        <summary class="nav-link py-2 cursor-pointer flex items-center justify-between">Packages <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></summary>
        <div class="mt-1 pl-4 pb-2 flex flex-col gap-2 text-sm">
          <a href="/packages#basic" class="text-neutral-400 hover:text-white">Basic Interior &amp; Exterior - From $110</a>
          <a href="/packages#full-interior" class="text-neutral-400 hover:text-white">Interior Reset &amp; Protection - From $150</a>
          <a href="/packages#pre-sale" class="text-neutral-400 hover:text-white">Pre Sale Detail - From $225</a>
          <a href="/packages#exterior" class="text-neutral-400 hover:text-white">Paint Enhancement - From $300</a>
          <a href="/packages#complete" class="text-neutral-400 hover:text-white">Correction &amp; Coating - From $1,000</a>
          <a href="/packages" class="text-white font-semibold mt-1">View all packages -&gt;</a>
          <div class="border-t border-white/10 my-2"></div>
          <div class="text-xs uppercase tracking-[0.16em] text-neutral-500 font-semibold pb-1">By service</div>
          <a href="/ceramic-coating" class="text-neutral-400 hover:text-white">Ceramic Coating</a>
          <a href="/paint-correction" class="text-neutral-400 hover:text-white">Paint Correction</a>
          <a href="/pre-sale-detail" class="text-neutral-400 hover:text-white">Pre-Sale Detail</a>
          <a href="/headlight-restoration" class="text-neutral-400 hover:text-white">Headlight Restoration</a>
          <a href="/leather-reconditioning" class="text-neutral-400 hover:text-white">Leather Reconditioning</a>
          <a href="/engine-bay-clean" class="text-neutral-400 hover:text-white">Engine Bay Clean</a>
          <a href="/advanced-odor-elimination" class="text-neutral-400 hover:text-white">Odor Elimination</a>
        </div>
      </details>
      <a href="/our-work" class="nav-link py-2">Our Work</a>
      <a href="/contact" class="enquire-btn mt-2 self-start">Enquire Now</a>
      <div class="pt-4 mt-2 border-t border-white/10 flex flex-col gap-2.5 text-sm">
        <a href="tel:0449801505" class="contact-row">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          <span>0449 801 505</span>
        </a>
        <a href="mailto:hello@radiantridesautocare.com.au" class="contact-row">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>
          <span class="break-all">hello@radiantridesautocare.com.au</span>
        </a>
        <a href="https://www.instagram.com/radiantrides_autocare/" target="_blank" rel="noopener" class="contact-row">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
          <span>@radiantrides_autocare</span>
        </a>
      </div>
    </div>
  </div>
</header>"""

FOOTER = """<footer class="bg-black border-t border-white/10">
  <div class="container-x py-14 grid md:grid-cols-4 gap-10">
    <div class="md:col-span-1">
      <img src="brand_assets/6993b18f5356d704752d6ff4_RR_Type_Only.png" alt="Radiant Rides AutoCare" class="h-10 w-auto mb-5" />
      <p class="text-neutral-400 text-sm leading-relaxed mb-4">
        Professional car detailing studio based in Cranbourne North, serving Melbourne since 2025.
      </p>
      <div class="flex items-center gap-3">
        <a href="https://www.instagram.com/radiantrides_autocare/" target="_blank" rel="noopener" aria-label="Instagram" class="w-10 h-10 flex items-center justify-center bg-white/5 hover:bg-white/15 border border-white/10 transition">
          <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
        </a>
        <a href="https://www.facebook.com/profile.php?id=61579215043451" target="_blank" rel="noopener" aria-label="Facebook" class="w-10 h-10 flex items-center justify-center bg-white/5 hover:bg-white/15 border border-white/10 transition">
          <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor"><path d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5.02 3.66 9.18 8.44 9.94v-7.03H7.9v-2.91h2.54V9.85c0-2.52 1.49-3.92 3.78-3.92 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.78-1.63 1.57v1.89h2.77l-.44 2.91h-2.33V22c4.78-.76 8.43-4.92 8.43-9.94z"/></svg>
        </a>
      </div>
    </div>
    <div>
      <h4 class="text-sm uppercase tracking-[0.16em] text-neutral-500 mb-4">Explore</h4>
      <ul class="space-y-2 text-neutral-300 text-sm">
        <li><a href="/" class="hover:text-white">Home</a></li>
        <li><a href="/about" class="hover:text-white">About</a></li>
        <li><a href="/packages" class="hover:text-white">Packages</a></li>
        <li><a href="/our-work" class="hover:text-white">Our Work</a></li>
        <li><a href="/contact" class="hover:text-white">Contact</a></li>
      </ul>
    </div>
    <div>
      <h4 class="text-sm uppercase tracking-[0.16em] text-neutral-500 mb-4">Contact</h4>
      <ul class="space-y-2 text-neutral-300 text-sm">
        <li><a href="tel:0449801505" class="hover:text-white">0449 801 505</a></li>
        <li><a href="mailto:hello@radiantridesautocare.com.au" class="hover:text-white break-all">hello@radiantridesautocare.com.au</a></li>
        <li><a href="https://maps.app.goo.gl/zjQsW3KK7zboiCJX7" target="_blank" rel="noopener" class="hover:text-white">Cranbourne North, Victoria, Australia</a></li>
      </ul>
    </div>
    <div>
      <h4 class="text-sm uppercase tracking-[0.16em] text-neutral-500 mb-4">Hours</h4>
      <ul class="space-y-2 text-neutral-300 text-sm">
        <li>Mon - Fri: 5pm - 9pm</li>
        <li>Sat - Sun: 7am - 7pm</li>
        <li class="text-neutral-400 text-xs leading-relaxed pt-1">All bookings by appointment only. Call us if you need a same-day service and we'll try our best to help.</li>
        <li class="pt-2">
          <a href="/contact" class="btn btn-primary text-xs">Book in now</a>
        </li>
      </ul>
    </div>
  </div>
  <div class="border-t border-white/10">
    <div class="container-x py-5 flex flex-col md:flex-row justify-between text-xs text-neutral-500 gap-2">
      <div>&copy; <span id="year"></span> Radiant Rides AutoCare. ABN 74 177 391 469. All rights reserved.</div>
      <div>Site by <a href="https://suterasites.com.au" target="_blank" rel="noopener" class="hover:text-white">Sutera Sites</a></div>
    </div>
  </div>
</footer>

<script src="assets/site.js" defer></script>"""

# ============================================================
# SERVICE CONFIGS (one entry per detailing service)
# ============================================================

SERVICES = {
    "ceramic-coating": {
        "label": "Ceramic Coating",
        "service_type_schema": "Ceramic Coating",
        "tagline_short": "paint protection",
        "what_it_does_intro": "It's not wax. It's not a polish. It's a chemically bonded layer that does four specific things to your factory paint.",
        "what_it_does_cards": [
            ("Locks out contamination", "Tar, bug guts, bird droppings and tree sap can't bond directly to the clear coat anymore. They sit on top of the ceramic layer and wash off cleanly."),
            ("Hydrophobic beading", "Water beads up and rolls off instead of clinging. Rain effectively rinses the car as you drive. Drying after a wash is a five-minute job, not twenty."),
            ("UV resistance", "Melbourne sun fades clear coat over years of exposure. Ceramic adds a UV-stable barrier that slows the oxidation that turns paint dull and chalky."),
            ("Deeper gloss", "Light refracts cleanly through a coated surface. Colours look richer, dark cars look wetter, metallic flake actually pops. It's the look you remember from the showroom."),
        ],
        "tiers_h2": "Three ways to protect your paint",
        "tiers_intro": "Entry-level sealant through to a full multi-year ceramic. We talk through which one fits your car and ownership horizon when you book in.",
        "tiers": [
            {
                "name": "Ceramic Sealant Add-On",
                "price": "$50",
                "primary": False,
                "features": [
                    "Spray-applied ceramic sealant",
                    "Months of hydrophobic protection",
                    "Add to any wash or detail package",
                    "Entry-level top-up between bigger jobs",
                ],
            },
            {
                "name": "Paint Enhancement<br/>with Ceramic Sealant",
                "price": "$300",
                "primary": True,
                "features": [
                    "Pre-foam and decontamination wash",
                    "Clay bar removes bonded contamination",
                    "Single stage machine polish",
                    "Choice of spray wax or ceramic sealant",
                    "Wheels cleaned, tyres dressed, windows",
                ],
            },
            {
                "name": "Correction &amp; Coating",
                "price": "$1,000",
                "primary": True,
                "features": [
                    "Everything in Paint Correction",
                    "Two-stage cut and polish",
                    "Multi-year ceramic coating applied",
                    "3 to 8 year longevity depending on product",
                    "Best fit for long-hold ownership",
                ],
            },
        ],
        "schema_offers": [
            ("Ceramic Sealant Add-On", "Spray-on ceramic sealant applied as part of Paint Enhancement. Entry-level protection."),
            ("Paint Enhancement with Ceramic Sealant", "Clay bar, decontamination wash, single stage polish, plus ceramic sealant."),
            ("Correction & Coating", "Full paint correction, 2-stage cut and polish, multi-year ceramic coating."),
        ],
        "tier_select_options": [
            "Ceramic Sealant Add-On - From $50",
            "Paint Enhancement with Ceramic Sealant - From $300",
            "Correction & Coating - From $1,000",
            "Not sure - recommend",
        ],
        "faq_default": [
            ("How long does ceramic coating last?", "Most ceramic coatings hold up between three and eight years depending on the product applied and how the car is maintained. Garage-kept cars and vehicles that get washed properly (no automatic brush washes) hold the gloss and beading longest. We talk you through which tier fits your car and your driving pattern when you book in."),
            ("Do I need paint correction before ceramic coating?", "If you want the ceramic to look its best for years, yes. Coating locks in whatever is on the paint at the time of application, including swirl marks, light scratches and water spots. Our Correction &amp; Coating package handles both stages in one booking so the ceramic is laid down on freshly corrected, perfectly clean paint."),
            ("How long does the booking take?", "Paint Enhancement with a ceramic sealant is typically a single day. Full Correction &amp; Coating usually takes one to two days depending on the size and condition of the vehicle. We confirm the timeline when we quote so you know when to drop off and pick up."),
            ("Can I wash my car normally after a ceramic coating?", "Yes, with two caveats. Skip the automatic brush washes at the local servo because they undo the work. Stick to a two-bucket hand wash with a pH-neutral shampoo. Ceramic makes the wash easier because dirt sheets off rather than bonding to the paint."),
        ],
        "hero_image": "brand_assets/bmw-exterior-04.jpeg",
        "from_price_label": "$300 (sealant) / $1,000 (full)",
    },
    "paint-correction": {
        "label": "Paint Correction",
        "service_type_schema": "Paint Correction",
        "tagline_short": "swirl removal and machine polish",
        "what_it_does_intro": "Paint correction is the multi-stage machine polishing process that removes the swirl marks, holograms and light scratches that build up on every car over time. It's also the prep step before any serious paint protection.",
        "what_it_does_cards": [
            ("Removes swirl marks", "Years of incorrect washing (drive-through car washes, dry rags, paper towels) leave fine circular scratches in the clear coat. Correction levels them out."),
            ("Restores depth and clarity", "Once the micro-scratches are gone, light bounces back cleanly. The colour underneath looks darker, the metallic flake pops, the gloss is back."),
            ("Preps for ceramic coating", "Coating locks in whatever is on the paint at the time of application. Correction is what gets the paint right before that lock-in happens."),
            ("Genuine cut and polish", "Two-stage cut and polish removes deeper defects then refines the finish, rather than glazing over the damage with fillers."),
        ],
        "tiers_h2": "Three correction levels",
        "tiers_intro": "From a single-stage enhancement to a full two-stage cut and polish with ceramic. We assess the paint and recommend the tier that fits the condition.",
        "tiers": [
            {
                "name": "Paint Enhancement",
                "price": "$300",
                "primary": False,
                "features": [
                    "Pre-foam and decontamination wash",
                    "Clay bar removes bonded contamination",
                    "Single stage machine polish",
                    "Removes light swirls and oxidation",
                    "Spray wax or ceramic sealant finish",
                ],
            },
            {
                "name": "Paint Correction",
                "price": "$400",
                "primary": True,
                "features": [
                    "Full decontamination prep",
                    "Targeted multi-pass correction",
                    "Removes deeper swirls and holograms",
                    "Brings back depth and gloss",
                    "Protected with sealant finish",
                ],
            },
            {
                "name": "Correction &amp; Coating",
                "price": "$1,000",
                "primary": True,
                "features": [
                    "Full paint correction included",
                    "Two-stage cut and polish",
                    "Multi-year ceramic coating applied",
                    "Long-haul protection on freshly corrected paint",
                    "Best fit for resale or long-hold ownership",
                ],
            },
        ],
        "schema_offers": [
            ("Paint Enhancement", "Single-stage machine polish with decontamination prep. Removes light swirls and oxidation."),
            ("Paint Correction", "Multi-pass correction that removes deeper swirls and holograms, restoring depth and gloss."),
            ("Correction & Coating", "Full two-stage cut and polish with multi-year ceramic coating applied."),
        ],
        "tier_select_options": [
            "Paint Enhancement - From $300",
            "Paint Correction - From $400",
            "Correction & Coating - From $1,000",
            "Not sure - recommend",
        ],
        "faq_default": [
            ("What is paint correction?", "It's a controlled, machine-led process that removes a thin layer of damaged clear coat to reveal a flat, defect-free surface underneath. Done right, it brings back the depth and gloss that washing alone can't restore."),
            ("Do I need full correction or just enhancement?", "Most daily drivers with swirl marks and dull paint do well with Paint Enhancement. Cars with deeper scratches, holograms from a prior bad polish, or paint that's been neglected for years need full Paint Correction. We assess and quote after seeing the car."),
            ("How long does correction take?", "Paint Enhancement is typically a single day. Full Paint Correction is one to two days. Correction &amp; Coating runs one to two days depending on size and condition. We confirm timelines when we quote."),
            ("Will correction damage the clear coat?", "No, when it's done correctly with the right pads, compounds and machine technique. We measure paint thickness on jobs that require deeper correction so we stay well within safe tolerance."),
        ],
        "hero_image": "brand_assets/bmw-exterior-02.jpeg",
        "from_price_label": "$300 (enhancement) / $1,000 (full)",
    },
    "car-detailing": {
        "label": "Car Detailing",
        "service_type_schema": "Car Detailing",
        "tagline_short": "interior and exterior detail",
        "what_it_does_intro": "Car detailing covers the everyday refresh through to the deep interior reset that takes a tired car back to feeling new. Four core stages run through every booking.",
        "what_it_does_cards": [
            ("Exterior wash and decontamination", "Pre-foam, two-bucket wash, wheels cleaned, tyres dressed, microfibre dry. The base every detail starts from."),
            ("Interior vacuum and deep clean", "Carpets, seats, mats, vents and the spots most washes miss. Upholstery deep clean or leather reconditioning on the bigger packages."),
            ("Surface protection", "Dashboard, centre console and door cards protected so the deep clean stays looking right for longer."),
            ("Glass, plastics, trim", "Windows streak-free, trim restored, plastics dressed. The finishing layer that ties the whole detail together."),
        ],
        "tiers_h2": "Three detailing packages",
        "tiers_intro": "From a quick weekly-driver refresh to a full interior reset. Mix and match with add-ons like odor elimination or leather reconditioning when you enquire.",
        "tiers": [
            {
                "name": "Basic Interior &amp; Exterior",
                "price": "$110",
                "primary": False,
                "features": [
                    "Pre-foam and two-bucket hand wash",
                    "Wheels cleaned, tyres dressed",
                    "Microfibre towel dry",
                    "Interior vacuum, surface wipe-down",
                    "Window cleaning inside and out",
                ],
            },
            {
                "name": "Interior Reset &amp; Protection",
                "price": "$150",
                "primary": True,
                "features": [
                    "Everything in Basic Interior Clean",
                    "Vents cleaned",
                    "Upholstery deep clean or leather reconditioning",
                    "Carpet deep clean",
                    "Dashboard, centre console &amp; door card protection",
                ],
            },
            {
                "name": "Paint Enhancement",
                "price": "$300",
                "primary": True,
                "features": [
                    "Full decontamination wash",
                    "Clay bar pass",
                    "Single stage machine polish",
                    "Wheels, tyres, windows",
                    "Spray wax or ceramic sealant",
                ],
            },
        ],
        "schema_offers": [
            ("Basic Interior & Exterior", "Pre-foam, two-bucket wash, vacuum, microfibre dry. The everyday refresh."),
            ("Interior Reset & Protection", "Vents, upholstery deep clean or leather reconditioning, dashboard protection."),
            ("Paint Enhancement", "Decontamination wash, clay bar, single stage polish, ceramic sealant option."),
        ],
        "tier_select_options": [
            "Basic Interior & Exterior - From $110",
            "Interior Reset & Protection - From $150",
            "Paint Enhancement - From $300",
            "Pre Sale Detail - From $225",
            "Not sure - recommend",
        ],
        "faq_default": [
            ("How long does detailing take?", "Timing depends on the size and condition of the car plus the package you book. A Basic Interior &amp; Exterior typically runs two to three hours. Bigger Interior Reset or Paint Enhancement packages are a half day to full day. We confirm timing when we quote."),
            ("What's the difference between a wash and a detail?", "A wash cleans the outside. A detail cleans the outside AND resets the inside, with deeper attention to vents, carpet, upholstery, trim and surfaces a wash never touches. The result lasts weeks, not days."),
            ("Do you do pre-sale details for cars being listed?", "Yes. Our Pre Sale Detail (from $225) is built specifically for cars being prepared for sale. We focus on the touch points and photo-ready surfaces that buyers actually look at."),
            ("Can I add odor elimination or leather reconditioning?", "Yes. Both run as add-ons to any package. Mention them in the enquiry form or when we call back and we'll factor them into the quote."),
        ],
        "hero_image": "brand_assets/mercedes-interior-front.jpeg",
        "from_price_label": "$110 (basic) / $300 (paint enhancement)",
    },
}

# ============================================================
# PAGE CONFIGS (one entry per suburb LP to build)
# ============================================================

PAGES = [
    {
        "service": "ceramic-coating",
        "suburb": "Narre Warren",
        "slug": "ceramic-coating-narre-warren",
        "drive_min": 15,
        "drive_route": "via Princes Hwy",
        "geo_lat": "-38.0269",
        "geo_lon": "145.3036",
        "intro_paragraphs": [
            "Narre Warren is a city-of-Casey hub with serious daily traffic flowing through Webb Street, Narre Warren-Cranbourne Road and the M1 ramps. Cars in Narre Warren are working hard. Long commutes, school runs, supermarket carparks, freeway grit. The factory clear coat takes a beating from week one.",
            "Ceramic coating is a hard, transparent layer of silica that bonds to the clear coat and stays put for years. Once it's on, dirt sheets off in the rain, washing is faster, and the paint resists the slow oxidation that turns a new car finish dull and chalky by year five. For Narre Warren families running everyday cars hard, it's the upgrade that protects the resale value most.",
            "We're a 15 minute drive from central Narre Warren down to our Cranbourne North studio. Cars are dropped off in the morning and you collect when the work is done, usually same day for Paint Enhancement with a sealant, one to two days for full Correction &amp; Coating.",
        ],
        "surrounding": [
            "Narre Warren South", "Berwick", "Hampton Park", "Hallam", "Endeavour Hills",
            "Cranbourne", "Cranbourne East", "Clyde North", "Hampton Park", "Lynbrook",
            "Lyndhurst", "Doveton",
        ],
        "cross_links": [
            ("Ceramic coating Berwick", "/ceramic-coating-berwick"),
            ("Paint correction Berwick", "/paint-correction-berwick"),
            ("Car detailing Cranbourne", "/car-detailing-cranbourne"),
            ("All packages", "/packages"),
        ],
        "faq_extra": [
            ("Are you mobile? Can you come to Narre Warren?", "We are not a mobile ceramic coating service. Ceramic application needs a controlled environment with the right lighting, temperature, and zero airborne contamination, which is why all coating work is carried out in our Cranbourne North studio. Narre Warren is about a 15 minute drive. We do offer <strong>mobile headlight restoration</strong> as a separate add-on."),
            ("How much is ceramic coating in Narre Warren?", "Pricing starts from $300 for Paint Enhancement with a ceramic sealant and from $1,000 for full Correction &amp; Coating with a multi-year ceramic. Final pricing depends on the vehicle size, current paint condition, and the coating tier you choose. We quote every job individually after we know the vehicle."),
        ],
    },
    {
        "service": "paint-correction",
        "suburb": "Berwick",
        "slug": "paint-correction-berwick",
        "drive_min": 12,
        "drive_route": "via M1",
        "geo_lat": "-38.0309",
        "geo_lon": "145.3471",
        "intro_paragraphs": [
            "Berwick paint takes a beating that you only really notice in direct sunlight. Swirl marks from years of hose-down washes, water spots from the local hard water, the dull haze that creeps over the bonnet and roof as the clear coat oxidises. None of it scrubs off. None of it polishes off in the driveway either. Removing it takes a proper machine correction.",
            "Paint correction is the multi-stage process that levels out the damaged top layer of clear coat to reveal flat, defect-free paint underneath. Done right, the colour looks deeper, the gloss is back, and metallic flake actually pops in the sun. It's the difference between a car that looks washed and a car that looks finished.",
            "We're a 12 minute drive from Berwick to our Cranbourne North studio via the M1. Drop the car in the morning, pick up clean and corrected. Most Paint Enhancement jobs run same day; full correction is one to two days depending on the vehicle and the condition.",
        ],
        "surrounding": [
            "Beaconsfield", "Officer", "Narre Warren South", "Hallam", "Hampton Park",
            "Clyde North", "Cranbourne", "Cranbourne East", "Pakenham", "Endeavour Hills",
            "Lynbrook", "Berwick",
        ],
        "cross_links": [
            ("Ceramic coating Berwick", "/ceramic-coating-berwick"),
            ("Paint correction Clyde North", "/paint-correction-clyde-north"),
            ("Ceramic coating Narre Warren", "/ceramic-coating-narre-warren"),
            ("All packages", "/packages"),
        ],
        "faq_extra": [
            ("Are you mobile? Can you come to Berwick?", "We are not a mobile paint correction service. Machine polishing needs a controlled environment with the right lighting to see defects properly, which is why all correction work is carried out in our Cranbourne North studio. Berwick is about a 12 minute drive."),
            ("How much is paint correction in Berwick?", "Pricing starts from $300 for Paint Enhancement and from $400 for full Paint Correction. Correction &amp; Coating bundles correction with a multi-year ceramic from $1,000. Final pricing depends on vehicle size and current paint condition, quoted after we see the car."),
        ],
    },
    {
        "service": "paint-correction",
        "suburb": "Clyde North",
        "slug": "paint-correction-clyde-north",
        "drive_min": 8,
        "drive_route": "via Berwick-Cranbourne Rd",
        "geo_lat": "-38.0944",
        "geo_lon": "145.3406",
        "intro_paragraphs": [
            "Clyde North is one of the fastest-growing suburbs in Casey, which means a lot of new builds, a lot of new cars in those driveways, and a lot of fresh clear coat that owners want to keep looking new. The catch is that even brand-new cars come off the showroom floor with light swirls and machine-marking from the dealer detail. Paint correction is the first step toward locking that paint in properly.",
            "Paint correction is the multi-stage machine polishing process that removes the micro-scratches, holograms and oxidation that build up in clear coat over time. The result is paint with the depth and gloss it had when it rolled off the line, ready for whatever protection layer you choose to put over the top.",
            "We're an 8 minute drive from Clyde North to our Cranbourne North studio via Berwick-Cranbourne Road. Closest suburb LP we offer for paint correction in the immediate Casey growth corridor. Drop the car in the morning and we'll have you back behind the wheel the same day on most enhancement bookings.",
        ],
        "surrounding": [
            "Clyde", "Cranbourne East", "Cranbourne", "Berwick", "Officer",
            "Pakenham", "Lynbrook", "Lyndhurst", "Cranbourne South", "Cranbourne West",
            "Hampton Park", "Narre Warren South",
        ],
        "cross_links": [
            ("Paint correction Berwick", "/paint-correction-berwick"),
            ("Ceramic coating Berwick", "/ceramic-coating-berwick"),
            ("Car detailing Cranbourne", "/car-detailing-cranbourne"),
            ("All packages", "/packages"),
        ],
        "faq_extra": [
            ("Are you mobile? Can you come to Clyde North?", "We are not a mobile paint correction service. Machine polishing needs a controlled environment with the right lighting to see defects properly, which is why all correction work is carried out in our Cranbourne North studio. Clyde North is about an 8 minute drive."),
            ("My car is brand new. Does it need correction?", "Often, yes. New cars usually come off the dealer detail with light swirls and machine-marking from a rushed polish. A Paint Enhancement before you apply any ceramic locks in a defect-free finish from day one. We're happy to assess and tell you straight if it doesn't need it."),
        ],
    },
    {
        "service": "car-detailing",
        "suburb": "Cranbourne",
        "slug": "car-detailing-cranbourne",
        "drive_min": 5,
        "drive_route": "local",
        "geo_lat": "-38.1099",
        "geo_lon": "145.2829",
        "intro_paragraphs": [
            "Cranbourne is our home patch. The studio is a few minutes up the road in Cranbourne North, and a good slice of our regulars come from Cranbourne, Cranbourne East, Cranbourne West and the surrounding pockets. If you're after a proper detail without having to drive halfway across Melbourne, you're already close.",
            "Detailing covers more ground than people assume. A weekly-driver wash and vacuum, a deep interior reset that pulls years of school-run wear out of the upholstery, or a Paint Enhancement that takes the bonnet from dull to glossy. Same studio, three different jobs, depending on what your car actually needs.",
            "Five minute drive from central Cranbourne. Drop off in the morning, we send updates through the day, pick up clean. Most Basic and Interior Reset jobs are same day, and we'll always be straight about timing when we quote.",
        ],
        "surrounding": [
            "Cranbourne East", "Cranbourne West", "Cranbourne North", "Cranbourne South", "Clyde North",
            "Clyde", "Lynbrook", "Lyndhurst", "Hampton Park", "Botanic Ridge",
            "Junction Village", "Skye",
        ],
        "cross_links": [
            ("Car detailing Pakenham", "/car-detailing-pakenham"),
            ("Ceramic coating Berwick", "/ceramic-coating-berwick"),
            ("Paint correction Clyde North", "/paint-correction-clyde-north"),
            ("All packages", "/packages"),
        ],
        "faq_extra": [
            ("Are you mobile? Can you come to Cranbourne?", "We are not a mobile detailing service. All general detailing is carried out at our Cranbourne North studio, about 5 minutes from central Cranbourne. We do offer <strong>mobile headlight restoration</strong> as a separate add-on."),
            ("How much is car detailing in Cranbourne?", "Pricing starts from $110 for our Basic Interior &amp; Exterior package and $150 for Interior Reset &amp; Protection. Paint Enhancement is from $300. Add-ons like odor elimination, leather reconditioning and engine bay clean are priced on top. We quote individually after knowing the vehicle."),
        ],
    },
    {
        "service": "car-detailing",
        "suburb": "Pakenham",
        "slug": "car-detailing-pakenham",
        "drive_min": 20,
        "drive_route": "via Princes Hwy / M1",
        "geo_lat": "-38.0719",
        "geo_lon": "145.4843",
        "intro_paragraphs": [
            "Pakenham is one of the biggest growth corridors in the south-east, with the kind of long commute distances that put serious mileage on a car. Daily-driver paint gets coated in road grime, interiors collect the dust and crumb load of a thousand school runs and coffee stops, and most owners don't have the time on a Sunday to actually reset all of it. That's what a proper detail does.",
            "Detailing isn't a wash. A wash cleans the outside. A detail cleans the outside AND resets the inside, with deeper attention to vents, carpet, upholstery, trim and surfaces a wash never touches. The result holds for weeks, not days, which is why most of our Pakenham regulars are on a roughly six-week rotation.",
            "We're a 20 minute drive from Pakenham to our Cranbourne North studio via the Princes Highway or M1. Drop off in the morning, pick up clean. Worth coordinating with another errand in the Cranbourne or Berwick direction so the trip earns its keep.",
        ],
        "surrounding": [
            "Officer", "Beaconsfield", "Berwick", "Pakenham South", "Pakenham Upper",
            "Cardinia", "Nar Nar Goon", "Bunyip", "Cockatoo", "Emerald",
            "Narre Warren", "Endeavour Hills",
        ],
        "cross_links": [
            ("Car detailing Cranbourne", "/car-detailing-cranbourne"),
            ("Ceramic coating Berwick", "/ceramic-coating-berwick"),
            ("Paint correction Berwick", "/paint-correction-berwick"),
            ("All packages", "/packages"),
        ],
        "faq_extra": [
            ("Are you mobile? Can you come to Pakenham?", "We are not a mobile detailing service. All general detailing is carried out at our Cranbourne North studio, about 20 minutes from Pakenham via the M1. We do offer <strong>mobile headlight restoration</strong> as a separate add-on, which may suit longer-distance bookings."),
            ("Is it worth the drive from Pakenham?", "Most of our Pakenham regulars combine the drop-off with another errand in the Cranbourne or Berwick direction. A proper detail holds for weeks, not days, so the trip earns its keep on the back of a single booking."),
        ],
    },
]

# ============================================================
# BUILDERS
# ============================================================

def build_what_it_does_cards(cards):
    icons = [
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 2.5l8 3v6c0 5-3.5 8.7-8 10-4.5-1.3-8-5-8-10v-6l8-3z"/></svg>',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 2.5s7 7.5 7 12a7 7 0 1 1-14 0c0-4.5 7-12 7-12z"/></svg>',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="5"/><path d="M12 1v3M12 20v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M1 12h3M20 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/></svg>',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="4 12 10 18 20 6"/></svg>',
    ]
    out = []
    for i, (title, body) in enumerate(cards):
        out.append(f"""      <div class="service-card">
        <div class="service-icon">
          {icons[i % 4]}
        </div>
        <h3 class="text-xl mb-2">{title}</h3>
        <p class="text-neutral-400 text-sm leading-relaxed">{body}</p>
      </div>""")
    return "\n".join(out)


def build_tier_cards(tiers):
    tick = '<svg class="feature-tick" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>'
    out = []
    for tier in tiers:
        features = "\n          ".join(
            f'<div class="feature-row">{tick}{f}</div>' for f in tier["features"]
        )
        btn_class = "btn btn-primary" if tier["primary"] else "btn btn-secondary"
        out.append(f"""      <div class="price-card">
        <div class="text-center mb-6">
          <h3 class="text-lg font-semibold text-white mb-3">{tier["name"]}</h3>
          <div class="text-xs uppercase tracking-[0.16em] text-neutral-400 mb-1">From</div>
          <div class="price-amount">{tier["price"]}</div>
        </div>
        <div class="flex-1 mb-6">
          {features}
        </div>
        <a href="#enquire" class="{btn_class} w-full">Enquire</a>
      </div>""")
    return "\n".join(out)


def build_suburb_chips(suburbs):
    out = []
    for s in suburbs:
        out.append(f'      <div class="border border-white/10 px-4 py-3 text-center"><p class="text-neutral-300 text-sm font-semibold">{s}</p></div>')
    return "\n".join(out)


def build_cross_link_pills(links):
    out = []
    for label, href in links:
        out.append(f'      <a href="{href}" class="pill border border-white/15 px-4 py-2 text-white hover:bg-white/5">{label}</a>')
    return "\n".join(out)


def build_faq_html(entries):
    chev = '<svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>'
    out = []
    for q, a in entries:
        out.append(f"""      <details>
        <summary>{q}
          {chev}
        </summary>
        <p>{a}</p>
      </details>""")
    return "\n".join(out)


def build_schema_offers(offers):
    parts = []
    for name, desc in offers:
        parts.append(
            f'          {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "{name}", "description": "{desc}" }} }}'
        )
    return ",\n".join(parts)


def build_faq_schema(entries):
    parts = []
    for q, a in entries:
        # Strip simple HTML tags from FAQ schema text for safety
        text = a.replace("<strong>", "").replace("</strong>", "").replace("&amp;", "and")
        q_clean = q.replace("&amp;", "and")
        parts.append(
            "        {\n"
            '          "@type": "Question",\n'
            f'          "name": "{q_clean}",\n'
            f'          "acceptedAnswer": {{ "@type": "Answer", "text": "{text}" }}\n'
            "        }"
        )
    return ",\n".join(parts)


def build_select_options(options):
    out = []
    for opt in options:
        v = opt.replace("&", "and")
        out.append(f'            <option value="{opt}">{v}</option>')
    return "\n".join(out)


def build_page(page):
    s = SERVICES[page["service"]]
    suburb = page["suburb"]
    slug = page["slug"]
    canonical = f"{SITE}/{slug}"
    title = f"{s['label']} {suburb} | Radiant Rides AutoCare"
    description = f"Professional {s['label'].lower()} for {suburb} drivers. {s['label']} at our Cranbourne North studio, {page['drive_min']} minutes from {suburb}. Enquire today."
    og_short = f"{s['label']} {suburb} | Radiant Rides AutoCare"
    og_desc = f"{s['label']} for {suburb} drivers. Booked in at our Cranbourne North studio, {page['drive_min']} minutes from {suburb}."

    faq_combined = s["faq_default"] + page.get("faq_extra", [])

    intro_paras_html = "\n        ".join(f"<p>{p}</p>" for p in page["intro_paragraphs"])

    what_cards = build_what_it_does_cards(s["what_it_does_cards"])
    tier_cards = build_tier_cards(s["tiers"])
    chips = build_suburb_chips(page["surrounding"])
    pills = build_cross_link_pills(page["cross_links"])
    faq_html = build_faq_html(faq_combined)
    schema_offers = build_schema_offers(s["schema_offers"])
    faq_schema = build_faq_schema(faq_combined)
    select_options = build_select_options(s["tier_select_options"])

    area_served_schema = ",\n".join(
        f'        {{ "@type": "City", "name": "{name}" }}'
        for name in [suburb] + page["surrounding"][:4]
    )

    form_subject = f"New {suburb} {s['label'].lower()} enquiry from radiantridesautocare.com.au"

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{description}" />
<meta name="google-site-verification" content="GEjj3uAIpsoPo9sPHQSo7hQLPrSucyHd-c6V0Ak8Ufg" />

<meta name="geo.region" content="AU-VIC" />
<meta name="geo.placename" content="{suburb}" />
<meta name="geo.position" content="{page['geo_lat']};{page['geo_lon']}" />
<meta name="ICBM" content="{page['geo_lat']}, {page['geo_lon']}" />

<meta property="og:title" content="{og_short}" />
<meta property="og:description" content="{og_desc}" />
<meta property="og:image" content="{SITE}/{s['hero_image']}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:type" content="website" />
<meta name="twitter:card" content="summary_large_image" />

<link rel="icon" type="image/png" sizes="32x32" href="brand_assets/699659fa91a4b7a50b6a86e0_favicon-32x32.png" />
<link rel="apple-touch-icon" href="brand_assets/699aee6a8a929099d7bd579d_RRAC_WEBCLIP.png" />

<link rel="canonical" href="{canonical}" />

{HEAD_COMMON}

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "AutoBodyShop",
      "@id": "{SITE}/#business",
      "name": "Radiant Rides AutoCare",
      "image": "{SITE}/brand_assets/6993c810021c99eafe30839f_Radiant_Rides_logo_art.png",
      "url": "{SITE}/",
      "telephone": "+61449801505",
      "email": "hello@radiantridesautocare.com.au",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "Crestway Dr",
        "addressLocality": "Cranbourne North",
        "addressRegion": "VIC",
        "addressCountry": "AU"
      }},
      "areaServed": [
{area_served_schema}
      ],
      "priceRange": "$$"
    }},
    {{
      "@type": "Service",
      "serviceType": "{s['service_type_schema']}",
      "name": "{s['label']} {suburb}",
      "description": "Professional {s['label'].lower()} for {suburb} vehicles. Carried out in-studio at our Cranbourne North location.",
      "provider": {{ "@id": "{SITE}/#business" }},
      "areaServed": [
        {{ "@type": "City", "name": "{suburb}" }}
      ],
      "hasOfferCatalog": {{
        "@type": "OfferCatalog",
        "name": "{s['label']} options for {suburb} drivers",
        "itemListElement": [
{schema_offers}
        ]
      }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Packages", "item": "{SITE}/packages" }},
        {{ "@type": "ListItem", "position": 3, "name": "{s['label']} {suburb}", "item": "{canonical}" }}
      ]
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
{faq_schema}
      ]
    }}
  ]
}}
</script>

<link rel="stylesheet" href="assets/site.css" />
</head>

<body>

{HEADER}

<nav aria-label="Breadcrumb" class="border-b border-white/10 bg-black">
  <div class="container-x py-3">
    <ol class="flex items-center gap-2 text-xs text-neutral-400">
      <li><a href="/" class="hover:text-white">Home</a></li>
      <li aria-hidden="true" class="text-neutral-600">/</li>
      <li><a href="/packages" class="hover:text-white">Packages</a></li>
      <li aria-hidden="true" class="text-neutral-600">/</li>
      <li class="text-white" aria-current="page">{s['label']} {suburb}</li>
    </ol>
  </div>
</nav>

<section class="relative hero-bg overflow-hidden">
  <img src="{s['hero_image']}" alt="" class="absolute inset-0 w-full h-full object-cover" />
  <div class="relative z-10 container-x py-20 md:py-28">
    <div class="max-w-3xl">
      <div class="tagline mb-5">Serving {suburb} from Cranbourne North</div>
      <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl leading-[1.05] mb-6">
        {s['label']}<br class="hidden sm:block" />
        <span>in {suburb}</span>
      </h1>
      <p class="text-lg md:text-xl text-neutral-300 max-w-2xl mb-9 leading-relaxed">
        Professional {s['label'].lower()} for {suburb} drivers. Booked in at our Cranbourne North studio, {page['drive_min']} minutes from {suburb}.
      </p>
      <div class="flex flex-wrap gap-3">
        <a href="#enquire" class="btn btn-primary">Get a quote</a>
        <a href="tel:0449801505" class="btn btn-secondary">Call 0449 801 505</a>
      </div>
    </div>
  </div>
</section>

<section class="py-20 md:py-28">
  <div class="container-x grid lg:grid-cols-5 gap-12 lg:gap-16">
    <div class="lg:col-span-3">
      <div class="tagline mb-4">{suburb} {s['tagline_short']}</div>
      <h2 class="text-3xl md:text-5xl mb-7 uppercase leading-tight">Why {suburb} drivers book {s['label'].lower()}</h2>
      <div class="space-y-5 text-neutral-300 text-lg leading-relaxed">
        {intro_paras_html}
      </div>
    </div>
    <aside class="lg:col-span-2">
      <div class="sub-card p-7 md:p-9">
        <div class="tagline mb-4">At a glance</div>
        <h3 class="text-2xl mb-5">{suburb} to our studio</h3>
        <ul class="space-y-3 text-neutral-200 text-base">
          <li class="flex justify-between border-b border-white/10 pb-3"><span class="text-neutral-400">Drive time</span><span class="font-semibold">~{page['drive_min']} min {page['drive_route']}</span></li>
          <li class="flex justify-between border-b border-white/10 pb-3"><span class="text-neutral-400">From</span><span class="font-semibold">{suburb}</span></li>
          <li class="flex justify-between border-b border-white/10 pb-3"><span class="text-neutral-400">To</span><span class="font-semibold">Cranbourne North studio</span></li>
          <li class="flex justify-between border-b border-white/10 pb-3"><span class="text-neutral-400">Booking</span><span class="font-semibold">Drop-off in studio</span></li>
          <li class="flex justify-between"><span class="text-neutral-400">From price</span><span class="font-semibold">{s['from_price_label']}</span></li>
        </ul>
        <a href="#enquire" class="btn btn-primary w-full mt-6">Enquire now</a>
      </div>
    </aside>
  </div>
</section>

<div class="section-divider"></div>

<section class="py-20 md:py-28">
  <div class="container-x">
    <div class="max-w-2xl mb-14">
      <div class="tagline mb-4">The detail</div>
      <h2 class="text-3xl md:text-5xl mb-5 uppercase leading-tight">What {s['label'].lower()} actually does</h2>
      <p class="text-neutral-400 text-lg leading-relaxed">{s['what_it_does_intro']}</p>
    </div>
    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
{what_cards}
    </div>
  </div>
</section>

<section class="py-20 md:py-28 bg-[#0a0a0a]">
  <div class="container-x">
    <div class="max-w-2xl mx-auto text-center mb-14">
      <div class="tagline mb-4">{s['label']} tiers</div>
      <h2 class="text-3xl md:text-5xl mb-5 uppercase">{s['tiers_h2']}</h2>
      <p class="text-neutral-400 text-lg">{s['tiers_intro']}</p>
    </div>
    <div class="grid md:grid-cols-3 gap-5">
{tier_cards}
    </div>
    <p class="text-center text-neutral-500 text-sm mt-8">Final pricing depends on vehicle size and current paint condition. We quote every job after seeing the car.</p>
  </div>
</section>

<section class="py-20 md:py-28">
  <div class="container-x">
    <div class="max-w-2xl mb-14">
      <div class="tagline mb-4">How it runs</div>
      <h2 class="text-3xl md:text-5xl mb-5 uppercase leading-tight">From your enquiry to a finished car</h2>
      <p class="text-neutral-400 text-lg leading-relaxed">Same six steps on every {suburb} job. No surprises, no scope creep.</p>
    </div>
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div class="service-card">
        <div class="text-xs uppercase tracking-[0.16em] text-[color:var(--accent)] mb-2 font-semibold">Step 01</div>
        <h3 class="text-xl mb-2">Enquire</h3>
        <p class="text-neutral-400 text-sm leading-relaxed">Drop your vehicle make, model, year and a photo of the current condition through the form below or by SMS.</p>
      </div>
      <div class="service-card">
        <div class="text-xs uppercase tracking-[0.16em] text-[color:var(--accent)] mb-2 font-semibold">Step 02</div>
        <h3 class="text-xl mb-2">Quote</h3>
        <p class="text-neutral-400 text-sm leading-relaxed">We come back within 24 hours with a tier recommendation and a fixed price for your specific car.</p>
      </div>
      <div class="service-card">
        <div class="text-xs uppercase tracking-[0.16em] text-[color:var(--accent)] mb-2 font-semibold">Step 03</div>
        <h3 class="text-xl mb-2">Book</h3>
        <p class="text-neutral-400 text-sm leading-relaxed">Pick a date that works. Larger jobs need a one or two day slot, so we plan around your week.</p>
      </div>
      <div class="service-card">
        <div class="text-xs uppercase tracking-[0.16em] text-[color:var(--accent)] mb-2 font-semibold">Step 04</div>
        <h3 class="text-xl mb-2">Drop off</h3>
        <p class="text-neutral-400 text-sm leading-relaxed">{page['drive_min']} minute drive from {suburb} {page['drive_route']}. Drop in the morning, we send updates through the day.</p>
      </div>
      <div class="service-card">
        <div class="text-xs uppercase tracking-[0.16em] text-[color:var(--accent)] mb-2 font-semibold">Step 05</div>
        <h3 class="text-xl mb-2">In studio</h3>
        <p class="text-neutral-400 text-sm leading-relaxed">Decontamination, machine work and finishing carried out in our controlled studio environment.</p>
      </div>
      <div class="service-card">
        <div class="text-xs uppercase tracking-[0.16em] text-[color:var(--accent)] mb-2 font-semibold">Step 06</div>
        <h3 class="text-xl mb-2">Hand back</h3>
        <p class="text-neutral-400 text-sm leading-relaxed">We walk you around the finish, brief you on the maintenance routine, and you drive home.</p>
      </div>
    </div>
  </div>
</section>

<section class="py-16 md:py-20 bg-[#0a0a0a]">
  <div class="container-x">
    <div class="max-w-2xl mb-10">
      <div class="tagline mb-4">Service area</div>
      <h2 class="text-2xl md:text-4xl uppercase mb-3 leading-tight">Around {suburb}</h2>
      <p class="text-neutral-400 text-base leading-relaxed">Drivers from these neighbouring suburbs also book in at our Cranbourne North studio.</p>
    </div>
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
{chips}
    </div>
    <div class="mt-8 flex flex-wrap gap-3 text-sm">
{pills}
    </div>
  </div>
</section>

<section class="py-20 md:py-28">
  <div class="container-x max-w-3xl">
    <div class="text-center mb-14">
      <div class="tagline mb-4">FAQs</div>
      <h2 class="text-3xl md:text-5xl">{s['label']} {suburb} - FAQs</h2>
    </div>
    <div class="faq">
{faq_html}
    </div>
  </div>
</section>

<section class="cta-banner py-16 md:py-24 px-6 md:px-10 text-center">
  <div class="max-w-4xl mx-auto">
    <h2 class="text-3xl md:text-5xl text-white mb-4">Ready to book your {suburb} car in?</h2>
    <p class="text-white/90 max-w-2xl mx-auto text-lg mb-7">Tell us about your vehicle and current condition. We'll come back with a {suburb} quote within 24 hours.</p>
    <div class="flex flex-wrap gap-3 justify-center">
      <a href="#enquire" class="btn btn-dark">Get a quote</a>
      <a href="tel:0449801505" class="btn btn-secondary">Call 0449 801 505</a>
    </div>
  </div>
</section>

<section id="enquire" class="py-20 md:py-28 bg-white text-neutral-900">
  <div class="container-x grid lg:grid-cols-5 gap-10 lg:gap-14 items-start">
    <div class="lg:col-span-2">
      <div class="inline-block px-3 py-1 border border-neutral-300 text-xs uppercase tracking-[0.18em] text-neutral-600 mb-5">{suburb} enquiries</div>
      <h2 class="text-3xl md:text-5xl text-neutral-950 mb-4 leading-tight">Quote my {s['label'].lower()}</h2>
      <p class="text-neutral-700 text-lg mb-8">Drop your car details. We'll get back to you within 24 hours with a fixed {suburb} quote.</p>
      <div class="space-y-3">
        <a href="tel:0449801505" class="group flex items-center gap-4 bg-neutral-100 hover:bg-neutral-200 transition p-5">
          <div class="w-10 h-10 bg-neutral-900 text-white flex items-center justify-center flex-shrink-0">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          </div>
          <div>
            <div class="text-xs uppercase tracking-[0.18em] text-neutral-500 mb-0.5">Phone</div>
            <div class="text-base font-semibold text-neutral-950">0449 801 505</div>
          </div>
        </a>
        <a href="mailto:hello@radiantridesautocare.com.au" class="group flex items-center gap-4 bg-neutral-100 hover:bg-neutral-200 transition p-5">
          <div class="w-10 h-10 bg-neutral-900 text-white flex items-center justify-center flex-shrink-0">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>
          </div>
          <div>
            <div class="text-xs uppercase tracking-[0.18em] text-neutral-500 mb-0.5">Email</div>
            <div class="text-base font-semibold text-neutral-950 break-all">hello@radiantridesautocare.com.au</div>
          </div>
        </a>
        <a href="https://maps.app.goo.gl/zjQsW3KK7zboiCJX7" target="_blank" rel="noopener" class="group flex items-center gap-4 bg-neutral-100 hover:bg-neutral-200 transition p-5">
          <div class="w-10 h-10 bg-neutral-900 text-white flex items-center justify-center flex-shrink-0">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          </div>
          <div>
            <div class="text-xs uppercase tracking-[0.18em] text-neutral-500 mb-0.5">Studio ({page['drive_min']} min from {suburb})</div>
            <div class="text-base font-semibold text-neutral-950">Cranbourne North, VIC</div>
          </div>
        </a>
      </div>
    </div>

    <div class="lg:col-span-3 bg-neutral-50 border border-neutral-200 p-6 md:p-10">
      <h3 class="text-xl md:text-2xl text-neutral-950 font-bold mb-2">Send us a message</h3>
      <p class="text-neutral-600 mb-6">Tell us about your car and the tier you're thinking. We'll come back with a {suburb} quote.</p>
      <form action="https://formspree.io/f/mojrwrgw" method="POST" class="space-y-4">
        <input type="hidden" name="_subject" value="{form_subject}" />
        <input type="hidden" name="_next" value="https://www.radiantridesautocare.com.au/thank-you" />
        <input type="hidden" name="_source_page" value="{slug}" />
        <input type="hidden" name="service_interest" value="{s['label']}" />
        <input type="hidden" name="suburb_interest" value="{suburb}" />

        <div class="grid sm:grid-cols-2 gap-4">
          <label class="block">
            <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Name</span>
            <input type="text" name="name" required class="form-input" placeholder="Your name" />
          </label>
          <label class="block">
            <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Phone</span>
            <input type="tel" name="phone" class="form-input" placeholder="0400 000 000" />
          </label>
        </div>
        <label class="block">
          <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Email</span>
          <input type="email" name="email" required class="form-input" placeholder="you@example.com" />
        </label>
        <div class="grid sm:grid-cols-2 gap-4">
          <label class="block">
            <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Vehicle</span>
            <input type="text" name="vehicle" class="form-input" placeholder="e.g. 2018 Mazda CX-5" />
          </label>
          <label class="block">
            <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Suburb</span>
            <input type="text" name="suburb" class="form-input" placeholder="{suburb}" value="{suburb}" />
          </label>
        </div>
        <label class="block">
          <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Tier</span>
          <select name="package" class="form-input">
            <option value="">Select a tier</option>
{select_options}
          </select>
        </label>
        <label class="block">
          <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Message</span>
          <textarea name="message" rows="5" class="form-input" placeholder="Tell us about your car and what you're after."></textarea>
        </label>
        <div class="pt-2">
          <button type="submit" class="btn btn-primary w-full sm:w-auto">Send enquiry</button>
          <p class="text-xs text-neutral-500 mt-3">We respond within 24 hours.</p>
        </div>
      </form>
    </div>
  </div>
</section>

{FOOTER}

</body>
</html>
"""


# ============================================================
# PHASE C - SERVICE HUB PAGES (Melbourne-wide)
# ============================================================
# One per service. Hand-built /ceramic-coating.html is the pattern-setter (C2).
# This script generates C3-C8.

SERVICE_HUBS = [
    {
        # C3 - Paint Correction (Melbourne-wide hub)
        "slug": "paint-correction",
        "label": "Paint Correction",
        "service_type_schema": "Paint Correction",
        "title": "Paint Correction Melbourne | Radiant Rides AutoCare",
        "description": "Professional paint correction in Melbourne. Swirl removal, machine polish, and clear-coat restoration at our Cranbourne North studio. From $300.",
        "og_description": "Machine polishing and swirl removal at our Cranbourne North studio. Single-stage enhancement through to full two-stage correction.",
        "hero_image": "brand_assets/bmw-exterior-02.jpeg",
        "hero_subhead": "Swirl removal, machine polish, and clear-coat restoration. All work in our Cranbourne North studio.",
        "intro_h2": "Long-haul gloss, properly restored",
        "intro_paragraphs": [
            "Paint correction is the multi-stage machine polishing process that removes the swirl marks, holograms, water spots and light scratches that build up in clear coat over time. Done right, it brings back the depth and gloss that washing alone can't restore.",
            "Most cars in Melbourne pick up a layer of micro-defects within the first two or three years. Sponge washes, automatic brush washes, dust on a dry car wiped with a microfibre, the wrong drying technique - all of it leaves marks. They're invisible in overcast light. In direct sun they show up as a haze and a spider-web pattern across the bonnet, roof and boot lid.",
            "We run three tiers of correction. A single-stage Paint Enhancement removes the light stuff. A full Paint Correction tackles deeper swirls and holograms. Correction &amp; Coating bundles the correction with a multi-year ceramic so the freshly corrected paint gets locked in. Right tier depends on the car and the condition.",
            "All correction work happens at our Cranbourne North studio. Machine polishing needs controlled lighting to see defects properly, which is why this isn't a service we do mobile. The studio is within a 20-minute drive of Berwick, Narre Warren, Cranbourne, Clyde North, Pakenham, Beaconsfield, Officer and Frankston.",
        ],
        "at_a_glance_label": "Paint correction, Radiant Rides",
        "at_a_glance_rows": [
            ("Studio", "Cranbourne North, VIC"),
            ("Tiers", "3 (enhancement / correction / full)"),
            ("From", "$300 (Paint Enhancement)"),
            ("Full correction + coating", "From $1,000"),
            ("Turnaround", "1 to 2 days"),
            ("Booking", "Drop-off in studio"),
        ],
        "what_it_does_intro": "Correction isn't a wax or a one-pass polish. It's a controlled removal of damaged clear coat to reveal flat, defect-free paint underneath. Four specific outcomes.",
        "what_it_does_cards": [
            ("Removes swirl marks", "Years of incorrect washing (drive-through brushes, dry rags, paper towels) leave fine circular scratches in the clear coat. Correction levels them out."),
            ("Restores depth and clarity", "Once the micro-scratches are gone, light bounces back cleanly. The colour underneath looks darker, the metallic flake pops, the gloss is back."),
            ("Preps for ceramic coating", "Coating locks in whatever is on the paint at the time of application. Correction is what gets the paint right before that lock-in happens."),
            ("True cut and polish", "Two-stage cut and polish removes deeper defects then refines the finish, rather than glazing over the damage with fillers."),
        ],
        "tiers_h2": "Three correction tiers",
        "tiers_intro": "From a single-stage enhancement to a full two-stage cut and polish with ceramic. We assess the paint and recommend the tier that fits the condition.",
        "tiers": [
            {
                "name": "Paint Enhancement",
                "price": "$300",
                "primary": False,
                "features": [
                    "Pre-foam and decontamination wash",
                    "Clay bar removes bonded contamination",
                    "Single stage machine polish",
                    "Removes light swirls and oxidation",
                    "Spray wax or ceramic sealant finish",
                ],
            },
            {
                "name": "Paint Correction",
                "price": "$400",
                "primary": True,
                "features": [
                    "Full decontamination prep",
                    "Targeted multi-pass correction",
                    "Removes deeper swirls and holograms",
                    "Brings back depth and gloss",
                    "Protected with sealant finish",
                ],
            },
            {
                "name": "Correction &amp; Coating",
                "price": "$1,000",
                "primary": True,
                "features": [
                    "Full paint correction included",
                    "Two-stage cut and polish",
                    "Multi-year ceramic coating applied",
                    "Long-haul protection on freshly corrected paint",
                    "Best fit for resale or long-hold ownership",
                ],
            },
        ],
        "suitable_for_h2": "Cars that earn back the correction spend",
        "suitable_for_intro": "Paint correction pays off most on these ownership patterns.",
        "suitable_for_cards": [
            ("Daily-driven swirled paint", "Cars three years and older with visible swirl marks in direct sun. Correction returns the finish closer to factory than you'd think possible."),
            ("Pre-coating prep", "About to apply ceramic? Correction comes first. The coating bonds to whatever is on the paint, so you want that surface defect-free."),
            ("Resale prep", "A corrected finish reads as 'looked after' on a test drive and supports the asking price. Especially true above $30k."),
            ("Dark-coloured cars", "Black, dark blue, deep red. Swirls show worst on dark paint and correction has the most visible impact."),
            ("Performance and prestige", "Cars where the paint is part of the appeal. European metallic finishes, sports cars driven hard, classic restorations."),
            ("Post-repaint correction", "Paint just back from panel beaters? Even good shops leave fine machine marks. A correction pass refines that finish before you take delivery."),
        ],
        "maintenance_h2": "After the correction",
        "maintenance_subhead": "Correction restores the finish. How you wash it from here decides how long the result lasts.",
        "maintenance_blocks": [
            {
                "h3": "First week",
                "items": [
                    "Avoid the first automatic brush wash for the rest of the car's life.",
                    "Light hand wash only for the first week.",
                    "If you've also coated, follow the ceramic cure guidance.",
                    "Park indoors or covered where possible while the sealant cures.",
                ],
            },
            {
                "h3": "Ongoing maintenance",
                "items": [
                    "Two-bucket hand wash with pH-neutral shampoo. Twice a month is plenty.",
                    "No automatic brush washes. They are the leading cause of new swirls.",
                    "Microfibre drying towel, not paper or hose-dry.",
                    "Yearly check-in detail keeps the finish where we left it.",
                ],
            },
        ],
        "suburb_cross_links": [
            ("Paint Correction Berwick", "Berwick paint correction at our Cranbourne North studio. 12 min drive via M1.", "/paint-correction-berwick"),
            ("Paint Correction Clyde North", "Defect-free paint for the Clyde North growth corridor. 8 min drive.", "/paint-correction-clyde-north"),
        ],
        "faq": [
            ("What is paint correction?", "It's a controlled machine-led process that removes a thin layer of damaged clear coat to reveal a flat, defect-free surface underneath. Done right, it brings back the depth and gloss that washing alone can't restore."),
            ("Do I need full correction or just enhancement?", "Most daily drivers with swirl marks and dull paint do well with Paint Enhancement. Cars with deeper scratches, holograms from a prior bad polish, or paint that's been neglected for years need full Paint Correction. We assess and quote after seeing the car."),
            ("How long does correction take?", "Paint Enhancement is typically a single day. Full Paint Correction is one to two days. Correction &amp; Coating runs one to two days depending on size and condition. We confirm timelines when we quote."),
            ("Will correction damage the clear coat?", "No, when it's done correctly with the right pads, compounds and machine technique. We measure paint thickness on jobs that require deeper correction so we stay well within safe tolerance."),
            ("Will the swirls come back?", "Not if you wash the car correctly. The leading cause of new swirls is automatic brush washes and dry-wiping with the wrong cloth. Two-bucket hand wash with pH-neutral shampoo is the rule."),
            ("Should I correct before applying ceramic?", "Yes. Ceramic coating locks in whatever is on the paint at the time of application, including swirl marks. Correction gets the surface right before the coating goes down."),
            ("Are you mobile? Can you come to me?", "No. Paint correction requires controlled studio lighting to see defects properly during the work. All correction is carried out at our Cranbourne North studio. We do offer <strong>mobile headlight restoration</strong> as a separate add-on."),
            ("How much does paint correction cost in Melbourne?", "From $300 for Paint Enhancement, from $400 for full Paint Correction, from $1,000 for Correction &amp; Coating with multi-year ceramic. Final pricing depends on vehicle size and current paint condition, quoted after we see the car."),
        ],
        "schema_offers": [
            ("Paint Enhancement", "Single-stage machine polish with decontamination prep. Removes light swirls and oxidation."),
            ("Paint Correction", "Multi-pass correction that removes deeper swirls and holograms, restoring depth and gloss."),
            ("Correction & Coating", "Full two-stage cut and polish with multi-year ceramic coating applied."),
        ],
        "tier_select_options": [
            "Paint Enhancement - From $300",
            "Paint Correction - From $400",
            "Correction & Coating - From $1,000",
            "Not sure - recommend",
        ],
        "service_interest": "Paint Correction",
        "form_subject": "New paint correction enquiry from radiantridesautocare.com.au",
        "cta_h2": "Ready to restore your paint?",
        "cta_body": "Tell us about your vehicle and current paint condition. We'll come back within 24 hours with a fixed Melbourne quote.",
    },
    {
        # C4 - Headlight Restoration (mobile-capable add-on)
        "slug": "headlight-restoration",
        "label": "Headlight Restoration",
        "service_type_schema": "Headlight Restoration",
        "title": "Headlight Restoration Melbourne | Mobile Service | Radiant Rides AutoCare",
        "description": "Mobile headlight restoration across Melbourne. Yellowed, foggy or oxidised lenses restored to clear at your address or in our Cranbourne North studio. Quoted per vehicle.",
        "og_description": "Mobile or in-studio. We restore yellowed, foggy headlights back to clear and seal them against re-oxidation.",
        "hero_image": "brand_assets/blue-car-tail-light.jpeg",
        "hero_subhead": "Yellowed, foggy headlights restored to clear. Mobile across Melbourne or in our Cranbourne North studio.",
        "intro_h2": "Mobile or in-studio headlight restoration",
        "intro_paragraphs": [
            "Headlight Restoration is the one service we do offer mobile. We come to your driveway or workplace anywhere across Melbourne and restore foggy, yellowed or oxidised plastic headlight lenses back to clear. Or, if you'd rather bring the car to us, we do the same job in our Cranbourne North studio.",
            "Plastic headlight lenses oxidise from UV exposure. The factory clear coating breaks down over five to ten years, the surface gets a yellow haze, light output drops noticeably, and the car looks older than it is. It's also a roadworthy issue on cars due for inspection. Restoration sands the oxidised layer off, polishes the lens back to clarity, and applies a UV-resistant sealant so it stays clear longer.",
            "Most cars are an hour or so per pair of headlights. We finish with a UV-resistant sealant that's the difference between a six-month fix and a result that holds for two-plus years. Done properly, it's the cheapest visible upgrade you can put on an older car.",
            "Starting from $50, with final pricing depending on the size of the lens, the level of oxidation, and whether you book mobile (call-out fee applies) or in-studio.",
        ],
        "at_a_glance_label": "Headlight restoration",
        "at_a_glance_rows": [
            ("Mode", "Mobile or in-studio"),
            ("Service area", "Melbourne (mobile)"),
            ("Time", "~1 hour per pair"),
            ("Finish", "UV-resistant sealant"),
            ("Longevity", "2+ years with sealant"),
            ("From", "$50 (mobile bookings add call-out fee)"),
        ],
        "what_it_does_intro": "Restoration is a four-step process that gets foggy plastic lenses back to clear and keeps them clear.",
        "what_it_does_cards": [
            ("Removes oxidised layer", "We wet-sand the yellowed, oxidised top layer off the plastic lens. This is the step most DIY kits skip or under-do."),
            ("Polishes back to clarity", "Progressive polishing compounds bring the lens back to optical clarity. Light output recovers. The car instantly looks newer."),
            ("Seals against UV", "A UV-resistant sealant locks in the result. Without this, the oxidation comes back within months. With it, you get years of clear."),
            ("Mobile-friendly", "Headlight restoration is the only service we do mobile. We bring everything to your driveway. Call-out fee applies."),
        ],
        "tiers_h2": "Single service, quoted per vehicle",
        "tiers_intro": "Headlight restoration starts from $50 per vehicle. Final pricing depends on lens size, oxidation level, and whether you book mobile (call-out fee) or in-studio.",
        "tiers": [
            {
                "name": "Headlight Restoration",
                "price": "$50",
                "primary": True,
                "features": [
                    "Wet-sand oxidised layer off the lens",
                    "Progressive polish back to optical clarity",
                    "UV-resistant sealant applied",
                    "Mobile (call-out fee) or in-studio",
                    "Both lenses included as standard pricing",
                    "~1 hour total per pair",
                ],
            },
        ],
        "suitable_for_h2": "When to book a restoration",
        "suitable_for_intro": "Headlight restoration earns its keep on specific patterns.",
        "suitable_for_cards": [
            ("Visibly yellowed lenses", "If the plastic looks hazy, milky or yellow in daylight, the oxidation is well underway. Restoration is the fix."),
            ("Reduced night-vision output", "Oxidised lenses scatter light. If your high-beam pattern looks weaker than it should, the lens is the most likely cause."),
            ("Cars 5+ years old", "Factory clear coatings start breaking down around year five to seven. Most cars in that age range benefit visibly."),
            ("Pre-sale prep", "A car for sale with foggy headlights reads as neglected. A restored pair makes the whole front of the car look fresher in photos."),
            ("Pre-roadworthy inspection", "Restoring lenses ahead of a roadworthy check avoids a fail mark on light output."),
            ("Mobile booking by appointment", "Can't drop the car off? We come to you anywhere in Melbourne with the call-out fee added."),
        ],
        "suburb_cross_links": [],
        "service_area_chips": [
            "Cranbourne North", "Cranbourne", "Berwick", "Narre Warren", "Pakenham", "Frankston",
            "Dandenong", "Hampton Park", "Clyde North", "Hallam", "Endeavour Hills", "Beaconsfield",
        ],
        "faq": [
            ("Do you do mobile headlight restoration?", "Yes. Headlight restoration is the only service we offer mobile. We come to you anywhere in Melbourne. A call-out fee applies. Bookings by appointment."),
            ("How long does a restoration take?", "Around an hour per pair of headlights once we're on site. Allow some setup and curing time around that."),
            ("How long does the result last?", "With our UV-resistant sealant, two-plus years is normal. Without a sealant (typical of cheap kits), the haze can return in months."),
            ("Can you fix lenses that are deeply cracked?", "No. Restoration fixes oxidation and surface haze. Deep cracks, impact damage or scoring through the plastic require lens replacement, which is a different repair."),
            ("How much does it cost?", "Starts from $50 per vehicle. Final pricing depends on lens size, level of oxidation, and whether you book mobile or in-studio. Mobile bookings include a call-out fee on top of the base price."),
            ("Is it worth it on an older car?", "Yes. Headlight restoration is one of the highest-visible-impact services we do per dollar spent. An older car can look five years younger from the front the same day."),
            ("Will it pass a roadworthy after restoration?", "If the lens itself isn't damaged, restoration plus sealant typically restores the lens back to roadworthy light output. If the failure is from damage rather than haze, replacement is the fix."),
            ("Can I book this with another detail at the studio?", "Yes. Headlight restoration is a popular add-on to any in-studio detail booking. Mention it on the enquiry and we'll include it in the time-block."),
        ],
        "schema_offers": [
            ("Headlight Restoration", "Mobile or in-studio. Wet-sand, polish and UV-sealant on yellowed plastic headlight lenses. Pricing quoted per vehicle."),
        ],
        "tier_select_options": [
            "Headlight Restoration - In-studio (From $50)",
            "Headlight Restoration - Mobile (From $50 + call-out fee)",
            "Not sure - recommend",
        ],
        "service_interest": "Headlight Restoration",
        "form_subject": "New headlight restoration enquiry from radiantridesautocare.com.au",
        "cta_h2": "Ready to clear those lenses?",
        "cta_body": "Tell us the car make and model and where you'd like us to do the job. We'll come back within 24 hours with a quote.",
    },
    {
        # C5 - Engine Bay Clean (add-on)
        "slug": "engine-bay-clean",
        "label": "Engine Bay Clean",
        "service_type_schema": "Engine Bay Detailing",
        "title": "Engine Bay Cleaning Melbourne | Radiant Rides AutoCare",
        "description": "Professional engine bay cleaning at our Cranbourne North studio. Safe degrease, dressed plastics, and a showroom-clean bay. Quoted per vehicle.",
        "og_description": "Safe engine bay degrease and dress at our Cranbourne North studio. Bookable add-on to any detail.",
        "hero_image": "brand_assets/foam-wash-4wd.jpeg",
        "hero_subhead": "Safe degrease and full dress of your engine bay. Bookable as an add-on at our Cranbourne North studio.",
        "intro_h2": "Engine bay cleaning, done safely",
        "intro_paragraphs": [
            "Engine bays collect grime fast. Oil residue, road dust, leaf litter, and the slow build-up that turns black plastic grey and metal surfaces dull. Most owners never touch the bay because the wrong approach can damage electronics, fuses or sensors. Done properly, it's one of the highest-impact details you can do to a car.",
            "We use a controlled approach: covers on the electrical components, the right degreaser for plastic and metal surfaces, low-pressure rinse rather than blast wash, and a finishing dress on the plastics so the bay holds the clean look. The whole bay comes back closer to showroom than you'd expect.",
            "Engine Bay Clean works best as an add-on to a Paint Enhancement or full detail booking. We're already set up, the time is incremental, and the car comes back finished top-to-bottom. We also do it as a standalone for cars about to be sold or going to a car show.",
            "Starts from $30 as an add-on to a detail booking, with final pricing depending on the size of the bay, the level of buildup, and whether it's standalone or paired.",
        ],
        "at_a_glance_label": "Engine bay clean",
        "at_a_glance_rows": [
            ("Studio", "Cranbourne North, VIC"),
            ("Mode", "In-studio only"),
            ("Add-on to", "Any detail or standalone"),
            ("Best paired with", "Pre Sale Detail or Paint Enhancement"),
            ("From", "$30 (add-on to a detail booking)"),
            ("Time", "Add ~1 hour to a detail booking"),
        ],
        "what_it_does_intro": "Engine bay cleaning isn't just degrease and rinse. Four specific steps make the difference between a clean bay and a damaged one.",
        "what_it_does_cards": [
            ("Electrical protection first", "We cover sensitive components - fuse box, alternator, intake, ECU - before any water touches the bay. This is the step that separates a safe clean from an expensive mistake."),
            ("Controlled degrease", "The right degreaser for plastic vs metal. Applied with brushes, not pressure-sprayed at electrical seals. Lifted with a low-pressure rinse."),
            ("Plastic and rubber dress", "Once the bay is clean and dry, we dress the plastics and rubber so the finish holds. Black plastic looks like black plastic again, not faded grey."),
            ("Final wipe-down", "Metal surfaces, battery casing, intake tube, hose runs - all wiped clean. The bay looks the way it did the day it left the factory."),
        ],
        "tiers_h2": "Single service, quoted per vehicle",
        "tiers_intro": "Engine bay clean starts from $30 as an add-on to a detail booking. Standalone or larger bays are quoted on enquiry.",
        "tiers": [
            {
                "name": "Engine Bay Clean",
                "price": "$30",
                "primary": True,
                "features": [
                    "Electrical components covered before clean",
                    "Controlled degrease on plastic and metal",
                    "Low-pressure rinse, no blast spray near electrics",
                    "Plastic and rubber dressed for hold",
                    "Final metal and surface wipe-down",
                    "Add-on to any detail, or standalone",
                ],
            },
        ],
        "suitable_for_h2": "When to book an engine bay clean",
        "suitable_for_intro": "Engine bay cleaning makes the most visible difference on these patterns.",
        "suitable_for_cards": [
            ("Pre-sale prep", "Buyers open the bonnet. A clean bay reads as 'looked after' and supports the asking price."),
            ("Car shows", "Show judges and Instagram both check under the bonnet. Engine bay clean is non-negotiable show prep."),
            ("Long-hold maintenance", "Once a year, paired with another detail. Catches the grime before it bakes on and corrodes plastics."),
            ("Recently serviced cars", "After major service work, the bay often has fingerprints, oil drips, and disturbed dirt. Cleanup makes the service work look complete."),
            ("Newly bought used cars", "Resetting a bay to clean lets you see leaks early, makes future maintenance easier, and starts ownership from a known baseline."),
            ("Bonded as a Paint Enhancement add-on", "Most common booking pattern. The car is already in-studio for a paint job, so the bay is incremental time and finishes the whole car."),
        ],
        "suburb_cross_links": [],
        "service_area_chips": [
            "Cranbourne North", "Cranbourne", "Berwick", "Narre Warren", "Pakenham", "Frankston",
            "Dandenong", "Hampton Park", "Clyde North", "Hallam", "Endeavour Hills", "Beaconsfield",
        ],
        "faq": [
            ("Is engine bay cleaning safe for electronics?", "Yes, when done properly. We cover sensitive components, use the right products, and never blast-pressure-wash near electrical seals. The vast majority of horror stories come from DIY pressure-washing without proper prep."),
            ("Can I do this on a modern hybrid or EV?", "Yes, with extra caution and the right protection on the high-voltage components. Mention the car type on enquiry and we'll confirm what we can and can't do safely."),
            ("How often should I have the bay cleaned?", "Once a year is plenty for most cars. Show cars or pre-sale prep can be done as one-offs. Daily drivers don't need it more often than the annual detail."),
            ("Is it just degrease and rinse?", "No. The clean is one step. Drying, dressing the plastics, and wiping down the metal surfaces is what makes the result look finished. Skipping those leaves the bay looking damp and patchy."),
            ("Will the result last?", "Months on a daily driver, longer on a car that's garaged. Dressing the plastics is the step that extends the look. Without it, the plastics start fading back within weeks."),
            ("Can you do it as a standalone or only as an add-on?", "Both. The most common booking is as an add-on to a Paint Enhancement, but we'll do it as a standalone for pre-sale prep or show prep."),
            ("Are you mobile?", "No. Engine bay cleaning is in-studio only. The controlled environment matters for electrical safety and water management."),
            ("How much does it cost?", "Starts from $30 as an add-on to a detail booking. Final pricing depends on bay size, level of buildup, and whether it's standalone or paired with a detail. Quoted per vehicle on enquiry."),
        ],
        "schema_offers": [
            ("Engine Bay Clean", "Professional in-studio engine bay degrease, protection of electrical components, and plastic/rubber dress. Quoted per vehicle."),
        ],
        "tier_select_options": [
            "Engine Bay Clean - Standalone",
            "Engine Bay Clean - Add-on to detail booking",
            "Not sure - recommend",
        ],
        "service_interest": "Engine Bay Clean",
        "form_subject": "New engine bay clean enquiry from radiantridesautocare.com.au",
        "cta_h2": "Ready to clean up under the bonnet?",
        "cta_body": "Tell us about your car and whether you'd like the bay cleaned as an add-on or a standalone booking. We'll come back within 24 hours with a quote.",
    },
    {
        # C6 - Leather Reconditioning (add-on)
        "slug": "leather-reconditioning",
        "label": "Leather Reconditioning",
        "service_type_schema": "Leather Reconditioning",
        "title": "Leather Reconditioning Melbourne | Radiant Rides AutoCare",
        "description": "Professional leather seat reconditioning at our Cranbourne North studio. Deep clean, condition, and protect tired or dry leather interiors. Quoted per vehicle.",
        "og_description": "Deep clean and condition tired leather seats and trim. In-studio at Cranbourne North.",
        "hero_image": "brand_assets/bmw-m-interior-front.jpeg",
        "hero_subhead": "Deep clean, conditioning and protection for tired or dry leather interiors. In-studio at Cranbourne North.",
        "intro_h2": "Leather brought back, not just wiped down",
        "intro_paragraphs": [
            "Leather seats are a high-touch surface that age fast if they're not looked after. Years of sweat, oils, sunscreen, denim transfer, and Melbourne sun dries the leather, cracks the finish, and embeds dirt deep in the pores. A wipe-down doesn't fix that. Reconditioning does.",
            "Our leather reconditioning is a multi-step process. We deep-clean to lift dirt out of the pores, treat the dyed finish where it's worn or faded, condition the leather to restore suppleness, and seal it with a UV-resistant protectant. The seats come back closer to new than most owners think possible.",
            "Best fit is luxury and prestige interiors where the leather is the differentiator, daily-driven cars with years of accumulated wear, or pre-sale prep where tired seats are knocking value off the asking price.",
            "Starts from $75, with final pricing depending on the number of seats, the size of the interior, the leather condition, and whether you book it as a standalone or add-on.",
        ],
        "at_a_glance_label": "Leather reconditioning",
        "at_a_glance_rows": [
            ("Studio", "Cranbourne North, VIC"),
            ("Mode", "In-studio only"),
            ("Scope", "Single seat, full front, or full interior"),
            ("Add-on to", "Interior Reset or standalone"),
            ("From", "$75"),
            ("Time", "Half to full day depending on scope"),
        ],
        "what_it_does_intro": "Reconditioning is four stages. Each one matters, and the order matters too.",
        "what_it_does_cards": [
            ("Deep pore clean", "We lift years of embedded dirt, oil and dye transfer out of the leather pores using leather-safe cleaners and controlled agitation. Cleaning before conditioning is non-negotiable."),
            ("Finish treatment", "Where the dye coating has worn or scuffed, we touch up the finish. The seats look uniform again, not patchy."),
            ("Conditioning", "Leather is skin. It needs moisture. We work in a leather-specific conditioner that restores suppleness, prevents cracking, and brings back the natural sheen."),
            ("UV protectant", "A finishing sealant slows future drying and fading from Melbourne sun. Reconditioning lasts longer with the seal than without."),
        ],
        "tiers_h2": "Single service, quoted per vehicle",
        "tiers_intro": "Leather reconditioning starts from $75. Final pricing depends on scope (single seat, front seats, or full interior) and the current condition.",
        "tiers": [
            {
                "name": "Leather Reconditioning",
                "price": "$75",
                "primary": True,
                "features": [
                    "Deep pore clean to lift embedded dirt and oils",
                    "Finish touch-up on worn or scuffed dye",
                    "Leather-specific conditioner restores suppleness",
                    "UV-resistant sealant slows future drying",
                    "Single seat, front pair, or full interior",
                    "Add-on to Interior Reset or standalone",
                ],
            },
        ],
        "suitable_for_h2": "When leather reconditioning pays off",
        "suitable_for_intro": "Reconditioning is the highest-impact interior service per dollar on cars with these patterns.",
        "suitable_for_cards": [
            ("Prestige and luxury interiors", "European leather is the reason you bought the car. Reconditioning preserves that feel for years longer than just vacuuming."),
            ("Daily drivers 4+ years old", "Wear shows fastest on the driver's bolster and the centre seat cushion. Annual reconditioning keeps the rest of the seat from catching up."),
            ("Pre-sale prep", "Tired leather is one of the first things a buyer notices. Reconditioning fixes the visible damage and supports the asking price."),
            ("Light-coloured leather", "Cream, tan, beige interiors show dirt and dye transfer worst. Reconditioning resets the colour back to factory."),
            ("Cars driven in workwear", "Denim transfers blue dye onto light leather. Trades workwear leaves marks. Reconditioning cleans the transfer out properly."),
            ("Long-hold ownership", "Annual reconditioning at the same time as your interior detail keeps the interior ageing at half the rate it otherwise would."),
        ],
        "suburb_cross_links": [],
        "service_area_chips": [
            "Cranbourne North", "Cranbourne", "Berwick", "Narre Warren", "Pakenham", "Frankston",
            "Dandenong", "Hampton Park", "Clyde North", "Hallam", "Endeavour Hills", "Beaconsfield",
        ],
        "faq": [
            ("Will this fix deep cracks in old leather?", "Reconditioning won't make deep structural cracks disappear. It will dramatically slow further cracking and restore colour and suppleness around the existing damage. Severely damaged leather needs full repair, which is a different specialty."),
            ("Can you do just the driver's seat?", "Yes. Driver-only reconditioning is a common booking because the driver's seat ages two to three times faster than the rest of the interior."),
            ("How long does it last?", "Twelve months between full reconditionings is typical for daily-driven cars. Garaged cars and lightly driven cars can stretch further. Our UV sealant is the main reason the result holds."),
            ("Does it work on perforated leather?", "Yes, with extra care during the clean step so cleaner doesn't pool in the perforations. We've done plenty of perforated sports seats."),
            ("What about leather trim on doors and dash?", "Same process. Door cards and dash leather often need it more than the seats themselves because they get direct sun all day."),
            ("Are you mobile?", "No. Leather reconditioning is in-studio only. The controlled environment matters for cleaner application, conditioner cure time, and avoiding cross-contamination with other surfaces."),
            ("Can I book this as an add-on to a regular detail?", "Yes. Reconditioning pairs naturally with our Interior Reset &amp; Protection package - the seats are already out of the way and we're already set up. Mention it on the enquiry."),
            ("How much does it cost?", "Starts from $75. Final pricing depends on scope (single seat, front pair, full interior) and the current leather condition. Quoted per vehicle on enquiry."),
        ],
        "schema_offers": [
            ("Leather Reconditioning", "Deep clean, finish touch-up, conditioning and UV-resistant sealant on leather seats and trim. In-studio. Quoted per vehicle."),
        ],
        "tier_select_options": [
            "Leather Reconditioning - Single seat",
            "Leather Reconditioning - Front seats",
            "Leather Reconditioning - Full interior",
            "Not sure - recommend",
        ],
        "service_interest": "Leather Reconditioning",
        "form_subject": "New leather reconditioning enquiry from radiantridesautocare.com.au",
        "cta_h2": "Ready to bring the leather back?",
        "cta_body": "Tell us about your car, the leather colour, and the scope you're after. We'll come back within 24 hours with a quote.",
    },
    {
        # C7 - Advanced Odor Elimination (add-on, differentiator)
        "slug": "advanced-odor-elimination",
        "label": "Advanced Odor Elimination",
        "service_type_schema": "Odor Elimination Treatment",
        "title": "Advanced Odor Elimination Melbourne | Radiant Rides AutoCare",
        "description": "Professional odor elimination for cars in Melbourne. Smoke, pet, food and chemical odors removed at source - not masked. In-studio at Cranbourne North.",
        "og_description": "Source-removal odor treatment for smoke, pet, food and chemical smells. In-studio at Cranbourne North.",
        "hero_image": "brand_assets/bmw-x5-interior-passenger.jpeg",
        "hero_subhead": "Smoke, pet, food and chemical odors removed at source. Not masked. In-studio at Cranbourne North.",
        "intro_h2": "Odor elimination that actually works",
        "intro_paragraphs": [
            "Most odor 'treatments' are just stronger scents layered over the underlying smell. The fragrance fades in days and the original odor comes back. Real odor elimination has to remove the source - the molecules embedded in carpet, upholstery, headlining, vents and door cards - not cover them.",
            "Our Advanced Odor Elimination Treatment is one of the differentiators we offer that few Melbourne detailers list explicitly. Source removal where possible, deep extraction from soft surfaces, treatment of the air-conditioning system that's been recirculating the smell, and a neutralising agent that breaks down the remaining molecules rather than masking them.",
            "Most cars need a single treatment. Heavy cases - long-term smokers, accidents involving food, pet incidents - sometimes need a second pass and we'll be straight about that on enquiry rather than overpromise.",
            "Starts from $120 per treatment. Final pricing depends on severity, source, and whether multiple treatments are likely. We're always straight up front about borderline cases.",
        ],
        "at_a_glance_label": "Advanced odor elimination",
        "at_a_glance_rows": [
            ("Studio", "Cranbourne North, VIC"),
            ("Approach", "Source removal, not masking"),
            ("Common sources", "Smoke, pet, food, chemical"),
            ("Treatments", "Typically 1, sometimes 2 for heavy cases"),
            ("From", "$120"),
            ("Time", "Half to full day"),
        ],
        "what_it_does_intro": "Real odor elimination is a four-step process. Skipping any one of them is why most 'odor treatments' fail.",
        "what_it_does_cards": [
            ("Source removal", "First, we find and remove the source where possible. Spilled food, embedded debris, pet hair packed into vents. You can't deodorise around something that's still there."),
            ("Deep extraction", "Hot-water extraction on carpets and upholstery pulls molecules out of soft surfaces where odor lives. This is the step that pet and smoke cases hinge on."),
            ("HVAC treatment", "The air-conditioning system recirculates and concentrates smells. We treat the evaporator and vents directly, not just the cabin air."),
            ("Neutralising treatment", "A finishing treatment that breaks down remaining odor molecules at a chemical level rather than masking them with fragrance. The car comes back smelling like nothing, not like a stronger scent."),
        ],
        "tiers_h2": "Single service, quoted per vehicle",
        "tiers_intro": "Treatment starts from $120 per vehicle. Heavy cases (long-term smoke, severe pet) may need a second pass which we'll flag up front.",
        "tiers": [
            {
                "name": "Advanced Odor Elimination",
                "price": "$120",
                "primary": True,
                "features": [
                    "Source removal - debris, residue, embedded material",
                    "Hot-water extraction on carpet and upholstery",
                    "HVAC treatment for vents and evaporator",
                    "Neutralising treatment, not fragrance masking",
                    "Single treatment for most cases",
                    "Heavy cases (smoke, pet) may need second pass",
                ],
            },
        ],
        "suitable_for_h2": "When odor elimination is the right service",
        "suitable_for_intro": "Specific patterns where source-removal odor treatment works best.",
        "suitable_for_cards": [
            ("Recently bought used cars", "You inherited the previous owner's smoke, pets, or habits. A one-off treatment resets the interior to neutral so you can actually enjoy the car."),
            ("Smoker's cars going to market", "Buyers walk away from cars that smell like smoke before they even drive them. Treatment is a high-ROI pre-sale step on smoker cars."),
            ("Pet owner refresh", "Long-term dog or cat transport leaves pet hair deep in carpet pile and pet odor in the upholstery. Treatment resets it."),
            ("Food spill recovery", "Spilled coffee, milk, takeaway. Spilled-and-set food odors don't air out. They need extraction and treatment."),
            ("Mould or moisture damage", "Water ingress (leaks, flooding, soaked carpet) leaves a musty smell that doesn't dry out. Treatment after drying clears the residual odor."),
            ("Hire and fleet cars", "Pre-handover treatment between drivers protects review scores and resale on fleet vehicles."),
        ],
        "suburb_cross_links": [],
        "service_area_chips": [
            "Cranbourne North", "Cranbourne", "Berwick", "Narre Warren", "Pakenham", "Frankston",
            "Dandenong", "Hampton Park", "Clyde North", "Hallam", "Endeavour Hills", "Beaconsfield",
        ],
        "faq": [
            ("Does this actually work on heavy smoke?", "Yes, on most cases. Smoke is one of the harder odors to eliminate because it permeates everything including the headlining. We've cleared long-term smoker cars with a single treatment in most cases. We'll tell you up front if your case is borderline."),
            ("Will my car smell like fragrance afterward?", "No. The goal is neutral, not 'stronger smell on top of the old smell'. The car will smell clean, like a clean car, not like air freshener."),
            ("How long does the result last?", "Permanently, if the source is gone and not reintroduced. If you continue smoking in the car, the smoke comes back. If you do another long pet road trip without cleaning the carpet, the pet smell returns. The treatment doesn't immunise the car against future odors."),
            ("Will it work on a flooded car?", "Depends on the severity and how long ago. Flood-damaged cars often have mould growth that needs to be addressed before odor treatment is the right next step. We'll assess and advise on enquiry."),
            ("Is one treatment enough?", "For most cases, yes. Heavy cases (long-term smokers, severe pet incidents) sometimes need a second pass. We'll quote the most likely scenario and be straight if a second treatment looks needed."),
            ("Can you treat just the HVAC system?", "Yes, as a standalone. Vent and evaporator treatment is a useful service on cars where the smell is concentrated when the AC turns on."),
            ("Are you mobile?", "No. Odor elimination is in-studio only. The treatment process needs controlled drying and curing conditions."),
            ("How much does it cost?", "Starts from $120 per treatment. Final pricing depends on the source, severity, and whether one or two treatments are likely. For heavy cases we'll often quote a price range up front."),
        ],
        "schema_offers": [
            ("Advanced Odor Elimination Treatment", "Source-removal odor treatment with deep extraction, HVAC treatment and neutralising finish. In-studio. Quoted per vehicle."),
        ],
        "tier_select_options": [
            "Odor Elimination - Standard",
            "Odor Elimination - Heavy (smoke / pet / long-term)",
            "Not sure - recommend",
        ],
        "service_interest": "Advanced Odor Elimination",
        "form_subject": "New odor elimination enquiry from radiantridesautocare.com.au",
        "cta_h2": "Ready to remove the smell at source?",
        "cta_body": "Tell us the source of the odor and how long it's been there. We'll come back within 24 hours with a quote and an honest assessment of whether one treatment will do it.",
    },
    {
        # C8 - Pre-Sale Detail (verified $225 price from packages.html)
        "slug": "pre-sale-detail",
        "label": "Pre-Sale Detail",
        "service_type_schema": "Pre-Sale Car Detail",
        "title": "Pre-Sale Car Detail Melbourne | From $225 | Radiant Rides AutoCare",
        "description": "Pre-sale car detail in Melbourne. Photo-ready interior and exterior prep that adds visible value to your listing. From $225 at our Cranbourne North studio.",
        "og_description": "Photo-ready pre-sale prep for cars going to market. From $225 at our Cranbourne North studio.",
        "hero_image": "brand_assets/bmw-exterior-03.jpeg",
        "hero_subhead": "Photo-ready interior and exterior prep that adds visible value to your sale listing. From $225 at our Cranbourne North studio.",
        "intro_h2": "Detail that pays for itself on resale",
        "intro_paragraphs": [
            "Pre-sale detail is built for one specific job: getting a car ready to list. Photos, test drives, walk-throughs. Every surface a buyer's eye lands on is reset to clean. The price you can list at goes up by more than the cost of the detail in almost every case.",
            "Buyers in Melbourne are sophisticated. They've scrolled through hundreds of listings before they get to yours. The cars that get clicks are the cars whose photos look better than the ones around them. Clean wheels, dressed tyres, polished paint, vacuumed carpet, wiped trim - all of it shows in the photos and all of it raises the perceived value.",
            "Our Pre-Sale Detail starts from $225 and includes the touch points and visible surfaces that buyers actually look at. For higher-end cars, we'll recommend layering Paint Enhancement on top so the photos pop and the test drive lands. For prestige cars going to market above $50k, full Correction &amp; Coating is a calculation worth running.",
            "Studio bookings only. Cranbourne North, with most south-east Melbourne suburbs within 20 minutes. Most cars are turned around in a single day.",
        ],
        "at_a_glance_label": "Pre-sale detail",
        "at_a_glance_rows": [
            ("Studio", "Cranbourne North, VIC"),
            ("From price", "$225"),
            ("Turnaround", "Typically single day"),
            ("Best paired with", "Paint Enhancement (higher-end cars)"),
            ("Mode", "In-studio only"),
            ("ROI", "Typically positive - listing price uplift > detail cost"),
        ],
        "what_it_does_intro": "Pre-sale prep focuses on what buyers actually see. Four areas that decide whether your listing gets clicked or scrolled past.",
        "what_it_does_cards": [
            ("Photo-ready exterior", "Wash, decontamination, wheel and tyre prep, dressed trim. The car photographs sharp from any angle. This is what gets buyers to click your listing."),
            ("Interior reset", "Vacuum, surface wipe-down, glass clean, plastic dress. The buyer slides into the driver's seat and the first impression is 'this owner cared'."),
            ("Touch-point detail", "Door handles, steering wheel, gear shift, indicator stalks. The surfaces buyers actually touch on the test drive. Clean here closes the sale."),
            ("Quick wins on visible wear", "Where it makes sense, we suggest one or two targeted upgrades (headlight restoration, leather conditioning) that lift the perceived value of the car for a fraction of the price uplift they enable."),
        ],
        "tiers_h2": "Pre-sale detail from $225",
        "tiers_intro": "Single offering. Pricing depends on vehicle size and current condition. Available as a standalone or paired with Paint Enhancement / Correction &amp; Coating for higher-end cars.",
        "tiers": [
            {
                "name": "Pre-Sale Detail",
                "price": "$225",
                "primary": True,
                "features": [
                    "Exterior wash, decontamination, wheel and tyre prep",
                    "Interior vacuum, surface wipe, glass and plastic dress",
                    "Touch-point detail on all buyer-contact surfaces",
                    "Photo-ready finish from any angle",
                    "Optional add-ons: paint enhancement, leather, headlights",
                    "Single-day turnaround for most cars",
                ],
            },
        ],
        "suitable_for_h2": "When pre-sale detail pays for itself",
        "suitable_for_intro": "ROI patterns where the listing-price uplift comfortably covers the detail cost.",
        "suitable_for_cards": [
            ("Used cars $15k+", "The price-uplift mechanic kicks in clearly above $15k. Buyers at this end are doing comparison shopping and respond to presentation."),
            ("Prestige cars going to market", "European cars, performance cars, or low-km examples. Pre-sale paired with Paint Enhancement or full Correction &amp; Coating compounds the value lift."),
            ("Trade-in negotiations", "Trade-in valuations are visual. A clean, finished car gets a better offer from the same dealer the same day."),
            ("Listings stuck on the market", "Relisted cars with thin click rates often have weak photos. A pre-sale detail and fresh photo set is a low-cost re-attempt."),
            ("Cars with visible neglect", "Tired paint, foggy headlights, scuffed trim. Pre-sale resets all of this so the photos don't telegraph 'haven't kept up with it'."),
            ("Pre-handover for sold cars", "Some sellers add pre-sale prep as a closing courtesy. Costs little, leaves a great impression, and supports word-of-mouth."),
        ],
        "suburb_cross_links": [],
        "service_area_chips": [
            "Cranbourne North", "Cranbourne", "Berwick", "Narre Warren", "Pakenham", "Frankston",
            "Dandenong", "Hampton Park", "Clyde North", "Hallam", "Endeavour Hills", "Beaconsfield",
        ],
        "faq": [
            ("How is pre-sale different from a regular detail?", "Pre-sale prioritises the visible surfaces buyers see in photos and on a test drive. A regular detail might go deeper into areas that don't affect the listing. Pre-sale is built around the listing photos and the buyer's eye path."),
            ("Should I pair pre-sale with paint enhancement?", "For higher-end cars (around $25k+), yes. The paint upgrade shows in photos and on the test drive, and the uplift typically outpaces the cost. We talk it through on enquiry."),
            ("How long does it take?", "Most cars are a single day. Cars with Paint Enhancement added are still typically same-day or next-morning pickup."),
            ("Will this help me sell faster?", "In our experience, yes - and at a slightly higher price. A clean, finished car gets more clicks, more inspections, and a stronger negotiating position. The combined effect typically pays back several times the cost."),
            ("Can I book this same day if my listing goes up tomorrow?", "Often yes, depending on the schedule. Call us on 0449 801 505 and we'll tell you straight whether we can fit it in."),
            ("What about photos - do you do those?", "We don't shoot the listing photos but we hand the car back ready to be photographed. Most owners shoot the same day with their phone, ideally in even outdoor light."),
            ("Are you mobile?", "No. Pre-sale detail is in-studio only. The controlled environment is what makes the difference between a wash and a finished car."),
            ("Is the $225 price the final cost?", "$225 is the starting price for most cars. Larger vehicles, dirtier vehicles, or add-on services (paint enhancement, leather, headlights) move the final number. We quote on enquiry."),
        ],
        "schema_offers": [
            ("Pre-Sale Car Detail", "Photo-ready exterior and interior prep for cars going to market. From $225 at Cranbourne North studio."),
        ],
        "tier_select_options": [
            "Pre-Sale Detail - Standard (From $225)",
            "Pre-Sale Detail + Paint Enhancement",
            "Pre-Sale Detail + Correction & Coating",
            "Not sure - recommend",
        ],
        "service_interest": "Pre-Sale Detail",
        "form_subject": "New pre-sale detail enquiry from radiantridesautocare.com.au",
        "cta_h2": "Listing soon? Let's get it photo-ready.",
        "cta_body": "Tell us about the car and the timeline. We'll come back within 24 hours with a quote and an honest call on whether to add Paint Enhancement.",
    },
]


def build_at_a_glance_rows(rows):
    out = []
    for i, (label, value) in enumerate(rows):
        cls = "flex justify-between" + ("" if i == len(rows) - 1 else " border-b border-white/10 pb-3")
        out.append(f'          <li class="{cls}"><span class="text-neutral-400">{label}</span><span class="font-semibold">{value}</span></li>')
    return "\n".join(out)


def build_suitable_for_cards(cards):
    out = []
    for title, body in cards:
        out.append(f"""      <div class="service-card">
        <h3 class="text-xl mb-2">{title}</h3>
        <p class="text-neutral-400 text-sm leading-relaxed">{body}</p>
      </div>""")
    return "\n".join(out)


def build_maintenance_block(block):
    tick = '<svg class="feature-tick mt-1 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>'
    items_html = "\n          ".join(
        f'<li class="flex gap-3 items-start">{tick}{item}</li>' for item in block["items"]
    )
    return f"""      <div>
        <h3 class="text-2xl mb-4 uppercase">{block['h3']}</h3>
        <ul class="space-y-3 text-neutral-300 text-base leading-relaxed">
          {items_html}
        </ul>
      </div>"""


def build_suburb_cross_link_cards(links):
    """Phase C cross-link cards (3-col grid). Each link is (title, body, href)."""
    if not links:
        return ""
    cards = []
    for title, body, href in links:
        cards.append(f"""      <a href="{href}" class="service-card flex items-start gap-4">
        <div class="service-icon flex-shrink-0"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 2.5l8 3v6c0 5-3.5 8.7-8 10-4.5-1.3-8-5-8-10v-6l8-3z"/></svg></div>
        <div><h3 class="text-lg mb-1">{title}</h3><p class="text-neutral-400 text-sm">{body}</p></div>
      </a>""")
    cards.append("""      <a href="/contact" class="service-card flex items-start gap-4 border-dashed">
        <div class="service-icon flex-shrink-0"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
        <div><h3 class="text-lg mb-1">Different suburb?</h3><p class="text-neutral-400 text-sm">We service all of south-east Melbourne. Drop us a note for a quote from your area.</p></div>
      </a>""")
    return "\n".join(cards)


def build_service_hub_page(s):
    canonical = f"{SITE}/{s['slug']}"
    intro_paras_html = "\n        ".join(f"<p>{p}</p>" for p in s["intro_paragraphs"])
    at_a_glance = build_at_a_glance_rows(s["at_a_glance_rows"])
    what_cards = build_what_it_does_cards(s["what_it_does_cards"])
    tier_cards = build_tier_cards(s["tiers"])
    suitable_cards = build_suitable_for_cards(s["suitable_for_cards"])

    # Tier grid layout: 1 tier centered, 2-3 tiers full grid
    if len(s["tiers"]) == 1:
        tier_grid_class = "grid md:grid-cols-1 max-w-2xl mx-auto gap-5"
    elif len(s["tiers"]) == 2:
        tier_grid_class = "grid md:grid-cols-2 gap-5"
    else:
        tier_grid_class = "grid md:grid-cols-3 gap-5"

    # Maintenance section is optional (some services don't have post-service maintenance)
    if s.get("maintenance_blocks"):
        maintenance_html = "\n".join(build_maintenance_block(b) for b in s["maintenance_blocks"])
        maintenance_section = f"""

<!-- Maintenance -->
<section class="py-20 md:py-28 bg-[#0a0a0a]">
  <div class="container-x">
    <div class="max-w-3xl mb-14">
      <div class="tagline mb-4">After the service</div>
      <h2 class="text-3xl md:text-5xl mb-5 uppercase leading-tight">{s['maintenance_h2']}</h2>
      <p class="text-neutral-400 text-lg leading-relaxed">{s['maintenance_subhead']}</p>
    </div>
    <div class="grid md:grid-cols-2 gap-12 lg:gap-16">
{maintenance_html}
    </div>
  </div>
</section>"""
    else:
        maintenance_section = ""

    # Suburb cross-links (only services with sibling suburb LPs)
    suburb_cards = build_suburb_cross_link_cards(s.get("suburb_cross_links", []))
    if suburb_cards:
        suburb_section = f"""

<!-- Suburb cross-links -->
<section class="py-20 md:py-24">
  <div class="container-x">
    <div class="max-w-2xl mb-10">
      <div class="tagline mb-4">Suburb pages</div>
      <h2 class="text-3xl md:text-5xl mb-4 uppercase leading-tight">{s['label']} in your suburb</h2>
      <p class="text-neutral-400 text-lg leading-relaxed">Suburb-specific pages with drive times, surrounding areas, and FAQ tailored to your local catchment.</p>
    </div>
    <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
{suburb_cards}
    </div>
  </div>
</section>"""
    elif s.get("service_area_chips"):
        # Fallback: show service-area chips for services without suburb LPs
        chips_html = "\n".join(
            f'      <div class="border border-white/10 px-4 py-3 text-center"><p class="text-neutral-300 text-sm font-semibold">{c}</p></div>'
            for c in s["service_area_chips"]
        )
        suburb_section = f"""

<!-- Service area -->
<section class="py-20 md:py-24">
  <div class="container-x">
    <div class="max-w-2xl mb-10">
      <div class="tagline mb-4">Service area</div>
      <h2 class="text-3xl md:text-5xl mb-4 uppercase leading-tight">Where we service</h2>
      <p class="text-neutral-400 text-lg leading-relaxed">{s['label']} for drivers across south-east Melbourne, booked at our Cranbourne North studio.</p>
    </div>
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
{chips_html}
    </div>
  </div>
</section>"""
    else:
        suburb_section = ""

    # FAQ + schema
    faq_html = build_faq_html(s["faq"])
    faq_schema = build_faq_schema(s["faq"])
    schema_offers = build_schema_offers(s["schema_offers"])
    select_options = build_select_options(s["tier_select_options"])

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{s['title']}</title>
<meta name="description" content="{s['description']}" />
<meta name="google-site-verification" content="GEjj3uAIpsoPo9sPHQSo7hQLPrSucyHd-c6V0Ak8Ufg" />

<meta property="og:title" content="{s['title']}" />
<meta property="og:description" content="{s['og_description']}" />
<meta property="og:image" content="{SITE}/{s['hero_image']}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:type" content="website" />
<meta name="twitter:card" content="summary_large_image" />

<link rel="icon" type="image/png" sizes="32x32" href="brand_assets/699659fa91a4b7a50b6a86e0_favicon-32x32.png" />
<link rel="apple-touch-icon" href="brand_assets/699aee6a8a929099d7bd579d_RRAC_WEBCLIP.png" />

<link rel="canonical" href="{canonical}" />

{HEAD_COMMON}

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "AutoBodyShop",
      "@id": "{SITE}/#business",
      "name": "Radiant Rides AutoCare",
      "image": "{SITE}/brand_assets/6993c810021c99eafe30839f_Radiant_Rides_logo_art.png",
      "url": "{SITE}/",
      "telephone": "+61449801505",
      "email": "hello@radiantridesautocare.com.au",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "Crestway Dr",
        "addressLocality": "Cranbourne North",
        "addressRegion": "VIC",
        "addressCountry": "AU"
      }},
      "areaServed": "Melbourne, Victoria",
      "priceRange": "$$"
    }},
    {{
      "@type": "Service",
      "serviceType": "{s['service_type_schema']}",
      "name": "{s['label']} Melbourne",
      "description": "{s['og_description']}",
      "provider": {{ "@id": "{SITE}/#business" }},
      "areaServed": {{ "@type": "City", "name": "Melbourne" }},
      "hasOfferCatalog": {{
        "@type": "OfferCatalog",
        "name": "{s['label']} options",
        "itemListElement": [
{schema_offers}
        ]
      }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Packages", "item": "{SITE}/packages" }},
        {{ "@type": "ListItem", "position": 3, "name": "{s['label']}", "item": "{canonical}" }}
      ]
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
{faq_schema}
      ]
    }}
  ]
}}
</script>

<link rel="stylesheet" href="assets/site.css" />
</head>

<body>

{HEADER}

<nav aria-label="Breadcrumb" class="border-b border-white/10 bg-black">
  <div class="container-x py-3">
    <ol class="flex items-center gap-2 text-xs text-neutral-400">
      <li><a href="/" class="hover:text-white">Home</a></li>
      <li aria-hidden="true" class="text-neutral-600">/</li>
      <li><a href="/packages" class="hover:text-white">Packages</a></li>
      <li aria-hidden="true" class="text-neutral-600">/</li>
      <li class="text-white" aria-current="page">{s['label']}</li>
    </ol>
  </div>
</nav>

<!-- Hero -->
<section class="relative hero-bg overflow-hidden">
  <img src="{s['hero_image']}" alt="" class="absolute inset-0 w-full h-full object-cover" />
  <div class="relative z-10 container-x py-20 md:py-28">
    <div class="max-w-3xl">
      <div class="tagline mb-5">Melbourne {s['label'].lower()}</div>
      <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl leading-[1.05] mb-6">
        {s['label']}<br class="hidden sm:block" />
        <span>in Melbourne</span>
      </h1>
      <p class="text-lg md:text-xl text-neutral-300 max-w-2xl mb-9 leading-relaxed">
        {s['hero_subhead']}
      </p>
      <div class="flex flex-wrap gap-3">
        <a href="#enquire" class="btn btn-primary">Get a quote</a>
        <a href="tel:0449801505" class="btn btn-secondary">Call 0449 801 505</a>
      </div>
    </div>
  </div>
</section>

<!-- Intro -->
<section class="py-20 md:py-28">
  <div class="container-x grid lg:grid-cols-5 gap-12 lg:gap-16">
    <div class="lg:col-span-3">
      <div class="tagline mb-4">What it is</div>
      <h2 class="text-3xl md:text-5xl mb-7 uppercase leading-tight">{s['intro_h2']}</h2>
      <div class="space-y-5 text-neutral-300 text-lg leading-relaxed">
        {intro_paras_html}
      </div>
    </div>
    <aside class="lg:col-span-2">
      <div class="sub-card p-7 md:p-9">
        <div class="tagline mb-4">At a glance</div>
        <h3 class="text-2xl mb-5">{s['at_a_glance_label']}</h3>
        <ul class="space-y-3 text-neutral-200 text-base">
{at_a_glance}
        </ul>
        <a href="#enquire" class="btn btn-primary w-full mt-6">Enquire now</a>
      </div>
    </aside>
  </div>
</section>

<div class="section-divider"></div>

<!-- What it does -->
<section class="py-20 md:py-28">
  <div class="container-x">
    <div class="max-w-2xl mb-14">
      <div class="tagline mb-4">The detail</div>
      <h2 class="text-3xl md:text-5xl mb-5 uppercase leading-tight">What {s['label'].lower()} actually does</h2>
      <p class="text-neutral-400 text-lg leading-relaxed">{s['what_it_does_intro']}</p>
    </div>
    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
{what_cards}
    </div>
  </div>
</section>

<!-- Tiers -->
<section class="py-20 md:py-28 bg-[#0a0a0a]">
  <div class="container-x">
    <div class="max-w-2xl mx-auto text-center mb-14">
      <div class="tagline mb-4">{s['label']} options</div>
      <h2 class="text-3xl md:text-5xl mb-5 uppercase">{s['tiers_h2']}</h2>
      <p class="text-neutral-400 text-lg">{s['tiers_intro']}</p>
    </div>
    <div class="{tier_grid_class}">
{tier_cards}
    </div>
    <p class="text-center text-neutral-500 text-sm mt-8">Final pricing depends on vehicle size and current condition. We quote every job after seeing the car.</p>
  </div>
</section>

<!-- Suitable for -->
<section class="py-20 md:py-28">
  <div class="container-x">
    <div class="max-w-2xl mb-14">
      <div class="tagline mb-4">Who it suits</div>
      <h2 class="text-3xl md:text-5xl mb-5 uppercase leading-tight">{s['suitable_for_h2']}</h2>
      <p class="text-neutral-400 text-lg leading-relaxed">{s['suitable_for_intro']}</p>
    </div>
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
{suitable_cards}
    </div>
  </div>
</section>{maintenance_section}{suburb_section}

<!-- FAQ -->
<section class="py-20 md:py-28 bg-[#0a0a0a]">
  <div class="container-x max-w-3xl">
    <div class="text-center mb-14">
      <div class="tagline mb-4">FAQs</div>
      <h2 class="text-3xl md:text-5xl">{s['label']} - FAQs</h2>
    </div>
    <div class="faq">
{faq_html}
    </div>
  </div>
</section>

<!-- CTA banner -->
<section class="cta-banner py-16 md:py-24 px-6 md:px-10 text-center">
  <div class="max-w-4xl mx-auto">
    <h2 class="text-3xl md:text-5xl text-white mb-4">{s['cta_h2']}</h2>
    <p class="text-white/90 max-w-2xl mx-auto text-lg mb-7">{s['cta_body']}</p>
    <div class="flex flex-wrap gap-3 justify-center">
      <a href="#enquire" class="btn btn-dark">Get a quote</a>
      <a href="tel:0449801505" class="btn btn-secondary">Call 0449 801 505</a>
    </div>
  </div>
</section>

<!-- Contact form -->
<section id="enquire" class="py-20 md:py-28 bg-white text-neutral-900">
  <div class="container-x grid lg:grid-cols-5 gap-10 lg:gap-14 items-start">
    <div class="lg:col-span-2">
      <div class="inline-block px-3 py-1 border border-neutral-300 text-xs uppercase tracking-[0.18em] text-neutral-600 mb-5">{s['label']} enquiries</div>
      <h2 class="text-3xl md:text-5xl text-neutral-950 mb-4 leading-tight">Quote my {s['label'].lower()}</h2>
      <p class="text-neutral-700 text-lg mb-8">Drop your car details. We'll get back to you within 24 hours with a fixed quote.</p>
      <div class="space-y-3">
        <a href="tel:0449801505" class="group flex items-center gap-4 bg-neutral-100 hover:bg-neutral-200 transition p-5">
          <div class="w-10 h-10 bg-neutral-900 text-white flex items-center justify-center flex-shrink-0">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          </div>
          <div>
            <div class="text-xs uppercase tracking-[0.18em] text-neutral-500 mb-0.5">Phone</div>
            <div class="text-base font-semibold text-neutral-950">0449 801 505</div>
          </div>
        </a>
        <a href="mailto:hello@radiantridesautocare.com.au" class="group flex items-center gap-4 bg-neutral-100 hover:bg-neutral-200 transition p-5">
          <div class="w-10 h-10 bg-neutral-900 text-white flex items-center justify-center flex-shrink-0">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>
          </div>
          <div>
            <div class="text-xs uppercase tracking-[0.18em] text-neutral-500 mb-0.5">Email</div>
            <div class="text-base font-semibold text-neutral-950 break-all">hello@radiantridesautocare.com.au</div>
          </div>
        </a>
        <a href="https://maps.app.goo.gl/zjQsW3KK7zboiCJX7" target="_blank" rel="noopener" class="group flex items-center gap-4 bg-neutral-100 hover:bg-neutral-200 transition p-5">
          <div class="w-10 h-10 bg-neutral-900 text-white flex items-center justify-center flex-shrink-0">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          </div>
          <div>
            <div class="text-xs uppercase tracking-[0.18em] text-neutral-500 mb-0.5">Studio</div>
            <div class="text-base font-semibold text-neutral-950">Cranbourne North, VIC</div>
          </div>
        </a>
      </div>
    </div>

    <div class="lg:col-span-3 bg-neutral-50 border border-neutral-200 p-6 md:p-10">
      <h3 class="text-xl md:text-2xl text-neutral-950 font-bold mb-2">Send us a message</h3>
      <p class="text-neutral-600 mb-6">Tell us about your car and what you're after. We'll come back with a quote.</p>
      <form action="https://formspree.io/f/mojrwrgw" method="POST" class="space-y-4">
        <input type="hidden" name="_subject" value="{s['form_subject']}" />
        <input type="hidden" name="_next" value="https://www.radiantridesautocare.com.au/thank-you" />
        <input type="hidden" name="_source_page" value="{s['slug']}" />
        <input type="hidden" name="service_interest" value="{s['service_interest']}" />

        <div class="grid sm:grid-cols-2 gap-4">
          <label class="block">
            <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Name</span>
            <input type="text" name="name" required class="form-input" placeholder="Your name" />
          </label>
          <label class="block">
            <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Phone</span>
            <input type="tel" name="phone" class="form-input" placeholder="0400 000 000" />
          </label>
        </div>
        <label class="block">
          <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Email</span>
          <input type="email" name="email" required class="form-input" placeholder="you@example.com" />
        </label>
        <div class="grid sm:grid-cols-2 gap-4">
          <label class="block">
            <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Vehicle</span>
            <input type="text" name="vehicle" class="form-input" placeholder="e.g. 2018 Mazda CX-5" />
          </label>
          <label class="block">
            <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Suburb</span>
            <input type="text" name="suburb" class="form-input" placeholder="e.g. Berwick" />
          </label>
        </div>
        <label class="block">
          <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Option</span>
          <select name="package" class="form-input">
            <option value="">Select an option</option>
{select_options}
          </select>
        </label>
        <label class="block">
          <span class="block text-xs uppercase tracking-[0.16em] text-neutral-600 mb-1.5 font-semibold">Message</span>
          <textarea name="message" rows="5" class="form-input" placeholder="Tell us about your car and what you're after."></textarea>
        </label>
        <div class="pt-2">
          <button type="submit" class="btn btn-primary w-full sm:w-auto">Send enquiry</button>
          <p class="text-xs text-neutral-500 mt-3">We respond within 24 hours.</p>
        </div>
      </form>
    </div>
  </div>
</section>

{FOOTER}

</body>
</html>
"""


def main():
    for page in PAGES:
        out_path = ROOT / f"{page['slug']}.html"
        html = build_page(page)
        out_path.write_text(html, encoding="utf-8")
        line_count = html.count("\n") + 1
        print(f"Wrote {page['slug']}.html  ({line_count} lines, {len(html)} chars)")
    for s in SERVICE_HUBS:
        out_path = ROOT / f"{s['slug']}.html"
        html = build_service_hub_page(s)
        out_path.write_text(html, encoding="utf-8")
        line_count = html.count("\n") + 1
        print(f"Wrote {s['slug']}.html  ({line_count} lines, {len(html)} chars)")


if __name__ == "__main__":
    main()
