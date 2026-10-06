# Public launch readiness — October 6, 2026

## Assessment

The development version is suitable for a small invited trial after the new archive/sort browser checks pass. It is not yet verified for an unrestricted public launch. Buying a domain can happen independently; do not announce a public launch until the launch-critical checks below are complete. No production promotion or domain purchase was made in this pass.

**utaheveryseason.com** fits the year-round scope, is easy to say and avoids limiting the guide to holidays. A direct Verisign .com registry RDAP request on October 6 returned HTTP 404 (no registered domain found): https://rdap.verisign.com/com/v1/domain/utaheveryseason.com . This does not reserve it; registrar checkout must confirm availability. Decide whether the public brand becomes “Utah Every Season” before sharing widely, so the site title, home-screen icon name and social accounts agree.

## Required before public launch

| Check | Current evidence | Remaining action |
|---|---|---|
| Live production deploy | Development source only; previous hosted preview required invited-account sign-in | Promote the reviewed development release, then test the public address without sign-in. Keep developer previews private or excluded from indexing. |
| Suggestions and contact | Static Netlify form names, validation, failure preservation and offline guards tested | Enable Netlify form detection, verify both forms are detected, send one labeled test through each live form and confirm actual receipt and private notification delivery. |
| Public contact | Contact/sponsorship form has no personal name or address | Create the separate inbox and configure private notifications. Confirm someone monitors corrections and inquiries. |
| Phone installation | Prior Android Chromium and iPhone WebKit engine QA passed | On an actual iPhone, install/reopen, save/reopen and import a calendar event. Android native installation remains a physical-device check too; do not advertise it as physically verified yet. |
| Event accuracy | 539 records, whole-list date/link checks; source sweep collected evidence but did not finish human verification | Resolve high-impact dates, ticket prices/fees, hours, venues and accommodation claims for launch-visible upcoming events. Read posters and follow ticket choices rather than equating extraction failures with unannounced details. The 81 unread pages are an editorial research queue, not user homework. |
| Image permissions and access | Local images, credits, alt text and illustrated fallbacks; automated access checks | Confirm publishable rights for every photographic asset. Manually check keyboard navigation, zoom, screen-reader labels, form feedback and phone touch controls. Automated checks alone do not establish complete ADA conformance. |
| Domain and search | Friendly URLs and sitemap already exist; this pass adds SITE_URL-based generation and preview noindex staging | Configure domain/DNS/HTTPS in Netlify, set production SITE_URL, rebuild and inspect canonical links, sitemap, robots and share-image URLs. Add Search Console ownership and submit the sitemap. Test redirects from the old production hostname. Moving to a new hostname creates separate local saved-list storage; export/import preserves a visitor’s list. |
| Editorial and paid listings | Terms, privacy, discretion and paid-placement disclosure exist | Review those pages as the actual publisher; establish correction response and sponsor approval practices. Ordinary inclusion stays free; do not sell undisclosed ranking. |
| Updates and recovery | Git history, development workflow and cached app update notice exist | Retain a known-good deploy; check the first update in an installed app and refresh stale cached data. Set a manageable editorial refresh schedule and review cancellations near the event date. |

The user’s useful contribution is a short real-phone visit and verification of live form receipt, plus decisions about brand/domain and the inbox. Event research and source review remain the editor’s work.

## This pass

- Read all 531 existing descriptions; explicitly rewrote 331 and retained factual descriptions that already met the standard. Descriptions focus on activities and practical expectations, with no gap-filling rationale or unsupported best/strongest claims.
- Cleaned 17 practical notes that described unfinished research. Source conflicts remain explicit in scheduling fields because visitors need that uncertainty.
- Synchronized 412 changed visitor-description cells in Event Database column N, preserving formulas and neighboring structure. Added eight complete rows with native Notable Event checkboxes and verified contents/format metadata.
- Default filtered ordering: boolean `notable_event: true`, then single-day listings, then A–Z within each group. Explicit A–Z, date or cost sorts override those tiers. Paid placements remain separate and disclosed above search.
- Existing website/canonical rows had no true notable flags at the start of this pass. Added significant festival/convention archive records and the newly announced 2027 Greek Festival as notable; future imports read the workbook’s Notable Event field without inventing occasion tags.
- Show past events is unchecked initially and includes ended events when enabled. A past date selection enables it; URL state persists. Ended listings are labeled, their individual pages explain that dates/prices concern that edition, and calendar links never offer past dates. No verification or publication timestamps were backdated.
- Historical additions: Harvest Moon September 19; FanX September 24–26; Greek Festival September 11–13; Festa Italiana September 19–20; Dogden September 12; Peach Days September 9–12; Ogden Pride’s Sunday main festival October 4. Its October 3 opening party is a separate program, not a September event.
- Future addition: Greek Festival September 10–12, 2027, from its organizer’s explicit announcement. Prior-year price, hours and detailed accommodations are not assigned to 2027.

## Evidence and limits

Whole-list data/calendar checks and local links pass for 539 records and 570 HTML pages. New unit checks cover notable priority, single-day priority, explicit-sort overrides, Utah date boundaries, unknown dates and historical filters. Browser regression checks cover real controls, archive labels, calendar suppression and filtered order at 390/768/1440 pixels. The refreshed hosted browser results will be stored in research/qa; do not substitute a previous run for this release.

Historical facts were read from dated organizer/organizer-ticketing pages, with current tourism corroboration for Ogden Pride. Some source pages have stale boilerplate: the Greek 2026 ticket page’s anniversary number is old, but its event dates, hours, price and access policy are specific; the date is not demoted for that copy error. FanX’s active ticket checkout has closed after the event, so archived advertised pass prices are labeled accordingly. Peach Days has multiple venues and component schedules; an undifferentiated all-day opening time is not invented.

Sources:
- https://ogdendowntown.com/harvestmoonogden/
- https://fanxsaltlake.com/ticket-info/
- https://fanxsaltlake.zendesk.com/hc/en-us/articles/24085123050263-What-are-the-hours-at-the-event-including-registration-programming-and-entry
- https://fanxsaltlake.zendesk.com/hc/en-us/articles/360007590913-ADA-Accommodations
- https://www.bigtickets.com/e/salt-lake-city-greek-festival/2026/
- https://www.saltlakecitygreekfestival.com/
- https://www.festaitalianaslc.com/about-festa
- https://ogdendowntown.com/dogden/
- https://www.boxelderchamber.com/peach-days/
- https://www.ogdenpride.org/news/ogden-pride-festival-2026-persist-resist-exist/
- https://www.visitogden.com/events/12th-annual-ogden-pride-festival/
- https://docs.netlify.com/manage/forms/setup/
- https://docs.netlify.com/manage/forms/notifications/
- https://docs.netlify.com/manage/domains/domains-fundamentals/understand-domains/
- https://developers.google.com/search/docs/appearance/structured-data/event

Google event-result eligibility needs further structured-data refinement: the current generated markup is basic and lacks complete address information on many records. This is a search enhancement, not a promise that Google will display special event results.
