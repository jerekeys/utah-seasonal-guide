from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse,unquote
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  for key in ['href','src']:
   value=a.get(key,'')
   if not value or value.startswith(('#','mailto:','data:','https:','http:')):continue
   p=unquote(urlparse(value).path)
   if not p:continue
   target=Path(p.lstrip('/')) if p.startswith('/') else self.page.parent/p
   if target.is_dir():target=target/'index.html'
   if not target.exists():errors.append(f'{self.page}: {value}')
errors=[];n=0
for page in list(Path('events').glob('*/index.html'))+list(Path('.').glob('*.html'))+list(Path('.').glob('*/index.html')):
 parser=Links();parser.page=page;parser.feed(page.read_text());n+=1
assert not errors,'\n'.join(errors[:30]);print(f'Checked local links on {n} pages')
