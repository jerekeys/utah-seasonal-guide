# Utah Halloween & Fall Guide 2026 — Website v2

A multi-page, static public website generated from the Google Sheet **Utah Halloween & Fall 2026 — Complete Ideas Guide**.

## Pages
- `index.html` — Explore directory
- `weekend.html` — Weekend planner
- `itineraries.html` — Ready-made itineraries
- `vibes.html` — Pick by vibe
- `standouts.html` — Standout recommendations
- `event.html?id=...` — reusable full event detail view
- `submit.html` — user submission/correction form
- `about.html` — methodology and accessibility notes

## Accessibility
The site uses semantic structure, visible keyboard focus, skip navigation, 44px+ primary tap targets, higher-contrast colors, form labels, reduced-motion support, descriptive alt text on event-specific photos, and empty alt text on decorative category art. This is intended to follow WCAG/ADA best practices but is not a formal accessibility certification.

## Social links
Event cards and detail pages render local logo icons only for Instagram, Facebook, Bluesky, TikTok, and LinkedIn when those URLs exist in the source data. Twitter/X links are intentionally not rendered.

## Images
A small number of events use event-specific images tied to official/tourism sources. All other cards use bundled decorative SVG category art so stock imagery is not mistaken for the actual event. Image credits are displayed under event-specific photos.

## Submission form
The form uses Netlify Forms (`data-netlify=true`) and a honeypot field. It will work automatically when the folder is deployed to Netlify. On another static host, connect `submit.html` to that provider's form handling service.

## Publish
Deploy this folder as-is to Netlify, Cloudflare Pages, GitHub Pages, or another static host. No build step or database is required.


## v3 taxonomy simplification
Public Explore filters now use 10 visitor-friendly regions and 14 broad activity types.
The original detailed regions/categories are retained in `assets/data.js` as
`sourceRegion` and `sourceCategories`, so free-text search still benefits from the
research taxonomy without exposing it as a huge filter list.


## v4 social enrichment
A current research pass expanded social-link coverage from 81 to 108 event listings.
Platform-link counts changed from {'instagram': 73, 'facebook': 7, 'bluesky': 1} to {'instagram': 97, 'facebook': 61, 'linkedin': 20, 'tiktok': 6, 'bluesky': 1}.
Supported platforms: Instagram, Facebook, TikTok, Bluesky, LinkedIn.
X/Twitter is intentionally excluded.


## v5 image policy and enrichment
- 13 listings currently have real promotional imagery.
- All other listings use original category-specific SVG artwork rather than a generic haunted-house placeholder.
- Real-image metadata records source URL, visible credit, usage type, and an internal rights note.
- Strong preference order: organizer permission -> explicit press/media asset -> source-hosted official promotional image -> original category artwork.
- Sundance's prior third-party image was removed because the resort routes media/photography usage through its press approval process.
- The submission form now accepts promo images/media-kit links with an authorization statement.


## v6
- Rebranded shell to **Utah Seasonal Guide** with Halloween & Fall 2026 as the current seasonal guide.
- Added sponsor-ready card infrastructure. Sponsored listings are hidden until `sponsored: true` is set and are always labeled.
- Added sourced accessibility summaries to 19 listings; absence of a badge means no verified accessibility claim was found, not that the event is inaccessible.
- Enforced **zero image hotlinks**. Only locally bundled image paths render.
- Retained 1 locally bundled real photo(s); all other cards use category art until a licensed/permissioned file is imported.
- License-checked 7 high-confidence Creative Commons/public-domain candidates and recorded them in the image audit / image credits page. They are deliberately not displayed until their actual bytes are bundled locally.
- Accessibility summaries link to the organizer/venue source and use warning styling for explicit limitations.
