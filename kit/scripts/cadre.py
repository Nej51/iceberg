import numpy as np, cv2, subprocess, os, math, wave, sys, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
CX,CY,CW,CH=81,50,918,1470
FD='/usr/share/fonts/truetype/google-fonts/'
XB=FD+'Poppins-ExtraBold.ttf' if os.path.exists(FD+'Poppins-ExtraBold.ttf') else FD+'Poppins-Bold.ttf'
MD=FD+'Poppins-Medium.ttf' if os.path.exists(FD+'Poppins-Medium.ttf') else XB
_f={}
def F(s,b=True):
    k=(s,b)
    if k not in _f: _f[k]=ImageFont.truetype(XB if b else MD,s)
    return _f[k]
WHT=(255,255,255);PNK=(255,90,170);CYN=(70,225,255);YEL=(255,214,70);GRN=(80,235,140);RED=(255,70,90);GRY=(150,150,165)
MIN='\u2212'
def ss(x): x=min(1,max(0,x)); return x*x*(3-2*x)
def back(x):
    x=min(1,max(0,x)); c=1.9; return 1+(c+1)*(x-1)**3+c*(x-1)**2
def seg(u,a,b): return min(1,max(0,(u-a)/(b-a)))
def mix(c1,c2,k): return tuple(int(a+(b-a)*k) for a,b in zip(c1,c2))
def sigcol(v):  # -120..-70 -> red..yellow..green
    k=min(1,max(0,(v+118)/43))
    return mix(RED,YEL,k*2) if k<0.5 else mix(YEL,GRN,(k-0.5)*2)
# ---------- frame art (same look as before) ----------
def rr_mask(w,h,r):
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],r,fill=255); return np.asarray(m,np.float32)[...,None]/255
CARD_M=rr_mask(CW,CH,56)
yy,xx=np.mgrid[0:H,0:W]
ANG=(np.arctan2(yy-(CY+CH/2),xx-(CX+CW/2))/(2*np.pi)+0.5).astype(np.float32)
PAL=np.array([[255,55,140],[170,70,255],[60,120,255],[40,220,255],[255,150,60],[255,55,140]],np.float32)[:,::-1]
LUT=np.array([PAL[int(p)]*(1-(p-int(p)))+PAL[min(int(p)+1,5)]*(p-int(p)) for p in np.linspace(0,4.999,512)],np.float32)
def ring_alpha(pad,r):
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).rounded_rectangle([CX-pad,CY-pad,CX+CW+pad,CY+CH+pad],r+pad,fill=255); return m
RING=np.asarray(ring_alpha(7,56),np.float32)[...,None]/255
GLOW=np.asarray(ring_alpha(10,56).filter(ImageFilter.GaussianBlur(40)),np.float32)[...,None]/255*0.7
EDGE=np.maximum(RING,GLOW)
BG0=(np.array([24,7,10],np.float32)*(1-EDGE)).astype(np.float32)
ANG_S=cv2.resize(ANG,(W//4,H//4),interpolation=cv2.INTER_NEAREST)
def background(t):
    col=cv2.resize(LUT[((ANG_S+t*0.12)%1*511).astype(np.int32)],(W,H),interpolation=cv2.INTER_LINEAR)
    return BG0+col*EDGE
def cap(lines,pad=(44,22),outline=(190,90,255)):
    tmp=ImageDraw.Draw(Image.new('RGBA',(10,10))); meas=[]
    for size,spans in lines:
        f=F(size); w=sum(tmp.textlength(t,font=f) for t,_ in spans); meas.append((f,w,int(size*1.22)))
    bw=int(max(m[1] for m in meas))+pad[0]*2; bh=sum(m[2] for m in meas)+pad[1]*2; M=30
    im=Image.new('RGBA',(bw+2*M,bh+2*M),(0,0,0,0))
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([M,M+8,M+bw,M+bh+8],40,fill=(0,0,0,190))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12))); d=ImageDraw.Draw(im)
    d.rounded_rectangle([M,M,M+bw,M+bh],40,fill=(14,8,30,240),outline=outline+(255,),width=5)
    y=M+pad[1]
    for (size,spans),(f,w,h) in zip(lines,meas):
        x=M+(bw-w)/2
        for t,c in spans:
            d.text((x,y+h/2),t,font=f,fill=c,anchor='lm',stroke_width=2,stroke_fill=(0,0,0)); x+=tmp.textlength(t,font=f)
        y+=h
    a=np.asarray(im,np.float32); return a[...,[2,1,0,3]].copy()
def paste(canvas,img,cx,cy,scale=1.0,alpha=1.0):
    if alpha<=0.01: return
    if abs(scale-1)>0.004: img=cv2.resize(img,None,fx=scale,fy=scale,interpolation=cv2.INTER_LINEAR)
    h,w=img.shape[:2]; x0=int(cx-w/2); y0=int(cy-h/2)
    xa,ya=max(0,x0),max(0,y0); xb,yb=min(canvas.shape[1],x0+w),min(canvas.shape[0],y0+h)
    if xb<=xa or yb<=ya: return
    s=img[ya-y0:yb-y0,xa-x0:xb-x0]; a=s[...,3:4]/255*alpha
    canvas[ya:yb,xa:xb]=canvas[ya:yb,xa:xb]*(1-a)+s[...,:3]*a
CAPY=1500
def C1(spans,size=60): return cap([(size,spans)])
def C2(top,tcol,spans,ts=40,ms=60): return cap([(ts,[(top,tcol)]),(ms,spans)])
# ---------- card background ----------
g=np.linspace(0,1,CH)[:,None,None]
CARD_BG=Image.fromarray((np.array([26,14,48])*(1-g)+np.array([8,6,20])*g).astype(np.uint8).repeat(CW,1))
rnd=random.Random(3)
STARS=[(rnd.randrange(CW),rnd.randrange(CH),rnd.random()) for _ in range(70)]
def ctext(d,cx,cy,t,size,fill=WHT,b=True,anchor='mm'): d.text((cx,cy),t,font=F(size,b),fill=fill,anchor=anchor)
def phone(d,x,y,w,h):
    d.rounded_rectangle([x-8,y-8,x+w+8,y+h+8],84,fill=(70,66,90))
    d.rounded_rectangle([x,y,x+w,y+h],76,fill=(6,6,10))
    d.rounded_rectangle([x+w/2-70,y+26,x+w/2+70,y+62],18,fill=(24,24,30))
    return (x+18,y+18,x+w-18,y+h-18)
def statusbar(d,x,y,w):
    ctext(d,x+78,y+46,'9:41',26)
    for i in range(4): d.rounded_rectangle([x+w-150+i*13,y+54-8-i*5,x+w-150+i*13+8,y+54],2,fill=WHT)
    ctext(d,x+w-70,y+46,'4G',24)
def ring(d,cx,cy,k,col=WHT,r0=30,r1=110):
    if 0<k<1:
        r=r0+(r1-r0)*k; a=int(255*(1-k)); d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=col+(a,),width=10)
def hl(d,box,t,col=PNK):
    p=0.5+0.5*math.sin(t*14); gr=4+8*p
    d.rounded_rectangle([box[0]-gr,box[1]-gr,box[2]+gr,box[3]+gr],22,outline=col,width=9)
    d.rounded_rectangle([box[0]-gr+3,box[1]-gr+3,box[2]+gr-3,box[3]+gr-3],20,outline=WHT,width=3)
def bars(d,cx,base,sc,n,col=WHT,off=(60,60,80),dx=0):
    for i in range(4):
        w=90*sc; gap=30*sc; hgt=(120+80*i)*sc; x=cx-(4*w+3*gap)/2+i*(w+gap)+dx
        d.rounded_rectangle([x,base-hgt,x+w,base],16*sc,fill=col if i<n else off)

