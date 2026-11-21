# Écrans « Double capture » (app Appareil photo, iPhone 17+). Lancer depuis kit/.
import sys, json, math, wave, random
import numpy as np
sys.path.insert(0, 'scripts')
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw, ImageFilter
OUT = 'public/'
W = (255, 255, 255); YEL = (255, 214, 10); G = (150, 150, 156); RED = (235, 77, 72)

def scene_rear():
    """Vue de la caméra arrière : scène de concert nuit (dessinée)."""
    h = 1300
    g = np.linspace(0, 1, h)[:, None, None]
    a = np.array((10, 8, 40)) * (1 - g) + np.array((40, 14, 70)) * g
    im = Image.fromarray(np.broadcast_to(a, (h, SW, 3)).astype(np.uint8)).convert('RGBA')
    L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for x0, c in [(80, (80, 120, 255)), (220, (190, 80, 255)), (380, (60, 160, 255)), (520, (200, 90, 255))]:
        d.polygon([(x0 - 8, 230), (x0 + 8, 230), (300 + (x0 - 300) * 0.3 + 90, 820), (300 + (x0 - 300) * 0.3 - 90, 820)], fill=c + (70,))
        d.ellipse([x0 - 22, 210, x0 + 22, 254], fill=c + (230,))
    L = L.filter(ImageFilter.GaussianBlur(14)); im = Image.alpha_composite(im, L)
    d = ImageDraw.Draw(im)
    d.rectangle([60, 190, 540, 204], fill=(30, 30, 50))
    d.rectangle([40, 800, 560, 850], fill=(18, 16, 34))  # scène
    for x, s in [(300, 1.0), (180, 0.8), (430, 0.8)]:  # musiciens (silhouettes)
        d.ellipse([x - 20 * s, 640 - 90 * s, x + 20 * s, 640 - 50 * s], fill=(12, 10, 26))
        d.rounded_rectangle([x - 34 * s, 640 - 52 * s, x + 34 * s, 800], 16, fill=(12, 10, 26))
    random.seed(3)
    for i in range(60):  # public (têtes)
        x = random.randint(-20, 620); y = random.randint(860, 1300); r = random.randint(34, 52) * (0.7 + (y - 860) / 900)
        d.ellipse([x - r, y - r, x + r, y + r * 1.4], fill=(14 + i % 6, 10, 30 + i % 10))
    return im.convert('RGB')

def pip_face(w=198, h=265):
    """Vue de la caméra avant : silhouette sans visage, fond salle."""
    im = Image.new('RGB', (w, h)); d = ImageDraw.Draw(im)
    for y in range(h): d.line([(0, y), (w, y)], fill=(int(40 + 30 * y / h), int(26 + 10 * y / h), int(90 + 30 * y / h)))
    d.ellipse([w / 2 - 50, 62, w / 2 + 50, 172], fill=(232, 182, 150))
    d.pieslice([w / 2 - 54, 52, w / 2 + 54, 150], 180, 360, fill=(70, 46, 40))  # cheveux
    d.rounded_rectangle([w / 2 - 95, 180, w / 2 + 95, h + 40], 70, fill=(52, 46, 90))
    d.rectangle([w / 2 - 22, 165, w / 2 + 22, 192], fill=(222, 170, 140))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 26, fill=255)
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0)); out.paste(im, (0, 0), m)
    ImageDraw.Draw(out).rounded_rectangle([0, 0, w - 1, h - 1], 26, outline=(255, 255, 255, 230), width=3)
    return out

def dual_icon(d, x, y, col, s=1.0):
    d.rounded_rectangle([x - 30 * s, y - 22 * s, x + 12 * s, y + 10 * s], 6, outline=col, width=3)
    d.rounded_rectangle([x - 8 * s, y - 6 * s, x + 30 * s, y + 24 * s], 6, fill=(0, 0, 0), outline=col, width=3)
    d.ellipse([x + 5 * s, y + 1 * s, x + 17 * s, y + 13 * s], fill=col)
    d.pieslice([x + 0 * s, y + 13 * s, x + 22 * s, y + 31 * s], 180, 360, fill=col)

def six_dots(d, x, y, ring=W, r=33):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(28, 28, 30), outline=ring, width=3)
    for i in range(3):
        for j in range(2): d.ellipse([x - 16 + i * 13 - 4.5, y - 7 + j * 13 - 4.5, x - 16 + i * 13 + 4.5, y - 7 + j * 13 + 4.5], fill=W)

def chrome(im, mode='VIDÉO', hd='HD 60', dual=False, rec=None, pip=None):
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle([0, 1130, SW, SH], fill=(0, 0, 0, 255))
    d.rectangle([0, 1000, SW, 1130], fill=(0, 0, 0, 90))
    d.rounded_rectangle([SW / 2 - 64, 20, SW / 2 + 64, 62], 21, fill=(0, 0, 0))
    d.ellipse([SW / 2 + 3, 44, SW / 2 + 11, 52], fill=(52, 199, 89))
    if rec is not None:
        d.rounded_rectangle([SW / 2 - 78, 112, SW / 2 + 78, 152], 12, fill=RED)
        d.text((SW / 2, 132), rec, font=FI(24, 'SemiBold'), fill=W, anchor='mm')
    elif mode == 'VIDÉO':
        x = 267 if dual else 300
        d.text((x, 124), hd.split()[0], font=FI(25, 'SemiBold'), fill=W, anchor='mm')
        d.text((x, 146), hd.split()[1], font=FI(14, 'SemiBold'), fill=W, anchor='mm')
        if dual: dual_icon(d, 333, 131, YEL, 0.9)
    if mode == 'VIDÉO' and rec is None:
        for x, l in zip([241, 300, 357, 416, 474], ['0,5', '1×', '2', '4', '8']):
            if l == '1×': d.ellipse([x - 28, 909, x + 28, 965], fill=(40, 40, 40, 220))
            d.text((x, 937), l, font=FI(22, 'SemiBold'), fill=YEL if l == '1×' else W, anchor='mm')
    # déclencheur
    d.ellipse([241, 1015, 359, 1133], fill=(0, 0, 0, 0), outline=(200, 200, 200), width=6)
    if rec is not None: d.rounded_rectangle([280, 1054, 320, 1094], 8, fill=RED)
    elif mode == 'PHOTO': d.ellipse([251, 1025, 349, 1123], fill=W)
    else: d.ellipse([250, 1024, 350, 1124], fill=RED)
    if rec is None:
        six_dots(d, 513, 1074, ring=YEL if dual else (120, 120, 126))
        d.ellipse([51, 1183, 121, 1253], fill=(40, 40, 42))
        d.ellipse([478, 1183, 548, 1253], fill=(40, 40, 42))
        d.arc([494, 1199, 532, 1237], 200, 340, fill=W, width=4); d.arc([494, 1199, 532, 1237], 20, 160, fill=W, width=4)
        d.rounded_rectangle([137, 1190, 463, 1246], 28, fill=(30, 30, 32))
        labs = {'VIDÉO': [('CINÉMATIQUE', 160), ('VIDÉO', 300), ('PHOTO', 414)], 'PHOTO': [('VIDÉO', 186), ('PHOTO', 300), ('PORTRAIT', 418)]}[mode]
        for l, x in labs:
            if l == mode: d.rounded_rectangle([x - 62, 1195, x + 62, 1241], 23, fill=(48, 48, 50))
            d.text((x, 1218), l, font=FI(21, 'SemiBold'), fill=YEL if l == mode else W, anchor='mm')
    else:
        d.ellipse([478, 1043, 548, 1105], fill=(40, 40, 42)); d.ellipse([500, 1061, 526, 1087], fill=W)
    if pip:
        im.paste(pip_face(), pip, pip_face())
    d.rounded_rectangle([SW / 2 - 70, 1278, SW / 2 + 70, 1287], 5, fill=W)
    return im

REAR = scene_rear()
def base(): return REAR.copy()

def menu_sheet():
    im = base().filter(ImageFilter.GaussianBlur(10)); im = Image.blend(im, Image.new('RGB', im.size, (0, 0, 0)), 0.55)
    d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle([60, 30, 170, 66], 18, fill=(110, 110, 116)); d.text((115, 48), 'Modifier', font=FI(17, 'SemiBold'), fill=W, anchor='mm')
    d.text((300, 124), 'HD', font=FI(25, 'SemiBold'), fill=W, anchor='mm'); d.text((300, 146), '60', font=FI(14, 'SemiBold'), fill=W, anchor='mm')
    d.rounded_rectangle([14, 451, 586, 1288], 60, fill=(105, 105, 110, 245))
    d.rounded_rectangle([272, 465, 328, 471], 3, fill=(170, 170, 176))
    items = [('FLASH',), ('EXPOSITION',), ('ACTION',), ('DOUBLE', 'CAPTURE'), ('FORMAT',), ('OUVERTURE', 'DE L’OBJECTIF'), ('MISE AU POINT',), ('OBTURATION',), ('BALANCE', 'DES BLANCS'), ('HISTOGRAMME',)]
    for i, lab in enumerate(items):
        if i < 9: x = [128, 300, 472][i % 3]; y = [576, 761, 946][i // 3]
        else: x, y = 300, 1131
        d.ellipse([x - 51, y - 51, x + 51, y + 51], fill=(62, 62, 66))
        c = (235, 235, 240)
        if i == 0: d.polygon([(x + 4, y - 26), (x - 12, y + 4), (x, y + 4), (x - 4, y + 26), (x + 12, y - 4), (x, y - 4)], fill=c); d.line([(x - 20, y - 20), (x + 20, y + 20)], fill=c, width=3)
        if i == 1: d.text((x, y - 4), '±', font=FI(44, 'Regular'), fill=c, anchor='mm')
        if i == 2:
            for k in range(3): d.line([(x - 26, y - 10 + k * 10), (x - 8, y - 10 + k * 10)], fill=c, width=3)
            d.ellipse([x + 4, y - 26, x + 14, y - 16], fill=c); d.line([(x + 8, y - 14), (x + 2, y + 6), (x + 14, y + 22)], fill=c, width=4); d.line([(x - 20, y - 22), (x + 22, y + 22)], fill=c, width=3)
        if i == 3: dual_icon(d, x, y, c, 1.0)
        if i == 4: d.text((x, y - 10), 'HD', font=FI(26, 'SemiBold'), fill=c, anchor='mm'); d.text((x, y + 16), '60', font=FI(18, 'SemiBold'), fill=c, anchor='mm')
        if i == 5:
            d.ellipse([x - 24, y - 24, x + 24, y + 24], outline=c, width=3)
            for k in range(6):
                a = k * math.pi / 3; d.line([(x + 24 * math.cos(a), y + 24 * math.sin(a)), (x + 10 * math.cos(a + 1.2), y + 10 * math.sin(a + 1.2))], fill=c, width=2)
        if i == 6:
            for sx, sy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]: d.line([(x + sx * 20, y + sy * 8), (x + sx * 20, y + sy * 20), (x + sx * 8, y + sy * 20)], fill=c, width=3)
            d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=c)
        if i == 7:
            for k in range(14):
                a = k * 2 * math.pi / 14; d.ellipse([x + 22 * math.cos(a) - 2, y + 22 * math.sin(a) - 2, x + 22 * math.cos(a) + 2, y + 22 * math.sin(a) + 2], fill=c)
            d.line([(x, y), (x, y - 18)], fill=c, width=3)
        if i == 8: d.ellipse([x + 2, y - 22, x + 24, y], outline=c, width=3); d.rounded_rectangle([x - 26, y - 6, x + 14, y + 16], 11, outline=c, width=3)
        if i == 9: d.line([(x - 26, y + 14), (x + 26, y + 14)], fill=c, width=3); d.line([(x - 22, y + 10), (x - 10, y - 8), (x - 2, y), (x + 8, y - 18), (x + 20, y + 10)], fill=c, width=3)
        for k, l in enumerate(lab):
            d.text((x, y + 77 + k * 27), l, font=FI(19, 'SemiBold'), fill=(232, 232, 236), anchor='mm')
    return im

PIP = (383, 110)
chrome(base(), 'PHOTO').save(OUT + 'dc_photo.png')
chrome(base(), 'VIDÉO', 'HD 60').save(OUT + 'dc_video.png')
menu_sheet().save(OUT + 'dc_menu.png')
chrome(base(), 'VIDÉO', 'HD 30', dual=True, pip=PIP).save(OUT + 'dc_dual.png')
chrome(base(), 'VIDÉO', 'HD 30', dual=True, rec='00:00:03', pip=PIP).save(OUT + 'dc_rec.png')
chrome(base(), 'VIDÉO', 'HD 30', dual=True, rec='00:00:08').save(OUT + 'dc_rec_nopip.png')
pip_face().save(OUT + 'dc_pip.png')
REAR.save(OUT + 'dc_rear.png')
json.dump({'duree': 64.43}, open('src/data.json', 'w'))

# ---- sons
SR = 44100; N = int(SR * 64.5); au = np.zeros(N)
def add(t, x):
    i = int(t * SR); j = min(N, i + len(x)); au[i:j] += x[:j - i]
def tone(f0, f1, dd, v, dec=6):
    tt = np.arange(int(SR * dd)) / SR; f = np.linspace(f0, f1, len(tt)); return v * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-dec * tt / dd)
def soft(): return tone(660, 660, 0.6, 0.12, 5) + np.pad(tone(990, 990, 0.45, 0.06, 5), (0, int(SR * 0.15)))
S = {'soft': soft(), 'pop': tone(520, 900, 0.09, 0.2), 'tick': tone(1400, 1100, 0.06, 0.18), 'ding': tone(1320, 1320, 0.5, 0.2) + tone(1980, 1980, 0.5, 0.09), 'err': tone(300, 220, 0.25, 0.22, 4)}
SC = [2.0, 6.5, 22.0, 25.3, 28.3, 31.0, 39.0, 43.1, 47.1, 51.2, 53.2, 58.5, 60.7]
ev = [(s, 'soft') for s in SC] + [(t, 'pop') for t in (8.8, 12.7, 14.9, 21.0, 26.2, 26.9, 27.6)] + [(t, 'tick') for t in (45.0, 45.3, 45.6, 45.9, 46.2, 49.3)] + \
     [(21.2, 'ding'), (42.3, 'ding'), (33.0, 'err'), (36.5, 'err')]
for t, k in ev: add(t, S[k])
w = wave.open(OUT + 'sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(au * 0.35 / 0.35, -1, 1) * 32767 * 1.0).astype(np.int16).tobytes()); w.close()
print('ok')
