# Écrans « Relooke ton écran verrouillé » (iOS 27 : heure en petit, cacher le lecteur, Étendre, Image Playground), 23/11/2026.
# Redessinés d'après la vidéo source (aucune image reprise). Lancer depuis kit/.
import sys, json, math, random
import numpy as np
sys.path.insert(0, 'scripts')
from ui_iphone import FI, SW, SH
from PIL import Image, ImageDraw, ImageFilter
OUT = 'public/'
W = (255, 255, 255); BLU = (10, 132, 255)
POS = {}
random.seed(4)

def vgrad(w, h, stops):
    ys = np.linspace(0, 1, h)[:, None]; out = np.zeros((h, 1, 3))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        m = (ys >= a) & (ys <= b); k = np.clip((ys - a) / max(1e-6, b - a), 0, 1)
        col = np.array(ca, float) * (1 - k) + np.array(cb, float) * k
        out = np.where(m[:, :, None], col[:, None, :], out)
    return Image.fromarray(np.broadcast_to(out, (h, w, 3)).astype(np.uint8), 'RGB')

def ridge(w, base, amp, seed, rough=6):
    rnd = random.Random(seed); pts = []; n = 40
    ph = [rnd.random() * 6 for _ in range(rough)]
    for i in range(n + 1):
        x = i / n; y = base
        for k in range(rough): y += amp / (k + 1) * math.sin(x * (k + 1.3) * 3.1 + ph[k])
        pts.append((x * w, y))
    return pts

def scene_mountains(w=600, h=1300):
    """Fond A : montagnes au crépuscule + lac (dessiné en code)."""
    im = vgrad(w, h, [(0, (18, 22, 70)), (0.32, (70, 60, 150)), (0.5, (236, 130, 150)), (0.58, (255, 190, 140)), (0.62, (90, 70, 140)), (1, (20, 20, 60))])
    d = ImageDraw.Draw(im, 'RGBA')
    gl = Image.new('RGBA', (w, h), (0, 0, 0, 0)); g = ImageDraw.Draw(gl); g.ellipse([w * .55 - 140, h * .52 - 140, w * .55 + 140, h * .52 + 140], fill=(255, 220, 170, 170))
    im.paste(gl.filter(ImageFilter.GaussianBlur(60)), (0, 0), gl.filter(ImageFilter.GaussianBlur(60)))
    d.ellipse([w * .55 - 34, h * .55 - 34, w * .55 + 34, h * .55 + 34], fill=(255, 236, 200, 255))
    for i in range(60):
        x, y = random.random() * w, random.random() * h * .3; r = random.random() * 1.6 + .4; d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, int(120 + 120 * random.random())))
    for base, amp, col, sd in [(h * .5, 60, (120, 80, 160), 1), (h * .55, 50, (80, 55, 130), 2), (h * .6, 34, (45, 35, 90), 3)]:
        pts = ridge(w, base, amp, sd); d.polygon(pts + [(w, h * .62), (0, h * .62)], fill=col)
    # lac (reflet)
    lake = im.crop((0, int(h * .38), w, int(h * .62))).transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(3))
    lake = Image.blend(lake, Image.new('RGB', lake.size, (30, 30, 80)), 0.45)
    im.paste(lake, (0, int(h * .62)))
    for i in range(30):
        y = h * .63 + random.random() * h * .2; x = w * .55 + (random.random() - .5) * 160 * (1 + (y - h * .62) / 200)
        d.rounded_rectangle([x - 30, y, x + 30, y + 3], 2, fill=(255, 220, 180, 110))
    d.rectangle([0, h * .86, w, h], fill=(20, 18, 50, 200))
    return im

def scene_sea(w=600, h=1300):
    """Fond B (« créé par Image Playground ») : coucher de soleil sur la mer, style illustration."""
    im = vgrad(w, h, [(0, (40, 30, 110)), (0.3, (190, 80, 160)), (0.5, (255, 150, 110)), (0.56, (255, 210, 140)), (0.58, (60, 60, 150)), (1, (15, 20, 70))])
    d = ImageDraw.Draw(im, 'RGBA')
    gl = Image.new('RGBA', (w, h), (0, 0, 0, 0)); g = ImageDraw.Draw(gl); g.ellipse([w / 2 - 200, h * .54 - 200, w / 2 + 200, h * .54 + 200], fill=(255, 200, 120, 160))
    gb = gl.filter(ImageFilter.GaussianBlur(70)); im.paste(gb, (0, 0), gb)
    d.pieslice([w / 2 - 90, h * .58 - 90, w / 2 + 90, h * .58 + 90], 180, 360, fill=(255, 236, 170, 255))
    for cy, cx, cw in [(.22, .25, 200), (.3, .75, 240), (.4, .3, 180), (.12, .7, 160)]:
        for j in range(4): d.ellipse([w * cx - cw / 2 + j * cw / 5, h * cy - 18 - j % 2 * 10, w * cx - cw / 2 + j * cw / 5 + cw / 2.2, h * cy + 18], fill=(255, 170, 170, 70))
    for i in range(70):
        y = h * .59 + (i / 70) ** 1.6 * h * .4; ww = 20 + (y - h * .58) * .9 * random.random()
        x = w / 2 + (random.random() - .5) * (60 + (y - h * .58) * 0.9)
        d.rounded_rectangle([x - ww / 2, y, x + ww / 2, y + 3 + (y - h * .58) / 120], 2, fill=(255, 210, 150, 140))
    return im

def island(d): d.rounded_rectangle([SW / 2 - 64, 20, SW / 2 + 64, 62], 21, fill=(0, 0, 0))
def status(d):
    d.text((60, 42), 'Orange F', font=FI(20, 'SemiBold'), fill=W, anchor='lm')
    for i in range(4): d.rounded_rectangle([452 + i * 9, 48 - i * 4, 458 + i * 9, 54], 2, fill=W)
    d.rounded_rectangle([500, 34, 540, 54], 6, outline=W, width=2); d.rounded_rectangle([503, 37, 530, 51], 3, fill=W)

DATE = 'lundi 23 novembre'
def clock_big(d, y=300, col=W):
    d.text((SW / 2, 150), DATE, font=FI(28, 'SemiBold'), fill=col, anchor='mm')
    d.text((SW / 2, y), '9:41', font=FI(220, 'Bold'), fill=col, anchor='mm')
def clock_small(d, col=W):
    d.text((SW / 2, 150), 'lun. 23 nov.   9:41', font=FI(30, 'SemiBold'), fill=col, anchor='mm')
def bottom(d):
    for x in (100, 500):
        d.ellipse([x - 40, 1160 - 40, x + 40, 1160 + 40], fill=(255, 255, 255, 50))
    # lampe + appareil photo
    d.rounded_rectangle([92, 1140, 108, 1178], 6, outline=W, width=3)
    d.rounded_rectangle([484, 1148, 516, 1174], 6, outline=W, width=3); d.ellipse([494, 1153, 506, 1167], outline=W, width=2)
    d.rounded_rectangle([SW / 2 - 70, 1270, SW / 2 + 70, 1279], 5, fill=W)

def player(im, dx=0, clear=False):
    """Grand lecteur « À l'écoute » (titre inventé, pochette dessinée)."""
    lay = Image.new('RGBA', (SW, SH), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = 30 + dx, 830, 570 + dx, 1080
    if clear:
        d.rounded_rectangle([x1 + 14, y0, x1 + 154, y1], 40, fill=(120, 120, 130, 200))
        d.text((x1 + 84, (y0 + y1) / 2), 'Effacer', font=FI(24, 'SemiBold'), fill=W, anchor='mm')
    blur = im.crop((max(0, x0), y0, min(SW, x1), y1)).filter(ImageFilter.GaussianBlur(24))
    card = Image.new('RGBA', (x1 - x0, y1 - y0), (0, 0, 0, 0)); card.paste(blur, (max(0, -x0), 0))
    tint = Image.new('RGBA', card.size, (255, 255, 255, 46)); card = Image.alpha_composite(card, tint)
    m = Image.new('L', card.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, card.size[0] - 1, card.size[1] - 1], 40, fill=255)
    lay.paste(card, (x0, y0), m)
    d.rounded_rectangle([x0, y0, x1, y1], 40, outline=(255, 255, 255, 90), width=2)
    cov = scene_sea(90, 90).resize((90, 90)); cm = Image.new('L', (90, 90), 0); ImageDraw.Draw(cm).rounded_rectangle([0, 0, 89, 89], 14, fill=255)
    lay.paste(cov, (x0 + 26, y0 + 24), cm)
    d.text((x0 + 134, y0 + 52), 'Nuit d’été', font=FI(26, 'SemiBold'), fill=W, anchor='lm')
    d.text((x0 + 134, y0 + 86), 'Les Vagues', font=FI(22), fill=(235, 235, 245), anchor='lm')
    d.rounded_rectangle([x0 + 30, y0 + 140, x1 - 30, y0 + 146], 3, fill=(255, 255, 255, 90)); d.rounded_rectangle([x0 + 30, y0 + 140, x0 + 200, y0 + 146], 3, fill=W)
    cy = y0 + 200; cx = (x0 + x1) / 2
    for s in (-1, 1):
        for k in (0, 1):
            bx = cx + s * 120 + s * k * 22
            d.polygon([(bx - s * 14, cy - 14), (bx - s * 14, cy + 14), (bx + s * 10, cy)], fill=W)
    d.rounded_rectangle([cx - 16, cy - 18, cx - 6, cy + 18], 3, fill=W); d.rounded_rectangle([cx + 6, cy - 18, cx + 16, cy + 18], 3, fill=W)
    im.paste(lay, (0, 0), lay)

def lock(wall, small=False, music=False, dx=0, clear=False, dim_clock=False):
    im = wall.copy(); d = ImageDraw.Draw(im, 'RGBA'); island(d); status(d)
    if small: clock_small(d)
    else: clock_big(d)
    if music: player(im, dx, clear); d = ImageDraw.Draw(im, 'RGBA')
    bottom(d)
    return im

def gallery(wall):
    """Appui long : galerie d'écrans verrouillés (aperçu + Personnaliser + bouton +)."""
    im = Image.new('RGB', (SW, SH), (10, 10, 14)); d = ImageDraw.Draw(im, 'RGBA'); island(d)
    pv = lock(wall).resize((380, 823)); m = Image.new('L', pv.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 379, 822], 50, fill=255)
    for sx in (-330, 330):
        side = wall.resize((380, 823)).point(lambda v: v * 0.45); im.paste(side, (110 + sx, 200), m)
    im.paste(pv, (110, 200), m)
    d.rounded_rectangle([150, 1080, 450, 1150], 35, fill=(70, 70, 78)); d.text((300, 1115), 'Personnaliser', font=FI(28, 'SemiBold'), fill=W, anchor='mm'); POS['perso'] = [300, 1115]
    d.ellipse([480, 1083, 544, 1147], fill=(70, 70, 78)); d.line([(512, 1099), (512, 1131)], fill=W, width=4); d.line([(496, 1115), (528, 1115)], fill=W, width=4); POS['plus'] = [512, 1115]
    for i in range(5): d.ellipse([256 + i * 20 - 4, 1048, 256 + i * 20 + 4, 1056], fill=W if i == 2 else (120, 120, 126))
    return im

def topbar(d, ok=True):
    d.rounded_rectangle([30, 84, 156, 132], 24, fill=(60, 60, 66, 200)); d.text((93, 108), 'Annuler', font=FI(22, 'SemiBold'), fill=W, anchor='mm')
    if ok: d.rounded_rectangle([474, 84, 570, 132], 24, fill=(10, 132, 255)); d.text((522, 108), 'OK', font=FI(22, 'SemiBold'), fill=W, anchor='mm')

def editor(wall, small=False, panel=False, sel=False):
    """Mode Personnaliser : zones cadrées (date, heure, widgets)."""
    im = wall.copy(); d = ImageDraw.Draw(im, 'RGBA'); island(d); topbar(d)
    if small:
        d.rounded_rectangle([120, 126, 480, 176], 20, outline=(255, 255, 255, 220), width=3); clock_small(d)
    else:
        d.rounded_rectangle([110, 128, 490, 172], 18, outline=(255, 255, 255, 160), width=2)
        d.rounded_rectangle([80, 190, 520, 410], 30, outline=(255, 255, 255, 230 if sel else 160), width=4 if sel else 2)
        clock_big(d)
        d.rounded_rectangle([120, 430, 480, 490], 20, outline=(255, 255, 255, 120), width=2); d.text((300, 460), '+  Ajouter des widgets', font=FI(20, 'SemiBold'), fill=W, anchor='mm')
    POS['clock'] = [300, 300]
    if panel:
        d.rounded_rectangle([10, 780, 590, 1300], 46, fill=(30, 30, 34, 245))
        d.rounded_rectangle([270, 794, 330, 800], 3, fill=(90, 90, 96))
        d.text((44, 850), 'Police et couleur', font=FI(28, 'Bold'), fill=W, anchor='lm')
        # icône « heure en petit » en haut à droite (nouveauté iOS 27)
        d.ellipse([490, 822, 550, 882], fill=(10, 132, 255) if small else (70, 70, 78))
        d.rounded_rectangle([505, 838, 535, 866], 6, outline=W, width=3); d.text((520, 852), '9:41', font=FI(9, 'Bold'), fill=W, anchor='mm')
        POS['mini'] = [520, 852]
        for i, f in enumerate(['Regular', 'SemiBold', 'Bold', 'Regular', 'SemiBold', 'Bold']):
            x = 76 + (i % 6) * 90; y = 950
            d.rounded_rectangle([x - 38, y - 38, x + 38, y + 38], 16, fill=(60, 60, 66) if i else (90, 90, 100), outline=W if i == 2 else None, width=3)
            d.text((x, y), '12', font=FI(30, f), fill=W, anchor='mm')
        for i, c in enumerate([(255, 255, 255), (255, 200, 210), (170, 200, 255), (255, 220, 150), (190, 255, 210), (220, 190, 255)]):
            x = 76 + i * 90; d.ellipse([x - 30, 1060 - 30, x + 30, 1060 + 30], fill=c, outline=W if i == 0 else None, width=4)
        d.rounded_rectangle([50, 1140, 550, 1150], 5, fill=(80, 80, 86)); d.ellipse([300, 1130, 330, 1160], fill=W)
    return im

def extend_edit(wall, ext=False):
    """Éditeur de photo : photo dézoomée qui ne remplit pas l'écran + bouton Étendre."""
    im = Image.new('RGB', (SW, SH), (14, 14, 18)); d = ImageDraw.Draw(im, 'RGBA')
    if ext:
        im.paste(wall, (0, 0))
    else:
        band = wall.crop((0, 380, 600, 860)).resize((480, 384))
        im.paste(band, (60, 470))
        d.rounded_rectangle([60, 470, 540, 854], 2, outline=(255, 255, 255, 140), width=2)
        for y in (200, 1000):
            d.line([(60, y), (540, y)], fill=(255, 255, 255, 50), width=1)
    d = ImageDraw.Draw(im, 'RGBA'); island(d); topbar(d)
    clock_big(d)
    if not ext:
        d.rounded_rectangle([200, 1020, 400, 1084], 32, fill=(255, 255, 255, 230))
        d.text((300, 1052), 'Étendre', font=FI(28, 'SemiBold'), fill=(10, 10, 14), anchor='mm'); POS['etendre'] = [300, 1052]
        d.text((300, 1120), 'Remplir l’écran avec Apple Intelligence', font=FI(17), fill=(200, 200, 210), anchor='mm')
    else:
        d.rounded_rectangle([170, 1020, 430, 1084], 32, fill=(60, 60, 66, 200))
        d.text((300, 1052), '✓ Étendu', font=FI(26, 'SemiBold'), fill=W, anchor='mm')
    return im

def add_menu():
    """Feuille « Ajouter un fond d'écran » : rangée d'options, dont Image Playground."""
    im = Image.new('RGB', (SW, SH), (10, 10, 14)); d = ImageDraw.Draw(im, 'RGBA'); island(d)
    d.rounded_rectangle([0, 110, 600, 1300], 46, fill=(28, 28, 32))
    d.text((300, 170), 'Ajouter un fond d’écran', font=FI(26, 'Bold'), fill=W, anchor='mm')
    d.rounded_rectangle([30, 84 + 40, 150, 132 + 40], 0, fill=(0, 0, 0, 0))
    items = [('Photos', 'photos'), ('Personnes', 'pers'), ('Image\nPlayground', 'ip'), ('Emoji', 'emoji'), ('Météo', 'meteo')]
    for i, (lab, k) in enumerate(items):
        x = 66 + i * 117; y = 280
        d.ellipse([x - 44, y - 44, x + 44, y + 44], fill=(58, 58, 64))
        if k == 'photos':
            for a in range(8):
                ang = a * math.pi / 4; cx, cy = x + 16 * math.cos(ang), y + 16 * math.sin(ang)
                d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=[(255, 149, 0, 200), (255, 204, 0, 200), (52, 199, 89, 200), (48, 176, 199, 200), (0, 122, 255, 200), (88, 86, 214, 200), (175, 82, 222, 200), (255, 45, 85, 200)][a])
        elif k == 'pers':
            d.ellipse([x - 12, y - 24, x + 12, y]); d.ellipse([x - 12, y - 24, x + 12, y], fill=W); d.pieslice([x - 24, y + 2, x + 24, y + 44], 180, 360, fill=W)
        elif k == 'ip':
            for r, c in [(30, (90, 120, 255)), (20, (200, 110, 255)), (10, (255, 180, 120))]:
                d.ellipse([x - r, y - r, x + r, y + r], fill=c)
        elif k == 'emoji':
            d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=(255, 205, 60)); d.ellipse([x - 12, y - 10, x - 4, y - 2], fill=(60, 40, 0)); d.ellipse([x + 4, y - 10, x + 12, y - 2], fill=(60, 40, 0)); d.arc([x - 14, y - 6, x + 14, y + 16], 20, 160, fill=(60, 40, 0), width=4)
        else:
            d.ellipse([x - 22, y - 22, x + 4, y + 4], fill=(255, 205, 60)); d.ellipse([x - 16, y - 6, x + 26, y + 20], fill=W)
        for j, l in enumerate(lab.split('\n')): d.text((x, y + 66 + j * 24), l, font=FI(18, 'SemiBold'), fill=W, anchor='mm')
        POS['m_' + k] = [x, y]
    d.text((40, 440), 'Suggestions', font=FI(24, 'Bold'), fill=W, anchor='lm')
    for i, wl in enumerate([scene_mountains(170, 368), scene_sea(170, 368), scene_mountains(170, 368).transpose(Image.FLIP_LEFT_RIGHT)]):
        m = Image.new('L', wl.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 169, 367], 26, fill=255)
        im.paste(wl, (30 + i * 190, 480), m)
        ImageDraw.Draw(im).text((115 + i * 190, 560), '9:41', font=FI(54, 'Bold'), fill=W, anchor='mm')
    return im

def playground():
    """Écran Image Playground : champ « Décris un fond d'écran » + styles. Le texte est tapé en overlay dans Remotion."""
    im = vgrad(SW, SH, [(0, (30, 26, 70)), (0.5, (60, 40, 110)), (1, (20, 18, 50))]); d = ImageDraw.Draw(im, 'RGBA'); island(d)
    d.rounded_rectangle([30, 84, 156, 132], 24, fill=(60, 60, 66, 200)); d.text((93, 108), 'Annuler', font=FI(22, 'SemiBold'), fill=W, anchor='mm')
    for r, c in [(80, (90, 120, 255, 120)), (55, (200, 110, 255, 140)), (30, (255, 180, 120, 160))]:
        d.ellipse([300 - r, 330 - r, 300 + r, 330 + r], fill=c)
    d.text((300, 470), 'Image Playground', font=FI(32, 'Bold'), fill=W, anchor='mm')
    for i, s in enumerate(['Animation', 'Illustration', 'Croquis']):
        x = 110 + i * 190; d.rounded_rectangle([x - 80, 540, x + 80, 590], 25, fill=(255, 255, 255, 60 if i else 200))
        d.text((x, 565), s, font=FI(20, 'SemiBold'), fill=(20, 20, 30) if i == 0 else W, anchor='mm')
    d.rounded_rectangle([30, 660, 570, 740], 40, fill=(255, 255, 255, 40), outline=(255, 255, 255, 120), width=2)
    d.text((70, 700), 'Décris un fond d’écran…', font=FI(22), fill=(200, 200, 215), anchor='lm'); POS['champ'] = [300, 700]
    # clavier
    d.rectangle([0, 860, 600, 1300], fill=(40, 40, 48))
    rows = ['azertyuiop', 'qsdfghjklm', 'wxcvbn']
    for r, row in enumerate(rows):
        n = len(row); kw = 52; x0 = (600 - n * 57) / 2
        for i, ch in enumerate(row):
            x = x0 + i * 57; y = 890 + r * 90
            d.rounded_rectangle([x, y, x + kw, y + 70], 10, fill=(90, 90, 100)); d.text((x + kw / 2, y + 35), ch, font=FI(26), fill=W, anchor='mm')
    d.rounded_rectangle([150, 1160, 450, 1230], 10, fill=(90, 90, 100)); d.text((300, 1195), 'espace', font=FI(22), fill=W, anchor='mm')
    return im

A = scene_mountains(); B = scene_sea()
A.save(OUT + 'ev_wallA.png'); B.save(OUT + 'ev_wallB.png')
lock(A).save(OUT + 'ev_big.png')
lock(A, music=True).save(OUT + 'ev_big_music.png')
gallery(A).save(OUT + 'ev_gal.png')
editor(A).save(OUT + 'ev_edit.png')
editor(A, sel=True).save(OUT + 'ev_edit_sel.png')
editor(A, panel=True, sel=True).save(OUT + 'ev_panel.png')
editor(A, small=True, panel=True).save(OUT + 'ev_panel_small.png')
lock(A, small=True).save(OUT + 'ev_small.png')
lock(A, small=True, music=True).save(OUT + 'ev_music.png')
lock(A, small=True, music=True, dx=-150, clear=True).save(OUT + 'ev_music_swipe.png')
lock(A, small=True, music=True, dx=-420, clear=True).save(OUT + 'ev_music_gone.png')
extend_edit(A).save(OUT + 'ev_ext.png')
extend_edit(A, ext=True).save(OUT + 'ev_ext_done.png')
add_menu().save(OUT + 'ev_add.png')
playground().save(OUT + 'ev_ip.png')
lock(B, small=True).save(OUT + 'ev_ip_result.png')
json.dump(POS, open('scripts/ev_pos.json', 'w')); print(json.dumps(POS))
