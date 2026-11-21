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
  const scr = pick(t, [[0, 'iv_call.png'], [11.8, 'iv_cc.png'], [18.2, 'iv_menu.png'], [25.64, 'iv_menu_on.png']]);
  const cur = t < 14.1 ? 1 : t < 19.36 ? 2 : t < 22.72 ? 3 : t < 26.0 ? 4 : 5;
  const st = Math.min(cur, 4);
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE + HOOK */}
    <Scene t0={0} t1={2.0}>
      <Photo src="img_bulle.png" t0={0} t1={2.3} dim={0.15} />
      <CoverTitle line="ON N’ENTEND PLUS QUE" keyword="TA VOIX" size={80} />
    </Scene>
    <Scene t0={2.0} t1={6.4}>
      <Photo src="img_bus.png" t0={2.0} t1={6.7} dim={0.25} />
      <Sent top={290} t0={2.0} t1={3.35} words={[[2.0, 'On t’entend mal'], [2.5, 'dans le bruit ?', RED]]} size={60} />
      <Sent top={290} t0={3.4} t1={6.6} words={[[3.4, 'Ton iPhone'], [4.0, 'efface', ELEC]]} size={72} />
      <Sent top={385} t0={3.4} t1={6.6} words={[[4.3, 'presque tous'], [4.82, 'les bruits']]} size={60} />
      <Icon src="police_car_light_3d.png" t0={2.1} size={170} x={880} y={620} />
      <Pill t0={5.7} x={540} y={1330} size={56} border={GRN}>en 5 secondes</Pill>
    </Scene>

    {/* ÉTAPES */}
    <Scene t0={6.4} t1={27.1}>
      <StepTag n={st} t0={[6.42, 14.1, 19.36, 22.72][st - 1]} />
      <Checklist cur={cur} t0={6.6} />
      <Sent top={400} t0={7.8} t1={11.0} words={[[7.88, 'Pendant l’appel,'], [8.74, 'glisse depuis', ELEC]]} size={52} />
      <Sent top={470} t0={7.8} t1={11.0} words={[[9.84, 'le coin en haut à droite']]} size={50} />
      <Sent top={400} t0={11.05} t1={14.1} words={[[11.05, 'Le'], [11.4, 'centre de contrôle', ELEC]]} size={58} />
      <Sent top={470} t0={11.05} t1={14.1} words={[[11.8, 's’ouvre']]} size={52} />
      <Sent top={400} t0={15.2} t1={19.36} words={[[15.22, 'Tout en haut,'], [15.96, 'touche la pastille']]} size={52} />
      <Sent top={470} t0={15.2} t1={19.36} words={[[16.7, 'orange', '#FF8A00'], [17.28, '« Téléphone »', '#FF8A00']]} size={56} />
      <Sent top={400} t0={20.6} t1={22.72} words={[[20.66, 'Descends jusqu’à']]} size={54} />
      <Sent top={470} t0={20.6} t1={22.72} words={[[21.54, '« Audio et vidéo »', ELEC]]} size={58} />
      <Sent top={400} t0={24.5} t1={27.3} words={[[24.52, 'Choisis']]} size={54} />
      <Sent top={470} t0={24.5} t1={27.3} words={[[24.98, '« Isolement de la voix »', GRN]]} size={54} />
      <ZoomPhone src={scr} t0={6.45} keys={[[6.5, 1, 300, 650], [8.6, 1.5, 420, 360], [11.6, 1, 300, 650], [15.3, 1.8, 300, 200], [18.2, 1, 300, 650], [20.6, 1.6, 300, 470], [23.2, 1.7, 360, 760], [26.4, 1.3, 360, 700]]}>
        <Swipe t0={8.8} />
        <HiBox sx={300} sy={107} w={380} h={58} t0={16.2} t1={18.2} />
        <HiBox sx={300} sy={400} w={500} h={62} t0={21.5} t1={22.72} />
        <HiBox sx={408} sy={799} w={256} h={68} t0={24.98} t1={25.64} />
      </ZoomPhone>
      <Stamp t0={26.0} text="ACTIVÉ !" color={GRN} x={760} y={1420} size={60} rot={-7} />
    </Scene>

    {/* RÉSULTAT */}
    <Scene t0={27.1} t1={30.1}>
      <Photo src="img_cafe.png" t0={27.1} t1={30.4} dim={0.2} />
      <Sent top={290} t0={27.2} t1={30.3} words={[[27.22, 'Et voilà :', GRN], [28.0, 'on n’entend plus']]} size={58} />
      <Sent top={380} t0={27.2} t1={30.3} words={[[28.72, 'que toi', ELEC], [29.22, 'même dans le bruit']]} size={58} />
    </Scene>

    {/* COMMENT ÇA MARCHE */}
    <Scene t0={30.1} t1={37.45}>
      <Glow x={540} y={900} r={320} color="#3b2cff" />
      <Pill t0={30.18} x={540} y={300} size={46}><Img src={staticFile('studio_microphone_3d.png')} style={{width: 60, height: 60}} />Comment ça marche ?</Pill>
      <Sent top={390} t0={31.85} t1={37.6} words={[[31.88, 'Il reconnaît'], [32.84, 'ta voix', ELEC]]} size={62} />
      <Sent top={475} t0={31.85} t1={37.6} words={[[33.46, 'et'], [33.54, 'efface', ELEC], [33.76, 'le reste']]} size={52} />
      <NoiseCard t0={30.4} tClean={33.54} top={600} />
      <Pill t0={35.28} x={300} y={1100} size={44} border={RED}>les voitures</Pill>
      <Pill t0={36.02} x={760} y={1100} size={44} border={RED}>le vent</Pill>
      <Pill t0={36.48} x={540} y={1230} size={44} border={RED}>les gens autour</Pill>
    </Scene>

    {/* PIÈGE */}
    <Scene t0={37.45} t1={46.0}>
      <Sent top={290} t0={37.5} t1={42.4} words={[[37.56, 'Attention,'], [38.5, 'un piège', RED]]} size={68} />
      <Sent top={385} t0={39.4} t1={42.4} words={[[39.44, 'ça améliore'], [39.96, 'TA voix', GRN]]} size={56} />
      <Sent top={290} t0={42.44} t1={46.2} words={[[42.44, 'Tu l’entends mal ?']]} size={64} />
      <Sent top={385} t0={42.44} t1={46.2} words={[[43.96, 'c’est à elle'], [44.34, 'de l’activer', YEL]]} size={56} />
      <VsCard t0={39.44} x={110} y={620} title="Toi" sub="voix nette" color={GRN} icon="studio_microphone_3d.png" />
      <VsCard t0={40.86} x={590} y={620} title="En face" sub="ne change pas" color="#9aa0b8" icon="telephone_receiver_3d.png" />
    </Scene>

    {/* BONUS */}
    <Scene t0={46.0} t1={51.7}>
      <Glow x={540} y={1000} r={300} color="#2c8a4a" />
      <Sent top={290} t0={46.1} t1={51.9} words={[[46.16, 'Bonne nouvelle', GRN]]} size={72} />
      <Sent top={385} t0={47.2} t1={51.9} words={[[47.28, 'il reste activé'], [48.08, 'pour tes prochains appels']]} size={48} />
      <Icon src="check_mark_button_3d.png" t0={47.6} size={260} x={540} y={830} />
      <Pill t0={49.74} x={330} y={1150} size={50}>FaceTime</Pill>
      <Pill t0={50.28} x={760} y={1150} size={50} border={GRN}>WhatsApp</Pill>
      <Pill t0={50.62} x={540} y={1290} size={40} border="#FF8A00">même pastille</Pill>
    </Scene>

    {/* PARTAGE */}
    <Scene t0={51.7} t1={55.95}>
      <Glow x={540} y={950} r={300} color="#4a2cff" />
      <Sent top={290} t0={51.8} t1={56.1} words={[[51.8, 'Quelqu’un t’appelle'], [52.8, 'toujours']]} size={58} />
      <Sent top={380} t0={51.8} t1={56.1} words={[[53.04, 'depuis un endroit'], [53.62, 'bruyant ?', YEL]]} size={58} />
      <Icon src="mobile_phone_with_arrow_3d.png" t0={54.0} size={340} x={540} y={940} />
      <Pill t0={54.24} x={540} y={1250} size={50} border={ELEC}>Envoie-lui cette vidéo</Pill>
    </Scene>

    <EndScreen t0={55.95} t1={58.3} tEnd={60.9} tAbonne={58.6} tPour={59.06} tImmergee={60.02} />
    <Finish total={61.8} />
  </AbsoluteFill>;
};
