# Écrans « Vider l'iPhone sur une carte SD » (iOS 26, mode sombre). Lancer depuis kit/.
import sys, json, math, wave
import numpy as np
sys.path.insert(0, 'scripts')
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw, ImageFilter
OUT = 'public/'
W = (255, 255, 255); G2 = (152, 152, 158); BLU = (10, 132, 255); ROW = (44, 44, 48); BG = (28, 28, 30); SEPC = (64, 64, 70)
CARD = 'Untitled'

def status(d, t='20:45'):
    d.rounded_rectangle([SW/2-64, 20, SW/2+64, 62], 21, fill=(0, 0, 0))
    d.text((70, 44), t, font=FI(24, 'SemiBold'), fill=W, anchor='lm')
    for i in range(4): d.rounded_rectangle([430+i*9, 48-i*4, 436+i*9, 54], 2, fill=W)
    d.text((474, 44), '4G', font=FI(17, 'SemiBold'), fill=W, anchor='lm')
    d.rounded_rectangle([504, 35, 540, 53], 5, fill=W)

def thumb(w, h, i):
    pal = [((255, 140, 90), (120, 40, 160)), ((40, 120, 255), (20, 220, 200)), ((255, 200, 60), (240, 90, 60)), ((60, 200, 120), (20, 80, 160)),
           ((200, 80, 220), (40, 40, 140)), ((255, 120, 160), (255, 210, 120)), ((80, 160, 255), (160, 80, 255)), ((40, 180, 90), (230, 230, 120)),
           ((255, 90, 90), (90, 30, 120)), ((120, 220, 255), (40, 60, 200)), ((250, 170, 80), (140, 60, 40)), ((150, 120, 255), (255, 140, 200))]
    c1, c2 = pal[i % len(pal)]
    g = np.linspace(0, 1, h)[:, None, None]; a = np.array(c1) * (1-g) + np.array(c2) * g
    im = Image.fromarray(np.broadcast_to(a, (h, w, 3)).astype(np.uint8))
    d = ImageDraw.Draw(im, 'RGBA')  # petit paysage : soleil + montagne
    d.ellipse([w*0.62, h*0.18, w*0.82, h*0.38], fill=(255, 255, 255, 150))
    d.polygon([(0, h), (w*0.35, h*0.5), (w*0.6, h*0.75), (w*0.8, h*0.55), (w, h*0.8), (w, h)], fill=(0, 0, 0, 70))
    return im

def check(d, x, y, r=17):
    d.ellipse([x-r, y-r, x+r, y+r], fill=BLU, outline=W, width=3)
    d.line([(x-8, y), (x-2, y+7), (x+9, y-7)], fill=W, width=4, joint='curve')

def share_icon(d, x, y, col=W, s=1.0):
    d.rounded_rectangle([x-15*s, y-6*s, x+15*s, y+22*s], 5, outline=col, width=3)
    d.rectangle([x-6*s, y-8*s, x+6*s, y-3*s], fill=(40, 40, 44))
    d.line([(x, y-22*s), (x, y+8*s)], fill=col, width=3)
    d.line([(x-9*s, y-13*s), (x, y-22*s), (x+9*s, y-13*s)], fill=col, width=3)

def photos_sel():
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); d = ImageDraw.Draw(im, 'RGBA')
    cw = (SW - 4) // 3; top = 230
    for i in range(18):
        x = (i % 3) * (cw + 2); y = top + (i // 3) * (cw + 2)
        if y > SH: break
        im.paste(thumb(cw, cw, i), (x, y))
        if i < 6: check(d, x + cw - 26, y + cw - 26)
    d.rectangle([0, 0, SW, 225], fill=(0, 0, 0, 235))
    status(d)
    d.text((34, 150), 'Photothèque', font=FI(44, 'Bold'), fill=W, anchor='lm')
    d.rounded_rectangle([440, 128, 566, 172], 22, fill=(60, 60, 66))
    d.text((503, 150), 'OK', font=FI(22, 'SemiBold'), fill=W, anchor='mm')
    # barre du bas flottante
    d.rounded_rectangle([24, 1170, SW-24, 1250], 40, fill=(38, 38, 42, 245), outline=(80, 80, 86))
    share_icon(d, 84, 1208)
    d.text((SW/2, 1210), '6 photos sélectionnées', font=FI(22, 'SemiBold'), fill=W, anchor='mm')
    x = 516; d.rectangle([x-12, 1196, x+12, 1226], outline=W, width=3); d.line([(x-17, 1196), (x+17, 1196)], fill=W, width=3)
    d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=W)
    return im

def share_sheet():
    s = Image.open('/home/claude/in/share.png').convert('RGB')
    s = s.resize((SW, round(s.height * SW / s.width)), Image.LANCZOS).crop((0, 0, SW, SH))
    # flouter les bords (photos perso qui dépassent) + la ligne d'heure perso
    for box in [(0, 280, 26, 660), (574, 280, 600, 660)]:
        s.paste(s.crop(box).filter(ImageFilter.GaussianBlur(14)), box[:2])
    return s

def chev(d, x, y, col=G2):
    d.line([(x-5, y-9), (x+4, y), (x-5, y+9)], fill=col, width=3)

def icon_cloud(d, x, y):
    d.ellipse([x-18, y-6, x+2, y+12], outline=BLU, width=3); d.ellipse([x-8, y-14, x+14, y+8], outline=BLU, width=3); d.ellipse([x+2, y-4, x+20, y+12], outline=BLU, width=3)
    d.rectangle([x-14, y-1, x+16, y+8], fill=ROW); d.line([(x-10, y+12), (x+12, y+12)], fill=BLU, width=3)
def icon_phone(d, x, y): d.rounded_rectangle([x-10, y-17, x+10, y+17], 5, outline=BLU, width=3)
def icon_drive(d, x, y, col=BLU):
    d.rounded_rectangle([x-19, y-6, x+19, y+12], 5, outline=col, width=3)
    d.line([(x-15, y-6), (x-9, y-14), (x+9, y-14), (x+15, y-6)], fill=col, width=3)
    d.ellipse([x+9, y+1, x+14, y+6], fill=col)

def row(d, y, label, ic, last=True, first=True, h=78):
    d.text((106, y), label, font=FI(27), fill=W, anchor='lm'); chev(d, 538, y); ic(d, 64, y)
    if not last: d.line([(106, y+h/2), (566, y+h/2)], fill=SEPC, width=1)

def group(d, y0, n, h=78):
    d.rounded_rectangle([24, y0, SW-24, y0+n*h], 30, fill=ROW)

def explorer(hi=False):
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle([0, 92, SW, SH+40], 44, fill=BG)
    status(d)
    d.ellipse([24, 130, 88, 194], fill=(44, 44, 48)); d.line([(44, 150), (68, 174)], fill=W, width=3); d.line([(68, 150), (44, 174)], fill=W, width=3)
    d.text((SW/2, 162), 'Explorer', font=FI(27, 'SemiBold'), fill=W, anchor='mm')
    d.ellipse([512, 130, 576, 194], fill=(44, 44, 48))
    for dx in (-12, 0, 12): d.ellipse([544+dx-3, 159, 544+dx+3, 165], fill=W)
    d.rounded_rectangle([24, 212, SW-24, 274], 31, fill=(44, 44, 48))
    d.text((84, 243), 'Rechercher', font=FI(26), fill=G2, anchor='lm'); d.ellipse([40, 230, 62, 252], outline=W, width=3)
    d.text((48, 330), 'Favoris', font=FI(30, 'Bold'), fill=W, anchor='lm')
    group(d, 365, 2)
    def dl(d, x, y): d.ellipse([x-16, y-16, x+16, y+16], outline=BLU, width=3); d.line([(x, y-8), (x, y+8)], fill=BLU, width=3); d.line([(x-6, y+2), (x, y+8), (x+6, y+2)], fill=BLU, width=3)
    def doc(d, x, y): d.rounded_rectangle([x-12, y-16, x+12, y+16], 4, outline=BLU, width=3)
    row(d, 404, 'Téléchargements', dl, last=False); row(d, 482, 'Documents', doc)
    d.text((48, 580), 'Emplacements', font=FI(30, 'Bold'), fill=W, anchor='lm')
    group(d, 615, 3)
    row(d, 654, 'iCloud Drive', icon_cloud, last=False); row(d, 732, 'Sur mon iPhone', icon_phone, last=False); row(d, 810, CARD, icon_drive)
    POS['card_row'] = [SW/2, 810]
    d.text((48, 908), 'Tags', font=FI(30, 'Bold'), fill=W, anchor='lm')
    group(d, 943, 2)
    def tag(d, x, y): d.ellipse([x-13, y-13, x+13, y+13], outline=G2, width=3)
    row(d, 982, 'Perso', tag, last=False); row(d, 1060, 'Travail', tag)
    save_bar(d)
    return im

def save_bar(d):
    d.rounded_rectangle([40, 1170, SW-40, 1256], 43, fill=(52, 52, 56), outline=(80, 80, 86))
    im_t = thumb(72, 40, 1); d._image.paste(im_t, (72, 1193))
    d.text((166, 1194), 'Enregistrer sous', font=FI(19), fill=G2, anchor='lm')
    d.text((166, 1226), '6 éléments', font=FI(24), fill=(200, 200, 206), anchor='lm')
    d.rounded_rectangle([412, 1188, 522, 1238], 25, fill=(70, 70, 76)); d.text((467, 1213), 'Tags', font=FI(22), fill=W, anchor='mm')

def folder(d, x, y, s=1.0):
    d.rounded_rectangle([x-46*s, y-30*s, x-6*s, y-18*s], 6, fill=(60, 150, 255))
    d.rounded_rectangle([x-48*s, y-24*s, x+48*s, y+36*s], 9, fill=(80, 170, 255))

def card_view(saved=False):
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); d = ImageDraw.Draw(im, 'RGBA')
    if not saved: d.rounded_rectangle([0, 92, SW, SH+40], 44, fill=BG)
    else: d.rectangle([0, 0, SW, SH], fill=(0, 0, 0))
    status(d)
    yb = 162 if not saved else 120
    d.ellipse([24, yb-32, 88, yb+32], fill=(44, 44, 48)); d.line([(62, yb-12), (50, yb), (62, yb+12)], fill=W, width=3)
    if not saved:
        d.text((SW/2, yb), CARD, font=FI(27, 'SemiBold'), fill=W, anchor='mm')
        d.rounded_rectangle([414, yb-30, 576, yb+30], 30, fill=BLU); d.text((495, yb), 'Enregistrer', font=FI(23, 'SemiBold'), fill=W, anchor='mm')
        POS['save_btn'] = [495, yb]
    else:
        d.text((40, 210), CARD, font=FI(44, 'Bold'), fill=W, anchor='lm')
        d.text((40, 258), '7 éléments, 58,2 Go disponibles', font=FI(20), fill=G2, anchor='lm')
    d.rounded_rectangle([24, yb+50 if not saved else 290, SW-24, (yb+112) if not saved else 352], 31, fill=(44, 44, 48))
    ys = (yb+81) if not saved else 321
    d.text((84, ys), 'Rechercher', font=FI(26), fill=G2, anchor='lm'); d.ellipse([40, ys-11, 62, ys+11], outline=W, width=3)
    y0 = 420 if saved else 330
    items = [('DCIM', None)] + ([(f'IMG_08{i:02d}', i) for i in range(6)] if saved else [])
    for k, (lab, ti) in enumerate(items):
        cx = 110 + (k % 3) * 190; cy = y0 + (k // 3) * 250
        if ti is None: folder(d, cx, cy + 40, 1.25)
        else:
            t_ = thumb(130, 130, ti); m = Image.new('L', (130, 130), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 129, 129], 14, fill=255); im.paste(t_, (cx-65, cy-25), m)
        d.text((cx, cy + 135), lab, font=FI(21, 'SemiBold'), fill=W, anchor='mm')
        d.text((cx, cy + 162), 'Aujourd’hui' if ti is not None else '214 éléments', font=FI(17), fill=G2, anchor='mm')
    if not saved: save_bar(d)
    else:
        d.rounded_rectangle([24, 1170, SW-24, 1250], 40, fill=(38, 38, 42, 245), outline=(80, 80, 86))
        for x, lab in [(110, 'Récents'), (300, 'Partagés'), (490, 'Parcourir')]:
            col = BLU if lab == 'Parcourir' else G2
            d.text((x, 1222), lab, font=FI(18, 'SemiBold'), fill=col, anchor='mm')
            if lab == 'Parcourir': folder(d, x, 1192, 0.32)
            else: d.ellipse([x-12, 1182, x+12, 1206], outline=col, width=3)
    d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=W)
    return im

POS = {}
photos_sel().save(OUT+'sd_photos.png')
share_sheet().save(OUT+'sd_share.png')
explorer().save(OUT+'sd_pick.png')
card_view(False).save(OUT+'sd_card.png')
card_view(True).save(OUT+'sd_files.png')
POS['duree'] = 58.4
json.dump(POS, open('src/data.json', 'w'), indent=0)

# ---- sons (35 %)
SR = 44100; N = int(SR * 58.5); au = np.zeros(N)
def add(t, x):
    i = int(t * SR); j = min(N, i + len(x)); au[i:j] += x[:j-i]
def tone(f0, f1, dd, v, dec=6):
    tt = np.arange(int(SR*dd)) / SR; f = np.linspace(f0, f1, len(tt)); return v * np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-dec*tt/dd)
def soft():
    return tone(660, 660, 0.6, 0.12, 5) + np.pad(tone(990, 990, 0.45, 0.06, 5), (0, int(SR*0.15)))
S = {'soft': soft(), 'pop': tone(520, 900, 0.09, 0.2), 'tick': tone(1400, 1100, 0.06, 0.18), 'ding': np.pad(tone(1320, 1320, 0.5, 0.2), (0, 0)) + tone(1980, 1980, 0.5, 0.09), 'err': tone(300, 220, 0.25, 0.22, 4)}
SC = [2.0, 6.4, 17.9, 35.6, 38.9, 43.9, 49.0, 52.5, 54.9]
ev = [(s, 'soft') for s in SC] + [(t, 'pop') for t in (12.9, 13.9, 15.3, 17.4, 24.3, 25.3, 28.7, 34.6)] + [(t, 'tick') for t in (22.8, 23.0, 23.2, 23.4, 23.6, 23.8, 27.5)] + \
     [(36.3, 'ding'), (40.1, 'err'), (44.9, 'err'), (33.0, 'ding')]
for t, k in ev: add(t, S[k])
au = np.clip(au * 0.35 / 0.35, -1, 1) * 0.35 / max(0.35, 1e-9)
w = wave.open(OUT+'sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(au, -1, 1)*32767).astype(np.int16).tobytes()); w.close()
print(POS)
