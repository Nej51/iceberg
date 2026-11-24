# Coupe les temps morts d'une voix off (silences trop longs) pour une vidéo plus nerveuse.
# Usage : python3 scripts/tighten.py <voix_entree> <voix_sortie.wav> [--max 0.30] [--garde 0.14] [--fin 1.2]
#   --max   : un silence plus long que ça (secondes) est raccourci
#   --garde : durée gardée pour ce silence (une petite respiration)
#   --fin   : silence ajouté à la fin (pour l'écran de fin)
# Affiche la durée avant/après. Relancer ensuite scripts/mots.py sur la voix coupée pour les temps des mots.
import sys, subprocess, wave, argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--max', type=float, default=0.30)
ap.add_argument('--garde', type=float, default=0.14)
ap.add_argument('--fin', type=float, default=1.2)
ap.add_argument('--seuil', type=float, default=-40.0, help='niveau (dB) sous lequel on considère que c\'est un silence')
a = ap.parse_args()

SR = 44100
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.src, '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.float32).copy()
win = int(0.02 * SR)  # fenêtres de 20 ms
n = len(x) // win
rms = np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1) + 1e-12)
db = 20 * np.log10(rms + 1e-9)
quiet = db < a.seuil

# repérer les plages de silence
plages, i = [], 0
while i < n:
    if quiet[i]:
        j = i
        while j < n and quiet[j]: j += 1
        plages.append((i * win, j * win)); i = j
    else: i += 1

parts, prev, coupe = [], 0, 0.0
for s, e in plages:
    d = (e - s) / SR
    if s == 0 or e >= len(x) - win:  # silence au tout début / à la fin : on le retire presque entièrement
        keep = int(0.05 * SR)
    elif d > a.max:
        keep = int(a.garde * SR)
    else:
        continue
    keep = min(keep, e - s)
    mid = s + keep // 2
    parts.append(x[prev:mid]); prev = e - (keep - keep // 2)
    coupe += d - keep / SR
parts.append(x[prev:])
y = np.concatenate(parts)
# petits fondus pour éviter les clics aux coupures
y = np.concatenate([y, np.zeros(int(a.fin * SR), np.float32)])
w = wave.open(a.out, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
print(f"avant {len(x)/SR:.2f} s -> après {len(y)/SR:.2f} s (temps morts retirés : {coupe:.2f} s)")
