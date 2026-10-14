#!/usr/bin/env node
/* Crawl Eventbrite's public Utah index, deduplicate it against the site, and
   produce a review queue. This is discovery only; public listings still need
   organizer/ticket verification before publication. */

const fs = require('fs');
const vm = require('vm');
const path = require('path');

const root = path.resolve(__dirname, '..');
const checkedOn = process.argv[2] || new Date().toISOString().slice(0, 10);
const from = process.argv[3] || checkedOn;
const to = process.argv[4] || `${checkedOn.slice(0, 4)}-12-31`;
const base = 'https://www.eventbrite.com/d/united-states--utah/all-events/';
const searchApi = 'https://www.eventbrite.com/api/v3/destination/search/';
const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
const csrf = Array.from({ length: 64 }, () => alphabet[Math.floor(Math.random() * alphabet.length)]).join('');

const context = { window: {} };
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(root, 'assets/data.js'), 'utf8'), context);
const existing = context.window.SITE_DATA.events;
const knownUrls = new Set(existing.map(e => (e.Website || '').split('?')[0].replace(/\/$/, '')));
const knownEventbriteIds = new Set(existing.flatMap(e => {
  const match = (e.Website || '').match(/tickets-(\d+)/);
  return match ? [match[1]] : [];
}));
const normalizeName = value => (value || '').toLowerCase().replace(/\b2026\b/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
const knownNames = new Set(existing.map(e => normalizeName(e['Event / attraction'])));

function extractServerData(html) {
  const marker = 'window.__SERVER_DATA__ = ';
  const start = html.indexOf(marker);
  if (start < 0) throw new Error('Eventbrite server data not found');
  const jsonStart = start + marker.length;
  let depth = 0;
  let inString = false;
  let escaped = false;
  for (let i = jsonStart; i < html.length; i++) {
    const char = html[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (char === '\\') escaped = true;
      else if (char === '"') inString = false;
      continue;
    }
    if (char === '"') inString = true;
    else if (char === '{') depth++;
    else if (char === '}' && --depth === 0) return JSON.parse(html.slice(jsonStart, i + 1));
  }
  throw new Error('Eventbrite server data was incomplete');
}

async function fetchPage(page) {
  const body = {
    event_search: {
      date_range: { from, to },
      page_size: 20,
      dedup: true,
      dates: 'current_future',
      places: ['85688567'],
      page,
    },
  };
  for (let attempt = 1; attempt <= 3; attempt++) {
    const response = await fetch(searchApi, {
      method: 'POST',
      headers: {
        'user-agent': 'Mozilla/5.0 (Utah Every Season editorial research)',
        'content-type': 'application/json',
        'referer': base,
        'x-csrftoken': csrf,
        'cookie': `csrftoken=${csrf}`,
      },
      body: JSON.stringify(body),
    });
    if (response.ok) {
      const searchData = await response.json();
      return { search_data: searchData, page_count: searchData.events?.pagination?.page_count || 1 };
    }
    if (attempt === 3) throw new Error(`${response.status} for Eventbrite search page ${page}`);
    await new Promise(resolve => setTimeout(resolve, attempt * 2000));
  }
}

function haystack(event) {
  return [event.name, event.summary, ...(event.tags || []).map(t => t.display_name || '')].join(' ').toLowerCase();
}

const positiveRules = [
  [9, /halloween|haunt|spooky|witch|ghost|costume|pumpkin|samhain/],
  [9, /christmas|holiday|santa|nutcracker|lights|carol|yuletide|winter market/],
  [9, /hanukkah|chanukah|kwanzaa|diwali|solstice|las posadas|día de los muertos|dia de los muertos/],
  [8, /thanksgiving|friendsgiving|turkey trot|veteran|indigenous|native american|native arts/],
  [6, /festival|fair|parade|market|bazaar|carnival|celebration|block party/],
  [5, /drag|cabaret|burlesque|nightlife|dance party|costume contest/],
  [4, /concert|opera|theatre|theater|musical|ballet|orchestra|choir|comedy|film screening|live music/],
  [4, /cultural|heritage|community|mutual aid|fundraiser|charity|benefit|lgbtq|queer|pride/],
  [3, /family|kids|children|all ages|craft|maker|storytime|museum|zoo|garden/],
  [3, /food|tasting|brunch|dinner|cocktail|beer|wine|cider/],
  [2, /outdoor|hike|nature|run|5k|sports|competition/],
];
const negativeRules = [
  [12, /webinar|online event|virtual event/],
  [9, /real estate|mortgage|insurance|sales training|investor|entrepreneur|business networking|career fair/],
  [7, /conference|summit|certification|continuing education|professional development|leadership training/],
  [5, /weekly|every week|recurring class|support group/],
];

function score(event) {
  const text = haystack(event);
  let value = 0;
  const reasons = [];
  for (const [points, rx] of positiveRules) if (rx.test(text)) { value += points; reasons.push(`+${points} ${rx.source.split('|').slice(0, 3).join('/')}`); }
  for (const [points, rx] of negativeRules) if (rx.test(text)) { value -= points; reasons.push(`-${points} ${rx.source.split('|').slice(0, 3).join('/')}`); }
  if (event.is_online_event) value -= 12;
  const city = event.primary_venue?.address?.city || (event.locations || []).find(location => location.type === 'locality')?.name || '';
  if (/Salt Lake City|South Salt Lake|Murray|Sandy|Draper|West Jordan|West Valley City|Millcreek|Midvale|Cottonwood Heights/i.test(city)) value += 3;
  if (event.start_date === event.end_date || !event.end_date) value += 1;
  return { value, reasons };
}

function compact(event) {
  const ranked = score(event);
  const locality = (event.locations || []).find(location => location.type === 'locality')?.name || '';
  return {
    eventbriteId: event.eventbrite_event_id,
    name: event.name,
    summary: event.summary,
    startDate: event.start_date,
    endDate: event.end_date,
    startTime: event.start_time,
    endTime: event.end_time,
    timezone: event.timezone,
    venue: event.primary_venue?.name || '',
    address: event.primary_venue?.address?.localized_address_display || '',
    city: event.primary_venue?.address?.city || locality,
    url: event.url,
    ticketUrl: event.tickets_url,
    image: event.image?.original || event.image || null,
    tags: (event.tags || []).map(t => t.display_name).filter(Boolean),
    score: ranked.value,
    scoreReasons: ranked.reasons,
  };
}

(async () => {
  const first = await fetchPage(1);
  const pageCount = Math.min(first.page_count || 1, 49);
  const pages = new Map([[1, first]]);
  const workers = Array.from({ length: 6 }, async (_, worker) => {
    for (let page = 2 + worker; page <= pageCount; page += 6) pages.set(page, await fetchPage(page));
  });
  await Promise.all(workers);

  const found = new Map();
  for (const page of [...pages.keys()].sort((a, b) => a - b)) {
    for (const event of pages.get(page).search_data?.events?.results || []) {
      const isUtah = (event.locations || []).some(location => location.type === 'region' && location.name === 'Utah');
      if (!event.is_online_event && isUtah) found.set(event.eventbrite_event_id, compact(event));
    }
  }

  const all = [...found.values()];
  const alreadyRepresented = all.filter(e => knownEventbriteIds.has(e.eventbriteId) || knownUrls.has(e.url.replace(/\/$/, '')) || knownNames.has(normalizeName(e.name)));
  const newToSite = all.filter(e => !knownEventbriteIds.has(e.eventbriteId) && !knownUrls.has(e.url.replace(/\/$/, '')) && !knownNames.has(normalizeName(e.name)));
  const reviewQueue = newToSite.filter(e => e.score >= 5).sort((a, b) => b.score - a.score || a.startDate.localeCompare(b.startDate) || a.name.localeCompare(b.name));
  const output = {
    checkedOn,
    range: { from, to },
    source: base,
    scope: `${pageCount} statewide Eventbrite result pages; public in-person Utah events only`,
    counts: {
      rawStatewideUnique: all.length,
      alreadyRepresentedByIdUrlOrExactName: alreadyRepresented.length,
      newToSite: newToSite.length,
      editorialReviewQueue: reviewQueue.length,
    },
    methodology: {
      discovery: 'Crawled Eventbrite public statewide search results and retained structured event, venue, schedule, tag and image metadata.',
      ranking: 'Holiday and seasonal relevance, public experience, cultural/community value, performance, family/adult fit and Salt Lake proximity raise review priority; online, business and professional-training listings are suppressed.',
      publicationRule: 'Discovery score never confirms an event. Each selected listing must be opened and verified for current schedule, full ticket price, age limit, accessibility, organizer language and image suitability before publication.',
    },
    reviewQueue,
    allNewEventbriteListings: newToSite.sort((a, b) => a.startDate.localeCompare(b.startDate) || a.name.localeCompare(b.name)),
  };
  const outPath = path.join(root, 'research', `eventbrite-crawl-${checkedOn}.json`);
  fs.writeFileSync(outPath, JSON.stringify(output, null, 2) + '\n');
  console.log(JSON.stringify({ outPath, ...output.counts, pages: pageCount }, null, 2));
})().catch(error => { console.error(error); process.exit(1); });
