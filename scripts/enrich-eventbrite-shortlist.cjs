#!/usr/bin/env node
/* Fetch organizer, venue, price and official-image details for the editorial
   shortlist produced by the statewide Eventbrite crawl. */

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const checkedOn = process.argv[2] || new Date().toISOString().slice(0, 10);
const ids = [
  '2000464681714', '2001095034115', '1999788122106', '1994592067567',
  '2003031576365', '2003209999032', '2002765395210', '2003248383842',
  '1990301658839', '2001097487453', '1998990307822', '2003043658503',
  '2003046396693', '1998504931047', '1999975561743', '1996471546138',
  '2002486517078', '1999738192766', '2002773146394', '2003376725716',
  '2002757950944', '1990446269373', '2000729400495', '2002954774649',
  '1991945879748', '1988736456276', '2001023141081', '1969841529040',
  '1991018082682', '2000891492316', '1978199111795', '2002098618864',
  '2003204533685', '1986090600450', '1992263906976', '2002228814282',
  '1998895378887', '2001006426086', '1993481734531', '2001095386168',
  '1978941183351', '1998339687800', '1997785724882', '1998250858108',
  '1998255397686', '1999719560035', '1999054288189',
];

async function getEvent(id) {
  const url = `https://www.eventbrite.com/api/v3/events/${id}/?expand=venue,organizer,ticket_availability,logo`;
  for (let attempt = 1; attempt <= 3; attempt++) {
    const response = await fetch(url, { headers: { 'user-agent': 'Mozilla/5.0 (Utah Every Season editorial research)' } });
    if (response.ok) return response.json();
    if (attempt === 3) throw new Error(`${response.status} for Eventbrite event ${id}`);
    await new Promise(resolve => setTimeout(resolve, attempt * 1500));
  }
}

function text(value) { return value?.text || ''; }

function compact(event) {
  const availability = event.ticket_availability || {};
  const min = availability.minimum_ticket_price?.display || null;
  const max = availability.maximum_ticket_price?.display || null;
  return {
    id: event.id,
    name: text(event.name),
    summary: event.summary || '',
    description: text(event.description),
    status: event.status,
    isFree: event.is_free,
    ticketAvailability: {
      available: availability.has_available_tickets ?? null,
      soldOut: availability.is_sold_out ?? null,
      minimum: min,
      maximum: max,
    },
    start: event.start,
    end: event.end,
    venue: event.venue ? { name: event.venue.name, ageRestriction: event.venue.age_restriction, address: event.venue.address } : null,
    organizer: event.organizer ? { name: event.organizer.name, url: event.organizer.url } : null,
    image: event.logo?.original || event.logo || null,
    url: event.url,
    changed: event.changed,
    categoryId: event.category_id,
    subcategoryId: event.subcategory_id,
    formatId: event.format_id,
  };
}

(async () => {
  const events = [];
  let cursor = 0;
  const workers = Array.from({ length: 6 }, async () => {
    while (cursor < ids.length) {
      const id = ids[cursor++];
      events.push(compact(await getEvent(id)));
    }
  });
  await Promise.all(workers);
  events.sort((a, b) => a.start.local.localeCompare(b.start.local) || a.name.localeCompare(b.name));
  const output = {
    checkedOn,
    source: 'Eventbrite public event API; organizer, venue, ticket availability and official image expansions',
    count: events.length,
    publicationRule: 'This file is a verification queue, not a publication list. Read the organizer description and any deeper ticket/accessibility material before adding an event.',
    events,
  };
  const outPath = path.join(root, 'research', `eventbrite-shortlist-${checkedOn}.json`);
  fs.writeFileSync(outPath, JSON.stringify(output, null, 2) + '\n');
  console.log(JSON.stringify({ outPath, count: events.length }, null, 2));
})().catch(error => { console.error(error); process.exit(1); });
