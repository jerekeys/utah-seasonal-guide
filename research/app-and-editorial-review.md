# App, privacy and editorial follow-up — October 6, 2026

## Delivered for development

- Installable manifest, standard and maskable PNG icons, Apple touch icon, service worker and platform-specific install guidance.
- My saved events in primary navigation, current saved count, reload persistence, export/import for separate browser/app storage.
- Offline shell, cached event data, visited event pages, connection notice and unavailable-page fallback. Forms and purchases are never queued offline.
- Anonymous site forms for event suggestions and contact/sponsorship inquiries; personal email composer removed.
- Plain-language editorial discretion, required submission acknowledgment, limited permission to edit/display submitted material; terms, privacy and sponsorship disclosure.
- Up to two time-limited paid placements above search, no fabricated advertisers, labels on both paid cards and destination pages.
- Deployment stages only public files. Research, tooling and dependencies are not served by Netlify.

## Event discoveries and corrections

Public blog and indexed social leads from Utah's Best Kept Secrets were checked against current organizers. Grand America's Witches Tea and Snowbasin's SnowWiesn Oktoberfest were absent and have been added. Most named farm/light attractions were already represented. Instagram's full current feed was throttled; this was not a complete feed review. Older posts contain dates and claims that cannot be substituted for 2026 organizer evidence.

Witches Tea: Sept 25–Nov 1, 11 AM–4 PM advertised event window; $55 adults/$39 age 12 and under, plus 18% gratuity and sales tax. Actual reservation availability can vary. Source: https://www.grandamerica.com/events/witches-tea-2026-10-07 and corroborating Oct 8 page. General afternoon-tea weekday hours differ and were not copied. Hotel's access page is about digital access, not physical venue access.

SnowWiesn: weekends Aug 29–Oct 18, noon–6 PM; $10 posted single-day admission, pass-holder access, free parking, leashed dogs on grass, no re-entry. Organizer's ticket shop returned 403, so extra charges and age variants remain unverified. Source: https://www.snowbasin.com/events/snowwiesn-oktoberfest/ .

PAAG Christmas Dinner heading says Dec 18; description says Dec 19. Event remains visible, with no invented date/calendar entry. Source: https://www.paagutah.org/paag-events/christmas-dinner .

## Verification boundary

Automated Chromium/Android and WebKit/iPhone engine checks do not prove physical home-screen installation, native share-sheet behavior or Apple Calendar import. Live Netlify preview and form-delivery verification are blocked by invited-account sign-in. Forms require Netlify form detection to be enabled and both form names to be detected after deploy; notifications can later go to a separate site inbox without exposing the address in source.

User QA should be five minutes of real-device interaction, not 81 source pages: install and reopen, save/reopen an event, open one image and one calendar link, send one clearly labeled test suggestion and confirm receipt in Netlify. Editorial source review remains our responsibility. The site currently contains 531 records; the earlier complete evidence collection was for 528 and remains distinct from a completed human review.

## Year-round extension

A grouped native dropdown replaces the horizontal holiday-button roster and defaults to All. The initial planning roster contains 80 buckets across four groups, spanning October 2026–October 2027. Fall and Halloween are separate; mixed harvest/haunt destinations may carry both. Samhain has its own category. The canonical workbook has Annual Calendar Roster plus separate Fall, Halloween and Samhain views.

Cougar Pride Center announces Pride in Progress on April 10, 2027: https://www.cougarpridecenter.org/pride . Only that date is reused; historical venues, performers and hours are not assigned to 2027. Admission and venue details remain forthcoming. Pride graphics use a locally hosted rainbow/heart SVG in the existing icon approach.

The browser regression suite passed all three widths (390, 768, 1440): holiday separation, empty future bucket, Ogden Día, image navigation, calendars, labels, date validation and intercepted suggestion submission. Android-engine checks reached and passed installability, persistence, export/import and offline event/search behavior; an asynchronous offline-notice assertion is being rerun with a visibility wait. Full engine results and physical installation remain distinct.
