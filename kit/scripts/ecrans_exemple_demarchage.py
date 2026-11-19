import sys, json, wave, numpy as np
sys.path.insert(0, 'scripts')
import ui_iphone as ui
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw
ui.init()
OUT = 'public/'
BG = (0, 0, 0); CARD = (28, 28, 30); SEPC = (56, 56, 58); G2 = (152, 152, 159); HI = (58, 58, 62)
WHITE = (255, 255, 255); GRN = (52, 199, 89); BLU = (10, 132, 255)
X0, X1 = 22, 578
POS = {}

def wrap(d, text, font, maxw):
    out, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = w
    out.append(cur); return out

def status(d, time='21:40'):
    d.text((70, 44), time, font=FI(25, 'SemiBold'), fill=WHITE, anchor='lm')
    d.rounded_rectangle([SW/2-64, 22, SW/2+64, 62], 21, fill=(0, 0, 0))
    for i in range(4): d.rounded_rectangle([452+i*9, 50-6-i*4, 458+i*9, 52], 2, fill=WHITE if i < 3 else (90, 90, 90))
    d.rounded_rectangle([500, 34, 540, 54], 6, fill=WHITE); d.text((520, 44), '46', font=FI(15, 'Bold'), fill=(0, 0, 0), anchor='mm')

def nav(d, title, back=True, right=None):
    if back:
        d.ellipse([22, 80, 82, 140], fill=(44, 44, 46)); d.line([(58, 96), (44, 110), (58, 124)], fill=WHITE, width=4, joint='curve')
    d.text((SW/2, 110), title, font=FI(24, 'SemiBold'), fill=WHITE, anchor='mm')
    if right:
        w = d.textlength(right, font=FI(22, 'Medium')) + 40
        d.rounded_rectangle([SW-22-w, 82, SW-22, 138], 28, fill=(44, 44, 46)); d.text((SW-22-w/2, 110), right, font=FI(22, 'Medium'), fill=WHITE, anchor='mm')

def sq(im, x, y, col, glyph, s=40):
    d = ImageDraw.Draw(im); d.rounded_rectangle([x, y, x+s, y+s], 10, fill=col); c = (x+s/2, y+s/2)
    if glyph == 'phone':
        d.arc([c[0]-11, c[1]-11, c[0]+11, c[1]+11], 100, 260, fill=WHITE, width=6)
    elif glyph == 'sara':
        d.rounded_rectangle([c[0]-8, c[1]-13, c[0]+8, c[1]+13], 4, fill=WHITE); d.ellipse([c[0]-7, c[1]-3, c[0]+9, c[1]+13], fill=(220, 40, 40))
        d.line([(c[0]-2, c[1]+2), (c[0]+4, c[1]+8)], fill=WHITE, width=2); d.line([(c[0]+4, c[1]+2), (c[0]-2, c[1]+8)], fill=WHITE, width=2)
    elif glyph == 'orange':
        d.ellipse([c[0]-13, c[1]-13, c[0]+13, c[1]+13], outline=WHITE, width=3); d.arc([c[0]-7, c[1]-7, c[0]+7, c[1]+7], 100, 260, fill=WHITE, width=5)
    elif glyph == 'mail':
        d.rectangle([c[0]-12, c[1]-8, c[0]+12, c[1]+8], fill=WHITE); d.line([(c[0]-12, c[1]-8), (c[0], c[1]+2), (c[0]+12, c[1]-8)], fill=col, width=2)
    elif glyph == 'dot': d.ellipse([c[0]-9, c[1]-9, c[0]+9, c[1]+9], fill=WHITE)
    elif glyph == 'sq': d.rounded_rectangle([c[0]-10, c[1]-10, c[0]+10, c[1]+10], 4, outline=WHITE, width=3)
    elif glyph == 'grid':
        for i in (-1, 1):
            for j in (-1, 1): d.rounded_rectangle([c[0]+i*6-5, c[1]+j*6-5, c[0]+i*6+5, c[1]+j*6+5], 2, fill=WHITE)

def toggle(d, x, y, on):
    d.rounded_rectangle([x, y-20, x+70, y+20], 20, fill=GRN if on else (57, 57, 61))
    kx = x+50 if on else x+20; d.ellipse([kx-17, y-17, kx+17, y+17], fill=WHITE)

def chev(d, x, y): d.line([(x, y-8), (x+7, y), (x, y+8)], fill=(110, 110, 115), width=3, joint='curve')

def card(im, y, rows, hi=None, key=None):
    """rows: dict(label, sub, icon=(col,glyph), right: '>'|('val',txt)|('tog',bool)|'check', desc). returns end y"""
    d = ImageDraw.Draw(im); hs = []
    for r in rows:
        dl = wrap(d, r['desc'], FI(19), 430) if r.get('desc') else []
        h = 74 if not (r.get('sub') or dl) else 74 + 24*(len(dl) or 1) + (6 if dl else 0)
        hs.append((h, dl))
    tot = sum(h for h, _ in hs)
    d.rounded_rectangle([X0, y, X1, y+tot], 26, fill=CARD)
    yy = y
    for i, (r, (h, dl)) in enumerate(zip(rows, hs)):
        if hi == r['label']:
            m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([X0, y, X1, y+tot], 26, fill=255)
            hl = Image.new('L', im.size, 0); ImageDraw.Draw(hl).rectangle([X0, yy, X1, yy+h], fill=255)
            from PIL import ImageChops
            im.paste(HI, (0, 0), ImageChops.multiply(m, hl)); d = ImageDraw.Draw(im)
        tx = X0+24
        if r.get('icon'): sq(im, X0+20, yy+(h-40)/2 if not dl else yy+17, *r['icon']); tx = X0+78
        ly = yy+37 if not (r.get('sub') or dl) else yy+32
        d.text((tx, ly), r['label'], font=FI(24), fill=WHITE, anchor='lm')
        if r.get('sub'): d.text((tx, ly+30), r['sub'], font=FI(19), fill=G2, anchor='lm')
        for k, l in enumerate(dl): d.text((tx, ly+20+k*24), l, font=FI(19), fill=G2, anchor='lt')
        rt = r.get('right'); cy = yy+h/2
        if rt == '>': chev(d, X1-34, cy)
        elif rt == 'check': d.line([(X1-48, cy), (X1-40, cy+9), (X1-26, cy-10)], fill=BLU, width=4, joint='curve')
        elif isinstance(rt, tuple) and rt[0] == 'val':
            d.text((X1-48, cy), rt[1], font=FI(23), fill=G2, anchor='rm'); chev(d, X1-34, cy)
        elif isinstance(rt, tuple) and rt[0] == 'tog': toggle(d, X1-96, cy, rt[1])
        if key is not None: POS[f"{key}:{r['label']}"] = [300, round(yy+h/2), h]
        yy += h
        if i < len(rows)-1: d.line([(tx, yy), (X1, yy)], fill=SEPC, width=1)
    return yy

def header(d, y, txt):
    d.text((X0+22, y), txt, font=FI(21, 'SemiBold'), fill=G2, anchor='lm'); return y+22

def base(title, back=True, right=None, time='21:40'):
    im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im); status(d, time); nav(d, title, back, right); return im, d

def homebar(d): d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=WHITE)

def save(im, n): im.save(OUT+n+'.png')

# ---- App Store Saracroche
def sara_icon(s):
    ic = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(ic)
    d.rounded_rectangle([0, 0, s-1, s-1], int(s*0.23), fill=(244, 196, 64))
    d.rounded_rectangle([s*0.36, s*0.14, s*0.68, s*0.74], int(s*0.06), fill=WHITE, outline=(30, 30, 30), width=max(2, s//40))
    d.ellipse([s*0.30, s*0.40, s*0.56, s*0.66], fill=(214, 40, 40), outline=WHITE, width=max(2, s//60))
    w = max(3, s//28); d.line([(s*0.37, s*0.47), (s*0.49, s*0.59)], fill=WHITE, width=w); d.line([(s*0.49, s*0.47), (s*0.37, s*0.59)], fill=WHITE, width=w)
    d.pieslice([-s*0.1, s*0.55, s*0.55, s*1.25], 270, 360, fill=(110, 70, 40))
    return ic

def appstore(btn):
    im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im); status(d, '21:38')
    d.ellipse([22, 80, 82, 140], fill=(44, 44, 46)); d.line([(58, 96), (44, 110), (58, 124)], fill=WHITE, width=4)
    ic = sara_icon(176); im.paste(ic, (30, 178), ic)
    d.text((232, 200), 'Saracroche :', font=FI(32, 'Bold'), fill=WHITE, anchor='lm')
    d.text((232, 240), "bloqueur d'appels", font=FI(32, 'Bold'), fill=WHITE, anchor='lm')
    d.text((232, 278), "Anti-spam d'appels et SMS", font=FI(21), fill=G2, anchor='lm')
    bw = 150 if btn == 'Obtenir' else 130
    d.rounded_rectangle([232, 306, 232+bw, 352], 23, fill=(100, 170, 255) if btn == 'Ouvrir' else BLU)
    d.text((232+bw/2, 329), btn, font=FI(23, 'Bold'), fill=WHITE, anchor='mm'); POS['as:btn'] = [232+bw/2, 329, 46]
    d.line([(30, 384), (SW, 384)], fill=SEPC)
    for i, (a, b, c) in enumerate([('12 K NOTES', '4,9', '★★★★★'), ("CATÉGORIE D'ÂGE", '4+', 'Ans'), ('CLASSEMENT', 'N°4', 'Utilitaires')]):
        cx = 100+i*172
        d.text((cx, 412), a, font=FI(15, 'SemiBold'), fill=G2, anchor='mm'); d.text((cx, 452), b, font=FI(34, 'Bold'), fill=(170, 170, 176), anchor='mm')
        d.text((cx, 492), c, font=FI(19 if i else 20), fill=G2, anchor='mm')
        if i: d.line([(cx-86, 400), (cx-86, 500)], fill=SEPC)
    d.line([(30, 522), (SW, 522)], fill=SEPC)
    d.text((30, 560), 'Nouveautés', font=FI(30, 'Bold'), fill=WHITE, anchor='lm')
    d.text((30, 606), 'Version 5.5.0', font=FI(21), fill=G2, anchor='lm'); d.text((570, 606), 'Il y a 1 sem.', font=FI(21), fill=G2, anchor='rm')
    d.text((30, 680), 'Aperçu', font=FI(30, 'Bold'), fill=WHITE, anchor='lm')
    for i in range(2):
        x = 30+i*330; d.rounded_rectangle([x, 720, x+310, 1200], 30, fill=(244, 196, 64))
        for k in range(4): d.rounded_rectangle([x+30, 760+k*48, x+30+[240, 200, 250, 170][k], 790+k*48], 8, fill=(40, 30, 10))
        d.rounded_rectangle([x+90, 980, x+220, 1200], 22, fill=WHITE, outline=(30, 30, 30), width=4)
    d.rounded_rectangle([30, 1170, 570, 1262], 46, fill=(38, 34, 28))
    for i, t in enumerate(["Aujourd'hui", 'Jeux', 'Apps', 'Arcade', 'Recherche']):
        d.text((84+i*108, 1240), t, font=FI(15, 'Medium'), fill=BLU if i == 4 else (230, 230, 230), anchor='mm')
        d.rounded_rectangle([70+i*108, 1186, 98+i*108, 1214], 7, outline=BLU if i == 4 else (230, 230, 230), width=3)
    homebar(d); return im
save(appstore('Obtenir'), 'as_get'); save(appstore('Ouvrir'), 'as_open')

# ---- Réglages
def reglages(hi=None):
    im, d = base('Réglages', back=False)
    y = 170
    y = card(im, y, [dict(label="Mode Avion", icon=((255, 149, 0), 'dot'), right=('tog', False)), dict(label='Wi-Fi', icon=(BLU, 'dot'), right=('val', 'Maison')),
                     dict(label='Bluetooth', icon=(BLU, 'dot'), right=('val', 'Oui')), dict(label='Batterie', icon=(GRN, 'sq'), right='>')]) + 30
    y = card(im, y, [dict(label='Général', icon=((142, 142, 147), 'dot'), right='>'), dict(label='Accessibilité', icon=(BLU, 'dot'), right='>'),
                     dict(label='Luminosité et affichage', icon=(BLU, 'dot'), right='>')]) + 30
    y = card(im, y, [dict(label='Notifications', icon=((255, 59, 48), 'sq'), right='>'), dict(label='Sons et vibrations', icon=((255, 45, 85), 'dot'), right='>'),
                     dict(label='Face ID et code', icon=(GRN, 'sq'), right='>'), dict(label='Confidentialité et sécurité', icon=(BLU, 'dot'), right='>')]) + 30
    y = card(im, y, [dict(label='Apps', icon=((94, 92, 230), 'grid'), right='>')], hi=hi, key='reg')
    d.rounded_rectangle([22, 1180, 578, 1240], 30, fill=(28, 28, 30)); d.text((60, 1210), 'Recherche', font=FI(22), fill=G2, anchor='lm')
    homebar(d); return im
save(reglages(), 'reg'); save(reglages('Apps'), 'reg_hi')

def apps(hi=None):
    im, d = base('Apps')
    y = header(d, 190, 'S') + 12
    y = card(im, y, [dict(label='Safari', icon=(BLU, 'dot'), right='>'), dict(label='Santé', icon=((255, 45, 85), 'dot'), right='>'),
                     dict(label='Saracroche', icon=((244, 196, 64), 'sara'), right='>'), dict(label='Shazam', icon=(BLU, 'dot'), right='>')], key='apps') + 30
    y = header(d, y+10, 'T') + 12
    y = card(im, y, [dict(label='Téléphone', icon=(GRN, 'phone'), right='>'), dict(label='TikTok', icon=((30, 30, 30), 'dot'), right='>'),
                     dict(label='Traduire', icon=(BLU, 'sq'), right='>'), dict(label='TV', icon=((70, 70, 76), 'sq'), right='>')], hi=hi, key='apps') + 30
    y = header(d, y+10, 'W') + 12
    card(im, y, [dict(label='Wallet', icon=((30, 30, 30), 'sq'), right='>'), dict(label='WhatsApp', icon=(GRN, 'phone'), right='>')])
    d.rounded_rectangle([22, 1180, 578, 1240], 30, fill=(28, 28, 30)); d.text((60, 1210), 'Rechercher dans les apps', font=FI(22), fill=G2, anchor='lm')
    homebar(d); return im
save(apps(), 'apps'); save(apps('Téléphone'), 'apps_hi')

J = "Les appels de numéros non enregistrés sonneront et les appels manqués seront affichés dans la liste des appels récents."
M = "Les correspondants dont le numéro n'est pas enregistré devront fournir plus d'informations avant que l'iPhone ne sonne. Des frais d'appel et de données peuvent s'appliquer."
N = "Les appels de numéros non enregistrés ne seront pas affichés. Ils seront transférés vers la messagerie vocale et apparaîtront dans la liste des appels récents."
def tel(sel='Jamais', hi=None):
    im, d = base('Téléphone')
    y = header(d, 180, 'Filtrer les correspondants inconnus'); POS['tel:hdr'] = [300, 180, 40]; y += 10
    y = card(im, y, [dict(label=l, desc=t, right='check' if sel == l else None) for l, t in
                     [('Jamais', J), ("Demander le motif de l'appel", M), ('Ne pas afficher', N)]], hi=hi, key='tel') + 30
    y = header(d, y+6, 'Filtrage des appels') + 10
    y = card(im, y, [dict(label='Correspondants inconnus', desc="Les appels manqués et les messages vocaux de numéros inconnus seront transférés vers la liste « Correspondants inconnus ».", right=('tog', False))]) + 26
    y = card(im, y, [dict(label='Contacts bloqués', right='>')]) + 26
    y = card(im, y, [dict(label='Assistance composition', right=('tog', True)), dict(label="Blocage d'appels et identification", right='>')], hi=hi, key='tel')
    homebar(d); return im
save(tel(), 'tel'); save(tel(hi="Blocage d'appels et identification"), 'tel_hi_bloc')
save(tel(hi="Demander le motif de l'appel"), 'tel_hi_motif'); save(tel("Demander le motif de l'appel"), 'tel_motif')

def bloc(on):
    im, d = base("Blocage d'appels et ide…", right='Modifier', time='21:40')
    y = header(d, 190, 'Identification des appels') + 12
    y = card(im, y, [dict(label='Email', icon=(BLU, 'mail'), right=('tog', False)), dict(label='Saracroche', icon=((244, 196, 64), 'sara'), right=('tog', on)),
                     dict(label='Orange Téléphone', icon=((255, 121, 0), 'orange'), right=('tog', False))], key='bloc') + 14
    for k, l in enumerate(wrap(d, "Autorisez les apps de blocage d'appels et d'identification pour bloquer des appels et afficher les numéros des appels entrants.", FI(19), 520)):
        d.text((X0+22, y+k*24), l, font=FI(19), fill=G2, anchor='lt')
    homebar(d); return im
save(bloc(False), 'bloc_off'); save(bloc(True), 'bloc_on')
POS['bloc:tog'] = [X1-61, POS['bloc:Saracroche'][1], 50]
POS['duree'] = 75.9  # longueur de voice.wav en secondes
json.dump(POS, open('src/data.json', 'w'), indent=0)
print(POS)

# ---- sons
T = 76.0; SR = 44100; au = np.zeros(int((T+0.5)*SR), np.float32)
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
sfx = json.load(open('scripts/sons_exemple.json'))
for t, k in sfx: add(max(0, t), S[k]*0.35/0.3)
au = np.clip(au, -1, 1); w = wave.open(OUT+'sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((au*32767).astype(np.int16).tobytes()); w.close()
