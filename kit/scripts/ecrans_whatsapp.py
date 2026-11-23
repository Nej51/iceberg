# Écrans « Conversation WhatsApp invisible » (code secret) + sons. Lancer depuis kit/. Contacts inventés.
import sys, json, wave, numpy as np
sys.path.insert(0, 'scripts')
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw
OUT = 'public/'
W = (255, 255, 255); G2 = (142, 142, 147); G3 = (100, 100, 105); BG = (11, 11, 12); CARD = (30, 30, 32); SEP = (44, 44, 46)
WGRN = (37, 211, 102); LGRN = (140, 230, 150); DGRN = (18, 60, 38)
KB_BG = (38, 38, 40); KEY = (100, 100, 104); KEY2 = (70, 70, 74)
POS = {}
CHATS = [('Famille', 'Maman : On mange à 20h', '18:44', (230, 120, 90)), ('Foot du jeudi', 'Hugo : Qui ramène le ballon ?', '17:02', (90, 140, 230)),
         ('Sarah', 'Tu as vu la surprise ?', '15:30', (200, 110, 200)), ('Thomas', 'Ok pour demain', '12:10', (240, 180, 70)),
         ('Léa', 'Merci pour hier !', '09:32', (120, 110, 200)), ('Travail', 'Réunion décalée à 14h', 'hier', (80, 180, 160))]

def status(d):
    d.text((70, 44), '22:30', font=FI(25, 'SemiBold'), fill=W, anchor='lm')
    d.rounded_rectangle([SW/2-64, 22, SW/2+64, 62], 21, fill=(0, 0, 0))
    for i in range(4): d.rounded_rectangle([440+i*9, 46-i*4, 446+i*9, 52], 2, fill=W)
    d.rounded_rectangle([500, 34, 540, 54], 6, fill=W); d.text((520, 44), '57', font=FI(15, 'Bold'), fill=(0, 0, 0), anchor='mm')
def homebar(d): d.rounded_rectangle([SW/2-70, 1278, SW/2+70, 1287], 5, fill=W)
def avatar(d, cx, cy, r, name, col):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=col); d.text((cx, cy), name[0], font=FI(int(r*0.9), 'SemiBold'), fill=W, anchor='mm')
def lock_ic(d, x, y, col=G2):
    d.rounded_rectangle([x-14, y-6, x+14, y+16], 5, outline=col, width=3); d.arc([x-9, y-20, x+9, y-2], 180, 360, fill=col, width=3)
    d.line([(x-6, y+4), (x+6, y+4)], fill=col, width=2); d.line([(x-6, y+10), (x+3, y+10)], fill=col, width=2)
def box_ic(d, x, y, col=G2):
    d.rectangle([x-14, y-12, x+14, y-4], outline=col, width=3); d.rectangle([x-11, y-4, x+11, y+14], outline=col, width=3); d.line([(x-4, y+2), (x+4, y+2)], fill=col, width=3)
def chat_row(d, y, name, msg, t, col):
    avatar(d, 52, y, 34, name, col)
    d.text((104, y-14), name, font=FI(24, 'SemiBold'), fill=W, anchor='lm'); d.text((SW-24, y-14), t, font=FI(18), fill=G2, anchor='rm')
    d.text((104, y+16), msg, font=FI(20), fill=G2, anchor='lm')
def tabbar(d):
    d.rounded_rectangle([20, 1186, SW-20, 1260], 37, fill=(28, 28, 30))
    for i, n in enumerate(['Actus', 'Appels', 'Commun.', 'Discussions', 'Vous']):
        x = 70+i*115; c = W if n == 'Discussions' else G2
        if n == 'Discussions': d.rounded_rectangle([x-56, 1192, x+56, 1254], 31, fill=(50, 50, 54))
        d.ellipse([x-12, 1200, x+12, 1224], outline=c, width=3); d.text((x, 1238), n, font=FI(14, 'SemiBold'), fill=c, anchor='mm')

def w_list(folder=True, search=None, found=False):
    im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im); status(d)
    d.ellipse([20, 80, 76, 136], fill=(36, 36, 38)); d.text((48, 106), '•••', font=FI(18, 'Bold'), fill=W, anchor='mm')
    d.ellipse([452, 80, 508, 136], fill=(36, 36, 38)); d.rounded_rectangle([466, 98, 494, 120], 5, outline=W, width=3)
    d.ellipse([520, 80, 576, 136], fill=LGRN); d.text((548, 107), '+', font=FI(36), fill=(0, 0, 0), anchor='mm')
    d.text((24, 176), 'Discussions', font=FI(44, 'Bold'), fill=W, anchor='lm')
    d.rounded_rectangle([22, 214, SW-22, 262], 24, fill=(36, 36, 38))
    if search: d.text((60, 238), search, font=FI(23), fill=W, anchor='lm'); d.line([(62+d.textlength(search, font=FI(23)), 224), (62+d.textlength(search, font=FI(23)), 252)], fill=WGRN, width=3)
    else: d.text((60, 238), 'Demander à Meta AI ou rechercher', font=FI(21), fill=G2, anchor='lm')
    d.ellipse([30, 228, 46, 244], outline=G2, width=2)
    POS['search'] = [300, 238]
    y = 300
    if search is None:
        for i, n in enumerate(['Toutes', 'Non lues', 'Favoris', 'Groupes']):
            x = 24+i*130; w = d.textlength(n, font=FI(20, 'SemiBold'))+36
            d.rounded_rectangle([x, 282, x+w, 324], 21, fill=DGRN if i == 0 else (30, 30, 32)); d.text((x+w/2, 303), n, font=FI(20, 'SemiBold'), fill=(210, 250, 210) if i == 0 else G2, anchor='mm')
        y = 370
        if folder:
            lock_ic(d, 52, y); d.text((104, y+4), 'Discussions verrouillées', font=FI(23, 'SemiBold'), fill=G2, anchor='lm'); POS['folder'] = [280, y+4]; y += 56
            d.line([(104, y-24), (SW, y-24)], fill=SEP)
        box_ic(d, 52, y); d.text((104, y+2), 'Archivées', font=FI(23, 'SemiBold'), fill=G2, anchor='lm'); d.text((SW-28, y+2), '2', font=FI(19), fill=G2, anchor='rm'); y += 74
        for k, (n, m, t, c) in enumerate(CHATS):
            if n == 'Sarah' and folder is not False: continue  # Sarah est déjà verrouillée
            chat_row(d, y+16, n, m, t, c); POS['row_'+n] = [300, y+16]; y += 98
        tabbar(d)
    else:
        if found:
            d.text((24, 300), 'Discussions verrouillées', font=FI(20, 'SemiBold'), fill=G2, anchor='lm')
            d.rounded_rectangle([18, 324, SW-18, 400], 18, outline=WGRN, width=3)
            lock_ic(d, 56, 362, W); d.text((100, 364), 'Discussions verrouillées', font=FI(24, 'SemiBold'), fill=W, anchor='lm'); POS['found'] = [300, 362]
        else:
            d.text((24, 300), 'Recherches récentes', font=FI(20, 'SemiBold'), fill=G2, anchor='lm')
            d.text((SW/2, 520), 'Aucun résultat', font=FI(24), fill=G2, anchor='mm')
        kb_letters(d, search)
    homebar(d); return im

def w_menu():
    im = w_list(folder=False); ov = Image.new('RGBA', (SW, SH), (0, 0, 0, 150)); im = Image.alpha_composite(im.convert('RGBA'), ov); d = ImageDraw.Draw(im)
    # aperçu de la conversation
    d.rounded_rectangle([20, 110, 380, 560], 30, fill=(22, 26, 24)); d.text((200, 140), 'Sarah', font=FI(22, 'SemiBold'), fill=W, anchor='mm')
    for k, (t, me) in enumerate([('Tu es dispo samedi ?', False), ('Oui pourquoi ?', True), ('Tu as vu la surprise ?', False)]):
        f = FI(19); w = d.textlength(t, font=f)+30; yy = 200+k*80
        if me: d.rounded_rectangle([360-w, yy, 360, yy+52], 18, fill=(0, 92, 75)); d.text((345, yy+26), t, font=f, fill=W, anchor='rm')
        else: d.rounded_rectangle([40, yy, 40+w, yy+52], 18, fill=(40, 40, 44)); d.text((55, yy+26), t, font=f, fill=W, anchor='lm')
    items = ['Marquer comme non lu', 'Archiver', 'Mode silencieux', 'Verrouiller la discussion', 'Ajouter aux favoris', 'Effacer la discussion']
    x0, y0, w, rh = 24, 590, 400, 72
    d.rounded_rectangle([x0, y0, x0+w, y0+len(items)*rh+24], 34, fill=(34, 34, 36))
    for i, n in enumerate(items):
        cy = y0+12+rh*i+rh/2
        if 'Verrouiller' in n: lock_ic(d, x0+40, cy-2, W); POS['m_lock'] = [x0+w/2, round(cy)]
        else: d.ellipse([x0+28, cy-12, x0+52, cy+12], outline=W, width=3)
        d.text((x0+76, cy), n, font=FI(24), fill=W, anchor='lm')
    return im.convert('RGB')

def nav(d, title, right=None):
    d.ellipse([20, 84, 76, 140], fill=(36, 36, 38)); d.line([(54, 98), (40, 112), (54, 126)], fill=W, width=4)
    d.text((92, 112), title, font=FI(25, 'SemiBold'), fill=W, anchor='lm')
    if right:
        w = d.textlength(right, font=FI(23))+40; d.rounded_rectangle([SW-20-w, 84, SW-20, 140], 28, fill=(36, 36, 38)); d.text((SW-20-w/2, 112), right, font=FI(23), fill=W, anchor='mm')
        POS['params_btn'] = [round(SW-20-w/2), 112]
def w_locked():
    im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im); status(d); nav(d, 'Discussions verrouill…', 'Paramètres')
    chat_row(d, 210, 'Sarah', 'Tu as vu la surprise ?', '15:30', (200, 110, 200)); homebar(d); return im
def toggle(d, x, y, on):
    d.rounded_rectangle([x, y-17, x+62, y+17], 17, fill=WGRN if on else (60, 60, 64)); cx = x+45 if on else x+17; d.ellipse([cx-14, y-14, cx+14, y+14], fill=W)
def w_params(on=False):
    im = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(im); status(d); nav(d, 'Paramètres de verrouillage')
    d.rounded_rectangle([18, 180, SW-18, 250], 20, fill=CARD); d.text((40, 215), 'Masquer les disc. verrouillées', font=FI(23), fill=W, anchor='lm'); toggle(d, 500, 215, on)
    POS['toggle'] = [531, 215]
    for k, t in enumerate(['Les discussions verrouillées n’apparaissent pas dans', 'votre liste. Pour les voir, saisissez votre code', 'secret dans la barre de recherche.']):
        d.text((36, 274+k*26), t, font=FI(17), fill=G2, anchor='lm')
    d.rounded_rectangle([18, 370, SW-18, 440], 20, fill=CARD); d.text((40, 405), 'Code secret', font=FI(23), fill=W, anchor='lm'); d.text((SW-60, 405), 'Oui' if on else 'Non', font=FI(21), fill=G2, anchor='rm'); d.text((SW-36, 405), '›', font=FI(28), fill=G2, anchor='mm')
    homebar(d); return im
def w_sheet():
    im = Image.new('RGB', (SW, SH), (22, 22, 24)); d = ImageDraw.Draw(im); status(d)
    d.ellipse([20, 84, 76, 140], fill=(40, 40, 44)); d.line([(36, 100), (60, 124)], fill=W, width=4); d.line([(60, 100), (36, 124)], fill=W, width=4)
    d.text((92, 112), 'Masquer les disc. verrouillées', font=FI(23, 'SemiBold'), fill=W, anchor='lm')
    d.ellipse([170, 210, 430, 400], fill=(130, 165, 185)); d.rounded_rectangle([245, 180, 355, 420], 18, fill=(225, 235, 245), outline=(70, 90, 110), width=4)
    for k in range(5): d.rounded_rectangle([262, 220+k*36, 338, 236+k*36], 6, fill=(110, 150, 200))
    for k, t in enumerate(['Masquez vos discussions à l’aide', 'd’un code secret pour plus', 'de confidentialité']):
        d.text((SW/2, 480+k*40), t, font=FI(29, 'Bold'), fill=W, anchor='mm')
    for k, t in enumerate(['Retrouvez les discussions verrouillées en saisissant', 'votre code dans la barre de recherche. Les discussions', 'seront effacées si vous oubliez votre code.']):
        d.text((SW/2, 620+k*30), t, font=FI(18), fill=(200, 200, 205), anchor='mm')
    d.rounded_rectangle([24, 1170, SW-24, 1236], 33, fill=(95, 225, 120)); d.text((SW/2, 1203), 'Créer un code secret', font=FI(24, 'SemiBold'), fill=(0, 0, 0), anchor='mm')
    POS['create'] = [300, 1203]; homebar(d); return im

KY0 = 860
def kb_letters(d, typed=''):
    d.rectangle([0, KY0, SW, SH], fill=KB_BG)
    kw, gap, kh = 52, 6, 76
    for r, row in enumerate(['azertyuiop', 'qsdfghjklm', 'wxcvbn\'']):
        n = len(row); y = KY0+20+r*(kh+14); x0 = (SW-(n*kw+(n-1)*gap))/2
        for i, ch in enumerate(row):
            x = x0+i*(kw+gap); d.rounded_rectangle([x, y, x+kw, y+kh], 10, fill=KEY); d.text((x+kw/2, y+kh/2), ch, font=FI(30), fill=W, anchor='mm')
        if r == 2:
            d.rounded_rectangle([12, y, 82, y+kh], 10, fill=KEY2); d.rounded_rectangle([SW-82, y, SW-12, y+kh], 10, fill=KEY2); d.text((SW-47, y+kh/2), '⌫', font=FI(28), fill=W, anchor='mm')
    y = KY0+20+3*(kh+14)
    d.rounded_rectangle([12, y, 130, y+kh], 10, fill=KEY2); d.text((71, y+kh/2), '123', font=FI(24), fill=W, anchor='mm')
    d.rounded_rectangle([140, y, 440, y+kh], 10, fill=KEY); d.rounded_rectangle([450, y, SW-12, y+kh], 10, fill=(10, 132, 255)); d.text((519, y+kh/2), 'OK', font=FI(22), fill=W, anchor='mm')
def w_code(typed):
    im = Image.new('RGB', (SW, SH), (22, 22, 24)); d = ImageDraw.Draw(im); status(d)
    d.ellipse([20, 84, 76, 140], fill=(40, 40, 44)); d.line([(54, 98), (40, 112), (54, 126)], fill=W, width=4)
    d.text((SW/2, 112), 'Créer un code secret', font=FI(23, 'SemiBold'), fill=W, anchor='mm')
    d.rounded_rectangle([470, 88, SW-20, 136], 24, fill=(95, 225, 120) if typed else (50, 70, 55)); d.text((515, 112), 'Suivant', font=FI(19, 'SemiBold'), fill=(0, 0, 0), anchor='mm')
    for k, t in enumerate(['Un code secret vous permet de retrouver vos', 'discussions verrouillées dans la barre de recherche.']):
        d.text((SW/2, 190+k*28), t, font=FI(18), fill=G2, anchor='mm')
    d.text((30, 280), 'CODE SECRET', font=FI(17, 'SemiBold'), fill=G2, anchor='lm')
    d.rounded_rectangle([18, 300, SW-18, 370], 20, fill=CARD, outline=WGRN if typed else CARD, width=2)
    d.text((40, 335), typed or 'Code secret', font=FI(26), fill=W if typed else G3, anchor='lm')
    if typed: d.line([(42+d.textlength(typed, font=FI(26)), 318), (42+d.textlength(typed, font=FI(26)), 352)], fill=WGRN, width=3)
    POS['code_field'] = [300, 335]
    kb_letters(d); homebar(d); return im

CODE = 'soleil'
S = {'w_list': lambda: w_list(True), 'w_list0': lambda: w_list(False), 'w_menu': w_menu, 'w_locked': w_locked, 'w_params': lambda: w_params(False), 'w_params_on': lambda: w_params(True),
     'w_sheet': w_sheet, 'w_code': lambda: w_code(CODE), 'w_hidden': lambda: w_list(None), 'w_search0': lambda: w_list(None, search=' ', found=False), 'w_search': lambda: w_list(None, search=CODE, found=True)}
for n, f in S.items(): f().save(OUT+n+'.png')
# pour l'écran « dossier masqué », folder=None : pas de dossier, Sarah absente
json.dump(POS, open('src/data.json', 'w'), indent=0)
print(POS)

# ---- durée + sons
POS['duree'] = 63.17
json.dump(POS, open('src/data.json', 'w'), indent=0)
T = 63.4; SR = 44100; au = np.zeros(int((T+0.5)*SR), np.float32)
def add(t, x):
    i = int(t*SR); x = x[:len(au)-i]; au[i:i+len(x)] += x
def tone(f0, f1, dd, v, dec=6):
    n = int(dd*SR); k = np.linspace(0, 1, n); ph = 2*np.pi*np.cumsum(f0+(f1-f0)*k)/SR
    return (np.sin(ph)*np.exp(-k*dec)*v).astype(np.float32)
def soft():
    n = int(0.42*SR); k = np.arange(n)/SR; env = np.minimum(1, k/0.012)*np.exp(-k*11)
    return ((np.sin(2*np.pi*587.33*k)*0.6+np.sin(2*np.pi*880*k)*0.28+np.sin(2*np.pi*1174.66*k)*0.08)*env*0.30).astype(np.float32)
SS = {'soft': soft(), 'pop': tone(520, 900, 0.09, 0.2), 'tick': tone(1400, 1100, 0.06, 0.18), 'ding': tone(1320, 1320, 0.5, 0.2)+tone(1980, 1980, 0.5, 0.09),
      'err': tone(300, 220, 0.25, 0.22, 4), 'shrink': tone(900, 300, 0.4, 0.13, 2)}
SC = [8.6, 23.8, 26.2, 29.2, 37.0, 44.9, 51.4, 56.9]
ev = [(s, 'soft') for s in SC]
ev += [(0.3, 'pop'), (2.06, 'pop'), (6.6, 'pop'), (9.64, 'tick'), (11.0, 'pop'), (12.92, 'tick'), (13.6, 'pop'), (15.4, 'tick'), (17.0, 'pop'), (18.76, 'tick'), (19.9, 'pop'),
       (21.26, 'tick'), (22.0, 'pop'), (24.2, 'shrink'), (25.02, 'pop'), (31.4, 'err'), (33.4, 'pop'), (35.6, 'ding'), (41.5, 'err'), (43.2, 'pop'), (47.4, 'ding'), (50.4, 'tick'), (53.6, 'pop'), (60.0, 'ding')]
ev += [(27.3+i*0.12, 'tick') for i in range(6)]
for a, k in ev: add(a, SS[k]*0.35/0.3)
au = np.clip(au, -1, 1); w = wave.open(OUT+'sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((au*32767).astype(np.int16).tobytes()); w.close()
print('sons ok')
