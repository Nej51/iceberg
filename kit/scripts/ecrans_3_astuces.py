# Écrans « 3 astuces cachées » (Envoyer plus tard, Pleine page, symbole °) + sons. Lancer depuis kit/.
import sys, json, wave, numpy as np
sys.path.insert(0, 'scripts')
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw
OUT = 'public/'
W = (255, 255, 255); G2 = (152, 152, 159); BLU = (10, 132, 255); BG = (28, 28, 30)
KB_BG = (38, 38, 40); KEY = (100, 100, 104); KEY2 = (70, 70, 74)
POS = {}

def status(d, fill=W):
    d.text((70, 44), '17:34', font=FI(25, 'SemiBold'), fill=fill, anchor='lm')
    d.rounded_rectangle([SW/2-64, 22, SW/2+64, 62], 21, fill=(0, 0, 0))
    for i in range(4): d.rounded_rectangle([440+i*9, 46-i*4, 446+i*9, 52], 2, fill=fill)
    d.rounded_rectangle([500, 34, 540, 54], 6, fill=(52, 199, 89)); d.text((520, 44), '78', font=FI(15, 'Bold'), fill=(0, 0, 0), anchor='mm')
def homebar(d, c=W): d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=c)
def dashed_rr(d, box, r, col, dash=10, gap=7, width=2):
    x0, y0, x1, y1 = box
    def seg(p0, p1):
        L = ((p1[0]-p0[0])**2+(p1[1]-p0[1])**2)**0.5; n = int(L//(dash+gap))+1
        for k in range(n):
            a = k*(dash+gap)/L; b = min(1, (k*(dash+gap)+dash)/L)
            d.line([(p0[0]+(p1[0]-p0[0])*a, p0[1]+(p1[1]-p0[1])*a), (p0[0]+(p1[0]-p0[0])*b, p0[1]+(p1[1]-p0[1])*b)], fill=col, width=width)
    seg((x0+r, y0), (x1-r, y0)); seg((x0+r, y1), (x1-r, y1)); seg((x0, y0+r), (x0, y1-r)); seg((x1, y0+r), (x1, y1-r))
    for (cx, cy, a0) in [(x0+r, y0+r, 180), (x1-r, y0+r, 270), (x1-r, y1-r, 0), (x0+r, y1-r, 90)]:
        for a in range(a0, a0+90, 18): d.arc([cx-r, cy-r, cx+r, cy+r], a, a+10, fill=col, width=width)
def clock(d, cx, cy, r, col=BLU, dashed=False):
    if dashed:
        for a in range(0, 360, 30): d.arc([cx-r, cy-r, cx+r, cy+r], a, a+18, fill=col, width=3)
        r2 = r-8; d.ellipse([cx-r2, cy-r2, cx+r2, cy+r2], fill=col)
    else: d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=col); r2 = r
    d.line([(cx, cy), (cx, cy-r2*0.6)], fill=W, width=3); d.line([(cx, cy), (cx+r2*0.45, cy+r2*0.2)], fill=W, width=3)

# ---------- Messages ----------
def header(d):
    d.line([(58, 96), (44, 110), (58, 124)], fill=BLU, width=4, joint='curve')
    d.ellipse([SW/2-42, 84, SW/2+42, 168], fill=(120, 110, 200)); d.text((SW/2, 126), 'L', font=FI(40, 'SemiBold'), fill=W, anchor='mm')
    d.text((SW/2, 192), 'Léa ›', font=FI(21), fill=W, anchor='mm')
    d.text((SW/2, 300), 'iMessage · Hier 21:02', font=FI(17), fill=G2, anchor='mm')
    f = FI(27); t = 'Tu fais quoi demain ?'; w = d.textlength(t, font=f)+44
    d.rounded_rectangle([24, 340, 24+w, 402], 31, fill=(44, 44, 46)); d.text((46, 371), t, font=f, fill=W, anchor='lm')
    t = 'Rien de spécial 😅'.replace(' 😅', ''); w = d.textlength(t, font=f)+44
    d.rounded_rectangle([SW-24-w, 420, SW-24, 482], 31, fill=BLU); d.text((SW-46, 451), t, font=f, fill=W, anchor='rm')

KY0 = 860
def kb_letters(d):
    d.rectangle([0, KY0, SW, SH], fill=KB_BG)
    kw, gap, kh = 52, 6, 76
    for r, row in enumerate(['azertyuiop', 'qsdfghjklm', 'wxcvbn\'']):
        n = len(row); y = KY0+20+r*(kh+14); x0 = (SW-(n*kw+(n-1)*gap))/2
        for i, ch in enumerate(row):
            x = x0+i*(kw+gap); d.rounded_rectangle([x, y, x+kw, y+kh], 10, fill=KEY); d.text((x+kw/2, y+kh/2), ch, font=FI(30), fill=W, anchor='mm')
        if r == 2:
            d.rounded_rectangle([12, y, 82, y+kh], 10, fill=KEY2); d.rounded_rectangle([SW-82, y, SW-12, y+kh], 10, fill=KEY2); d.text((SW-47, y+kh/2), '⌫', font=FI(28), fill=W, anchor='mm')
    y = KY0+20+3*(kh+14)
    d.rounded_rectangle([12, y, 130, y+kh], 10, fill=KEY2); d.text((71, y+kh/2), '123', font=FI(24), fill=W, anchor='mm')
    d.rounded_rectangle([140, y, 440, y+kh], 10, fill=KEY); d.rounded_rectangle([450, y, SW-12, y+kh], 10, fill=KEY2); d.text((519, y+kh/2), 'retour', font=FI(22), fill=W, anchor='mm')

NUMS = ['1234567890', '-/:;()€&@"']
def kb_nums(d, pop=None):
    d.rectangle([0, KY0, SW, SH], fill=KB_BG)
    kw, gap, kh = 52, 6, 76
    for r, row in enumerate(NUMS):
        y = KY0+20+r*(kh+14); x0 = (SW-(10*kw+9*gap))/2
        for i, ch in enumerate(row):
            x = x0+i*(kw+gap); hl = pop and ch == '0' and r == 0
            d.rounded_rectangle([x, y, x+kw, y+kh], 10, fill=(150, 150, 156) if hl else KEY); d.text((x+kw/2, y+kh/2), ch, font=FI(30), fill=W, anchor='mm')
            if ch == '0' and r == 0: POS['k0'] = [round(x+kw/2), round(y+kh/2)]
    y = KY0+20+2*(kh+14)
    d.rounded_rectangle([12, y, 92, y+kh], 10, fill=KEY2); d.text((52, y+kh/2), '#+=', font=FI(20), fill=W, anchor='mm')
    for i, ch in enumerate('.,?!\''):
        x = 104+i*80; d.rounded_rectangle([x, y, x+70, y+kh], 10, fill=KEY); d.text((x+35, y+kh/2), ch, font=FI(30), fill=W, anchor='mm')
    d.rounded_rectangle([SW-92, y, SW-12, y+kh], 10, fill=KEY2); d.text((SW-52, y+kh/2), '⌫', font=FI(28), fill=W, anchor='mm')
    y = KY0+20+3*(kh+14)
    d.rounded_rectangle([12, y, 140, y+kh], 10, fill=KEY2); d.text((76, y+kh/2), 'ABC', font=FI(24), fill=W, anchor='mm')
    d.rounded_rectangle([150, y, 440, y+kh], 10, fill=KEY); d.rounded_rectangle([450, y, SW-12, y+kh], 10, fill=KEY2); d.text((519, y+kh/2), 'retour', font=FI(22), fill=W, anchor='mm')
    if pop:  # bulle au-dessus du 0 : « ° » et « 0 »
        kx, ky = POS['k0']; bx1 = SW-6; bx0 = bx1-150; by0 = ky-38-120; by1 = ky-38
        d.rounded_rectangle([bx0, by0, bx1, by1], 22, fill=(90, 90, 94), outline=(120, 120, 126), width=2)
        cells = [('°', bx0+40), ('0', bx1-40)]
        for ch, cx in cells:
            on = (pop == 'deg' and ch == '°') or (pop == 'zero' and ch == '0')
            if on: d.rounded_rectangle([cx-30, by0+14, cx+30, by1-14], 12, fill=(29, 110, 245))
            d.text((cx, (by0+by1)/2), ch, font=FI(44), fill=W, anchor='mm')
        POS['pop_deg'] = [bx0+40, round((by0+by1)/2)]; POS['pop_zero'] = [bx1-40, round((by0+by1)/2)]

def input_bar(d, y, typed='', pill=None, send=False):
    d.ellipse([20, y+4, 76, y+60], fill=(44, 44, 46)); d.text((48, y+31), '+', font=FI(36), fill=W, anchor='mm')
    POS['plus'] = [48, y+32]
    h = 64 if not pill else 128
    top = y+64-h
    d.rounded_rectangle([88, top, SW-22, y+64], 32, outline=(70, 70, 74), width=2, fill=(30, 30, 32))
    if pill:
        dashed_rr(d, [100, top+10, SW-34, top+58], 22, (80, 150, 230))
        clock(d, 128, top+34, 13); d.text((152, top+34), pill+' ›', font=FI(22, 'SemiBold'), fill=(90, 170, 255), anchor='lm')
        d.text((SW-60, top+34), '×', font=FI(30), fill=(90, 170, 255), anchor='mm')
        POS['pill'] = [300, top+34]
    d.text((110, y+32), typed or 'iMessage', font=FI(25), fill=W if typed else G2, anchor='lm')
    if send:
        d.ellipse([SW-70, y+12, SW-30, y+52], fill=BLU); d.line([(SW-50, y+42), (SW-50, y+22)], fill=W, width=4); d.line([(SW-59, y+30), (SW-50, y+21), (SW-41, y+30)], fill=W, width=4)
        POS['send'] = [SW-50, y+32]

def m_conv():
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); d = ImageDraw.Draw(im); status(d); header(d)
    input_bar(d, KY0-84); kb_letters(d); return im
def m_menu():
    im = m_conv(); ov = Image.new('RGBA', (SW, SH), (0, 0, 0, 110)); im = Image.alpha_composite(im.convert('RGBA'), ov); d = ImageDraw.Draw(im)
    items = [('Appareil photo', (90, 90, 96)), ('Photos', (255, 255, 255)), ('Envoyer plus tard', None), ('Genmoji', (240, 200, 80)), ('Position', (52, 199, 89))]
    x0, y0, w, rh = 14, 420, 450, 82
    d.rounded_rectangle([x0, y0, x0+w, y0+len(items)*rh+20], 34, fill=(30, 30, 32), outline=(60, 60, 64), width=2)
    for i, (n, c) in enumerate(items):
        cy = y0+10+rh*i+rh/2
        if c is None: clock(d, x0+56, cy, 26, (90, 170, 255), dashed=True); POS['m_later'] = [x0+w/2, round(cy)]
        else:
            d.ellipse([x0+30, cy-26, x0+82, cy+26], fill=c)
            if n == 'Photos':
                for k, col in enumerate([(255, 80, 80), (255, 190, 40), (60, 200, 90), (60, 140, 255)]):
                    a = k*90; import math; px = x0+56+12*math.cos(math.radians(a)); py = cy+12*math.sin(math.radians(a)); d.ellipse([px-9, py-9, px+9, py+9], fill=col)
            if n == 'Position': d.ellipse([x0+44, cy-12, x0+68, cy+12], fill=W); d.ellipse([x0+49, cy-7, x0+63, cy+7], fill=BLU)
            if n == 'Appareil photo': d.rounded_rectangle([x0+40, cy-12, x0+72, cy+14], 5, fill=(30, 30, 32)); d.ellipse([x0+48, cy-7, x0+64, cy+9], fill=(90, 90, 96))
        d.text((x0+110, cy), n, font=FI(30), fill=W, anchor='lm')
    return im.convert('RGB')

def picker(d):
    y0 = KY0-10; d.rounded_rectangle([12, y0, SW-12, SH-20], 40, fill=(36, 36, 38))
    rows = [('Sam. 21 nov.', '06', '57'), ('Dim. 22 nov.', '07', '58'), ("Aujourd'hui", '08', '59'), ('Mar. 24 nov.', '09', '00'), ('Mer. 25 nov.', '10', '01'), ('Jeu. 26 nov.', '11', '02'), ('Ven. 27 nov.', '12', '03')]
    cy0 = y0+105; d.rounded_rectangle([28, cy0+3*52-30, SW-28, cy0+3*52+30], 20, fill=(58, 58, 62))
    for i, (a, b, c) in enumerate(rows):
        y = cy0+i*52; on = i == 3; col = W if on else (120, 120, 126); f = FI(32 if on else 27, 'SemiBold' if on else 'Regular')
        d.text((250, y), a, font=f, fill=col, anchor='rm'); d.text((360, y), b, font=f, fill=col, anchor='mm'); d.text((460, y), c, font=f, fill=col, anchor='mm')
    POS['picker'] = [300, cy0+3*52]
def m_picker():
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); d = ImageDraw.Draw(im); status(d); header(d)
    input_bar(d, KY0-104, pill='Demain 09:00'); picker(d); homebar(d); return im
MSG = 'Joyeux anniversaire !'
def m_typed():
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); d = ImageDraw.Draw(im); status(d); header(d)
    input_bar(d, KY0-84, typed=MSG, pill='Demain 09:00', send=True); kb_letters(d); return im
def m_sent():
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); d = ImageDraw.Draw(im); status(d); header(d)
    f = FI(27); w = d.textlength(MSG, font=f)+44
    d.text((SW/2, 560), 'Envoi : demain à 09:00', font=FI(18, 'SemiBold'), fill=G2, anchor='mm')
    dashed_rr(d, [SW-24-w, 590, SW-24, 652], 30, (90, 170, 255), width=3); d.text((SW-46, 621), MSG, font=f, fill=W, anchor='rm')
    POS['sent'] = [round(SW-24-w/2), 621]
    input_bar(d, KY0-84); kb_letters(d); return im

# ---------- Safari / capture ----------
def recipe(im, x, y, w, h, s=1.0):
    d = ImageDraw.Draw(im); d.rectangle([x, y, x+w, y+h], fill=(250, 248, 244))
    F = lambda n, wt='Regular': FI(max(6, int(n*s)), wt)
    d.text((x+24*s, y+40*s), 'Gâteau au chocolat', font=F(34, 'Bold'), fill=(30, 20, 15), anchor='lm')
    d.text((x+24*s, y+80*s), '★★★★★  · 45 min · 6 pers.', font=F(18), fill=(140, 110, 80), anchor='lm')
    d.rounded_rectangle([x+24*s, y+110*s, x+w-24*s, y+330*s], int(18*s), fill=(92, 58, 40))
    d.ellipse([x+w/2-110*s, y+150*s, x+w/2+110*s, y+300*s], fill=(70, 40, 28)); d.ellipse([x+w/2-90*s, y+165*s, x+w/2+90*s, y+270*s], fill=(110, 70, 48))
    yy = y+370*s; d.text((x+24*s, yy), 'Ingrédients', font=F(26, 'Bold'), fill=(30, 20, 15), anchor='lm')
    for k, t in enumerate(['200 g de chocolat noir', '100 g de beurre', '3 œufs', '80 g de sucre', '50 g de farine']):
        d.text((x+34*s, yy+44*s+k*36*s), '•  '+t, font=F(20), fill=(70, 60, 55), anchor='lm')
    yy += 260*s; d.text((x+24*s, yy), 'Préparation', font=F(26, 'Bold'), fill=(30, 20, 15), anchor='lm')
    for k in range(int(26)):
        yb = yy+40*s+k*30*s
        if yb > y+h-20*s: break
        ln = [480, 520, 400, 500, 300, 510, 470, 260][k % 8]*s*(w/600)
        if k % 4 == 0: d.text((x+24*s, yb+8*s), f'Étape {k//4+1}', font=F(20, 'Bold'), fill=(150, 90, 40), anchor='lm')
        else: d.rounded_rectangle([x+24*s, yb, x+24*s+ln, yb+14*s], int(7*s), fill=(205, 200, 195))
def c_page():
    im = Image.new('RGB', (SW, SH), (250, 248, 244)); d = ImageDraw.Draw(im)
    recipe(im, 0, 80, SW, 1100); status(d, fill=(0, 0, 0))
    d.rounded_rectangle([20, 1190, SW-20, 1256], 33, fill=(235, 235, 240)); d.text((SW/2, 1223), 'recettes-maison.fr', font=FI(22), fill=(40, 40, 40), anchor='mm')
    homebar(d, (0, 0, 0)); return im
def editor(full):
    im = Image.new('RGB', (SW, SH), (22, 22, 24)); d = ImageDraw.Draw(im); status(d)
    d.ellipse([20, 84, 84, 148], fill=(44, 44, 46)); d.line([(40, 104), (64, 128)], fill=W, width=4); d.line([(64, 104), (40, 128)], fill=W, width=4)
    d.rounded_rectangle([250, 84, 490, 148], 32, fill=(44, 44, 46))
    for k in range(3): d.ellipse([292+k*76-14, 102, 292+k*76+14, 130], outline=W, width=3)
    d.ellipse([510, 84, 574, 148], fill=(200, 200, 204)); d.line([(526, 118), (538, 130), (558, 102)], fill=(0, 0, 0), width=5)
    d.rounded_rectangle([22, 178, SW-22, 246], 34, fill=(44, 44, 46))
    sel = [SW/2+2, 184, SW-28, 240] if full else [28, 184, SW/2-2, 240]
    d.rounded_rectangle(sel, 28, fill=(0, 0, 0))
    d.text((SW/4+10, 212), 'Écran', font=FI(26, 'SemiBold'), fill=W, anchor='mm'); d.text((3*SW/4-10, 212), 'Pleine page', font=FI(26, 'SemiBold'), fill=W, anchor='mm')
    POS['tab_full'] = [round(3*SW/4-10), 212]
    if not full:
        pg = Image.new('RGB', (SW, 1100), (250, 248, 244)); recipe(pg, 0, 0, SW, 1100)
        pg = pg.resize((420, 770)); im.paste(pg, (90, 290)); d.rectangle([90, 290, 510, 1060], outline=(90, 90, 94), width=2)
    else:
        pg = Image.new('RGB', (SW, 2600), (250, 248, 244)); recipe(pg, 0, 0, SW, 2600)
        im.paste(pg.crop((0, 0, SW, 1500)).resize((380, 950)), (90, 290))
        strip = pg.resize((70, 300)); im.paste(strip, (496, 300)); d.rectangle([490, 294, 572, 1256], fill=(36, 36, 38)); im.paste(pg.resize((70, 940)), (496, 300))
        d.rounded_rectangle([492, 296, 570, 520], 10, outline=W, width=4)
    return im

# ---------- clavier chiffres (degré) ----------
def k_screen(typed, pop=None):
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); d = ImageDraw.Draw(im); status(d); header(d)
    input_bar(d, KY0-84, typed=typed, send=True); kb_nums(d, pop); return im

S = {'m_conv': m_conv, 'm_menu': m_menu, 'm_picker': m_picker, 'm_typed': m_typed, 'm_sent': m_sent, 'c_page': c_page,
     'c_ecran': lambda: editor(False), 'c_full': lambda: editor(True),
     'k_num': lambda: k_screen('Il fait 3'), 'k_zero': lambda: k_screen('Il fait 3', 'zero'), 'k_deg': lambda: k_screen('Il fait 3', 'deg'), 'k_done': lambda: k_screen('Il fait 3°')}
for n, f in S.items(): f().save(OUT+n+'.png')
POS['duree'] = 64.41
json.dump(POS, open('src/data.json', 'w'), indent=0)
print(POS)

# ---- sons
T = 64.5; SR = 44100; au = np.zeros(int((T+0.5)*SR), np.float32)
def add(t, x):
    i = int(t*SR); x = x[:len(au)-i]; au[i:i+len(x)] += x
def tone(f0, f1, dd, v, dec=6):
    n = int(dd*SR); k = np.linspace(0, 1, n); ph = 2*np.pi*np.cumsum(f0+(f1-f0)*k)/SR
    return (np.sin(ph)*np.exp(-k*dec)*v).astype(np.float32)
def soft():
    n = int(0.42*SR); k = np.arange(n)/SR; env = np.minimum(1, k/0.012)*np.exp(-k*11)
    return ((np.sin(2*np.pi*587.33*k)*0.6+np.sin(2*np.pi*880*k)*0.28+np.sin(2*np.pi*1174.66*k)*0.08)*env*0.30).astype(np.float32)
def shutter():
    n = int(0.12*SR); return (np.random.RandomState(1).randn(n)*np.exp(-np.linspace(0, 1, n)*18)*0.18).astype(np.float32)
SS = {'soft': soft(), 'pop': tone(520, 900, 0.09, 0.2), 'tick': tone(1400, 1100, 0.06, 0.18), 'ding': tone(1320, 1320, 0.5, 0.2)+tone(1980, 1980, 0.5, 0.09),
      'err': tone(300, 220, 0.25, 0.22, 4), 'shut': shutter()}
SC = [5.4, 10.4, 20.2, 23.7, 28.2, 32.3, 37.3, 43.6, 47.4, 50.0, 55.0, 58.1]
ev = [(s, 'soft') for s in SC]
ev += [(0.3, 'pop'), (6.7, 'pop'), (6.9, 'pop'), (7.1, 'pop'), (12.9, 'tick'), (13.25, 'pop'), (15.6, 'tick'), (15.9, 'pop'), (17.75, 'tick'), (18.62, 'pop'),
       (19.44, 'tick'), (19.6, 'ding'), (20.3, 'pop'), (25.3, 'pop'), (25.65, 'err'), (27.1, 'pop'), (31.0, 'pop'), (32.86, 'shut'), (34.3, 'tick'), (34.55, 'pop'),
       (36.5, 'ding'), (39.56, 'tick'), (40.24, 'tick'), (40.66, 'tick'), (41.6, 'err'), (46.16, 'pop'), (51.9, 'tick'), (52.2, 'pop'), (54.6, 'tick'), (54.9, 'ding'), (56.0, 'pop'), (61.0, 'ding')]
for a, k in ev: add(a, SS[k]*0.35/0.3)
au = np.clip(au, -1, 1); w = wave.open(OUT+'sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((au*32767).astype(np.int16).tobytes()); w.close()
print('ok')
