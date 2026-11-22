# data.json + sfx pour la vidéo « Sons en arrière-plan » (22/11/2026). Lancer depuis kit/.
import json, wave, numpy as np
POS = json.load(open('scripts/sa_pos.json')); POS['duree'] = 76.3
json.dump(POS, open('src/data.json', 'w'), indent=0)
T = 76.6; SR = 44100; au = np.zeros(int(T*SR), np.float32)
def add(t, x):
    i = int(t*SR); x = x[:len(au)-i]; au[i:i+len(x)] += x
def tone(f0, f1, dd, v, dec=6):
    n = int(dd*SR); k = np.linspace(0, 1, n); ph = 2*np.pi*np.cumsum(f0+(f1-f0)*k)/SR
    return (np.sin(ph)*np.exp(-k*dec)*v).astype(np.float32)
def soft():
    n = int(0.42*SR); k = np.arange(n)/SR; env = np.minimum(1, k/0.012)*np.exp(-k*11)
    return ((np.sin(2*np.pi*587.33*k)*0.6+np.sin(2*np.pi*880*k)*0.28+np.sin(2*np.pi*1174.66*k)*0.08)*env*0.30).astype(np.float32)
S = {'soft': soft(), 'pop': tone(520, 900, 0.09, 0.2), 'tick': tone(1400, 1100, 0.06, 0.18), 'ding': tone(1320, 1320, 0.5, 0.2)+tone(1980, 1980, 0.5, 0.09), 'err': tone(300, 220, 0.25, 0.22, 4)}
SC = [2.0, 9.3, 15.0, 37.5, 50.2, 59.1, 65.0, 70.3, 72.9]
ev = [(s, 'soft') for s in SC]
ev += [(4.68, 'pop'), (5.26, 'pop'), (5.78, 'pop'), (7.66, 'pop'), (8.22, 'pop'), (8.88, 'pop'), (12.42, 'ding'), (17.0, 'tick'), (19.0, 'tick'), (22.0, 'tick'),
       (25.84, 'tick'), (26.46, 'tick'), (27.2, 'tick'), (28.06, 'tick'), (29.84, 'tick'), (32.4, 'tick'), (34.9, 'tick'), (37.6, 'ding'), (39.7, 'pop'), (43.9, 'pop'),
       (46.5, 'pop'), (47.1, 'pop'), (47.8, 'pop'), (48.6, 'ding'), (51.3, 'err'), (56.4, 'err'), (57.9, 'tick'), (60.8, 'tick'), (62.2, 'pop'), (66.3, 'pop'), (68.6, 'pop'), (69.4, 'pop')]
for a, k in ev: add(a, S[k]*0.35/0.3)
au = np.clip(au, -1, 1); w = wave.open('public/sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((au*32767).astype(np.int16).tobytes()); w.close()
print(POS)
