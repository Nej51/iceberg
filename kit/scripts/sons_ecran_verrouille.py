# data.json + sfx pour la vidéo « Relooke ton écran verrouillé » (23/11/2026). Lancer depuis kit/.
import json, wave, numpy as np
POS = json.load(open('scripts/ev_pos.json')); POS['duree'] = 65.3
json.dump(POS, open('src/data.json', 'w'), indent=0)
T = 65.6; SR = 44100; au = np.zeros(int(T*SR), np.float32)
def add(t, x):
    i = int(t*SR); x = x[:len(au)-i]; au[i:i+len(x)] += x
def tone(f0, f1, dd, v, dec=6):
    n = int(dd*SR); k = np.linspace(0, 1, n); ph = 2*np.pi*np.cumsum(f0+(f1-f0)*k)/SR
    return (np.sin(ph)*np.exp(-k*dec)*v).astype(np.float32)
def soft():
    n = int(0.42*SR); k = np.arange(n)/SR; env = np.minimum(1, k/0.012)*np.exp(-k*11)
    return ((np.sin(2*np.pi*587.33*k)*0.6+np.sin(2*np.pi*880*k)*0.28+np.sin(2*np.pi*1174.66*k)*0.08)*env*0.30).astype(np.float32)
S = {'soft': soft(), 'pop': tone(520, 900, 0.09, 0.2), 'tick': tone(1400, 1100, 0.06, 0.18), 'ding': tone(1320, 1320, 0.5, 0.2)+tone(1980, 1980, 0.5, 0.09), 'err': tone(300, 220, 0.25, 0.22, 4)}
SC = [2.0, 6.1, 19.36, 30.74, 40.08, 47.2, 55.4, 59.32, 61.58]
ev = [(s, 'soft') for s in SC]
ev += [(2.86, 'ding'), (4.3, 'pop'), (10.8, 'tick'), (12.2, 'tick'), (14.5, 'tick'), (15.64, 'pop'), (23.1, 'tick'), (24.4, 'pop'), (28.82, 'err'), (30.0, 'tick'),
       (35.4, 'tick'), (36.0, 'ding'), (38.1, 'pop'), (38.6, 'pop'), (39.2, 'pop'), (41.0, 'tick'), (41.98, 'tick'), (46.2, 'ding'), (47.4, 'err'), (50.9, 'pop'), (52.6, 'pop'), (58.1, 'pop')]
for i, c in enumerate('un coucher de soleil sur la mer'):
    if c != ' ': ev.append((44.6 + i * 0.035, 'tick'))
for a, k in ev: add(a, S[k]*0.35/0.3)
au = np.clip(au, -1, 1); w = wave.open('public/sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((au*32767).astype(np.int16).tobytes()); w.close()
print(POS)
