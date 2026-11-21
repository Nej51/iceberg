import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {useT, sp, lin, Sent, Background, Glass, Icon, Scene, ZoomPhone, StepTag, Checklist, HiBox, Stamp, Pill, Photo, CallCard, Bubble, Glow, pick, fontCss, ELEC, RED, GRN, YEL, CoverTitle, EndScreen, Finish} from './lib';
// Vidéo « Isolement de la voix » pendant les appels, 21/11/2026.

// barres de son : voix (bleu) + bruit (rouge) qui disparaît à partir de tClean
const NoiseCard: React.FC<{t0: number; tClean: number; top: number}> = ({t0, tClean, top}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 13); const c = lin(t, tClean, tClean + 1.2);
  const N = 34;
  return <Glass style={{left: 140, top, width: 800, height: 360, transform: `scale(${k})`, opacity: Math.min(1, k * 1.5), overflow: 'hidden'}}>
    <div style={{position: 'absolute', left: 30, top: 22, fontFamily: 'Int', fontWeight: 600, fontSize: 30, color: c > 0.5 ? '#9fb6ff' : '#ff9a92'}}>{c > 0.5 ? 'ce que la personne entend : ta voix' : 'ce que la personne entend : tout'}</div>
    {Array.from({length: N}).map((_, i) => {
      const voice = 0.35 + 0.65 * Math.abs(Math.sin(t * 3.1 + i * 0.45)) * Math.exp(-Math.pow((i - N / 2) / 9, 2));
      const noise = Math.abs(Math.sin(t * 17 + i * 2.9) * Math.cos(t * 11 + i * 1.7));
      const h = 30 + 180 * (voice * 0.6 + noise * 0.8 * (1 - c));
      const col = noise * (1 - c) > voice * 0.5 ? RED : ELEC;
      return <div key={i} style={{position: 'absolute', left: 40 + i * 21.5, top: 210 - h / 2, width: 12, height: h, borderRadius: 6, background: col, boxShadow: `0 0 14px ${col}`}} />;
    })}
  </Glass>;
};
// glissement du doigt depuis le coin haut droit (coordonnées écran 600x1300)
const Swipe: React.FC<{t0: number; scale?: number}> = ({t0, scale = 1}) => {
  const t = useT(); const p = lin(t, t0, t0 + 0.9); if (t < t0 || t > t0 + 1.4) return null; const o = 1 - lin(t, t0 + 1.0, t0 + 1.4);
  const x = 540, y = 30 + 420 * (1 - Math.pow(1 - p, 2));
  return <>
    <div style={{position: 'absolute', left: (x - 4) * scale, top: 30 * scale, width: 8 * scale, height: (y - 30) * scale, borderRadius: 4 * scale, background: 'linear-gradient(180deg,transparent,rgba(120,160,255,0.9))', opacity: o}} />
    <div style={{position: 'absolute', left: (x - 34) * scale, top: (y - 34) * scale, width: 68 * scale, height: 68 * scale, borderRadius: '50%', background: 'rgba(255,255,255,0.75)', border: `${4 * scale}px solid #fff`, boxShadow: `0 0 ${30 * scale}px ${ELEC}`, opacity: o}} />
  </>;
};
const VsCard: React.FC<{t0: number; y: number; x: number; title: string; sub: string; color: string; icon: string}> = ({t0, y, x, title, sub, color, icon}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12);
  return <Glass style={{left: x, top: y, width: 380, height: 430, transform: `scale(${k})`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 18, border: `3px solid ${color}`, boxShadow: `0 0 40px ${color}66`}}>
    <Img src={staticFile(icon)} style={{width: 170, height: 170, filter: 'drop-shadow(0 16px 20px rgba(0,0,0,0.5))'}} />
    <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 52, color: '#fff'}}>{title}</div>
    <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 34, color}}>{sub}</div>
  </Glass>;
};

export const Video: React.FC = () => {
  const t = useT();
  const scr = pick(t, [[0, 'iv_call.png'], [24.4, 'iv_cc.png'], [30.2, 'iv_menu.png'], [38.06, 'iv_menu_on.png']]);
  const cur = t < 26.8 ? 1 : t < 31.8 ? 2 : t < 36.2 ? 3 : t < 38.3 ? 4 : 5;
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE : le résultat */}
    <Scene t0={0} t1={2.0}>
      <Photo src="img_bulle.png" t0={0} t1={2.3} dim={0.15} />
      <CoverTitle line="ON N’ENTEND PLUS QUE" keyword="TA VOIX" size={80} />
    </Scene>

    {/* ACCROCHE : la rue */}
    <Scene t0={2.0} t1={6.1}>
      <Photo src="img_bus.png" t0={2.0} t1={6.4} dim={0.25} />
      <Sent top={290} t0={2.0} t1={6.3} words={[[2.0, 'Un bus passe,'], [2.0, 'une sirène', RED]]} size={62} />
      <Sent top={380} t0={2.0} t1={6.3} words={[[2.66, 'et la personne'], [3.22, 'te répète…']]} size={58} />
      <Icon src="police_car_light_3d.png" t0={2.1} size={170} x={880} y={600} />
      <Bubble t0={4.12} y={1350} text="Quoi ? Je t'entends pas !" label="En face" />
    </Scene>

    {/* CONSÉQUENCE */}
    <Scene t0={6.1} t1={12.6}>
      <Sent top={290} t0={6.16} t1={8.15} words={[[6.16, 'Tu finis par'], [6.68, 'crier…', YEL]]} size={68} />
      <Sent top={380} t0={6.16} t1={8.15} words={[[7.0, 'ou par'], [7.36, 'raccrocher', RED]]} size={68} />
      <Sent top={290} t0={8.2} t1={12.8} words={[[8.2, 'alors que c’était'], [8.94, 'un appel'], [9.24, 'important', ELEC]]} size={60} />
      <CallCard t0={6.3} y={640} title="Appel terminé" sub="00:12" color={RED} />
      <Stamp t0={7.36} text="RACCROCHÉ" color={RED} x={540} y={960} size={58} />
      <Pill t0={10.12} x={540} y={1120} size={48}><Img src={staticFile('stethoscope_3d.png')} style={{width: 60, height: 60}} />ton médecin</Pill>
      <Pill t0={10.68} x={540} y={1250} size={48}>ton patron</Pill>
      <Pill t0={11.3} x={540} y={1380} size={48} border={YEL}>un recruteur</Pill>
    </Scene>

    {/* DÉCLIC */}
    <Scene t0={12.6} t1={20.1}>
      <Glow x={540} y={1000} r={320} color="#3b2cff" />
      <Sent top={290} t0={12.7} t1={17.25} words={[[12.82, 'Ton iPhone peut'], [13.74, 'effacer', ELEC]]} size={68} />
      <Sent top={385} t0={12.7} t1={17.25} words={[[13.98, 'presque tous les bruits'], [15.28, 'autour de toi']]} size={50} />
      <NoiseCard t0={12.9} tClean={13.9} top={600} />
      <Pill t0={16.38} x={540} y={1080} size={44}><Img src={staticFile('key_3d.png')} style={{width: 56, height: 56}} />un réglage bien caché</Pill>
      <Sent top={1200} t0={17.85} t1={20.2} words={[[17.9, 'Rassure-toi :'], [18.6, '5 secondes', GRN]]} size={62} />
      <Icon src="studio_microphone_3d.png" t0={18.6} size={220} x={540} y={1450} />
    </Scene>

    {/* ÉTAPES */}
    <Scene t0={20.1} t1={40.0}>
      <StepTag n={Math.min(cur, 4)} t0={[20.2, 26.82, 31.82, 36.18][Math.min(cur, 4) - 1]} />
      <Checklist cur={cur} t0={20.3} />
      <Sent top={400} t0={20.9} t1={23.9} words={[[21.06, 'Pendant un appel,'], [21.96, 'glisse depuis', ELEC]]} size={52} />
      <Sent top={470} t0={20.9} t1={23.9} words={[[23.02, 'le coin en haut à droite']]} size={50} />
      <Sent top={400} t0={23.95} t1={26.8} words={[[24.0, 'Le'], [24.38, 'centre de contrôle', ELEC]]} size={58} />
      <Sent top={470} t0={23.95} t1={26.8} words={[[24.6, 's’ouvre']]} size={52} />
      <Sent top={400} t0={27.4} t1={31.8} words={[[27.4, 'Tout en haut,'], [28.44, 'touche la pastille']]} size={52} />
      <Sent top={470} t0={27.4} t1={31.8} words={[[29.32, 'orange', '#FF8A00'], [29.64, '« Téléphone »', '#FF8A00']]} size={56} />
      <Sent top={400} t0={32.5} t1={36.2} words={[[32.9, 'Descends jusqu’à']]} size={54} />
      <Sent top={470} t0={32.5} t1={36.2} words={[[33.7, '« Audio et vidéo »', ELEC]]} size={58} />
      <Sent top={400} t0={36.8} t1={40.2} words={[[37.14, 'Choisis']]} size={54} />
      <Sent top={470} t0={36.8} t1={40.2} words={[[37.42, '« Isolement de la voix »', GRN]]} size={54} />
      <ZoomPhone src={scr} t0={20.15} keys={[[20.2, 1, 300, 650], [21.9, 1.5, 420, 360], [24.4, 1, 300, 650], [28.2, 1.8, 300, 200], [30.2, 1, 300, 650], [33.2, 1.6, 300, 470], [36.5, 1.7, 360, 760], [38.6, 1.3, 360, 700]]}>
        <Swipe t0={22.1} />
        <HiBox sx={300} sy={107} w={380} h={58} t0={28.8} t1={30.2} />
        <HiBox sx={300} sy={400} w={500} h={62} t0={33.7} t1={36.2} />
        <HiBox sx={408} sy={799} w={256} h={68} t0={37.42} t1={38.06} />
      </ZoomPhone>
      <Stamp t0={38.3} text="ACTIVÉ !" color={GRN} x={760} y={1420} size={60} rot={-7} />
    </Scene>

    {/* RÉSULTAT */}
    <Scene t0={40.0} t1={43.7}>
      <Photo src="img_cafe.png" t0={40.0} t1={44.0} dim={0.2} />
      <Sent top={290} t0={40.1} t1={43.9} words={[[40.1, 'Et voilà :', GRN], [40.6, 'on n’entend plus']]} size={58} />
      <Sent top={380} t0={40.1} t1={43.9} words={[[41.16, 'que toi', ELEC], [41.84, 'même dans le bruit']]} size={58} />
    </Scene>

    {/* PARTAGE */}
    <Scene t0={43.7} t1={47.6}>
      <Glow x={540} y={950} r={300} color="#4a2cff" />
      <Sent top={290} t0={43.76} t1={47.8} words={[[43.76, 'Quelqu’un t’appelle'], [44.84, 'toujours']]} size={58} />
      <Sent top={380} t0={43.76} t1={47.8} words={[[45.04, 'depuis un endroit'], [45.6, 'bruyant ?', YEL]]} size={58} />
      <Icon src="mobile_phone_with_arrow_3d.png" t0={46.0} size={340} x={540} y={940} />
      <Pill t0={46.22} x={540} y={1250} size={50} border={ELEC}>Envoie-lui cette vidéo</Pill>
    </Scene>

    {/* PRÉCISION */}
    <Scene t0={47.6} t1={55.8}>
      <Sent top={290} t0={47.7} t1={51.35} words={[[47.7, 'Petite'], [47.98, 'précision', YEL]]} size={70} />
      <Sent top={390} t0={48.7} t1={51.35} words={[[48.86, 'ça améliore'], [49.16, 'TA voix', GRN]]} size={58} />
      {t < 51.4 && <>
      <VsCard t0={49.3} x={110} y={620} title="Toi" sub="voix nette" color={GRN} icon="studio_microphone_3d.png" />
      <VsCard t0={50.2} x={590} y={620} title="En face" sub="ne change pas" color="#9aa0b8" icon="telephone_receiver_3d.png" />
      </>}
      <Sent top={290} t0={51.4} t1={56.0} words={[[51.46, 'Le réglage'], [51.84, 'reste activé', GRN]]} size={62} />
      <Sent top={385} t0={51.4} t1={56.0} words={[[52.46, 'pour tes prochains appels']]} size={50} />
      {t >= 51.4 && <>
        <Icon src="check_mark_button_3d.png" t0={52.0} size={230} x={540} y={1170} />
        <Pill t0={54.34} x={330} y={1420} size={48}>FaceTime</Pill>
        <Pill t0={54.84} x={760} y={1420} size={48} border={GRN}>WhatsApp</Pill>
      </>}
    </Scene>

    {/* QUESTION */}
    <Scene t0={55.8} t1={57.94}>
      <Sent top={330} t0={55.9} t1={58.1} words={[[55.9, 'Tu le connaissais,'], [56.78, 'ce réglage ?', ELEC]]} size={66} />
      <Icon src="speech_balloon_3d.png" t0={56.4} size={320} x={540} y={920} />
    </Scene>

    <EndScreen t0={57.94} t1={60.16} tEnd={62.6} tAbonne={60.5} tPour={60.86} tImmergee={61.66} />
    <Finish total={63.4} />
  </AbsoluteFill>;
};
