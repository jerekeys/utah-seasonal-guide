const assert=require('assert');
const fs=require('fs');
const vm=require('vm');
const CAMPAIGN=require('../assets/social-campaign.js');
const EDITORIAL=require('../assets/social-editorial.js');

const context={window:{}};
vm.createContext(context);
vm.runInContext(fs.readFileSync('assets/data.js','utf8'),context);
const events=context.window.SITE_DATA.events;
const anchor='2026-10-07';

function checkCampaign(series){
  const campaign=CAMPAIGN.generate(events,{series,anchor,count:6,editorial:EDITORIAL});
  assert(campaign.events.length>=4,`${series}: too few events`);
  assert.strictEqual(new Set(campaign.events.map(event=>event.id)).size,campaign.events.length,`${series}: duplicate events`);
  assert(campaign.events.every(event=>!event.isWatch),`${series}: watchlist event selected`);
  for(const event of campaign.events){
    assert(campaign.caption.includes(event['Event / attraction']),`${series}: event missing from caption`);
    assert(campaign.caption.includes(event.Website),`${series}: source link missing from caption`);
    assert(campaign.altText.includes(event['Event / attraction']),`${series}: event missing from alt text`);
  }
  assert(campaign.caption.includes('Plan your visit:'),`${series}: caption lacks planning links`);
  return campaign;
}

const automatic=checkCampaign('auto');
assert.strictEqual(automatic.series,'found','Wednesday auto mode should choose the discovery-led Found It brief');
assert(automatic.seriesDescription,'Automatic campaigns should explain the chosen editorial brief');

const weekend=checkCampaign('weekend');
const [weekendStart,weekendEnd]=CAMPAIGN.weekendRange(anchor);
assert(weekend.events.every(event=>CAMPAIGN.datesFor(event).some(date=>date>=weekendStart&&date<=weekendEnd)),'Weekend campaign included an event outside the weekend');
assert(weekend.events.filter(event=>event.publicRegion==='Salt Lake Metro').length>=4,'Weekend campaign should contain at least four Salt Lake Metro events');
const editorialWeekend=CAMPAIGN.generate(events,{series:'weekend',anchor:'2026-10-08',count:6,editorial:EDITORIAL});
assert.strictEqual(editorialWeekend.events[0].id,'ogden-d-a-de-los-muertos','Explicit editorial lead should outrank the mathematical score');
assert(/regional exception/i.test(editorialWeekend.selectionNotes[editorialWeekend.events[0].id]),'Editorial rationale should be retained');

const free=checkCampaign('free');
assert(free.events.every(event=>event.isFree),'Free campaign included a paid event');

const late=checkCampaign('lastchance');
assert(late.events.some(event=>event.endDate),'Last Chance campaign lacks an ending event');

const field=checkCampaign('field');
const nearby=field.events.filter(event=>event.publicRegion==='Salt Lake Metro');
assert(nearby.length>=Math.ceil(field.events.length*.66),'Ordinary campaigns should be dominated by Salt Lake Metro events');
const fieldWeekendEnd=CAMPAIGN.weekendRange(anchor)[1];
assert(field.events.filter(event=>CAMPAIGN.nextDate(event,anchor)>fieldWeekendEnd).length>=Math.ceil(field.events.length*.83),'Field Guide should primarily look beyond the immediate weekend');

const drive=checkCampaign('drive');
assert(drive.events.reduce((sum,event)=>sum+CAMPAIGN.proximityLevel(event),0)/drive.events.length<field.events.reduce((sum,event)=>sum+CAMPAIGN.proximityLevel(event),0)/field.events.length,'Worth the Drive should favor events farther from Salt Lake City');

const adults=checkCampaign('adults');
assert(adults.events.every(event=>CAMPAIGN.adultProfile(event).focused),'Adults Focused included an event without an adult-oriented signal');
assert(adults.events.filter(event=>{const profile=CAMPAIGN.adultProfile(event);return profile.age21||profile.nightlife}).length>=Math.ceil(adults.events.length/2),'Adults Focused should be dominated by 21+ or nightlife events');

const kids=CAMPAIGN.generate(events,{series:'kids',anchor:'2026-10-08',count:6,editorial:EDITORIAL});
assert(kids.events.length>=4,'Kids campaign should contain at least four events');
assert(kids.events.every(event=>CAMPAIGN.kidProfile(event).focused),'Events for Kids included an event without child-specific programming');
assert(kids.events.every(event=>!CAMPAIGN.adultProfile(event).age18&&!CAMPAIGN.adultProfile(event).age21),'Events for Kids included an adult-restricted event');
assert.strictEqual(kids.events[0].id,'little-haunts-this-is-the-place','Kids editorial lead should appear first');

const pets=CAMPAIGN.generate(events,{series:'pets',anchor:'2026-10-08',count:6,editorial:EDITORIAL});
assert(pets.events.length>=4,'Pet-friendly campaign should produce a usable short list');
assert(pets.events.every(event=>CAMPAIGN.petFriendly(event)),'Pet-friendly campaign included an event without explicit pet permission or a dedicated pet activity');
assert(pets.caption.includes('Pet policy: Pets are welcome'),'Pet-friendly campaign caption should explain that policy details are event-specific');
assert(pets.title.includes('pet-friendly'),'Pet-friendly campaign title should identify the series');
assert(pets.events.every((event,index)=>index===0||CAMPAIGN.nextDate(pets.events[index-1],pets.anchor)<=CAMPAIGN.nextDate(event,pets.anchor)),'Pet-friendly campaign should be chronological');
assert(pets.events.filter(event=>event.publicRegion==='Salt Lake Metro').length>=Math.ceil(pets.events.length*.5),'Pet-friendly campaign should keep a local majority when the verified candidate pool allows');
assert(pets.candidates.slice(0,2).every(event=>event.publicRegion==='Salt Lake Metro'),'Pet-friendly scoring should rank Salt Lake Metro listings ahead of regional listings');

const found=checkCampaign('found');
assert(found.events.every(event=>{const profile=CAMPAIGN.adultProfile(event);return !profile.age18&&!profile.age21}),'Found It should not duplicate age-restricted adult programming');

const repeated=CAMPAIGN.generate(events,{series:'field',anchor,count:6,editorial:EDITORIAL,recentIds:field.events.map(event=>event.id)});
assert(repeated.events.filter(event=>field.events.some(first=>first.id===event.id)).length<field.events.length,'Recent-post history should rotate at least one event');

console.log('Social campaigns pass editorial, personality, timing, Salt Lake focus, adult/kid eligibility, rotation, caption and accessibility checks');
