import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile} from 'remotion';
import {useT, sp, lin, Sent, Background, Scene, Phone, ZoomPhone, StepTag, Checklist, HiBox, Stamp, Photo, Glow, Waves, Pill, pick, fontCss, ELEC, RED, GRN, CoverTitle} from './lib';
// « Au secours » version SANS VOIX (25/11/2026) : tout se lit à l'écran, ~29 s, pas de musique (Nej ajoute un son tendance).
export const MUET_TOTAL = 29.4;

const Giant: React.FC<{t0: number; t1: number; text: string; color: string; size?: number; top?: number}> = ({t0, t1, text, color, size = 300, top = 720}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const z = 1 + 0.06 * sp(t, t0 + text.length * 0.08 + 0.2, 10);
  return <div style={{position: 'absolute', top, left: 0, width: 1080, textAlign: 'center', transform: `scale(${z})`}}>
    {text.split('').map((c, i) => { const k = sp(t, t0 + i * 0.08, 9);
      return <span key={i} style={{display: 'inline-block', fontFamily: 'Pop', fontWeight: 700, fontSize: size, color, lineHeight: 1, textShadow: `0 10px 40px rgba(0,0,0,0.7), 0 0 60px ${color}`,
        transform: `translateY(${(1 - k) * -700}px)`, opacity: Math.min(1, k * 2)}}>{c}</span>; })}</div>;
};

export const Video: React.FC = () => {
  const t = useT();
  // écrans du tuto (étapes)
  const scr = pick(t, [[10.0, 'as_reg.png'], [11.9, 'as_fid0.png'], [12.6, 'as_fid1.png'], [14.2, 'as_all.png'], [16.0, 'as_new0.png'],
    [16.4, 'as_new1.png'], [16.85, 'as_new2.png'], [17.3, 'as_new3.png'], [17.75, 'as_new4.png'], [18.2, 'as_new5.png'], [18.65, 'as_new6.png'], [19.1, 'as_new7.png'],
    [21.3, 'as_sc.png'], [22.7, 'as_name.png'], [23.9, 'as_sc2.png'], [24.3, 'as_ask.png']]);
  const cur = t < 14.2 ? 1 : t < 16.0 ? 2 : t < 22.7 ? 3 : t < 26.6 ? 4 : 5;
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE + accroche */}
    <Scene t0={0} t1={4.6}>
      <Photo src="img_escalier.png" t0={0} t1={4.9} dim={0.12} />
      <Waves cx={150} cy={1325} t0={2.2} color={ELEC} r0={30} />
      <Sent top={300} t0={2.05} t1={4.6} words={[[2.05, 'Tu tombes,']]} size={84} />
      <Sent top={410} t0={2.6} t1={4.6} words={[[2.6, 'ton iPhone est'], [2.85, 'hors de portée', RED]]} size={64} />
      <CoverTitle line="TON IPHONE APPELLE À" keyword="L’AIDE" />
    </Scene>

    {/* « Dis Siri, au secours » -> le résultat */}
    <Scene t0={4.6} t1={8.1}>
      <Glow x={540} y={1000} r={360} color="#7a2cff" />
      <Sent top={280} t0={4.75} t1={6.3} words={[[4.75, 'Tu dis juste :']]} size={64} />
      <Sent top={370} t0={5.05} t1={6.3} words={[[5.05, '« Dis Siri,'], [5.35, 'au secours »', ELEC]]} size={80} />
      <Sent top={300} t0={6.4} t1={8.1} words={[[6.4, 'Et ton iPhone'], [6.7, 'fait tout', GRN]]} size={84} />
      <Phone src={t < 6.4 ? 'as_siri.png' : 'as_done.png'} x={540} top={520} w={470} t0={4.65} />
    </Scene>

    {/* l'IA le crée */}
    <Scene t0={8.1} t1={10.0}>
      <Glow x={540} y={900} r={400} color={ELEC} />
      <Giant t0={8.2} t1={10.0} text="L’IA" color={ELEC} />
      <Sent top={1100} t0={8.7} t1={10.0} words={[[8.7, 'le crée'], [8.9, 'pour toi', ELEC]]} size={76} />
    </Scene>

    {/* ÉTAPES */}
    <Scene t0={10.0} t1={26.6}>
      <StepTag n={1} t0={10.05} />
      {t >= 14.2 && <StepTag n={2} t0={14.2} />}
      {t >= 16.0 && <StepTag n={3} t0={16.0} />}
      {t >= 22.7 && <StepTag n={4} t0={22.7} />}
      <Checklist cur={cur} t0={10.1} />
      <ZoomPhone src={scr} t0={10.0} keys={[[10.0, 1, 300, 650], [10.9, 1.7, 300, 890], [11.9, 1.75, 300, 587], [14.2, 1, 300, 650], [14.8, 1.8, 470, 200],
        [16.0, 1.75, 300, 470], [21.0, 1.4, 400, 700], [21.3, 1, 300, 650], [22.7, 1.8, 300, 200], [23.9, 1, 300, 650], [24.3, 1.5, 300, 730]]}>
        <HiBox sx={300} sy={890} w={556} h={62} t0={11.0} t1={11.9} />
        <HiBox sx={300} sy={587} w={556} h={62} t0={12.2} t1={14.2} />
        <HiBox sx={556} sy={108} w={70} h={70} t0={15.0} t1={16.0} />
        <HiBox sx={522} sy={792} w={62} h={62} t0={20.9} t1={21.3} />
        <HiBox sx={300} sy={110} w={300} h={56} t0={22.9} t1={23.9} />
        <HiBox sx={300} sy={685} w={460} h={80} t0={24.6} t1={26.6} />
      </ZoomPhone>
      {/* étape 1 */}
      <Sent top={385} t0={10.3} t1={11.9} words={[[10.3, 'Réglages', ELEC]]} />
      <Sent top={465} t0={10.7} t1={11.9} words={[[10.7, 'puis'], [10.8, 'Face ID et code', ELEC]]} />
      <Sent top={385} t0={12.0} t1={14.2} words={[[12.0, 'Active'], [12.15, 'Siri', ELEC]]} />
      <Sent top={465} t0={12.35} t1={14.2} words={[[12.35, 'en mode verrouillé', ELEC]]} />
      {/* étape 2 */}
      <Sent top={385} t0={14.35} t1={16.0} words={[[14.35, 'Ouvre'], [14.5, 'Raccourcis', ELEC]]} />
      <Sent top={465} t0={14.8} t1={16.0} words={[[14.8, 'et touche le'], [15.0, '+', ELEC]]} />
      {/* étape 3 */}
      <Sent top={385} t0={16.15} t1={20.9} words={[[16.15, 'Écris ce que tu veux']]} />
      <Sent top={465} t0={16.5} t1={20.9} words={[[16.5, 'avec tes mots', ELEC]]} />
      <Sent top={385} t0={20.95} t1={22.7} words={[[20.95, 'Valide', GRN]]} />
      {t < 22.7 && <Stamp t0={21.5} text="C’EST PRÊT !" color={GRN} x={540} y={470} size={70} />}
      {/* étape 4 */}
      <Sent top={385} t0={22.85} t1={24.3} words={[[22.85, 'Nomme-le']]} />
      <Sent top={465} t0={23.05} t1={24.3} words={[[23.05, '« Au secours »', ELEC]]} />
      <Sent top={385} t0={24.4} t1={26.6} words={[[24.4, 'Teste-le'], [24.6, 'avec'], [24.75, 'Maman', GRN]]} />
      <Stamp t0={25.2} text="PAS LE 112" color={RED} x={540} y={1380} size={60} rot={-5} />
    </Scene>

    {/* partage + abonnement */}
    <Scene t0={26.6} t1={MUET_TOTAL}>
      <Photo src="img_alerte.png" t0={26.6} t1={MUET_TOTAL + 0.5} dim={0.2} />
      <Sent top={290} t0={26.7} t1={MUET_TOTAL} words={[[26.7, 'Envoie ça']]} size={84} />
      <Sent top={395} t0={27.0} t1={MUET_TOTAL} words={[[27.0, 'à quelqu’un'], [27.2, 'qui vit seul', ELEC]]} size={70} />
      <Logo t0={27.6} />
    </Scene>

    {/* barre de progression + petits sons (pas de voix, pas de musique) */}
    <div style={{position: 'absolute', left: 0, top: 0, height: 8, width: `${(t / MUET_TOTAL) * 100}%`, background: ELEC, boxShadow: `0 0 20px ${ELEC}`}} />
    <Audio src={staticFile('sfx_muet.wav')} />
  </AbsoluteFill>;
};

// petit logo + pseudo, en bas à gauche de la zone sûre
const Logo: React.FC<{t0: number}> = ({t0}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 11);
  return <div style={{position: 'absolute', left: 80, top: 1290, display: 'flex', alignItems: 'center', gap: 22, transform: `scale(${k})`, transformOrigin: 'left center', opacity: Math.min(1, k * 1.5)}}>
    <Img src={staticFile('logo.png')} style={{width: 150, height: 150, filter: 'drop-shadow(0 0 25px rgba(110,80,255,0.7))'}} />
    <div style={{padding: '14px 30px', borderRadius: 40, background: 'rgba(10,12,40,0.6)', border: '2px solid rgba(90,200,255,0.7)', fontFamily: 'Pop', fontWeight: 700, fontSize: 44, color: '#fff'}}>@iphoneiceberg</div>
  </div>;
};
