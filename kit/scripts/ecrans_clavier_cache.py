# Écrans « Clavier caché » (Messages en mode sombre + clavier AZERTY sombre) + sons. Lancer depuis kit/.
import sys, json, wave, numpy as np
sys.path.insert(0, 'scripts')
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw
OUT = 'public/'
W = (255, 255, 255); G2 = (152, 152, 159); BLU = (10, 132, 255)
KB_BG = (30, 30, 32); KEY = (88, 88, 92); KEY2 = (54, 54, 58)
POS = {}

def status(d):
    d.text((70, 44), '20:14', font=FI(25, 'SemiBold'), fill=W, anchor='lm')
    d.rounded_rectangle([SW/2-64, 22, SW/2+64, 62], 21, fill=(0, 0, 0))
    for i in range(4): d.rounded_rectangle([452+i*9, 46-i*4, 458+i*9, 52], 2, fill=W)
    d.rounded_rectangle([500, 34, 540, 54], 6, fill=W); d.text((520, 44), '82', font=FI(15, 'Bold'), fill=(0, 0, 0), anchor='mm')

KY0 = 800
def keyboard(d, sugg, hi=None):
    d.rectangle([0, KY0, SW, SH], fill=KB_BG)
    # barre de suggestions
    xs = [100, 300, 500]
    for i, s in enumerate(sugg):
        if i == 1 and s: d.rounded_rectangle([210, KY0+14, 390, KY0+62], 14, fill=(62, 62, 66))
        d.text((xs[i], KY0+38), s, font=FI(24, 'SemiBold' if i == 1 else 'Regular'), fill=W, anchor='mm')
        if i < 2: d.line([(200+200*i, KY0+22), (200+200*i, KY0+54)], fill=(70, 70, 74), width=2)
    kw, gap, kh = 52, 6, 76
    rows = ['azertyuiop', 'qsdfghjklm', 'wxcvbn\'']
    for r, row in enumerate(rows):
        n = len(row); y = KY0+80+r*(kh+14)
        x0 = (SW-(n*kw+(n-1)*gap))/2
        for i, ch in enumerate(row):
            x = x0+i*(kw+gap)
            d.rounded_rectangle([x, y, x+kw, y+kh], 10, fill=(150, 150, 156) if ch == hi else KEY)
            d.text((x+kw/2, y+kh/2), ch, font=FI(30), fill=W, anchor='mm')
            POS[f'k:{ch}'] = [round(x+kw/2), round(y+kh/2)]
        if r == 2:
            d.rounded_rectangle([12, y, 12+70, y+kh], 10, fill=KEY2); d.polygon([(47, y+20), (30, y+40), (40, y+40), (40, y+56), (54, y+56), (54, y+40), (64, y+40)], outline=W)
            d.rounded_rectangle([SW-82, y, SW-12, y+kh], 10, fill=KEY2); d.text((SW-47, y+kh/2), '⌫', font=FI(28), fill=W, anchor='mm')
    y = KY0+80+3*(kh+14)
    d.rounded_rectangle([12, y, 130, y+kh], 10, fill=KEY2); d.text((71, y+kh/2), '123', font=FI(24), fill=W, anchor='mm')
    d.rounded_rectangle([140, y, 440, y+kh], 10, fill=KEY); d.text((290, y+kh/2), 'espace', font=FI(24), fill=W, anchor='mm')
    d.rounded_rectangle([450, y, SW-12, y+kh], 10, fill=KEY2); d.text((519, y+kh/2), 'retour', font=FI(24), fill=W, anchor='mm')
    d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=W)

def msg_screen(typed='', hi=None):
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); d = ImageDraw.Draw(im); status(d)
    d.line([(58, 96), (44, 110), (58, 124)], fill=BLU, width=4, joint='curve')
    d.ellipse([SW/2-42, 84, SW/2+42, 168], fill=(120, 110, 200)); d.text((SW/2, 126), 'L', font=FI(40, 'SemiBold'), fill=W, anchor='mm')
    d.text((SW/2, 192), 'Léa ›', font=FI(21), fill=W, anchor='mm')
    d.text((SW/2, 440), "iMessage · Aujourd'hui 20:12", font=FI(17), fill=G2, anchor='mm')
    f = FI(28); t = 'On dîne ce soir ?'; w = d.textlength(t, font=f)+44
    d.rounded_rectangle([24, 600, 24+w, 664], 32, fill=(38, 38, 40)); d.text((46, 632), t, font=f, fill=W, anchor='lm')
    d.ellipse([20, 720, 70, 770], fill=(44, 44, 46)); d.text((45, 744), '+', font=FI(32), fill=G2, anchor='mm')
    d.rounded_rectangle([82, 718, SW-22, 772], 27, outline=(70, 70, 74), width=2)
    d.text((104, 745), (typed or 'iMessage') + ('|' if typed else ''), font=FI(25), fill=W if typed else G2, anchor='lm')
    if typed: d.ellipse([SW-64, 726, SW-28, 762], fill=BLU); d.line([(SW-46, 754), (SW-46, 734)], fill=W, width=4); d.line([(SW-55, 742), (SW-46, 733), (SW-37, 742)], fill=W, width=4)
    if typed.endswith('tem'): sugg = ['tempête', 'temps', 'temple']
    elif typed.endswith('temp'): sugg = ['tempête', 'temps', 'température']
    elif typed.startswith('pas le'): sugg = ['temps', 'problème', 'droit']
    elif typed.startswith('pas'): sugg = ['le', 'de', 'encore']
    else: sugg = ['Oui', 'Non', 'Ce soir']
    keyboard(d, sugg, hi)
    return im

TYPED = 'pas le tem'
EV = []  # [seconde, nom_png]
t = 15.95
msg_screen().save(OUT+'kc_0.png'); EV.append([0, 'kc_0.png'])
for i in range(1, len(TYPED)+1):
    ch = TYPED[i-1]; n = f'kc_{i}.png'
    msg_screen(TYPED[:i], hi=ch if ch != ' ' else None).save(OUT+f'kc_{i}h.png')
    msg_screen(TYPED[:i]).save(OUT+n)
    EV.append([round(t, 2), f'kc_{i}h.png']); EV.append([round(t+0.09, 2), n]); t += 0.135
POS['EV'] = EV
POS['duree'] = 61.97
json.dump(POS, open('src/data.json', 'w'), indent=0)

# ---- sons
T = 62.5; SR = 44100; au = np.zeros(int((T+0.5)*SR), np.float32)
def add(t, x):
    i = int(t*SR); x = x[:len(au)-i]; au[i:i+len(x)] += x
def tone(f0, f1, dd, v, dec=6):
    n = int(dd*SR); k = np.linspace(0, 1, n); ph = 2*np.pi*np.cumsum(f0+(f1-f0)*k)/SR
    return (np.sin(ph)*np.exp(-k*dec)*v).astype(np.float32)
def soft():
    n = int(0.42*SR); k = np.arange(n)/SR; env = np.minimum(1, k/0.012)*np.exp(-k*11)
    return ((np.sin(2*np.pi*587.33*k)*0.6+np.sin(2*np.pi*880*k)*0.28+np.sin(2*np.pi*1174.66*k)*0.08)*env*0.30).astype(np.float32)
S = {'soft': soft(), 'pop': tone(520, 900, 0.09, 0.2), 'tick': tone(1400, 1100, 0.06, 0.18), 'ding': tone(1320, 1320, 0.5, 0.2)+tone(1980, 1980, 0.5, 0.09),
     'err': tone(300, 220, 0.25, 0.22, 4), 'grow': tone(300, 900, 0.5, 0.15, 2), 'shrink': tone(900, 300, 0.4, 0.13, 2)}
SC = [5.9, 13.0, 19.75, 26.65, 33.7, 43.6, 49.85, 55.7, 58.1]
ev = [(s, 'soft') for s in SC]
ev += [(0.3, 'pop'), (2.6, 'pop'), (9.7, 'pop'), (14.35, 'pop'), (18.5, 'pop'), (21.28, 'tick'), (21.94, 'tick'), (22.22, 'tick'), (24.5, 'ding'),
       (24.92, 'pop'), (25.32, 'pop'), (26.04, 'pop'), (28.3, 'grow'), (32.0, 'shrink'), (36.4, 'tick'), (37.7, 'ding'), (41.8, 'pop'), (47.4, 'err'), (49.3, 'err'),
       (51.7, 'tick'), (51.85, 'tick'), (52.0, 'tick'), (52.1, 'tick'), (52.25, 'err'), (54.9, 'pop'), (60.5, 'ding')]
ev += [(a, 'tick') for a, n in EV[1:] if n.endswith('h.png')]
for a, k in ev: add(a, S[k]*0.35/0.3)
au = np.clip(au, -1, 1); w = wave.open(OUT+'sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((au*32767).astype(np.int16).tobytes()); w.close()
print('ok', len(EV))
