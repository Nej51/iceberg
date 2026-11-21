import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import data from './data.json';
import {useT, sp, lin, Sent, Background, Scene, HiBox, ZoomPhone, Stamp, Pill, Glow, pick, fontCss, ELEC, RED, GRN, YEL, CoverTitle, EndScreen} from './lib';
const P: any = data;
// Format COURT (16 s) sans voix, calé sur une musique funk à 112 BPM (temps n = 0,07 + 0,5345 × n).
// Exporté SANS musique : Nej ajoute le son dans l'appli TikTok/Insta, en le faisant démarrer à 0 s.
const B = (n: number) => 0.07 + 0.5345 * n;

// curseur de Notes (jaune) qui clignote, puis glisse d'un temps à l'autre
const Cursor: React.FC<{scale?: number; track: boolean; x: number; y: number}> = ({scale = 1, track, x, y}) => {
  const t = useT(); const on = track || Math.floor(t * 2) % 2 === 0;
  return <div style={{position: 'absolute', left: (x - 2) * scale, top: (y - 4) * scale, width: (track ? 6 : 4) * scale, height: 46 * scale, borderRadius: 3 * scale,
    background: track ? '#c7c7cc' : '#FFCC00', opacity: on ? 1 : 0, boxShadow: track ? `0 0 ${12 * scale}px rgba(255,255,255,0.6)` : 'none'}} />;
};
const Tap: React.FC<{scale?: number; x: number; y: number; t0: number}> = ({scale = 1, x, y, t0}) => {
  const t = useT(); if (t < t0 || t > t0 + 0.45) return null; const k = sp(t, t0, 10); const r = 34 * scale;
  return <div style={{position: 'absolute', left: x * scale - r, top: y * scale - r, width: r * 2, height: r * 2, borderRadius: '50%', border: `${4 * scale}px solid ${RED}`,
    background: 'rgba(255,69,58,0.25)', transform: `scale(${0.6 + 0.6 * k})`, opacity: 1 - lin(t, t0 + 0.3, t0 + 0.45)}} />;
};

export const Video: React.FC = () => {
  const t = useT();
  const src = pick(t, [[0, 'cs_notes.png'], [B(10), 'cs_track.png'], [B(17), 'cs_notes.png'], [B(19), 'cs_ok.png']]);
  const track = t >= B(10) && t < B(17);
  // glissement du curseur par paliers sur les temps 12, 14, 16
  const E = P.cur_end, R = P.cur_err; const hops = [B(12), B(14), B(16)];
  let f = 0; hops.forEach((h, i) => { f = Math.max(f, (i + interpolate(t, [h, h + 0.3], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})) / 3 * (t >= h ? 1 : 0)); });
  const cx = E[0] + (R[0] - E[0]) * f, cy = E[1] + (R[1] - E[1]) * f + (track ? -8 * Math.sin(f * Math.PI) : 0);
  const EB = P.err_box, SP = P.espace;
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />
    <Glow x={540} y={1000} r={320} color="#3b2cff" />

    <CoverTitle line="TON CLAVIER CACHE" keyword="UNE SOURIS" size={92} />

    {t < B(22) && <ZoomPhone src={src} t0={0} keys={[[0, 1.6, 300, 1010], [B(17) - 0.1, 2.0, EB[0], EB[1] + 30], [B(21), 1.6, 300, 1010]]}>
      <Cursor track={track} x={t >= B(19) ? EB[0] + 20 : cx} y={cy} />
      {(P.wrong_taps as number[][]).map((p, i) => <Tap key={i} x={p[0]} y={p[1]} t0={B(5 + i)} />)}
      <HiBox sx={SP[0]} sy={SP[1]} w={330} h={92} t0={B(10)} t1={B(12)} />
      <HiBox sx={EB[0] + 10} sy={EB[1] + 20} w={44} h={58} t0={B(17)} t1={B(19)} />
    </ZoomPhone>}

    <Scene t0={2.0} t1={B(10) - 0.15}>
      <Sent top={270} t0={B(4)} t1={B(10)} words={[[B(4), 'Placer le curseur ?'], [B(6), 'Mission', RED], [B(6) + 0.1, 'impossible…', RED]]} size={64} />
    </Scene>
    <Scene t0={B(10)} t1={B(16) + 0.2}>
      <Sent top={270} t0={B(10)} t1={B(12)} words={[[B(10), 'Appui long sur'], [B(10) + 0.15, 'espace', ELEC]]} size={74} />
      <Sent top={270} t0={B(12)} t1={B(17)} words={[[B(12), 'Le clavier devient'], [B(13), 'une souris', GRN]]} size={64} />
      <Stamp t0={B(10)} text="APPUI LONG" color={ELEC} x={540} y={470} size={52} />
    </Scene>
    <Scene t0={B(17)} t1={B(22) - 0.2}>
      <Sent top={270} t0={B(17)} t1={B(22)} words={[[B(17), 'Pile sur la'], [B(18), 'faute', RED]]} size={74} />
      <Stamp t0={B(20)} text="CORRIGÉ !" color={GRN} x={540} y={470} size={60} />
    </Scene>

    <EndScreen t0={B(22)} t1={B(26)} tEnd={B(30)} tAbonne={B(26) + 0.05} tPour={B(27)} tImmergee={B(28)} />
    <div style={{position: 'absolute', left: 0, top: 0, height: 8, width: `${(t / 16.1) * 100}%`, background: ELEC, boxShadow: `0 0 20px ${ELEC}`}} />
  </AbsoluteFill>;
};
