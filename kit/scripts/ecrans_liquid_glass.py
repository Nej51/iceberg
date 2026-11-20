# Écrans « Liquid Glass / lisibilité » (mode SOMBRE, comme les captures de Nej, iOS 27) + sons.  Lancer depuis kit/.
import sys, json, wave, numpy as np
sys.path.insert(0, 'scripts')
import ui_iphone as ui
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw, ImageFilter
ui.init()
OUT = 'public/'
BG = (0, 0, 0); CARD = (28, 28, 30); SEP = (56, 56, 58); TXT = (255, 255, 255); G2 = (152, 152, 159)
HI = (58, 58, 62); BLU = (10, 132, 255); GRN = (48, 209, 88); W = (255, 255, 255)
X0, X1 = 22, 578
POS = {}

def wrap(d, text, font, maxw):
    out, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = w
    out.append(cur); return out

def status(d, dark=True, time='17:40'):
    c = W if dark else TXT
    d.text((70, 44), time, font=FI(25, 'SemiBold'), fill=c, anchor='lm')
    d.rounded_rectangle([SW/2-64, 22, SW/2+64, 62], 21, fill=(0, 0, 0))
    for i in range(4): d.rounded_rectangle([452+i*9, 46-i*4, 458+i*9, 52], 2, fill=c)
    d.rounded_rectangle([500, 34, 540, 54], 6, fill=c); d.text((520, 44), '70', font=FI(15, 'Bold'), fill=(255, 255, 255) if not dark else (0, 0, 0), anchor='mm')

def nav(d, title, back=True):
    if back:
        d.ellipse([22, 80, 82, 140], fill=(44, 44, 46)); d.line([(58, 96), (44, 110), (58, 124)], fill=TXT, width=4, joint='curve')
    d.text((SW/2, 110), title, font=FI(24, 'SemiBold'), fill=TXT, anchor='mm')

def icon(im, x, y, col, s=40):
    d = ImageDraw.Draw(im); d.rounded_rectangle([x, y, x+s, y+s], 10, fill=col); c = (x+s/2, y+s/2)
    d.ellipse([c[0]-9, c[1]-9, c[0]+9, c[1]+9], outline=W, width=3)

def toggle(d, x, y, on):
    d.rounded_rectangle([x, y-20, x+70, y+20], 20, fill=GRN if on else (57, 57, 61))
    kx = x+50 if on else x+20; d.ellipse([kx-17, y-17, kx+17, y+17], fill=W)

def chev(d, x, y): d.line([(x, y-8), (x+7, y), (x, y+8)], fill=(110, 110, 115), width=3, joint='curve')

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

def homebar(d, c=W): d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=c)
def save(im, n): im.save(OUT+n+'.png')


def reglages(hi=None):
    im, d = base('Réglages', back=False); y = 170
    card(im, y, [dict(label='Général', icon=(142, 142, 147), right='>'), dict(label='Accessibilité', icon=BLU, right='>'), dict(label='Apparence', icon=(20, 20, 22), right='>'),
                 dict(label='Bouton Action', icon=BLU, right='>'), dict(label='Caméra', icon=(142, 142, 147), right='>'), dict(label='Centre de contrôle', icon=(142, 142, 147), right='>'),
                 dict(label="Écran d'accueil", icon=BLU, right='>'), dict(label='En veille', icon=(20, 20, 22), right='>'), dict(label="Fond d'écran", icon=(50, 160, 220), right='>'),
                 dict(label='Luminosité et affichage', icon=BLU, right='>'), dict(label='Recherche', icon=(142, 142, 147), right='>')], hi=hi, key='reg')
    d.rounded_rectangle([40, 1180, 560, 1240], 30, fill=(44, 44, 46)); d.text((80, 1210), 'Recherche', font=FI(22), fill=G2, anchor='lm')
    homebar(d); return im
save(reglages(), 'lg_reg'); save(reglages('Apparence'), 'lg_reg_hi_app'); save(reglages('Accessibilité'), 'lg_reg_hi_acc')

def apparence(hi=None, val='Plus transparent'):
    im, d = base('Apparence'); y = header(d, 180, 'Apparence') + 12
    d.rounded_rectangle([X0, y, X1, y+380], 26, fill=CARD)
    for i, (lab, chk) in enumerate([('Claire', False), ('Sombre', True)]):
        cx = 190 + i*220; g = Image.new('RGB', (100, 210)); gd = ImageDraw.Draw(g)
        for k in range(210): gd.line([(0, k), (100, k)], fill=((220-k//2, 235-k//3, 245) if i == 0 else (20+k//6, 40+k//5, 120+k//3)))
        m = Image.new('L', g.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 99, 209], 16, fill=255); im.paste(g, (cx-50, y+24), m)
        d.text((cx, y+262), lab, font=FI(23), fill=TXT, anchor='mm')
        if chk: d.ellipse([cx-14, y+290, cx+14, y+318], fill=BLU); d.line([(cx-6, y+304), (cx-1, y+310), (cx+7, y+298)], fill=W, width=3)
        else: d.ellipse([cx-14, y+290, cx+14, y+318], outline=G2, width=2)
    y += 380 + 30
    y = card(im, y, [dict(label='Automatique', right=('tog', True)), dict(label='Options', right=('val', 'Sombre la nuit'))]) + 30
    y = card(im, y, [dict(label='Liquid Glass', right=('val', val), desc="Liquid Glass s'adapte dynamiquement au contenu situé en dessous.")], hi=hi, key='app') + 30
    card(im, y, [dict(label='Taille du texte', right='>'), dict(label='Texte en gras', right=('tog', False))])
    homebar(d); return im
save(apparence(), 'lg_app'); save(apparence('Liquid Glass'), 'lg_app_hi')

# Liquid Glass : aperçu (dégradé, pas la photo d'Apple) + curseur Transparent -> Teinté
def lg(pos):
    im, d = base('Liquid Glass'); y = 170
    g = Image.new('RGB', (556, 380)); gd = ImageDraw.Draw(g)
    for k in range(380): gd.line([(0, k), (556, k)], fill=(40+k//6, 90+k//8, 200-k//5))
    for cx, cy, r, c in [(150, 120, 120, (255, 140, 200)), (420, 220, 150, (120, 230, 255)), (300, 320, 110, (180, 120, 255))]:
        gd.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c)
    g = g.filter(ImageFilter.GaussianBlur(40))
    bar = Image.new('RGBA', (500, 64), (0, 0, 0, 0)); bd = ImageDraw.Draw(bar)
    alpha = int(60 + 170*pos); bd.rounded_rectangle([0, 0, 499, 63], 32, fill=(30, 30, 34, alpha), outline=(255, 255, 255, 90), width=2)
    bd.ellipse([24, 20, 46, 42], outline=(255, 255, 255, 230), width=3); bd.text((64, 32), 'Recherche', font=FI(22), fill=(255, 255, 255, 230), anchor='lm')
    g = g.convert('RGBA'); g.alpha_composite(bar, (28, 290)); g = g.convert('RGB')
    m = Image.new('L', g.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 555, 379], 30, fill=255); im.paste(g, (X0, y), m)
    y += 380 + 26
    d.rounded_rectangle([X0, y, X1, y+72], 36, fill=CARD)
    x0, x1 = X0+80, X1-80; kx = x0 + (x1-x0)*pos
    d.rounded_rectangle([x0, y+33, x1, y+39], 3, fill=(70, 70, 74)); d.rounded_rectangle([x0, y+33, kx, y+39], 3, fill=BLU)
    d.rounded_rectangle([kx-26, y+20, kx+26, y+52], 16, fill=W)
    d.rounded_rectangle([X0+22, y+24, X0+50, y+48], 6, outline=G2, width=2); d.rounded_rectangle([X1-50, y+24, X1-22, y+48], 6, fill=G2)
    POS['lg:slider'] = [300, y+36]; POS['lg:teinte'] = [round(x1), y+36]
    for k, l in enumerate(wrap(d, "« Transparent » révèle davantage le contenu situé en dessous. « Teinté » augmente l'opacité, accentuant le contraste du contenu et des commandes.", FI(18), 520)):
        d.text((X0+22, y+96+k*24), l, font=FI(18), fill=G2, anchor='lt')
    homebar(d); return im
for i, p in enumerate([0.15, 0.35, 0.55, 0.75, 0.95]): save(lg(p), f'lg_slider{i}')

def access(hi=None):
    im, d = base('Accessibilité'); y = header(d, 180, 'Vision') + 12
    card(im, y, [dict(label='VoiceOver', icon=(20, 20, 22), right=('val', 'Non')), dict(label='Zoom', icon=(20, 20, 22), right=('val', 'Non')),
                 dict(label='Affichage et taille du texte', icon=BLU, right='>'), dict(label='Mouvement', icon=GRN, right='>'),
                 dict(label='Contenu énoncé', icon=(20, 20, 22), right='>'), dict(label='Audiodescription', icon=BLU, right=('val', 'Non'))], hi=hi, key='acc')
    homebar(d); return im
save(access(), 'lg_acc'); save(access('Affichage et taille du texte'), 'lg_acc_hi')

# Affichage et taille du texte (ordre iOS : Réduire la transparence AU-DESSUS d'Augmenter le contraste) — écran imaginé
RT = "Améliore le contraste en réduisant la transparence et le flou sur certains arrière-plans pour plus de lisibilité."
AC = "Augmente le contraste des couleurs entre le premier plan et l'arrière-plan des apps."
def affichage(contrast=False, transp=False, hi=None):
    im, d = base('Affichage et taille du texte'); y = 170
    y = card(im, y, [dict(label='Texte en gras', right=('tog', False)), dict(label='Texte plus grand', right=('val', 'Non')), dict(label='Formes des boutons', right=('tog', False)),
                     dict(label='Étiquettes Activé/Désactivé', right=('tog', False))]) + 30
    y = card(im, y, [dict(label='Réduire la transparence', right=('tog', transp), desc=RT)], hi=hi, key='aff') + 30
    y = card(im, y, [dict(label='Augmenter le contraste', right=('tog', contrast), desc=AC)], hi=hi, key='aff') + 30
    card(im, y, [dict(label='Différencier sans couleur', right=('tog', False)), dict(label='Inversion intelligente', right=('tog', False))])
    homebar(d); return im
save(affichage(), 'lg_aff'); save(affichage(hi='Augmenter le contraste'), 'lg_aff_hi_c'); save(affichage(True), 'lg_aff_c')
save(affichage(True, hi='Réduire la transparence'), 'lg_aff_hi_t'); save(affichage(True, True), 'lg_aff_ct')

POS['duree'] = 60.65
json.dump(POS, open('src/data.json', 'w'), indent=0)
T = 61.0; SR = 44100; au = np.zeros(int((T+0.5)*SR), np.float32)
def add(t, x):
    i = int(t*SR); x = x[:len(au)-i]; au[i:i+len(x)] += x
def tone(f0, f1, dd, v, dec=6):
    n = int(dd*SR); k = np.linspace(0, 1, n); ph = 2*np.pi*np.cumsum(f0+(f1-f0)*k)/SR
    return (np.sin(ph)*np.exp(-k*dec)*v).astype(np.float32)
def soft():
    n = int(0.42*SR); k = np.arange(n)/SR; env = np.minimum(1, k/0.012)*np.exp(-k*11)
    return ((np.sin(2*np.pi*587.33*k)*0.6+np.sin(2*np.pi*880*k)*0.28+np.sin(2*np.pi*1174.66*k)*0.08)*env*0.30).astype(np.float32)
S = {'soft': soft(), 'pop': tone(520, 900, 0.09, 0.2), 'tick': tone(1400, 1100, 0.06, 0.18), 'ding': tone(1320, 1320, 0.5, 0.2)+tone(1980, 1980, 0.5, 0.09)}
EV = [(4.8, 'soft'), (8.4, 'soft'), (12.3, 'soft'), (16.4, 'soft'), (24.85, 'soft'), (29.5, 'soft'), (37.3, 'soft'), (42.2, 'soft'), (49.5, 'soft'), (53.3, 'soft'), (55.8, 'soft'),
      (0.3, 'pop'), (2.4, 'pop'), (13.7, 'pop'), (40.0, 'pop'), (50.6, 'pop'), (51.4, 'pop'),
      (17.6, 'tick'), (18.4, 'tick'), (19.3, 'tick'), (26.0, 'tick'), (26.7, 'tick'), (27.7, 'tick'), (30.6, 'tick'), (43.9, 'tick'),
      (21.6, 'ding'), (31.3, 'ding'), (44.3, 'ding'), (57.9, 'ding')]
for t, k in EV: add(t, S[k]*0.35/0.3)
au = np.clip(au, -1, 1); w = wave.open(OUT+'sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((au*32767).astype(np.int16).tobytes()); w.close()
print({k: v for k, v in POS.items()})
