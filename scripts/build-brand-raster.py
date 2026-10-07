from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
INK="#17221d"; PAPER="#f5f0e4"; SIGNAL="#ef5a29"; PANEL="#fffdf8"

def font(size,bold=False,serif=False,mono=False):
    choices=[]
    if mono: choices=["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"]
    elif serif: choices=["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]
    elif bold: choices=["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    else: choices=["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for p in choices:
        try:return ImageFont.truetype(p,size)
        except OSError:pass
    return ImageFont.load_default()

def mark_points(cx,cy,size,scale=1.0):
    pts=[(32,4),(38,24),(57,15),(42,32),(57,49),(38,40),(32,60),(26,40),(7,49),(22,32),(7,15),(26,24)]
    return [((x-32)/56*size*scale+cx,(y-32)/56*size*scale+cy) for x,y in pts]

def draw_mark(draw,cx,cy,size,paper=PAPER,ink=INK,signal=SIGNAL,scale=1.0):
    draw.polygon(mark_points(cx,cy,size,scale),fill=signal)
    r=size*.09*scale;draw.ellipse((cx-r,cy-r,cx+r,cy+r),fill=paper)
    r=size*.038*scale;draw.ellipse((cx-r,cy-r,cx+r,cy+r),fill=ink)

def app_icon(size,maskable=False):
    img=Image.new("RGB",(size,size),INK);d=ImageDraw.Draw(img)
    draw_mark(d,size/2,size/2,size,PAPER,INK,SIGNAL,.72 if maskable else .84)
    return img

def grid(draw,w,h,ink):
    line=ink+"18"
    step=42
    for x in range(0,w,step):draw.line((x,0,x,h),fill=line,width=1)
    for y in range(0,h,step):draw.line((0,y,w,y),fill=line,width=1)

def share_card(name,title,paper,ink,accent,season):
    w,h=1200,630
    img=Image.new("RGB",(w,h),paper);d=ImageDraw.Draw(img)
    grid(d,w,h,ink)
    d.rectangle((0,0,20,h),fill=SIGNAL)
    draw_mark(d,78,75,90,paper,ink,SIGNAL,.82)
    d.text((145,43),"UTAH EVERY SEASON",font=font(29,bold=True),fill=ink)
    d.text((145,83),"OBSESSIVE FIELD GUIDE",font=font(17,mono=True),fill=season)
    d.line((72,142,1128,142),fill=ink,width=2)
    d.text((72,190),title,font=font(74,serif=True),fill=ink)
    d.text((76,302),"Things worth leaving the house for.",font=font(33),fill=ink)
    # field-guide plate on the right
    d.rectangle((825,365,1128,535),fill=PANEL,outline=ink,width=2)
    d.rectangle((825,365,838,535),fill=accent)
    draw_mark(d,972,438,120,PANEL,ink,SIGNAL,.72)
    d.text((862,492),"FIELD PLATE / 2026–27",font=font(14,mono=True),fill=ink)
    d.text((72,542),"FIELD GUIDE  ·  VERIFIED DETAILS  ·  INDEPENDENT EDITORIAL",font=font(17,mono=True),fill=ink)
    out=ROOT/"assets"/"share"/f"{name}.png";out.parent.mkdir(parents=True,exist_ok=True);img.save(out,optimize=True)

for name,size,mask in [("icon-180.png",180,False),("icon-192.png",192,False),("icon-512.png",512,False),("icon-maskable-512.png",512,True)]:
    out=ROOT/"assets"/"app"/name;out.parent.mkdir(parents=True,exist_ok=True);app_icon(size,mask).save(out,optimize=True)

themes={
 "halloween":("HALLOWEEN","#fff3e3","#211b22","#ff9b3d","#6f3d78"),
 "thanksgiving":("FALL / THANKSGIVING","#f7efe0","#34251d","#d87a2d","#7b3d2f"),
 "winter":("WINTER","#eef6f8","#172e41","#bce6ed","#38627a"),
 "christmas":("CHRISTMAS","#f4f6ec","#17382b","#d8bb67","#a32c3a"),
 "dayofdead":("DÍA DE LOS MUERTOS","#fbf1f8","#34213f","#f7b64d","#7c3658"),
 "diwali":("DIWALI","#fff4ee","#3b1931","#ffc459","#973d68"),
 "hanukkah":("HANUKKAH","#f0f5fc","#172d4a","#e7cd7a","#265386"),
 "kwanzaa":("KWANZAA","#f7f5eb","#222720","#acd184","#a63436"),
 "newyear":("NEW YEAR","#f7f2fa","#292037","#f5d981","#694983"),
 "pride":("PRIDE","#f7f2fa","#292037","#f0d687","#694983"),
 "veterans":("VETERANS DAY","#f5f5f0","#192e47","#f2dfb1","#a13e42"),
 "yule":("YULE / SOLSTICE","#f2f5e9","#23372b","#ddce81","#3e6350"),
}
for name,(title,paper,ink,accent,season) in themes.items():share_card(name,title,paper,ink,accent,season)
print("Built brand app icons and",len(themes),"share cards")
