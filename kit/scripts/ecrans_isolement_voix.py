# Écrans « Isolement de la voix » (appel + centre de contrôle iOS 26, mode sombre). Lancer depuis kit/.
import sys, json, math
sys.path.insert(0, 'scripts')
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw, ImageFilter
OUT = 'public/'
W = (255, 255, 255); G2 = (160, 160, 166); ORG = (226, 92, 14); BLU = (10, 132, 255); GRN = (52, 199, 89); RED = (255, 59, 48)
POS = {}

def bg_blur():
    im = Image.new('RGB', (SW, SH), (22, 22, 26)); d = ImageDraw.Draw(im)
    for x, y, r, c in [(120, 300, 160, (60, 70, 90)), (480, 520, 180, (70, 50, 80)), (200, 1000, 200, (50, 60, 80)), (450, 1150, 150, (90, 40, 50))]:
        d.ellipse([x-r, y-r, x+r, y+r], fill=c)
    return im.filter(ImageFilter.GaussianBlur(90))

def island(d, pill=False):
    d.rounded_rectangle([SW/2-64, 22, SW/2+64, 62], 21, fill=(0, 0, 0))
    d.ellipse([SW/2-48, 36, SW/2-36, 48], fill=ORG)

def status(d, t='12:18'):
    d.text((66, 44), t, font=FI(24, 'SemiBold'), fill=W, anchor='lm')
    for i in range(4): d.rounded_rectangle([440+i*9, 48-i*4, 446+i*9, 54], 2, fill=W)
    d.text((492, 44), '4G', font=FI(17, 'SemiBold'), fill=W, anchor='lm')
    d.rounded_rectangle([520, 35, 552, 53], 5, fill=W)

def mic(d, cx, cy, s, col):
    d.rounded_rectangle([cx-4*s, cy-9*s, cx+4*s, cy+3*s], 4*s, fill=col)
    d.arc([cx-7*s, cy-6*s, cx+7*s, cy+7*s], 0, 180, fill=col, width=max(2, int(1.6*s)))
    d.line([(cx, cy+7*s), (cx, cy+10*s)], fill=col, width=max(2, int(1.6*s)))

def call_screen():
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); im.paste(Image.new('RGB', (SW, SH), (40, 40, 46)).filter(ImageFilter.GaussianBlur(4)))
    d = ImageDraw.Draw(im); island(d); status(d)
    d.text((SW/2, 150), 'Appel…', font=FI(28), fill=G2, anchor='mm')
    d.text((SW/2, 205), 'Léa', font=FI(50, 'SemiBold'), fill=W, anchor='mm')
    btn = [('Audio', 120, 900), ('FaceTime', 300, 900), ('Couper le micro', 480, 900), ('Plus', 120, 1110), ('Raccrocher', 300, 1110), ('Clavier', 480, 1110)]
    for lab, x, y in btn:
        col = RED if lab == 'Raccrocher' else (W if lab == 'Audio' else (62, 62, 68))
        d.ellipse([x-58, y-58, x+58, y+58], fill=col)
        ic = (0, 0, 0) if lab == 'Audio' else W
        if lab == 'Audio':
            d.polygon([(x-22, y-10), (x-10, y-10), (x+4, y-24), (x+4, y+24), (x-10, y+10), (x-22, y+10)], fill=ic)
            for r in (12, 22): d.arc([x+4-r, y-r, x+4+r, y+r], -45, 45, fill=ic, width=4)
        elif lab == 'Raccrocher':
            d.rounded_rectangle([x-30, y-8, x+30, y+10], 9, fill=W)
        elif lab == 'Couper le micro': mic(d, x, y, 2.6, W); d.line([(x-22, y-26), (x+22, y+26)], fill=W, width=4)
        elif lab == 'Plus':
            for dx in (-16, 0, 16): d.ellipse([x+dx-5, y-5, x+dx+5, y+5], fill=W)
        elif lab == 'Clavier':
            for i in range(3):
                for j in range(3): d.ellipse([x-20+i*20-5, y-20+j*20-5, x-20+i*20+5, y-20+j*20+5], fill=W)
        else:
            d.rounded_rectangle([x-26, y-16, x+10, y+16], 6, fill=W); d.polygon([(x+12, y-4), (x+28, y-14), (x+28, y+14), (x+12, y+4)], fill=W)
        f = FI(21); lines = ['Couper', 'le micro'] if lab == 'Couper le micro' else [lab]
        for k, l in enumerate(lines): d.text((x, y+84+k*26), l, font=f, fill=W, anchor='mm')
    d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=W)
    return im

def cc_screen(hi=False):
    im = bg_blur(); d = ImageDraw.Draw(im, 'RGBA'); island(d)
    # pastille orange Téléphone / Commandes
    d.rounded_rectangle([118, 86, 482, 128], 21, fill=(200, 80, 10, 255))
    mic(d, 140, 108, 1.3, W); d.ellipse([166, 96, 190, 120], fill=BLU)
    d.text((206, 107), 'Téléphone', font=FI(22, 'SemiBold'), fill=W, anchor='lm')
    d.text((330, 107), 'Commandes ›', font=FI(22), fill=(255, 200, 160), anchor='lm')
    POS['cc:pill'] = [300, 107]
    d.text((66, 180), 'Orange F 4G', font=FI(21, 'SemiBold'), fill=W, anchor='lm'); d.text((480, 180), '70 %', font=FI(21, 'SemiBold'), fill=W, anchor='rm')
    on = {1, 5, 10}
    for r in range(4):
        for c in range(4):
            x, y = 108+c*128, 275+r*128; i = r*4+c
            d.ellipse([x-52, y-52, x+52, y+52], fill=(255, 255, 255, 235) if i in on else (110, 110, 118, 150))
            col = (20, 20, 20) if i in on else W
            if i == 1:
                for k in range(4): d.rounded_rectangle([x-22+k*12, y+12-k*8, x-14+k*12, y+16], 3, fill=GRN)
            elif i == 5: d.line([(x-12, y-12), (x+12, y+10), (x, y+22), (x, y-22), (x+12, y-10), (x-12, y+12)], fill=BLU, width=4)
            elif i == 10:
                for rr in (10, 20): d.arc([x-rr, y-rr, x+rr, y+rr], 200, 340, fill=BLU, width=4)
                d.ellipse([x-5, y-5, x+5, y+5], fill=BLU)
            elif i == 3: d.polygon([(x-22, y+4), (x+24, y-4), (x+24, y+4)], fill=col); d.line([(x-6, y-18), (x+4, y+18)], fill=col, width=6)
            elif i == 0:
                for rr in (8, 18, 28): d.arc([x-rr, y-rr+12, x+rr, y+rr+12], 225, 315, fill=col, width=4)
            elif i == 11: d.ellipse([x-20, y-20, x+20, y+20], fill=col); d.ellipse([x-8, y-28, x+28, y+8], fill=(110, 110, 118, 255))
            elif i == 8: d.rounded_rectangle([x-9, y-24, x+9, y+24], 4, fill=col)
            elif i == 9:
                d.rounded_rectangle([x-18, y-24, x+18, y+24], 5, outline=col, width=3)
                for a in range(3):
                    for b in range(3): d.ellipse([x-12+a*12-3, y-8+b*11-3, x-12+a*12+3, y-8+b*11+3], fill=col)
            else: d.ellipse([x-16, y-16, x+16, y+16], outline=col, width=4)
    # curseurs
    for x, f in [(365, 0.6), (493, 0.3)]:
        d.rounded_rectangle([x-52, 870, x+52, 1100], 50, fill=(110, 110, 118, 150))
        d.rounded_rectangle([x-52, 1100-230*f, x+52, 1100], 50, fill=(255, 255, 255, 240))
    for y, t in [(918, 'Ouvrir Radio'), (1045, 'Mémo vocal')]:
        d.rounded_rectangle([58, y-50, 288, y+50], 50, fill=(110, 110, 118, 150)); d.text((110, y), t, font=FI(21, 'SemiBold'), fill=W, anchor='lm')
    return im

OPTS = ['Automatique', 'Standard', 'Isolement de la voix', 'Large spectre']
def menu_screen(sel='Standard'):
    im = bg_blur().filter(ImageFilter.GaussianBlur(10)); d = ImageDraw.Draw(im, 'RGBA'); island(d)
    d.rounded_rectangle([118, 86, 482, 128], 21, fill=(200, 80, 10, 110))
    d.rounded_rectangle([70, 148, 90, 174], 7, fill=W); d.text((100, 160), 'Confidentialité', font=FI(26, 'SemiBold'), fill=W, anchor='lm')
    d.line([(58, 190), (545, 190)], fill=(255, 255, 255, 50), width=1)
    rows = [('Téléphone', GRN, 'Micro', ORG), ('Services sys.', (140, 140, 148), 'Position', BLU)]
    for k, (a, ca, b, cb) in enumerate(rows):
        y = 232+k*78
        d.rounded_rectangle([60, y-16, 92, y+16], 8, fill=ca); d.text((104, y), a, font=FI(23), fill=W, anchor='lm')
        d.ellipse([288, y-15, 318, y+15], fill=cb); d.text((330, y), b, font=FI(21), fill=G2, anchor='lm')
        d.line([(58, y+39), (545, y+39)], fill=(255, 255, 255, 40), width=1)
    y = 400
    d.rounded_rectangle([62, y-12, 84, y+12], 4, fill=W); d.polygon([(84, y-4), (94, y-11), (94, y+11), (84, y+4)], fill=W)
    d.text((102, y), 'Audio et vidéo', font=FI(26, 'SemiBold'), fill=W, anchor='lm'); d.text((532, y), 'Téléphone', font=FI(25, 'SemiBold'), fill=W, anchor='rm')
    POS['mn:av'] = [300, y]
    d.line([(58, y+28), (545, y+28)], fill=(255, 255, 255, 50), width=1)
    d.rounded_rectangle([58, 455, 545, 580], 50, fill=(130, 130, 138, 120), outline=(255, 255, 255, 60))
    mic(d, 86, 498, 1.6, W); d.text((112, 498), 'Entrée', font=FI(25, 'SemiBold'), fill=W, anchor='lm')
    d.text((515, 498), 'Identique au système ⌃', font=FI(21), fill=W, anchor='rm')
    for i in range(23): d.rounded_rectangle([74+i*20.4, 530, 84+i*20.4, 552], 5, fill=(255, 255, 255, 240 if i == 0 else 70))
    d.rounded_rectangle([58, 612, 545, 915], 50, fill=(130, 130, 138, 120), outline=(255, 255, 255, 70))
    POS['mn:card'] = [300, 763]
    d.rounded_rectangle([72, 626, 270, 900], 34, fill=(5, 5, 8))
    for i in range(40):
        x = 90+i*4.3; a = abs(math.sin(i*0.7))*(1 if sel != 'Standard' else 0.6)
        d.line([(x, 763-14*a), (x, 763+14*a)], fill=(60, 200, 255, 200), width=2)
    d.ellipse([150, 741, 194, 785], outline=W, width=3); mic(d, 172, 763, 1.2, W)
    for k, o in enumerate(OPTS):
        y = 655+k*72; s = o == sel
        if s: d.rounded_rectangle([287, y-30, 530, y+30], 30, fill=W)
        col = (20, 20, 20) if s else (W if k < 3 else (255, 255, 255, 80))
        if s: d.ellipse([300, y-10, 320, y+10], fill=BLU)
        else: mic(d, 316, y, 1.1, col)
        d.text((345 if not s else 330, y), o, font=FI(19 if len(o) > 14 else 23, 'Regular' if s else 'SemiBold'), fill=col, anchor='lm')
        POS['mn:'+o] = [408, y]
    return im

call_screen().save(OUT+'iv_call.png')
cc_screen().save(OUT+'iv_cc.png')
menu_screen('Standard').save(OUT+'iv_menu.png')
menu_screen('Isolement de la voix').save(OUT+'iv_menu_on.png')
json.dump(POS, open('scripts/iv_pos.json', 'w'))
print(POS)

# ---- data.json + sons
POS['duree'] = 61.8
json.dump(POS, open('src/data.json', 'w'), indent=0)
import wave, numpy as np
T = 62.2; SR = 44100; au = np.zeros(int(T*SR), np.float32)
def add(t, x):
    i = int(t*SR); x = x[:len(au)-i]; au[i:i+len(x)] += x
def tone(f0, f1, dd, v, dec=6):
    n = int(dd*SR); k = np.linspace(0, 1, n); ph = 2*np.pi*np.cumsum(f0+(f1-f0)*k)/SR
    return (np.sin(ph)*np.exp(-k*dec)*v).astype(np.float32)
def soft():
    n = int(0.42*SR); k = np.arange(n)/SR; env = np.minimum(1, k/0.012)*np.exp(-k*11)
    return ((np.sin(2*np.pi*587.33*k)*0.6+np.sin(2*np.pi*880*k)*0.28+np.sin(2*np.pi*1174.66*k)*0.08)*env*0.30).astype(np.float32)
S = {'soft': soft(), 'pop': tone(520, 900, 0.09, 0.2), 'tick': tone(1400, 1100, 0.06, 0.18), 'ding': tone(1320, 1320, 0.5, 0.2)+tone(1980, 1980, 0.5, 0.09),
     'err': tone(300, 220, 0.25, 0.22, 4), 'swoosh': tone(400, 1200, 0.3, 0.1, 3)}
SC = [2.0, 6.4, 14.1, 19.36, 22.72, 27.1, 30.1, 37.45, 46.0, 51.7, 55.95, 58.3]
ev = [(s, 'soft') for s in SC]
ev += [(5.7, 'pop'), (8.8, 'swoosh'), (11.8, 'tick'), (16.3, 'tick'), (18.2, 'tick'), (21.54, 'tick'), (24.98, 'tick'), (25.64, 'ding'), (33.54, 'swoosh'),
       (35.28, 'pop'), (36.02, 'pop'), (36.48, 'pop'), (38.5, 'err'), (39.44, 'pop'), (40.86, 'pop'), (47.6, 'ding'), (49.74, 'pop'), (50.28, 'pop'), (54.24, 'pop')]
for a, k in ev: add(a, S[k]*0.35/0.3)
au = np.clip(au, -1, 1); w = wave.open(OUT+'sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((au*32767).astype(np.int16).tobytes()); w.close()
