import React from 'react';
import {AbsoluteFill, Audio, Img, interpolate, spring, staticFile, useCurrentFrame} from 'remotion';
export const ELEC = '#2F5BFF', RED = '#FF453A', GRN = '#34C759', YEL = '#FFD60A', ORG = '#FF8A00';
export const fontCss = `
@font-face{font-family:Pop;src:url(${staticFile('Poppins-Bold.ttf')});font-weight:700}
@font-face{font-family:Int;src:url(${staticFile('Inter-Bold.otf')});font-weight:700}
@font-face{font-family:Int;src:url(${staticFile('Inter-SemiBold.otf')});font-weight:600}`;
export const C = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const useT = () => useCurrentFrame() / 30;
export const sp = (t: number, t0: number, damping = 14) => (t < t0 ? 0 : spring({frame: (t - t0) * 30, fps: 30, config: {damping, mass: 0.7, stiffness: 140}}));
export const lin = (t: number, a: number, b: number) => interpolate(t, [a, b], [0, 1], C);
export const TS = '0 6px 30px rgba(0,0,0,0.65)';

export const Word: React.FC<{t0: number; children: React.ReactNode; size?: number; color?: string}> = ({t0, children, size = 130, color = '#fff'}) => {
  const t = useT(); const k = sp(t, t0); if (t < t0) return null;
  const glow = color !== '#fff' ? `, 0 0 30px ${color}88` : '';
  return <span style={{display: 'inline-block', fontFamily: 'Pop', fontWeight: 700, fontSize: size, color, lineHeight: 1.12, letterSpacing: -1, textShadow: TS + glow,
    transform: `translateY(${(1 - k) * 60}px) scale(${0.9 + 0.1 * k})`, filter: `blur(${(1 - Math.min(1, k)) * 18}px)`, opacity: Math.min(1, k * 1.4), margin: '0 10px', whiteSpace: 'nowrap'}}>{children}</span>;
};
export const Line: React.FC<{top: number; children: React.ReactNode}> = ({top, children}) =>
  <div style={{position: 'absolute', top, left: 60, width: 860, textAlign: 'center'}}>{children}</div>;
export type W = [number, string, string?];
export const Sent: React.FC<{top: number; t0: number; t1: number; words: W[]; size?: number}> = ({top, t0, t1, words, size = 66}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const o = lin(t, t1 - 0.2, t1);
  return <div style={{opacity: 1 - o}}><Line top={top}>{words.map(([a, w, c], i) => <Word key={i} t0={a} size={size} color={c || '#fff'}>{w}</Word>)}</Line></div>;
};
export const Background: React.FC = () => {
  const t = useT();
  const b = (x: number, y: number, r: number, c: string, s: number, ph: number) =>
    <div style={{position: 'absolute', left: x + 120 * Math.sin(t * s + ph) - r, top: y + 160 * Math.cos(t * s * 0.8 + ph) - r, width: r * 2, height: r * 2, borderRadius: '50%', background: c, filter: 'blur(120px)', opacity: 0.55}} />;
  return <AbsoluteFill style={{background: 'linear-gradient(180deg,#05060f 0%,#0a0d2a 55%,#120a2e 100%)', overflow: 'hidden'}}>
    {b(200, 500, 380, '#1e3cff', 0.5, 0)}{b(900, 1300, 420, '#6a2cff', 0.4, 2)}{b(500, 1900, 360, '#0a6cff', 0.6, 4)}
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.55) 100%)'}} /></AbsoluteFill>;
};
export const Glass: React.FC<{style?: React.CSSProperties; children?: React.ReactNode}> = ({style, children}) =>
  <div style={{position: 'absolute', borderRadius: 48, background: 'linear-gradient(135deg,rgba(255,255,255,0.16),rgba(255,255,255,0.04))',
    border: '1.5px solid rgba(255,255,255,0.22)', boxShadow: '0 30px 80px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.35)',
    backdropFilter: 'blur(30px)', WebkitBackdropFilter: 'blur(30px)', ...style}}>{children}</div>;
export const Icon: React.FC<{src: string; t0: number; size: number; x: number; y: number; float?: boolean}> = ({src, t0, size, x, y, float = true}) => {
  const t = useT(); const k = sp(t, t0, 11); if (t < t0) return null;
  return <Img src={staticFile(src)} style={{position: 'absolute', left: x - size / 2, top: y - size / 2 + (float ? 10 * Math.sin(t * 2.2 + x) : 0), width: size, height: size,
    transform: `scale(${k}) rotate(${(1 - k) * -25}deg)`, filter: 'drop-shadow(0 25px 30px rgba(0,0,0,0.5))'}} />;
};
export const Scene: React.FC<{t0: number; t1: number; children: React.ReactNode}> = ({t0, t1, children}) => {
  const t = useT(); if (t < t0 || t > t1 + 0.3) return null; const o = lin(t, t1, t1 + 0.3); const i = t0 <= 0 ? 1 : lin(t, t0, t0 + 0.25); // 1re scène : pas de fondu, sinon la couverture est vide
  return <AbsoluteFill style={{opacity: Math.min(i, 1 - o), filter: o > 0 ? `blur(${o * 24}px)` : undefined, transform: `scale(${1 + o * 0.15})`}}>{children}</AbsoluteFill>;
};
export const SW = 600, SH = 1300;
export const Phone: React.FC<{src: string; x: number; top: number; w: number; t0?: number; tilt?: number; ph?: number; float?: boolean; children?: React.ReactNode}> = ({src, x, top, w, t0, tilt = 0, ph = 0, float = true, children}) => {
  const t = useT(); const p = w * 0.03; const iw = w - 2 * p; const ih = iw * SH / SW; const k = t0 === undefined ? 1 : sp(t, t0, 16);
  const dx = float ? Math.sin(t * 0.8 + ph) * (w * 0.018) : 0, dy = float ? Math.sin(t * 0.62 + ph + 1) * (w * 0.022) : 0;
  const ry = float ? Math.sin(t * 0.55 + ph) * 4.5 : 0, rx = (1 - k) * 35 + tilt + (float ? Math.sin(t * 0.47 + ph + 2) * 2.2 : 0);
  return <div style={{position: 'absolute', left: x - w / 2, top: top + (1 - k) * 1000, width: w, height: ih + 2 * p, perspective: 1700}}>
    <div style={{position: 'absolute', inset: -w * 0.18, borderRadius: '50%', background: 'radial-gradient(ellipse at center, rgba(47,91,255,0.5), rgba(106,44,255,0.25) 45%, transparent 72%)', filter: 'blur(60px)', opacity: 0.9 * k}} />
    <div style={{width: '100%', height: '100%', borderRadius: w * 0.16, padding: p, boxSizing: 'border-box', background: 'linear-gradient(145deg,#7a7a84,#2a2a30 42%,#55555c)', boxShadow: '0 60px 120px rgba(0,0,0,0.7), inset 0 0 0 2px rgba(255,255,255,0.18)', transform: `translate(${dx}px,${dy}px) rotateX(${rx}deg) rotateY(${ry}deg)`, transformStyle: 'preserve-3d'}}>
      <div style={{width: iw, height: ih, borderRadius: w * 0.14, overflow: 'hidden', position: 'relative', background: '#000'}}>
        <Img src={staticFile(src)} style={{width: iw, height: ih}} />
        <div style={{position: 'absolute', inset: 0, background: `linear-gradient(${110 + ry * 4}deg, rgba(255,255,255,0.1) 0%, transparent 22%, transparent 78%, rgba(255,255,255,0.05) 100%)`, pointerEvents: 'none'}} />
        <div style={{position: 'absolute', left: 0, top: 0, width: iw, height: ih}}>{React.Children.map(children, (c) => React.isValidElement(c) ? React.cloneElement(c as any, {scale: iw / SW}) : c)}</div>
      </div></div></div>;
};
export const HiBox: React.FC<{sx: number; sy: number; w: number; h: number; t0: number; t1?: number; scale?: number}> = ({sx, sy, w, h, t0, t1 = 999, scale = 1}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const k = sp(t, t0, 12); const pls = 0.5 + 0.5 * Math.sin(t * 5);
  return <div style={{position: 'absolute', left: (sx - w / 2) * scale, top: (sy - h / 2) * scale, width: w * scale, height: h * scale, borderRadius: 18 * scale, border: `${3.5 * scale}px solid rgba(90,140,255,${0.7 + 0.3 * pls})`, boxShadow: `0 0 ${(16 + 16 * pls) * scale}px rgba(47,91,255,0.9), inset 0 0 ${12 * scale}px rgba(47,91,255,0.4)`, transform: `scale(${1.04 - 0.04 * k})`, opacity: Math.min(1, k * 1.6)}} />;
};
export const ZW = 440, ZP = ZW * 0.03, ZS = (ZW - 2 * ZP) / 600;
export const ZoomPhone: React.FC<{src: string; keys: [number, number, number, number][]; t0: number; children?: React.ReactNode}> = ({src, keys, t0, children}) => {
  const t = useT(); let z = 1, fx = 300, fy = 650;
  for (let i = 0; i < keys.length; i++) { const [a, zz, xx, yy] = keys[i]; const pz = i ? keys[i - 1] : [a, 1, 300, 650];
    const k = interpolate(t, [a, a + 0.6], [0, 1], {...C, easing: (x) => 1 - Math.pow(1 - x, 3)});
    if (t >= a) { z = pz[1] + (zz - pz[1]) * k; fx = pz[2] + (xx - pz[2]) * k; fy = pz[3] + (yy - pz[3]) * k; } }
  const winTop = 560, winH = 900; const px = 540 - ZW / 2 + ZP + fx * ZS, py = 20 + ZP + fy * ZS; const m = 1 - 1 / z;
  return <div style={{position: 'absolute', left: 0, top: winTop, width: 1080, height: winH, overflow: 'hidden', WebkitMaskImage: 'linear-gradient(180deg,transparent 0,#000 60px,#000 calc(100% - 60px),transparent 100%)'}}>
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 2000, transformOrigin: `${px}px ${py}px`, transform: `translate(${(540 - px) * m}px, ${(winH / 2 - py) * m}px) scale(${z})`}}>
      <Phone src={src} x={540} top={20} w={ZW} t0={t0} float={false}>{children}</Phone></div></div>;
};
export const Waves: React.FC<{cx: number; cy: number; t0: number; color?: string; r0?: number}> = ({cx, cy, t0, color = GRN, r0 = 120}) => {
  const t = useT(); if (t < t0) return null;
  return <>{[0, 1, 2].map((i) => { const p = ((t - t0) * 0.9 + i / 3) % 1; const r = r0 + p * 260;
    return <div key={i} style={{position: 'absolute', left: cx - r, top: cy - r, width: r * 2, height: r * 2, borderRadius: '50%', border: `${8 - 6 * p}px solid ${color}`, opacity: (1 - p) * 0.8, boxShadow: `0 0 40px ${color}`}} />;})}</>;
};
export const StepTag: React.FC<{n: number; t0: number}> = ({n, t0}) => {
  const t = useT(); const k = sp(t, t0, 13);
  return <Glass style={{left: 540 - 210, top: 250, width: 420, height: 110, borderRadius: 55, display: 'flex', alignItems: 'center', gap: 22, padding: '0 22px', boxSizing: 'border-box',
    transform: `scale(${k}) translateY(${(1 - k) * -40}px)`, opacity: Math.min(1, k * 1.5)}}>
    <div style={{width: 72, height: 72, borderRadius: 22, background: ELEC, boxShadow: `0 0 30px ${ELEC}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Pop', fontWeight: 700, fontSize: 46, color: '#fff'}}>{n}</div>
    <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 58, color: '#fff', letterSpacing: 2}}>ÉTAPE {n}</div></Glass>;
};
export const Checklist: React.FC<{cur: number; t0: number}> = ({cur, t0}) => {
  const t = useT();
  return <div style={{position: 'absolute', left: 52, top: 640, display: 'flex', flexDirection: 'column', gap: 34}}>
    {[1, 2, 3, 4].map((n, i) => { const k = sp(t, t0 + i * 0.08, 12); const done = n < cur, on = n === cur; const p = 0.5 + 0.5 * Math.sin(t * 6);
      return <div key={n} style={{width: 78, height: 78, borderRadius: 26, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${k})`,
        background: done ? GRN : on ? ELEC : 'rgba(255,255,255,0.08)', border: on || done ? 'none' : '2px solid rgba(255,255,255,0.25)',
        boxShadow: on ? `0 0 ${20 + 20 * p}px ${ELEC}` : done ? `0 0 20px ${GRN}` : 'none', fontFamily: 'Pop', fontWeight: 700, fontSize: 42, color: '#fff'}}>
        {done ? <svg width="40" height="40" viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6.5" stroke="#fff" strokeWidth="3.4" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg> : n}</div>; })}
  </div>;
};
export const Stamp: React.FC<{t0: number; text: string; color: string; x: number; y: number; rot?: number; size?: number}> = ({t0, text, color, x, y, rot = -8, size = 70}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 10);
  return <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) rotate(${rot}deg) scale(${2 - k})`, opacity: Math.min(1, k * 2), whiteSpace: 'nowrap',
    background: color, border: '7px solid #fff', borderRadius: 30, padding: '14px 40px', fontFamily: 'Pop', fontWeight: 700, fontSize: size, color: '#fff', boxShadow: `0 20px 60px rgba(0,0,0,0.5), 0 0 40px ${color}`}}>{text}</div>;
};
export const Pill: React.FC<{t0: number; x: number; y: number; children: React.ReactNode; size?: number; border?: string}> = ({t0, x, y, children, size = 44, border}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12);
  return <Glass style={{left: x, top: y, transform: `translate(-50%,-50%) scale(${k})`, borderRadius: 60, padding: '18px 40px', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', gap: 18,
    fontFamily: 'Pop', fontWeight: 700, fontSize: size, color: '#fff', border: border ? `2.5px solid ${border}` : undefined}}>{children}</Glass>;
};
// photo plein cadre, thème nuit
export const Photo: React.FC<{src: string; t0: number; t1: number; dim?: number}> = ({src, t0, t1, dim = 0.3}) => {
  const t = useT(); const z = 1.04 + 0.08 * lin(t, t0, t1);
  return <AbsoluteFill style={{overflow: 'hidden'}}>
    <Img src={staticFile(src)} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${z})`}} />
    <AbsoluteFill style={{background: `rgba(5,6,20,${dim})`}} />
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(5,6,15,0.92) 0%, rgba(5,6,15,0.55) 28%, transparent 48%, transparent 75%, rgba(18,10,46,0.75) 100%)'}} />
  </AbsoluteFill>;
};
// carte appel
export const CallCard: React.FC<{t0: number; y: number; title: string; sub: string; color: string; icon?: string; t1?: number}> = ({t0, y, title, sub, color, icon = 'telephone_receiver_3d.png', t1 = 999}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const k = sp(t, t0, 13); const sh = Math.sin(t * 40) * 4 * (1 - lin(t, t0, t0 + 1.5));
  return <Glass style={{left: 140, top: y, width: 800, height: 190, transform: `translateY(${(1 - k) * -80}px) translateX(${sh}px)`, opacity: Math.min(1, k * 1.5), display: 'flex', alignItems: 'center', padding: '0 34px', boxSizing: 'border-box', gap: 28}}>
    <Img src={staticFile(icon)} style={{width: 110, height: 110, filter: 'drop-shadow(0 10px 20px rgba(0,0,0,0.5))'}} />
    <div style={{flex: 1}}><div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 32, color: 'rgba(220,225,255,0.8)'}}>{sub}</div>
      <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 50, color, whiteSpace: 'nowrap'}}>{title}</div></div>
    <div style={{width: 84, height: 84, borderRadius: 42, background: color === RED ? RED : GRN, boxShadow: `0 0 30px ${color === RED ? RED : GRN}`}} />
  </Glass>;
};
export const Bubble: React.FC<{t0: number; y: number; right?: boolean; text: string; label: string; t1?: number}> = ({t0, y, right, text, label, t1 = 999}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const k = sp(t, t0, 12);
  return <div style={{position: 'absolute', top: y, left: right ? undefined : 90, right: right ? 160 : undefined, maxWidth: 760, transform: `scale(${k})`, transformOrigin: right ? 'right top' : 'left top'}}>
    <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 28, color: 'rgba(200,210,255,0.85)', marginBottom: 10, textAlign: right ? 'right' : 'left'}}>{label}</div>
    <div style={{background: right ? ELEC : 'rgba(255,255,255,0.14)', border: '1.5px solid rgba(255,255,255,0.25)', borderRadius: 40, padding: '24px 34px', fontFamily: 'Int', fontWeight: 600, fontSize: 40, color: '#fff', lineHeight: 1.25, boxShadow: right ? `0 0 40px ${ELEC}88` : '0 20px 50px rgba(0,0,0,0.4)'}}>{text}</div></div>;
};
// tri des appels (carte déclic)
export const Sorter: React.FC<{t0: number}> = ({t0}) => {
  const t = useT(); const calls: [number, string, boolean][] = [[0.2, 'Démarchage', false], [0.8, 'Maman', true], [1.4, 'Numéro inconnu', false], [2.0, 'Livreur', true]];
  return <Glass style={{left: 140, top: 1000, width: 800, height: 420, overflow: 'hidden'}}>
    <div style={{position: 'absolute', left: 0, right: 0, top: 205, height: 6, background: ELEC, boxShadow: `0 0 30px ${ELEC}`}} />
    {calls.map(([d, l, ok], i) => { const tt = t - t0 - d; if (tt < 0) return null; const y = -90 + Math.min(tt, 1.6) * 260; const past = y > 150;
      const fade = !ok && past ? lin(tt, 0.95, 1.3) : 0;
      return <div key={i} style={{position: 'absolute', left: 400 - 230 + (i % 2 ? 60 : -60), top: y, width: 460, height: 84, borderRadius: 42, display: 'flex', alignItems: 'center', gap: 16, padding: '0 26px', boxSizing: 'border-box',
        background: past ? (ok ? GRN : RED) : 'rgba(255,255,255,0.15)', opacity: 1 - fade, fontFamily: 'Pop', fontWeight: 700, fontSize: 36, color: '#fff', transform: `scale(${1 - fade * 0.3})`}}>
        <span>{past ? (ok ? '✔' : '✖') : '☎'}</span><span style={{whiteSpace: 'nowrap'}}>{l}</span></div>; })}
  </Glass>;
};
export const Glow: React.FC<{x: number; y: number; r: number; color: string}> = ({x, y, r, color}) =>
  <div style={{position: 'absolute', left: x - r, top: y - r, width: 2 * r, height: 2 * r, borderRadius: '50%', background: color, filter: 'blur(80px)', opacity: 0.6}} />;


export const pick = (t: number, list: [number, string][]) => { let s = list[0][1]; for (const [a, v] of list) if (t >= a) s = v; return s; };

// TITRE DE COUVERTURE (obligatoire, frame 0 -> 1,6 s). line = texte blanc, key = mot sur bandeau bleu
export const CoverTitle: React.FC<{line: string; keyword: string; after?: string; size?: number}> = ({line, keyword, after, size = 104}) => {
  const t = useT(); if (t >= 2.0) return null; const o = lin(t, 1.6, 2.0);
  return <div style={{position: 'absolute', top: 0, left: 0, width: 1080, height: 1920, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: '0 60px', boxSizing: 'border-box',
    background: `radial-gradient(ellipse 75% 22% at 50% 50%, rgba(0,0,20,${0.55 * (1 - o)}), transparent)`, filter: `blur(${o * 20}px)`, opacity: 1 - o}}>
    {line && <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: size, color: '#fff', lineHeight: 1.08, textShadow: TS}}>{line}</div>}
    <div style={{display: 'inline-block', marginTop: 18, background: ELEC, borderRadius: 22, padding: '6px 34px', fontFamily: 'Pop', fontWeight: 700, fontSize: size + 8, color: '#fff', boxShadow: `0 0 50px ${ELEC}`}}>{keyword}</div>
    {after && <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: size, color: '#fff', lineHeight: 1.08, textShadow: TS, marginTop: 10}}>{after}</div>}
  </div>;
};

// FIN : « Enregistre cette vidéo » (t0) puis logo + « Abonne-toi » (t1). Mots calés sur la voix via les temps donnés.
export const EndScreen: React.FC<{t0: number; t1: number; tEnd: number; tAbonne: number; tPour: number; tImmergee: number}> = ({t0, t1, tEnd, tAbonne, tPour, tImmergee}) => {
  const t = useT();
  return <>
    <Scene t0={t0} t1={t1}>
      <Sent top={330} t0={t0} t1={t1 + 0.3} words={[[t0 + 0.05, 'Enregistre'], [t0 + 0.45, 'cette vidéo', ELEC]]} size={84} />
      <Icon src="bookmark_3d.png" t0={t0 + 0.5} size={380} x={540} y={900} />
      <Pill t0={t0 + 0.8} x={540} y={1240} size={50}>pour la retrouver</Pill>
    </Scene>
    <Scene t0={t1} t1={tEnd + 1}>
      <Glow x={540} y={760} r={340} color="#7a2cff" />
      <Sent top={300} t0={t1} t1={tEnd + 2} words={[[tAbonne, 'Abonne-toi', YEL]]} size={96} />
      {(() => { const k = sp(t, t1 + 0.05, 9); return <Img src={staticFile('logo.png')} style={{position: 'absolute', left: 240, top: 440 + 8 * Math.sin(t * 2.2), width: 600, height: 600, transform: `scale(${k}) rotate(${(1 - k) * -20}deg)`, filter: 'drop-shadow(0 0 40px rgba(110,80,255,0.7))'}} />; })()}
      <Sent top={1080} t0={t1} t1={tEnd + 2} words={[[tPour, 'pour découvrir la partie']]} size={58} />
      <Sent top={1155} t0={t1} t1={tEnd + 2} words={[[tImmergee, 'immergée', ELEC], [tImmergee + 0.5, 'de ton iPhone']]} size={58} />
      <Pill t0={tImmergee - 0.3} x={540} y={1340} size={46} border="#4fd7ff">@iphoneiceberg</Pill>
    </Scene>
  </>;
};

// Barre de progression + sons (à mettre en dernier dans la vidéo)
export const Finish: React.FC<{total: number}> = ({total}) => { const t = useT();
  return <><div style={{position: 'absolute', left: 0, top: 0, height: 8, width: `${(t / total) * 100}%`, background: ELEC, boxShadow: `0 0 20px ${ELEC}`}} />
    <Audio src={staticFile('voice.wav')} /><Audio src={staticFile('sfx.wav')} /></>; };
