import React from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, Sequence, staticFile} from 'remotion';
import {useT, lin, fontCss, ELEC, CoverTitle, Caption, HookPunch, CapData} from './lib';
import cap from './sous_titres_test.json';
// Test des nouveaux outils (24/11/2026) : accroche coup de poing + sous-titres mot à mot + voix sans temps morts.
export const TEST_TOTAL = 15.3;
const CLIPS: [number, number, number][] = [[0, 52.5, 0.72], [2.94, 44.87, 0.84], [4.28, 39.97, 0.97], [6.42, 12.57, 0.7], [8.34, 34.87, 0.84], [10.04, 57.5, 0.85], [11.64, 48.47, 0.93], [13.36, 16.64, 1.0]];
const VY = 540, VH = 900;
const Layer: React.FC = () => {
  const t = useT();
  return <div style={{position: 'absolute', left: 0, top: VY, width: 1080, height: VH, overflow: 'hidden', WebkitMaskImage: 'linear-gradient(180deg,transparent 0,#000 110px,#000 calc(100% - 110px),transparent 100%)'}}>
    {CLIPS.map(([a, from, rate], i) => { const b = i + 1 < CLIPS.length ? CLIPS[i + 1][0] : TEST_TOTAL; const z = 1 + 0.06 * lin(t, a, b);
      return <Sequence key={i} from={Math.round(a * 30)} durationInFrames={Math.max(1, Math.round((b - a) * 30))} layout="none">
        <div style={{position: 'absolute', inset: 0, transform: `scale(${z})`}}><OffthreadVideo src={staticFile('clip2.mp4')} startFrom={Math.round(from * 30)} playbackRate={rate} muted style={{width: 1080, height: VH}} /></div></Sequence>; })}
  </div>;
};
const Label: React.FC<{t0: number; text: string; top?: number}> = ({t0, text, top = 300}) => {
  const t = useT(); if (t < t0) return null; const k = lin(t, t0, t0 + 0.35);
  return <div style={{position: 'absolute', top, left: 60, width: 860, textAlign: 'center', fontFamily: 'Int', fontWeight: 600, fontSize: 34, letterSpacing: 8, color: 'rgba(255,255,255,0.6)', opacity: k}}>{text}</div>;
};
export const Test: React.FC = () => {
  const t = useT();
  return <AbsoluteFill style={{background: '#040406'}}>
    <style>{fontCss}</style>
    <Layer />
    {t < 2.1 && <AbsoluteFill style={{background: 'radial-gradient(ellipse 70% 30% at 50% 50%, rgba(0,0,0,0.55), rgba(0,0,0,0.25))', opacity: 1 - lin(t, 1.6, 2.0)}} />}
    <CoverTitle line="VOICI" keyword="L’IPHONE 20" size={112} />
    <HookPunch t1={4.9} top={215} size={80} words={[[2.0, 'Pas d’iPhone 19'], [2.42, 'mais un'], [2.94, 'iPhone 20', ELEC], [4.28, 'incurvé', ELEC]]} />
    {t >= 6.42 && <Label t0={6.42} top={300} text="RUMEUR 1 / 4" />}
    {t >= 8.34 && t < 11.6 && <Label t0={8.34} top={350} text="SELON BLOOMBERG" />}
    <Caption data={cap as CapData} from={4.9} top={1240} />
    <Audio src={staticFile('voice_test.wav')} />
    <div style={{position: 'absolute', left: 0, top: 0, height: 8, width: `${(t / TEST_TOTAL) * 100}%`, background: ELEC, boxShadow: `0 0 20px ${ELEC}`}} />
  </AbsoluteFill>;
};
