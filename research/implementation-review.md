# Development preview review — October 6, 2026

This is a substantial development revision, not a completed production release. Production/main has not been changed.

## Delivered

- 528 canonical event pages: 517 announced listings and 11 pending listings. A listing can be announced while its full operating calendar remains incomplete.
- Eleven holiday/observance choices. One event can appear under several holidays without creating duplicate pages.
- Holiday colors, 55 seasonal vector placeholders, 11 social-sharing PNGs and a favicon; existing Halloween activity artwork retained. Día de los Muertos and Veterans Day have distinct artwork.
- Simplified 13-region and 12-activity filters, saved events, free admission, community, dates, tonight and open-now filters, progressive loading and readable event URLs.
- Editorial holiday ratings and practical flags. Cultural communities are not ranked as attractions. Holiday tags and community affiliation are separate fields.
- 406 listings have explicit normalized visit dates. 111 announced listings still need complete operating dates. Unknown schedules do not appear in date-sensitive searches. Unknown hours produce clearly labeled all-day calendar reminders. Utah timezone, DST changes, overnight sessions, ICS escaping and all-day boundaries are tested.
- Revised public copy, separate accommodations information, organizer links, corrections, credits and mobile layouts.
- Suggest/correct form builds an email to jerekeys@gmail.com, validates fields and dates, and provides a copyable fallback. It requires the visitor to finish sending in an email app; it is not an automatic server-side delivery endpoint.
- Five new events added to the native research workbook, with exact source hyperlinks. EVE watchlist lead resolved. ZooLights, PAAG date conflict and two Southern Utah Hanukkah leads demoted after source review.

## Research and photographs

Searches extended across organizer calendars, venues, libraries, nightlife, community meals, cultural observances, sensory accommodations, winter workshops and current-year ticketing. Old dates, out-of-state results and holiday dates without event confirmation were excluded. No claim of exhaustive Utah coverage is made.

The source image inventory covers all 528 listings. Initial automated discovery found candidates on 430 listings; this is a candidate inventory, not 430 approved event photographs. Generic navigation imagery, stock, logos, wrong-event posters and low-resolution files still require rejection. The choir image inspected was a 2027 spring/summer collage, not the Christmas show, and was rejected. The inspected Luminaria image was too small for the intended use. Christkindlmarkt and Grand America holiday-tea photographs were reviewed and imported locally; 42 listings now have locally hosted images. Organizer provenance is recorded; no open image license is claimed.

## QA

Local and GitHub checks validate event IDs, page/asset paths, 546 pages of local links, normalized dates and calendar edge cases. Browser review at 390, 768 and 1440 pixels exercises holiday/date/free filters, saving, event details, calendar controls, form labels and image loading. It found and led to fixes for ARIA semantics, narrow-screen event overflow and relative image URLs. Automated WCAG scans cover the directory pages under test; they are not a complete ADA assessment. A final mobile review also prompted a visible two-row navigation, shorter hero and fully expanded filter panels.

Remaining release checks: inspect the actual Netlify development deployment while signed in with an invited account; review other page types, all theme contrast states, keyboard-only and screen-reader use, zoom/reflow, iOS Safari and Android Chrome; verify calendar import on real calendar clients; complete image/rights review; resolve missing date/hour records; and verify message delivery if replacing the email-composer form with a direct submission endpoint.

## Recommendations

UtahEverySeason.com was available in Porkbun's live search on October 6, 2026 at $11.08/year, with $11.08 listed renewal. It was not purchased. Cloudflare listed standard .com registration and renewal at $10.46. Keep the existing Netlify/GitHub preview workflow for now; Cloudflare Pages is an affordable alternative for this static site, with a free plan allowing 500 builds/month.

Start with an installable web app before native iOS/Android. A native app becomes more useful with saved outings, optional reminders, offline plans and maps. A website wrapper alone risks Apple's minimum-functionality rule. Developer-account fees currently list $99/year for Apple and $25 one-time for Google Play, before engineering and maintenance.

Prioritize correction reports, last-checked organizer links, shareable saved outings and opt-in reminders. Add a moderated photo feed with date, event, credit and consent. Introduce visitor reviews later, showing visit dates and separating visitor opinion from editorial seasonal ratings and factual accommodations. Avoid anonymous unmoderated feeds and pay-to-rank placements.
