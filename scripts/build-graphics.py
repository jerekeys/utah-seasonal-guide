import pathlib,json
palettes={'halloween':('#211b22','#ffb45c','#a92d34'),'christmas':('#132f25','#e8c777','#a32c3a'),'winter':('#172e41','#bce6ed','#38627a'),'hanukkah':('#172d4a','#e7cd7a','#265386'),'diwali':('#3b1931','#ffc459','#973d68'),'thanksgiving':('#352818','#eec778','#794521'),'yule':('#23372b','#ddce81','#3e6350'),'newyear':('#292037','#f5d981','#694983'),'kwanzaa':('#222720','#acd184','#a63436')}
icons={
 'halloween':'<path d="M800 275q45-100 100-85l-50 110" fill="none" stroke="ACC" stroke-width="30"/><ellipse cx="800" cy="500" rx="195" ry="170" fill="ACC"/><path d="m680 450 75-35 15 80Zm240 0-75-35-15 80Z M675 550q125 120 250 0l-45 110H720Z" fill="INK"/>',
 'christmas':'<path d="m800 215 55 155h-25l90 120h-45l90 140H635l90-140h-45l90-120h-25Z" fill="ACC"/><rect x="778" y="630" width="44" height="70" fill="ACC"/><path d="m800 165 12 30 33 1-26 20 9 32-28-18-28 18 9-32-26-20 33-1Z" fill="RED"/><g fill="RED"><circle cx="800" cy="360" r="18"/><circle cx="760" cy="480" r="18"/><circle cx="850" cy="540" r="18"/><circle cx="740" cy="580" r="18"/></g>',
 'winter':'<g stroke="ACC" stroke-width="25" stroke-linecap="round"><path d="M800 220v450M605 332l390 226M605 558l390-226"/><path d="m750 250 50 50 50-50m-100 390 50-50 50 50m-216-245 66-18-18-66m284 0-18 66 66 18m-380 102 66 18-18 66m284 0-18-66 66-18"/></g>',
 'diwali':'<path d="M605 490h390q-25 195-195 195T605 490Z" fill="ACC"/><path d="M800 440q-110-90 0-245 100 145 0 245Z" fill="ACC"/><path d="M800 440q-40-50 0-110 40 60 0 110Z" fill="RED"/><ellipse cx="800" cy="490" rx="200" ry="35" fill="RED"/>',
 'thanksgiving':'<path d="M800 225q-95 135-185 50l20 180-80 55 160 50 85 115 85-115 160-50-80-55 20-180q-90 85-185-50Z" fill="ACC"/><path d="M800 365v330m0-180-90-60m90 110 90-60" fill="none" stroke="INK" stroke-width="20"/>',
 'yule':'<circle cx="800" cy="355" r="115" fill="ACC"/><g stroke="ACC" stroke-width="20"><path d="M800 170v50m0 270v50m-185-185h50m270 0h50M668 223l38 38m188 188 38 38m0-264-38 38m-188 188-38 38"/></g><path d="m620 645 60-90h-30l50-80 50 80h-30l60 90Zm150 0 60-90h-30l50-80 50 80h-30l60 90Z" fill="RED"/>',
 'newyear':'<g fill="none" stroke="ACC" stroke-width="18" stroke-linecap="round"><path d="M800 220v100m0 200v100M600 420h100m200 0h100M660 280l70 70m140 140 70 70m0-280-70 70m-140 140-70 70"/></g><circle cx="800" cy="420" r="45" fill="RED"/><path d="M620 700q90-140 180 0 90-140 180 0" fill="none" stroke="RED" stroke-width="25"/>',
}
def candles(theme):
 n=9 if theme=='hanukkah' else 7; xs=[800+(i-(n-1)/2)*54 for i in range(n)];s='<path d="M800 540v120m-70 0h140" fill="none" stroke="ACC" stroke-width="20"/>'
 for i,x in enumerate(xs):
  y=270 if theme=='hanukkah' and i==4 else 330;col='ACC' if theme=='hanukkah' else '#d84f50' if i<3 else '#0b0c0b' if i==3 else '#60af70';s+=f'<rect x="{x-10}" y="{y}" width="20" height="{520-y}" fill="{col}"/><path d="M{x} {y-15}q-22-30 0-58 22 28 0 58Z" fill="ACC"/><path d="M{x} 520Q{x} 560 800 560" stroke="ACC" stroke-width="12" fill="none"/>'
 return s
icons['hanukkah']=candles('hanukkah');icons['kwanzaa']=candles('kwanzaa')

palettes['dayofdead']=('#34213f','#f7b64d','#c44b82')
palettes['veterans']=('#192e47','#f2dfb1','#a13e42')
icons['dayofdead']='<path d="M640 440q0-220 160-220t160 220v100l-55 45v90H695v-90l-55-45Z" fill="ACC"/><g fill="INK"><ellipse cx="730" cy="430" rx="42" ry="48"/><ellipse cx="870" cy="430" rx="42" ry="48"/><path d="m800 480-30 55h60Z"/><path d="M725 600h150v22H725Z"/></g><g fill="RED"><circle cx="800" cy="320" r="35"/><circle cx="650" cy="470" r="25"/><circle cx="950" cy="470" r="25"/></g><g stroke="INK" stroke-width="10"><path d="M750 580v55m50-55v55m50-55v55"/></g>'
icons['veterans']='<path d="m800 255 63 127 140 20-102 99 24 140-125-66-125 66 24-140-102-99 140-20Z" fill="ACC"/><g fill="none" stroke="RED" stroke-width="24" stroke-linecap="round"><path d="M650 690q-145-90-100-255m400 255q145-90 100-255"/><path d="m570 555-65-35m65 80-65-15m105 70-65 10m385-110 65-35m-65 80 65-15m-105 70 65 10"/></g>'

activity={'community':'','performance':'<path d="M1080 490v170m0-170 90-20v170m-90-140 90-20" fill="none" stroke="ACC" stroke-width="20"/><ellipse cx="1058" cy="660" rx="28" ry="20" fill="ACC"/><ellipse cx="1148" cy="640" rx="28" ry="20" fill="ACC"/>','market':'<rect x="1040" y="540" width="125" height="130" rx="10" stroke="ACC" fill="INK" stroke-width="16"/><path d="M1070 540v-30q35-70 65 0v30" fill="none" stroke="ACC" stroke-width="16"/>','nightlife':'<path d="m1030 510 70 95 70-95Zm70 95v90m-45 0h90" fill="none" stroke="ACC" stroke-width="16"/>','active':'<circle cx="1100" cy="500" r="20" fill="ACC"/><path d="m1100 535-35 55 55 20 35 65m-55-115 60 10m-60 30-60 65" fill="none" stroke="ACC" stroke-width="18"/>'}
out=pathlib.Path('assets/art/seasonal');out.mkdir(parents=True,exist_ok=True)
for theme,(ink,acc,red) in palettes.items():
 for kind,mark in activity.items():
  s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900"><rect width="1600" height="900" fill="INK"/><circle cx="800" cy="450" r="320" fill="RED" opacity=".22"/><g fill="ACC" opacity=".4"><circle cx="300" cy="250" r="12"/><circle cx="1250" cy="230" r="10"/><circle cx="350" cy="650" r="8"/><circle cx="1220" cy="670" r="12"/></g>{icons[theme]}{mark}</svg>'
  for a,b in [('INK',ink),('ACC',acc),('RED',red)]:s=s.replace(a,b)
  (out/f'{theme}-{kind}.svg').write_text(s)
p=pathlib.Path('assets/data.js');d=json.loads(p.read_text().removeprefix('window.SITE_DATA = ').rstrip(';\n'))
themes={'Halloween & Fall':'halloween','Día de los Muertos':'dayofdead','Veterans Day':'veterans','Christmas':'christmas','Hanukkah':'hanukkah','Diwali':'diwali','Kwanzaa':'kwanzaa','Yule & Solstice':'yule','New Year':'newyear','Thanksgiving':'thanksgiving'}
for e in d['events']:
 theme=themes.get(e['primaryHoliday'],'winter');e['theme']=theme;kind='nightlife' if 'Nightlife & Parties' in e['publicTypes'] else 'performance' if 'Live Music & Performance' in e['publicTypes'] else 'market' if 'Markets & Shopping' in e['publicTypes'] else 'active' if 'Active & Outdoors' in e['publicTypes'] else 'community'
 e['placeholder']=f'assets/art/seasonal/{theme}-{kind}.svg' if theme!='halloween' else f'assets/art/{e.get("artKey","default")}.svg'
 if not pathlib.Path(e['placeholder']).exists():e['placeholder']=f'assets/art/seasonal/{theme}-{kind}.svg'
p.write_text('window.SITE_DATA = '+json.dumps(d,ensure_ascii=False,separators=(',',':'))+';\n')
pathlib.Path('assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#19201d"/><path d="m32 8 8 16 18 3-13 13 3 18-16-8-16 8 3-18L6 27l18-3Z" fill="#f3d47c"/></svg>')
print('Created 45 seasonal SVGs and favicon; run export-social.cjs for PNG exports')
