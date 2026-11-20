# Écrans « Accès guidé » (mode CLAIR, comme les captures de Nej, iOS 26/27) + sons.  Lancer depuis kit/.
import sys, json, wave, numpy as np
sys.path.insert(0, 'scripts')
import ui_iphone as ui
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw, ImageFilter
ui.init()
OUT = 'public/'
BG = (242, 242, 247); CARD = (255, 255, 255); SEP = (222, 222, 226); TXT = (0, 0, 0); G2 = (138, 138, 142)
HI = (209, 209, 214); BLU = (0, 122, 255); GRN = (52, 199, 89); W = (255, 255, 255)
X0, X1 = 22, 578
POS = {}

def wrap(d, text, font, maxw):
    out, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = w
    out.append(cur); return out

def status(d, dark=False, time='14:36'):
    c = W if dark else TXT
    d.text((70, 44), time, font=FI(25, 'SemiBold'), fill=c, anchor='lm')
    d.rounded_rectangle([SW/2-64, 22, SW/2+64, 62], 21, fill=(0, 0, 0))
    for i in range(4): d.rounded_rectangle([452+i*9, 46-i*4, 458+i*9, 52], 2, fill=c)
    d.rounded_rectangle([500, 34, 540, 54], 6, fill=c); d.text((520, 44), '70', font=FI(15, 'Bold'), fill=(255, 255, 255) if not dark else (0, 0, 0), anchor='mm')

def nav(d, title, back=True):
    if back:
        d.ellipse([22, 80, 82, 140], fill=W); d.line([(58, 96), (44, 110), (58, 124)], fill=TXT, width=4, joint='curve')
    d.text((SW/2, 110), title, font=FI(24, 'SemiBold'), fill=TXT, anchor='mm')

def icon(im, x, y, col, s=40):
    d = ImageDraw.Draw(im); d.rounded_rectangle([x, y, x+s, y+s], 10, fill=col); c = (x+s/2, y+s/2)
    d.ellipse([c[0]-9, c[1]-9, c[0]+9, c[1]+9], outline=W, width=3)

def toggle(d, x, y, on):
    d.rounded_rectangle([x, y-20, x+70, y+20], 20, fill=GRN if on else (233, 233, 235))
    kx = x+50 if on else x+20; d.ellipse([kx-17, y-17, kx+17, y+17], fill=W, outline=(225, 225, 228))

def chev(d, x, y): d.line([(x, y-8), (x+7, y), (x, y+8)], fill=(190, 190, 195), width=3, joint='curve')

def card(im, y, rows, hi=None, key=None):
    d = ImageDraw.Draw(im); hs = []
    for r in rows:
        dl = wrap(d, r['desc'], FI(18), 500) if r.get('desc') else []
        hs.append((72 + (24*len(dl)+10 if dl else 0), dl))
    tot = sum(h for h, _ in hs); d.rounded_rectangle([X0, y, X1, y+tot], 26, fill=CARD)
    yy = y
    for i, (r, (h, dl)) in enumerate(zip(rows, hs)):
        if hi == r['label']:
            top = i == 0; bot = i == len(rows)-1
            d.rounded_rectangle([X0, yy, X1, yy+h], 26 if (top or bot) else 0, fill=HI)
            if top and not bot: d.rectangle([X0, yy+h-30, X1, yy+h], fill=HI)
            if bot and not top: d.rectangle([X0, yy, X1, yy+30], fill=HI)
        tx = X0+24
        if r.get('icon'): icon(im, X0+18, yy+16, r['icon']); tx = X0+74
        col = BLU if r.get('link') else TXT
        d.text((tx, yy+36), r['label'], font=FI(23), fill=col, anchor='lm')
        for k, l in enumerate(dl): d.text((X0+24, yy+66+k*24), l, font=FI(18), fill=G2, anchor='lt')
        rt = r.get('right'); cy = yy+36
        if rt == '>': chev(d, X1-34, cy)
        elif isinstance(rt, tuple) and rt[0] == 'val': d.text((X1-48, cy), rt[1], font=FI(22), fill=G2, anchor='rm'); chev(d, X1-34, cy)
        elif isinstance(rt, tuple) and rt[0] == 'tog': toggle(d, X1-96, cy, rt[1])
        if key: POS[f"{key}:{r['label']}"] = [300, round(yy+36), h]
        if rt and isinstance(rt, tuple) and rt[0] == 'tog' and key: POS[f"{key}:{r['label']}:tog"] = [X1-61, round(cy)]
        yy += h
        if i < len(rows)-1: d.line([(tx, yy), (X1, yy)], fill=SEP, width=1)
    return yy

def header(d, y, t): d.text((X0+22, y), t, font=FI(20, 'SemiBold'), fill=G2, anchor='lm'); return y+20

def base(title, back=True):
    im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im); status(d); nav(d, title, back); return im, d

def homebar(d, c=TXT): d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=c)
def save(im, n): im.save(OUT+n+'.png')

# 1. Réglages
def reglages(hi=None):
    im, d = base('Réglages', back=False); y = 170
    y = card(im, y, [dict(label='Mode Avion', icon=(255, 149, 0), right=('tog', False)), dict(label='Wi-Fi', icon=BLU, right=('val', 'Maison')),
                     dict(label='Bluetooth', icon=BLU, right=('val', 'Oui')), dict(label='Batterie', icon=GRN, right='>')]) + 30
    y = card(im, y, [dict(label='Général', icon=(142, 142, 147), right='>'), dict(label='Accessibilité', icon=BLU, right='>'),
                     dict(label='Apparence', icon=(30, 30, 30), right='>'), dict(label='Bouton Action', icon=BLU, right='>'),
                     dict(label='Caméra', icon=(142, 142, 147), right='>'), dict(label='Centre de contrôle', icon=(142, 142, 147), right='>')], hi=hi, key='reg') + 30
    d.rounded_rectangle([22, 1180, 578, 1240], 30, fill=(227, 227, 232)); d.text((60, 1210), 'Recherche', font=FI(22), fill=G2, anchor='lm')
    homebar(d); return im
save(reglages(), 'ag_reg'); save(reglages('Accessibilité'), 'ag_reg_hi')

# 2. Accessibilité (descendu jusqu'à Général)
def access(hi=None):
    im, d = base('Accessibilité')
    y = header(d, 180, 'Parole') + 12
    y = card(im, y, [dict(label='Parole en direct', icon=BLU, right=('val', 'Non')), dict(label='Voix personnelle', icon=BLU, right='>'),
                     dict(label='Raccourcis vocaux', icon=(30, 30, 30), right=('val', 'Non'))]) + 30
    y = header(d, y+8, 'Accessoires') + 12
    y = card(im, y, [dict(label='Claviers et saisie', icon=(142, 142, 147), right='>')]) + 30
    y = header(d, y+8, 'Général') + 12
    card(im, y, [dict(label='Accès guidé', icon=(30, 30, 30), right=('val', 'Non')), dict(label="Accès d'aide", icon=(30, 30, 30), right='>'),
                 dict(label='Siri', icon=(255, 45, 85), right='>'), dict(label='Raccourci Accessibilité', icon=BLU, right=('val', 'Demander')),
                 dict(label='Réglages selon les apps', icon=BLU, right='>')], hi=hi, key='acc')
    homebar(d); return im
save(access(), 'ag_acc'); save(access('Accès guidé'), 'ag_acc_hi')

# 3. Accès guidé
AGD = "La fonction « Accès guidé » vous permet de limiter l'accès de l'iPhone à une app spécifique et de contrôler les fonctionnalités disponibles. Pour activer « Accès guidé », cliquez trois fois sur le bouton latéral une fois dans l'app que vous voulez utiliser."
def ag(on, hi=None):
    im, d = base('Accès guidé'); y = 180
    y = card(im, y, [dict(label='Accès guidé', right=('tog', on), desc=AGD)], key='ag') + 30
    y = card(im, y, [dict(label='Réglages des codes', right='>')], hi=hi, key='ag') + 30
    y = card(im, y, [dict(label='Limites de temps', right='>')]) + 30
    y = card(im, y, [dict(label='Raccourci Accessibilité', right=('tog', False), desc="Si vous appuyez trois fois sur le bouton latéral durant une session d'Accès guidé, vos réglages « Raccourci Accessibilité » s'affichent.")]) + 30
    card(im, y, [dict(label="Verrouillage auto. de l'écran", right=('val', 'Par défaut'))])
    homebar(d); return im
save(ag(False), 'ag_off'); save(ag(True), 'ag_on'); save(ag(True, 'Réglages des codes'), 'ag_on_hi')

# 4. Réglages des codes
def codes(hi=False):
    im, d = base('Réglages des codes'); y = 180
    y = card(im, y, [dict(label="Définir le code d'Accès guidé", link=True, desc="Définissez le code à utiliser lorsqu'Accès guidé est activé.")], hi="Définir le code d'Accès guidé" if hi else None, key='codes') + 30
    card(im, y, [dict(label='Face ID', right=('tog', False), desc="Utilisez Face ID pour arrêter « Accès guidé ».")])
    homebar(d); return im
save(codes(), 'ag_codes'); save(codes(True), 'ag_codes_hi')

# 5. Clavier de code (clair = définir ; sombre = sortir)
def pad(n, dark=False, title='Définir le code', sub='Tapez un code'):
    bg = (0, 0, 0) if dark else BG; fg = W if dark else TXT
    im = Image.new('RGB', (SW, SH), bg); d = ImageDraw.Draw(im); status(d, dark)
    d.text((SW/2, 112), title, font=FI(24, 'SemiBold'), fill=fg, anchor='mm')
    d.ellipse([520, 86, 568, 134], fill=(44, 44, 46) if dark else W); d.line([(534, 100), (554, 120)], fill=fg, width=3); d.line([(554, 100), (534, 120)], fill=fg, width=3)
    d.text((SW/2, 380), sub, font=FI(24), fill=fg, anchor='mm')
    for i in range(6):
        cx = SW/2 - 125 + i*50; box = [cx-12, 428, cx+12, 452]
        if i < n: d.ellipse(box, fill=fg)
        else: d.ellipse(box, outline=fg, width=2)
    kb = (40, 40, 42) if dark else (209, 211, 217); key = (90, 90, 94) if dark else W
    d.rectangle([0, 860, SW, SH], fill=kb)
    labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '', '0', '']
    for i, l in enumerate(labels):
        if not l: continue
        c, r = i % 3, i // 3; x0 = 14 + c*192; y0 = 880 + r*92
        d.rounded_rectangle([x0, y0, x0+180, y0+80], 12, fill=key); d.text((x0+90, y0+40), l, font=FI(34), fill=fg, anchor='mm')
    homebar(d, fg); return im
for n in range(7): save(pad(n), f'ag_pad{n}'); save(pad(n, True, 'Saisissez le code', 'Tapez votre code'), f'ag_padd{n}')

# 6. App ouverte : une photo (plage) en plein écran
photo = Image.open(OUT+'img_tend.png').convert('RGB')
pw, ph = photo.size; crop = photo.crop((int(pw*0.48), int(ph*0.425), int(pw*0.655), int(ph*0.52))).resize((SW, int(SW*(ph*0.095)/(pw*0.175))))
def photo_scr(banner=None):
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); im.paste(crop, (0, (SH-crop.height)//2)); d = ImageDraw.Draw(im); status(d, True)
    d.text((SW/2, 112), '20 novembre', font=FI(22, 'SemiBold'), fill=W, anchor='mm')
    if banner:
        bx = Image.new('RGBA', (SW, SH), (0, 0, 0, 0)); bd = ImageDraw.Draw(bx)
        bd.rounded_rectangle([150, 470, 450, 650], 30, fill=(235, 235, 240, 235))
        for k, l in enumerate(banner): bd.text((300, 510+k*34), l, font=FI(24, 'SemiBold'), fill=TXT, anchor='mm')
        im = Image.alpha_composite(im.convert('RGBA'), bx).convert('RGB'); d = ImageDraw.Draw(im)
    homebar(d, W); return im
save(photo_scr(), 'ag_photo'); save(photo_scr(['Accès guidé', 'activé.', 'Appuyez 3 fois', 'pour quitter.']), 'ag_photo_on')
save(photo_scr(['Accès guidé', 'désactivé.']), 'ag_photo_off')

# 7. Écran de session (Démarrer / Reprendre)
def session(left, right):
    im = Image.new('RGB', (SW, SH), (28, 28, 30)); d = ImageDraw.Draw(im); status(d, True)
    lw = d.textlength(left, font=FI(22, 'SemiBold')) + 40
    d.rounded_rectangle([22, 84, 22+lw, 136], 26, fill=(58, 58, 60)); d.text((22+lw/2, 110), left, font=FI(22, 'SemiBold'), fill=W, anchor='mm')
    d.text((SW/2, 110), 'Accès guidé', font=FI(23, 'SemiBold'), fill=W, anchor='mm')
    rw = d.textlength(right, font=FI(22, 'SemiBold')) + 40
    d.rounded_rectangle([578-rw, 84, 578, 136], 26, fill=BLU); d.text((578-rw/2, 110), right, font=FI(22, 'SemiBold'), fill=W, anchor='mm')
    POS[f'sess:{right}'] = [round(578-rw/2), 110, round(rw)]; POS[f'sess:{left}'] = [round(22+lw/2), 110, round(lw)]
    mini = photo_scr().resize((330, 715)); m = Image.new('L', mini.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 329, 714], 40, fill=255)
    im.paste(mini, (135, 170), m)
    for k, l in enumerate(["Entourez les zones de", "l'écran à bloquer."]): d.text((40, 960+k*30), l, font=FI(21), fill=(200, 200, 205), anchor='lm')
    d.rounded_rectangle([330, 950, 578, 1010], 30, fill=BLU); d.text((454, 980), 'Réglages de session', font=FI(20, 'SemiBold'), fill=W, anchor='mm')
    POS['sess:reglages'] = [454, 980, 248]
    homebar(d, W); return im
save(session('Annuler', 'Démarrer'), 'ag_start'); save(session('Fin', 'Reprendre'), 'ag_fin')

# 8. Réglages de session (bonus limite de temps) — libellés à confirmer
def opts(limit):
    im = session('Annuler', 'Démarrer'); d = ImageDraw.Draw(im)
    d.rounded_rectangle([12, 560, 588, 1290], 40, fill=(44, 44, 46)); d.text((SW/2, 610), 'Réglages de session', font=FI(24, 'SemiBold'), fill=W, anchor='mm')
    y = 660
    for l, on in [('Bouton latéral', False), ('Boutons de volume', False), ('Mouvement', False), ('Claviers', False), ('Toucher', True), ('Limite de temps', limit)]:
        d.text((44, y+36), l, font=FI(23), fill=W, anchor='lm')
        d.rounded_rectangle([X1-96, y+16, X1-26, y+56], 20, fill=GRN if on else (80, 80, 84)); kx = X1-46 if on else X1-76; d.ellipse([kx-17, y+19, kx+17, y+53], fill=W)
        if l == 'Limite de temps': POS['opts:limite'] = [300, y+36, 72]; POS['opts:tog'] = [X1-61, y+36]
        y += 72; d.line([(44, y), (X1, y)], fill=(70, 70, 74))
    if limit:
        d.text((SW/2, y+50), '0 h   15 min', font=FI(34, 'SemiBold'), fill=W, anchor='mm')
    return im
save(opts(False), 'ag_opts'); save(opts(True), 'ag_opts_on')

POS['duree'] = 61.6
json.dump(POS, open('src/data.json', 'w'), indent=0)

# ---- sons
T = 62.0; SR = 44100; au = np.zeros(int((T+0.5)*SR), np.float32)
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
EV = [(4.95, 'soft'), (10.7, 'soft'), (16.85, 'soft'), (21.35, 'soft'), (26.4, 'soft'), (36.6, 'soft'), (41.35, 'soft'), (46.75, 'soft'), (52.3, 'soft'), (56.15, 'soft'), (58.5, 'soft'),
      (0.3, 'pop'), (6.3, 'pop'), (12.5, 'pop'), (37.3, 'pop'), (39.2, 'pop'), (47.0, 'pop'), (53.4, 'pop'), (54.3, 'pop'), (54.9, 'pop'),
      (17.9, 'tick'), (20.5, 'tick'), (22.3, 'tick'), (23.4, 'tick'), (32.7, 'tick'), (45.85, 'tick'), (48.2, 'tick'),
      (30.7, 'tick'), (30.9, 'tick'), (31.1, 'tick'), (43.5, 'tick'), (43.7, 'tick'), (43.9, 'tick'),
      (24.3, 'tick'), (24.4, 'tick'), (24.5, 'tick'), (24.6, 'tick'), (24.7, 'tick'), (24.8, 'tick'),
      (45.1, 'tick'), (45.25, 'tick'), (45.4, 'tick'), (45.55, 'tick'), (45.7, 'tick'), (45.8, 'tick'),
      (33.3, 'ding'), (46.1, 'ding'), (49.2, 'ding'), (60.4, 'ding'), (7.7, 'err'), (35.3, 'err')]
for t, k in EV: add(t, S[k]*0.35/0.3)
au = np.clip(au, -1, 1); w = wave.open(OUT+'sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((au*32767).astype(np.int16).tobytes()); w.close()
print({k: v for k, v in POS.items()})
