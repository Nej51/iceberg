import React from 'react';
import {AbsoluteFill, OffthreadVideo, Sequence, staticFile} from 'remotion';
import {useT, sp, lin, Scene, fontCss, ELEC, TS, CoverTitle, EndScreen, Finish, Caption, CapData, HookPunch} from './lib';
import cap from './st_ht.json';
// Haptic Touch (27/11/2026) : tournage de Nej (iPhone filmé dans la voiture), refait au style sobre.
export const HT_TOTAL = 60.75;

const Night: React.FC = () => { const t = useT();
  return <AbsoluteFill style={{background: '#040406'}}>
    <div style={{position: 'absolute', left: 20, top: 480 + 30 * Math.sin(t * 0.5), width: 1040, height: 1040, borderRadius: '50%', background: 'radial-gradient(circle, rgba(47,91,255,0.22), transparent 65%)', filter: 'blur(40px)'}} />
  </AbsoluteFill>; };

// Vidéo de Nej : plan [a, b] de la voix, démarre à la seconde `raw` du tournage. zoom = [[t, échelle, x, y]] (point visé, repère vidéo 1080x1920)
const VY = 300, VS = 0.92;
const Clip: React.FC<{a: number; b: number; raw: number; rate?: number; zoom?: [number, number, number, number][]; blur?: number}> = ({a, b, raw, rate = 1, zoom = [], blur = 0}) => {
  const t = useT(); if (t < a - 0.01 || t > b + 0.35) return null;
  let z = 1, fx = 540, fy = 900;
  for (let i = 0; i < zoom.length; i++) { const [s, zz, xx, yy] = zoom[i]; const p = i ? zoom[i - 1] : [s, 1, 540, 900];
    const k = lin(t, s, s + 0.7); const e = 1 - Math.pow(1 - k, 3); if (t >= s) { z = p[1] + (zz - p[1]) * e; fx = p[2] + (xx - p[2]) * e; fy = p[3] + (yy - p[3]) * e; } }
  const push = 1 + 0.03 * lin(t, a, b);
  return <AbsoluteFill style={{overflow: 'hidden'}}>
    <div style={{position: 'absolute', left: (1080 - 1080 * VS) / 2, top: VY, width: 1080 * VS, height: 1920 * VS, transformOrigin: `${fx * VS}px ${fy * VS}px`, transform: `scale(${z * push})`, filter: blur ? `blur(${blur}px) brightness(0.55)` : undefined}}>
      <Sequence from={Math.round(a * 30)} layout="none">
        <OffthreadVideo src={staticFile('ht_raw.mp4')} startFrom={Math.round(raw * 30)} playbackRate={rate} muted style={{width: '100%', height: '100%'}} />
      </Sequence>
    </div>
    {/* fondus noirs haut / bas / côtés */}
    <AbsoluteFill style={{background: 'linear-gradient(180deg, #040406 0%, #040406 15%, rgba(4,4,6,0.55) 26%, transparent 36%, transparent 80%, rgba(4,4,6,0.85) 95%, #040406 100%)'}} />
    <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(4,4,6,0.8) 0%, transparent 14%, transparent 86%, rgba(4,4,6,0.8) 100%)'}} />
  </AbsoluteFill>;
};

const Head: React.FC<{t0: number; t1: number; tag: string; a: string; b?: string; c?: string; size?: number}> = ({t0, t1, tag, a, b, c, size = 64}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const k = sp(t, t0, 15); const o = lin(t, t1 - 0.25, t1);
  return <div style={{position: 'absolute', top: 250, left: 60, width: 860, textAlign: 'center', opacity: Math.min(1, k * 1.6) * (1 - o), transform: `translateY(${(1 - k) * 30}px)`}}>
    <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 32, letterSpacing: 9, color: ELEC}}>{tag}</div>
    <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: size, lineHeight: 1.12, color: '#fff', marginTop: 14, textShadow: TS}}>{a}{b && <span style={{color: ELEC}}>{b}</span>}{c}</div>
  </div>;
};

// chrono réel de l'appui (mesuré sur le tournage)
const Chrono: React.FC<{t0: number; t1: number; press: number; open: number; tag: string}> = ({t0, t1, press, open, tag}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const k = sp(t, t0, 14); const o = lin(t, t1 - 0.25, t1);
  const v = Math.max(0, Math.min(t, open) - press); const done = t >= open; const kd = sp(t, open, 10);
  return <div style={{position: 'absolute', top: 240, left: 60, width: 860, textAlign: 'center', opacity: Math.min(1, k * 1.6) * (1 - o)}}>
    <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 34, letterSpacing: 9, color: ELEC}}>{tag}</div>
    <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 150, lineHeight: 1.05, color: '#fff', textShadow: done ? `0 0 40px ${ELEC}` : TS, transform: `scale(${1 + 0.08 * kd * (1 - lin(t, open + 0.3, open + 0.6))})`}}>
      {v.toFixed(1).replace('.', ',')} s</div>
  </div>;
};

const Big: React.FC<{t0: number; t1: number; top?: number; children: React.ReactNode; size?: number}> = ({t0, t1, top = 640, children, size = 86}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const k = sp(t, t0, 13); const o = lin(t, t1 - 0.25, t1);
  return <div style={{position: 'absolute', top, left: 60, width: 960 - 60, textAlign: 'center', fontFamily: 'Pop', fontWeight: 700, fontSize: size, lineHeight: 1.15, color: '#fff', textShadow: TS,
    transform: `scale(${0.9 + 0.1 * k})`, opacity: Math.min(1, k * 1.5) * (1 - o)}}>{children}</div>;
};

// barre de recherche des Réglages (sobre) + résultat
const Search: React.FC<{t0: number; type0: number; res: number}> = ({t0, type0, res}) => {
  const t = useT(); const k = sp(t, t0, 14); const txt = 'Haptic Touch'; const n = Math.max(0, Math.min(txt.length, Math.floor((t - type0) / 0.07) + 1)); const typing = t >= type0;
  const kr = sp(t, res, 13); const cur = Math.floor(t * 2.2) % 2 === 0;
  return <>
    <div style={{position: 'absolute', left: 110, top: 640, width: 860, height: 120, borderRadius: 60, background: 'rgba(255,255,255,0.1)', border: '1.5px solid rgba(255,255,255,0.22)', backdropFilter: 'blur(20px)',
      display: 'flex', alignItems: 'center', gap: 26, padding: '0 40px', boxSizing: 'border-box', transform: `scale(${0.9 + 0.1 * k})`, opacity: Math.min(1, k * 1.5)}}>
      <svg width="54" height="54" viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5" stroke="rgba(255,255,255,0.75)" strokeWidth="2.4" fill="none" /><path d="M15.5 15.5L20 20" stroke="rgba(255,255,255,0.75)" strokeWidth="2.4" strokeLinecap="round" /></svg>
      <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 56, color: typing ? '#fff' : 'rgba(255,255,255,0.45)'}}>{typing ? txt.slice(0, n) : 'Rechercher'}<span style={{color: ELEC, opacity: cur ? 1 : 0}}>|</span></div>
    </div>
    {t >= res && <div style={{position: 'absolute', left: 110, top: 800, width: 860, borderRadius: 40, background: 'rgba(255,255,255,0.08)', border: `2.5px solid ${ELEC}`, boxShadow: `0 0 40px rgba(47,91,255,0.5)`,
      padding: '30px 44px', boxSizing: 'border-box', transform: `translateY(${(1 - kr) * 40}px)`, opacity: Math.min(1, kr * 1.6)}}>
      <div style={{fontFamily: 'Int', fontWeight: 700, fontSize: 56, color: '#fff'}}>Haptic Touch</div>
      <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 38, color: 'rgba(255,255,255,0.6)', marginTop: 8}}>Accessibilité › Toucher</div>
    </div>}
  </>;
};

export const Video: React.FC = () => {
  const t = useT();
  return <AbsoluteFill style={{background: '#040406'}}>
    <style>{fontCss}</style>
    <Night />

    {/* COUVERTURE + ACCROCHE : le menu « Haptic Touch » et l'appui lent */}
    <Scene t0={0} t1={6.2}>
      <Clip a={0} b={6.2} raw={13.4} />
      <HookPunch t1={6.0} top={250} size={88} words={[[2.5, 'Un réglage'], [3.1, 'de 3 secondes', ELEC], [4.45, 'avant'], [5.25, 'après', ELEC]]} />
      {t < 2.0 && <AbsoluteFill style={{background: `rgba(0,0,0,${0.5 * (1 - lin(t, 1.6, 2.0))})`}} />}
      <CoverTitle line="TON IPHONE TE FAIT" keyword="ATTENDRE" size={84} />
    </Scene>

    <Scene t0={6.24} t1={8.2}>
      <Clip a={6.24} b={8.2} raw={0.0} />
      <Head t0={6.3} t1={8.2} tag="EN 4 ÉTAPES" a="Voilà comment " b="faire" />
    </Scene>
    <Scene t0={8.24} t1={11.32}>
      <Clip a={8.24} b={11.32} raw={1.9} />
      <Head t0={8.3} t1={11.32} tag="ÉTAPE 1" a="Réglages › " b="Accessibilité" />
    </Scene>
    <Scene t0={11.36} t1={15.68}>
      <Clip a={11.36} b={15.68} raw={4.8} />
      <Head t0={11.4} t1={15.68} tag="ÉTAPE 2" a="Physique et motricité › " b="Toucher" size={58} />
    </Scene>
    <Scene t0={15.72} t1={18.78}>
      <Clip a={15.72} b={18.78} raw={9.9} />
      <Head t0={15.78} t1={18.78} tag="ÉTAPE 3" a="Touche " b="Haptic Touch" />
    </Scene>
    <Scene t0={18.82} t1={21.92}>
      <Clip a={18.82} b={21.92} raw={13.1} zoom={[[19.0, 1.45, 540, 600]]} />
      <Head t0={18.86} t1={21.92} tag="3 DURÉES" a="Longue, Par défaut, " b="Courte" size={58} />
    </Scene>
    <Scene t0={21.96} t1={25.96}>
      <Clip a={21.96} b={25.96} raw={23.0} />
      <Head t0={22.0} t1={25.96} tag="ÉTAPE 4" a="Coche " b="Courte" c=" et teste" />
    </Scene>
    <Scene t0={26.0} t1={28.5}>
      <Clip a={26.0} b={28.5} raw={24.6} />
      <Head t0={26.04} t1={28.5} tag="ET VOILÀ" a="Ça s’ouvre " b="tout de suite" />
    </Scene>
    <Scene t0={28.54} t1={29.86}>
      <Big t0={28.58} t1={29.86} top={760} size={96}>Regarde la <span style={{color: ELEC}}>différence</span></Big>
    </Scene>

    {/* AVANT / APRÈS avec le vrai temps d'appui */}
    <Scene t0={29.9} t1={33.16}>
      <Clip a={29.9} b={33.16} raw={16.9} />
      <Chrono t0={29.92} t1={33.16} press={30.3} open={31.6} tag="AVANT · LONGUE" />
    </Scene>
    <Scene t0={33.2} t1={34.68}>
      <Clip a={33.2} b={34.68} raw={24.6} />
      <Chrono t0={33.22} t1={34.68} press={33.5} open={34.1} tag="APRÈS · COURTE" />
    </Scene>
    <Scene t0={34.72} t1={38.04}>
      <Clip a={34.72} b={38.04} raw={0.0} rate={0.6} blur={14} />
      <Big t0={34.8} t1={38.04} top={560} size={80}>Ça marche <span style={{color: ELEC}}>partout</span></Big>
      <Big t0={36.06} t1={38.04} top={760} size={76}>Applis</Big>
      <Big t0={36.6} t1={38.04} top={870} size={76}>Liens</Big>
      <Big t0={37.04} t1={38.04} top={980} size={76}>Photos</Big>
    </Scene>

    {/* LE PIÈGE */}
    <Scene t0={38.08} t1={44.44}>
      <Clip a={38.08} b={42.3} raw={28.6} rate={0.55} />
      <Clip a={42.3} b={44.44} raw={19.9} />
      <Head t0={38.12} t1={42.3} tag="LE PIÈGE" a="Un menu s’ouvre " b="par erreur ?" size={50} />
      <Head t0={42.34} t1={44.44} tag="LA SOLUTION" a="Repasse sur " b="Par défaut" />
    </Scene>

    {/* BONUS : la recherche */}
    <Scene t0={44.48} t1={51.08}>
      <Head t0={44.52} t1={51.08} tag="BONUS" a="Pas besoin de " b="chercher" />
      <Search t0={44.6} type0={47.84} res={49.72} />
    </Scene>

    {/* PARTAGE */}
    <Scene t0={51.12} t1={54.9}>
      <Big t0={51.16} t1={54.9} top={680}>Envoie-la à quelqu’un qui trouve son iPhone <span style={{color: ELEC}}>trop lent</span></Big>
    </Scene>

    <Caption data={cap as CapData} from={2.0} until={54.9} top={1360} />
    <EndScreen t0={54.96} t1={56.9} tEnd={59.5} tAbonne={57.34} tPour={57.88} tImmergee={58.62} />
    <Finish total={HT_TOTAL} />
  </AbsoluteFill>;
};
