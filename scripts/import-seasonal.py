import json,re,unicodedata,datetime,pathlib,difflib,collections
root=pathlib.Path(__file__).resolve().parents[1]
p=root/'assets/data.js'; import subprocess
old=json.loads(subprocess.check_output(['git','show','origin/development:assets/data.js'],cwd=root,text=True).removeprefix('window.SITE_DATA = ').rstrip(';\n'))
rows=json.load(open(root/'research/source-database.json'));headers=rows[0]
def norm(s):return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')
def clean(s):
 if not s:return ''
 return ' '.join(t.strip() for t in re.split(r'(?<=[.!?])\s+',s) if not re.search(r'\b(QA|recheck|canonical|ingestion|do not publish|before publish|primary.*preferred|discovered because|research|surfaced|indexing|retain as|retain.*tag|website ingestion|current.*source used|deduplic|needs confirmation)\b',t,re.I))
regions={'Ogden / Weber':'Ogden, Weber & Morgan','Salt Lake City':'Salt Lake City','Salt Lake Valley':'Salt Lake Valley','Davis County':'Davis County','Utah County':'Utah County','Park City / Summit':'Park City & Wasatch Back','Wasatch Back':'Park City & Wasatch Back','Salt Lake Mountains':'Salt Lake Valley','Cache Valley':'Cache & Northern Utah'}
holidays=old['holidays']
def tags(s):
 # Use the canonical roster, including deliberately untagged notable events.
 out=[]
 for token in re.split(r'\s*[|]\s*',str(s or '')):
  if token in holidays:out.append(token)
  elif token=='Halloween & Fall':out.extend(['Halloween','Fall'])
 return list(dict.fromkeys(out))
def types(c):
 return [l for l,k in [('Lights & Displays','lights|display|lantern'),('Markets & Shopping','market|shopping|boutique|bazaar'),('Live Music & Performance','concert|theatre|theater|ballet|performance|film|choir|symphony|drag|cabaret|burlesque'),('Nightlife & Parties','nightlife|party|rave|bar crawl|club|singles'),('Active & Outdoors','race|fitness|skating|ski|outdoor|hike'),('Food & Drink','dining|food|brunch|breakfast|meal|beer'),('Workshops & Learning','craft|workshop|science|educational|museum'),('Community & Culture','community|culture|cultural|ceremony|civic|nativity|faith'),('Santa & Family','santa|family'),('Giving & Volunteering','charity|giveaway|volunteer|service|donation'),('Haunts & Scares','haunt|horror|paranormal|krampus'),('Farms & Harvest','farm|pumpkin|maze') ] if re.search(k,c,re.I)] or ['Community & Culture']
events=old['events'];index={norm(e['Event / attraction']):e for e in events};research=[]
for n,row in enumerate(rows[1:],2):
 if not row or not row[0]:continue
 r={h:(row[i] if i<len(row) and row[i]!=None else '') for i,h in enumerate(headers)};status=r['2026 status'];key=norm(r['Event']);start=r['Start date'];end=r['End date'];holiday=tags(r['Normalized Holiday Tags'] or r['Holiday / Season'])
 if 'Discovery lead' in status or not status:research.append(r);continue
 e=index.get(key)
 if not e:
  # Keep existing stable URLs for punctuation-only and high-confidence name variants.
  close=difflib.get_close_matches(key,index.keys(),n=1,cutoff=.985)
  e=index.get(close[0]) if close else None
 if not e:
  e={'id':key,'Event / attraction':r['Event'],'socials':[],'photo':None,'sponsored':False};events.append(e);index[key]=e
 e.update({'holidays':holiday,'primaryHoliday':holiday[0] if holiday else '','Region':r['Region'] or r['City'],'sourceRegion':r['Region'],'publicRegion':regions.get(r['Region'],r['Region'] or 'Other Utah'),'categories':[r['Category']],'sourceCategories':[r['Category']],'publicTypes':types(r['Category']),'First date':start,'startDate':start,'endDate':end,'2026 schedule':(start if start==end else f'{start} – {end}') if start and re.fullmatch(r'20\d\d-\d\d-\d\d',str(end)) else end or 'Dates to be announced','Times':r['Time / schedule'],'Price':r['Price / admission'] or 'Price not announced','Age':r['Age / audience'] or 'Audience details on official page','Location':', '.join(x for x in [r['Venue'],r['City']] if x),'Status':status,'Website':r['Source URL'],'Why / thoughts':clean(r['Research notes']) or 'Visit the event page for the program, tickets and the latest details.','Extra notes':clean(r['Accessibility / practical flag']),'travelTier':r['Travel Tier'],'lastVerified':r['Last Verified'] or '2026-10-06','qaFlags':r['QA Flags'],'timezone':'America/Denver','sourceRow':n,'isWatch':bool(re.search(r'watch|historical|not.*confirmed',status,re.I)),'flags':[]})
 if 'Notable Event' in r:e['notable_event']=str(r['Notable Event']).strip().lower()=='true'
 elif 'notable_event' in r:e['notable_event']=str(r['notable_event']).strip().lower()=='true'
 else:e.setdefault('notable_event',False)
 e['isFree']=bool(re.match(r'^Free($| / public| admission|;)|^Complimentary',e['Price'],re.I)) and not re.search(r'free with|no price|not stated|no admission stated',e['Price'],re.I)
 prices=[float(x) for x in re.findall(r'\$(\d+(?:\.\d+)?)',e['Price'])];price=max(prices) if prices else None
 e['costCount']=1 if e['isFree'] else 2 if price!=None and price<=25 else 3 if price!=None and price<=50 else 4 if price!=None and price<=100 else 5 if price!=None else 0
 e['Cost']='' # use written prices instead of inferred emoji shorthand
 txt=' '.join([r['Category'],r['Practical Flags'],r['Accessibility / practical flag'],r['Age / audience'],e['Price'],r['Research notes']])
 for label,rx in [('Outdoor','\boutdoor\b'),('Indoor','\bindoor\b'),('21+','21\\+'),('18+','18\\+'),('Reservation required','reservations? required|pre-registration|by appointment'),('Sold out','sold out'),('Walking','significant walking|large outdoor walking|walking between'),('Fog / lasers','fog|haze|lasers'),('Weather dependent','weather-dependent'),('Community meal','community meal'),('Free admission','^$')]:
  if re.search(rx,txt,re.I):e['flags'].append(label)
 e['flags']+= [x.strip() for x in r['Practical Flags'].split(';') if x.strip() and x.strip() not in e['flags'] and x.strip() not in ['Free']]
 if e['isFree']:e['flags'].insert(0,'Free admission')
 e['rating']={'type':r['Seasonal Rating Type'],'value':r['Seasonal Rating'],'basis':'Editorial guide to the experience; not a customer review.'} if r['Seasonal Rating'] else None
 if not e['rating'] and 'Halloween & Fall' in holiday and e.get('ghostCount'):e['rating']={'type':'Scare level','value':e['ghostCount'],'basis':'Editorial scare guidance.'}
 if not e['rating'] and 'Active & Outdoors' in e['publicTypes']:e['rating']={'type':'Activity level','value':3 if re.search('race|fitness|ski',r['Category'],re.I) else 2,'basis':'Editorial activity guidance based on the advertised format.'}
 if r['Social URL']:
  url=r['Social URL'];platform=next((k for k in ['instagram','facebook','tiktok','linkedin','bluesky'] if k in url or k=='bluesky' and 'bsky.app' in url),None)
  if platform and not any(s.get('url')==url for s in e['socials']):e['socials'].append({'platform':platform,'url':url})
 # Only precise single-day dates or explicitly daily/selected occurrences feed date tools.
 e['occurrenceDates']=[];e['scheduleConfidence']='unresolved';e['scheduleNote']='Choose a date on the organizer’s calendar.'
 conflict=bool(re.search(r'conflict|date confirmation|date caveat|schedule needs recheck|corrected organizer',status+' '+r['QA Flags']+' '+r['Research notes'],re.I))
 if start and re.fullmatch(r'20\d\d-\d\d-\d\d',str(start)) and not conflict and not e['isWatch']:
  a=datetime.date.fromisoformat(start);b=datetime.date.fromisoformat(end) if re.fullmatch(r'20\d\d-\d\d-\d\d',str(end)) else a;time=r['Time / schedule'];diff=(b-a).days
  if a==b and re.fullmatch(r'20\d\d-\d\d-\d\d',str(end)):e['occurrenceDates']=[start]
  elif re.search(r'\bdaily\b|\bnightly\b|both nights|both listed dates|self-guided anytime',time,re.I) and 0<=diff<150:e['occurrenceDates']=[(a+datetime.timedelta(days=i)).isoformat() for i in range(diff+1)]
  if e['occurrenceDates']:e['scheduleConfidence']='verified-dates';e['scheduleNote']=''
 if conflict:e['scheduleNote']='The organizer’s posted dates differ. Check the event page before making plans.';e['occurrenceDates']=[]
 # Generic practical context is not a sourced accommodation badge.
 if re.search(r'wheelchair-accessible seating|no-stress adaptive|officially designated.*sensory',r['Accessibility / practical flag'],re.I):
  e['accessibility']={'summary':r['Accessibility / practical flag'],'url':r['Source URL'],'tone':'positive'}
 # Never treat a current-year copyright as evidence of a current season.
 if e['id'] in ['zoolights-2026','zoolights-silent-night']:
  e.update(isWatch=True,occurrenceDates=[],scheduleConfidence='unresolved',Status='2026–27 season not yet announced',**{'2026 schedule':'2026–27 dates to be announced','Times':'Hours to be announced','Price':'2026–27 prices to be announced','Extra notes':'','Why / thoughts':'An outdoor holiday light display at Hogle Zoo. Watch for the new season announcement.'});e['flags']=[];e['rating']=None;e.pop('accessibility',None)
 # Icon artwork theme.
 e['artKey']=e.get('artKey') or ('nightlife' if 'Nightlife & Parties' in e['publicTypes'] else 'performance' if 'Live Music & Performance' in e['publicTypes'] else 'community')
for e in events:
 e.setdefault('holidays',[]);e.setdefault('primaryHoliday',e['holidays'][0] if e['holidays'] else '');e.setdefault('notable_event',False);e.setdefault('flags',[]);e.setdefault('lastVerified','2026-10-04');e.setdefault('timezone','America/Denver');e.setdefault('rating',{'type':'Scare level','value':e.get('ghostCount'),'basis':'Editorial scare guidance.'} if e.get('ghostCount') else None)
 if not e.get('sourceRow'):e['Why / thoughts']=clean(e.get('Why / thoughts',''));e['Extra notes']=clean(e.get('Extra notes',''));e['isFree']=bool(re.match(r'^Free($| admission|;)',e.get('Price',''),re.I))
# Deduplicate only exact stable identity. Record any conflicts for review.
seen={};merged=[]
for e in events:
 if e['id'] in seen:continue
 seen[e['id']]=e;merged.append(e)
old['events']=merged;old['holidays']=holidays;old['regions']=sorted(set(e['publicRegion'] for e in merged));old['categories']=sorted(set(t for e in merged for t in e['publicTypes']));old['ages']=sorted(set(e['Age'] for e in merged))
old['meta'].update(title='Utah Seasonal Guide · 2026–27',updated='October 6, 2026',eventCount=len(merged),confirmedCount=sum(not e['isWatch'] for e in merged),watchCount=sum(e['isWatch'] for e in merged),siteVersion='v10-editorial-archive',publicRegionCount=len(old['regions']))
p.write_text('window.SITE_DATA = '+json.dumps(old,ensure_ascii=False,separators=(',',':'))+';\n')
(root/'research/unpublished-leads.json').write_text(json.dumps(research,ensure_ascii=False,indent=2))
print('Imported',len(merged),'events;',old['meta']['confirmedCount'],'confirmed;',len(research),'unpublished research leads')

# Preserve additive seasons after every canonical import.
subprocess.run(["python3",str(root/"scripts/apply-season-membership.py")],cwd=root,check=True)
