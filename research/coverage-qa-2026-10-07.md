# Coverage and discovery review — October 7, 2026

## Result

- 572 listings; 289 have a reviewed, locally hosted photograph (50.5%).
- 32 additional completed September/early October events, plus Snowbird Oktoberfest, which started in August and continues through October 11.
- Ten additions cover Labor Day weekend; Snowbird also explicitly includes Labor Day.
- Calendar seasons are additive: Fall September–November, Winter December–February, Spring March–May, Summer June–August. Holiday, religious, cultural and community membership remains separate.
- The canonical event database received 33 listings and additive season labels in 458 existing cells. Existing normalization formulas were preserved.

## Search architecture applied

Historical discovery used date-bounded September/early October programs, with primary organizer archives, municipal calendars, university programs, tourism event calendars, parks, performance calendars and ticket systems. Searches covered Salt Lake, Utah County, Davis, Weber, Box Elder/Cache, Park City/Wasatch Back, Tooele, Moab, Vernal, Richfield, Cedar City and Southern Utah. Coverage included Labor Day civic traditions, cultural and heritage festivals, Pride, arts and crafts, music and storytelling, film, fairgrounds, parks, river programs, endurance sports and off-road recreation. The dated evidence for each accepted addition is in `september-backfill-2026-10-06.json`.

Source conflicts were resolved using the dated primary program. Examples include PhenomeCon's September 9–12 dates, Camp Floyd's actual Fairfield location, Garden of Quilts' shortened Friday hours and cancelled Meet the Maker activity, and Deer Valley's separate adult tasting and younger non-drinking admission. The Avenues Street Fair was not incorrectly backfilled from a superseded September notice: the current date is October 10. Events already represented were not duplicated. This is a substantial expansion, not a claim that every past Utah event has been found.

Where an archived ticket tariff could not be recovered, the listing says the archived price is unverified. It does not claim that the organizer never announced a price. Historical event dates are retained; verification dates were not artificially backdated.

## Photographs

Candidates were visually inspected from official event, venue, government, tourism and producer pages or Wikimedia Commons. Selection required the actual event, activity, named venue or location. Posters with inserted text, logos, unrelated performers, wrong locations and insufficiently sized thumbnails were rejected. Venue and historical images are explicitly labelled. Image source and applicable CC license links are retained. The Commons search for Ashton Gardens returned locations in England, which were rejected rather than attached to Utah listings.

The selected-image ledger is `photo-selection-coverage-2026-10-06.json`. `assets/reviewed-photo-manifest.json` identifies the 131 additional graphic assets and a perceptual subject check. The package workflow downloads only these reviewed sources and rejects a changed subject or incomplete package before advancing development. All 289 listing image files decoded locally. Six damaged intermediate files were repaired and checked before packaging.

## Functional checks

Local full-list checks passed for asset paths, Utah dates, weekday schedules, overnight visibility, calendar UTC/DST conversion and escaping, known performance start times, chronological sorting tiers, explicit sorts, recurring versus single-day classification, past-event behavior, public editorial language and additive holiday/season membership. Local HTML link checks passed on 603 pages. Public staging excludes research files, source tools and dependencies.

Default order: notable events with an upcoming occurrence within 45 days, chronological by start date; then genuinely single-day annual or one-off events, chronological; then remaining events, chronological. Explicit name, date or cost sorts take precedence. Vibes retain their explanations and exploration links, with examples removed. Credits begin with the camera marker. Event card images link to event pages.

The complete development package passed its GitHub Actions review at source commit `d93a9a51f1d131cea4b36ff4c822ba39521cb6bf` (workflow run `37553949249`) and advanced the `development` branch to that exact commit. The package regenerated and verified all 131 new reviewed photo assets before testing.

Browser checks passed at 390, 768 and 1440 CSS pixels. They covered the current-season default, distinct spring/summer/winter themes, Ogden holiday filtering, image-to-event navigation, the three-tier default sort, explicit sort overrides, archive visibility and persistence, date searches, saved events, calendar generation, vibe explanations, form validation, photo-permission acknowledgement, responsive overflow, broken images and automated accessibility checks. No browser errors, broken listing images, horizontal overflow or automated accessibility violations were reported on the tested pages.

The final visual review corrected the generic October view to use fall artwork, added distinct spring and summer illustrations, removed unintended fills from the winter snowflake and restored a compact desktop hero so the search controls remain visible. The import path now recognizes both slash- and pipe-separated category fields, preventing valid holiday/season overlaps from being dropped during future imports.

Installable-app checks passed in Chromium and WebKit device emulation, including manifest validity, saved-event persistence, list export/import, offline search, cached event pages, offline fallback behavior and preservation of a failed submission. These are automated browser/device-emulation checks; physical installation on an Android phone and an iPhone remains a launch check.

The Netlify development URL is protected by team authentication. The development branch and deployable package are verified, but an unauthenticated browser cannot independently inspect the hosted result. Production remains untouched.
