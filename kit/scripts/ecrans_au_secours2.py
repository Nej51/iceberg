# Écrans « Au secours » v2 (26/11/2026) — MODE SOMBRE, nouvel exemple (ma sœur), « Décrire un raccourci » (iOS 27).
# Refaite car TikTok avait jugé la v1 « non originale ». Lancer depuis kit/.
import sys, json
sys.path.insert(0, 'scripts')
from ui_iphone import FI, SW, SH, grad
from PIL import Image, ImageDraw, ImageFilter
OUT = 'public/'
W = (255, 255, 255); BLU = (10, 132, 255); GRN = (48, 209, 88); RED = (255, 69, 58)
BG = (0, 0, 0); CARD = (28, 28, 30); TX = (255, 255, 255); G = (142, 142, 147); SEP = (56, 56, 58); FIELD = (44, 44, 46)
POS = {}

def status(d):
    d.text((66, 44), '9:41', font=FI(24, 'SemiBold'), fill=TX, anchor='lm'); d.rounded_rectangle([SW/2-64, 22, SW/2+64, 62], 21, fill=(0, 0, 0))
    for i in range(4): d.rounded_rectangle([452+i*9, 46-i*4, 458+i*9, 52], 2, fill=TX)
    d.rounded_rectangle([500, 34, 540, 54], 6, fill=TX)
def homebar(d): d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=W)
def back(d, title):
    d.ellipse([20, 82, 76, 138], fill=CARD); d.line([(54, 96), (40, 110), (54, 124)], fill=TX, width=4, joint='curve')
    d.text((SW/2, 110), title, font=FI(22, 'SemiBold'), fill=TX, anchor='mm')
def toggle(d, x, y, on):
    d.rounded_rectangle([x, y-19, x+66, y+19], 19, fill=GRN if on else (57, 57, 61)); kx = x+47 if on else x+19; d.ellipse([kx-16, y-16, kx+16, y+16], fill=W)
def sq(d, x, y, c): d.rounded_rectangle([x-17, y-17, x+17, y+17], 8, fill=c)
def wrap(d, txt, f, maxw):
    out, line = [], ''
    for w_ in txt.split(' '):
        tt = (line+' '+w_).strip()
        if d.textlength(tt, font=f) > maxw and line: out.append(line); line = w_
        else: line = tt
    if line: out.append(line)
    return out
def keyboard(im, y0=880):
    d = ImageDraw.Draw(im); d.rectangle([0, y0, SW, SH], fill=(43, 43, 45)); kw = 50
    for r, row in enumerate(['azertyuiop', 'qsdfghjklm', 'wxcvbn']):
        n = len(row); x0 = (SW-(n*kw+(n-1)*6))/2 if r < 2 else 128
        for i, ch in enumerate(row):
            x = x0+i*(kw+6); y = y0+14+r*88; d.rounded_rectangle([x, y, x+kw, y+74], 10, fill=(108, 108, 112)); d.text((x+kw/2, y+37), ch, font=FI(28), fill=TX, anchor='mm')
    d.rounded_rectangle([150, y0+282, 450, y0+356], 10, fill=(108, 108, 112)); d.text((300, y0+319), 'espace', font=FI(22), fill=TX, anchor='mm')
def sparkle(d, x, y, r, c):
    d.polygon([(x, y-r), (x+r*0.28, y-r*0.28), (x+r, y), (x+r*0.28, y+r*0.28), (x, y+r), (x-r*0.28, y+r*0.28), (x-r, y), (x-r*0.28, y-r*0.28)], fill=c)

# ---- écran verrouillé (fond nuit)
def lock(kind='plain'):
    im = grad(SW, SH, (8, 12, 40), (40, 20, 90)); d = ImageDraw.Draw(im, 'RGBA'); status(d)
    d.text((SW/2, 150), 'jeudi 26 novembre', font=FI(24, 'SemiBold'), fill=(255, 255, 255, 220), anchor='mm')
    d.text((SW/2, 250), '21:47', font=FI(150, 'Bold'), fill=(255, 255, 255, 235), anchor='mm')
    if kind == 'siri':
        g = Image.new('RGBA', (SW, SH)); gd = ImageDraw.Draw(g)
        for i, c in enumerate([(255, 80, 160), (120, 90, 255), (60, 200, 255), (255, 170, 60)]):
            gd.rectangle([0, 0, SW, SH], outline=c+(255,), width=26-i*5)
        g = g.filter(ImageFilter.GaussianBlur(10)); im.paste(g, (0, 0), g); d = ImageDraw.Draw(im, 'RGBA')
        d.rounded_rectangle([80, 1000, 520, 1084], 42, fill=(40, 40, 46, 235)); d.text((SW/2, 1042), 'Dis Siri, au secours', font=FI(30, 'SemiBold'), fill=TX, anchor='mm')
    if kind == 'done':
        d.rounded_rectangle([40, 420, 560, 780], 36, fill=(40, 40, 46, 235))
        d.text((70, 462), 'Au secours', font=FI(24, 'Bold'), fill=TX, anchor='lm')
        for i, l in enumerate(['Lampe torche allumée', 'Volume au maximum', 'Économie d’énergie activée', 'Position envoyée à Sœur']):
            y = 520+i*64; d.ellipse([66, y-17, 100, y+17], fill=BLU); d.line([(74, y), (81, y+8), (93, y-8)], fill=W, width=4)
            d.text((118, y), l, font=FI(22), fill=TX, anchor='lm')
    if kind == 'allow':
        im = im.filter(ImageFilter.GaussianBlur(18)); d = ImageDraw.Draw(im, 'RGBA')
        d.rounded_rectangle([50, 470, 550, 900], 40, fill=(44, 44, 48, 250))
        d.text((SW/2, 530), 'Autoriser « Au secours »', font=FI(26, 'Bold'), fill=TX, anchor='mm')
        d.text((SW/2, 570), 'à envoyer un message', font=FI(26, 'Bold'), fill=TX, anchor='mm')
        d.text((SW/2, 610), 'à Sœur ?', font=FI(26, 'Bold'), fill=TX, anchor='mm')
        for i, l in enumerate(['Autoriser une fois', 'Toujours autoriser', 'Ne pas autoriser']):
            y = 660+i*76; d.line([(50, y), (550, y)], fill=SEP, width=2); d.text((SW/2, y+38), l, font=FI(25, 'SemiBold' if i == 1 else 'Regular'), fill=BLU, anchor='mm')
            POS['al_'+str(i)] = [300, y+38]
    homebar(d)
    return im

# ---- Réglages
def reglages():
    im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im); status(d)
    d.text((32, 140), 'Réglages', font=FI(44, 'Bold'), fill=TX, anchor='lm')
    groups = [[('Général', (142, 142, 147)), ('Accessibilité', BLU), ('Fond d’écran', (40, 170, 255)), ('Siri', (60, 60, 200)), ('Caméra', (142, 142, 147))],
              [('Notifications', RED), ('Sons et vibrations', (255, 45, 85)), ('Concentration', (94, 92, 230)), ('Temps d’écran', (94, 92, 230))],
              [('Face ID et code', GRN), ('Appel d’urgence SOS', RED), ('Batterie', GRN), ('Confidentialité et sécurité', BLU)]]
    y = 210
    for g in groups:
        d.rounded_rectangle([22, y, 578, y+len(g)*64], 26, fill=CARD)
        for i, (l, c) in enumerate(g):
            yy = y+32+i*64; sq(d, 64, yy, c); d.text((100, yy), l, font=FI(22), fill=TX, anchor='lm'); d.text((552, yy), '›', font=FI(28), fill=(98, 98, 102), anchor='rm')
            if i < len(g)-1: d.line([(100, yy+32), (578, yy+32)], fill=SEP)
            POS['r_'+l] = [300, yy]
        y += len(g)*64+36
    homebar(d); return im

# ---- Face ID et code (partie basse)
ROWS = ['Affichage du jour et Recherche', 'Centre de notifications', 'Centre de contrôle', 'Widgets de l’écran verrouillé', 'Activités en direct', 'Siri', 'Répondre par message', 'Contrôle du domicile', 'Portefeuille', 'Rappeler les appels manqués']
def faceid(siri=False):
    im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im); status(d); back(d, 'Face ID et code')
    d.text((44, 196), 'AUTORISER L’ACCÈS EN MODE VERROUILLÉ', font=FI(17), fill=G, anchor='lm')
    y0 = 224; d.rounded_rectangle([22, y0, 578, y0+len(ROWS)*66], 26, fill=CARD)
    for i, l in enumerate(ROWS):
        y = y0+33+i*66; d.text((44, y), l, font=FI(21), fill=TX, anchor='lm')
        toggle(d, 490, y, siri if l == 'Siri' else l not in ('Centre de contrôle', 'Contrôle du domicile'))
        if i < len(ROWS)-1: d.line([(44, y+33), (578, y+33)], fill=SEP)
        POS['f_'+l] = [300, y]
    homebar(d); return im

# ---- Raccourcis
def allsc(menu=False):
    im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im, 'RGBA'); status(d)
    d.ellipse([522, 82, 578, 138], fill=CARD); d.text((550, 108), '+', font=FI(44), fill=TX, anchor='mm'); POS['plus'] = [550, 110]
    d.text((32, 175), 'Raccourcis', font=FI(40, 'Bold'), fill=TX, anchor='lm')
    d.rounded_rectangle([22, 220, 578, 266], 14, fill=FIELD); d.text((60, 243), 'Rechercher', font=FI(21), fill=G, anchor='lm')
    tiles = [('Rentrer à la maison', (52, 120, 246)), ('Mode Lecture', (94, 92, 230)), ('Minuteur pâtes', (255, 120, 80)), ('Note vocale', (230, 80, 120)),
             ('Wi-Fi invités', (40, 170, 160)), ('Réveil week-end', (255, 159, 10)), ('Playlist sport', (48, 170, 90)), ('Photo du jour', (150, 110, 230))]
    for i, (l, c) in enumerate(tiles):
        x = 22+(i % 2)*284; y = 290+(i//2)*150
        d.rounded_rectangle([x, y, x+272, y+138], 26, fill=c); d.ellipse([x+18, y+18, x+54, y+54], outline=W, width=4)
        d.text((x+20, y+108), l, font=FI(21, 'SemiBold'), fill=W, anchor='lm')
    if menu:
        d.rectangle([0, 0, SW, SH], fill=(0, 0, 0, 120))
        d.rounded_rectangle([0, 760, SW, SH], 40, fill=(36, 36, 40))
        d.rounded_rectangle([SW/2-40, 776, SW/2+40, 782], 3, fill=(90, 90, 94))
        d.text((SW/2, 830), 'Nouveau raccourci', font=FI(26, 'Bold'), fill=TX, anchor='mm')
        opts = [('Décrire un raccourci', 'Apple Intelligence le crée pour toi', True), ('Créer à la main', 'Ajouter des actions une par une', False)]
        for i, (a, b, ai) in enumerate(opts):
            y = 890+i*130; d.rounded_rectangle([30, y, 570, y+112], 26, fill=(54, 54, 58))
            if ai:
                g = grad(56, 56, (255, 120, 80), (120, 90, 255)); m = Image.new('L', (56, 56), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 55, 55], 14, fill=255)
                im.paste(g, (52, y+28), m); d = ImageDraw.Draw(im, 'RGBA'); sparkle(d, 80, y+56, 18, W)
            else: d.rounded_rectangle([52, y+28, 108, y+84], 14, fill=(90, 90, 94)); d.text((80, y+56), '+', font=FI(34), fill=W, anchor='mm')
            d.text((130, y+40), a, font=FI(24, 'SemiBold'), fill=TX, anchor='lm'); d.text((130, y+76), b, font=FI(19), fill=G, anchor='lm')
            POS['opt'+str(i)] = [300, y+56]
    homebar(d); return im

# ---- décrire (texte tapé morceau par morceau)
CUTS = ['Allume la lampe torche,', 'monte le volume au maximum,', 'active le mode économie d’énergie,', 'envoie ma position à ma sœur', 'avec le message « J’ai besoin d’aide »,', 'puis propose-moi d’appeler le 112 ou ma sœur.']
def describe(n, loading=False):
    im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im, 'RGBA'); status(d); back(d, 'Décrire un raccourci')
    g = grad(SW-44, 6, (255, 120, 80), (120, 90, 255), True); im.paste(g, (22, 168)); d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle([22, 190, 578, 846], 30, fill=CARD)
    d.text((SW/2, 240), 'Que doit faire', font=FI(26, 'Bold'), fill=TX, anchor='mm'); d.text((SW/2, 276), 'ton raccourci ?', font=FI(26, 'Bold'), fill=TX, anchor='mm')
    d.rounded_rectangle([44, 316, 556, 820], 20, fill=FIELD)
    txt = ' '.join(CUTS[:n]); f = FI(24); y = 356
    if not txt: d.text((66, y), 'Décris ce que tu veux…', font=f, fill=G, anchor='lm'); d.line([(64, y-16), (64, y+16)], fill=BLU, width=3)
    lines = wrap(d, txt, f, 470)
    for l in lines: d.text((66, y), l, font=f, fill=TX, anchor='lm'); y += 36
    if txt and not loading: lx = 66+d.textlength(lines[-1], font=f)+4; d.line([(lx, y-52), (lx, y-20)], fill=BLU, width=3)
    d.ellipse([500, 770, 544, 814], fill=BLU if n == len(CUTS) else (80, 80, 84)); d.line([(522, 802), (522, 782)], fill=W, width=4); d.line([(512, 790), (522, 780), (532, 790)], fill=W, width=4)
    POS['send'] = [522, 792]
    if loading:
        d.rounded_rectangle([22, 870, 578, 960], 26, fill=CARD); sparkle(d, 80, 915, 20, (180, 140, 255))
        d.text((118, 915), 'Création du raccourci…', font=FI(24, 'SemiBold'), fill=TX, anchor='lm')
    else: keyboard(im)
    homebar(d); return im

# ---- raccourci créé
ACTS = [('Allumer la lampe torche', (255, 159, 10)), ('Régler le volume sur 100 %', (255, 45, 85)), ('Activer le mode Économie d’énergie', GRN),
        ('Envoyer ma position à Sœur', (52, 120, 246)), ('Message : « J’ai besoin d’aide »', GRN), ('Choisir : appeler le 112 ou Sœur', (142, 142, 147))]
def done(name='Nouveau raccourci', edit=False):
    im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im); status(d)
    d.ellipse([20, 82, 76, 138], fill=CARD); d.line([(54, 96), (40, 110), (54, 124)], fill=TX, width=4, joint='curve')
    d.text((550, 110), 'OK', font=FI(24, 'SemiBold'), fill=BLU, anchor='rm')
    tw = d.textlength(name, font=FI(23, 'SemiBold'))
    if edit:
        d.rounded_rectangle([SW/2-tw/2-24, 88, SW/2+tw/2+24, 132], 14, fill=FIELD, outline=BLU, width=3)
        d.line([(SW/2+tw/2+6, 96), (SW/2+tw/2+6, 124)], fill=BLU, width=3)
    d.text((SW/2, 110), name + ('' if edit else '  ⌄'), font=FI(23, 'SemiBold'), fill=TX, anchor='mm'); POS['title'] = [300, 110]
    for i, (l, c) in enumerate(ACTS):
        y = 180+i*104; d.rounded_rectangle([22, y, 578, y+88], 22, fill=CARD); sq(d, 62, y+44, c)
        f = FI(21 if len(l) < 32 else 19); d.text((96, y+44), l, font=f, fill=TX, anchor='lm')
    if edit: keyboard(im)
    else: d.text((SW/2, 840), 'Rechercher des actions', font=FI(21), fill=G, anchor='mm'); homebar(d)
    return im

lock().save(OUT+'s2_lock.png'); lock('siri').save(OUT+'s2_siri.png'); lock('done').save(OUT+'s2_done.png'); lock('allow').save(OUT+'s2_allow.png')
reglages().save(OUT+'s2_reg.png'); faceid(False).save(OUT+'s2_fid0.png'); faceid(True).save(OUT+'s2_fid1.png')
allsc().save(OUT+'s2_all.png'); allsc(True).save(OUT+'s2_menu.png')
for n in range(len(CUTS)+1): describe(n).save(OUT+f's2_d{n}.png')
describe(len(CUTS), True).save(OUT+'s2_load.png')
done().save(OUT+'s2_sc.png'); done('Au secours', True).save(OUT+'s2_name.png'); done('Au secours').save(OUT+'s2_sc2.png')
json.dump(POS, open('src/data_s2.json', 'w'), indent=0)
print(POS)
