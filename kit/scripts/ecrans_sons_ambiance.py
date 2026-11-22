# Écrans « Sons en arrière-plan + Musique d'ambiance » (centre de contrôle sombre, réglages clairs, comme les captures de Nej, 22/11/2026). Lancer depuis kit/.
import sys, json, math
sys.path.insert(0, 'scripts')
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw, ImageFilter
OUT = 'public/'
W = (255, 255, 255); G2 = (160, 160, 166); BLU = (10, 132, 255); GRN = (52, 199, 89); RED = (255, 59, 48); NAV = (58, 110, 230)
POS = {}

def bg_blur():
    im = Image.new('RGB', (SW, SH), (70, 70, 74)); d = ImageDraw.Draw(im)
    for x, y, r, c in [(120, 300, 170, (95, 95, 100)), (480, 600, 180, (80, 80, 86)), (200, 1000, 200, (60, 60, 66)), (520, 760, 60, (120, 60, 40))]:
        d.ellipse([x-r, y-r, x+r, y+r], fill=c)
    return im.filter(ImageFilter.GaussianBlur(70))

def island(d): d.rounded_rectangle([SW/2-110, 20, SW/2+110, 72], 26, fill=(0, 0, 0))

def notes(d, x, y, s, col):  # icône ♩♩♩
    for i, dy in enumerate([4, -6, 4]):
        cx = x - 16*s + i*16*s
        d.ellipse([cx-6*s, y+10*s+dy*s-5*s, cx+4*s, y+10*s+dy*s+4*s], fill=col)
        d.line([(cx+3*s, y+10*s+dy*s), (cx+3*s, y-12*s+dy*s)], fill=col, width=max(2, int(3*s)))

def note_icon(d, x, y, col, kind):
    if kind == 'repos': d.text((x-18, y), 'z', font=FI(26, 'SemiBold'), fill=col, anchor='mm'); d.text((x-6, y-14), 'z', font=FI(18, 'SemiBold'), fill=col, anchor='mm')
    elif kind == 'relax':
        d.pieslice([x-30, y-14, x-2, y+14], 180, 360, fill=col); d.line([(x-36, y+4), (x+2, y+4)], fill=col, width=3)
    elif kind == 'prod': d.rounded_rectangle([x-32, y-14, x-6, y+12], 4, outline=col, width=3)
    else: d.ellipse([x-30, y-14, x-14, y+2], fill=col); d.ellipse([x-20, y-14, x-4, y+2], fill=col); d.polygon([(x-30, y-6), (x-4, y-6), (x-17, y+12)], fill=col)
    d.ellipse([x-2, y+4, x+14, y+18], fill=col); d.line([(x+12, y+10), (x+12, y-20)], fill=col, width=4); d.line([(x+12, y-20), (x+24, y-14)], fill=col, width=5)

def header(d, edit=False):
    island(d)
    d.ellipse([50, 30, 92, 72], fill=(120, 120, 126)); d.line([(71, 40), (71, 62)], fill=W, width=4); d.line([(60, 51), (82, 51)], fill=W, width=4)
    POS['plus'] = [71, 51]
    d.ellipse([508, 30, 550, 72], fill=(120, 120, 126)); d.arc([518, 41, 540, 63], 300, 240, fill=W, width=3); d.line([(529, 38), (529, 50)], fill=W, width=3)
    d.text((70, 160), 'Orange F 4G', font=FI(20, 'SemiBold'), fill=W, anchor='lm'); d.text((520, 160), '70 %', font=FI(20, 'SemiBold'), fill=W, anchor='rm')

TILE = (190, 190, 196, 150); TILE_ON = (255, 255, 255, 240)
MUS = [('Relaxation', 'relax'), ('Bien-être', 'bien'), ('Productivité', 'prod'), ('Repos', 'repos')]

def minus(d, x, y):
    d.ellipse([x-15, y-15, x+15, y+15], fill=(120, 120, 126)); d.line([(x-7, y), (x+7, y)], fill=W, width=4)

def cc_before(edit=False):
    """Centre de contrôle habituel (avant ajout)."""
    im = bg_blur(); d = ImageDraw.Draw(im, 'RGBA'); header(d)
    # bloc connexions + musique
    d.rounded_rectangle([50, 210, 290, 450], 46, fill=TILE)
    for i, c in enumerate([(255, 149, 0), GRN, BLU, BLU]):
        x, y = 110+(i % 2)*120, 270+(i//2)*120; d.ellipse([x-40, y-40, x+40, y+40], fill=c if i else (120, 120, 126, 200))
    d.rounded_rectangle([310, 210, 550, 450], 46, fill=TILE); d.text((340, 300), 'Pas de lecture', font=FI(19, 'SemiBold'), fill=W, anchor='lm')
    for r in range(2):
        for c in range(4):
            x, y = 110+c*126, 540+r*126; d.ellipse([x-48, y-48, x+48, y+48], fill=TILE)
            d.ellipse([x-14, y-14, x+14, y+14], outline=W, width=4)
            if edit: minus(d, x-36, y-36)
    for x, f in [(363, 0.6), (488, 0.35)]:
        d.rounded_rectangle([x-48, 790, x+48, 1020], 46, fill=TILE); d.rounded_rectangle([x-48, 1020-230*f, x+48, 1020], 46, fill=(255, 255, 255, 230))
    d.ellipse([62, 790, 158, 886], fill=TILE); d.ellipse([188, 790, 284, 886], fill=TILE)
    if edit:
        for x, y in [(110, 540), (236, 540)]: pass
        d.rounded_rectangle([150, 1150, 450, 1200], 25, fill=(150, 150, 156, 170))
        d.text((300, 1175), 'Ajouter une commande', font=FI(21, 'SemiBold'), fill=W, anchor='mm')
        POS['add'] = [300, 1175]
    POS['vide'] = [300, 1090]
    return im

def gallery(query='', results=None, hi=None):
    """Feuille « Ajouter une commande » avec recherche."""
    im = bg_blur().filter(ImageFilter.GaussianBlur(10)); d = ImageDraw.Draw(im, 'RGBA'); island(d)
    d.rounded_rectangle([20, 100, 580, 1320], 50, fill=(48, 48, 52, 245))
    d.rounded_rectangle([270, 116, 330, 122], 3, fill=(120, 120, 126))
    d.rounded_rectangle([46, 146, 554, 206], 30, fill=(78, 78, 84))
    d.ellipse([66, 164, 86, 184], outline=G2, width=3); d.line([(83, 181), (92, 190)], fill=G2, width=3)
    d.text((104, 176), query or 'Rechercher des commandes', font=FI(22, 'SemiBold' if query else 'Regular'), fill=W if query else G2, anchor='lm')
    if query: d.rectangle([108 + d.textlength(query, font=FI(22, 'SemiBold')), 160, 111 + d.textlength(query, font=FI(22, 'SemiBold')), 192], fill=BLU)
    POS['search'] = [300, 176]
    if results is None:
        y = 260
        for sec, n in [('Accessibilité', 4), ('Appareil photo', 3), ('Horloge', 4)]:
            d.text((60, y), sec, font=FI(21, 'SemiBold'), fill=W, anchor='lm'); y += 70
            for i in range(n):
                x = 100+i*130; d.ellipse([x-40, y-40, x+40, y+40], fill=(78, 78, 84)); d.ellipse([x-12, y-12, x+12, y+12], outline=W, width=3)
            y += 110
    elif results == 'sons':
        d.text((60, 270), 'Accessibilité', font=FI(21, 'SemiBold'), fill=W, anchor='lm')
        x, y = 120, 370; d.ellipse([x-56, y-56, x+56, y+56], fill=(78, 78, 84)); notes(d, x, y, 1.3, W)
        d.text((x, 452), 'Sons en', font=FI(18), fill=W, anchor='mm'); d.text((x, 476), 'arrière-plan', font=FI(18), fill=W, anchor='mm')
        POS['res_sons'] = [x, y]
    else:
        d.text((60, 270), 'Musique d’ambiance', font=FI(21, 'SemiBold'), fill=W, anchor='lm')
        for i, (lab, k) in enumerate(MUS):
            x = 95+i*137; y = 370; d.ellipse([x-54, y-54, x+54, y+54], fill=(78, 78, 84)); note_icon(d, x, y, W, k)
            d.text((x, 452), lab, font=FI(17), fill=W, anchor='mm'); POS['res_'+k] = [x, y]
    return im

def cc_after(playing=None, sons_on=False):
    """Centre de contrôle avec les 4 Musiques d'ambiance + Sons en arrière-plan (comme la capture de Nej)."""
    im = bg_blur(); d = ImageDraw.Draw(im, 'RGBA'); header(d)
    for i, (lab, k) in enumerate(MUS):
        x0, y0 = 50+(i % 2)*262, 210+(i//2)*250; on = playing == k
        d.rounded_rectangle([x0, y0, x0+238, y0+228], 50, fill=TILE_ON if on else TILE, outline=(255, 255, 255, 90), width=2)
        col = (30, 30, 30) if on else (235, 235, 240)
        note_icon(d, x0+72, y0+60, BLU if on else col, k)
        d.text((x0+28, y0+138), 'Musique d’ambiance', font=FI(17, 'SemiBold'), fill=col, anchor='lm')
        d.text((x0+28, y0+164), lab, font=FI(17, 'SemiBold'), fill=col, anchor='lm')
        d.text((x0+28, y0+192), 'Lecture' if on else 'À l’arrêt', font=FI(17), fill=col, anchor='lm')
        POS['t_'+k] = [x0+119, y0+114]
    x, y = 108, 785
    d.ellipse([x-56, y-56, x+56, y+56], fill=TILE_ON if sons_on else TILE); notes(d, x, y, 1.25, BLU if sons_on else W)
    POS['sons'] = [x, y]
    for i, (a, b) in enumerate([('Démarrer une', 'conversation'), ('Ouvrir', 'Claude')]):
        x0 = 50+i*262; d.rounded_rectangle([x0, 880, x0+238, 990], 55, fill=TILE)
        d.text((x0+100, 920), a, font=FI(17, 'SemiBold'), fill=W, anchor='lm'); d.text((x0+100, 948), b, font=FI(17, 'SemiBold'), fill=W, anchor='lm')
        d.ellipse([x0+28, 908, x0+80, 960], outline=W, width=3)
    return im

def bs_menu():
    im = bg_blur().filter(ImageFilter.GaussianBlur(14)); d = ImageDraw.Draw(im, 'RGBA'); island(d)
    x0, x1, y0 = 45, 555, 390
    d.rounded_rectangle([x0, y0, x1, y0+455], 50, fill=(168, 168, 172, 245))
    d.ellipse([x0+14, y0+14, x0+92, y0+92], fill=W); notes(d, x0+53, y0+53, 1.0, BLU)
    d.text((300, y0+40), 'Sons en arrière-plan', font=FI(23, 'SemiBold'), fill=W, anchor='mm')
    d.text((300, y0+68), 'Pluie sur le toit', font=FI(20), fill=W, anchor='mm')
    for yy in (108, 175, 248, 300, 375): d.line([(x0, y0+yy), (x1, y0+yy)], fill=(255, 255, 255, 120), width=1)
    d.text((x0+16, y0+140), 'Volume', font=FI(20, 'SemiBold'), fill=W, anchor='lm')
    d.polygon([(x0+20, y0+205), (x0+28, y0+205), (x0+36, y0+197), (x0+36, y0+227), (x0+28, y0+219), (x0+20, y0+219)], fill=W)
    d.rounded_rectangle([x0+56, y0+208, x0+430, y0+216], 4, fill=(230, 230, 235))
    d.rounded_rectangle([x0+390, y0+196, x0+446, y0+228], 16, fill=W); d.text((x1-16, y0+212), '100', font=FI(20), fill=W, anchor='rm')
    POS['m_vol'] = [300, y0+212]
    d.text((x0+16, y0+274), 'Sons', font=FI(20, 'SemiBold'), fill=W, anchor='lm')
    d.text((x0+16, y0+338), 'Son', font=FI(21), fill=W, anchor='lm'); d.text((x1-16, y0+338), 'Pluie sur le toit', font=FI(21), fill=W, anchor='rm')
    POS['m_son'] = [300, y0+338]
    d.text((300, y0+415), 'Réglages des sons en arrière-plan…', font=FI(20), fill=W, anchor='mm')
    POS['m_reg'] = [300, y0+415]
    return im

SONS = ['Bruit équilibré', 'Bruit clair', 'Bruit sombre', 'Océan', 'Pluie', 'Cours d’eau', 'Nuit', 'Feu', 'Rue', 'Vapeur', 'Avion', 'Bateau', 'Bus', 'Train', 'Pluie sur le toit', 'Nuit calme']
def bs_list(sel='Pluie sur le toit', top=0):
    im = bg_blur().filter(ImageFilter.GaussianBlur(14)); d = ImageDraw.Draw(im, 'RGBA'); island(d)
    d.rounded_rectangle([75, 95, 525, 1240], 46, fill=(40, 40, 42, 250))
    d.text((300, 150), 'Sons', font=FI(28, 'SemiBold'), fill=W, anchor='mm'); d.line([(75, 196), (525, 196)], fill=(80, 80, 84), width=1)
    for i, s in enumerate(SONS[top:top+16]):
        y = 236+i*62
        if y > 1210: break
        d.text((110, y), s, font=FI(23), fill=W, anchor='lm')
        if s == sel: d.line([(470, y), (480, y+10), (496, y-12)], fill=BLU, width=4)
        d.line([(110, y+31), (525, y+31)], fill=(66, 66, 70), width=1)
        POS['s_'+s] = [300, y]
    return im

# ---- réglages en mode clair (comme l'enregistrement d'écran de Nej)
LBG = (242, 242, 247); LTX = (0, 0, 0); LG = (128, 128, 133); LSEP = (220, 220, 225)
def lstatus(d):
    d.text((66, 44), '13:18', font=FI(24, 'SemiBold'), fill=LTX, anchor='lm'); d.rounded_rectangle([SW/2-64, 22, SW/2+64, 62], 21, fill=(0, 0, 0))
    for i in range(4): d.rounded_rectangle([452+i*9, 46-i*4, 458+i*9, 52], 2, fill=LTX)
    d.rounded_rectangle([500, 34, 540, 54], 6, fill=LTX)
def lnav(d, title):
    d.ellipse([20, 82, 76, 138], fill=W); d.line([(54, 96), (40, 110), (54, 124)], fill=LTX, width=4, joint='curve')
    d.text((SW/2, 110), title, font=FI(22 if len(title) < 26 else 19, 'SemiBold'), fill=LTX, anchor='mm')
def ltoggle(d, x, y, on):
    d.rounded_rectangle([x, y-19, x+66, y+19], 19, fill=GRN if on else (225, 225, 230)); kx = x+47 if on else x+19; d.ellipse([kx-16, y-16, kx+16, y+16], fill=W)
def card(d, y0, h): d.rounded_rectangle([22, y0, 578, y0+h], 26, fill=W)
def foot(d, y, txt):
    f = FI(15); words = txt.split(); line = ''; yy = y
    for w_ in words:
        tt = (line+' '+w_).strip()
        if d.textlength(tt, font=f) > 520: d.text((40, yy), line, font=f, fill=LG, anchor='lm'); yy += 20; line = w_
        else: line = tt
    d.text((40, yy), line, font=f, fill=LG, anchor='lm')

def reglages(lock_on=False, hi=None):
    im = Image.new('RGB', (SW, SH), LBG); d = ImageDraw.Draw(im); lstatus(d); lnav(d, 'Sons en arrière-plan')
    card(d, 170, 66); d.text((44, 203), 'Sons en arrière-plan', font=FI(21), fill=LTX, anchor='lm'); ltoggle(d, 490, 203, True)
    foot(d, 260, 'Émet des sons en arrière-plan pour masquer les bruits environnants indésirables. Ces sons peuvent réduire les distractions et améliorer la concentration.')
    card(d, 320, 66); d.text((44, 353), 'Son', font=FI(21), fill=LTX, anchor='lm'); d.text((540, 353), 'Pluie sur le toit  ›', font=FI(21), fill=LG, anchor='rm')
    card(d, 412, 110); d.text((44, 440), 'Volume Pluie sur le toit', font=FI(18), fill=LG, anchor='lm'); d.text((556, 440), '100', font=FI(18), fill=LG, anchor='rm')
    d.rounded_rectangle([70, 486, 520, 492], 3, fill=BLU); d.ellipse([500, 472, 540, 506], fill=W, outline=LSEP)
    card(d, 548, 190); d.text((44, 582), 'Utiliser à la lecture de médias', font=FI(21), fill=LTX, anchor='lm'); ltoggle(d, 490, 582, True)
    d.line([(44, 616), (578, 616)], fill=LSEP); d.text((44, 646), 'Volume à la lecture de médias', font=FI(18), fill=LG, anchor='lm'); d.text((556, 646), '64', font=FI(18), fill=LG, anchor='rm')
    d.rounded_rectangle([70, 684, 520, 690], 3, fill=LSEP); d.rounded_rectangle([70, 684, 330, 690], 3, fill=BLU); d.ellipse([312, 670, 352, 704], fill=W, outline=LSEP)
    d.text((44, 722), 'Lire l’échantillon', font=FI(19), fill=BLU, anchor='lm')
    card(d, 770, 66); d.text((44, 803), 'Égaliseur', font=FI(21), fill=LTX, anchor='lm'); d.text((540, 803), 'Non  ›', font=FI(21), fill=LG, anchor='rm')
    card(d, 862, 66); d.text((44, 895), 'Couper les sons avec un minuteur', font=FI(21), fill=LTX, anchor='lm'); d.text((540, 895), 'Non  ›', font=FI(21), fill=LG, anchor='rm')
    POS['r_timer'] = [300, 895]
    card(d, 954, 86); d.text((44, 984), 'Ne plus lire les sons en', font=FI(21), fill=LTX, anchor='lm'); d.text((44, 1012), 'mode verrouillé', font=FI(21), fill=LTX, anchor='lm')
    ltoggle(d, 490, 997, lock_on); POS['r_lock'] = [300, 997]; POS['r_lock_tg'] = [523, 997]
    foot(d, 1066, 'Lorsque cette option est activée, les sons en arrière-plan ne seront plus lus au verrouillage de l’iPhone.')
    return im

def minuteur(mode='delai'):
    im = Image.new('RGB', (SW, SH), LBG); d = ImageDraw.Draw(im); lstatus(d); lnav(d, 'Couper les sons avec un minuteur')
    card(d, 170, 66); d.text((44, 203), 'Minuteur', font=FI(21), fill=LTX, anchor='lm'); ltoggle(d, 490, 203, True)
    card(d, 262, 132)
    for i, l in enumerate(['À une heure précise', 'Après un certain délai']):
        y = 295+i*66; d.text((44, y), l, font=FI(21), fill=LTX, anchor='lm')
        if (mode == 'heure') == (i == 0): d.line([(522, y), (532, y+10), (550, y-12)], fill=BLU, width=4)
        POS['m_'+str(i)] = [300, y]
    d.line([(44, 328), (578, 328)], fill=LSEP)
    card(d, 420, 66); d.text((44, 453), 'Couper après' if mode == 'delai' else 'Couper à', font=FI(21), fill=LTX, anchor='lm')
    d.rounded_rectangle([440, 433, 558, 473], 20, fill=(232, 232, 237)); d.text((499, 453), '45 min' if mode == 'delai' else '01:00', font=FI(20), fill=LTX, anchor='mm')
    return im

cc_before().save(OUT+'sa_cc.png')
cc_before(True).save(OUT+'sa_edit.png')
gallery().save(OUT+'sa_gal.png')
gallery('Sons en arrière-plan', 'sons').save(OUT+'sa_gal_sons.png')
gallery('Musique d’ambiance', 'mus').save(OUT+'sa_gal_mus.png')
cc_after().save(OUT+'sa_after.png')
cc_after(sons_on=True).save(OUT+'sa_after_sons.png')
cc_after(playing='repos').save(OUT+'sa_after_repos.png')
bs_menu().save(OUT+'sa_menu.png')
bs_list().save(OUT+'sa_list.png')
reglages(True).save(OUT+'sa_reg_on.png')
reglages(False).save(OUT+'sa_reg_off.png')
minuteur('delai').save(OUT+'sa_min.png')
minuteur('heure').save(OUT+'sa_min_h.png')
print(json.dumps(POS))
json.dump(POS, open('scripts/sa_pos.json', 'w'))
