# Utah Every Season

A multi-page static field guide to Utah events, traditions and temporary experiences, backed by the Google Sheet **Utah Seasonal Event Discovery Backend — 2026–27**. The public identity is **Utah Every Season** — *Utah’s obsessive guide to what to do next.* The older Halloween/Fall workbook remains a research baseline, but the canonical detailed event source is the backend workbook’s **Event Database** tab.

## Development workflow
- `main` is production and should only receive reviewed release batches.
- `development` is the working branch used for the persistent Netlify branch preview.
- Routine design/content/code changes should be committed to `development` first.
- After review, merge a batch to `main` to trigger a single production deploy.

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
Event-specific promotional images may be sourced from official organizer, venue, attraction, tourism or promoter websites. Image files are downloaded and hosted locally rather than hotlinked, and source/credit information is retained when available. Category artwork is the fallback when a suitable official event-specific image is not available. Creative Commons and public-domain assets retain their required attribution and license metadata.

## Submission form
The form uses Netlify Forms (`data-netlify=true`) and a honeypot field. It will work automatically when the folder is deployed to Netlify. On another static host, connect `submit.html` to that provider's form handling service.

## Publish
Deploy this folder as-is to Netlify, Cloudflare Pages, GitHub Pages, or another static host. No build step or database is required.

## v3 taxonomy simplification
Public Explore filters use 10 visitor-friendly regions and 14 broad activity types. The original detailed regions/categories are retained in `assets/data.js` as `sourceRegion` and `sourceCategories`, so free-text search still benefits from the research taxonomy without exposing it as a huge filter list.

## v4 social enrichment
A research pass expanded social-link coverage across event listings. Supported platforms: Instagram, Facebook, TikTok, Bluesky, LinkedIn. X/Twitter is intentionally excluded.

## v5 image enrichment
- Real-image metadata records source URL, visible credit, usage type, and an internal rights/source note.
- The submission form accepts promo images/media-kit links with an authorization statement.

## v6 seasonal architecture
- Rebranded shell to **Utah Seasonal Guide** with Halloween & Fall 2026 as the current seasonal guide.
- Added sponsor-ready card infrastructure. Sponsored listings are hidden until `sponsored: true` is set and are always labeled.
- Added sourced accessibility summaries; absence of a badge means no verified accessibility claim was found, not that the event is inaccessible.
- Enforced **zero image hotlinks**. Only locally bundled image paths render.
- Accessibility summaries link to the organizer/venue source and use warning styling for explicit limitations.

## v7 broader event architecture
- **Occasion / Collection is optional.** Use it only when an event genuinely belongs to a holiday, season, heritage/cultural month, religious observance, or other editorial collection.
- **Event Type is separate and required.** Examples include Festival, Market, Convention, Film Festival, Parade, Concert, Workshop, Race, and Community Tradition.
- Standalone signature events may have a blank Occasion / Collection and still be eligible for the public **All** directory.
- Do **not** create or assign synthetic `Other` or `General Event` occasion values. Blank is the correct value when no collection applies.
- The backend **Notable Event** flag is the editorial mechanism for selecting major standalone events. It is independent of sponsorship and must never be treated as a paid-placement field.
- For website ingestion, holiday/season-tagged events remain eligible through their collections; blank-occasion events should be included only when they meet editorial inclusion standards, normally via **Notable Event**.
- Research/discovery explicitly includes signature cultural/community festivals, public fan/pop-culture conventions, notable specialty markets and expos, film festivals, parades/processions, and distinctive local traditions.
- Consumer/public access is required for standalone conventions, expos and markets. Vendor-only, trade-only, invite-only and private industry events are excluded unless they contain a separately listable public component.
- The holiday/season selector should be built only from real occasion/collection tags. Standalone notable events appear under **All** and through Event Type/search rather than creating another catch-all filter.
- Current seeded research targets include Utah Greek Festival, an Italian-American/Festa Italiana target, FanX, and the Strange & Unusual Market at Mountain America Expo Center.

## v8 metro geography + date-filter reliability
- Public geography collapses **Salt Lake City** and **Salt Lake Valley** into one **Salt Lake Metro** filter. It includes Salt Lake City plus valley communities such as Sandy, Draper, West Jordan, South Jordan, Midvale, Murray, Millcreek, Cottonwood Heights, Taylorsville, West Valley City, Riverton, Herriman, Bluffdale, Magna and Kearns.
- Detailed source geography may remain more specific internally, but the visitor-facing region filter should not split the metro into city vs. valley.
- Date filters must operate on actual occurrence dates, not only an event's first date or a broad season span.
- The date engine may conservatively infer recurrence only when the listing supplies a clear date range plus explicit weekday/daily hours. Phrases such as **select nights**, **hours vary by date**, or **performance schedule varies** must not be expanded into every date without stronger evidence.
- Exact current calendars override recurrence inference. Major recurring haunts with known calendar failures should be date-verified and stored with explicit occurrence dates.
- **Today**, **Tomorrow**, **This Weekend**, **Tonight**, date sorting, and schedule labels all use the same resolved schedule function so filtering and display cannot drift apart.

## Current image and visual policy
- Official organizer/venue/attraction/promoter hero and promotional images are acceptable event-specific imagery for the guide.
- Download and host those files locally; do not hotlink them from the source site.
- Record the original source URL and visible photographer/organization credit when available.
- Prefer a genuinely event-specific image over generic stock photography.
- Use the bold category SVG artwork when no suitable official event image is available.
- Category SVGs use a 16:9 composition with the primary subject kept in the center safe area for square crops.


## Brand system & social toolkit
- The permanent publication identity lives in `assets/brand.css` and `assets/brand/`.
- Core concept: **modern field guide + road atlas + cultural almanac**.
- Seasonal themes change accent colors, not the underlying identity.
- Editorial metadata such as **FIELD NOTE**, **VERIFIED**, region, date and price is intentionally part of the visual language.
- The complete usage guide is in `docs/brand-toolkit.md`.
- The internal, no-index social card maker is available at `/toolkit/`. It can pull from current event data, use event or uploaded photography, and export 1080×1350, 1080×1920 and 1080×1080 PNGs without a paid design service.
- Recurring social franchises: **The Weekend File**, **Tonight**, **Free This Weekend**, **Right Now**, **Last Chance**, **Worth the Drive**, **Adults Focused**, **Events for Kids**, **Found It**, and **Editor's Field Guide**. Each has a distinct editorial brief; dated human-curated leads and exclusions live in `assets/social-editorial.js`.
- Generative **Field Plates** replace generic placeholder images. They are selected automatically from event taxonomy + occasion and require no per-event artwork; see `assets/field-plates.js` and `docs/brand-toolkit.md`.
