import json,pathlib,re
p=pathlib.Path('assets/data.js');d=json.loads(p.read_text()[19:].rstrip(';\n'))
copy={
'north-pole-express-2026':'Ride a holiday train with cocoa and cookies. Santa boards at the North Pole, with a gift for each child.',
'yule-fairs-at-crone-s-hollow':'Explore three rotating vendor fairs at Crone’s Hollow, with seasonal gifts and alternative holiday finds.',
'utah-metropolitan-ballet-the-nutcracker-autism-performance':'A Nutcracker performance designed for autistic guests and their families. Check the organizer’s accommodation details when booking.',
'grand-america-holiday-brunch-at-laurel':'Holiday brunch on Christmas Eve, Christmas Day and New Year’s Day. Choose your visit date and reserve with Laurel.',
'temple-square-daily-christmas-performances':'Hear school and community choirs, missionary groups, and string, flute, guitar and bell ensembles. Check the daily program for individual performance times.',
'springville-santa-village-free-santa-visits':'Visit Santa during additional sessions following Springville’s main holiday festival.',
'paranormal-percussion':'A percussion-focused Halloween performance for a musical night out.',
'provo-trick-or-treat-resource-fair':'Trick-or-treating and a community resource fair in Provo.',
'graveyard-shift-a-costume-party':'An October 17 costume party at Soundwell. Dress up and check the event page for the lineup and tickets.',
'halloween-edm-at-cache-bar':'Spend Halloween night with electronic music at Cache Bar.',
'odd-lake-city-halloween-festival':'Browse more than 90 artists and makers, with curiosities, antiques and horror-inspired merchandise.',
'saratoga-springs-fall-festival':'A city fall festival with inflatables, a petting zoo, train rides, trick-or-treating, food trucks and a community fair.',
 'taylorsville-fall-festival':'A heritage-center fall event with games, pumpkin decorating, pie-eating contests, quilts and photo areas.',
'rocktober-ogden-dinosaur-park':'Live local music, beer from Ogden Beer Company and discounted geodes at the Dinosaur Park.',
 'utah-olympic-park-autumn-scenic-chairlift':'Take a scenic chairlift ride for early-autumn views in Park City. Operation depends on the weather.',
 'the-park-center-trunk-or-treat-murray':'A city-hosted trunk-or-treat at Murray’s Park Center.'}
for e in d['events']:
 if e['id'] in copy:e['Why / thoughts']=copy[e['id']]
 for key in ['Why / thoughts','Extra notes','Age','Price']:
  s=e.get(key,'');s=s.replace(' | ','. ');s=re.sub(r'(?i)accessibility details to capture','Ask the organizer about specific access needs',s);s=re.sub(r'(?i)price to capture','price not yet announced',s);s=re.sub(r'(?i)Verify promoter/ticket age policy','Age requirements not yet announced',s);e[key]=s
p.write_text('window.SITE_DATA = '+json.dumps(d,ensure_ascii=False,separators=(',',':'))+';\n')
