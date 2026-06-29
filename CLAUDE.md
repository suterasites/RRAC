# CLAUDE.md - Radiant Rides Auto Care

> Migration from Webflow to static HTML/CSS/JS. Kicked off 2026-05-04, target completion Tue 2026-05-20. Webflow per-site plan ($28/mo) cancels after cutover.

## Business Context

**Business Name:** Radiant Rides Auto Care
**Tagline:** Your car deserves a Radiant touch. We handle the details so you don't have to.
**Owner:** Dylan Tanner (Head Detailer) - stays anonymous on site (no name/title)
**Phone:** 0449 801 505
**Email:** hello@radiantridesautocare.com.au
**ABN:** 98 500 156 705
**Location:** Crestway Dr, Cranbourne North, VIC
**Live URL:** www.radiantridesautocare.com.au
**Domain registrar:** Registry Australia (Dylan owns domain)
**Instagram:** @radiantrides_autocare
**Facebook:** https://www.facebook.com/profile.php?id=61579215043451

### Services
- Interior Clean
- Exterior Clean
- Paint Protection
- Paint Correction
- Basic Interior & Exterior Package
- Full Interior Detail
- Exterior Enhancement
- Complete Exterior Enhancement
- Subscription Detailing
- Mobile Headlight Restoration

### Service Area
Cranbourne North + Melbourne (mobile-capable for headlight restoration; in-shop for full details)

### Tracking (preserve verbatim on every page)
- GA4: `G-C62DXBY0EC`
- Google Site Verification: `GEjj3uAIpsoPo9sPHQSo7hQLPrSucyHd-c6V0Ak8Ufg`
- No Google Ads conversion pixel currently (Dylan declined Ads on 2026-03-11; revisit if pricing reaches $800+)

### Third-party widgets in use on Webflow (decide per-page whether to keep)
- ReviewsJet (testimonial slider on most pages)
- Elfsight platform script

### Open client tasks (handled in third-party admin, not code)
- Elfsight Instagram feed: switch layout from 8 tiles to 6 tiles per row (Dylan feedback 2026-05-13). Edit at elfsight.com -> Instagram Feed widget -> Layout settings.

---

## Reference Source

Current Webflow site: https://www.radiantridesautocare.com.au/
Scraped HTML reference: `C:/Users/james/AppData/Local/Temp/radiant_rides_scrape/`
- `index.html`, `about.html`, `packages.html`, `our-work.html`, `contact-page.html`
- `webflow.shared.css` (full Webflow CSS dump - use for typography/spacing reference)
- `originals.txt` (list of all CDN-original asset URLs)

## Site Structure (mirrors Webflow sitemap)

| Slug | File | Purpose |
|------|------|---------|
| `/` | `index.html` | Homepage |
| `/about` | `about.html` | About |
| `/packages` | `packages.html` | Service packages and pricing |
| `/our-work` | `our-work.html` | Gallery |
| `/contact` | `contact.html` | Contact form (Formspree). Webflow slug was `/contact-page` - keep `/contact-page` redirect to `/contact` via `_redirects` for any external links. |
| `/thank-you` | `thank-you.html` | Form submission thank-you |

## Always Do First
- Invoke the `frontend-design` skill before writing any frontend code.

## Reference Matching
- Match layout, spacing, typography, and color from the live Webflow site (open in a browser tab while building) and the scraped HTML.
- Do not redesign or add sections that aren't on the Webflow site.
- Keep copy verbatim from the scraped Webflow HTML.

## Local Server
- Start: `node serve.mjs` (serves root at `http://localhost:3500`)
- Never screenshot a `file:///` URL.

## Screenshot Workflow
- `node screenshot.mjs http://localhost:3500 <label>` saves to `temporary screenshots/screenshot-N-<label>.png` (desktop 1440x900)
- `node screenshot-mobile.mjs http://localhost:3500 <label>` for mobile (390x844 @2x)
- Reference screenshots from Webflow are prefixed `ref-` (capture using puppeteer against the live URL).
- Compare reference vs build, fix diffs, re-screenshot. At least 2 rounds per page.

## Output Defaults
- Single HTML file per page, component styles inline in a `<style>` block, unless told otherwise.
- **Tailwind: precompiled static CSS, NOT the CDN.** Link `<link rel="stylesheet" href="assets/tailwind.css" />` (loaded before `assets/site.css` so site.css wins the cascade). The `cdn.tailwindcss.com` Play CDN was removed 2026-06-18 (render-blocking 124KB JS, the dominant perf issue). After adding/changing utility classes, rebuild with the standalone CLI (no Node needed):
  `/tmp/tailwindcss -c /tmp/rrac-tw.config.js -i /tmp/rrac-tw-input.css -o assets/tailwind.css --minify`
  (config `content` = `*.html`, safelist `hidden`/`open`/`active`/`menu-active`/`has-value`; input = the three `@tailwind` directives). Download the CLI from `github.com/tailwindlabs/tailwindcss/releases` (`tailwindcss-macos-arm64`, match v3.4.17). Verify class coverage before deploy.
- Google Fonts: Sora (700) for headings, Inter (400, 500) for body. Loaded off the critical path via `rel="preload" as="style"` + `onload` swap with a `<noscript>` fallback (not a plain render-blocking stylesheet).
- Mobile-first responsive.

## Brand Palette (from Webflow CSS)
- `--neutral-darkest`: `#000`
- `--cod-gray`: `#101010` (primary surface)
- `--cod-gray-darker`: `#060606`
- `--neutral-darker`: `#191919`
- `--white`: `#fff`
- `--neutral-lightest`: `#f2f2f2`
- `--lavender`: `#d93be3` (accent)
- `--lavender-dark`: `#ad2fb5`
- `--lavender-darkest`: `#411144`

Default scheme is dark (black background, white text, lavender accents) - "Radiant" feel.

## Brand Assets
- `brand_assets/` contains logos, hero images, gallery photos pulled from Webflow CDN (24 originals).
- Logo files: `6993c810021c99eafe30839f_Radiant_Rides_logo_art.png` (full logo), `6993b18f5356d704752d6ff4_RR_Type_Only.png` (wordmark), `699aee6a8a929099d7bd579d_RRAC_WEBCLIP.png` (apple touch icon), `699659fa91a4b7a50b6a86e0_favicon-32x32.png` (favicon).
- Real customer photos (Dylan's actual work): files starting with `6997b...` (5 photos).
- Relume placeholder images (files starting with `698d3d...` or `69965...`): use only where Dylan hasn't supplied real photos. Replace with real Dylan-supplied photos opportunistically in monthly updates.

## Deployment
- Git remote: `github.com/suterasites/radiant-rides-autocare` (to be created).
- Push to `main`, then Cloudflare Pages auto-deploys.
- Domain cutover (DNS via Registry Australia) happens after build review - James handles DNS.
- Webflow subscription cancels post-cutover.

## Multi-Page Consistency
- Navbar identical across all pages.
- Footer identical across all pages.
- Internal links use relative paths matching the sitemap structure.

## Form Handling
- Contact form on `contact.html` posts to Formspree endpoint `https://formspree.io/f/mojrwrgw`.
- On success, redirect to `/thank-you`.
- Notification email goes to hello@radiantridesautocare.com.au.

## Hard Rules
- Do not add sections, features, or content not in the Webflow reference.
- Do not "improve" the Webflow design - mirror it.
- Do not use em dashes anywhere. Use hyphens, commas, or periods.
- Keep GA4 tag (`G-C62DXBY0EC`) and Google Site Verification meta on every page.
- Ownership commitment: post 6-month lock-in (after 2026-08-18), Dylan can request the full source bundle. Static HTML/CSS/JS makes this easy - keep it portable, no proprietary build steps.
