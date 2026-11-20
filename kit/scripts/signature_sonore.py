# Signature sonore iCeberg v2 « premium » : nappe tech la nuit, STÉRÉO (fabriquée ici = aucun droit d'auteur).
# Usage : python3 scripts/signature_sonore.py <durée_s> public/bed.wav
import sys, wave, numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
SR = 44100
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 30.0
OUT = sys.argv[2] if len(sys.argv) > 2 else 'public/bed.wav'
BPM = 92; BEAT = 60 / BPM; BAR = 4 * BEAT; SWING = 0.06 * BEAT
rng = np.random.default_rng(7)
n = int(DUR * SR); t = np.arange(n) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def lp(x, c, o=2): return sosfilt(butter(o, c, 'low', fs=SR, output='sos'), x)
def hp(x, c, o=2): return sosfilt(butter(o, c, 'high', fs=SR, output='sos'), x)
L = np.zeros(n); R = np.zeros(n)

CH = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 69], [48, 55, 60, 62, 64], [55, 59, 62, 64, 67]]  # Am9 Fmaj7 Cadd9 G6
ROOT = [45, 41, 48, 43]; SEG = 2 * BAR

# --- pompe douce calée sur le kick (temps 1 et 3)
duck = np.ones(n)
for b in range(int(DUR / BEAT) + 1):
    if b % 2: continue
    a = int(b * BEAT * SR); m = min(n - a, int(0.45 * SR))
    if m <= 0: break
    tt = np.arange(m) / SR; duck[a:a + m] = np.minimum(duck[a:a + m], 1 - 0.45 * np.exp(-tt * 9))

# --- nappe « supersaw » : 7 voix désaccordées réparties en stéréo, filtre qui respire
padL = np.zeros(n); padR = np.zeros(n); k = 0; start = 0.0
while start < DUR:
    ch = CH[k % 4]; a, b = int(start * SR), min(n, int((start + SEG + 1.0) * SR)); tt = np.arange(b - a) / SR
    env = np.minimum(1, tt / 1.0) * np.minimum(1, np.maximum(0, SEG + 1.0 - tt) / 1.0)
    for m in ch:
        for v, det in enumerate(np.linspace(-0.12, 0.12, 7)):
            f = hz(m) * 2 ** (det / 12); saw = 2 * ((f * tt + rng.random()) % 1) - 1; pan = v / 6
            padL[a:b] += saw * env * (1 - pan) * 0.05; padR[a:b] += saw * env * pan * 0.05
    k += 1; start += SEG
blk = 4096
for s in range(0, n, blk):
    c = 900 + 700 * (0.5 + 0.5 * np.sin(2 * np.pi * (s / SR) / (SEG * 2)))
    padL[s:s + blk] = lp(padL[s:s + blk], c); padR[s:s + blk] = lp(padR[s:s + blk], c)
padL = lp(padL, 2500); padR = lp(padR, 2500)
L += padL * duck * 0.9; R += padR * duck * 0.9

# --- basse sub qui suit la fondamentale
sub = np.zeros(n)
for k in range(int(DUR / SEG) + 1):
    a, b = int(k * SEG * SR), min(n, int((k + 1) * SEG * SR))
    if b <= a: break
    tt = np.arange(b - a) / SR; f = hz(ROOT[k % 4] - 12); env = np.minimum(1, tt / 0.05) * np.minimum(1, np.maximum(0, SEG - tt) / 0.1)
    sub[a:b] = (np.sin(2 * np.pi * f * tt) + 0.15 * np.sin(4 * np.pi * f * tt)) * env
L += sub * duck * 0.28; R += sub * duck * 0.28

# --- arpège cloche FM + écho ping-pong
arpL = np.zeros(n); arpR = np.zeros(n); step = BEAT / 2; i = 0
while i * step < DUR:
    ch = CH[int(i * step // SEG) % 4]; m = ch[[0, 2, 4, 3, 1, 3, 4, 2][i % 8]] + 24
    a = int((i * step + (SWING if i % 2 else 0)) * SR); Ln = min(n - a, int(1.2 * SR))
    if Ln <= 0: break
    tt = np.arange(Ln) / SR; f = hz(m); idx = 1.6 * np.exp(-tt * 8)
    note = np.sin(2 * np.pi * f * tt + idx * np.sin(2 * np.pi * f * 3.5 * tt)) * np.exp(-tt * 4.5) * np.minimum(1, tt / 0.003)
    vel = 0.9 if i % 2 == 0 else 0.55; pan = 0.35 + 0.3 * ((i % 4) / 3)
    arpL[a:a + Ln] += note * vel * (1 - pan); arpR[a:a + Ln] += note * vel * pan; i += 1
arpL = lp(arpL, 6000); arpR = lp(arpR, 6000)
d = int(BEAT * 0.75 * SR); eL = np.zeros(n); eR = np.zeros(n)
eL[d:] += arpR[:-d] * 0.4; eR[2 * d:] += arpL[:-2 * d] * 0.3
L += (arpL + lp(eL, 3000)) * 0.13; R += (arpR + lp(eR, 3000)) * 0.13

# --- batterie feutrée : kick rond, rimshot léger (2 et 4), charleston swingué
kick = np.zeros(n); rim = np.zeros(n); hat = np.zeros(n)
for b in range(int(DUR / BEAT) + 1):
    a = int(b * BEAT * SR)
    if a >= n: break
    if b % 2 == 0:
        m = min(n - a, int(0.4 * SR)); tt = np.arange(m) / SR
        kick[a:a + m] += np.tanh(1.5 * np.sin(2 * np.pi * (48 + 90 * np.exp(-tt * 35)) * tt) * np.exp(-tt * 8))
    else:
        m = min(n - a, int(0.12 * SR)); tt = np.arange(m) / SR
        rim[a:a + m] += (np.sin(2 * np.pi * 1700 * tt) * 0.5 + rng.standard_normal(m) * 0.5) * np.exp(-tt * 45)
    for off, vel in ((0.5, 0.7), (0.0, 0.35)):
        a2 = int((b + off) * BEAT * SR + (SWING * SR if off else 0)); m = min(n - a2, int(0.06 * SR))
        if m > 0: hat[a2:a2 + m] += rng.standard_normal(m) * np.exp(-np.arange(m) / SR * 80) * vel
hat = hp(hat, 7000, 4); rim = hp(rim, 900)
L += kick * 0.30 + rim * 0.06 + hat * 0.045; R += kick * 0.30 + rim * 0.07 + hat * 0.06

# --- réverbe à convolution (salle sombre ~2,4 s), stéréo
ir_n = int(2.4 * SR); it = np.arange(ir_n) / SR
irL = lp(rng.standard_normal(ir_n) * np.exp(-it * 2.6), 4000); irR = lp(rng.standard_normal(ir_n) * np.exp(-it * 2.6), 4000)
irL /= np.sqrt((irL ** 2).sum()) * 4; irR /= np.sqrt((irR ** 2).sum()) * 4
L = L + fftconvolve(L, irL)[:n] * 0.35; R = R + fftconvolve(R, irR)[:n] * 0.35

# --- master : élargissement, chaleur, EQ, fondus, normalisation
M, S = (L + R) / 2, (L - R) / 2
S = hp(S, 200) * 1.3; L, R = M + S, M - S
pk = max(np.abs(L).max(), np.abs(R).max()); L, R = L / pk * 1.4, R / pk * 1.4
L = np.tanh(L) ; R = np.tanh(R)
L = lp(hp(L, 30), 14000); R = lp(hp(R, 30), 14000)
fi, fo = int(0.8 * SR), int(1.8 * SR)
for X in (L, R): X[:fi] *= np.linspace(0, 1, fi); X[-fo:] *= np.linspace(1, 0, fo)
pk = max(np.abs(L).max(), np.abs(R).max()); L, R = L / pk * 0.85, R / pk * 0.85
st = np.empty(2 * n); st[0::2] = L; st[1::2] = R
w = wave.open(OUT, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
print('ok', OUT, DUR)
