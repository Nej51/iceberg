import sys,os,json,subprocess,wave
exec(open('cadre.py').read())
import ui_iphone as ui
from ui_iphone import SW,SH,BZ,BW,BH
ui.init(); ui.build_thumbs()
# ---------- phone ----------
def make_body():
    b=Image.new('RGBA',(BW,BH),(0,0,0,0)); g=ui.grad(BW,BH,(92,92,100),(40,40,46),True).convert('RGBA')
    b.paste(g,(0,0),ui.rmask(BW,BH,108)); d=ImageDraw.Draw(b); d.rounded_rectangle([6,6,BW-7,BH-7],102,fill=(8,8,10)); return b
BODY=make_body(); SMASK=ui.rmask(SW,SH,88)
PS=0.98; PCX=CW/2; PCY=690
def shadow_sprite(s):
    w,h=int(BW*s),int(BH*s); m=Image.new('L',(w+120,h+120),0); ImageDraw.Draw(m).rounded_rectangle([60,80,60+w,80+h],int(108*s),fill=150)
    return m.filter(ImageFilter.GaussianBlur(30))
_sh={}
def put_phone(im,scr,cx=PCX,cy=PCY,s=PS,rot=0,blur=0):
    p=BODY.copy(); p.paste(scr,(BZ,BZ),SMASK)
    if abs(s-1)>0.001: p=p.resize((int(BW*s),int(BH*s)),Image.BILINEAR)
    if not rot and not blur:
        k=round(s,3)
        if k not in _sh: _sh[k]=shadow_sprite(k)
        sh=_sh[k]; im.paste((0,0,0),(int(cx-sh.width/2),int(cy-sh.height/2)),sh)
    if rot: p=p.rotate(rot,expand=True,resample=Image.BICUBIC)
    if blur:
        a=np.asarray(p).astype(np.float32); k_=np.zeros((1,blur*2+1),np.float32); k_[0,:]=1/(blur*2+1)
        p=Image.fromarray(cv2.filter2D(a,-1,k_).astype(np.uint8),'RGBA')
    im.paste(p,(int(cx-p.width/2),int(cy-p.height/2)),p)
def s2c(sx,sy,cx=PCX,cy=PCY,s=PS): return cx+(BZ+sx-BW/2)*s, cy+(BZ+sy-BH/2)*s
def kz(keys,u):
    if u<=keys[0][0]: return keys[0][1:]
    for (a,*p),(b,*q) in zip(keys,keys[1:]):
        if u<=b: k=ss((u-a)/(b-a)); return tuple(x+(y-x)*k for x,y in zip(p,q))
    return keys[-1][1:]
# ---------- shared screen helpers ----------
def chip(scr,name,k=1.0):
    if k<=0: return
    x,y=ui.icon_xy(name); d=ImageDraw.Draw(scr,'RGBA'); s=back(k)
    cx,cy=x+88,y+8; r=22*s; d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(52,199,89)); ui.lockbadge(d,cx,cy,max(1,r*0.92),(52,199,89),(255,255,255))
def home(chips=(),tch=None,press=0):
    scr=ui.HOME.copy()
    for c in chips: chip(scr,c,1)
    if tch: ui.touch(scr,*tch,press)
    return scr
def ctx(name,items,pressed=None,k=1.0,tch=None,press=0,chips=()):
    scr=ui.HOME_BLUR.copy(); x,y=ui.icon_xy(name)
    ic=ui.icon(name,104); ui.comp(scr,ic,(x-4,y-4))
    for c in chips: chip(scr,c,1)
    h=sum(10 if it=='-' else 64 for it in items); mx=min(max(x-6,16),SW-16-410)
    my=y+118 if name not in ui.DOCK else y-h-16
    ui.menu(scr,mx,my,items,pressed=pressed,k=k)
    if tch: ui.touch(scr,*tch,press)
    return scr,(mx,my)
def item_pt(items,idx,mx,my): return (mx+180,my+ui.menu_item_y(items,idx))
def timer_pill(im,sec,col):
    w,h=330,112; x=CW/2-w/2; y=26; d=ImageDraw.Draw(im,'RGBA')
    d.rounded_rectangle([x,y,x+w,y+h],30,fill=(14,6,12),outline=col,width=5)
    d.text((CW/2,y+h/2+2),f'00:{int(sec):02d}' if sec<60 else '01:00',font=F(78),fill=col,anchor='mm')
    d.rectangle([CW/2-14,y-14,CW/2+14,y],fill=col)
def stamp(im,txt,col,k,cx,cy,rot=-8,size=86):
    if k<=0: return
    tmp=ImageDraw.Draw(im); w=int(tmp.textlength(txt,font=F(size)))+80
    st=Image.new('RGBA',(w,size+70),(0,0,0,0)); sd=ImageDraw.Draw(st)
    sd.rounded_rectangle([6,6,w-6,size+64],30,fill=col+(240,),outline=(255,255,255),width=8); sd.text((w/2,(size+70)/2),txt,font=F(size),fill=(255,255,255),anchor='mm')
    st=st.rotate(rot,expand=True,resample=Image.BICUBIC); s=back(k); st=st.resize((max(2,int(st.width*s)),max(2,int(st.height*s))))
    im.paste(st,(int(cx-st.width/2),int(cy-st.height/2)),st)
def redx(d,box,k,width=16):
    x0,y0,x1,y1=box
    if k>0: d.line([(x0,y0),(x0+(x1-x0)*min(1,k*2),y0+(y1-y0)*min(1,k*2))],fill=(255,59,48),width=width)
    if k>0.5: kk=(k-0.5)*2; d.line([(x1,y0),(x1-(x1-x0)*kk,y0+(y1-y0)*kk)],fill=(255,59,48),width=width)
# ---------- scenes: f(im,u,t,D) ----------
TYPED='J’arrive, je suis dans la rue'
def s_hook(im,u,t,D):
    if u<0.45:
        n=int(seg(u,0.04,0.42)*len(TYPED)); put_phone(im,ui.scr_conversation(TYPED[:n],int(t*3)%2==0))
    elif u<0.57:
        k=ss(seg(u,0.45,0.58)); put_phone(im,ui.scr_conversation(TYPED),PCX+k*1250,PCY-k*120,PS,rot=-30*k,blur=int(4+30*min(1,k*3)))
        if u<0.5: d=ImageDraw.Draw(im,'RGBA'); d.rectangle([0,0,CW,CH],fill=(255,40,60,int(90*(1-seg(u,0.45,0.5)))))
    else:
        k=ss(seg(u,0.57,0.66)); sway=math.sin(t*2.2)*2.5
        put_phone(im,home(),PCX-900*(1-k)+30,PCY+20,0.92,rot=7+sway,blur=int(20*(1-k)) if k<1 else 0)
        stamp(im,'DÉJÀ OUVERT',(255,59,48),seg(u,0.68,0.78),CW/2,430,-8,80)
def s_useless(im,u,t,D):
    d=ImageDraw.Draw(im,'RGBA')
    for i,(lab,kx) in enumerate((('Ton code',0.18),('Ton Face ID',0.34))):
        x=70+i*410; y=90; d.rounded_rectangle([x,y,x+370,y+330],40,fill=(24,22,40),outline=(90,80,140),width=4)
        if i==0:
            for j in range(6): cx=x+75+j*44; d.ellipse([cx-13,y+125,cx+13,y+151],fill='white')
        else: ui.faceid_glyph(d,x+185,y+140,72,(255,255,255),9)
        d.text((x+185,y+262),lab,font=F(40),fill='white',anchor='mm'); redx(d,(x+40,y+30,x+330,y+300),seg(u,kx,kx+0.12),18)
    tt=t*1.6; tp=tt%1
    scr=home(tch=(300+120*math.sin(int(tt)*1.7),700+260*math.cos(int(tt)*2.3)),press=0)
    put_phone(im,scr,PCX,1010,0.56)
    k=back(seg(u,0.5,0.6))
    if k>0:
        d=ImageDraw.Draw(im,'RGBA'); w=560*k; d.rounded_rectangle([CW/2-w/2,520,CW/2+w/2,600],40,fill=(20,60,40),outline=(52,199,89),width=5)
        if k>0.8: d.text((CW/2,560),'aucun code demandé',font=F(42),fill=(80,235,140),anchor='mm')
def s_chrono(im,u,t,D):
    sec=float(np.interp(u,[0,0.07,0.32,0.58,0.86],[0,10,20,40,60])); sc=0.82; cy=790
    if u<0.32:
        scr=ui.scr_photos_grid(hl=[4,7] if u>0.1 else None,t=t)
    elif u<0.58:
        scr=ui.scr_mail(); k=back(seg(u,0.36,0.42)); pt=ui.login_card(scr,k,u>0.5)
        if u>0.45 and pt: ui.touch(scr,pt[0],pt[1],0.3 if u>0.5 else 0)
    else:
        scr=ui.scr_messages_list()
        for i,(a,ti,bo) in enumerate(((0.6,'Ma Banque','Votre code : 482 913'),(0.66,'Compte e-mail','Code de vérification : 615 207'),(0.72,'Paiement','Code de validation : 307 518'))):
            ui.banner(scr,80+i*134,ss(seg(u,a,a+0.04)),ti,bo)
    put_phone(im,scr,PCX,cy,sc)
    if u>0.86:
        d=ImageDraw.Draw(im,'RGBA'); d.rectangle([0,0,CW,CH],fill=(10,0,4,int(170*seg(u,0.86,0.9))))
        p=1+0.05*math.sin(t*10); d.text((CW/2,700),'01:00',font=F(int(230*p)),fill=(255,59,48),anchor='mm')
    timer_pill(im,sec,(255,59,48))
def s_parade(im,u,t,D):
    d=ImageDraw.Draw(im,'RGBA')
    for i,n in enumerate(('Photos','Mail','Messages','Notes')):
        k=back(seg(u,0.02+i*0.06,0.1+i*0.06))
        if k<=0: continue
        x=CW/2-230+(i%2)*270; y=180+(i//2)*300; ic=ui.icon(n,190).resize((max(2,int(190*k)),max(2,int(190*k))))
        im.paste(ic,(int(x+95-ic.width/2),int(y+95-ic.height/2)),ic)
        kb=back(seg(u,0.3+i*0.08,0.38+i*0.08))
        if kb>0: r=44*kb; d.ellipse([x+175-r,y+15-r,x+175+r,y+15+r],fill=(52,199,89),outline=(255,255,255),width=6); ui.lockbadge(d,x+175,y+15,max(1,r*0.8),(52,199,89),(255,255,255))
        d.text((x+95,y+222),n,font=F(36),fill='white',anchor='mm')
    k=back(seg(u,0.7,0.8))
    if k>0:
        w=420*k; d.rounded_rectangle([CW/2-w/2,860,CW/2+w/2,960],50,fill=(20,60,40),outline=(52,199,89),width=6)
        if k>0.8: d.text((CW/2,910),'1 minute',font=F(56),fill=(80,235,140),anchor='mm')
M_PHOTOS=['Le plus récent','Favoris','Rechercher','-','Modifier l’écran d’accueil','Partager l’app','*Exiger Face ID','!Supprimer l’app']
def s_step1(im,u,t,D):
    pc=ui.icon_center('Photos')
    if u<0.22:
        scr=home(tch=pc if u>0.05 else None,press=seg(u,0.08,0.22))
    elif u<0.48:
        k=back(seg(u,0.22,0.28)); scr,(mx,my)=ctx('Photos',M_PHOTOS,pressed=6 if u>0.4 else None,k=k)
        if u>0.33: ui.touch(scr,*item_pt(M_PHOTOS,6,mx,my),0.3 if u>0.4 else 0)
    elif u<0.68:
        scr=ui.HOME_BLUR.copy(); bt=ui.alert(scr,'Exiger Face ID pour « Photos » ?','Il faudra ton visage ou ton code pour l’ouvrir.',['Exiger Face ID','Annuler'],pressed=0 if u>0.6 else None,k=back(seg(u,0.48,0.53)))
        if u>0.56 and bt: ui.touch(scr,*bt[0],0.3 if u>0.6 else 0)
    elif u<0.82:
        scr=home(); ui.faceid_hud(scr,'ok',seg(u,0.68,0.8))
    else:
        scr=home(); chip(scr,'Photos',seg(u,0.82,0.9))
    put_phone(im,scr)
CAM1=[(0,1,CW/2,690),(0.06,1,CW/2,690),(0.2,1.32,*s2c(250,700)),(0.46,1.32,*s2c(250,700)),(0.52,1.18,*s2c(300,640)),(0.66,1.18,*s2c(300,640)),(0.8,1,CW/2,690),(0.86,1.25,*s2c(150,480)),(1,1.25,*s2c(150,480))]
M2={'Mail':['Nouveau message','Rechercher','-','*Exiger Face ID','!Supprimer l’app'],'Messages':['Nouveau message','-','*Exiger Face ID','!Supprimer l’app'],'Notes':['Nouvelle note','Nouvelle liste','-','*Exiger Face ID','!Supprimer l’app']}
def s_step2(im,u,t,D):
    apps=['Mail','Messages','Notes']; i=min(2,int(u*3)); v=u*3-i; name=apps[i]; done=['Photos']+apps[:i]; items=M2[name]; idx=items.index('*Exiger Face ID')
    if v<0.2: scr=home(done,tch=ui.icon_center(name),press=seg(v,0.02,0.2))
    elif v<0.55:
        scr,(mx,my)=ctx(name,items,pressed=idx if v>0.42 else None,k=back(seg(v,0.2,0.27)),chips=done)
        if v>0.32: ui.touch(scr,*item_pt(items,idx,mx,my),0.3 if v>0.42 else 0)
    elif v<0.8:
        scr=ui.HOME_BLUR.copy(); bt=ui.alert(scr,f'Exiger Face ID pour « {name} » ?','Il faudra ton visage ou ton code pour l’ouvrir.',['Exiger Face ID','Annuler'],pressed=0 if v>0.68 else None,k=back(seg(v,0.55,0.6)))
        if v>0.62 and bt: ui.touch(scr,*bt[0],0.3 if v>0.68 else 0)
    else:
        scr=home(done); chip(scr,name,seg(v,0.8,0.9))
    put_phone(im,scr)
M3=['Copier','Dupliquer','Masquer','-','Ajuster la date et l’heure','!Supprimer']
def s_step3(im,u,t,D):
    if u<0.14:
        scr=ui.scr_photos_grid(); 
        if u>0.05: ui.touch(scr,*ui.grid_pos(4),seg(u,0.1,0.14))
    elif u<0.22: scr=ui.scr_photo_full(ss(seg(u,0.14,0.22)))
    elif u<0.36:
        scr=ui.scr_photo_full()
        if u>0.28: ui.touch(scr,SW-54,124,0.3 if u>0.32 else 0)
    elif u<0.56:
        scr=ui.scr_photo_full(); d=ImageDraw.Draw(scr,'RGBA'); d.rectangle([0,0,SW,SH],fill=(0,0,0,60))
        ui.menu(scr,170,170,M3,pressed=2 if u>0.48 else None,k=back(seg(u,0.36,0.41)))
        if u>0.44: ui.touch(scr,*item_pt(M3,2,170,170),0.3 if u>0.48 else 0)
    elif u<0.7:
        scr=ui.scr_photo_full(); pt=ui.sheet(scr,'Cette photo sera masquée. Tu la retrouveras dans l’album « Masquées », protégé par Face ID.','Masquer la photo',pressed=u>0.64,k=ss(seg(u,0.56,0.6)))
        if u>0.61 and pt: ui.touch(scr,*pt,0.3 if u>0.64 else 0)
    elif u<0.8: scr=ui.scr_photos_grid(hide_id=ss(seg(u,0.7,0.77)))
    else: scr=ui.scr_collections(hl=u>0.84,t=t)
    put_phone(im,scr)
CAM3=[(0,1,CW/2,690),(0.34,1,CW/2,690),(0.4,1.3,*s2c(380,330)),(0.54,1.3,*s2c(380,330)),(0.6,1.25,*s2c(300,1080)),(0.69,1.25,*s2c(300,1080)),(0.74,1,CW/2,690),(0.84,1,CW/2,690),(0.9,1.25,*s2c(300,480)),(1,1.25,*s2c(300,480))]
PIN=[3,7,1,5,9,2]
def s_replay(im,u,t,D):
    sc=0.82; cy=790; done=['Photos','Mail','Messages','Notes']
    if u<0.1: scr=home(tch=ui.icon_center('Photos') if u>0.05 else None,press=0.3 if u>0.08 else 0)
    elif u<0.3: scr=ui.scr_locked_app('Photos','scan' if u<0.2 else 'fail',seg(u,0.1,0.3)*(1 if u<0.2 else 0.5),'Utilise Face ID pour ouvrir' if u<0.2 else 'Ce n’est pas ton visage')
    elif u<0.56:
        tk=[0.33+i*0.025 for i in range(6)]; n=sum(1 for a in tk if u>=a)
        lit=None
        for j,a in enumerate(tk):
            if a<=u<a+0.018: lit=[i for i,kk in enumerate(ui.KP) if kk and kk[0]==str(PIN[j])][0]
        scr=ui.scr_passcode(n if u<0.5 else 6,shake=seg(u,0.5,0.54),lit=lit,err=u>=0.5)
    elif u<0.86:
        apps=['Mail','Messages','Notes']; i=min(2,int((u-0.56)/0.1)); v=(u-0.56)/0.1-i; name=apps[i]
        if v<0.35: scr=home(tch=ui.icon_center(name),press=0.3 if v>0.2 else 0)
        else: scr=ui.scr_locked_app(name,'fail',(v-0.35)*0.4,'Ce n’est pas ton visage')
    else: scr=home(done)
    put_phone(im,scr,PCX,cy,sc)
    timer_pill(im,25+35*seg(u,0,0.95),(80,235,140))
    if u<0.12: stamp(im,'ET CETTE FOIS ?',(130,70,230),seg(u,0,0.05),CW/2,560,-5,70)
    if u>0.88: stamp(im,'BLOQUÉ',(52,170,90),seg(u,0.88,0.94),CW/2,700,-8,96)
def s_lost(im,u,t,D):
    scr=ui.scr_findmy(on=u>0.55,t=t)
    if 0.4<u<0.58: ui.touch(scr,SW-125,1015,0.3 if u>0.48 else 0)
    put_phone(im,scr,PCX,760,0.86)
    d=ImageDraw.Draw(im,'RGBA'); k=back(seg(u,0.02,0.1))
    if k>0:
        w=700*k; d.rounded_rectangle([CW/2-w/2,30,CW/2+w/2,120],45,fill=(16,12,34),outline=CYN,width=5)
        if k>0.8: d.text((CW/2,75),'Depuis le téléphone d’un ami',font=F(38),fill=CYN,anchor='mm')
O1=cap([(52,[("D'autres tutos sur",WHT)])],outline=(0,0,0)); O2=cap([(78,[('tutoriel-iphone.fr',PNK)])],pad=(50,30)); O3=cap([(56,[('Lien en bio',CYN)])],pad=(40,16),outline=CYN)
def s_outro(im,u,t,D):
    d=ImageDraw.Draw(im,'RGBA')
    for j in range(3): ring(d,CW/2,720,((t*0.4)+j/3)%1,(170,90,255),100,620)
SC=[
 dict(f=s_hook,d=7.0,caps=[(0,.45,C1([('Ton iPhone ',WHT),('arraché',PNK),('…',WHT)])),(.45,1,C1([('…écran ',WHT),('allumé',PNK)]))],sfx=[(.45,'pop'),(.7,'err')]),
 dict(f=s_useless,d=6.0,caps=[(0,.5,C1([('Pas besoin de ',WHT),('ton code',PNK)])),(.5,1,C1([('Il est ',WHT),('déjà ouvert',YEL)]))],sfx=[(.18,'err'),(.34,'err')]),
 dict(f=s_chrono,d=14.0,caps=[(0,.32,C2('SA 1re MINUTE',PNK,[('Ta pièce d’identité, ',WHT),('ton RIB',YEL)],ms=50)),(.32,.58,C2('SA 1re MINUTE',PNK,[('Nouveau ',WHT),('mot de passe',YEL),(' demandé',WHT)],ms=50)),(.58,.86,C2('SA 1re MINUTE',PNK,[('Le code arrive… ',WHT),('chez lui',PNK)],ms=52)),(.86,1,C1([('Tes comptes ',WHT),('sont à lui',PNK)]))],sfx=[(.1,'err'),(.5,'tick'),(.6,'pop'),(.66,'pop'),(.72,'pop'),(.86,'err')]),
 dict(f=s_parade,d=5.0,caps=[(0,.62,C1([('Bloqué en ',WHT),('moins d’1 minute',GRN)],54)),(.62,1,C1([('Sans rien ',WHT),('installer',GRN)]))],sfx=[(.3,'tick'),(.38,'tick'),(.46,'tick'),(.54,'tick'),(.72,'ding')]),
 dict(f=s_step1,d=10.0,step=1,cam=CAM1,caps=[(0,.24,C2('ÉTAPE 1',CYN,[('Doigt appuyé sur ',WHT),('Photos',YEL)])),(.24,.48,C2('ÉTAPE 1',CYN,[('Choisis ',WHT),('« Exiger Face ID »',YEL)],ms=54)),(.48,1,C2('ÉTAPE 1',CYN,[('Valide',GRN)]))],sfx=[(.22,'pop'),(.41,'tick'),(.6,'tick'),(.74,'ding')]),
 dict(f=s_step2,d=9.0,step=2,caps=[(0,1,C2('ÉTAPE 2',CYN,[('Même chose : ',WHT),('Mail, Messages, Notes',YEL)],ms=48))],sfx=[(v,'tick') for v in (0.14,0.47,0.81)]+[(v,'ding') for v in (0.27,0.6,0.94)]),
 dict(f=s_step3,d=11.0,step=3,cam=CAM3,caps=[(0,.36,C2('ÉTAPE 3',CYN,[('Ouvre ta ',WHT),('pièce d’identité',YEL)],ms=54)),(.36,.7,C2('ÉTAPE 3',CYN,[('•••  puis  ',WHT),('« Masquer »',YEL)])),(.7,1,C2('ÉTAPE 3',CYN,[('Rangée sous ',WHT),('ton visage',GRN)]))],sfx=[(.12,'tick'),(.34,'tick'),(.5,'tick'),(.66,'tick'),(.86,'ding')]),
 dict(f=s_replay,d=13.0,caps=[(0,.1,C1([('Retour ',WHT),('dans la rue',YEL)])),(.1,.3,C1([('Il lui faut ton visage : ',WHT),('raté',PNK)],52)),(.3,.56,C1([('Codes au hasard : ',WHT),('refusé',PNK)])),(.56,.88,C1([('Mail, Messages, Notes : ',WHT),('fermés',PNK)],50)),(.88,1,C1([('Aucune de ',WHT),('tes infos',GRN)]))],sfx=[(.08,'tick'),(.22,'err'),(.5,'err'),(.6,'err'),(.7,'err'),(.8,'err'),(.9,'ding')]+[(0.33+i*0.025,'tick') for i in range(6)]),
 dict(f=s_lost,d=6.0,caps=[(0,.45,C1([('Toi, tu le ',WHT),('bloques',GRN)])),(.45,1,C1([('à distance avec ',WHT),('Localiser',GRN)]))],sfx=[(.48,'tick'),(.56,'ding')]),
 dict(f=s_outro,d=6.0,outro=True,caps=[(0,.3,C1([('Fais-le ',WHT),('maintenant',YEL)])),(.3,1.2,C1([('Abonne-toi',YEL),(' pour la suite',WHT)]))],sfx=[(.2,'pop'),(.38,'pop'),(.62,'ding')]),
]
OUT_T=(0.2,0.38,0.62)
ST=[0,3.68,7.64,25.1,28.6,34.96,41.6,51.1,64.85,69.2,77.33]
for i,s_ in enumerate(SC): s_['d']=ST[i+1]-ST[i]
WARP={0:[(.45,2.4),(.57,2.95),(.68,3.2)],1:[(.18,6.3),(.34,6.9),(.5,7.2)],
 2:[(.07,10.6),(.1,12.9),(.32,15.8),(.36,16.9),(.5,18.3),(.58,19.2),(.6,19.6),(.66,20.3),(.72,20.9),(.86,22.3)],
 3:[(.3,26.2),(.7,27.1)],4:[(.06,29.0),(.22,30.5),(.33,31.9),(.4,32.6),(.48,33.4),(.56,33.8),(.6,34.0),(.68,34.3)],
 5:[(.333,37.2),(.667,39.4)],6:[(.1,43.2),(.22,43.9),(.28,46.2),(.36,46.6),(.48,47.6),(.56,48.0),(.64,48.4),(.7,48.6),(.8,49.4)],
 7:[(.05,53.2),(.1,53.8),(.2,56.3),(.3,57.2),(.33,57.5),(.5,58.6),(.56,59.3),(.66,60.0),(.76,60.8),(.86,61.6),(.88,62.4)],
 8:[(.4,66.9),(.55,67.3)]}
for i,w in WARP.items(): SC[i]['warp']=[(du,to-ST[i]) for du,to in w]
CAPS={0:[(2.4,C1([('En plein message, ',WHT),('dans la rue',YEL)],52)),(None,C1([('On t’',WHT),('arrache',PNK),(' ton iPhone',WHT)]))],
 1:[(4.9,C1([('Écran ',WHT),('encore allumé',PNK)])),(None,C1([('Pas besoin de ',WHT),('ton code',PNK)]))],
 2:[(10.6,C1([('Sa ',WHT),('1re minute',PNK),(' avec',WHT)])),(15.8,C2('GALERIE',PNK,[('Ta pièce d’identité, ',WHT),('ton RIB',YEL)],ms=50)),(19.2,C2('BOÎTE MAIL',PNK,[('Nouveau ',WHT),('mot de passe',YEL),(' demandé',WHT)],ms=50)),(22.3,C2('SMS',PNK,[('Le code arrive… ',WHT),('chez lui',PNK)],ms=52)),(None,C1([('Tes comptes ',WHT),('sont à lui',PNK)]))],
 3:[(27.4,C1([('Bloqué en ',WHT),('moins d’1 minute',GRN)],54)),(None,C1([('Sans rien ',WHT),('installer',GRN)]))],
 4:[(31.3,C2('ÉTAPE 1',CYN,[('Doigt appuyé sur ',WHT),('Photos',YEL)])),(33.8,C2('ÉTAPE 1',CYN,[('Choisis ',WHT),('« Exiger Face ID »',YEL)],ms=54)),(None,C2('ÉTAPE 1',CYN,[('Valide',GRN)]))],
 5:[(38.3,C2('ÉTAPE 2',CYN,[('Même chose : ',WHT),('Mail, Messages, Notes',YEL)],ms=48)),(None,C2('ÉTAPE 2',CYN,[('Des apps ',WHT),('sensibles',YEL),(' aussi',WHT)]))],
 6:[(45.6,C2('ÉTAPE 3',CYN,[('Ta pièce d’identité ',WHT),('+ ton RIB',YEL)],ms=52)),(48.2,C2('ÉTAPE 3',CYN,[('•••  puis  ',WHT),('« Masquer »',YEL)])),(None,C2('ÉTAPE 3',CYN,[('Rangées sous ',WHT),('ton visage',GRN)]))],
 7:[(53.2,C1([('Refaisons ',WHT),('la scène',YEL)])),(57.2,C1([('Il lui faut ton visage : ',WHT),('raté',PNK)],52)),(59.3,C1([('Codes au hasard : ',WHT),('refusé',PNK)])),(62.4,C1([('Mail, Messages, Notes : ',WHT),('verrouillés',PNK)],46)),(None,C1([('Aucune de ',WHT),('tes infos',GRN)]))],
 8:[(67.3,C1([('Toi, tu le ',WHT),('bloques',GRN)])),(None,C1([('à distance avec ',WHT),('Localiser',GRN)]))],
 9:[(71.5,C1([('Fais-le ',WHT),('maintenant',YEL)])),(None,C1([('Abonne-toi',YEL),(' pour la suite',WHT)]))]}
for i,cl in CAPS.items():
    D=SC[i]['d']; out=[]; a0=0
    for te,img in cl:
        b0=1.0 if te is None else (te-ST[i])/D; out.append((a0,b0,img)); a0=b0
    SC[i]['caps']=out
D9=SC[9]['d']; OUT_T=((72.2-ST[9])/D9,(74.0-ST[9])/D9,(75.6-ST[9])/D9)
def warp_u(s,t):
    w=s.get('warp')
    if not w: return t/s['d']
    return float(np.interp(t,[0]+[x[1] for x in w]+[s['d']],[0]+[x[0] for x in w]+[1]))
def unwarp(s,u):
    w=s.get('warp')
    if not w: return u*s['d']
    return float(np.interp(u,[0]+[x[0] for x in w]+[1],[0]+[x[1] for x in w]+[s['d']]))
TOTAL=sum(s['d'] for s in SC)
def render(s,t,T):
    D=s['d']; u=warp_u(s,t)
    im=CARD_BG.copy(); d=ImageDraw.Draw(im,'RGBA')
    for (x,y,p) in STARS:
        a=int(60+60*math.sin(T*1.5+p*20)); d.ellipse([x-2,y-2,x+2,y+2],fill=(160,140,255,max(0,a)))
    s['f'](im,u,t,D)
    card=np.asarray(im,np.float32)[...,::-1]
    z,fx,fy=kz(s['cam'],u) if s.get('cam') else (1,CW/2,CH/2)
    z*=1+0.08*(1-ss(t/0.35))
    if z>1.002:
        x0=min(max(fx-CW/(2*z),0),CW-CW/z); y0=min(max(fy-CH/(2*z),0),CH-CH/z)
        M=np.float32([[z,0,-x0*z],[0,z,-y0*z]]); card=cv2.warpAffine(card,M,(CW,CH),flags=cv2.INTER_LINEAR)
    canvas=background(T)
    reg=canvas[CY:CY+CH,CX:CX+CW]; reg[:]=reg*(1-CARD_M)+card*CARD_M
    if s.get('outro'):
        for img,y,t0 in zip((O1,O2,O3),(560,720,900),OUT_T):
            uu=t-t0*D
            if uu>0: paste(canvas,img,W/2,y,0.55+0.45*back(uu/0.3),min(1,uu/0.12))
    x0,x1=CX+40,CX+CW-40
    cv2.line(canvas,(x0,CY+22),(x1,CY+22),(90,70,90),8,cv2.LINE_AA); cv2.line(canvas,(x0,CY+22),(int(x0+(x1-x0)*T/TOTAL),CY+22),(255,255,255),8,cv2.LINE_AA)
    if s.get('step'):
        for i in range(3): cv2.circle(canvas,(CX+CW-70-(2-i)*46,CY+70),14,(255,225,70) if i<s['step'] else (120,100,120),-1,cv2.LINE_AA)
    for (a,b,img) in s['caps']:
        a*=D; b*=D
        if a<=t<b:
            uu=t-a; paste(canvas,img,W/2,CAPY,0.55+0.45*back(uu/0.28),min(1,uu/0.12)*min(1,(b-t)/0.12))
    if t<0.12: canvas[:]=canvas+(255-canvas)*(0.35*(1-t/0.12))
    return np.clip(canvas,0,255).astype(np.uint8)
if __name__=='__main__':
    if sys.argv[1]=='test':
        tiles=[]; T=0
        for s in SC:
            for u in s.get('tu',(0.2,0.45,0.62,0.9)): tiles.append(cv2.resize(render(s,unwarp(s,u),T+unwarp(s,u)),(216,384)))
            T+=s['d']
        while len(tiles)%10: tiles.append(np.zeros_like(tiles[0]))
        cv2.imwrite('test.jpg',np.vstack([np.hstack(tiles[i:i+10]) for i in range(0,len(tiles),10)])); sys.exit()
    OUT=sys.argv[2]
    out=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','20','-preset','medium','-pix_fmt','yuv420p','video.mp4'],stdin=subprocess.PIPE)
    T=0.0; sfx=[]
    for s in SC:
        n=round(s['d']*FPS); sfx.append((T,'soft'))
        for c in s['caps']: sfx.append((T+c[0]*s['d']+0.02,'pop'))
        for v,ty in s.get('sfx',[]): sfx.append((T+unwarp(s,v),ty))
        for i in range(n): out.stdin.write(render(s,i/FPS,T+i/FPS).tobytes())
        T+=n/FPS
    out.stdin.close(); out.wait()
    SR=44100; au=np.zeros(int((T+0.2)*SR),np.float32)
    def add(t,x):
        i=int(t*SR); x=x[:len(au)-i]; au[i:i+len(x)]+=x
    def tone(f0,f1,dd,v,dec=6):
        n=int(dd*SR); k=np.linspace(0,1,n); ph=2*np.pi*np.cumsum(f0+(f1-f0)*k)/SR
        return (np.sin(ph)*np.exp(-k*dec)*v).astype(np.float32)
    def soft():
        n=int(0.42*SR); k=np.arange(n)/SR; env=np.minimum(1,k/0.012)*np.exp(-k*11)
        return ((np.sin(2*np.pi*587.33*k)*0.6+np.sin(2*np.pi*880*k)*0.28+np.sin(2*np.pi*1174.66*k)*0.08)*env*0.30).astype(np.float32)
    err=np.concatenate([tone(330,300,0.09,0.2,4),np.zeros(int(0.04*SR),np.float32),tone(300,260,0.12,0.2,4)])
    S={'soft':soft(),'pop':tone(520,900,0.09,0.2),'tick':tone(1400,1100,0.06,0.18),'ding':tone(1320,1320,0.5,0.2)+tone(1980,1980,0.5,0.09),'err':err}
    for t,k in sfx: add(max(0,t),S[k])
    au=np.clip(au,-1,1); w=wave.open('sfx.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((au*32767).astype(np.int16).tobytes()); w.close()
    if 'voice' in sys.argv: cmd=f'ffmpeg -v error -y -i video.mp4 -i voice.wav -i sfx.wav -filter_complex "[2:a]volume=0.35[s];[1:a][s]amix=inputs=2:duration=first:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart {OUT}'
    else: cmd=f'ffmpeg -v error -y -i video.mp4 -i sfx.wav -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart {OUT}'
    subprocess.run(cmd,shell=True,check=True); print('done',T)
