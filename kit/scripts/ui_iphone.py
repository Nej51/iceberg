# realistic iOS-like UI kit
import numpy as np, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
IP='/usr/share/fonts/opentype/inter/'
_fi={}
def FI(size,w='Regular'):
    k=(size,w)
    if k not in _fi: _fi[k]=ImageFont.truetype(IP+f'Inter-{w}.otf',size)
    return _fi[k]
SW,SH=600,1300; BZ=20; BW,BH=SW+2*BZ,SH+2*BZ
BLUE=(0,122,255); IRED=(255,59,48); IGRN=(52,199,89); LGRAY=(242,242,247); SEP=(220,220,225); TXT2=(142,142,147)
def comp(im,lay,xy=(0,0)):
    im.paste(lay,(int(xy[0]),int(xy[1])),lay)
def grad(w,h,c1,c2,horiz=False):
    g=np.linspace(0,1,w if horiz else h)
    g=g[None,:,None] if horiz else g[:,None,None]
    a=np.array(c1,float)*(1-g)+np.array(c2,float)*g
    a=np.broadcast_to(a,(h,w,3)) if True else a
    return Image.fromarray(np.ascontiguousarray(a).astype(np.uint8),'RGB')
def rmask(w,h,r):
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],r,fill=255); return m
# ---------------- icons ----------------
ICBG={'Photos':((255,255,255),(255,255,255)),'Mail':((40,170,255),(14,104,232)),'Messages':((104,240,122),(12,186,50)),
 'Notes':((255,255,255),(250,250,250)),'Téléphone':((104,240,122),(12,186,50)),'Safari':((255,255,255),(226,226,232)),
 'Appareil photo':((230,230,234),(160,160,168)),'Réglages':((150,150,156),(96,96,100)),'Calendrier':((255,255,255),(255,255,255)),
 'Horloge':((20,20,20),(0,0,0)),'Plans':((236,242,226),(214,230,206)),'App Store':((26,196,255),(10,108,230)),
 'Wallet':((24,24,24),(0,0,0)),'Ma Banque':((32,64,140),(12,26,70)),'Contacts':((236,236,238),(200,200,206)),
 'Météo':((70,160,255),(28,96,214)),'Musique':((255,100,124),(250,36,60)),'Localiser':((120,232,120),(40,196,80))}
def make_icon(name,S=96,k=3):
    s=S*k; c1,c2=ICBG[name]; body=grad(s,s,c1,c2).convert('RGBA'); d=ImageDraw.Draw(body,'RGBA')
    P=lambda a:a*s
    if name=='Photos':
        cols=[(255,149,0),(255,204,0),(52,199,89),(48,176,199),(0,122,255),(88,86,214),(175,82,222),(255,45,85)]
        for i,c in enumerate(cols):
            lay=Image.new('RGBA',(s,s),(0,0,0,0)); ld=ImageDraw.Draw(lay)
            ld.ellipse([P(.5)-P(.105),P(.16),P(.5)+P(.105),P(.5)],fill=c+(205,))
            body.alpha_composite(lay.rotate(-i*45,center=(s/2,s/2),resample=Image.BICUBIC))
    elif name=='Mail':
        d.rounded_rectangle([P(.16),P(.28),P(.84),P(.72)],P(.05),fill='white')
        d.line([(P(.18),P(.31)),(P(.5),P(.54)),(P(.82),P(.31))],fill=(30,140,245),width=int(P(.035)),joint='curve')
    elif name in ('Messages',):
        d.ellipse([P(.15),P(.2),P(.85),P(.72)],fill='white'); d.polygon([(P(.27),P(.6)),(P(.19),P(.8)),(P(.42),P(.68))],fill='white')
    elif name=='Notes':
        d.rectangle([0,0,s,P(.27)],fill=(255,204,0)); d.line([(0,P(.27)),(s,P(.27))],fill=(230,180,0),width=int(P(.01)))
        for y in (.44,.6,.76): d.line([(P(.12),P(y)),(P(.88),P(y))],fill=(212,212,218),width=int(P(.022)))
    elif name=='Téléphone':
        lay=Image.new('RGBA',(s,s),(0,0,0,0)); ld=ImageDraw.Draw(lay)
        ld.arc([P(.22),P(.22),P(.78),P(.78)],105,255,fill='white',width=int(P(.13)))
        for a in (105,255):
            ex=P(.5)+P(.215)*math.cos(math.radians(a)); ey=P(.5)+P(.215)*math.sin(math.radians(a)); ld.ellipse([ex-P(.1),ey-P(.075),ex+P(.1),ey+P(.075)],fill='white')
        body.alpha_composite(lay.rotate(-45,center=(s/2,s/2),resample=Image.BICUBIC))
    elif name=='Safari':
        d.ellipse([P(.1),P(.1),P(.9),P(.9)],fill=(28,140,252))
        for a in range(0,360,15):
            r1,r2=P(.36),P(.39); ca,sa=math.cos(math.radians(a)),math.sin(math.radians(a))
            d.line([(s/2+r1*ca,s/2+r1*sa),(s/2+r2*ca,s/2+r2*sa)],fill=(220,235,255),width=int(P(.012)))
        d.polygon([(P(.5)+P(.06),P(.5)+P(.06)),(P(.72),P(.28)),(P(.5)-P(.06),P(.5)-P(.06))],fill=(255,59,48))
        d.polygon([(P(.5)+P(.06),P(.5)+P(.06)),(P(.28),P(.72)),(P(.5)-P(.06),P(.5)-P(.06))],fill='white')
    elif name=='Appareil photo':
        d.rounded_rectangle([P(.13),P(.3),P(.87),P(.76)],P(.08),fill=(42,42,46)); d.rounded_rectangle([P(.36),P(.23),P(.64),P(.32)],P(.03),fill=(42,42,46))
        d.ellipse([P(.34),P(.37),P(.66),P(.69)],fill=(120,120,128)); d.ellipse([P(.4),P(.43),P(.6),P(.63)],fill=(20,20,24))
    elif name=='Réglages':
        pts=[]
        for i in range(48):
            a=2*math.pi*i/48; r=P(.38) if (i//2)%2==0 else P(.31); pts.append((s/2+r*math.cos(a),s/2+r*math.sin(a)))
        d.polygon(pts,fill=(70,70,74)); d.ellipse([P(.5)-P(.22),P(.5)-P(.22),P(.5)+P(.22),P(.5)+P(.22)],fill=(170,170,176))
        d.ellipse([P(.5)-P(.09),P(.5)-P(.09),P(.5)+P(.09),P(.5)+P(.09)],fill=(70,70,74))
    elif name=='Calendrier':
        d.text((P(.5),P(.24)),'JEUDI',font=FI(int(P(.15)),'SemiBold'),fill=(255,59,48),anchor='mm')
        d.text((P(.5),P(.62)),'12',font=FI(int(P(.48)),'Regular'),fill=(20,20,20),anchor='mm')
    elif name=='Horloge':
        d.ellipse([P(.08),P(.08),P(.92),P(.92)],fill='white')
        for i in range(12):
            a=2*math.pi*i/12; d.line([(s/2+P(.33)*math.cos(a),s/2+P(.33)*math.sin(a)),(s/2+P(.38)*math.cos(a),s/2+P(.38)*math.sin(a))],fill=(30,30,30),width=int(P(.02)))
        d.line([(s/2,s/2),(s/2+P(.16),s/2-P(.12))],fill='black',width=int(P(.04))); d.line([(s/2,s/2),(s/2-P(.04),s/2-P(.3))],fill='black',width=int(P(.03)))
        d.line([(s/2,s/2),(s/2-P(.2),s/2+P(.22))],fill=(255,140,0),width=int(P(.015)))
    elif name=='Plans':
        d.polygon([(0,P(.62)),(P(.4),0),(P(.62),0),(0,P(.95))],fill=(255,255,255)); d.polygon([(P(.45),s),(s,P(.35)),(s,P(.6)),(P(.7),s)],fill=(255,214,90))
        d.line([(P(.25),P(.8)),(P(.55),P(.5)),(P(.75),P(.28))],fill=(0,122,255),width=int(P(.06)),joint='curve'); d.ellipse([P(.66),P(.18),P(.84),P(.36)],fill=(255,59,48))
    elif name=='App Store':
        w_=int(P(.07)); d.line([(P(.5),P(.2)),(P(.27),P(.72))],fill='white',width=w_); d.line([(P(.5),P(.2)),(P(.73),P(.72))],fill='white',width=w_); d.line([(P(.22),P(.58)),(P(.78),P(.58))],fill='white',width=w_)
    elif name=='Wallet':
        for i,c in enumerate([(30,120,255),(255,160,0),(52,199,89),(255,59,48)]):
            d.rounded_rectangle([P(.16),P(.22+i*.1),P(.84),P(.5+i*.1)],P(.05),fill=c)
    elif name=='Ma Banque':
        d.text((P(.5),P(.5)),'€',font=FI(int(P(.56)),'Bold'),fill='white',anchor='mm')
    elif name=='Contacts':
        d.ellipse([P(.36),P(.2),P(.64),P(.48)],fill=(150,150,156)); d.ellipse([P(.2),P(.52),P(.8),P(1.0)],fill=(150,150,156))
    elif name=='Météo':
        d.ellipse([P(.42),P(.14),P(.8),P(.52)],fill=(255,214,10))
        for (x0,y0,x1,y1) in ((.14,.46,.52,.78),(.36,.36,.76,.76),(.56,.5,.88,.8)): d.ellipse([P(x0),P(y0),P(x1),P(y1)],fill='white')
        d.rectangle([P(.3),P(.62),P(.72),P(.8)],fill='white')
    elif name=='Musique':
        d.ellipse([P(.26),P(.6),P(.46),P(.78)],fill='white'); d.ellipse([P(.56),P(.52),P(.76),P(.7)],fill='white')
        d.line([(P(.44),P(.68)),(P(.44),P(.28))],fill='white',width=int(P(.05))); d.line([(P(.74),P(.6)),(P(.74),P(.2))],fill='white',width=int(P(.05)))
        d.polygon([(P(.42),P(.26)),(P(.76),P(.18)),(P(.76),P(.3)),(P(.42),P(.38))],fill='white')
    elif name=='Localiser':
        for r,a in ((.36,90),(.25,140)): d.ellipse([P(.5-r),P(.5-r),P(.5+r),P(.5+r)],outline=(255,255,255,a),width=int(P(.04)))
        d.ellipse([P(.42),P(.42),P(.58),P(.58)],fill='white')
    out=Image.new('RGBA',(s,s),(0,0,0,0)); out.paste(body,(0,0),rmask(s,s,int(s*.225)))
    return out.resize((S,S),Image.LANCZOS)
ICONS={}
def icon(name,S=96):
    k=(name,S)
    if k not in ICONS: ICONS[k]=make_icon(name,S)
    return ICONS[k]
# ---------------- wallpaper / home ----------------
def wallpaper():
    rng=np.random.default_rng(7); yy,xx=np.mgrid[0:SH,0:SW]
    img=np.zeros((SH,SW,3)); img[:]=np.array([18,20,60])
    for (cx,cy,r,c) in [(120,250,420,(90,60,200)),(520,520,460,(30,110,220)),(200,1000,520,(200,70,140)),(560,1180,380,(255,140,80))]:
        w=np.exp(-((xx-cx)**2+(yy-cy)**2)/(2*r*r*0.35))[...,None]; img=img*(1-w*0.85)+np.array(c)*w*0.85
    return Image.fromarray(img.clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(30))
COLS=[44,182,320,458]; ROWY=[430,585,740]
LAYOUT={'Photos':(0,0),'Appareil photo':(1,0),'Mail':(2,0),'Notes':(3,0),'Horloge':(0,1),'Plans':(1,1),'Réglages':(2,1),'App Store':(3,1),
        'Wallet':(0,2),'Ma Banque':(1,2),'Contacts':(2,2),'Météo':(3,2)}
DOCK=['Téléphone','Safari','Messages','Musique']; DOCKY=1144
def icon_xy(name):
    if name in DOCK: return COLS[DOCK.index(name)],DOCKY
    c,r=LAYOUT[name]; return COLS[c],ROWY[r]
def icon_center(name):
    x,y=icon_xy(name); return x+48,y+48
def statusbar(d,dark=False,time='9:41'):
    col=(0,0,0) if dark else (255,255,255)
    d.text((112,50),time,font=FI(31,'SemiBold'),fill=col,anchor='mm')
    for i in range(4): d.rounded_rectangle([420+i*11,58-8-i*5,420+i*11+7,58],2,fill=col)
    for i,r in enumerate((22,15,8)): d.arc([486-r,60-r,486+r,60+r],225,315,fill=col,width=5)
    d.rounded_rectangle([510,40,556,62],7,outline=col,width=3); d.rounded_rectangle([514,44,546,58],4,fill=col); d.rectangle([558,47,561,55],fill=col)
def island(d): d.rounded_rectangle([SW/2-64,20,SW/2+64,62],21,fill=(0,0,0))
def homebar(d,dark=False): d.rounded_rectangle([SW/2-70,1278,SW/2+70,1287],5,fill=(0,0,0) if dark else (255,255,255))
WALL=None
def build_home():
    global WALL
    WALL=wallpaper(); im=WALL.copy(); d=ImageDraw.Draw(im,'RGBA')
    # widgets
    wg=grad(250,250,(70,150,255),(30,90,210)).convert('RGBA'); im.paste(wg,(42,140),rmask(250,250,40))
    d.text((66,172),'Paris',font=FI(26,'SemiBold'),fill='white'); d.text((62,198),'11°',font=FI(80,'Regular'),fill='white')
    d.ellipse([66,300,96,330],fill=(255,214,10)); d.text((66,342),'Nuageux',font=FI(22,'SemiBold'),fill='white')
    d.rounded_rectangle([308,140,558,390],40,fill=(255,255,255,245))
    d.text((334,172),'JEUDI',font=FI(24,'SemiBold'),fill=(255,59,48)); d.text((330,196),'12',font=FI(92,'Regular'),fill=(20,20,20))
    d.text((334,330),'Aucun évènement',font=FI(21,'Regular'),fill=TXT2)
    labf=FI(20,'Medium')
    for n,(c,r) in LAYOUT.items():
        x,y=COLS[c],ROWY[r]; comp(im,icon(n),(x,y))
        d.text((x+48+1,y+118+1),n,font=labf,fill=(0,0,0,120),anchor='mm'); d.text((x+48,y+118),n,font=labf,fill='white',anchor='mm')
    d.rounded_rectangle([SW/2-82,1030,SW/2+82,1076],23,fill=(255,255,255,70))
    d.ellipse([SW/2-70,1043,SW/2-54,1059],outline='white',width=3); d.line([(SW/2-57,1057),(SW/2-50,1064)],fill='white',width=3)
    d.text((SW/2+18,1053),'Rechercher',font=FI(20,'SemiBold'),fill='white',anchor='mm')
    dock=WALL.crop((22,1118,578,1270)).filter(ImageFilter.GaussianBlur(14)); im.paste(dock,(22,1118),rmask(556,152,52))
    d.rounded_rectangle([22,1118,578,1270],52,fill=(255,255,255,55))
    for n in DOCK: x,y=icon_xy(n); comp(im,icon(n),(x,y))
    island(d); statusbar(d); homebar(d)
    return im
HOME=None; HOME_BLUR=None
def init():
    global HOME,HOME_BLUR
    HOME=build_home(); HOME_BLUR=HOME.filter(ImageFilter.GaussianBlur(16))
    ov=Image.new('RGBA',HOME.size,(0,0,0,70)); comp(HOME_BLUR,ov)
# ---------------- widgets ----------------
def touch(im,x,y,press=0.0,alpha=1.0):
    lay=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    r=34*(1-0.12*min(1,press*4))
    d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255,int(120*alpha)),outline=(255,255,255,int(220*alpha)),width=4)
    if press>0:
        R=r+10+40*press; d.ellipse([x-R,y-R,x+R,y+R],outline=(255,255,255,int(200*alpha*(1-press*0.6))),width=6)
    comp(im,lay)
def menu(im,x,y,items,hi=None,pressed=None,k=1.0,w=410,dark=False):
    """items: list of str or ('-') ; str starting with '!' = red ; '*' = faceid icon"""
    if k<=0.02: return
    ih=64; h=sum(10 if it=='-' else ih for it in items)
    lay=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.rounded_rectangle([0,0,w-1,h-1],26,fill=(246,246,248,245)); yy=0
    for i,it in enumerate(items):
        if it=='-': d.rectangle([0,yy,w,yy+10],fill=(222,222,228)); yy+=10; continue
        txt=it.lstrip('!*'); col=IRED if it.startswith('!') else (0,0,0)
        if i==pressed: d.rectangle([0,yy,w,yy+ih],fill=(214,214,220))
        d.text((24,yy+ih/2),txt,font=FI(25,'Regular'),fill=col,anchor='lm')
        if it.startswith('*'): faceid_glyph(d,w-44,yy+ih/2,13,(0,0,0))
        if i<len(items)-1 and items[i+1]!='-': d.line([(0,yy+ih),(w,yy+ih)],fill=(214,214,220),width=1)
        yy+=ih
    m=rmask(w,h,26); lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay.split()[3]),np.asarray(m))))
    if k<1:
        lay=lay.resize((max(2,int(w*k)),max(2,int(h*k))),Image.BILINEAR)
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([x,y+10,x+lay.width,y+lay.height+10],26,fill=(0,0,0,70))
    comp(im,sh.filter(ImageFilter.GaussianBlur(14))); comp(im,lay,(int(x),int(y)))
    return h
def menu_item_y(items,idx):
    yy=0
    for i,it in enumerate(items):
        if i==idx: return yy+32
        yy+=10 if it=='-' else 64
def wrap(d,text,font,maxw):
    words=text.split(); lines=['']
    for w_ in words:
        t=(lines[-1]+' '+w_).strip()
        if d.textlength(t,font=font)<=maxw: lines[-1]=t
        else: lines.append(w_)
    return lines
def alert(im,title,msg,buttons,pressed=None,k=1.0,w=440):
    if k<=0.02: return None
    tmp=ImageDraw.Draw(im); tl=wrap(tmp,title,FI(29,'SemiBold'),w-60); ml=wrap(tmp,msg,FI(22,'Regular'),w-60)
    h=40+len(tl)*38+12+len(ml)*30+28+len(buttons)*76
    lay=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.rounded_rectangle([0,0,w-1,h-1],32,fill=(248,248,250,248)); y=40
    for l in tl: d.text((w/2,y+16),l,font=FI(29,'SemiBold'),fill='black',anchor='mm'); y+=38
    y+=12
    for l in ml: d.text((w/2,y+13),l,font=FI(22,'Regular'),fill=(60,60,67),anchor='mm'); y+=30
    y+=28; boxes=[]
    for i,b in enumerate(buttons):
        d.line([(0,y),(w,y)],fill=(206,206,212),width=2)
        if i==pressed: d.rectangle([0,y+1,w,y+76],fill=(220,220,226))
        d.text((w/2,y+38),b.lstrip('!'),font=FI(28,'SemiBold' if i==0 else 'Regular'),fill=IRED if b.startswith('!') else BLUE,anchor='mm'); boxes.append(y); y+=76
    lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay.split()[3]),np.asarray(rmask(w,h,32)))))
    x0=(SW-w)/2; y0=(SH-h)/2
    if k<1:
        lay=lay.resize((max(2,int(w*k)),max(2,int(h*k))),Image.BILINEAR); x0=(SW-lay.width)/2; y0=(SH-lay.height)/2
    comp(im,lay,(int(x0),int(y0)))
    return [(SW/2,y0+(b+38)) for b in boxes]
def faceid_glyph(d,cx,cy,r,col,width=None):
    w_=width or max(2,int(r*0.16)); c=r*0.42
    for sx in (-1,1):
        for sy in (-1,1):
            x=cx+sx*r; y=cy+sy*r
            d.line([(x,y-sy*c),(x,y)],fill=col,width=w_); d.line([(x,y),(x-sx*c,y)],fill=col,width=w_)
    d.line([(cx-r*.38,cy-r*.32),(cx-r*.38,cy-r*.12)],fill=col,width=w_); d.line([(cx+r*.38,cy-r*.32),(cx+r*.38,cy-r*.12)],fill=col,width=w_)
    d.line([(cx,cy-r*.3),(cx,cy+r*.12),(cx-r*.12,cy+r*.12)],fill=col,width=w_)
    d.arc([cx-r*.42,cy-r*.05,cx+r*.42,cy+r*.48],30,150,fill=col,width=w_)
def faceid_hud(im,state,u):
    """state: 'scan','ok','fail' ; centered rounded HUD"""
    lay=Image.new('RGBA',(220,220),(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.rounded_rectangle([0,0,219,219],44,fill=(40,40,44,235))
    if state=='ok':
        k=min(1,u*3); d.ellipse([110-62*k,104-62*k,110+62*k,104+62*k],outline=(255,255,255),width=8)
        if k>0.6: d.line([(80,106),(102,128),(142,84)],fill='white',width=10,joint='curve')
        d.text((110,190),'Face ID',font=FI(22,'SemiBold'),fill='white',anchor='mm')
    else:
        dx=math.sin(u*60)*12 if state=='fail' else 0; col=(255,90,80) if state=='fail' else (255,255,255)
        pul=1+0.06*math.sin(u*20) if state=='scan' else 1
        faceid_glyph(d,110+dx,100,56*pul,col,8)
        d.text((110,190),'Face ID' if state=='scan' else 'Non reconnu',font=FI(22,'SemiBold'),fill=col,anchor='mm')
    comp(im,lay,(int(SW/2-110),540))
def lockbadge(d,cx,cy,r=20,bg=(255,255,255),fg=(0,0,0)):
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=bg)
    d.arc([cx-r*.38,cy-r*.66,cx+r*.38,cy+r*.06],180,360,fill=fg,width=max(2,int(r*.16)))
    d.line([(cx-r*.38,cy-r*.3),(cx-r*.38,cy-r*.04)],fill=fg,width=max(2,int(r*.16))); d.line([(cx+r*.38,cy-r*.3),(cx+r*.38,cy-r*.04)],fill=fg,width=max(2,int(r*.16)))
    d.rounded_rectangle([cx-r*.52,cy-r*.08,cx+r*.52,cy+r*.55],max(1,r*.12),fill=fg)
# ---------------- app screens ----------------
def nav_light(im,title,big=True,back=None):
    d=ImageDraw.Draw(im,'RGBA'); island(d); statusbar(d,dark=True)
    if back: d.text((30,118),'‹ '+back,font=FI(28,'Regular'),fill=BLUE,anchor='lm')
    if big: d.text((30,190),title,font=FI(46,'Bold'),fill='black',anchor='lm')
    return d
def keyboard(im,y0=860):
    d=ImageDraw.Draw(im,'RGBA'); d.rectangle([0,y0,SW,SH],fill=(209,212,219))
    rows_=['azertyuiop','qsdfghjklm','wxcvbn']; kw=52
    for r,row in enumerate(rows_):
        n=len(row); x0=(SW-(n*kw+(n-1)*6))/2 if r<2 else 120
        for i,ch in enumerate(row):
            x=x0+i*(kw+6); y=y0+16+r*92; d.rounded_rectangle([x,y,x+kw,y+78],10,fill='white'); d.text((x+kw/2,y+39),ch,font=FI(30),fill='black',anchor='mm')
    d.rounded_rectangle([150,y0+300,450,y0+378],10,fill='white'); d.text((300,y0+339),'espace',font=FI(24),fill='black',anchor='mm')
    homebar(d,True)
def scr_conversation(typed='',cursor=True):
    im=Image.new('RGB',(SW,SH),(255,255,255)); d=ImageDraw.Draw(im,'RGBA')
    d.rectangle([0,0,SW,250],fill=(248,248,248)); island(d); statusbar(d,True)
    d.ellipse([SW/2-44,100,SW/2+44,188],fill=(170,170,178)); d.text((SW/2,144),'S',font=FI(42,'SemiBold'),fill='white',anchor='mm')
    d.text((SW/2,216),'Sarah ›',font=FI(22,'Regular'),fill='black',anchor='mm'); d.line([(0,250),(SW,250)],fill=SEP)
    def bub(txt,right,y):
        f=FI(28); w=d.textlength(txt,font=f)+44
        x0=SW-24-w if right else 24
        d.rounded_rectangle([x0,y,x0+w,y+64],32,fill=BLUE if right else (233,233,235)); d.text((x0+22,y+32),txt,font=f,fill='white' if right else 'black',anchor='lm')
    bub('Tu arrives quand ?',False,320); bub('Dans 5 min',True,410); bub('Je suis à la gare',False,500)
    d.rounded_rectangle([24,780,SW-24,840],30,outline=(200,200,206),width=2,fill='white')
    d.text((48,810),typed+('|' if cursor else ''),font=FI(26),fill='black' if typed else TXT2,anchor='lm')
    keyboard(im,860); return im
THUMBS=None
def build_thumbs():
    global THUMBS; rnd=random.Random(5); T=[]
    for i in range(21):
        a=rnd.choice([((255,170,90),(255,90,120)),((120,200,255),(40,110,220)),((255,220,150),(250,160,60)),((150,230,170),(60,160,110)),((200,170,255),(110,80,200)),((250,240,230),(220,200,180))])
        im=grad(196,196,*a).convert('RGBA'); d=ImageDraw.Draw(im,'RGBA'); k=rnd.random()
        if k<0.35: d.ellipse([120,30,170,80],fill=(255,240,200)); d.polygon([(0,196),(70,110),(140,170),(196,120),(196,196)],fill=(40,60,70,220))
        elif k<0.65: d.rectangle([0,130,196,196],fill=(240,220,180)); d.rectangle([0,105,196,130],fill=(40,140,200))
        else: d.ellipse([60,60,136,136],fill=(255,255,255,90)); d.ellipse([78,40,118,80],fill=(255,220,190)); d.rounded_rectangle([62,84,134,170],30,fill=(255,255,255,170))
        T.append(im)
    T[4]=idcard_img(196,196,True); T[7]=rib_img(196,196); THUMBS=T
def idcard(w,h):
    im=grad(w,h,(232,240,250),(200,218,240)).convert('RGBA'); d=ImageDraw.Draw(im,'RGBA'); k=w/520
    d.rectangle([0,0,w,48*k],fill=(30,70,150)); d.text((20*k,24*k),"CARTE D'IDENTITÉ",font=FI(int(26*k),'Bold'),fill='white',anchor='lm')
    d.rounded_rectangle([22*k,70*k,160*k,250*k],10*k,fill=(170,180,196)); d.ellipse([60*k,92*k,122*k,160*k],fill=(120,130,150)); d.ellipse([38*k,165*k,144*k,280*k],fill=(120,130,150))
    d.rectangle([22*k,250*k,160*k,262*k],fill=(232,240,250))
    for i,(a,b) in enumerate((('NOM','DUPONT'),('PRÉNOM','Camille'),('NÉE LE','14.03.1996'),('N°','X4F7 82K1'))):
        y=(78+i*44)*k; d.text((182*k,y),a,font=FI(int(15*k),'SemiBold'),fill=(90,100,120)); d.text((182*k,y+16*k),b,font=FI(int(22*k),'SemiBold'),fill=(20,30,50))
    d.rectangle([0,h-50*k,w,h],fill=(214,224,236)); d.text((20*k,h-25*k),'IDFRADUPONT<<<<<<<<<<<<<',font=FI(int(18*k),'Medium'),fill=(80,90,110),anchor='lm')
    return im
def idcard_img(w,h,thumb=False):
    im=Image.new('RGBA',(w,h),(60,64,72,255)); c=idcard(int(w*0.9),int(w*0.9*0.63)); comp(im,c,(int(w*0.05),int((h-c.height)/2))); return im
def rib_img(w,h):
    im=Image.new('RGBA',(w,h),(90,84,76,255)); d=ImageDraw.Draw(im); d.rectangle([22,14,w-22,h-14],fill=(250,250,248))
    d.text((34,32),'RIB',font=FI(26,'Bold'),fill=(20,20,20))
    for i in range(6): d.line([(34,80+i*16),(w-34-(i%3)*20,80+i*16)],fill=(170,170,170),width=4)
    return im
def scr_photos_grid(hide_id=0.0,hl=None,t=0):
    im=Image.new('RGB',(SW,SH),(255,255,255)); nav_light(im,'Photothèque')
    d=ImageDraw.Draw(im,'RGBA'); d.text((30,234),'2 438 photos',font=FI(20),fill=TXT2,anchor='lm')
    order=list(range(21))
    pos=[]; idx=0
    for i in order:
        if i in (4,7) and hide_id>=1: continue
        pos.append(i)
    for j,i in enumerate(pos):
        x=(j%3)*201; y=262+(j//3)*201
        if y>SH-140: break
        th=THUMBS[i]
        if i in (4,7) and hide_id>0:
            s=max(2,int(196*(1-hide_id))); th=th.resize((s,s)); comp(im,th,(int(x+98-s/2),int(y+98-s/2))); continue
        comp(im,th,(x,y))
        if hl and i in hl:
            p=0.5+0.5*math.sin(t*12); d.rectangle([x+3,y+3,x+193,y+193],outline=(255,59,48),width=int(5+3*p))
    d.rectangle([0,SH-120,SW,SH],fill=(255,255,255,235)); d.rounded_rectangle([150,SH-104,450,SH-44],30,fill=(236,236,240))
    d.rounded_rectangle([156,SH-98,300,SH-50],24,fill='white'); d.text((228,SH-74),'Photothèque',font=FI(19,'SemiBold'),fill='black',anchor='mm'); d.text((375,SH-74),'Collections',font=FI(19),fill='black',anchor='mm')
    homebar(d,True); return im
def grid_pos(i):
    return (i%3)*201+98, 262+(i//3)*201+98
def scr_photo_full(k=1.0):
    im=Image.new('RGB',(SW,SH),(0,0,0)); d=ImageDraw.Draw(im,'RGBA')
    c=idcard(560,353)
    if k<1:
        w=int(196+(560-196)*k); c=c.resize((w,int(w*0.63))); gx,gy=grid_pos(4); cx=gx*(1-k)+300*k; cy=gy*(1-k)+650*k
    else: cx,cy=300,650
    comp(im,c,(int(cx-c.width/2),int(cy-c.height/2)))
    if k>=1:
        island(d); statusbar(d)
        d.ellipse([22,92,86,156],fill=(60,60,64)); d.text((54,122),'‹',font=FI(44,'Regular'),fill='white',anchor='mm')
        d.ellipse([SW-86,92,SW-22,156],fill=(60,60,64))
        for i in (-1,0,1): d.ellipse([SW-54+i*14-4,120,SW-54+i*14+4,128],fill='white')
        d.text((SW/2,112),'Aujourd’hui',font=FI(24,'SemiBold'),fill='white',anchor='mm'); d.text((SW/2,140),'09:12',font=FI(19),fill=(200,200,200),anchor='mm')
        homebar(d)
    return im
def sheet(im,msg,btn,pressed=False,k=1.0):
    if k<=0: return None
    d=ImageDraw.Draw(im,'RGBA'); ov=Image.new('RGBA',im.size,(0,0,0,int(90*k))); comp(im,ov)
    y0=SH-330+(1-k)*330
    d=ImageDraw.Draw(im,'RGBA'); d.rounded_rectangle([16,y0,SW-16,y0+190],28,fill=(248,248,250,250))
    for i,l in enumerate(wrap(d,msg,FI(21),SW-90)): d.text((SW/2,y0+40+i*28),l,font=FI(21),fill=(110,110,116),anchor='mm')
    d.line([(16,y0+112),(SW-16,y0+112)],fill=SEP,width=2)
    if pressed: d.rectangle([16,y0+113,SW-16,y0+188],fill=(222,222,228))
    d.text((SW/2,y0+151),btn,font=FI(28,'Regular'),fill=BLUE,anchor='mm')
    d.rounded_rectangle([16,y0+204,SW-16,y0+280],28,fill='white'); d.text((SW/2,y0+242),'Annuler',font=FI(28,'SemiBold'),fill=BLUE,anchor='mm')
    return (SW/2,y0+151)
def scr_collections(hl=False,t=0):
    im=Image.new('RGB',(SW,SH),(242,242,247)); nav_light(im,'Collections'); d=ImageDraw.Draw(im,'RGBA')
    d.text((30,262),'Utilitaires',font=FI(30,'Bold'),fill='black',anchor='lm')
    rows_=[('Importations',False),('Doublons',False),('Masquées',True),('Supprimés récemment',True),('Captures d’écran',False)]
    d.rounded_rectangle([20,300,SW-20,300+len(rows_)*84],22,fill='white')
    for i,(n,lk) in enumerate(rows_):
        y=300+i*84
        if hl and n=='Masquées': d.rectangle([20,y,SW-20,y+84],fill=(225,236,255))
        d.rounded_rectangle([40,y+20,84,y+64],10,fill=(0,122,255,40)); d.ellipse([52,y+32,72,y+52],outline=BLUE,width=3)
        if n=='Masquées': d.line([(46,y+60),(78,y+24)],fill=BLUE,width=3)
        d.text((104,y+42),n,font=FI(27,'SemiBold' if n=='Masquées' else 'Regular'),fill='black',anchor='lm')
        if lk: lockbadge(d,SW-110,y+42,16,(255,255,255),(142,142,147))
        d.text((SW-50,y+42),'›',font=FI(34),fill=(196,196,200),anchor='mm')
        if i<len(rows_)-1: d.line([(104,y+84),(SW-20,y+84)],fill=SEP)
    if hl:
        p=0.5+0.5*math.sin(t*12); d.rounded_rectangle([14,300+2*84-6,SW-14,300+3*84+6],16,outline=(255,59,48),width=int(5+3*p))
    homebar(d,True); return im
def scr_mail(t=0):
    im=Image.new('RGB',(SW,SH),(255,255,255)); nav_light(im,'Boîte de réception',back='Boîtes'); d=ImageDraw.Draw(im,'RGBA')
    mails=[('Ma Banque','Votre relevé est disponible','Consultez vos comptes en ligne…'),('Compte e-mail','Activité de connexion','Nouvelle connexion détectée…'),('Boutique','Votre commande est expédiée','Suivez votre colis…'),('Assurance','Votre attestation','Retrouvez votre document…'),('Impôts','Votre avis est disponible','Connectez-vous à votre espace…'),('Streaming','Ton abonnement','Merci de ta fidélité…')]
    for i,(a,b,c) in enumerate(mails):
        y=240+i*150; d.ellipse([22,y+22,36,y+36],fill=BLUE)
        d.text((50,y+28),a,font=FI(27,'SemiBold'),fill='black',anchor='lm'); d.text((SW-28,y+28),'09:0'+str(i),font=FI(20),fill=TXT2,anchor='rm')
        d.text((50,y+66),b,font=FI(23,'Medium'),fill='black',anchor='lm'); d.text((50,y+100),c,font=FI(21),fill=TXT2,anchor='lm')
        d.line([(50,y+140),(SW,y+140)],fill=SEP)
    homebar(d,True); return im
def login_card(im,k,pressed,title='Ma Banque'):
    if k<=0: return None
    w,h=500,420; lay=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.rounded_rectangle([0,0,w-1,h-1],30,fill=(255,255,255,252),outline=(220,220,226),width=2)
    d.text((w/2,58),title,font=FI(32,'Bold'),fill=(20,40,90),anchor='mm'); d.text((w/2,100),'Se connecter',font=FI(22),fill=TXT2,anchor='mm')
    for i,lab in enumerate(('Identifiant','Mot de passe')):
        d.rounded_rectangle([40,140+i*86,w-40,206+i*86],14,outline=(200,200,206),width=2); d.text((60,173+i*86),lab,font=FI(22),fill=TXT2,anchor='lm')
    if pressed: d.rounded_rectangle([70,330,w-70,390],14,fill=(255,230,230))
    d.text((w/2,360),'Mot de passe oublié ?',font=FI(26,'SemiBold'),fill=IRED if pressed else BLUE,anchor='mm')
    if k<1: lay=lay.resize((max(2,int(w*k)),max(2,int(h*k))))
    comp(im,lay,(int(SW/2-lay.width/2),int(560-lay.height/2)))
    return (SW/2,560-210+360)
def scr_messages_list():
    im=Image.new('RGB',(SW,SH),(255,255,255)); nav_light(im,'Messages'); d=ImageDraw.Draw(im,'RGBA')
    for i,(n,m) in enumerate((('Sarah','Dans 5 min'),('Maman','Bisous, à dimanche'),('Ma Banque','Votre code…'),('Livreur','Colis déposé'),('Léo','Ok ça marche'))):
        y=240+i*130; d.ellipse([24,y+20,104,y+100],fill=(170,170,178)); d.text((64,y+60),n[0],font=FI(34,'SemiBold'),fill='white',anchor='mm')
        d.text((124,y+42),n,font=FI(27,'SemiBold'),fill='black',anchor='lm'); d.text((124,y+80),m,font=FI(22),fill=TXT2,anchor='lm'); d.line([(124,y+126),(SW,y+126)],fill=SEP)
    homebar(d,True); return im
def banner(im,y,k,title,body,app='Messages'):
    if k<=0: return
    w=SW-32; lay=Image.new('RGBA',(w,124),(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.rounded_rectangle([0,0,w-1,123],30,fill=(250,250,252,250),outline=(225,225,230),width=2)
    lay.alpha_composite(icon(app,56),(18,34)); d.text((92,40),title,font=FI(24,'SemiBold'),fill='black',anchor='lm'); d.text((w-24,40),'maintenant',font=FI(18),fill=TXT2,anchor='rm')
    d.text((92,82),body,font=FI(24,'Regular'),fill='black',anchor='lm')
    sh=Image.new('RGBA',im.size,(0,0,0,0)); yy=y-(1-k)*160
    ImageDraw.Draw(sh).rounded_rectangle([16,yy+8,16+w,yy+132],30,fill=(0,0,0,int(60*k))); comp(im,sh.filter(ImageFilter.GaussianBlur(10)))
    if k<1: lay.putalpha(Image.fromarray((np.asarray(lay.split()[3])*k).astype(np.uint8)))
    comp(im,lay,(16,int(yy)))
def scr_locked_app(name,state,u,msg=None):
    im=HOME_BLUR.copy(); d=ImageDraw.Draw(im,'RGBA'); d.rectangle([0,0,SW,SH],fill=(0,0,0,90))
    comp(im,icon(name,130),(SW//2-65,200)); lockbadge(d,SW/2+58,320,26,(255,255,255),(0,0,0))
    d.text((SW/2,400),f'« {name} » est verrouillée',font=FI(30,'SemiBold'),fill='white',anchor='mm')
    d.text((SW/2,442),msg or 'Utilise Face ID pour ouvrir',font=FI(23),fill=(220,220,226),anchor='mm')
    faceid_hud(im,state,u); d=ImageDraw.Draw(im,'RGBA')
    d.rounded_rectangle([SW/2-150,1050,SW/2+150,1112],31,fill=(255,255,255,60)); d.text((SW/2,1081),'Saisir le code',font=FI(24,'SemiBold'),fill='white',anchor='mm')
    island(d); statusbar(d); return im
KP=[('1',''),('2','ABC'),('3','DEF'),('4','GHI'),('5','JKL'),('6','MNO'),('7','PQRS'),('8','TUV'),('9','WXYZ'),None,('0',''),None]
def kp_pos(i): return SW/2+(i%3-1)*170, 560+(i//3)*170
def scr_passcode(n,shake=0.0,lit=None,err=False):
    im=HOME_BLUR.copy(); d=ImageDraw.Draw(im,'RGBA'); d.rectangle([0,0,SW,SH],fill=(0,0,0,110))
    island(d); statusbar(d); lockbadge(d,SW/2,190,22,(0,0,0,0),(255,255,255))
    d.text((SW/2,270),'Code incorrect' if err else 'Saisir le code',font=FI(32,'Regular'),fill='white',anchor='mm')
    dx=math.sin(shake*50)*22*(1-shake) if shake>0 else 0
    for i in range(6):
        x=SW/2+(i-2.5)*44+dx; d.ellipse([x-11,345,x+11,367],outline='white',width=3,fill='white' if i<n else None)
    for i,kk in enumerate(KP):
        if kk is None: continue
        x,y=kp_pos(i); d.ellipse([x-72,y-72,x+72,y+72],fill=(255,255,255,140 if lit==i else 55))
        d.text((x,y-10 if kk[1] else y),kk[0],font=FI(52,'Regular'),fill='white',anchor='mm')
        if kk[1]: d.text((x,y+34),kk[1],font=FI(15,'SemiBold'),fill='white',anchor='mm')
    d.text((SW-110,1210),'Annuler',font=FI(26),fill='white',anchor='mm'); return im
def scr_findmy(k_btn=0.0,on=False,t=0):
    im=Image.new('RGB',(SW,SH),(233,228,216)); d=ImageDraw.Draw(im,'RGBA')
    for (a,b,w_) in [((0,300),(600,520),40),((150,0),(380,1300),34),((0,820),(600,700),30),((420,0),(520,1300),22)]: d.line([a,b],fill='white',width=w_)
    d.polygon([(40,560),(230,600),(200,760),(30,720)],fill=(190,224,180)); d.rectangle([380,140,560,280],fill=(200,220,240))
    cx,cy=300,560
    for j in range(2):
        r=40+90*((t*0.8+j/2)%1); d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(52,199,89,int(200*(1-(r-40)/90))),width=4)
    d.ellipse([cx-40,cy-40,cx+40,cy+40],fill='white'); d.rounded_rectangle([cx-14,cy-26,cx+14,cy+26],6,fill=(40,40,44))
    island(d); statusbar(d,True)
    d.rounded_rectangle([0,760,SW,SH],34,fill=(255,255,255,252)); d.rounded_rectangle([SW/2-36,774,SW/2+36,781],4,fill=(200,200,206))
    d.text((30,830),'iPhone de Camille',font=FI(34,'Bold'),fill='black',anchor='lm'); d.text((30,872),'Il y a 1 min · 450 m',font=FI(22),fill=TXT2,anchor='lm')
    d.text((30,940),'Marquer comme perdu',font=FI(26,'SemiBold'),fill='black',anchor='lm')
    d.rounded_rectangle([30,970,SW-30,1060],22,fill=(242,242,247))
    if on:
        lockbadge(d,80,1015,22,IRED,(255,255,255)); d.text((118,1015),'Activé',font=FI(26,'SemiBold'),fill=IRED,anchor='lm'); d.text((SW-60,1015),'iPhone verrouillé',font=FI(20),fill=TXT2,anchor='rm')
    else:
        d.text((60,1015),'Désactivé',font=FI(24),fill=TXT2,anchor='lm')
        d.rounded_rectangle([SW-200,988,SW-50,1042],27,fill=(int(0+30*k_btn),122,255)); d.text((SW-125,1015),'Activer',font=FI(23,'SemiBold'),fill='white',anchor='mm')
    homebar(d,True); return im
