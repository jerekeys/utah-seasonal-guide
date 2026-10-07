const assert=require('assert');
const fs=require('fs');
const vm=require('vm');
const CAMPAIGN=require('../assets/social-campaign.js');

const context={window:{}};
vm.createContext(context);
vm.runInContext(fs.readFileSync('assets/data.js','utf8'),context);
const events=context.window.SITE_DATA.events;
const anchor='2026-10-07';

function checkCampaign(series){
  const campaign=CAMPAIGN.generate(events,{series,anchor,count:6});
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
assert.strictEqual(automatic.series,'topical','Auto mode should identify the strong current holiday story');
assert(automatic.topic,'Topical campaign should name its topic');

const weekend=checkCampaign('weekend');
const [weekendStart,weekendEnd]=CAMPAIGN.weekendRange(anchor);
assert(weekend.events.every(event=>CAMPAIGN.datesFor(event).some(date=>date>=weekendStart&&date<=weekendEnd)),'Weekend campaign included an event outside the weekend');

const free=checkCampaign('free');
assert(free.events.every(event=>event.isFree),'Free campaign included a paid event');

const late=checkCampaign('lastchance');
assert(late.events.some(event=>event.endDate),'Last Chance campaign lacks an ending event');

console.log('Social campaigns pass timing, eligibility, diversity, caption and accessibility checks');
