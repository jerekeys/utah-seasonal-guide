import json,pathlib,datetime
p=pathlib.Path('assets/data.js');d=json.loads(p.read_text().removeprefix('window.SITE_DATA = ').rstrip(';\n'))
for e in d['events']:
 if e['id']=='winter-craftacular':e.update(Location='Magna Library, 2675 S 8950 W, Magna',Price='Free',isFree=True,costCount=1,scheduleNote='Craft materials are provided. For tweens, teens and adults.',publicRegion='Salt Lake Valley')
 if 'christkindlmarkt' in e['id']:e.update(occurrenceDates=['2026-12-02','2026-12-03','2026-12-04','2026-12-05'],Times='11:00 AM–8:00 PM')
 if 'luminaria' in e['id'] and not e['isWatch']:
  a=datetime.date(2026,11,12);b=datetime.date(2027,1,9);e['occurrenceDates']=[]
  while a<=b:
   if a.weekday()!=6 and a.isoformat() not in ['2026-12-24','2026-12-25']:e['occurrenceDates'].append(a.isoformat())
   a+=datetime.timedelta(days=1)
  e['Times']='Timed entry; select a slot on the ticket page';e['scheduleNote']='Monday–Saturday, except Christmas Eve and Christmas Day. Book an entry time with the organizer.'
p.write_text('window.SITE_DATA = '+json.dumps(d,ensure_ascii=False,separators=(',',':'))+';\n')
g=pathlib.Path('scripts/build-graphics.py');s=g.read_text().split('# Export precise vector')[0];g.write_text(s+"print('Created 45 seasonal SVGs and favicon; run export-social.cjs for PNG exports')\n")
p=pathlib.Path('assets/date-tools.js');s=p.read_text();s=s.replace('if(!h)return false;const parts=', 'const parts=');s=s.replace('return mins>=h.start&&mins<h.end}return true}', "const y=iso(add(localDate(w.start),-1)),prev=hoursForDate(e,y);return (!!h&&mins>=h.start&&mins<h.end)||(dates.includes(y)&&prev?.end>1440&&mins<prev.end-1440)}return true}");p.write_text(s)
p=pathlib.Path('netlify.toml');s=p.read_text().split('[context.development]')[0];p.write_text(s)
