# Écrans « Au secours » (raccourci d'urgence créé par l'IA de Raccourcis), 22/11/2026. Lancer depuis kit/.
import sys, json
sys.path.insert(0, 'scripts')
from ui_iphone import FI, SW, SH, grad
from PIL import Image, ImageDraw, ImageFilter
OUT = 'public/'
W = (255, 255, 255); BLU = (10, 132, 255); GRN = (52, 199, 89); RED = (255, 59, 48)
LBG = (242, 242, 247); LTX = (0, 0, 0); LG = (128, 128, 133); LSEP = (220, 220, 225)
POS = {}

def status(d, dark=False):
    c = W if dark else LTX
    d.text((66, 44), '9:41', font=FI(24, 'SemiBold'), fill=c, anchor='lm'); d.rounded_rectangle([SW/2-64, 22, SW/2+64, 62], 21, fill=(0, 0, 0))
    for i in range(4): d.rounded_rectangle([452+i*9, 46-i*4, 458+i*9, 52], 2, fill=c)
    d.rounded_rectangle([500, 34, 540, 54], 6, fill=c)
def back(d, title):
    d.ellipse([20, 82, 76, 138], fill=W); d.line([(54, 96), (40, 110), (54, 124)], fill=LTX, width=4, joint='curve')
    d.text((SW/2, 110), title, font=FI(22, 'SemiBold'), fill=LTX, anchor='mm')
def toggle(d, x, y, on):
    d.rounded_rectangle([x, y-19, x+66, y+19], 19, fill=GRN if on else (225, 225, 230)); kx = x+47 if on else x+19; d.ellipse([kx-16, y-16, kx+16, y+16], fill=W)
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
    d = ImageDraw.Draw(im); d.rectangle([0, y0, SW, SH], fill=(209, 212, 219)); kw = 50
    for r, row in enumerate(['azertyuiop', 'qsdfghjklm', 'wxcvbn']):
        n = len(row); x0 = (SW-(n*kw+(n-1)*6))/2 if r < 2 else 128
        for i, ch in enumerate(row):
            x = x0+i*(kw+6); y = y0+14+r*88; d.rounded_rectangle([x, y, x+kw, y+74], 10, fill=W); d.text((x+kw/2, y+37), ch, font=FI(28), fill=LTX, anchor='mm')
    d.rounded_rectangle([150, y0+282, 450, y0+356], 10, fill=W); d.text((300, y0+319), 'espace', font=FI(22), fill=LTX, anchor='mm')

# ---- écran verrouillé
def lock(kind='plain'):
    im = grad(SW, SH, (60, 40, 150), (230, 90, 120)); d = ImageDraw.Draw(im, 'RGBA'); status(d, True)
    d.text((SW/2, 150), 'dimanche 22 novembre', font=FI(24, 'SemiBold'), fill=(255, 255, 255, 230), anchor='mm')
    d.text((SW/2, 250), '9:41', font=FI(150, 'Bold'), fill=(255, 255, 255, 240), anchor='mm')
    if kind == 'siri':
        g = Image.new('RGBA', (SW, SH)); gd = ImageDraw.Draw(g)
        for i, c in enumerate([(255, 80, 160), (120, 90, 255), (60, 200, 255), (255, 170, 60)]):
            gd.rectangle([0, 0, SW, SH], outline=c+(255,), width=26-i*5)
        g = g.filter(ImageFilter.GaussianBlur(10)); im.paste(g, (0, 0), g); d = ImageDraw.Draw(im, 'RGBA')
        d.rounded_rectangle([90, 1000, 510, 1084], 42, fill=(255, 255, 255, 235)); d.text((SW/2, 1042), '« Au secours »', font=FI(30, 'SemiBold'), fill=LTX, anchor='mm')
    if kind == 'done':
        d.rounded_rectangle([40, 420, 560, 780], 36, fill=(255, 255, 255, 235))
        d.text((70, 462), 'Au secours', font=FI(24, 'Bold'), fill=LTX, anchor='lm')
        for i, l in enumerate(['Lampe torche allumée', 'Volume à fond', 'Économie d’énergie activée', 'Position envoyée à Maman, Papa']):
            y = 520+i*64; d.ellipse([66, y-17, 100, y+17], fill=GRN); d.line([(74, y), (81, y+8), (93, y-8)], fill=W, width=4)
            d.text((118, y), l, font=FI(22), fill=LTX, anchor='lm')
    d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=W)
    return im

# ---- Réglages
def reglages():
    im = Image.new('RGB', (SW, SH), LBG); d = ImageDraw.Draw(im); status(d)
    d.text((32, 140), 'Réglages', font=FI(44, 'Bold'), fill=LTX, anchor='lm')
    groups = [[('Général', (142, 142, 147)), ('Accessibilité', BLU), ('Fond d’écran', (40, 170, 255)), ('Recherche', (142, 142, 147)), ('Siri', (60, 60, 200))],
              [('Notifications', RED), ('Sons et vibrations', (255, 45, 85)), ('Concentration', (88, 86, 214)), ('Temps d’écran', (88, 86, 214))],
              [('Face ID et code', GRN), ('SOS d’urgence', RED), ('Batterie', GRN), ('Confidentialité', BLU)]]
    y = 210
    for g in groups:
        d.rounded_rectangle([22, y, 578, y+len(g)*64], 26, fill=W)
        for i, (l, c) in enumerate(g):
            yy = y+32+i*64; sq(d, 64, yy, c); d.text((100, yy), l, font=FI(22), fill=LTX, anchor='lm'); d.text((552, yy), '›', font=FI(28), fill=(196, 196, 200), anchor='rm')
            if i < len(g)-1: d.line([(100, yy+32), (578, yy+32)], fill=LSEP)
            POS['r_'+l] = [300, yy]
        y += len(g)*64+36
    return im

# ---- Face ID et code
ROWS = ['Affichage du jour et Recherche', 'Centre de notifications', 'Centre de contrôle', 'Widgets de l’écran verrouillé', 'Activités en direct', 'Siri', 'Répondre par message', 'Maison', 'Cartes', 'Rappeler les appels manqués']
def faceid(siri=False):
    im = Image.new('RGB', (SW, SH), LBG); d = ImageDraw.Draw(im); status(d); back(d, 'Face ID et code')
    d.text((44, 196), 'AUTORISER L’ACCÈS EN MODE VERROUILLÉ', font=FI(17), fill=LG, anchor='lm')
    y0 = 224; d.rounded_rectangle([22, y0, 578, y0+len(ROWS)*66], 26, fill=W)
    for i, l in enumerate(ROWS):
        y = y0+33+i*66; d.text((44, y), l, font=FI(21), fill=LTX, anchor='lm')
        toggle(d, 490, y, siri if l == 'Siri' else l != 'Centre de contrôle')
        if i < len(ROWS)-1: d.line([(44, y+33), (578, y+33)], fill=LSEP)
        POS['f_'+l] = [300, y]
    return im

# ---- Raccourcis : tous les raccourcis
def allsc():
    im = Image.new('RGB', (SW, SH), LBG); d = ImageDraw.Draw(im); status(d)
    d.text((556, 110), '+', font=FI(48), fill=BLU, anchor='mm'); POS['plus'] = [556, 108]
    d.text((32, 175), 'Tous les raccourcis', font=FI(40, 'Bold'), fill=LTX, anchor='lm')
    d.rounded_rectangle([22, 220, 578, 266], 14, fill=(227, 227, 232)); d.text((60, 243), 'Rechercher', font=FI(21), fill=LG, anchor='lm')
    tiles = [('Nouveau raccourci 2', (230, 180, 60)), ('Rédiger une note', (150, 110, 230)), ('Ouvrir la radio', (60, 150, 240)), ('Télécharger', (230, 160, 60)),
             ('Enregistrer', (50, 120, 230)), ('Mode Sommeil', (60, 150, 240)), ('Minuteur', (225, 110, 110)), ('Itinéraire maison', (220, 120, 70)), ('Traduire', (50, 120, 230)), ('Musique', (230, 100, 130))]
    for i, (l, c) in enumerate(tiles):
        x = 22+(i % 2)*284; y = 290+(i//2)*150
        d.rounded_rectangle([x, y, x+272, y+138], 26, fill=c); d.ellipse([x+18, y+18, x+54, y+54], outline=W, width=4)
        d.text((x+20, y+108), l, font=FI(21, 'SemiBold'), fill=W, anchor='lm')
    return im

# ---- nouveau raccourci (demande écrite)
FULL = 'Quand je dis Au secours : allume la lampe torche, mets le volume à fond, active l’économie d’énergie, envoie ma position à Maman et Papa avec « Urgence, j’ai besoin d’aide », puis demande-moi si j’appelle le 112 ou Maman.'
CUTS = ['Quand je dis Au secours :', 'allume la lampe torche,', 'mets le volume à fond,', 'active l’économie d’énergie,', 'envoie ma position à Maman et Papa', 'avec « Urgence, j’ai besoin d’aide »,', 'puis demande-moi si j’appelle le 112 ou Maman.']
def newsc(n):
    im = Image.new('RGB', (SW, SH), LBG); d = ImageDraw.Draw(im); status(d); back(d, 'Nouveau raccourci')
    d.rounded_rectangle([22, 170, 578, 846], 30, fill=W)
    d.text((SW/2, 222), 'Que voulez-vous que', font=FI(26, 'Bold'), fill=LTX, anchor='mm'); d.text((SW/2, 258), 'votre raccourci fasse ?', font=FI(26, 'Bold'), fill=LTX, anchor='mm')
    d.rounded_rectangle([44, 300, 556, 820], 20, fill=(246, 246, 250), outline=(205, 205, 215), width=2)
    txt = ' '.join(CUTS[:n]); f = FI(24); y = 340
    if not txt: d.text((66, y), 'Décrivez votre raccourci…', font=f, fill=(170, 170, 176), anchor='lm'); d.line([(64, y-16), (64, y+16)], fill=BLU, width=3)
    for l in wrap(d, txt, f, 470): d.text((66, y), l, font=f, fill=LTX, anchor='lm'); y += 36
    if txt: lx = 66+d.textlength(wrap(d, txt, f, 470)[-1], font=f)+4; d.line([(lx, y-52), (lx, y-20)], fill=BLU, width=3)
    d.ellipse([500, 770, 544, 814], fill=BLU if n == len(CUTS) else (200, 200, 206)); d.line([(522, 802), (522, 782)], fill=W, width=4); d.line([(512, 790), (522, 780), (532, 790)], fill=W, width=4)
    POS['send'] = [522, 792]
    keyboard(im)
    return im

# ---- raccourci créé
ACTS = [('Allumer la lampe torche', (255, 159, 10)), ('Régler le volume sur 100 %', (255, 45, 85)), ('Activer le mode Économie d’énergie', GRN),
        ('Envoyer ma position à Maman, Papa', (52, 120, 246)), ('Message : « Urgence, j’ai besoin d’aide »', GRN), ('Demander : Maman ou 112 ?', (142, 142, 147))]
def done(name='Nouveau raccourci 3', edit=False):
    im = Image.new('RGB', (SW, SH), LBG); d = ImageDraw.Draw(im); status(d)
    d.ellipse([20, 82, 76, 138], fill=W); d.line([(54, 96), (40, 110), (54, 124)], fill=LTX, width=4, joint='curve')
    d.text((550, 110), 'OK', font=FI(24, 'SemiBold'), fill=BLU, anchor='rm')
    tw = d.textlength(name, font=FI(23, 'SemiBold'))
    if edit:
        d.rounded_rectangle([SW/2-tw/2-24, 88, SW/2+tw/2+24, 132], 14, fill=W, outline=BLU, width=3)
        d.line([(SW/2+tw/2+6, 96), (SW/2+tw/2+6, 124)], fill=BLU, width=3)
    d.text((SW/2, 110), name + ('' if edit else '  ⌄'), font=FI(23, 'SemiBold'), fill=LTX, anchor='mm'); POS['title'] = [300, 110]
    for i, (l, c) in enumerate(ACTS):
        y = 180+i*104; d.rounded_rectangle([22, y, 578, y+88], 22, fill=W); sq(d, 62, y+44, c)
        f = FI(21 if len(l) < 32 else 19); d.text((96, y+44), l, font=f, fill=LTX, anchor='lm')
    if edit: keyboard(im)
    else: d.text((SW/2, 840), 'Rechercher des actions', font=FI(21), fill=LG, anchor='mm')
    return im

# ---- test : la question
def ask():
    im = lock('plain').filter(ImageFilter.GaussianBlur(18)); d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle([50, 480, 550, 860], 40, fill=(245, 245, 248, 250))
    d.text((SW/2, 540), 'Au secours', font=FI(22, 'SemiBold'), fill=LG, anchor='mm')
    d.text((SW/2, 586), 'Qui veux-tu appeler ?', font=FI(28, 'Bold'), fill=LTX, anchor='mm')
    for i, (l, c) in enumerate([('Maman', GRN), ('112', RED)]):
        y = 650+i*86; d.rounded_rectangle([80, y, 520, y+70], 20, fill=c); d.text((SW/2, y+35), l, font=FI(26, 'SemiBold'), fill=W, anchor='mm'); POS['a_'+l] = [300, y+35]
    d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=W)
    return im

lock().save(OUT+'as_lock.png'); lock('siri').save(OUT+'as_siri.png'); lock('done').save(OUT+'as_done.png')
reglages().save(OUT+'as_reg.png'); faceid(False).save(OUT+'as_fid0.png'); faceid(True).save(OUT+'as_fid1.png')
allsc().save(OUT+'as_all.png')
for n in range(len(CUTS)+1): newsc(n).save(OUT+f'as_new{n}.png')
done().save(OUT+'as_sc.png'); done('Au secours', True).save(OUT+'as_name.png'); done('Au secours').save(OUT+'as_sc2.png'); ask().save(OUT+'as_ask.png')
POS['duree'] = 65.0
json.dump(POS, open('src/data.json', 'w'), indent=0)
print(POS)
