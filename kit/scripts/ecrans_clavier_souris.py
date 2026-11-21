# Écrans « clavier = souris » (Notes + clavier, mode SOMBRE) pour le format court sur le son. Lancer depuis kit/.
import sys, json
sys.path.insert(0, 'scripts')
import ui_iphone as ui
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw
ui.init()
OUT = 'public/'; W = (255, 255, 255); G2 = (152, 152, 159); YEL = (255, 204, 0)
FAUX = "On se retrouve au restaurent à 20h ce soir ?"
BON = "On se retrouve au restaurant à 20h ce soir ?"
TX, TY, FONT = 40, 690, FI(34)
POS = {}

def status(d):
    d.text((70, 44), '11:30', font=FI(25, 'SemiBold'), fill=W, anchor='lm')
    d.rounded_rectangle([SW/2-64, 22, SW/2+64, 62], 21, fill=(0, 0, 0))
    for i in range(4): d.rounded_rectangle([452+i*9, 46-i*4, 458+i*9, 52], 2, fill=W)
    d.rounded_rectangle([500, 34, 540, 54], 6, fill=W)

def lines(d, text, maxw=520):
    out, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=FONT) <= maxw: cur = t
        else: out.append(cur); cur = w
    out.append(cur); return out

def notes(text, track=False):
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); d = ImageDraw.Draw(im); status(d)
    d.ellipse([22, 80, 82, 140], fill=(44, 44, 46)); d.line([(58, 96), (44, 110), (58, 124)], fill=YEL, width=4)
    d.rounded_rectangle([470, 84, 578, 136], 26, fill=YEL); d.text((524, 110), 'OK', font=FI(24, 'SemiBold'), fill=(0, 0, 0), anchor='mm')
    d.text((TX, 200), '21 novembre 2026 à 11:30', font=FI(18), fill=G2, anchor='lm')
    for k, l in enumerate(['Samedi soir', '', 'Réserver la table pour 4', 'Prévenir Léa et Karim', "Prendre le cadeau d'anniversaire"]):
        d.text((TX, 250 + k*48), l, font=FI(34, 'Bold') if k == 0 else FONT, fill=W if k == 0 else (200, 200, 205), anchor='lt')
    for k, l in enumerate(lines(d, text)): d.text((TX, TY + k*48), l, font=FONT, fill=W, anchor='lt')
    # clavier
    kb_top = 840; d.rectangle([0, kb_top, SW, SH], fill=(44, 44, 46))
    rows = ['azertyuiop', 'qsdfghjklm', 'wxcvbn']
    key = (74, 74, 78) if not track else (64, 64, 68)
    for r, row in enumerate(rows):
        n = len(row); kw = 52; gap = 6; x0 = (SW - (n*kw + (n-1)*gap))/2 if r < 2 else 110
        for i, ch in enumerate(row):
            x = x0 + i*(kw+gap); y = kb_top + 20 + r*96
            d.rounded_rectangle([x, y, x+kw, y+80], 10, fill=key)
            if not track: d.text((x+kw/2, y+40), ch, font=FI(30), fill=W, anchor='mm')
    y = kb_top + 20 + 3*96
    d.rounded_rectangle([14, y, 128, y+80], 10, fill=(90, 90, 94) if not track else key)
    if not track: d.text((71, y+40), '123', font=FI(24), fill=W, anchor='mm')
    d.rounded_rectangle([140, y, 460, y+80], 10, fill=key)
    if not track: d.text((300, y+40), 'espace', font=FI(24), fill=W, anchor='mm')
    POS['espace'] = [300, y+40]
    d.rounded_rectangle([472, y, 586, y+80], 10, fill=(90, 90, 94) if not track else key)
    if not track: d.text((529, y+40), 'retour', font=FI(22), fill=W, anchor='mm')
    d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=W)
    return im, d

im, d = notes(FAUX); im.save(OUT+'cs_notes.png')
im, d = notes(FAUX, True); im.save(OUT+'cs_track.png')
im, d = notes(BON); im.save(OUT+'cs_ok.png')
# positions du curseur (x, y) : fin du texte, puis glisse jusqu'à « restaurent » (entre « a » et « u » fautifs → on vise « e » de -ent)
ls = lines(d, FAUX)
def pos_after(sub, line_idx):
    l = ls[line_idx]; i = l.index(sub) + len(sub)
    return [round(TX + d.textlength(l[:i], font=FONT)), TY + line_idx*48]
li = next(i for i, l in enumerate(ls) if 'restaurent' in l)
POS['cur_end'] = [round(TX + d.textlength(ls[-1], font=FONT)), TY + (len(ls)-1)*48]
POS['cur_err'] = pos_after('restaur', li)          # juste avant le « e » fautif
l = ls[li]; i0 = l.index('restaurent') + len('restaur')
POS['err_box'] = [round(TX + d.textlength(l[:i0], font=FONT)), TY + li*48, round(d.textlength('e', font=FONT))]
POS['wrong_taps'] = [[150, TY + 20], [420, TY + li*48 + 70], [260, TY + li*48 - 30]]
POS['duree'] = 16.1
json.dump(POS, open('src/data.json', 'w'), indent=0); print(POS)
