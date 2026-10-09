(()=>{
const MONTHS={jan:0,january:0,feb:1,february:1,mar:2,march:2,apr:3,april:3,may:4,jun:5,june:5,jul:6,july:6,aug:7,august:7,sep:8,sept:8,september:8,oct:9,october:9,nov:10,november:10,dec:11,december:11};
const DAYS={sun:0,sunday:0,mon:1,monday:1,tue:2,tues:2,tuesday:2,wed:3,wednesday:3,thu:4,thur:4,thurs:4,thursday:4,fri:5,friday:5,sat:6,saturday:6};
const pad=n=>String(n).padStart(2,'0');
const iso=d=>`${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
const localDate=s=>{const m=String(s||'').match(/^(\d{4})-(\d{2})-(\d{2})$/);return m?new Date(+m[1],+m[2]-1,+m[3]):null};
const add=(d,n)=>new Date(d.getFullYear(),d.getMonth(),d.getDate()+n);
function monthNum(s){return MONTHS[String(s||'').toLowerCase().replace('.','')]}
function dateFromParts(mon,day){const m=monthNum(mon);return Number.isInteger(m)?new Date(2026,m,+day):null}
function datesBetween(a,b,allowedDays=null){const out=[];for(let d=new Date(a);d<=b;d=add(d,1)){if(!allowedDays||allowedDays.has(d.getDay()))out.push(iso(d))}return out}
function weekdaySet(text){const found=new Set();Object.entries(DAYS).forEach(([name,n])=>{if(new RegExp(`\\b${name}s?\\b`,'i').test(text))found.add(n)});return found}
function parseSchedule(event){
  if(Array.isArray(event.occurrenceDates)&&event.occurrenceDates.length)return {dates:[...new Set(event.occurrenceDates)].sort(),confidence:'curated'};
  const schedule=String(event['2026 schedule']||'').replace(/[–—]/g,'-');
  const first=String(event['First date']||'');
  const dates=new Set(); let confidence='inferred';
  if(/^20\d{2}-\d{2}-\d{2}$/.test(first))dates.add(first); else {const m=first.match(/\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+(\d{1,2})\b/i);if(m){const d=dateFromParts(m[1],m[2]);if(d)dates.add(iso(d))}}
  const weekdays=weekdaySet(schedule);
  // Month-contained recurrence, e.g. Fridays & Saturdays in October.
  const inMonth=schedule.match(/\bin\s+(January|February|March|April|May|June|July|August|September|October|November|December)\b/i);
  if(inMonth&&weekdays.size){const mn=monthNum(inMonth[1]);const a=new Date(2026,mn,1),b=new Date(2026,mn+1,0);datesBetween(a,b,weekdays).forEach(x=>dates.add(x));}
  // Explicit ranges, e.g. Oct 2-30 or Sep 18-Nov 14.
  const rangeRe=/(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+(\d{1,2})\s*-\s*(?:(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+)?(\d{1,2})/ig;
  let r; while((r=rangeRe.exec(schedule))){const a=dateFromParts(r[1],r[2]),b=dateFromParts(r[3]||r[1],r[4]);if(!a||!b)continue;const span=Math.round((b-a)/86400000);const selective=/select dates|various dates|multiple dates|see (?:site|calendar)|schedule varies/i.test(schedule);if(weekdays.size){datesBetween(a,b,weekdays).forEach(x=>dates.add(x));}else if(span<=4||/daily|every day|nightly|throughout|open daily/i.test(schedule)){datesBetween(a,b).forEach(x=>dates.add(x));}else if(!selective){confidence='partial';}}
  // Explicit month/day mentions not already covered.
  const singleRe=/(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+(\d{1,2})(?!\s*-)/ig;
  let s;while((s=singleRe.exec(schedule))){const d=dateFromParts(s[1],s[2]);if(d)dates.add(iso(d))}
  return {dates:[...dates].sort(),confidence};
}
function parseTime(text){
 const t=String(text||'').replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();
 const m=t.match(/\b(\d{1,2})(?::(\d{2}))?\s*(AM|PM)?\s*-\s*(\d{1,2})(?::(\d{2}))?\s*(AM|PM|midnight|noon)\b/i);if(!m)return null;
 function mins(h,mi,ap){h=+h;mi=+(mi||0);ap=String(ap||'').toLowerCase();if(ap==='midnight')return 1440;if(ap==='noon')return 720;if(ap==='pm'&&h!==12)h+=12;if(ap==='am'&&h===12)h=0;return h*60+mi}
 let ap1=m[3],ap2=m[6];if(!ap1&&/am|pm/i.test(ap2))ap1=ap2;let start=mins(m[1],m[2],ap1),end=mins(m[4],m[5],ap2);if(end<start)end+=1440;return {start,end,label:m[0]};
}
function enrich(e){const sched=parseSchedule(e),time=parseTime(e.Times);e._dateMeta={...sched,time};return e}
function selectedWindow(value){const now=new Date();let a,b,label='';if(!value)return null;if(value==='today'||value==='tonight'){a=new Date(now.getFullYear(),now.getMonth(),now.getDate());b=a;label=value==='tonight'?'Tonight':'Today'}else if(value==='tomorrow'){a=add(new Date(now.getFullYear(),now.getMonth(),now.getDate()),1);b=a;label='Tomorrow'}else if(value==='weekend'||value==='next-weekend'){const base=new Date(now.getFullYear(),now.getMonth(),now.getDate());const wd=base.getDay();let toFri=wd<=5?5-wd:6; if(wd===0)toFri=-2; if(value==='next-weekend')toFri+=7;a=add(base,toFri);b=add(a,2);label=value==='weekend'?'This weekend':'Next weekend'}else if(/^\d{4}-\d{2}-\d{2}$/.test(value)){a=localDate(value);b=a;label=a.toLocaleDateString(undefined,{weekday:'short',month:'short',day:'numeric'})}else return null;return {start:iso(a),end:iso(b),label}}
function overlaps(e,w){if(!w)return true;const ds=e._dateMeta?.dates||[];return ds.some(d=>d>=w.start&&d<=w.end)}
function applyDateParam(){if(!window.SITE_DATA?.events)return;window.SITE_DATA.events.forEach(enrich);const p=new URLSearchParams(location.search),v=p.get('when');const w=selectedWindow(v);if(w){window.SITE_DATA.events=window.SITE_DATA.events.filter(e=>overlaps(e,w));window.SITE_DATA._dateFilter=w;}}
function updateWhen(v){const u=new URL(location.href);if(v)u.searchParams.set('when',v);else u.searchParams.delete('when');location.href=u.toString()}
function injectControls(){const controls=document.querySelector('.controls');if(!controls)return;const current=new URLSearchParams(location.search).get('when')||'';const row=document.createElement('div');row.className='date-filter-row';row.innerHTML=`<span class="date-filter-label">When</span><button type="button" data-when="today">Today</button><button type="button" data-when="tonight">Tonight</button><button type="button" data-when="tomorrow">Tomorrow</button><button type="button" data-when="weekend">This weekend</button><button type="button" data-when="next-weekend">Next weekend</button><label class="date-picker-label">Pick a date <input type="date" id="datePick" min="2026-09-01" max="2027-10-31"></label><button type="button" data-when="" class="date-clear">Any date</button>`;controls.prepend(row);row.querySelectorAll('[data-when]').forEach(b=>{b.classList.toggle('active',b.dataset.when===current);b.addEventListener('click',()=>updateWhen(b.dataset.when))});const picker=row.querySelector('#datePick');if(/^\d{4}-\d{2}-\d{2}$/.test(current))picker.value=current;picker.addEventListener('change',()=>picker.value&&updateWhen(picker.value));const summary=document.querySelector('#filterSummary');if(summary&&window.SITE_DATA._dateFilter){summary.textContent+=` · ${window.SITE_DATA._dateFilter.label}`}}
window.DATE_TOOLS={parseSchedule,parseTime,enrich,selectedWindow,iso};
applyDateParam();
window.addEventListener('DOMContentLoaded',injectControls);
})();
