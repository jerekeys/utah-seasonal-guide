(()=>{
const events=window.SITE_DATA?.events||[];const byId=new Map(events.map(e=>[e.id,e]));
const iso=d=>`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
const date=s=>{const [y,m,d]=s.split('-').map(Number);return new Date(y,m-1,d)};
const range=(start,end,days=null)=>{const out=[];for(let d=date(start),last=date(end);d<=last;d.setDate(d.getDate()+1)){if(!days||days.includes(d.getDay()))out.push(iso(d))}return out};
const hours=(dates,fn)=>Object.fromEntries(dates.map(d=>[d,fn(d)]).filter(([,v])=>v));
function apply(id,cfg){const e=byId.get(id);if(!e)return;Object.assign(e,cfg,{scheduleVerifiedOn:'2026-10-06'})}

// Lagoon Frightmares — official Lagoon 2026 Frightmares + park-hours calendars.
{
 const dates=[...range('2026-09-11','2026-11-08',[5,6,0]),'2026-10-15'].sort();
 const hoursByDate=hours(dates,d=>{const wd=date(d).getDay();if(d==='2026-10-15'||d==='2026-10-16'||d==='2026-10-17')return '10 AM-11 PM';if(d==='2026-10-31')return '10 AM-5 PM';if(wd===5)return '5 PM-11 PM';if(wd===6)return '10 AM-11 PM';if(wd===0)return '10 AM-8 PM';return null});
 apply('frightmares-at-lagoon',{occurrenceDates:dates,hoursByDate,Times:'Fri 5-11 PM; Sat 10 AM-11 PM; Sun 10 AM-8 PM, with select special hours',scheduleSource:'https://www.lagoonpark.com/park-info/schedule-hours/'});
}

// Hogle Halloween — Thursdays-Sundays Sept 24-Oct 18; nightly Oct 22-30.
{
 const dates=[...range('2026-09-24','2026-10-18',[4,5,6,0]),...range('2026-10-22','2026-10-30')];
 apply('hogle-halloween-a-boo-lights-experience',{occurrenceDates:[...new Set(dates)].sort(),hoursByDate:hours(dates,()=> '6:30 PM-9:30 PM'),Times:'6:30-9:30 PM',scheduleSource:'https://www.hoglezoo.org/hogle-halloween/'});
}

// Gardner Village WitchFest — official published village hours, closed Sundays.
{
 const dates=range('2026-09-18','2026-10-31',[1,2,3,4,5,6]);
 const hoursByDate=hours(dates,d=>{const dt=date(d),wd=dt.getDay(),month=dt.getMonth();if(d==='2026-10-31')return '10 AM-4 PM';if(month===8)return wd>=1&&wd<=4?'10 AM-6 PM':'10 AM-8 PM';return wd>=1&&wd<=5?'10 AM-8 PM':'10 AM-9 PM'});
 apply('gardner-village-witchfest',{occurrenceDates:dates,hoursByDate,Times:'Sep: Mon-Thu 10 AM-6 PM, Fri-Sat 10 AM-8 PM; Oct: Mon-Fri 10 AM-8 PM, Sat 10 AM-9 PM; Halloween 10 AM-4 PM',scheduleSource:'https://www.gardnervillage.com/witch-fest'});
}

// Sundance Halloween Lift Rides — exact official dates and hours.
{
 const dates=['2026-10-15','2026-10-16','2026-10-17','2026-10-19','2026-10-22','2026-10-23','2026-10-24','2026-10-26','2026-10-27','2026-10-28','2026-10-29','2026-10-30','2026-10-31'];
 apply('halloween-lift-rides-sundance',{occurrenceDates:dates,hoursByDate:hours(dates,()=> '7 PM-10 PM'),Times:'7-10 PM',scheduleSource:'https://www.sundanceresort.com/events/halloween-lift-rides/'});
}

// Get Freaky — exact 2026 festival dates and published operating hours.
{
 const dates=['2026-10-23','2026-10-24','2026-10-25'];
 apply('get-freaky-neon-nightmare',{occurrenceDates:dates,hoursByDate:{'2026-10-23':'7 PM-2 AM','2026-10-24':'7 PM-2 AM','2026-10-25':'6 PM-1 AM'},Times:'Fri-Sat 7 PM-2 AM; Sun 6 PM-1 AM',scheduleSource:'https://getfreakyslc.com/info-faq/'});
}

// Asylum 49 — official event calendar entries, including date-specific closing times.
{
 const dates=['2026-09-18','2026-09-19','2026-09-25','2026-09-26','2026-10-01','2026-10-02','2026-10-03','2026-10-06','2026-10-07','2026-10-08','2026-10-09','2026-10-10','2026-10-13','2026-10-14','2026-10-15','2026-10-16','2026-10-17','2026-10-20','2026-10-21','2026-10-22','2026-10-23','2026-10-24','2026-10-30','2026-10-31','2026-11-06','2026-11-07','2026-11-13','2026-11-14'];
 const hoursByDate=hours(dates,d=>{if(d.startsWith('2026-09')||d.startsWith('2026-11'))return '7 PM-11 PM';const wd=date(d).getDay();return wd===5||wd===6?'7 PM-11:59 PM':'7 PM-10 PM'});
 apply('asylum-49',{occurrenceDates:dates,hoursByDate,Times:'Most Tue-Thu 7-10 PM; Fri-Sat 7 PM-midnight; select Sep/Nov nights 7-11 PM',scheduleSource:'https://www.asylum49.com/events'});
}

// Red Butte Garden After Dark — daily Oct 15-30, hours vary by weekday/weekend.
{
 const dates=range('2026-10-15','2026-10-30');
 const hoursByDate=hours(dates,d=>{const wd=date(d).getDay();return wd>=1&&wd<=4?'6 PM-8 PM':'6 PM-9 PM'});
 apply('garden-after-dark-adventures-in-neverland',{occurrenceDates:dates,hoursByDate,Times:'Mon-Thu 6-8 PM; Fri-Sun 6-9 PM',scheduleSource:'https://redbuttegarden.org/events/garden-after-dark/garden-after-dark-faq/'});
}

// Cornbelly's Lehi — official ticket structure identifies Mon-Thu weekday and Fri-Sat weekend admission.
{
 const dates=range('2026-09-21','2026-10-31',[1,2,3,4,5,6]);
 apply('cornbelly-s-corn-maze-pumpkin-fest-lehi',{occurrenceDates:dates,scheduleSource:'https://cornbellys.com/pages/calendar'});
}
})();
