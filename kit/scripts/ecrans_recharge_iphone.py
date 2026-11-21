# Écrans « Recharger un iPhone avec un iPhone » (21/11/2026). Lancer depuis kit/.
import sys, math
sys.path.insert(0, 'scripts')
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw, ImageFilter
OUT = 'public/'
W = (255, 255, 255); GRN = (52, 199, 89); RED = (255, 59, 48); GRY = (142, 142, 147)

def wall():
    # fond sombre à vagues grises (inspiré de son fond d'écran)
    im = Image.new('RGB', (SW, SH), (24, 23, 24)); d = ImageDraw.Draw(im, 'RGBA')
    for k in range(7):
        pts = [(x, 200 + k * 170 + 140 * math.sin(x / 140 + k * 0.9)) for x in range(-20, SW + 40, 10)]
        poly = pts + [(SW + 40, SH + 40), (-20, SH + 40)]
        d.polygon(poly, fill=(70 + k * 6, 66 + k * 6, 66 + k * 6, 46))
        d.line(pts, fill=(200, 200, 200, 70), width=2)
    return im.filter(ImageFilter.GaussianBlur(2))

def batt_icon(d, x, y, pct, charging):
    col = GRN if charging else (RED if pct <= 10 else W)
    d.rounded_rectangle([x, y, x + 40, y + 20], 6, outline=(255, 255, 255, 120), width=2)
    d.rounded_rectangle([x + 42, y + 6, x + 45, y + 14], 1, fill=(255, 255, 255, 120))
    w = max(4, int(36 * pct / 100)); d.rounded_rectangle([x + 2, y + 2, x + 2 + w, y + 18], 4, fill=col)
    if charging: d.polygon([(x + 22, y + 2), (x + 14, y + 11), (x + 20, y + 11), (x + 17, y + 18), (x + 26, y + 8), (x + 20, y + 8)], fill=W)

def status(d, pct, charging, dark=True, time=None):
    c = W if dark else (0, 0, 0)
    d.rounded_rectangle([SW / 2 - 64, 22, SW / 2 + 64, 62], 21, fill=(0, 0, 0))
    if time: d.text((66, 44), time, font=FI(24, 'SemiBold'), fill=c, anchor='lm')
    else: d.text((50, 44), 'Orange F', font=FI(22), fill=c, anchor='lm')
    for i in range(4): d.rounded_rectangle([420 + i * 9, 48 - i * 4, 426 + i * 9, 54], 2, fill=c)
    batt_icon(d, 500, 34, pct, charging)

def lock(pct, charging):
    im = wall(); d = ImageDraw.Draw(im, 'RGBA'); status(d, pct, charging)
    d.text((SW / 2, 125), 'samedi 21 novembre', font=FI(26, 'SemiBold'), fill=(235, 235, 240), anchor='mm')
    d.text((SW / 2, 225), '21:47', font=FI(150, 'Bold'), fill=(240, 240, 245), anchor='mm')
    if charging:
        d.rounded_rectangle([SW / 2 - 150, 610, SW / 2 + 150, 690], 40, fill=(0, 0, 0, 140))
        d.polygon([(205, 630), (190, 652), (202, 652), (196, 672), (216, 646), (204, 646)], fill=GRN)
        d.text((232, 650), f'En charge : {pct} %', font=FI(28, 'SemiBold'), fill=W, anchor='lm')
    elif pct <= 10:
        d.rounded_rectangle([SW / 2 - 190, 610, SW / 2 + 190, 690], 40, fill=(0, 0, 0, 140))
        d.text((SW / 2, 650), f'Batterie faible : {pct} %', font=FI(28, 'SemiBold'), fill=(255, 120, 110), anchor='mm')
    for x in (110, 490):
        d.ellipse([x - 48, 1140, x + 48, 1236], fill=(40, 40, 44, 200))
    d.rounded_rectangle([102, 1166, 118, 1212], 5, fill=W); d.rounded_rectangle([468, 1174, 512, 1206], 7, fill=W); d.ellipse([480, 1180, 500, 1200], fill=(40, 40, 44))
    d.rounded_rectangle([SW / 2 - 70, 1278, SW / 2 + 70, 1287], 5, fill=W)
    return im

def reglages(pct, charging):
    im = Image.new('RGB', (SW, SH), (235, 235, 240)); d = ImageDraw.Draw(im); status(d, pct, charging, dark=False, time='21:47')
    d.ellipse([22, 92, 82, 152], fill=(250, 250, 252), outline=(220, 220, 225)); d.line([(58, 106), (44, 122), (58, 138)], fill=(0, 0, 0), width=4)
    d.text((SW / 2, 122), 'Batterie', font=FI(32, 'SemiBold'), fill=(0, 0, 0), anchor='mm')
    d.rounded_rectangle([24, 200, 576, 400], 40, fill=W)
    d.text((48, 262), f'{pct}', font=FI(74, 'SemiBold'), fill=(0, 0, 0), anchor='lm'); wd = d.textlength(f'{pct}', font=FI(74, 'SemiBold'))
    d.text((60 + wd, 278), '%', font=FI(28, 'SemiBold'), fill=(0, 0, 0), anchor='lm')
    if charging:
        d.polygon([(64, 288), (50, 308), (60, 308), (54, 328), (72, 302), (62, 302)], fill=(48, 160, 70))
        d.text((82, 308), 'En charge', font=FI(28, 'SemiBold'), fill=(48, 160, 70), anchor='lm')
        d.text((552, 308), '80 %', font=FI(24), fill=GRY, anchor='rm')
    else:
        d.text((48, 308), 'Batterie faible', font=FI(28, 'SemiBold'), fill=RED, anchor='lm')
    d.rounded_rectangle([48, 336, 552, 350], 7, fill=(215, 215, 220))
    d.rounded_rectangle([48, 336, 48 + max(14, int(504 * pct / 100)), 350], 7, fill=(70, 160, 80) if charging else RED)
    d.text((40, 460), 'Utilisation quotidienne', font=FI(30, 'SemiBold'), fill=(110, 110, 115), anchor='lm')
    d.rounded_rectangle([24, 490, 576, 1000], 40, fill=W)
    d.text((48, 545), 'Moyenne', font=FI(22), fill=GRY, anchor='lm'); d.text((48, 590), '46 %', font=FI(38, 'SemiBold'), fill=(110, 110, 115), anchor='lm')
    d.text((200, 545), 'Aujourd’hui', font=FI(22), fill=(50, 110, 230), anchor='lm'); d.text((200, 590), '97 %', font=FI(38, 'SemiBold'), fill=(50, 110, 230), anchor='lm')
    hs = [90, 150, 130, 140, 120, 110, 120, 220]
    for i, h in enumerate(hs):
        x = 56 + i * 46; c = (60, 110, 230) if i == 7 else (150, 150, 155)
        d.rounded_rectangle([x, 900 - h, x + 30, 900], 8, fill=c)
        d.text((x + 15, 930), 'SDLMMJVS'[i], font=FI(20), fill=c, anchor='mm')
    d.line([(48, 790), (552, 790)], fill=(200, 200, 205), width=3)
    d.rounded_rectangle([SW / 2 - 70, 1278, SW / 2 + 70, 1287], 5, fill=(0, 0, 0))
    return im

lock(2, False).save(OUT + 'rc_lock_low.png')
lock(3, True).save(OUT + 'rc_lock_chg.png')
lock(64, False).save(OUT + 'rc_lock_ami.png')
reglages(2, False).save(OUT + 'rc_batt_low.png')
reglages(3, True).save(OUT + 'rc_batt_chg.png')
print('ok')

# ---- data.json + sons (temps = voix d'origine, convertis avec m())
import json, wave, numpy as np
CUTS = [5.45, 9.04, 11.0, 12.95, 17.05, 18.36, 19.38, 23.0, 24.3, 29.25, 31.88, 34.6, 39.0, 42.8, 45.48, 47.25, 49.4]
P, BON, BLEN, DUR = 0.42, 31.88, 6.0, 70.47
m = lambda s: s + P * len([c for c in CUTS if c < s]) + (BLEN + P if s > BON else 0)
bo = lambda s: m(BON) + P + s
json.dump({'duree': DUR}, open('src/data.json', 'w'))
SR = 44100; au = np.zeros(int((DUR + 0.5) * SR), np.float32)
def add(t, x):
    i = int(t * SR); x = x[:len(au) - i]; au[i:i + len(x)] += x
def tone(f0, f1, dd, v, dec=6):
    n = int(dd * SR); k = np.linspace(0, 1, n); ph = 2 * np.pi * np.cumsum(f0 + (f1 - f0) * k) / SR
    return (np.sin(ph) * np.exp(-k * dec) * v).astype(np.float32)
def soft():
    n = int(0.42 * SR); k = np.arange(n) / SR; env = np.minimum(1, k / 0.012) * np.exp(-k * 11)
    return ((np.sin(2 * np.pi * 587.33 * k) * 0.6 + np.sin(2 * np.pi * 880 * k) * 0.28 + np.sin(2 * np.pi * 1174.66 * k) * 0.08) * env * 0.30).astype(np.float32)
S = {'soft': soft(), 'pop': tone(520, 900, 0.09, 0.2), 'tick': tone(1400, 1100, 0.06, 0.18), 'ding': tone(1320, 1320, 0.5, 0.2) + tone(1980, 1980, 0.5, 0.09),
     'err': tone(300, 220, 0.25, 0.22, 4), 'swoosh': tone(400, 1200, 0.3, 0.1, 3)}
ev = [(m(s), 'soft') for s in [5.45, 9.04, 17.05, 18.36, 23.0, 29.25, 34.6, 39.0, 42.8, 47.25, 49.4, 52.0]] + [(bo(6.0) + 0.1, 'soft'), (m(31.88), 'soft')]
ev += [(m(a), k) for a, k in [(4.84, 'pop'), (6.3, 'swoosh'), (7.9, 'pop'), (10.14, 'tick'), (10.36, 'tick'), (13.3, 'pop'), (13.9, 'pop'), (14.14, 'swoosh'), (16.26, 'ding'),
      (21.9, 'pop'), (22.54, 'pop'), (23.74, 'err'), (27.84, 'pop'), (28.24, 'pop'), (29.96, 'pop'), (30.9, 'pop'), (33.52, 'pop'), (38.42, 'err'), (43.3, 'ding'), (48.74, 'pop'), (49.02, 'pop')]]
ev += [(bo(a), k) for a, k in [(1.62, 'pop'), (2.34, 'pop'), (3.26, 'pop'), (5.04, 'pop')]]
for a, k in ev: add(a, S[k] * 0.35 / 0.3)
au = np.clip(au, -1, 1); w = wave.open(OUT + 'sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((au * 32767).astype(np.int16).tobytes()); w.close()
print('sons ok', round(m(39.0), 2), round(m(47.25), 2))
