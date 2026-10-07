const fs=require('fs'),vm=require('vm'),assert=require('assert');const ctx={window:{},Intl,Date};vm.createContext(ctx);for(const p of ['assets/data.js','assets/date-tools.js'])vm.runInContext(fs.readFileSync(p,'utf8'),ctx);const d=ctx.window.SITE_DATA,t=ctx.window.DATE_TOOLS,ids=new Set;for(const e of d.events){assert(!ids.has(e.id),'Duplicate '+e.id);ids.add(e.id);assert(fs.existsSync('events/'+e.id+'/index.html'));assert(fs.existsSync(e.placeholder));if(e.photo?.src)assert(fs.existsSync(e.photo.src));if(e.isWatch)assert(!e.occurrenceDates.length,'Watch calendar '+e.id);for(const day of e.occurrenceDates||[])assert(/^202[67]-\d\d-\d\d$/.test(day),day)}assert.equal(t.today(new Date('2026-10-07T01:00:00Z')),'2026-10-06');assert.equal(t.parseTime('8 PM–midnight').end,1440);assert.equal(t.parseTime('9 PM–2 AM').end,1560);assert.equal(t.hoursForDate({Times:'Mon–Fri 5–9 PM'},'2026-10-10'),null);assert.equal(t.matchesWhen({Times:'Hours to be announced',occurrenceDates:['2026-10-06']},'tonight',new Date('2026-10-06T20:00Z')),false);assert.equal(t.matchesWhen({Times:'9 PM–2 AM',occurrenceDates:['2026-10-05','2026-10-06']},'open-now',new Date('2026-10-06T07:00Z')),true);console.log('Validated '+ids.size+' event records, asset paths, Utah dates, weekday rules and overnight filtering');

ctx.document={readyState:"loading",addEventListener(){}};ctx.TextEncoder=TextEncoder;vm.runInContext(fs.readFileSync("assets/event-enhancements.js","utf8"),ctx);const cal=ctx.window.CALENDAR_TOOLS;assert.equal(cal.utc("2026-10-10",19*60),"20261011T010000Z");assert.equal(cal.utc("2026-12-03",11*60),"20261203T180000Z");assert.equal(cal.utc("2026-10-31",26*60),"20261101T090000Z");const ice=cal.ics({id:"sample",Times:"11 AM–8 PM","Event / attraction":"A, B; C",Location:"Utah",Website:"https://example.com", "Why / thoughts":"Example"},"2026-12-03");assert(ice.includes("SUMMARY:A\\, B\\; C"));assert(ice.includes("DTEND:20261204T030000Z"));assert(cal.times({Times:"Not announced"},"2026-12-03").allDay);console.log("Calendar UTC, DST transition, escaping and save-the-date checks passed");

// End-result checks run across the entire published list, including migration edge cases.
for(const e of d.events){if(e.startDate)assert(/^\d{4}-\d{2}-\d{2}$/.test(e.startDate),e.id+" start");if(e.endDate)assert(/^\d{4}-\d{2}-\d{2}$/.test(e.endDate),e.id+" end");assert(e.flags.includes("Free admission")===!!e.isFree,e.id+" free flag");if(/d[ií]a.*muertos|day of the dead/i.test(e['Event / attraction'])){assert(e.holidays.includes('Día de los Muertos'),e.id+" holiday");assert(!/scare/i.test(e.rating?.type||''),e.id+" cultural scare rating")}if(e.scheduleConfidence==='date-conflict')assert(!e.occurrenceDates.length,e.id+" uncertain calendar");}
const choir=d.events.find(e=>e.id==='salt-lake-men-s-choir-somewhere-in-my-memory');assert.equal(choir.occurrenceDates.length,3);assert.equal(t.startForDate(choir,'2026-12-13'),960);assert(t.matchesWhen(choir,'tonight',new Date('2026-12-11T20:00Z')));assert(!t.matchesWhen(choir,'tonight',new Date('2026-12-13T20:00Z')));assert.equal(cal.times(choir,'2026-12-11').start,'20261212T023000Z');assert(cal.times(choir,'2026-12-11').reminder);console.log('Whole-list holiday, cost, date endpoints and published performance-start checks passed');

// Ordering and archive behavior are separate from date filtering.
const fixture=(id,name,dates,notable=false)=>({id,'Event / attraction':name,occurrenceDates:dates,endDate:dates.at(-1),notable_event:notable,Times:'Hours forthcoming'});
const recurring=fixture('a','A recurring',['2026-10-10','2026-10-11']);
const single=fixture('z','Z single',['2026-10-10']);
const notable=fixture('n','N notable',['2027-09-10','2027-09-11'],true);
assert(t.compareEvents(notable,single,'recommended','2026-10-06')>0);assert(t.compareEvents({...notable,occurrenceDates:['2026-10-25'],endDate:'2026-10-25'},single,'recommended','2026-10-06')<0);assert(t.isCurrentNotable({...notable,occurrenceDates:['2026-11-20'],endDate:'2026-11-20'},'2026-10-06'));assert(!t.isCurrentNotable({...notable,occurrenceDates:['2026-11-21'],endDate:'2026-11-21'},'2026-10-06')); assert(t.compareEvents(single,recurring)<0);
assert(t.compareEvents(single,recurring,'name')>0);assert(t.compareEvents(recurring,notable,'date','2026-10-06')<0);
assert(t.isPast(fixture('past','Past',['2026-09-19']),'2026-10-06'));
assert(!t.isPast(recurring,'2026-10-06'));assert(!t.isPast({isWatch:true,occurrenceDates:['2025-09-19']},'2026-10-06'));
assert(!t.isPast({occurrenceDates:['2026-09-19'],endDate:'2026-10-31'},'2026-10-06'));
assert(!t.isPast({occurrenceDates:[]},'2026-10-06'));
assert(t.matchesWhen(fixture('past','Past',['2026-09-19']),'2026-09-19'));
for(const e of d.events){assert(typeof e.notable_event==='boolean',e.id+' notable flag');assert(d.regions.includes(e.publicRegion),e.id+' public region');assert(!/gap|bundle filler|fresh.*addition|taxonomy|primary.*capture|producer sweep|child event|separately.*filtering|known by name.*j209|this captures|original.list omission/i.test(e['Why / thoughts']),e.id+' internal copy');}
console.log('Notable ordering, explicit sorts, historical filters and public editorial checks passed');

assert(!t.isPast({id:'overnight',Times:'9 PM–2 AM',occurrenceDates:['2026-10-05'],endDate:'2026-10-05'},'2026-10-06',new Date('2026-10-06T07:00Z')));
assert(t.isPast({id:'overnight',Times:'9 PM–2 AM',occurrenceDates:['2026-10-05'],endDate:'2026-10-05'},'2026-10-06',new Date('2026-10-06T09:00Z')));
console.log('Final-night rollover remains visible until closing');

vm.runInContext(fs.readFileSync('assets/vibes.js','utf8'),ctx);const vs=ctx.window.VIBE_GUIDES;assert.equal(vs.length,27);assert.equal(new Set(vs.map(v=>v.id)).size,27);for(const v of vs){assert(v.description.length>40);assert(d.events.some(e=>ctx.window.matchesVibe(e,v)),v.id+' empty collection');}const dogs=vs.find(v=>v.id==='dogs');assert(ctx.window.matchesVibe(d.events.find(e=>e.id==='hounds-haunts'),dogs));assert(!ctx.window.matchesVibe(d.events.find(e=>e.id==='frightmares-at-lagoon'),dogs));console.log('Explained vibe collections and dog membership passed');

assert(t.isUpcomingSoon(single,'2026-10-06'));assert(!t.isUpcomingSoon(notable,'2026-10-06'));console.log('Notable priority respects the next 45 days');

// Every ordering tier remains chronological, even when a notable is also single-day.
const ns=fixture('ns','Z notable single',['2026-10-20'],true),nm=fixture('nm','A notable multi',['2026-10-15','2026-10-16'],true);
assert(t.compareEvents(nm,ns,'recommended','2026-10-06')<0);
assert(t.compareEvents(fixture('early','Z early',['2026-10-09']),fixture('late','A late',['2026-10-10']),'recommended','2026-10-06')<0);
assert(!t.isSingleDay({...single,recurrence:'weekly'}));assert(t.isSingleDay({...single,recurrence:'annual'}));
assert(t.compareEvents({...recurring,startDate:'2026-09-01'},fixture('later','A later',['2026-10-01','2026-10-02']),'date','2026-10-06')<0);
const seasonFor=day=>({12:'Winter',1:'Winter',2:'Winter',3:'Spring',4:'Spring',5:'Spring',6:'Summer',7:'Summer',8:'Summer',9:'Fall',10:'Fall',11:'Fall'})[+day.slice(5,7)];
for(const e of d.events){if(e.isWatch)continue;for(const day of t.parseSchedule(e).dates)assert(e.holidays.includes(seasonFor(day)),e.id+' missing '+seasonFor(day));}
assert(d.events.find(e=>e.id==='labor-day-luau-at-thanksgiving-point-2026').holidays.includes('Labor Day'));
assert(!fs.readFileSync('assets/site.js','utf8').includes('rows.length?`<ul>'));
assert(fs.readFileSync('assets/site.js','utf8').includes('📷:'));
console.log('Chronological tiers, recurrence, additive seasons, archive backfill and image-credit checks passed');

assert(d.events.filter(e=>e.photo).length>=Math.ceil(d.events.length/2),'At least half of listings have reviewed photos');
console.log('Photo coverage meets the requested halfway threshold');
