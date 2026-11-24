import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, Sequence, staticFile} from 'remotion';
import {useT, sp, lin, Sent, Background, Glass, Scene, Stamp, Pill, Glow, fontCss, ELEC, RED, GRN, YEL, ORG, TS, CoverTitle, EndScreen, Finish} from './lib';
// Vidéo « Voici l'iPhone 20 » (rumeurs iPhone 20 Pro), 24/11/2026. Images = vidéo source découpée dans une carte.
export const TOTAL = 62.7;
const CX = 60, CY = 660, CW = 960, CH = 540;

// carte vidéo : clips = [début (s voix), début dans clip.mp4 (s), vitesse]
const Card: React.FC<{t0: number; t1: number; clips: [number, number, number][]; enter?: boolean}> = ({t0, t1, clips, enter = true}) => {
  const t = useT(); if (t < t0 || t > t1 + 0.35) return null;
  const k = enter ? sp(t, t0, 12) : 1; const o = lin(t, t1, t1 + 0.3);
  let ci = 0; for (let i = 0; i < clips.length; i++) if (t >= clips[i][0]) ci = i;
  const pk = sp(t, clips[ci][0], 12); const cut = ci > 0;
  const dy = 8 * Math.sin(t * 1.1), ry = 2.5 * Math.sin(t * 0.7), rx = (1 - k) * 30 + 1.5 * Math.sin(t * 0.9);
  return <div style={{position: 'absolute', left: CX, top: CY, width: CW, height: CH, perspective: 1800, opacity: Math.min(1, k * 1.5) * (1 - o),
    transform: `translateY(${dy + (1 - k) * 260}px) scale(${(0.82 + 0.18 * k) * (1 - o * 0.08)})`}}>
    <div style={{position: 'absolute', inset: -90, borderRadius: 120, background: 'radial-gradient(ellipse at center, rgba(47,91,255,0.55), rgba(106,44,255,0.25) 50%, transparent 75%)', filter: 'blur(50px)'}} />
    <div style={{position: 'absolute', inset: 0, borderRadius: 44, overflow: 'hidden', background: '#000', border: '2px solid rgba(255,255,255,0.3)',
      boxShadow: '0 40px 100px rgba(0,0,0,0.75), 0 0 60px rgba(47,91,255,0.35)', transform: `rotateX(${rx}deg) rotateY(${ry}deg)`}}>
      {clips.map(([a, from, rate], i) => { const b = i + 1 < clips.length ? clips[i + 1][0] : t1 + 0.4;
        return <Sequence key={i} from={Math.round(a * 30)} durationInFrames={Math.max(1, Math.round((b - a) * 30) + 1)} layout="none">
          <div style={{position: 'absolute', inset: 0, transform: `scale(${i === ci && cut ? 1 + 0.12 * (1 - pk) : 1.0})`}}>
            <OffthreadVideo src={staticFile('clip.mp4')} startFrom={Math.round(from * 30)} playbackRate={rate} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} /></div></Sequence>; })}
      {cut && <div style={{position: 'absolute', inset: 0, background: '#fff', opacity: 0.35 * (1 - Math.min(1, pk * 1.6))}} />}
      <div style={{position: 'absolute', inset: 0, background: `linear-gradient(${115 + ry * 6}deg, rgba(255,255,255,0.14) 0%, transparent 25%, transparent 75%, rgba(255,255,255,0.06) 100%)`}} />
    </div></div>;
};

const RumorTag: React.FC<{n: number; t0: number}> = ({n, t0}) => {
  const t = useT(); const k = sp(t, t0, 12);
  return <Glass style={{left: 540 - 230, top: 250, width: 460, height: 110, borderRadius: 55, display: 'flex', alignItems: 'center', gap: 22, padding: '0 22px', boxSizing: 'border-box',
    transform: `scale(${k}) translateY(${(1 - k) * -40}px)`, opacity: Math.min(1, k * 1.5)}}>
    <div style={{width: 72, height: 72, borderRadius: 22, background: ELEC, boxShadow: `0 0 30px ${ELEC}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Pop', fontWeight: 700, fontSize: 46, color: '#fff'}}>{n}</div>
    <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 56, color: '#fff', letterSpacing: 2}}>RUMEUR {n}</div></Glass>;
};
// barre 1-2-3-4 sous la carte
const RumorBar: React.FC<{cur: number; t0: number}> = ({cur, t0}) => {
  const t = useT();
  return <div style={{position: 'absolute', left: 0, width: 1080, top: 1355, display: 'flex', justifyContent: 'center', gap: 26}}>
    {[1, 2, 3, 4].map((n, i) => { const k = sp(t, t0 + i * 0.06, 12); const done = n < cur, on = n === cur; const p = 0.5 + 0.5 * Math.sin(t * 6);
      return <div key={n} style={{width: on ? 150 : 74, height: 74, borderRadius: 37, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${k})`,
        background: done ? GRN : on ? ELEC : 'rgba(255,255,255,0.08)', border: on || done ? 'none' : '2px solid rgba(255,255,255,0.25)',
        boxShadow: on ? `0 0 ${18 + 18 * p}px ${ELEC}` : done ? `0 0 16px ${GRN}` : 'none', fontFamily: 'Pop', fontWeight: 700, fontSize: 38, color: '#fff'}}>
        {done ? <svg width="36" height="36" viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6.5" stroke="#fff" strokeWidth="3.4" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg> : n}</div>; })}
  </div>;
};
const Under: React.FC<{t0: number; t1: number; children: React.ReactNode; border?: string; size?: number}> = ({t0, t1, children, border, size = 44}) => {
  const t = useT(); if (t > t1) return null; return <Pill t0={t0} x={540} y={1265} size={size} border={border}>{children}</Pill>;
};
// mini iPhone (courbé = bords lumineux arrondis, plat = coins nets)
const Mini: React.FC<{x: number; y: number; w: number; h: number; t0: number; curved: boolean; label?: string; color?: string}> = ({x, y, w, h, t0, curved, label, color = ELEC}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 10); const f = 6 * Math.sin(t * 2 + x);
  return <div style={{position: 'absolute', left: x - w / 2, top: y - h / 2 + f, width: w, height: h, transform: `scale(${k}) rotate(${(1 - k) * -18}deg)`}}>
    <div style={{position: 'absolute', inset: 0, borderRadius: curved ? w * 0.22 : w * 0.08, background: curved ? 'linear-gradient(90deg,#9fb4ff 0%,#1b2a7a 9%,#0d1440 50%,#1b2a7a 91%,#9fb4ff 100%)' : '#0d1440',
      border: curved ? 'none' : '5px solid #8a8f9c', boxShadow: curved ? `0 0 40px ${color}, inset 0 0 30px rgba(140,170,255,0.6)` : '0 20px 40px rgba(0,0,0,0.5)'}} />
    <div style={{position: 'absolute', left: w / 2 - w * 0.17, top: h * 0.04, width: w * 0.34, height: w * 0.1, borderRadius: 30, background: '#000'}} />
    {label && <div style={{position: 'absolute', top: h + 22, left: -60, width: w + 120, textAlign: 'center', fontFamily: 'Pop', fontWeight: 700, fontSize: 40, color, whiteSpace: 'nowrap'}}>{label}</div>}
  </div>;
};
const Box: React.FC<{t0: number; t1: number; children: React.ReactNode}> = ({t0, t1, children}) => {
  const t = useT(); if (t < t0 || t > t1 + 0.35) return null; const k = sp(t, t0, 12); const o = lin(t, t1, t1 + 0.3);
  return <Glass style={{left: CX, top: CY - 20, width: CW, height: CH + 40, transform: `scale(${(0.85 + 0.15 * k)})`, opacity: Math.min(1, k * 1.5) * (1 - o), overflow: 'visible'}}>{children}</Glass>;
};
const Count: React.FC<{t0: number; to: number; dur: number}> = ({t0, to, dur}) => {
  const t = useT(); const v = Math.round(to * (1 - Math.pow(1 - lin(t, t0, t0 + dur), 3))); return <>{v}</>;
};

export const Video: React.FC = () => {
  const t = useT();
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* ACCROCHE */}
    <Scene t0={0} t1={6.6}>
      <Card t0={0} t1={6.6} enter={false} clips={[[0, 18.3, 0.85], [5.0, 22.4, 1]]} />
      <CoverTitle line="VOICI L’" keyword="IPHONE 20" />
      <Sent top={280} t0={2.0} t1={7} words={[[2.0, 'Pas d’iPhone'], [2.0, '19 Pro', RED]]} size={76} />
      <Sent top={380} t0={2.0} t1={7} words={[[2.46, 'mais un'], [3.04, 'iPhone 20 Pro', ELEC]]} size={76} />
      <Under t0={4.1} t1={5.0} border="#4fd7ff">aux bords incurvés</Under>
      <Stamp t0={5.06} text="RUMEURS" color={ORG} x={540} y={1280} />
    </Scene>

    {/* RUMEUR 1 : verre courbé */}
    <Scene t0={6.6} t1={16.85}>
      <RumorTag n={1} t0={7.16} />
      <Sent top={400} t0={7.9} t1={9.1} words={[[8.0, 'Du verre'], [8.32, 'courbé', ELEC], [8.56, 'tout autour']]} size={62} />
      <Sent top={400} t0={9.1} t1={13.5} words={[[9.22, 'Écran arrondi sur'], [12.08, 'les 4 bords', ELEC]]} size={62} />
      <Sent top={400} t0={13.5} t1={17} words={[[13.58, 'Bordures de'], [14.66, '1 mm', ELEC]]} size={66} />
      <Sent top={485} t0={13.5} t1={17} words={[[15.4, 'presque'], [16.26, 'invisibles', GRN]]} size={56} />
      <Card t0={6.8} t1={16.85} clips={[[6.8, 8.23, 0.7], [9.4, 9.73, 0.7], [12.3, 25.7, 0.65]]} />
      <Under t0={9.42} t1={13.4}>Mark Gurman · Bloomberg</Under>
      <RumorBar cur={1} t0={7.3} />
    </Scene>

    {/* RUMEUR 2 : 4 prototypes */}
    <Scene t0={16.85} t1={24.85}>
      <RumorTag n={2} t0={17.0} />
      <Sent top={400} t0={17.5} t1={20.9} words={[[18.02, 'Apple testerait'], [19.1, '4 prototypes', ELEC]]} size={62} />
      <Sent top={400} t0={20.9} t1={25} words={[[21.0, '2 courbés', ELEC], [23.2, '+ 2 plats', YEL]]} size={66} />
      <Sent top={485} t0={20.9} t1={25} words={[[24.2, 'au cas où', SOFTC]]} size={52} />
      <Card t0={16.9} t1={20.85} clips={[[16.9, 13.9, 0.62]]} />
      <Box t0={20.9} t1={24.85}>
        <Mini x={150} y={240} w={150} h={300} t0={21.0} curved label="courbé" />
        <Mini x={370} y={240} w={150} h={300} t0={21.25} curved label="courbé" />
        <Mini x={590} y={240} w={150} h={300} t0={23.2} curved={false} label="plat" color={YEL} />
        <Mini x={810} y={240} w={150} h={300} t0={23.4} curved={false} label="plat" color={YEL} />
      </Box>
      <RumorBar cur={2} t0={17.1} />
    </Scene>

    {/* RUMEUR 3 : 200 Mpx */}
    <Scene t0={24.85} t1={31.6}>
      <RumorTag n={3} t0={24.94} />
      <Sent top={400} t0={25.4} t1={32} words={[[25.6, 'Une caméra de'], [26.36, '200 Mpx', ELEC]]} size={66} />
      <Sent top={485} t0={27.9} t1={32} words={[[28.02, 'meilleure'], [30.22, 'la nuit', ELEC], [30.62, 'et en contre-jour']]} size={50} />
      <Card t0={24.9} t1={31.6} clips={[[24.9, 5.0, 1.0], [28.0, 11.67, 0.55]]} />
      <Under t0={26.3} t1={40} border={ELEC} size={50}><span style={{color: '#fff'}}><Count t0={26.36} to={200} dur={1.1} /></span><span style={{color: SOFTC}}>mégapixels</span></Under>
      <RumorBar cur={3} t0={25.0} />
    </Scene>

    {/* RUMEUR 4 : boutons, puce, batterie, écran, Dynamic Island */}
    <Scene t0={31.6} t1={44.95}>
      <RumorTag n={4} t0={31.96} />
      <Sent top={400} t0={32.6} t1={34.1} words={[[32.82, 'Des boutons qui'], [33.4, 'ne s’enfoncent plus', ELEC]]} size={56} />
      <Sent top={400} t0={34.1} t1={36.0} words={[[34.2, 'Nouvelle puce'], [34.76, 'A21 Pro', ELEC]]} size={62} />
      <Sent top={400} t0={36.0} t1={37.95} words={[[36.06, 'Batterie qui dure'], [36.74, 'plus longtemps', GRN]]} size={58} />
      <Sent top={400} t0={37.95} t1={42.45} words={[[38.38, 'Un écran plus'], [38.52, 'grand', ELEC]]} size={66} />
      <Sent top={400} t0={42.45} t1={45.3} words={[[42.66, 'Dynamic Island'], [43.62, 'conservée', GRN]]} size={62} />
      <Sent top={485} t0={42.45} t1={45.3} words={[[44.4, 'mais plus petite']]} size={52} />
      <Card t0={31.7} t1={37.9} clips={[[31.7, 0.3, 0.9], [34.0, 16.4, 0.9], [36.1, 2.3, 1.0]]} />
      <Under t0={34.3} t1={36.0} border={ELEC}>Puce A21 Pro</Under>
      <Under t0={36.2} t1={37.9} border={GRN}>Batterie plus endurante</Under>
      <Box t0={37.95} t1={42.4}>
        <Mini x={300} y={300} w={190} h={390} t0={39.66} curved label={'Pro : 6,4"'} />
        <Mini x={660} y={275} w={215} h={440} t0={41.22} curved label={'Pro Max : ≈ 7"'} color="#b48cff" />
      </Box>
      <Card t0={42.45} t1={44.95} clips={[[42.45, 10.2, 0.5]]} />
      <RumorBar cur={4} t0={32.0} />
    </Scene>

    {/* RIEN N'EST SÛR + PARTAGE */}
    <Scene t0={44.95} t1={53.6}>
      <Sent top={290} t0={45.0} t1={50.2} words={[[45.04, 'Attention :']]} size={70} />
      <Sent top={390} t0={45.0} t1={50.2} words={[[45.58, 'rien n’est'], [46.06, 'encore sûr', RED]]} size={70} />
      <Sent top={290} t0={50.2} t1={54} words={[[50.34, 'Quelqu’un hésite à'], [51.76, 'changer d’iPhone ?', YEL]]} size={58} />
      <Sent top={390} t0={50.2} t1={54} words={[[52.58, 'Envoie-lui'], [52.88, 'cette vidéo', ELEC]]} size={70} />
      <Card t0={45.0} t1={53.6} clips={[[45.0, 22.4, 0.75], [49.4, 8.23, 0.75], [51.4, 9.73, 0.75]]} />
      <Under t0={48.3} t1={50.2} border={ELEC}>Sortie prévue : septembre 2027</Under>
    </Scene>

    {/* PETIT DÉBAT */}
    <Scene t0={53.6} t1={56.25}>
      <Glow x={540} y={1000} r={330} color="#3b2cff" />
      <Sent top={330} t0={53.6} t1={57} words={[[54.2, 'Et toi ?', YEL]]} size={110} />
      <Mini x={300} y={950} w={220} h={450} t0={55.2} curved label="Courbé" />
      <div style={{position: 'absolute', left: 0, width: 1080, top: 900, textAlign: 'center', fontFamily: 'Pop', fontWeight: 700, fontSize: 70, color: '#fff', textShadow: TS, opacity: lin(t, 55.6, 55.8)}}>ou</div>
      <Mini x={780} y={950} w={220} h={450} t0={55.9} curved={false} label="Plat" color={YEL} />
    </Scene>

    <EndScreen t0={56.26} t1={58.8} tEnd={61.2} tAbonne={58.86} tPour={59.28} tImmergee={60.24} />
    <Finish total={TOTAL} />
  </AbsoluteFill>;
};
const SOFTC = 'rgba(200,210,255,0.85)';
