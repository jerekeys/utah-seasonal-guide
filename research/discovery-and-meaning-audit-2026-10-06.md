# Discovery and meaning audit — October 6, 2026

## Scope
Compared all 251 event rows plus the Weekend Planner and Vibes & Standouts sheets in the supplied read-only snapshot of Utah Halloween & Fall 2026 — Complete Ideas Guide against development source aabfb44 (539 listings). The attachment is historical reference, not a claim about its live Google Drive source. No original workbook or website event records were changed in this audit.

## Result
The website has better date filtering, calendar handling, year-round coverage and saved lists, but it does not yet match the original guide's editorial discovery depth. All 251 original event names match exactly; Age, Intensity, Category and research Region fields are unchanged for all 251. This rules out loss of those rows/fields, not errors inherited from the original research.

The original guide has 21 vibe entry points and 14 ready-made itineraries. The current website has 15 general vibe links; its route page offers generic category links rather than actual event combinations. Date night, dogs, live animals, books/stories, witchy, unusual local traditions, short stops and residential-display loops merit recovery as curated collections with date-valid event IDs. Do not restore old itinerary dates without checking present organizer schedules.

## Concrete drift and inconsistencies
| Listing / feature | Current problem | Needed treatment |
|---|---|---|
| Creepy Doll Head Necklace Drop-In Bar | Description says no reservation required; flags say Reservation required | Remove contradictory requirement after retaining source evidence; protect against negated phrase imports |
| Dave & Boo-ster's Moonlight Mixer | Description correctly says minimum age needs clarification; flags assert both 18+ and 21+ | Do not convert alcohol ID requirements or adult-oriented marketing into an admission age |
| Castle of Chaos | 18+ flag and 5/5 rating apply across the listing although description scopes adults-only full contact to Level 5 | Label Level 5 explicitly; distinguish selectable intensity from event-wide restrictions |
| Murder at the Juice Joint | Whole-event Sold out flag, although original note says October 28 sold out and October 30/31 were added | Store availability per performance; recheck checkout before asserting current availability |
| Black Island Farms / Nightmare Acres | Combined daytime farm/nighttime haunt only appears under Halloween and retains a teen-oriented age field | Add appropriate Fall coverage and scope audience/intensity by component |
| Cornbelly's Lehi | Original note had ages 3+ ticketed / 2 and under free; current narrative and practical notes omit it | Reverify and restore in admission details, without lengthening the card narrative |
| Silent Santa | Card and detail renderer both limit flags to five; resident priority and reservation requirement are hidden | Cards can summarize; event pages must expose all material booking restrictions |
| Locations | 156 listings repeat the final locality, e.g. Wellsville, Wellsville | Avoid appending city when it is already in venue/address |
| Dogs discovery | Dog events exist, but existing dog-oriented listings mostly lack a Dog-friendly flag and there is no dog vibe | Explicit verified pet policies, dog collection; service-animal access remains separate |
| Search | Detailed Category/sourceCategories are retained but excluded from the search text, despite the metadata claim that research tags remain searchable | Include searchable research tags without displaying all of them as filter options |

239 original listings had Extra notes; only one matched listing retains that field. Many useful notes were moved into descriptions, so this is not 238 proven losses. The migration needs semantic checks for admission exceptions, ticket inclusions, physical conditions, child guidance and separate programs, not a blanket copy of old notes.

## Import / display causes
scripts/import-seasonal.py concatenates category, flags, access notes, audience, price and research notes, then regex-matches labels anywhere in that text. It does not consistently recognize negation, per-date scope or optional tiers. Explicit structured admission and booking fields should own restrictions; narrative matching should raise an editorial review item rather than publish a firm flag.
assets/site.js flagsHTML uses slice(0,5) for both cards and details. Keep compact cards but show the complete practical information on details.
Do not treat all ages as a universal child recommendation, alcohol service as 21+ admission, free-to-enter as all activities free, or optional full-contact as the whole attraction's scare level.

## Photos
42 / 539 listings have images (7.8%); 497 use art. Original-guide coverage is 40 / 251 (15.9%). Existing photos include five Creative Commons images; most are official promotional sources.
The previous extraction audit lists 433 records with unreviewed candidates and 75 source-fetch failures, plus 20 without a candidate. These counts include existing photos and logos/navigation/stock, and therefore are not 433 usable replacements.
Visually reviewed three downloaded candidates:
- Ogden Día de los Muertos: OFOAM's 2024 photo shows an ofrenda, marigolds and the actual Ogden Amphitheater setting. Strong exact-event candidate; identify as a previous edition and establish reuse permission/credit.
  Source: https://ofoam.org/dia-de-los-muertos
  Asset: https://ofoam.org/images/econa-article-images/564/full/1600/diadelosmuertos-2024-4658-enhanced-nr.jpeg
- Staheli farm Fall page featured asset shows a witch character interacting at the farm. Authentic subject, but weak representation of the broad daytime farm listing; stronger for a witch-specific program.
  Source: https://stahelifamilyfarm.com/fall/
  Asset: https://stahelifamilyfarm.com/wp-content/uploads/2026/07/SFF-Page-Featured-Image-Fall-1-copy.webp
- Provo Pioneer Village: official site photo shows historic wagons/cabins. Good venue image if clearly labeled; does not itself depict the harvest festival.
  Source: https://www.provopioneervillage.org/
  Asset: https://www.provopioneervillage.org/wp-content/uploads/2024/08/DSC4838-scaled-e1724601089186-2048x1154.jpg

Lagoon Frightmares and Sundance Halloween Lift Rides already have relevant locally hosted photographs. Do not spend the next pass rediscovering those or replace them with generic logos.
The Commons Halloween-in-Utah category is sparse and includes irrelevant graphics; broaden searches by exact event, location, organizer and earlier editions. Verify the individual asset license, credit, subject and image quality. Official-page presence is provenance, not a reuse grant. Prior-year event photos and venue-only photos need honest captions/alt text. Posters can carry valuable schedule evidence but should not be mistaken for photography.

## Richer without clutter
Cards: image, title, current dates, location, admission summary, one or two descriptive sentences, and the two or three most consequential facts.
Details: complete hours, admission exceptions/inclusions, minimum age versus recommendation, booking requirements, access information and all practical flags.
Discovery: curated vibe collections and realistic nearby pairings, keeping expired combinations out of upcoming recommendations.
Research: retain source-backed facts in structured fields with per-field evidence/date. User-facing prose summarizes them; it must not become the only source for re-importing labels.

## Limits
Whole-list exact-field comparison and targeted semantic/source/image inspection completed. This is not a new human verification of all 539 organizer/ticket pages. No new photos published or permissions claimed. Findings are recorded for review; event corrections and expanded image sourcing remain implementation work.
