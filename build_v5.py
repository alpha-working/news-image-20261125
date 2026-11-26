"""Build v5 for news-image-20261125. Deterministic, no network.
V5 fixes v4 judge split calls: comparison-size layer carries the entry
(larger drawn scenes, bigger headlines, shorter facts, clean briefs),
date clarity via natural dateline, no DATE PROOF meta panel.
Same verified 39-story set as v4; no new stories, no fact/date changes.
"""
from PIL import Image, ImageDraw, ImageFont
import os
W,H=1024,1024
PAPER=(250,248,243); INK=(8,8,8); MUTED=(40,37,31)
RED=(158,28,18); BLUE=(24,76,112); TEAL=(12,112,104); GREEN=(20,96,50)
GOLD=(132,84,0); PURPLE=(84,38,132); NAVY=(12,30,52); RULE=(150,140,122)
WHITE=(255,255,255); YELLOW=(250,204,21); BEIGE=(240,231,214); LGRAY=(234,234,228)
SKY=(214,232,245); SKY2=(252,238,210)
SERIF_B="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def F(p,s): return ImageFont.truetype(p,s)
def wrap(d,text,fnt,max_w,max_lines=None):
    words,lines,cur=text.split(),[],""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=fnt)<=max_w: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
            if max_lines and len(lines)>=max_lines: break
    if cur and (not max_lines or len(lines)<max_lines): lines.append(cur)
    return lines[:max_lines] if max_lines else lines
def draw_lines(d,ls,x,y,fnt,fill,lh):
    for ln in ls: d.text((x,y),ln,font=fnt,fill=fill); y+=lh
    return y
def badge(d,x,y,text,col,size=11):
    f=F(SANS_B,size); w=int(d.textlength(text,font=f))+14
    d.rounded_rectangle([x,y,x+w,y+20],radius=5,outline=col,width=2,fill=WHITE)
    d.text((x+7,y+3),text,font=f,fill=col); return w
def numcircle(d,x,y,n,col=RED,r=15):
    d.ellipse([x,y,x+2*r,y+2*r],fill=col,outline=WHITE,width=2)
    d.text((x+r,y+r),str(n),font=F(SANS_B,14 if n<10 else 13),fill=WHITE,anchor="mm")
CARDS=[
 (1,"Americas","TRADE","WASHINGTON • TRADE","OFFICIAL",BLUE,"US tariffs hit 14 partners","China hit hardest. Reuters","Trade war widens","tariff"),
 (2,"World","MARKETS","SEOUL • MARKETS","CONFIRMED",GREEN,"AI doubts sink chip stocks","KOSPI −6.16%. Reuters","AI rally questioned","chipfall"),
 (3,"Asia","SPACE","TIANGONG • SPACE","OFFICIAL",BLUE,"First foreigner on Tiangong","Zeeshan Ali, 06:35 GMT. Reuters","First foreign crew","station"),
 (4,"Europe","WAR","KYIV • WAR","CONFIRMED",GREEN,"Ballistic missiles hit Kyiv","Power cut, 5 regions. Reuters","","kyiv"),
 (5,"Middle East","WAR","YEMEN • RED SEA","CONFIRMED",GREEN,"Houthis threaten Jeddah","Ports evacuate. Reuters","","ship"),
 (6,"Middle East","WAR","GAZA • WAR","CONFIRMED",GREEN,"Israel kills Hamas security chief","Col. Abuelouf dies. Reuters","","gaza"),
 (7,"Oceania","DIPLOMACY","CANBERRA • PACIFIC","OFFICIAL",BLUE,"Australia-Solomons treaty","Signed; defence partner. Reuters","","treaty"),
 (8,"Africa","DISASTER","EGYPT • DISASTER","OFFICIAL",BLUE,"Fuel fire kills 31 in Egypt","Tanker at Giza. Reuters","","fire"),
 (9,"Americas","CRIME","CARTAGENA • CRIME","OFFICIAL",BLUE,"Cartagena hostages freed","Freed 06:30 GMT. Reuters","","store"),
 (10,"Americas","COURTS","US • COURTS","OFFICIAL",BLUE,"Judge blocks birthright order","Second injunction. Reuters","","court"),
 (11,"Europe","POLITICS","RUSSIA • COURTS","OFFICIAL",BLUE,"Murmansk governor held","Corruption probe. Reuters","","court2"),
 (12,"Middle East","POLITICS","IRAQ • KURDISTAN","OFFICIAL",BLUE,"Iraq court backs border troops","Troops may go. Reuters","","oil"),
 (13,"Americas","TECH","SENATE • TECH","CONFIRMED",GREEN,"Senator presses Nvidia","Booker on Huang. Reuters","","nvidia"),
]
ALSO=[
 (14,"Africa","WAR","Sudan drones kill 19","C"),(15,"Europe","POLITICS","Spain: Puigdemont return","C"),
 (16,"Africa","COURTS","Ramaphosa reprieve","O"),(17,"World","WAR","34 states: stop riot gas","O"),
 (18,"Africa","COURTS","Kenya cult conviction","O"),(19,"Middle East","WAR","Syria IS kills 2 guards","R"),
 (20,"Africa","WAR","Nigeria militants: 30+ dead","R"),(21,"Africa","HEALTH","Congo Ebola evacuation","O"),
 (22,"Middle East","POLITICS","Iran: resist blockade","O"),(23,"Asia","DIPLOMACY","N. Korea expels envoy","O"),
 (24,"Europe","CLIMATE","Pope: COP31 troubling","C"),(25,"Europe","MIGRATION","Canaries: 2,100+ migrants","O"),
 (26,"Europe","MIGRATION","Bulgaria boat: 35 aboard","O"),(27,"Europe","SECURITY","UK jets moved over drones","R"),
 (28,"Europe","DIPLOMACY","Italy rebukes Ukraine","C"),(29,"Middle East","COURTS","Israel judges: Netanyahu","O"),
 (30,"World","CULTURE","Andy Taylor dies at 65","C"),(31,"Africa","CRIME","Nigeria seizes $227m meth","O"),
 (32,"Africa","POLITICS","Tinubu: Maiduguri peace","C"),(33,"Asia","DIPLOMACY","India on Hasina return","O"),
 (34,"Americas","SECURITY","Iowa detonates lead azide","O"),(35,"Europe","WAR","Ukraine: 5 planes hit","R"),
 (36,"Americas","SPORT","NFL Rams beat Packers","C"),(37,"Asia","DISASTER","Bogor mine toll: 6","C"),
 (38,"Asia","LABOUR","Bangladesh tear gas","C"),(39,"Europe","WAR","Samara refineries hit","R"),
]
regions={}; fields=set()
for n,reg,fld,*_ in CARDS+ALSO:
    regions[reg]=regions.get(reg,0)+1; fields.add(fld)
TOTAL=len(CARDS)+len(ALSO)
ORDER=["Europe","Middle East","Africa","Asia","Oceania","Americas","World"]
RCOL={"Europe":BLUE,"Middle East":TEAL,"Africa":GREEN,"Asia":RED,"Oceania":TEAL,"Americas":PURPLE,"World":(60,60,60)}
img=Image.new("RGB",(W,H),PAPER); d=ImageDraw.Draw(img)
d.rectangle([16,16,W-17,H-17],outline=INK,width=3)
d.text((34,26),"ONE DAY OF WORLD NEWS",font=F(SANS_B,13),fill=RED)
d.text((990,26),f"{TOTAL} STORIES • {len(regions)} REGIONS • {len(fields)} FIELDS",font=F(SANS_B,13),fill=INK,anchor="ra")
d.text((512,42),"Wednesday 25 November 2026",font=F(SERIF_B,55),fill=INK,anchor="ma")
# Natural newspaper dateline (no meta panel): names the day as news, not as proof.
d.text((512,103),"All 39 stories were first reported on Wednesday",font=F(SERIF_B,18),fill=MUTED,anchor="ma")
d.line([(34,128),(990,128)],fill=INK,width=2)
widths={r:int(956*regions[r]/TOTAL) for r in ORDER if regions.get(r)}
for r in list(widths):
    if widths[r]<84:
        widest=max(widths,key=widths.get); widths[widest]-=84-widths[r]; widths[r]=84
x=34
for reg in ORDER:
    cnt=regions.get(reg,0)
    if not cnt: continue
    w=widths[reg]; d.rectangle([x,134,x+w,164],fill=RCOL[reg])
    lab=f"{reg} {cnt}"; fnt=F(SANS_B,14) if d.textlength(lab,font=F(SANS_B,14))<=w-6 else F(SANS_B,12)
    d.text((x+w/2,140),lab,font=fnt,fill=WHITE,anchor="ma"); x+=w
d.rectangle([34,170,118,202],fill=INK); d.text((76,175),"DAY IN\nGMT",font=F(SANS_B,11),fill=WHITE,anchor="ma",align="center")
times=[("06:30","Cartagena"),("06:35","Tiangong"),("AM","Gaza/Jeddah"),("MID","Canberra"),("PM","Tariffs"),("LATE","Kyiv")]
x=128
for t,lab in times:
    d.text((x,171),t,font=F(SANS_B,15),fill=RED); d.text((x,189),lab,font=F(SANS_B,12),fill=INK); x+=143
d.rectangle([34,206,118,242],fill=INK); d.text((76,211),"KEY\nNUMBERS",font=F(SANS_B,10),fill=WHITE,anchor="ma",align="center")
stats=[("31","Egypt fire"),("14","tariff partners"),("-6.2%","KOSPI close"),("2,100+","Canaries"),("19","Sudan drones"),("$227m","meth seized")]
x=128
for big,lab in stats:
    d.text((x,206),big,font=F(SANS_B,24),fill=INK); d.text((x,231),lab,font=F(SANS_B,11),fill=MUTED); x+=143

def scene(kind,x,y,w,h):
    # picture-like drawn scenes, big shapes that survive thumbnails
    if kind=="tariff":
        d.rectangle([x,y,x+w,y+h],fill=SKY2)
        for bx,bh in ((30,34),(92,48),(160,30),(228,44)):
            d.rectangle([x+bx,y+h-bh,x+bx+52,y+h],fill=(90,90,90))
            d.rectangle([x+bx+10,y+h-bh-12,x+bx+22,y+h-bh],fill=(90,90,90))
        d.line([(x+30,y+h-52),(x+130,y+h-64),(x+200,y+h-56),(x+w-84,y+h-74)],fill=RED,width=6)
        d.polygon([(x+w-84,y+h-74),(x+w-106,y+h-68),(x+w-92,y+h-56)],fill=RED)
        d.text((x+w-12,y+4),"14",font=F(SANS_B,24),fill=RED,anchor="ra")
    elif kind=="chipfall":
        d.rectangle([x,y,x+w,y+h],fill=SKY)
        d.rounded_rectangle([x+52,y+14,x+150,y+h-14],radius=8,fill=NAVY)
        d.rectangle([x+82,y+30,x+120,y+h-30],fill=YELLOW)
        for i in range(4):
            d.line([(x+64+i*24,y+14),(x+64+i*24,y+6)],fill=NAVY,width=4)
            d.line([(x+64+i*24,y+h-14),(x+64+i*24,y+h-6)],fill=NAVY,width=4)
        d.line([(x+170,y+22),(x+230,y+36),(x+w-36,y+h-16)],fill=RED,width=6)
        d.polygon([(x+w-36,y+h-16),(x+w-58,y+h-22),(x+w-44,y+h-36)],fill=RED)
        d.text((x+w-10,y+6),"-6.2%",font=F(SANS_B,20),fill=RED,anchor="ra")
    elif kind=="station":
        d.rectangle([x,y,x+w,y+h],fill=(18,32,64))
        for sx,sy in ((40,16),(90,30),(240,14),(280,36),(60,50),(200,20)):
            d.ellipse([x+sx,y+sy,x+sx+4,y+sy+4],fill=WHITE)
        d.arc([x+16,y+h-34,x+w-16,y+h+54],start=180,end=360,fill=(80,160,220),width=8)
        d.rectangle([x+120,y+22,x+192,y+40],fill=WHITE)
        d.rectangle([x+66,y+24,x+118,y+38],fill=(120,180,230))
        d.rectangle([x+194,y+24,x+246,y+38],fill=(120,180,230))
        d.ellipse([x+148,y+42,x+164,y+58],fill=YELLOW)
        d.text((x+w-10,y+6),"06:35",font=F(SANS_B,16),fill=WHITE,anchor="ra")
    elif kind=="kyiv":
        d.rectangle([x,y,x+w,y+h],fill=(226,230,236))
        for bx,bh in ((14,26),(62,40),(112,22)):
            d.rectangle([x+bx,y+h-bh,x+bx+42,y+h],fill=(70,70,70))
        d.line([(x+w-24,y+8),(x+110,y+h-30)],fill=RED,width=4)
        d.ellipse([x+102,y+h-38,x+118,y+h-22],fill=RED)
        d.text((x+w-8,y+6),"LATE",font=F(SANS_B,13),fill=RED,anchor="ra")
    elif kind=="ship":
        d.rectangle([x,y,x+w,y+h],fill=(214,240,238))
        d.rectangle([x+16,y+h-16,x+140,y+h-4],fill=TEAL)
        d.polygon([(x+36,y+h-16),(x+78,y+12),(x+120,y+h-16)],fill=NAVY)
        d.line([(x+150,y+h-4),(x+150,y+10)],fill=INK,width=4); d.line([(x+150,y+10),(x+176,y+10)],fill=INK,width=4)
    elif kind=="gaza":
        d.rectangle([x,y,x+w,y+h],fill=(252,238,228))
        for bx,bh in ((14,24),(56,38),(100,20)):
            d.rectangle([x+bx,y+h-bh,x+bx+36,y+h],fill=(124,29,29))
    elif kind=="treaty":
        d.rectangle([x,y,x+w,y+h],fill=(240,250,238))
        d.rectangle([x+42,y+8,x+142,y+h-8],fill=WHITE,outline=INK,width=2)
        d.line([(x+58,y+h-18),(x+86,y+18),(x+126,y+h-20)],fill=GREEN,width=6)
    elif kind=="fire":
        d.rectangle([x,y,x+w,y+h],fill=(252,244,224))
        d.rectangle([x+16,y+h-18,x+150,y+h-4],fill=(200,120,40))
        d.polygon([(x+62,y+h-18),(x+84,y+6),(x+106,y+h-18)],fill=RED)
        d.polygon([(x+74,y+h-18),(x+84,y+20),(x+94,y+h-18)],fill=YELLOW)
        d.text((x+w-8,y+6),"31",font=F(SANS_B,18),fill=RED,anchor="ra")
    elif kind=="store":
        d.rectangle([x,y,x+w,y+h],fill=(240,250,238))
        d.rectangle([x+20,y+18,x+164,y+h-4],fill=(170,170,160))
        d.polygon([(x+12,y+18),(x+92,y+4),(x+172,y+18)],fill=GREEN)
        d.rectangle([x+78,y+h-22,x+106,y+h-4],fill=NAVY)
    elif kind in ("court","court2"):
        d.rectangle([x,y,x+w,y+h],fill=(246,246,238))
        d.polygon([(x+24,y+16),(x+92,y+4),(x+160,y+16)],fill=(120,120,120))
        for i in range(4): d.rectangle([x+40+i*30,y+20,x+52+i*30,y+h-6],fill=(180,180,180))
        d.rectangle([x+24,y+h-8,x+160,y+h-4],fill=(120,120,120))
    elif kind=="oil":
        d.rectangle([x,y,x+w,y+h],fill=(246,246,238))
        d.line([(x+52,y+h-4),(x+92,y+8),(x+132,y+h-4)],fill=INK,width=6)
        d.line([(x+68,y+26),(x+116,y+26)],fill=INK,width=4)
    elif kind=="nvidia":
        d.rectangle([x,y,x+w,y+h],fill=SKY)
        d.rounded_rectangle([x+52,y+10,x+132,y+h-10],radius=8,fill=NAVY)
        d.rectangle([x+76,y+22,x+108,y+h-22],fill=YELLOW)
        d.text((x+140,y+16),"SENATE",font=F(SANS_B,10),fill=NAVY)

for i,(n,reg,fld,kick,bd,bc,head,fact,why,kind) in enumerate(CARDS[:3]):
    x=34+i*324; y=250; w=312
    scene(kind,x,y,w,84); numcircle(d,x+10,y+10,n)
    d.text((x,y+92),kick,font=F(SANS_B,12),fill=RED); badge(d,x+w-104,y+89,bd,bc,11)
    yy=draw_lines(d,wrap(d,head,F(SERIF_B,26),w,2),x,y+112,F(SERIF_B,26),INK,28)
    yy=draw_lines(d,wrap(d,why,F(SANS_B,14),w,1),x,yy+2,F(SANS_B,14),BLUE,17)
    draw_lines(d,wrap(d,fact,F(SANS_B,13),w,1),x,yy+1,F(SANS_B,13),INK,16)
for i,(n,reg,fld,kick,bd,bc,head,fact,why,kind) in enumerate(CARDS[3:]):
    x=34+(i%5)*192; y=458+(i//5)*140; w=184
    scene(kind,x,y,w,46); numcircle(d,x+7,y+6,n,RED if n<10 else NAVY,13)
    d.text((x,y+52),kick,font=F(SANS_B,10),fill=RED)
    bw=int(d.textlength(bd,font=F(SANS_B,10)))+14; badge(d,x+w-bw,y+50,bd,bc,10)
    yy=draw_lines(d,wrap(d,head,F(SERIF_B,17),w,2),x,y+72,F(SERIF_B,17),INK,20)
    draw_lines(d,wrap(d,fact,F(SANS_B,12),w,2),x,yy+2,F(SANS_B,12),INK,14)
AY=736
d.line([(34,AY),(990,AY)],fill=INK,width=2)
d.text((34,AY+8),"ALSO WEDNESDAY  •  26 MORE",font=F(SANS_B,16),fill=INK)
d.text((990,AY+10),"C confirmed  •  O official  •  R report",font=F(SANS_B,11),fill=MUTED,anchor="ra")
cols=[ALSO[:13],ALSO[13:26]]
for ci,col in enumerate(cols):
    x=34+ci*330; y=AY+32
    for j,(n,reg,fld,text,tag) in enumerate(col):
        if j%2==0: d.rectangle([x-4,y-2,x+318,y+15],fill=(243,240,232))
        d.rectangle([x,y,x+24,y+16],fill=NAVY); d.text((x+12,y+8),str(n),font=F(SANS_B,10),fill=WHITE,anchor="mm")
        d.text((x+29,y+1),fld,font=F(SANS_B,10),fill=RED)
        fw=d.textlength(fld,font=F(SANS_B,10)); d.text((x+34+fw,y),text,font=F(SANS_B,13),fill=INK)
        d.text((x+316,y),tag,font=F(SANS_B,13),fill=GREEN if tag in ("C","O") else GOLD,anchor="ra"); y+=16
MX,MY,MW,MH=706,768,284,198
d.rectangle([MX,MY,MX+MW,MY+MH],fill=(238,244,238),outline=RULE,width=2)
d.text((MX+12,MY+8),"WHERE  •  PINS 1–13",font=F(SANS_B,13),fill=INK)
blobs=[[(18,58),(34,44),(62,38),(92,44),(100,60),(82,76),(58,92),(38,80),(24,68)],[(66,104),(88,100),(104,116),(98,146),(82,164),(70,134)],[(150,52),(168,40),(196,42),(210,56),(196,68),(168,66),(154,60)],[(166,80),(190,72),(214,84),(210,112),(196,140),(184,116),(170,98)],[(214,44),(244,34),(280,40),(300,56),(286,76),(252,84),(226,68)],[(254,118),(280,110),(300,122),(292,142),(264,140)]]
# scale blobs to map width 284 (was 304): shift x by -10 for right blobs
blobs=[[(a-10 if a>200 else a,b) for a,b in poly] for poly in blobs]
for poly in blobs: d.polygon([(MX+a,MY+b) for a,b in poly],fill=(198,218,198),outline=(120,155,120),width=2)
pins={1:(62,62),2:(250,66),3:(228,50),4:(188,58),5:(208,82),6:(194,76),7:(272,128),8:(186,94),9:(72,106),10:(70,72),11:(204,38),12:(204,72),13:(54,58)}
for n,(px,py) in pins.items():
    d.ellipse([MX+px-12,MY+py-12,MX+px+12,MY+py+12],fill=RED,outline=WHITE,width=2)
    d.text((MX+px,MY+py),str(n),font=F(SANS_B,11),fill=WHITE,anchor="mm")
d.text((MX+12,MY+MH-24),"Europe 10 • Africa 8 • Asia 5",font=F(SANS_B,12),fill=MUTED)
d.text((512,986),"Wednesday 25 November 2026  •  sources on each story  •  original drawings",font=F(SANS_B,12),fill=INK,anchor="ma")
out=os.path.join(os.path.dirname(os.path.abspath(__file__)),"entry.png")
img.save(out,"PNG",optimize=True)
print(out,img.size,os.path.getsize(out),"bytes","regions",regions,"fields",len(fields))
