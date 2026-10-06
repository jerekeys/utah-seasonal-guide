(()=>{
const tz='America/Denver',pad=n=>String(n).padStart(2,'0');
const iso=d=>`${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
const localDate=s=>/^\d{4}-\d{2}-\d{2}$/.test(s||'')?new Date(+s.slice(0,4),+s.slice(5,7)-1,+s.slice(8,10),12):null;
const add=(d,n)=>new Date(d.getFullYear(),d.getMonth(),d.getDate()+n,12);
function today(now=new Date()){return new Intl.DateTimeFormat('en-CA',{timeZone:tz,year:'numeric',month:'2-digit',day:'2-digit'}).format(now)}
function clock(s,hint=''){s=s.trim().toLowerCase();if(s==='midnight')return 1440;if(s==='noon')return 720;let m=s.match(/^(\d{1,2})(?::(\d{2}))?\s*(am|pm)$/)|| (hint?s.match(/^(\d{1,2})(?::(\d{2}))?$/):null);if(!m||+m[1]>12||+m[1]<1||+(m[2]||0)>59)return null;const ap=m[3]||hint;return (+m[1]%12+(ap==='pm'?12:0))*60+ +(m[2]||0)}
function parseTime(src){src=String(src||'').replace(/[–—]/g,'-');const m=src.match(/\b(\d{1,2}(?::\d{2})?\s*(?:AM|PM)?|noon|midnight)\s*-\s*(\d{1,2}(?::\d{2})?\s*(?:AM|PM)|noon|midnight)\b/i);if(!m)return null;const ap=(m[2].match(/(am|pm)/i)||[])[1]?.toLowerCase();let start=clock(m[1],ap),end=clock(m[2]);if(start===null||end===null)return null;if(end<=start)end+=1440;if(end-start>18*60)return null;return {start,end,label:m[0]}}
const dayNames=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
const dayToken='Sun(?:day)?|Mon(?:day)?|Tue(?:sday)?|Wed(?:nesday)?|Thu(?:rsday)?|Fri(?:day)?|Sat(?:urday)?';
function dayIndex(s){return dayNames.findIndex(x=>String(s).toLowerCase().startsWith(x.toLowerCase()))}
function weekdays(src){
 src=String(src||'').replace(/[–—]/g,'-');
 const out=new Set();
 for(const m of src.matchAll(new RegExp(`\\b(${dayToken})s?\\s*-\\s*(${dayToken})s?\\b`,'ig'))){const a=dayIndex(m[1]),b=dayIndex(m[2]);if(a>=0&&b>=0)for(let i=a;;i=(i+1)%7){out.add(i);if(i===b)break}}
 for(const m of src.matchAll(new RegExp(`\\b(${dayToken})s?\\b`,'ig'))){const d=dayIndex(m[1]);if(d>=0)out.add(d)}
 if(/\b(?:daily|nightly|every\s+day|everyday|open\s+daily|open\s+every\s+day)\b/i.test(src))for(let i=0;i<7;i++)out.add(i);
 if(/\bclosed\s+sundays?\b/i.test(src))out.delete(0);
 return [...out]
}
function startForDate(e,date){
 if(e.isWatch)return null;
 const explicit=e.startTimesByDate?.[date];if(explicit){const [h,m]=explicit.split(':').map(Number);return h*60+m}
 const src=String(e.Times||'').trim();
 let match=src.match(/^(\d{1,2}(?::\d{2})?\s*(?:AM|PM))(?:\s+(?:nightly|daily))?$/i);
 if(!match)match=src.match(/^(?:starts?|opens?)\s*(?:at\s*)?(\d{1,2}(?::\d{2})?\s*(?:AM|PM))/i);
 return match?clock(match[1]):null
}
function hoursForDate(e,date){
 if(e.isWatch)return null;
 if(e.hoursByDate?.[date])return parseTime(e.hoursByDate[date]);
 const s=e.Times||'',parts=s.split(/;|\n|\|/),day=localDate(date)?.getDay();
 const rules=parts.map(p=>({...parseTime(p),days:weekdays(p)})).filter(r=>r.start!=null);
 const rule=rules.find(r=>r.days.includes(day))||rules.find(r=>!r.days.length);
 if(!rule)return null;
 if(/VIP|doors|seatings|show\/dancing|show starts/i.test(s)&&parts.length>1)return null;
 return rule
}
const months={jan:0,january:0,feb:1,february:1,mar:2,march:2,apr:3,april:3,may:4,jun:5,june:5,jul:6,july:6,aug:7,august:7,sep:8,sept:8,september:8,oct:9,october:9,nov:10,november:10,dec:11,december:11};
const monthToken='Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?';
const monthIndex=s=>months[String(s).toLowerCase().replace('.','')];
function yearHint(e){for(const v of [e.startDate,e['First date'],...(e.occurrenceDates||[])]){const m=String(v||'').match(/^(20\d{2})-/);if(m)return +m[1]}const m=String(e['2026 schedule']||'').match(/\b(20\d{2})\b/);return m?+m[1]:2026}
function dateRange(e){
 const src=String(e['2026 schedule']||'').replace(/[–—]/g,'-');
 let m=src.match(/\b(20\d{2})-(\d{2})-(\d{2})\s*-\s*(20\d{2})-(\d{2})-(\d{2})\b/);
 if(m)return{start:`${m[1]}-${m[2]}-${m[3]}`,end:`${m[4]}-${m[5]}-${m[6]}`};
 m=src.match(new RegExp(`\\b(${monthToken})\\.?\\s+(\\d{1,2})(?:st|nd|rd|th)?\\s*-\\s*(?:(${monthToken})\\.?\\s+)?(\\d{1,2})(?:st|nd|rd|th)?(?:,?\\s*(20\\d{2}))?`,'i'));
 if(m){const y=+(m[5]||yearHint(e)),sm=monthIndex(m[1]),em=m[3]?monthIndex(m[3]):sm,ey=em<sm?y+1:y;return{start:`${y}-${pad(sm+1)}-${pad(+m[2])}`,end:`${ey}-${pad(em+1)}-${pad(+m[4])}`}}
 return null
}
function monthRange(e){
 const src=String(e['2026 schedule']||'');
 const m=src.match(new RegExp(`\\bin\\s+(${monthToken})\\b`,'i'));if(!m)return null;
 const y=yearHint(e),mo=monthIndex(m[1]),last=new Date(y,mo+1,0,12).getDate();
 return{start:`${y}-${pad(mo+1)}-01`,end:`${y}-${pad(mo+1)}-${pad(last)}`}
}
function textDates(e){
 const src=`${e['2026 schedule']||''}; ${e.Times||''}`.replace(/[–—]/g,'-'),out=new Set(),range=dateRange(e),baseYear=yearHint(e);
 const rangeStart=range?localDate(range.start):null,rangeEnd=range?localDate(range.end):null;
 const yearForMonth=mo=>rangeStart&&rangeEnd&&rangeEnd.getFullYear()>rangeStart.getFullYear()&&mo<rangeStart.getMonth()?rangeEnd.getFullYear():baseYear;
 for(const m of src.matchAll(/\b(20\d{2})-(\d{2})-(\d{2})\b/g))out.add(`${m[1]}-${m[2]}-${m[3]}`);
 for(const m of src.matchAll(new RegExp(`\\b(${monthToken})\\.?\\s+(\\d{1,2})(?:st|nd|rd|th)?\\b`,'ig'))){const mo=monthIndex(m[1]);out.add(`${yearForMonth(mo)}-${pad(mo+1)}-${pad(+m[2])}`)}
 for(const m of src.matchAll(new RegExp(`\\b(${monthToken})\\.?\\s+((?:\\d{1,2}(?:st|nd|rd|th)?\\s*(?:,|&|and)\\s*)+\\d{1,2}(?:st|nd|rd|th)?)`,'ig'))){const mo=monthIndex(m[1]),y=yearForMonth(mo);for(const n of m[2].match(/\d{1,2}/g)||[])out.add(`${y}-${pad(mo+1)}-${pad(+n)}`)}
 return[...out].filter(d=>localDate(d)).sort()
}
function inferredDates(e){
 if(e.isWatch)return[];
 const explicit=[...new Set([...(e.occurrenceDates||[]),...textDates(e)])].filter(d=>/^\d{4}-\d{2}-\d{2}$/.test(d));
 const src=`${e['2026 schedule']||''}; ${e.Times||''}`,days=weekdays(src);
 let range=dateRange(e);if(!range&&days.length)range=monthRange(e);
 if(!range)return[...new Set(explicit)].sort();
 const select=/\bselect(?:ed)?\s+(?:dates?|nights?)\b/i.test(src);
 const vague=/\b(?:performance schedule varies|multiple sessions|official calendar varies|hours vary by date|timed tickets;?\s*varies|varies by date)\b/i.test(src);
 let activeDays=[...days];
 const a=localDate(range.start),b=localDate(range.end);if(!a||!b||b<a)return[...new Set(explicit)].sort();
 const span=Math.round((b-a)/86400000)+1;
 if(!activeDays.length){
   const daily=/\b(?:daily|nightly|every\s+day|everyday|open\s+daily|open\s+every\s+day)\b/i.test(src);
   const typeText=(e.publicTypes||[]).join('|'),timeText=String(e.Times||''),blocked=/\b(?:select(?:ed)?\s+(?:dates?|nights?)|listed nights|date-specific|specific dates|multiple performances)\b/i.test(src);
   const continuous=!blocked&&(/\b(?:display|lights?|self-guided|anytime)\b/i.test(timeText)||(/Lights & Displays/.test(typeText)&&!!parseTime(timeText)));
   if((daily||(!select&&!vague&&(span<=7||continuous))))activeDays=[0,1,2,3,4,5,6];
 }
 if(!activeDays.length||(select&&!days.length&&!/\b(?:daily|nightly|every\s+day|everyday)\b/i.test(src)))return[...new Set(explicit)].sort();
 const inferred=[];for(let d=new Date(a);d<=b;d=add(d,1))if(activeDays.includes(d.getDay()))inferred.push(iso(d));
 return[...new Set([...explicit,...inferred])].sort()
}
function parseSchedule(e){const explicit=(e.occurrenceDates||[]).filter(d=>/^\d{4}-\d{2}-\d{2}$/.test(d)),dates=inferredDates(e);return{dates,confidence:dates.length>explicit.length?'inferred-recurring':(e.scheduleConfidence||'unresolved')}}
function enrich(e){e._dateMeta=parseSchedule(e);return e}
function selectedWindow(v,now=new Date()){let a=localDate(today(now)),b=a,label=v;if(v==='tomorrow')a=b=add(a,1);else if(v==='weekend'||v==='next-weekend'){const wd=a.getDay();a=add(a,(wd===0?-2:wd===6?-1:5-wd)+(v==='next-weekend'?7:0));b=add(a,2)}else if(/^\d{4}-\d{2}-\d{2}$/.test(v))a=b=localDate(v);else if(!['today','tonight','open-now'].includes(v))return null;return{start:iso(a),end:iso(b),label}}
function matchesWhen(e,v,now=new Date()){
 if(!v)return true;if(e.isWatch)return false;const w=selectedWindow(v,now);if(!w)return false;const dates=parseSchedule(e).dates;
 if(!dates.some(d=>d>=w.start&&d<=w.end)){
   if(v!=='open-now')return false;
   const y=iso(add(localDate(w.start),-1)),h=hoursForDate(e,y),parts=new Intl.DateTimeFormat('en-US',{timeZone:tz,hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(now),mins=+parts.find(p=>p.type==='hour').value*60+ +parts.find(p=>p.type==='minute').value;
   return dates.includes(y)&&h?.end>1440&&mins<h.end-1440
 }
 if(v==='tonight'){const h=hoursForDate(e,w.start),start=startForDate(e,w.start);return (!!h&&h.end>17*60&&h.start<1440)||(start!==null&&start>=17*60)}
 if(v==='open-now'){const h=hoursForDate(e,w.start),parts=new Intl.DateTimeFormat('en-US',{timeZone:tz,hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(now),mins=+parts.find(p=>p.type==='hour').value*60+ +parts.find(p=>p.type==='minute').value,y=iso(add(localDate(w.start),-1)),prev=hoursForDate(e,y);return (!!h&&mins>=h.start&&mins<h.end)||(dates.includes(y)&&prev?.end>1440&&mins<prev.end-1440)}
 return true
}
function nextOccurrence(e,from=today()){return parseSchedule(e).dates.find(d=>d>=from)||null}
function isPast(e,from=today(),now=new Date()){
 if(e.isWatch)return false;
 // The final night can remain open after midnight on the following date.
 if(from===today(now)&&matchesWhen(e,'open-now',now))return false;
 const dates=parseSchedule(e).dates,ends=[...dates,e.endDate].filter(d=>/^\d{4}-\d{2}-\d{2}$/.test(d||''));
 return ends.length>0&&ends.every(d=>d<from)
}
function isSingleDay(e){
 if(e.isWatch)return false;
 const dates=parseSchedule(e).dates;
 return dates.length===1&&(!e.endDate||e.endDate===dates[0])
}
function isUpcomingSoon(e,from=today()){
 if(e.isWatch)return false;
 const next=nextOccurrence(e,from);
 return !!next&&next>=from&&next<=iso(add(localDate(from),45))
}
function isCurrentNotable(e,from=today()){return e.notable_event===true&&isUpcomingSoon(e,from)}
function compareEvents(a,b,sort='recommended',from=today()){
 const name=()=>a['Event / attraction'].localeCompare(b['Event / attraction'])||a.id.localeCompare(b.id);
 if(sort==='name')return name();
 if(sort==='cost')return (a.costCount||9)-(b.costCount||9)||name();
 if(sort==='date')return (nextOccurrence(a,from)||'9999').localeCompare(nextOccurrence(b,from)||'9999')||name();
 return Number(isCurrentNotable(b,from))-Number(isCurrentNotable(a,from))||Number(isSingleDay(b))-Number(isSingleDay(a))||name()
}
window.DATE_TOOLS={iso,localDate,add,today,parseTime,startForDate,hoursForDate,parseSchedule,enrich,selectedWindow,matchesWhen,nextOccurrence,isPast,isSingleDay,isUpcomingSoon,isCurrentNotable,compareEvents};
})();