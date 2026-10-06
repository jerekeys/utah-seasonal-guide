(()=>{
const tz='America/Denver',pad=n=>String(n).padStart(2,'0');
const iso=d=>`${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
const localDate=s=>/^\d{4}-\d{2}-\d{2}$/.test(s||'')?new Date(+s.slice(0,4),+s.slice(5,7)-1,+s.slice(8,10),12):null;
const add=(d,n)=>new Date(d.getFullYear(),d.getMonth(),d.getDate()+n,12);
function today(now=new Date()){return new Intl.DateTimeFormat('en-CA',{timeZone:tz,year:'numeric',month:'2-digit',day:'2-digit'}).format(now)}
function clock(s,hint=''){s=s.trim().toLowerCase();if(s==='midnight')return 1440;if(s==='noon')return 720;let m=s.match(/^(\d{1,2})(?::(\d{2}))?\s*(am|pm)$/)|| (hint?s.match(/^(\d{1,2})(?::(\d{2}))?$/):null);if(!m||+m[1]>12||+m[1]<1||+(m[2]||0)>59)return null;const ap=m[3]||hint;return (+m[1]%12+(ap==='pm'?12:0))*60+ +(m[2]||0)}
function parseTime(src){src=String(src||'').replace(/[–—]/g,'-');const m=src.match(/\b(\d{1,2}(?::\d{2})?\s*(?:AM|PM)?|noon|midnight)\s*-\s*(\d{1,2}(?::\d{2})?\s*(?:AM|PM)|noon|midnight)\b/i);if(!m)return null;const ap=(m[2].match(/(am|pm)/i)||[])[1]?.toLowerCase();let start=clock(m[1],ap),end=clock(m[2]);if(start===null||end===null)return null;if(end<=start)end+=1440;if(end-start>18*60)return null;return {start,end,label:m[0]}}
const names=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
function weekdays(s){const out=new Set();for(let i=0;i<7;i++)if(new RegExp('\\b'+names[i]+'(?:day|sday|nesday|rsday|urday)?s?\\b','i').test(s))out.add(i);const m=s.match(/\b(Sun|Mon|Tue|Wed|Thu|Fri|Sat)[a-z]*\s*[–-]\s*(Sun|Mon|Tue|Wed|Thu|Fri|Sat)[a-z]*/i);if(m){const a=names.findIndex(x=>x.toLowerCase()===m[1].toLowerCase()),b=names.findIndex(x=>x.toLowerCase()===m[2].toLowerCase());for(let i=a;;i=(i+1)%7){out.add(i);if(i===b)break}}return [...out]}
function startForDate(e,date){if(e.isWatch)return null;const explicit=e.startTimesByDate?.[date];if(explicit){const [h,m]=explicit.split(':').map(Number);return h*60+m}const match=String(e.Times||'').trim().match(/^(\d{1,2}(?::\d{2})?\s*(?:AM|PM))(?:\s+(?:nightly|daily))?$/i);return match?clock(match[1]):null}
function hoursForDate(e,date){if(e.isWatch)return null;if(e.hoursByDate?.[date])return parseTime(e.hoursByDate[date]);const s=e.Times||'',parts=s.split(/;|\n|\|/);const day=localDate(date)?.getDay();const rules=parts.map(p=>({...parseTime(p),days:weekdays(p)})).filter(r=>r.start!=null);const rule=rules.find(r=>r.days.includes(day))||rules.find(r=>!r.days.length);if(!rule)return null; // Never apply Monday-only hours on a Saturday.
 if(/VIP|doors|seatings|show\/dancing|show starts/i.test(s)&&parts.length>1)return null;
 return rule}
function parseSchedule(e){return{dates:e.isWatch?[]:[...(e.occurrenceDates||[])].sort(),confidence:e.scheduleConfidence||'unresolved'}}
function enrich(e){e._dateMeta=parseSchedule(e);return e}
function selectedWindow(v,now=new Date()){let a=localDate(today(now)),b=a,label=v;if(v==='tomorrow')a=b=add(a,1);else if(v==='weekend'||v==='next-weekend'){const wd=a.getDay();a=add(a,(wd===0?-2:wd===6?-1:5-wd)+(v==='next-weekend'?7:0));b=add(a,2)}else if(/^\d{4}-\d{2}-\d{2}$/.test(v))a=b=localDate(v);else if(!['today','tonight','open-now'].includes(v))return null;return{start:iso(a),end:iso(b),label}}
function matchesWhen(e,v,now=new Date()){if(!v)return true;if(e.isWatch)return false;const w=selectedWindow(v,now);if(!w)return false;const dates=parseSchedule(e).dates;if(!dates.some(d=>d>=w.start&&d<=w.end)){// Include yesterday's late event only when still open now.
 if(v!=='open-now')return false;const y=iso(add(localDate(w.start),-1)),h=hoursForDate(e,y),parts=new Intl.DateTimeFormat('en-US',{timeZone:tz,hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(now);const mins=+parts.find(p=>p.type==='hour').value*60+ +parts.find(p=>p.type==='minute').value;return dates.includes(y)&&h?.end>1440&&mins<h.end-1440}
 if(v==='tonight'){const h=hoursForDate(e,w.start);const start=startForDate(e,w.start);return (!!h&&h.end>17*60&&h.start<1440)||(start!==null&&start>=17*60)}
 if(v==='open-now'){const h=hoursForDate(e,w.start);const parts=new Intl.DateTimeFormat('en-US',{timeZone:tz,hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(now),mins=+parts.find(p=>p.type==='hour').value*60+ +parts.find(p=>p.type==='minute').value;const y=iso(add(localDate(w.start),-1)),prev=hoursForDate(e,y);return (!!h&&mins>=h.start&&mins<h.end)||(dates.includes(y)&&prev?.end>1440&&mins<prev.end-1440)}return true}
function nextOccurrence(e,from=today()){return parseSchedule(e).dates.find(d=>d>=from)||null}
window.DATE_TOOLS={iso,localDate,add,today,parseTime,startForDate,hoursForDate,parseSchedule,enrich,selectedWindow,matchesWhen,nextOccurrence};
})();
