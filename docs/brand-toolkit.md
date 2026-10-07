# Utah Every Season — Brand & Social Toolkit

## Brand idea
**Utah’s obsessive guide to what to do next.**

The visual system treats the site like a modern Utah field guide: researched, annotated, practical, slightly eccentric, and built to reward curiosity. It should never resemble a generic tourism bureau, ticketing marketplace, or beige lifestyle blog.

## Permanent identity
- **Name:** Utah Every Season
- **Tagline:** Utah’s obsessive guide to what to do next.
- **Concept:** field guide + road atlas + cultural almanac
- **Core signal color:** Signal Orange `#EF5A29`
- **Field Ink:** `#17221D`
- **Field Paper:** `#F5F0E4`
- **Panel:** `#FFFDF8`
- The field mark is in `assets/brand/field-mark.svg` and `field-mark-ink.svg`.

Seasonal colors are accents, not rebrands. Halloween, Christmas, Pride, summer, etc. may change accent palettes while typography, mark, grid, metadata treatment, and editorial voice remain constant.

## Typography
No paid font dependency.
- **Display / editorial:** system serif stack (Iowan/Palatino/Georgia)
- **Body:** system sans
- **Metadata / verification / labels:** system monospace

The contrast between editorial serif headlines and monospaced metadata is a defining part of the identity.

## Information as decoration
Research is part of the product, so small factual metadata may become graphic language:
- FIELD NOTE 0472
- VERIFIED OCT 06
- SALT LAKE METRO
- FREE
- WORTH THE DRIVE
- TONIGHT

Do not expose internal workflow notes, confidence debates, spreadsheet mechanics, or research process. Public metadata should help someone decide what to do.

## Photography
Photography does not need one color grade. The publication frame provides consistency.
- Prefer real event/venue photography when it accurately represents the listing.
- Keep source/credit records.
- Do not hotlink.
- Do not fake event photography with generic stock.
- When no real photo exists, use clearly illustrated field-guide artwork.

## Social editorial franchises
Use these repeatedly so followers learn the formats:
1. **The Weekend File** — weekly roundup / carousel cover.
2. **Worth the Drive** — one destination event worth traveling for.
3. **Found It** — obscure, strange, or easy-to-miss discovery.
4. **Tonight** — timely same-day recommendation.
5. **Free This Weekend** — saveable free-event roundup.
6. **The Field Guide** — thematic collection (pumpkin patches, lights, Pride, film festivals, etc.).

The internal browser tool lives at `/toolkit/` and exports 1080×1350, 1080×1920, and 1080×1080 PNGs. It can pull directly from `assets/data.js` or use manual copy and a local uploaded image.

## Editorial visual rules
- One strong headline; do not cram full event descriptions into a graphic.
- Use the site for dates, pricing, maps, accessibility detail, and source links.
- “Verified” means the underlying record was actually checked.
- Sponsored material must remain explicitly labeled; never style paid inclusion as an editorial accolade.
- Avoid marketing puffery. Describe what the experience is and why it is notable.
- Maintain accessible contrast. Signal Orange works best as a mark/accent, not long body text on light backgrounds.
- Never use the field mark as a decorative bullet so often that it loses recognition value.

## Website behavior
The permanent brand layer lives in `assets/brand.css`. Seasonal palette variables continue to come from `assets/seasonal.css`. The field-guide layer should survive future holiday/season additions without component redesigns.

## Social workflow
1. Verify/update the event in the database.
2. Open `/toolkit/`.
3. Choose the editorial series and event.
4. Choose the current season palette.
5. Adjust headline/details; upload a stronger image if needed.
6. Export the PNG.
7. Edit/copy the caption starter.
8. Add platform-native alt text/captions when publishing.
9. Point people back to the relevant filtered page or event page rather than only the homepage.
