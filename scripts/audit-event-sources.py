"""Gather event-specific evidence; findings are review leads, never auto-confirmations."""
import concurrent.futures, datetime, json, pathlib, re, urllib.request, urllib.parse, threading
from html.parser import HTMLParser
ROOT=pathlib.Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'assets/data.js').read_text().removeprefix('window.SITE_DATA = ').rstrip(';\n'))
class Page(HTMLParser):
 def __init__(self):super().__init__();self.text=[];self.links=[];self.images=[];self.skip=0;self.link=None
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t in ('script','style'):self.skip+=1
  if t=='a':self.link={'url':a.get('href',''),'label':a.get('aria-label','')}
  if t=='img':self.images.append({'url':a.get('src') or a.get('data-src',''),'alt':a.get('alt','')})
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
  if t=='a' and self.link:self.links.append(self.link);self.link=None
 def handle_data(self,s):
  if self.skip:return
  s=' '.join(s.split())
  if s:self.text.append(s)
  if self.link:self.link['label']+=' '+s
cache={};lock=threading.Lock()
def fetch(url):
 with lock:
  if url in cache:return cache[url]
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'UtahSeasonalGuide/1.0 (public event research)'})
  with urllib.request.urlopen(req,timeout=10) as r:
   raw=r.read(2000000).decode('utf8','replace');base=r.geturl()
  p=Page();p.feed(raw);text=' '.join(p.text)
  evidence=[]
  for m in re.finditer(r'\$\s*\d+(?:\.\d\d)?|\b(?:wheelchair|accessible|accessibility|ASL|hearing|sensory|neurodiver|LGBTQ|queer|Latino|Mexican|Hanukkah|Diwali|202[567]|\d{1,2}:\d\d\s*[AP]M)\b',text,re.I):
   excerpt=text[max(0,m.start()-100):m.end()+190]
   if excerpt not in evidence:evidence.append(excerpt)
  out={'url':base,'status':'read','evidence':evidence[:100],'links':[dict(a,url=urllib.parse.urljoin(base,a['url'])) for a in p.links], 'images':[dict(a,url=urllib.parse.urljoin(base,a['url'])) for a in p.images if a['url']]}
 except Exception as x:out={'url':url,'status':'unavailable: '+type(x).__name__,'evidence':[],'links':[],'images':[]}
 with lock:cache[url]=out
 return out
def review(e):
 pages=[];queue=[(e.get('Website',''),0)];seen=set()
 while queue and len(pages)<5:
  url,depth=queue.pop(0)
  if not url.startswith(('http://','https://')) or url in seen:continue
  seen.add(url);p=fetch(url);pages.append(dict(p,depth=depth))
  if depth<2:
   candidates=[a for a in p['links'] if re.search(r'ticket|admission|book now|buy now|accessib|accommodation|sensory',a['label'],re.I) and a['url'].startswith('https://') and not re.search('login|sign.in|donat|facebook|instagram|mailto',a['url'],re.I)]
   # Prioritize admission, then accommodation pages; preserve the actual linked route.
   candidates.sort(key=lambda a:0 if re.search('ticket|admission|buy now',a['label'],re.I) else 1)
   queue.extend((a['url'],depth+1) for a in candidates[:3])
 issues=[]
 if re.search(r'not.*announc|not.*post|ticketed|tickets required|see.*ticket',e.get('Price',''),re.I):issues.append('admission needs deeper review')
 if not e.get('accessibility'):issues.append('accommodation evidence needs review')
 if not e.get('occurrenceDates'):issues.append('operating dates need review')
 if not e.get('communities'):issues.append('community relevance needs review (may correctly be none)')
 return {'id':e['id'],'name':e['Event / attraction'],'issues':issues,'pages':pages,'humanReviewComplete':False}
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:rows=list(pool.map(review,D['events']))
report={'checked':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'All published records; up to two linked levels, five pages per record. Evidence requires event-level interpretation and poster review.','events':rows}
(ROOT/'research/source-evidence-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('Audited',len(rows),'records;',len(cache),'unique pages;',sum(any(p['status']=='read' for p in e['pages']) for e in rows),'records with readable evidence. No facts auto-published.')
