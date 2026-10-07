"""Add calendar seasons without replacing cultural, religious or holiday tags."""
import json,pathlib,datetime,collections,re,subprocess
p=pathlib.Path('assets/data.js');s=p.read_text();d=json.loads(s[s.index('{'):].strip().rstrip(';'))
seasons={12:'Winter',1:'Winter',2:'Winter',3:'Spring',4:'Spring',5:'Spring',6:'Summer',7:'Summer',8:'Summer',9:'Fall',10:'Fall',11:'Fall'}
resolved=json.loads(subprocess.check_output(['node','-e',"const fs=require('fs'),vm=require('vm');const ctx={window:{},Intl,Date};vm.createContext(ctx);vm.runInContext(fs.readFileSync('assets/data.js','utf8'),ctx);vm.runInContext(fs.readFileSync('assets/date-tools.js','utf8'),ctx);console.log(JSON.stringify(Object.fromEntries(ctx.window.SITE_DATA.events.map(e=>[e.id,ctx.window.DATE_TOOLS.parseSchedule(e).dates]))));"]))
changes=[]
for e in d['events']:
 dates=set(resolved.get(e['id'],[]) if not e.get('isWatch') else []);start=e.get('startDate');end=e.get('endDate') or start
 if not dates and start and end and not e.get('isWatch') and e.get('scheduleConfidence')!='date-conflict':
  a=datetime.date.fromisoformat(start);b=datetime.date.fromisoformat(end)
  if 0<=(b-a).days<=730:
   while a<=b:dates.add(a.isoformat());a+=datetime.timedelta(days=1)
 found=[x for x in ['Fall','Winter','Spring','Summer'] if any(re.match(r'^\d{4}-\d{2}-\d{2}$',v) and seasons[int(v[5:7])]==x for v in dates)]
 before=e.get('holidays',[])
 e['seasons']=found if found else [h for h in before if h in seasons.values()]
 e['holidays']=list(dict.fromkeys([*before,*e['seasons']]))
 if before!=e['holidays']:changes.append({'id':e['id'],'before':before,'after':e['holidays']})
 # Explicit repeated programs do not get the annual one-day boost.
 text=' '.join(str(e.get(k,'')) for k in ['Event / attraction','2026 schedule','Extra notes'])
 if re.search(r'\b(weekly|every (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|monthly|first friday|second saturday)\b',text,re.I):e['recurrence']='recurring'
d['meta']['seasonDefinition']='Fall: September–November; Winter: December–February; Spring: March–May; Summer: June–August. Holiday and cultural tags are additive.'
p.write_text('window.SITE_DATA = '+json.dumps(d,ensure_ascii=False,indent=2)+';\n')
pathlib.Path('research/season-membership-2026-10-06.json').write_text(json.dumps({'definition':d['meta']['seasonDefinition'],'changes':changes,'memberships':[{'id':e['id'],'seasons':e['seasons'],'holidays':e['holidays']} for e in d['events']]},ensure_ascii=False,indent=2))
print('Added seasons to',len(changes),'events');print(collections.Counter(h for e in d['events'] for h in e['seasons']))
