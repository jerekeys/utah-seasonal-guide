# Event evidence and review — October 6, 2026

Public listing and scheduling confidence are separate decisions. Keep an announced event discoverable when its organizer has published a current event or program but left stale prose elsewhere. Prefer current event-specific ticket variants, dated posters, structured calendar entries and specific organizer announcements over old descriptive text. A generic current-year footer or automatically updated holiday header alone does not establish a new event date. Identify uncertainty in the particular field; do not demote the entire event solely because some copy is old.

For admission, follow the organizer's actual Tickets/Buy/Register link, then the specific event and ticket-choice screen (normally one or two linked levels). Record adult/child, member/advance/door options and mandatory fees where shown. A blank extraction or unloaded widget does not mean prices are unannounced. Never infer free admission from an absent price.

Read event-specific posters visually, including dates, start times, venue, age restrictions and prices. Do not substitute a different upcoming-concert image. Record the exact source and inspection method. Embedded images and ticket widgets require a separate review when text extraction misses them.

Review accommodation/FAQ and venue pages, distinguishing event-specific provisions from general venue access and prior-season programs. Include mobility, hearing/ASL, vision, neurodivergent/sensory provisions, service-animal policies, companion options and request deadlines when documented. No absence of published information implies an inaccessible event.

Review holiday relevance and community affiliation separately. Cultural observances are not Halloween subcategories and do not receive scare ratings. A venue's name does not establish the event's holiday. Do not assign a community solely from a performer's assumed identity.

Dates used by search/calendar must be operating dates, not application deadlines or a continuous span between separate performances. Start times may be known even when running time is not. In that case, a calendar action creates an explicitly labeled one-hour reminder at the published start; it does not assert a one-hour performance.

`audit-event-sources.py` inventories every listing, follows actual admission/accommodation links up to two levels and stores page evidence and poster candidates. Its excerpts are research leads. Each record remains marked `humanReviewComplete: false` until an event-specific review is documented. Generic page navigation, unrelated products, registration prices and historical dates cannot be automatically promoted to event facts.

## Visitor descriptions, ranking and historical editions

Use “Why / thoughts” (workbook Research notes / column N) as visitor-facing editorial copy: one or two factual sentences describing the experience and any essential expectation. No research rationale, gap-filling commentary, ingestion instructions, unsupported superlatives or generic marketing slogans. Keep evidence and unresolved research work in QA/research fields. Practical uncertainty that affects a visit belongs in date, price, access or before-you-go fields; do not hide it merely to sound confident.

Export the native Notable Event checkbox as the boolean `notable_event`. Do not infer it from paid placement, a current date, title adjectives or missing holiday tags. The default order after filtering is notable with a confirmed occurrence between today and 45 days ahead (inclusive), single-day, then alphabetical; explicit sort choices take precedence. Past editions, undated listings and distant future notable events get no notable boost. Untagged notable events remain available under All, search and activity filters.

Historical editions use verified historical operating dates, retain genuine verification timestamps and are hidden from default results once ended. Show past events and specific past date searches reveal them. Never assign a historical program, cost, performer or accommodation to the next year without current evidence. Link future editions through distinct dated records; do not silently replace a previous edition’s dates.

## Images and explained collections

Select photos from official organizer, venue, destination or organizer social sources, or a Creative Commons repository. Verify that the image depicts the actual event, location or activity attractively and has adequate source dimensions. Avoid logos and inserted graphic text; use a suitable photo area from a poster when available. Optimize locally, preserve credit and CC license information, and write literal descriptive alt text. Clearly identify venue-only views or past-edition photos when needed. The publisher has authorized selection under these criteria; individual image approvals are not required.

Each vibe needs a concrete visitor-facing explanation and an intentional matching rule. Do not equate free admission with free purchases, dog sessions with a universal pet policy, all-ages admission with a child recommendation, or ordinary evening events with sensory-friendly provision. Upcoming examples must respect ended-event filtering; a vibe combines with date, place, occasion and other search filters.
