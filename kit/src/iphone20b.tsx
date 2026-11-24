import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, Sequence, staticFile} from 'remotion';
import {useT, sp, lin, Sent, fontCss, ELEC, CoverTitle, Finish} from './lib';
import CL from './clips2.json';
// « Voici l'iPhone 20 » v3 (24/11/2026) : style sobre — fond noir, vidéo bord à bord, blanc + 1 bleu.
export const TOTAL = 62.7;
const CLIPS = CL as [number, number, number][];
const VY = 540, VH = 900, VEND = 56.3;

const VideoLayer: React.FC = () => {
  const t = useT(); if (t > VEND + 0.5) return null; const o = lin(t, VEND, VEND + 0.45);
  return <div style={{position: 'absolute', left: 0, top: VY, width: 1080, height: VH, overflow: 'hidden', opacity: 1 - o,
    WebkitMaskImage: 'linear-gradient(180deg,transparent 0,#000 110px,#000 calc(100% - 110px),transparent 100%)'}}>
    {CLIPS.map(([a, from, rate], i) => { const b = i + 1 < CLIPS.length ? CLIPS[i + 1][0] : VEND + 0.5; const z = 1 + 0.06 * lin(t, a, b);
      return <Sequence key={i} from={Math.round(a * 30)} durationInFrames={Math.max(1, Math.round((b - a) * 30))} layout="none">
        <div style={{position: 'absolute', inset: 0, transform: `scale(${z})`}}>
          <OffthreadVideo src={staticFile('clip2.mp4')} startFrom={Math.round(from * 30)} playbackRate={rate} muted style={{width: 1080, height: VH}} /></div></Sequence>; })}
  </div>;
};
const Label: React.FC<{t0: number; t1: number; n: number}> = ({t0, t1, n}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const k = lin(t, t0, t0 + 0.35), o = lin(t, t1 - 0.25, t1);
  return <div style={{position: 'absolute', top: 232, width: 1080, textAlign: 'center', fontFamily: 'Int', fontWeight: 600, fontSize: 32, letterSpacing: 8, color: 'rgba(255,255,255,0.55)',
    opacity: k * (1 - o), transform: `translateY(${(1 - k) * 12}px)`}}>RUMEUR {n} / 4</div>;
};
const Info: React.FC<{t0: number; t1: number; text: string}> = ({t0, t1, text}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const k = lin(t, t0, t0 + 0.4), o = lin(t, t1 - 0.25, t1);
  return <div style={{position: 'absolute', top: 470, width: 1080, textAlign: 'center', padding: '0 80px', boxSizing: 'border-box', fontFamily: 'Int', fontWeight: 600, fontSize: 40,
    color: 'rgba(255,255,255,0.7)', opacity: k * (1 - o), transform: `translateY(${(1 - k) * 14}px)`}}>{text}</div>;
};
const L1 = 290, L2 = 378, S1 = 72;

const End: React.FC = () => {
  const t = useT(); if (t < 56.26) return null;
  const k = sp(t, 58.85, 10);
  return <>
    {t < 59.1 && <div style={{opacity: 1 - lin(t, 58.7, 59.0)}}>
      <Sent top={760} t0={56.26} t1={59.1} words={[[56.3, 'Enregistre'], [56.8, 'cette vidéo', ELEC]]} size={84} />
      <div style={{position: 'absolute', top: 880, width: 1080, textAlign: 'center', fontFamily: 'Int', fontWeight: 600, fontSize: 44, color: 'rgba(255,255,255,0.65)', opacity: lin(t, 57.2, 57.6)}}>pour la retrouver quand tu en auras besoin</div>
    </div>}
    {t >= 58.8 && <>
      <div style={{position: 'absolute', left: 240, top: 600, width: 600, height: 600, borderRadius: '50%', background: 'radial-gradient(circle, rgba(47,91,255,0.35), transparent 65%)', filter: 'blur(40px)', opacity: k}} />
      <Sent top={420} t0={58.8} t1={70} words={[[58.86, 'Abonne-toi']]} size={92} />
      <Img src={staticFile('logo.png')} style={{position: 'absolute', left: 290, top: 560 + 8 * Math.sin(t * 2), width: 500, height: 500, transform: `scale(${k})`}} />
      <Sent top={1100} t0={58.8} t1={70} words={[[59.28, 'pour découvrir la partie']]} size={54} />
      <Sent top={1170} t0={58.8} t1={70} words={[[60.24, 'immergée', ELEC], [60.72, 'de ton iPhone']]} size={54} />
      <div style={{position: 'absolute', top: 1290, width: 1080, textAlign: 'center', fontFamily: 'Int', fontWeight: 600, fontSize: 38, letterSpacing: 2, color: 'rgba(255,255,255,0.55)', opacity: lin(t, 60.5, 61.0)}}>@iphoneiceberg</div>
    </>}
  </>;
};

export const Video: React.FC = () => {
  const t = useT();
  return <AbsoluteFill style={{background: '#040406'}}>
    <style>{fontCss}</style>
    <AbsoluteFill style={{background: 'radial-gradient(ellipse 80% 40% at 50% 52%, rgba(30,50,140,0.18), transparent 70%)'}} />
    <VideoLayer />

    {/* ACCROCHE */}
    <CoverTitle line="VOICI L’" keyword="IPHONE 20" size={118} />
    <Sent top={L1} t0={2.0} t1={3.8} words={[[2.0, 'Pas d’iPhone 19 Pro']]} size={S1} />
    <Sent top={L2} t0={2.0} t1={3.8} words={[[2.46, 'mais un'], [3.04, 'iPhone 20 Pro', ELEC]]} size={S1} />
    <Sent top={L1} t0={3.8} t1={6.6} words={[[3.82, 'aux bords'], [4.24, 'incurvés', ELEC]]} size={S1} />
    <Info t0={5.06} t1={6.6} text="Voici tout ce qu’on sait" />

    {/* RUMEUR 1 */}
    <Label n={1} t0={7.1} t1={16.85} />
    <Sent top={L1} t0={7.9} t1={9.1} words={[[8.0, 'Du verre'], [8.32, 'courbé', ELEC]]} size={S1} />
    <Sent top={L2} t0={7.9} t1={9.1} words={[[8.56, 'tout autour']]} size={S1} />
    <Sent top={L1} t0={9.1} t1={13.5} words={[[9.22, 'Un écran arrondi']]} size={S1} />
    <Sent top={L2} t0={9.1} t1={13.5} words={[[11.86, 'sur les'], [12.08, '4 bords', ELEC]]} size={S1} />
    <Info t0={9.42} t1={13.5} text="Selon Mark Gurman, de Bloomberg" />
    <Sent top={L1} t0={13.5} t1={16.85} words={[[13.58, 'Des bordures de'], [14.66, '1 mm', ELEC]]} size={S1} />
    <Info t0={15.4} t1={16.85} text="presque invisibles de face" />

    {/* RUMEUR 2 */}
    <Label n={2} t0={16.95} t1={24.85} />
    <Sent top={L1} t0={17.5} t1={20.9} words={[[18.02, 'Apple testerait']]} size={S1} />
    <Sent top={L2} t0={17.5} t1={20.9} words={[[19.1, '4 prototypes', ELEC]]} size={S1} />
    <Sent top={L1} t0={20.9} t1={24.85} words={[[21.0, '2 avec écran'], [21.86, 'courbé', ELEC]]} size={S1} />
    <Sent top={L2} t0={20.9} t1={24.85} words={[[23.2, '2 avec écran plat']]} size={S1} />
    <Info t0={24.2} t1={24.85} text="au cas où" />

    {/* RUMEUR 3 */}
    <Label n={3} t0={24.9} t1={31.6} />
    <Sent top={L1} t0={25.4} t1={31.6} words={[[25.6, 'Un appareil photo de']]} size={S1} />
    <Sent top={L2} t0={25.4} t1={31.6} words={[[26.36, '200 mégapixels', ELEC]]} size={S1} />
    <Info t0={28.02} t1={31.6} text="Meilleur la nuit et en contre-jour" />

    {/* RUMEUR 4 */}
    <Label n={4} t0={31.9} t1={44.95} />
    <Sent top={L1} t0={32.6} t1={34.1} words={[[32.82, 'Des boutons qui']]} size={S1} />
    <Sent top={L2} t0={32.6} t1={34.1} words={[[33.4, 'ne s’enfoncent plus', ELEC]]} size={S1} />
    <Sent top={L1} t0={34.1} t1={35.95} words={[[34.2, 'Une nouvelle puce']]} size={S1} />
    <Sent top={L2} t0={34.1} t1={35.95} words={[[34.76, 'A21 Pro', ELEC]]} size={S1} />
    <Sent top={L1} t0={35.95} t1={37.95} words={[[36.06, 'Une batterie qui tient']]} size={S1} />
    <Sent top={L2} t0={35.95} t1={37.95} words={[[36.74, 'plus longtemps', ELEC]]} size={S1} />
    <Sent top={L1} t0={37.95} t1={42.45} words={[[38.38, 'Un écran plus'], [38.52, 'grand', ELEC]]} size={S1} />
    <Info t0={39.66} t1={41.15} text="6,4 pouces pour le Pro" />
    <Info t0={41.22} t1={42.45} text="presque 7 pouces pour le Pro Max" />
    <Sent top={L1} t0={42.45} t1={44.95} words={[[42.66, 'La Dynamic Island']]} size={S1} />
    <Sent top={L2} t0={42.45} t1={44.95} words={[[43.62, 'reste'], [44.5, 'en plus petit', ELEC]]} size={S1} />

    {/* RIEN N'EST SÛR + PARTAGE */}
    <Sent top={L1} t0={44.95} t1={50.2} words={[[45.04, 'Attention :']]} size={S1} />
    <Sent top={L2} t0={44.95} t1={50.2} words={[[45.58, 'rien n’est'], [46.06, 'encore sûr', ELEC]]} size={S1} />
    <Info t0={48.0} t1={50.2} text="Sortie prévue en septembre 2027" />
    <Sent top={L1} t0={50.2} t1={53.6} words={[[50.34, 'Quelqu’un hésite'], [51.36, 'à changer d’iPhone ?']]} size={56} />
    <Sent top={L2 + 10} t0={50.2} t1={53.6} words={[[52.58, 'Envoie-lui'], [52.88, 'cette vidéo', ELEC]]} size={S1} />

    {/* DÉBAT */}
    <Sent top={L1} t0={53.6} t1={56.26} words={[[54.2, 'Et toi ?']]} size={S1} />
    <Sent top={L2} t0={53.6} t1={56.26} words={[[55.18, 'Courbé ou'], [56.0, 'plat ?', ELEC]]} size={S1} />

    <End />
    <Finish total={TOTAL} />
  </AbsoluteFill>;
};
