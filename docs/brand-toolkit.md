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

## Photography and Field Plates
Photography does not need one color grade. The publication frame provides consistency.
- Prefer real event/venue photography when it accurately represents the listing.
- Keep source/credit records.
- Do not hotlink.
- Do not fake event photography with generic stock.
- When no real photo exists, the site automatically renders a **Field Plate** instead of a generic placeholder.

### Field Plates are generative, not per-event assets
Do **not** create a new placeholder file when adding an event. `assets/field-plates.js` uses existing event metadata to choose a reusable specimen family, seasonal/occasion treatment, region annotation, and deterministic plate number. A new event therefore requires zero illustration administration.

Current specimen families cover haunts, harvest/farms, lights, markets, performance, food, outdoors, workshops, nightlife, family/Christmas, giving, film, parades, fandom/conventions, residential displays and community/culture. Culturally specific treatments include Día de los Muertos, Diwali, Hanukkah, Yule/Solstice and Pride.

The old `placeholder` value may remain in legacy/generated event data for compatibility, but the public site and social toolkit do not use it when photography is absent.

**Maintenance rule:** add a new specimen family only when a genuinely new event class repeatedly appears and the existing families communicate it poorly. Do not add one for a single event.

Field Plates deliberately say **NO EVENT PHOTO**. They should never be mistaken for documentary photography or imply a location-specific map. Contour lines are abstract field-guide texture, not real topography.

## Social editorial franchises
Use these repeatedly so followers learn the formats:
1. **The Weekend File** — Salt Lake-first weekly shortlist led by major moments and one-day events.
2. **Tonight** — low-friction same-day plans with concrete hours and a live/one-night bias.
3. **Free This Weekend** — genuinely free, community-minded plans; it may return a shorter set rather than pad the post with weak regional matches.
4. **Right Now** — one coherent current holiday or cultural story told through meaningfully different event types.
5. **Last Chance** — limited runs that are actually ending soon, ordered by urgency.
6. **Worth the Drive** — destination experiences where leaving the Wasatch Front is part of the premise.
7. **Adults Focused** — verified 21+, nightlife, drinks and distinctly grown-up programming.
8. **Events for Kids** — child-specific programming screened for age fit, intensity and practical timing.
9. **Found It** — unusual, specific and under-the-radar discoveries rather than another roundup of major attractions.
10. **Editor's Field Guide** — a Salt Lake-first forward-looking sampler that balances a headline, a timely one-off and different ways to go out.

Each franchise has a separate selection policy. Ordinary series reserve at least two-thirds of available slots for Salt Lake Metro events; **Worth the Drive** reverses that rule. Explicit selections, exclusions and dated lead choices live in `assets/social-editorial.js` and outrank automated scoring. The toolkit displays a short rationale for every selection. Events used in a downloaded browser-generated package are deprioritized for 14 days so consecutive posts rotate when qualified alternatives exist.

The internal browser tool lives at `/toolkit/` and exports a complete 1080×1350 carousel plus a matching vertical-video production request. It pulls directly from `assets/data.js` and leaves every selection reorderable, replaceable or removable.

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
5. If the event has no real photo, the toolkit automatically uses its Field Plate. Keep it or upload a stronger event image.
6. Adjust the headline/details.
7. Export the PNG.
8. Edit/copy the caption starter.
9. Add platform-native alt text/captions when publishing.
10. Point people back to the relevant filtered page or event page rather than only the homepage.


## Media frame + no-photo artwork
Event photography and generated no-photo artwork use the same publication frame:
- inset keyline;
- field glyph + **UTAH EVERY SEASON** tab;
- **FIELD NOTE** identifier;
- occasion/season label.

The frame is the brand. The underlying image is the subject. Do not repeat the event title or dense metadata inside website-card media.

When no trustworthy event photograph exists, `assets/field-plates.js` generates a restrained specimen illustration over a topographic-inspired contour field. The illustration itself stays centered and fully visible; the contour field is recomposed to the destination dimensions rather than cropping a single master.

Built-in field-art presets:
- `card` / `hero`: 1600×900
- `square`: 1080×1080
- `portrait`: 1080×1350
- `story`: 1080×1920

The social toolkit also requests field artwork at the exact dimensions of its media region, so changing from feed portrait to square or Story/Reel recomposes the contour field while preserving the central specimen.
