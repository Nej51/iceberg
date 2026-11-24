# Sous-titres mot à mot : transcrit la voix, découpe en petits blocs lisibles et VÉRIFIE qu'ils tiennent à l'écran.
# Usage : python3 scripts/sous_titres.py public/voice.wav [fr|en] [--taille 64] [--mots 3] [--depuis 0]
# Écrit src/sous_titres.json (lu par le composant <Caption> de lib.tsx).
# Vérifications : largeur de chaque bloc (Poppins Bold mesurée), mots trop rapides, blocs vides.
import sys, json, argparse, subprocess
import numpy as np
from PIL import ImageFont

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('lang', nargs='?', default='fr')
ap.add_argument('--taille', type=int, default=64)
ap.add_argument('--mots', type=int, default=3, help='mots max par bloc')
ap.add_argument('--largeur', type=int, default=860, help='largeur max d\'un bloc (px), zone sûre x 110 -> 970')
ap.add_argument('--depuis', type=float, default=0, help='pas de sous-titres avant cette seconde (ex. pendant le titre de couverture)')
ap.add_argument('--out', default='src/sous_titres.json')
a = ap.parse_args()

from faster_whisper import WhisperModel
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.src, '-ar', '16000', '-ac', '1', '-f', 'f32le', '-'], capture_output=True).stdout
audio = np.frombuffer(raw, np.float32)
m = WhisperModel('small', device='cpu', compute_type='int8')
segs, _ = m.transcribe(audio, language=a.lang, word_timestamps=True)
mots = []
for w in (w for s in segs for w in s.words if w.word.strip()):
    txt = w.word.strip()
    # Whisper coupe les élisions (« n » + « 'aurait ») : on recolle avec une vraie apostrophe
    if mots and (txt[0] in "'’" or mots[-1][2][-1] in "'’"):
        s0, _, prevw = mots.pop(); mots.append((s0, w.end, prevw.rstrip("'’") + '’' + txt.lstrip("'’"))); continue
    mots.append((w.start, w.end, txt.replace("'", '’')))

font = ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf', a.taille)
PAD = 2 * 18 + 10  # marge de la pastille du mot actif
def largeur(ws): return sum(font.getlength(w) for w in ws) + font.getlength(' ') * (len(ws) - 1) + PAD

blocs, cur = [], []
for i, (s, e, w) in enumerate(mots):
    if s < a.depuis: continue
    trop_large = cur and largeur([x[2] for x in cur] + [w]) > a.largeur
    pause = cur and s - cur[-1][1] > 0.35
    if cur and (len(cur) >= a.mots or trop_large or pause):
        blocs.append(cur); cur = []
    cur.append((s, e, w))
    if w[-1] in '.?!:,;' and len(cur) >= 1:
        blocs.append(cur); cur = []
if cur: blocs.append(cur)

out, alertes = [], []
for k, b in enumerate(blocs):
    t1 = blocs[k + 1][0][0] if k + 1 < len(blocs) else b[-1][1] + 0.4
    t1 = min(t1, b[-1][1] + 0.6)
    L = largeur([x[2] for x in b])
    if L > a.largeur: alertes.append(f"bloc trop large ({L:.0f} px) : {' '.join(x[2] for x in b)}")
    for s, e, w in b:
        if e - s < 0.05: alertes.append(f"mot très rapide ({e-s:.2f} s) : {w}")
    out.append({'t0': round(b[0][0], 2), 't1': round(t1, 2), 'mots': [[round(s, 2), w] for s, e, w in b]})

json.dump({'taille': a.taille, 'blocs': out}, open(a.out, 'w'), ensure_ascii=False)
print(f"{len(mots)} mots -> {len(out)} blocs -> {a.out}")
print('OK : tout tient à l\'écran' if not alertes else 'À VÉRIFIER :\n- ' + '\n- '.join(alertes))
