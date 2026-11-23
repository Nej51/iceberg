import sys, json, wave, numpy as np
sys.path.insert(0, 'scripts')
import ui_iphone as ui
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw, ImageFont
ui.init()
OUT = 'public/'
BG = (0, 0, 0); CARD = (28, 28, 30); SEPC = (56, 56, 58); G2 = (152, 152, 159)
WHITE = (255, 255, 255); GRN = (52, 199, 89); BLU = (10, 132, 255)
MONO = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', s)
MONOB = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', s)
TG = (60, 230, 110)

def status(d, time='21:40', fill=WHITE, net=False):
    d.text((70, 44), time, font=FI(25, 'SemiBold'), fill=fill, anchor='lm')
    d.rounded_rectangle([SW/2-64, 22, SW/2+64, 62], 21, fill=(0, 0, 0))
    if net:
        for i in range(4): d.rounded_rectangle([452+i*9, 50-6-i*4, 458+i*9, 52], 2, fill=fill)
    else:  # pas de réseau
        d.text((470, 44), 'SOS', font=FI(17, 'Bold'), fill=fill, anchor='mm')
    d.rounded_rectangle([500, 34, 540, 54], 6, fill=fill); d.text((520, 44), '62', font=FI(15, 'Bold'), fill=(0, 0, 0) if fill == WHITE else WHITE, anchor='mm')
def homebar(d, c=WHITE): d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=c)
def save(im, n): im.save(OUT+n+'.png')

# ---------- icônes (dessins simples, pas les vraies) ----------
def ic_bitchat(s):
    ic = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(ic)
    d.rounded_rectangle([0, 0, s-1, s-1], int(s*0.23), fill=(14, 14, 16), outline=(70, 70, 76), width=max(1, s//80))
    d.text((s/2, s/2), 'BIT', font=MONO(int(s*0.3)), fill=(225, 225, 230), anchor='mm'); return ic
def ic_organic(s):
    ic = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(ic)
    d.rounded_rectangle([0, 0, s-1, s-1], int(s*0.23), fill=(46, 160, 90))
    d.ellipse([s*0.28, s*0.16, s*0.72, s*0.6], fill=WHITE)
    d.polygon([(s*0.31, s*0.47), (s*0.69, s*0.47), (s*0.5, s*0.84)], fill=WHITE)
    d.ellipse([s*0.40, s*0.28, s*0.60, s*0.48], fill=(46, 160, 90)); return ic
def ic_kiwix(s):
    ic = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(ic)
    d.rounded_rectangle([0, 0, s-1, s-1], int(s*0.23), fill=(250, 250, 250))
    d.ellipse([s*0.2, s*0.3, s*0.72, s*0.74], fill=(40, 40, 44)); d.ellipse([s*0.58, s*0.26, s*0.8, s*0.48], fill=(40, 40, 44))
    d.line([(s*0.78, s*0.4), (s*0.92, s*0.5)], fill=(40, 40, 44), width=max(2, s//30))
    d.line([(s*0.4, s*0.72), (s*0.38, s*0.84)], fill=(40, 40, 44), width=max(2, s//40)); d.line([(s*0.52, s*0.72), (s*0.54, s*0.84)], fill=(40, 40, 44), width=max(2, s//40))
    return ic
for f, n in [(ic_bitchat, 'ic_bitchat'), (ic_organic, 'ic_organic'), (ic_kiwix, 'ic_kiwix')]: f(400).save(OUT+n+'.png')

# ---------- App Store (mode sombre) ----------
def shot_bitchat(im, x, y, w, h):
    d = ImageDraw.Draw(im); d.rounded_rectangle([x, y, x+w, y+h], 26, fill=(8, 8, 10), outline=(50, 50, 55), width=2)
    d.text((x+w/2, y+90), 'bitchat', font=MONOB(36), fill=TG, anchor='mm')
    for k, t in enumerate(['offline communication', 'end-to-end encryption', 'no phone number', 'mesh relay']):
        d.text((x+26, y+170+k*60), '› '+t, font=MONO(17), fill=(170, 230, 180), anchor='lm')
def shot_map(im, x, y, w, h):
    d = ImageDraw.Draw(im); d.rounded_rectangle([x, y, x+w, y+h], 26, fill=(232, 236, 222))
    for k in range(6): d.line([(x, y+60+k*80), (x+w, y+20+k*90)], fill=(255, 255, 255), width=10)
    d.line([(x+80, y), (x+140, y+h)], fill=(250, 210, 110), width=14)
    d.polygon([(x+40, y+300), (x+170, y+260), (x+200, y+380), (x+60, y+420)], fill=(190, 225, 170))
    d.ellipse([x+w/2-16, y+h/2-16, x+w/2+16, y+h/2+16], fill=BLU, outline=WHITE, width=5)
def shot_wiki(im, x, y, w, h):
    d = ImageDraw.Draw(im); d.rounded_rectangle([x, y, x+w, y+h], 26, fill=(250, 250, 250))
    d.text((x+24, y+60), 'Wikipédia', font=FI(30, 'Bold'), fill=(20, 20, 20), anchor='lm')
    for k in range(9): d.rounded_rectangle([x+24, y+110+k*36, x+24+[250, 230, 260, 200, 240, 180, 255, 220, 150][k], y+126+k*36], 5, fill=(200, 200, 205))
def appstore(icon, l1, l2, sub, cat, notes, shot, btn='Obtenir'):
    im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im); status(d, '21:38', net=True)
    d.ellipse([22, 80, 82, 140], fill=(44, 44, 46)); d.line([(58, 96), (44, 110), (58, 124)], fill=WHITE, width=4)
    ic = icon(176); im.paste(ic, (30, 178), ic)
    d.text((232, 200 if l2 else 214), l1, font=FI(32, 'Bold'), fill=WHITE, anchor='lm')
    if l2: d.text((232, 240), l2, font=FI(32, 'Bold'), fill=WHITE, anchor='lm')
    d.text((232, 278), sub, font=FI(21), fill=G2, anchor='lm')
    bw = 150; d.rounded_rectangle([232, 306, 232+bw, 352], 23, fill=BLU)
    d.text((232+bw/2, 329), btn, font=FI(23, 'Bold'), fill=WHITE, anchor='mm')
    d.line([(30, 384), (SW, 384)], fill=SEPC)
    for i, (a, b, c) in enumerate([(notes, '4,6', '★★★★★'), ("CATÉGORIE D'ÂGE", '4+', 'Ans'), ('CATÉGORIE', '', cat)]):
        cx = 100+i*172
        d.text((cx, 412), a, font=FI(15, 'SemiBold'), fill=G2, anchor='mm')
        if b: d.text((cx, 452), b, font=FI(34, 'Bold'), fill=(170, 170, 176), anchor='mm')
        else: d.ellipse([cx-18, 434, cx+18, 470], outline=(170, 170, 176), width=4)
        d.text((cx, 492), c, font=FI(19 if i else 20), fill=G2, anchor='mm')
        if i: d.line([(cx-86, 400), (cx-86, 500)], fill=SEPC)
    d.line([(30, 522), (SW, 522)], fill=SEPC)
    d.text((30, 560), 'Prix', font=FI(30, 'Bold'), fill=WHITE, anchor='lm'); d.text((570, 560), 'Gratuit', font=FI(26, 'SemiBold'), fill=GRN, anchor='rm')
    d.text((30, 640), 'Aperçu', font=FI(30, 'Bold'), fill=WHITE, anchor='lm')
    for i in range(2): shot(im, 30+i*330, 680, 310, 480)
    d.rounded_rectangle([30, 1170, 570, 1262], 46, fill=(30, 30, 34))
    for i, t in enumerate(["Aujourd'hui", 'Jeux', 'Apps', 'Arcade', 'Recherche']):
        d.text((84+i*108, 1240), t, font=FI(15, 'Medium'), fill=BLU if i == 4 else (230, 230, 230), anchor='mm')
        d.rounded_rectangle([70+i*108, 1186, 98+i*108, 1214], 7, outline=BLU if i == 4 else (230, 230, 230), width=3)
    homebar(d); return im
save(appstore(ic_bitchat, 'bitchat mesh', '', 'Messagerie sans internet', 'Réseaux sociaux', 'NOTES', shot_bitchat), 'si_bc_store')
save(appstore(ic_organic, 'Organic Maps', '', 'Cartes et GPS hors ligne', 'Navigation', 'NOTES', shot_map), 'si_om_store')
save(appstore(ic_kiwix, 'Kiwix', '', 'Wikipédia hors ligne', 'Référence', 'NOTES', shot_wiki), 'si_kx_store')

# ---------- BitChat : discussion (style terminal) ----------
im = Image.new('RGB', (SW, SH), (6, 6, 8)); d = ImageDraw.Draw(im); status(d)
d.text((30, 110), 'bitchat/', font=MONOB(28), fill=TG, anchor='lm'); d.text((200, 110), '#mesh', font=MONO(24), fill=(150, 150, 155), anchor='lm')
d.text((570, 110), '3 à proximité', font=MONO(18), fill=TG, anchor='rm')
d.line([(0, 145), (SW, 145)], fill=(40, 40, 44), width=2)
msgs = [('@lea', "quelqu'un a du réseau ?"), ('@tom', 'non, rien depuis 1 h'), ('@marc', 'on se retrouve à la place ?'), ('@moi', 'ok, j’arrive dans 10 min'), ('@lea', 'super, à tout de suite')]
y = 190
for who, txt in msgs:
    c = (110, 180, 255) if who == '@moi' else TG
    d.text((30, y), '<'+who+'>', font=MONOB(22), fill=c, anchor='lm'); d.text((30, y+36), txt, font=MONO(22), fill=(225, 225, 230), anchor='lm'); y += 92
d.rounded_rectangle([20, 1150, 580, 1220], 16, outline=(60, 60, 66), width=2); d.text((40, 1185), '> écris un message…', font=MONO(22), fill=(110, 110, 116), anchor='lm')
d.text((SW/2, 1110), 'Bluetooth · sans internet', font=MONO(18), fill=(120, 120, 126), anchor='mm')
homebar(d); save(im, 'si_bc_chat')

# ---------- Organic Maps : télécharger des cartes ----------
im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im); status(d, net=True)
d.ellipse([22, 80, 82, 140], fill=(44, 44, 46)); d.line([(58, 96), (44, 110), (58, 124)], fill=WHITE, width=4)
d.text((SW/2, 110), 'Télécharger des cartes', font=FI(24, 'SemiBold'), fill=WHITE, anchor='mm')
d.rounded_rectangle([22, 160, 578, 214], 14, fill=(28, 28, 30)); d.text((50, 187), 'Rechercher', font=FI(22), fill=G2, anchor='lm')
d.text((30, 260), 'FRANCE', font=FI(18, 'SemiBold'), fill=G2, anchor='lm')
regs = ['Auvergne-Rhône-Alpes', 'Bretagne', 'Grand Est', 'Île-de-France', 'Normandie', 'Nouvelle-Aquitaine', 'Occitanie', "Provence-Alpes-Côte d'Azur"]
d.rounded_rectangle([22, 280, 578, 280+len(regs)*82], 20, fill=(28, 28, 30))
for i, r in enumerate(regs):
    yy = 280+i*82+41; d.text((44, yy), r, font=FI(24), fill=WHITE, anchor='lm')
    d.ellipse([520, yy-18, 556, yy+18], outline=GRN, width=3); d.line([(538, yy-9), (538, yy+7)], fill=GRN, width=3); d.line([(530, yy), (538, yy+8), (546, yy)], fill=GRN, width=3)
    if i < len(regs)-1: d.line([(44, yy+41), (578, yy+41)], fill=SEPC)
homebar(d); save(im, 'si_om_dl')
im2 = im.copy(); d = ImageDraw.Draw(im2); yy = 280+3*82+41
d.rectangle([24, yy-40, 576, yy+40], fill=(46, 46, 50)); d.text((44, yy), 'Île-de-France', font=FI(24), fill=WHITE, anchor='lm')
d.ellipse([520, yy-18, 556, yy+18], fill=GRN); d.line([(530, yy), (536, yy+7), (548, yy-8)], fill=WHITE, width=4)
d.text((500, yy), 'Téléchargée', font=FI(18), fill=GRN, anchor='rm'); save(im2, 'si_om_dl_ok')

# ---------- Organic Maps : carte hors ligne + GPS ----------
im = Image.new('RGB', (SW, SH), (234, 238, 226)); d = ImageDraw.Draw(im)
import random; random.seed(3)
d.polygon([(0, 700), (250, 640), (330, 900), (60, 980), (0, 960)], fill=(195, 228, 175))
d.polygon([(400, 200), (600, 160), (600, 480), (450, 430)], fill=(170, 210, 240))
for k in range(9): d.line([(0, 120+k*140), (SW, 60+k*150)], fill=WHITE, width=12)
for k in range(5): d.line([(60+k*130, 0), (120+k*120, SH)], fill=WHITE, width=10)
d.line([(170, 0), (260, SH)], fill=(250, 205, 100), width=20); d.line([(0, 520), (SW, 430)], fill=(250, 205, 100), width=18)
d.text((380, 560), 'Paris', font=FI(26, 'Bold'), fill=(60, 60, 70), anchor='mm')
d.rounded_rectangle([22, 70, 578, 136], 33, fill=WHITE); d.text((60, 103), 'Rechercher', font=FI(24), fill=(140, 140, 146), anchor='lm')
d.ellipse([28, 80, 46, 98], outline=(140, 140, 146), width=3)
for r, a in [(90, 50), (60, 90)]:
    lay = Image.new('RGBA', (SW, SH), (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse([300-r, 760-r, 300+r, 760+r], fill=(10, 132, 255, a)); im.paste(lay, (0, 0), lay)
d = ImageDraw.Draw(im); d.ellipse([280, 740, 320, 780], fill=BLU, outline=WHITE, width=6)
d.rounded_rectangle([170, 1000, 430, 1056], 28, fill=(30, 30, 34)); d.text((300, 1028), 'Mode avion · GPS actif', font=FI(19, 'SemiBold'), fill=WHITE, anchor='mm')
d.rounded_rectangle([0, 1100, SW, SH], 0, fill=WHITE)
for i, t in enumerate(['Rechercher', 'Itinéraire', 'Signets', 'Menu']):
    d.text((75+i*150, 1180), t, font=FI(18, 'Medium'), fill=(60, 60, 66), anchor='mm'); d.rounded_rectangle([58+i*150, 1130, 92+i*150, 1160], 8, outline=(60, 60, 66), width=3)
homebar(d, (0, 0, 0)); save(im, 'si_om_map')

# ---------- Kiwix : bibliothèque + article ----------
im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im); status(d, net=True)
d.text((30, 120), 'Bibliothèque', font=FI(40, 'Bold'), fill=WHITE, anchor='lm')
d.rounded_rectangle([22, 170, 578, 224], 14, fill=(28, 28, 30)); d.text((50, 197), 'wikipedia français', font=FI(22), fill=WHITE, anchor='lm')
rows = [('Wikipédia (français)', 'Complet, avec images'), ('Wikipédia (français)', 'Sans images, plus léger'), ('Wikipédia (français)', 'Mini, le plus léger'), ('Wikivoyage (français)', 'Guides de voyage')]
d.rounded_rectangle([22, 260, 578, 260+len(rows)*120], 20, fill=(28, 28, 30))
for i, (a, b) in enumerate(rows):
    yy = 260+i*120+60; wi = ic_kiwix(70); im.paste(wi, (40, int(yy-35)), wi)
    d.text((130, yy-18), a, font=FI(24, 'SemiBold'), fill=WHITE, anchor='lm'); d.text((130, yy+18), b, font=FI(19), fill=G2, anchor='lm')
    d.ellipse([520, yy-18, 556, yy+18], outline=BLU, width=3); d.line([(538, yy-9), (538, yy+7)], fill=BLU, width=3); d.line([(530, yy), (538, yy+8), (546, yy)], fill=BLU, width=3)
    if i < len(rows)-1: d.line([(130, yy+60), (578, yy+60)], fill=SEPC)
homebar(d); save(im, 'si_kx_lib')
im = Image.new('RGB', (SW, SH), (255, 255, 255)); d = ImageDraw.Draw(im); status(d, fill=(0, 0, 0))
d.rounded_rectangle([22, 80, 578, 134], 14, fill=(238, 238, 242)); d.text((300, 107), 'Bluetooth', font=FI(22), fill=(60, 60, 66), anchor='mm')
d.text((30, 190), 'Bluetooth', font=FI(44, 'Bold'), fill=(20, 20, 20), anchor='lm'); d.line([(30, 230), (570, 230)], fill=(210, 210, 215), width=2)
txt = "Le Bluetooth est une norme de communication sans fil à courte portée. Elle permet à deux appareils proches d'échanger des données sans câble et sans connexion à internet."
yy = 270; line = ''
for w in txt.split():
    t2 = (line+' '+w).strip()
    if d.textlength(t2, font=FI(24)) > 540: d.text((30, yy), line, font=FI(24), fill=(30, 30, 30), anchor='lm'); yy += 40; line = w
    else: line = t2
d.text((30, yy), line, font=FI(24), fill=(30, 30, 30), anchor='lm')
d.text((30, yy+70), 'Histoire', font=FI(32, 'Bold'), fill=(20, 20, 20), anchor='lm')
for k in range(10): d.rounded_rectangle([30, yy+120+k*40, 30+[520, 500, 540, 470, 510, 530, 380, 520, 490, 300][k], yy+138+k*40], 6, fill=(215, 215, 220))
d.rounded_rectangle([190, 1180, 410, 1236], 28, fill=(30, 30, 34)); d.text((300, 1208), 'Hors ligne', font=FI(21, 'SemiBold'), fill=WHITE, anchor='mm')
homebar(d, (0, 0, 0)); save(im, 'si_kx_art')

json.dump({'duree': 64.23}, open('src/data.json', 'w'))

# ---------- sons ----------
T = 65.0; SR = 44100; au = np.zeros(int((T+0.5)*SR), np.float32)
def add(t, x):
    i = int(t*SR); x = x[:len(au)-i]; au[i:i+len(x)] += x
def tone(f0, f1, dd, v, dec=6):
    n = int(dd*SR); k = np.linspace(0, 1, n); ph = 2*np.pi*np.cumsum(f0+(f1-f0)*k)/SR
    return (np.sin(ph)*np.exp(-k*dec)*v).astype(np.float32)
def soft():
    n = int(0.42*SR); k = np.arange(n)/SR; env = np.minimum(1, k/0.012)*np.exp(-k*11)
    return ((np.sin(2*np.pi*587.33*k)*0.6+np.sin(2*np.pi*880*k)*0.28+np.sin(2*np.pi*1174.66*k)*0.08)*env*0.30).astype(np.float32)
err = np.concatenate([tone(330, 300, 0.09, 0.2, 4), np.zeros(int(0.04*SR), np.float32), tone(300, 260, 0.12, 0.2, 4)])
S = {'soft': soft(), 'pop': tone(520, 900, 0.09, 0.2), 'tick': tone(1400, 1100, 0.06, 0.18), 'ding': tone(1320, 1320, 0.5, 0.2)+tone(1980, 1980, 0.5, 0.09), 'err': err}
sfx = [(2.84, 'pop'), (3.1, 'pop'), (3.36, 'pop'), (6.5, 'soft'), (7.9, 'tick'), (8.6, 'soft'), (10.74, 'soft'), (13.24, 'soft'), (14.52, 'soft'), (15.9, 'tick'), (16.8, 'tick'), (17.84, 'soft'),
       (21.26, 'soft'), (22.6, 'tick'), (24.18, 'tick'), (25.28, 'tick'), (26.4, 'soft'), (27.3, 'ding'), (27.7, 'pop'), (27.9, 'pop'), (28.1, 'pop'), (29.48, 'soft'), (34.6, 'soft'),
       (37.7, 'pop'), (38.76, 'err'), (40.54, 'soft'), (42.72, 'err'), (45.24, 'soft'), (46.78, 'pop'), (51.02, 'err'), (52.32, 'soft'), (54.78, 'pop'), (58.34, 'soft'), (60.58, 'soft')]
for t, k in sfx: add(max(0, t), S[k]*0.35/0.3)
au = np.clip(au, -1, 1); w = wave.open(OUT+'sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((au*32767).astype(np.int16).tobytes()); w.close()
print('ok')
