(()=>{
const MONTHS={jan:0,january:0,feb:1,february:1,mar:2,march:2,apr:3,april:3,may:4,jun:5,june:5,jul:6,july:6,aug:7,august:7,sep:8,sept:8,september:8,oct:9,october:9,nov:10,november:10,dec:11,december:11};
const DAY_NAMES={sun:0,sunday:0,mon:1,monday:1,tue:2,tues:2,tuesday:2,wed:3,wednesday:3,thu:4,thur:4,thurs:4,thursday:4,fri:5,friday:5,sat:6,saturday:6};
const pad=n=>String(n).padStart(2,'0');
const iso=d=>`${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
const localDate=s=>{const m=String(s||'').match(/^(\d{4})-(\d{2})-(\d{2})$/);return m?new Date(+m[1],+m[2]-1,+m[3]):null};
const add=(d,n)=>new Date(d.getFullYear(),d.getMonth(),d.getDate()+n);
const monthNum=s=>MONTHS[String(s||'').toLowerCase().replace('.','')];
const dateFromParts=(mon,day)=>{const m=monthNum(mon);return Number.isInteger(m)?new Date(2026,m,+day):null};
function datesBetween(a,b,allowedDays=null){const out=[];for(let d=new Date(a);d<=b;d=add(d,1)){if(!allowedDays||allowedDays.has(d.getDay()))out.push(iso(d))}return out}
function weekdaySet(text){
 const found=new Set();const src=String(text||'');
 Object.entries(DAY_NAMES).forEach(([name,n])=>{if(new RegExp(`\\b${name}s?\\b`,'i').test(src))found.add(n)});
 const range=/\b(sun(?:day)?|mon(?:day)?|tue(?:s|sday)?|wed(?:nesday)?|thu(?:r|rs|rsday)?|fri(?:day)?|sat(?:urday)?)\s*-\s*(sun(?:day)?|mon(?:day)?|tue(?:s|sday)?|wed(?:nesday)?|thu(?:r|rs|rsday)?|fri(?:day)?|sat(?:urday)?)\b/ig;let m;
 while((m=range.exec(src))){const a=DAY_NAMES[m[1].toLowerCase()],b=DAY_NAMES[m[2].toLowerCase()];if(a==null||b==null)continue;for(let d=a;;d=(d+1)%7){found.add(d);if(d===b)break}}
 return found;
}
function addMonthDayLists(schedule,dates){
 const re=/(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+((?:\d{1,2}(?:st|nd|rd|th)?(?:\s*(?:,|&|and)\s*|\s+)){1,8}\d{1,2}(?:st|nd|rd|th)?)/ig;let m;
 while((m=re.exec(schedule))){for(const n of m[2].match(/\d{1,2}/g)||[]){const d=dateFromParts(m[1],n);if(d)dates.add(iso(d))}}
}
function parseSchedule(event){
 if(Array.isArray(event.occurrenceDates)&&event.occurrenceDates.length)return {dates:[...new Set(event.occurrenceDates)].sort(),confidence:'curated',source:'occurrenceDates'};
 const schedule=String(event['2026 schedule']||'').replace(/[–—]/g,'-');const first=String(event['First date']||'');const dates=new Set();let confidence='inferred';
 if(/^2026-\d{2}-\d{2}$/.test(first))dates.add(first);else{const m=first.match(/\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+(\d{1,2})\b/i);if(m){const d=dateFromParts(m[1],m[2]);if(d)dates.add(iso(d))}}
 const weekdays=weekdaySet(schedule);addMonthDayLists(schedule,dates);
 const inMonth=schedule.match(/\bin\s+(January|February|March|April|May|June|July|August|September|October|November|December)\b/i);if(inMonth&&weekdays.size){const mn=monthNum(inMonth[1]);datesBetween(new Date(2026,mn,1),new Date(2026,mn+1,0),weekdays).forEach(x=>dates.add(x))}
 const rangeRe=/(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+(\d{1,2})\s*-\s*(?:(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+)?(\d{1,2})/ig;let r;
 while((r=rangeRe.exec(schedule))){const a=dateFromParts(r[1],r[2]),b=dateFromParts(r[3]||r[1],r[4]);if(!a||!b||b<a)continue;const span=Math.round((b-a)/86400000);const selective=/select dates|various dates|multiple dates|see (?:site|calendar)|schedule varies/i.test(schedule);if(weekdays.size)datesBetween(a,b,weekdays).forEach(x=>dates.add(x));else if(span<=4||/daily|every day|nightly|open daily|daily through|runs daily|each day/i.test(schedule))datesBetween(a,b).forEach(x=>dates.add(x));else if(!selective)confidence='partial'}
 const through=schedule.match(/\bthrough\s+(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+(\d{1,2})\b/i);if(through&&dates.size&&/daily|every day|nightly|open daily/i.test(schedule)){const a=localDate([...dates].sort()[0]),b=dateFromParts(through[1],through[2]);if(a&&b&&b>=a)datesBetween(a,b).forEach(x=>dates.add(x))}
 const singleRe=/(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+(\d{1,2})(?!\s*-)/ig;let s;while((s=singleRe.exec(schedule))){const d=dateFromParts(s[1],s[2]);if(d)dates.add(iso(d))}
 if(/select dates|various dates|multiple dates|see (?:site|calendar)|schedule varies/i.test(schedule)&&dates.size<2)confidence='partial';
 return {dates:[...dates].sort(),confidence,source:'parsed'};
}
function clockMinutes(token,ampmHint=''){token=String(token||'').trim().toLowerCase();if(token==='midnight')return 1440;if(token==='noon')return 720;const m=token.match(/^(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$/i);if(!m)return null;let h=+m[1],mi=+(m[2]||0),ap=(m[3]||ampmHint||'').toLowerCase();if(ap==='pm'&&h!==12)h+=12;if(ap==='am'&&h===12)h=0;return h*60+mi}
function parseTimeRange(text){const src=String(text||'').replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();const m=src.match(/\b(midnight|noon|\d{1,2}(?::\d{2})?\s*(?:AM|PM)?)\s*-\s*(midnight|noon|\d{1,2}(?::\d{2})?\s*(?:AM|PM)?)/i);if(!m)return null;const endAP=((m[2].match(/(am|pm)/i)||[])[1]||'').toLowerCase();let start=clockMinutes(m[1],endAP),end=clockMinutes(m[2]);if(start==null||end==null)return null;if(end<=start)end+=1440;return {start,end,label:m[0]}}
function parseHours(text){
 const src=String(text||'').trim();if(!src)return {rules:[],confidence:'none'};const parts=src.split(/\s*[;|]\s*|\n+/).filter(Boolean),rules=[];
 for(const part of parts){const range=parseTimeRange(part);if(!range)continue;const days=weekdaySet(part);rules.push({...range,days:[...days]})}
 if(!rules.length){const range=parseTimeRange(src);if(range)rules.push({...range,days:[]})}
 return {rules,confidence:rules.length?'parsed':'text-only',raw:src};
}
function hoursForDate(event,date){if(event.hoursByDate?.[date]){const r=parseTimeRange(event.hoursByDate[date]);if(r)return {...r,confidence:'curated'}}const meta=event._hoursMeta||parseHours(event.Times);const d=localDate(date);if(!d)return null;const exact=meta.rules.find(r=>r.days?.includes(d.getDay()));const fallback=meta.rules.find(r=>!r.days?.length);const r=exact||fallback||meta.rules[0];return r?{...r,confidence:meta.confidence}:null}
function enrich(e){e._dateMeta=parseSchedule(e);e._hoursMeta=parseHours(e.Times);return e}
function selectedWindow(value,now=new Date()){let a,b,label='';if(!value)return null;if(value==='today'||value==='tonight'){a=new Date(now.getFullYear(),now.getMonth(),now.getDate());b=a;label=value==='tonight'?'Tonight':'Today'}else if(value==='tomorrow'){a=add(new Date(now.getFullYear(),now.getMonth(),now.getDate()),1);b=a;label='Tomorrow'}else if(value==='weekend'||value==='next-weekend'){const base=new Date(now.getFullYear(),now.getMonth(),now.getDate()),wd=base.getDay();let toFri=wd===6?-1:wd===0?-2:5-wd;if(value==='next-weekend')toFri+=7;a=add(base,toFri);b=add(a,2);label=value==='weekend'?'This weekend':'Next weekend'}else if(/^\d{4}-\d{2}-\d{2}$/.test(value)){a=localDate(value);b=a;label=a.toLocaleDateString(undefined,{weekday:'short',month:'short',day:'numeric'})}else return null;return {start:iso(a),end:iso(b),label,value}}
function matchesWhen(event,value,now=new Date()){if(!value)return true;const w=selectedWindow(value,now);if(!w)return true;const ds=event._dateMeta?.dates||parseSchedule(event).dates;if(!ds.some(d=>d>=w.start&&d<=w.end))return false;if(value!=='tonight')return true;const h=hoursForDate(event,w.start);if(!h)return true;return h.end>17*60&&h.start<26*60}
function nextOccurrence(event,from=iso(new Date())){const ds=event._dateMeta?.dates||parseSchedule(event).dates;return ds.find(d=>d>=from)||null}
window.DATE_TOOLS={parseSchedule,parseTime:parseTimeRange,parseHours,hoursForDate,enrich,selectedWindow,matchesWhen,nextOccurrence,iso,localDate,add};
})();
