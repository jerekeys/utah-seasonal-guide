import concurrent.futures,datetime,json,pathlib,urllib.request,urllib.parse,re
from html.parser import HTMLParser
D=json.loads(pathlib.Path('assets/data.js').read_text()[19:].rstrip(';\n'))
class Images(HTMLParser):
 def __init__(self):super().__init__();self.images=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);url=None
  if tag=='meta' and (a.get('property') or a.get('name') or '').lower() in ['og:image','og:image:secure_url','twitter:image']:url=a.get('content')
  if tag=='img':
   url=a.get('src') or a.get('data-src')
   srcset=a.get('srcset') or a.get('data-srcset')
   if srcset:url=srcset.split(',')[-1].strip().split()[0]
  if url and not any(x in url.lower() for x in ['logo','icon','favicon','avatar','spinner','data:']):self.images.append({'url':url,'alt':a.get('alt','')})
def inspect(url):
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'UtahSeasonalGuide/1.0 (event photo research)'})
  with urllib.request.urlopen(req,timeout=12) as r:
   if 'html' not in r.headers.get('Content-Type',''):return {'status':'No HTML image source','candidates':[]}
   p=Images();p.feed(r.read(2500000).decode('utf-8','replace'));base=r.geturl()
  out=[]
  for a in p.images:
   a['url']=urllib.parse.urljoin(base,a['url'])
   if a['url'].startswith('https://') and a['url'] not in [x['url'] for x in out]:out.append(a)
  return {'status':'Candidates need visual and rights review' if out else 'No usable candidate identified','candidates':out[:40]}
 except Exception as x:return {'status':'Source unavailable: '+type(x).__name__,'candidates':[]}
urls=list(dict.fromkeys(e['Website'] for e in D['events'] if e.get('Website','').startswith('https://')))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:pages=dict(zip(urls,pool.map(inspect,urls)))
report=[{'id':e['id'],'name':e['Event / attraction'],'source':e['Website'],'publishedPhoto':e.get('photo'),'placeholder':e['placeholder'],**pages.get(e['Website'],{'status':'No source URL','candidates':[]})} for e in D['events']]
pathlib.Path('research/photo-audit.json').write_text(json.dumps({'checked':datetime.datetime.now(datetime.timezone.utc).isoformat(),'events':report},ensure_ascii=False,indent=2))
print('Recorded source-level image research for',len(report),'events; candidates are not automatically published.')
