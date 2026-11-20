import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import data from './data.json';
import {useT, sp, lin, Sent, Background, Glass, Icon, Scene, Phone, HiBox, ZoomPhone, StepTag, Checklist, Stamp, Pill, Photo, Glow, pick, fontCss, ELEC, RED, GRN, YEL, CoverTitle, EndScreen, Finish} from './lib';
const P: any = data;
// Vidéo « Avant de prêter ton iPhone » (Accès guidé), 20/11/2026.

// déclic : grille d'apps qui s'éteignent sauf une, cadenas dessus
const AppGrid: React.FC<{t0: number}> = ({t0}) => {
  const t = useT(); const cols = ['#FF453A', '#FF9F0A', '#FFD60A', '#34C759', '#2F5BFF', '#5E5CE6', '#BF5AF2', '#FF375F', '#64D2FF'];
  return <Glass style={{left: 190, top: 900, width: 700, height: 560}}>
    {cols.map((c, i) => { const keep = i === 4; const k = sp(t, t0 + 0.1 * i, 12); const off = keep ? 0 : lin(t, t0 + 1.0 + 0.12 * i, t0 + 1.3 + 0.12 * i);
      const x = 95 + (i % 3) * 190, y = 50 + Math.floor(i / 3) * 165;
      return <div key={i} style={{position: 'absolute', left: x, top: y, width: 130, height: 130, borderRadius: 34, background: c, transform: `scale(${k * (keep ? 1 + 0.12 * lin(t, t0 + 2.2, t0 + 2.6) : 1 - 0.15 * off)})`,
        opacity: 1 - 0.8 * off, filter: off > 0 ? `grayscale(${off})` : undefined, boxShadow: keep && t > t0 + 2.2 ? `0 0 50px ${ELEC}` : '0 10px 30px rgba(0,0,0,0.4)'}} />; })}
    <Icon src="locked_3d.png" t0={t0 + 2.4} size={130} x={350} y={140} />
  </Glass>;
};
// bouton latéral qui s'allume + compteur ×1 ×2 ×3
const SideBtn: React.FC<{x: number; y: number; taps: number[]}> = ({x, y, taps}) => {
  const t = useT(); if (t < taps[0] - 0.3) return null; const n = taps.filter((a) => t >= a).length; const flash = taps.some((a) => t >= a && t < a + 0.15);
  return <>
    <div style={{position: 'absolute', left: x, top: y, width: 16, height: 120, borderRadius: 8, background: flash ? '#fff' : ELEC, boxShadow: `0 0 ${flash ? 50 : 25}px ${ELEC}`}} />
    {n > 0 && <div style={{position: 'absolute', left: x + 40, top: y + 20, fontFamily: 'Pop', fontWeight: 700, fontSize: 80, color: '#fff', textShadow: `0 0 30px ${ELEC}`, transform: `scale(${1 + (flash ? 0.25 : 0)})`}}>×{n}</div>}
  </>;
};

const R = P['reg:Accessibilité'], A = P['acc:Accès guidé'], AT = P['ag:Accès guidé:tog'], AC = P['ag:Réglages des codes'], CD = P["codes:Définir le code d'Accès guidé"];
const DM = P['sess:Démarrer'], FN = P['sess:Fin'], OT = P['opts:tog'], SR = P['sess:reglages'];

export const Video: React.FC = () => {
  const t = useT();
  const s1 = pick(t, [[0, 'ag_reg.png'], [17.9, 'ag_reg_hi.png'], [18.3, 'ag_acc.png'], [20.5, 'ag_acc_hi.png']]);
  const padN = Math.min(6, Math.max(0, Math.floor((t - 24.25) / 0.1) + 1));
  const s2 = pick(t, [[0, 'ag_off.png'], [22.3, 'ag_on.png'], [23.3, 'ag_on_hi.png'], [23.6, 'ag_codes.png'], [24.0, 'ag_codes_hi.png'], [24.2, `ag_pad${t >= 24.25 ? padN : 0}.png`]]);
  const padD = Math.min(6, Math.max(0, Math.floor((t - 45.05) / 0.15) + 1));
  const s3 = pick(t, [[0, 'ag_photo.png'], [32.3, 'ag_start.png'], [33.3, 'ag_photo_on.png']]);
  const s4 = pick(t, [[0, 'ag_photo.png'], [44.2, `ag_padd${t >= 45.05 ? padD : 0}.png`], [45.9, 'ag_fin.png'], [46.15, 'ag_photo_off.png']]);
  const s5 = pick(t, [[0, 'ag_start.png'], [47.8, 'ag_opts.png'], [49.2, 'ag_opts_on.png']]);
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* ACCROCHE */}
    <Scene t0={0} t1={4.9}>
      <Photo src="img_tend.png" t0={0} t1={5} dim={0.15} />
      <CoverTitle line="AVANT DE" keyword="PRÊTER" after="TON IPHONE" />
      <Sent top={300} t0={2.0} t1={2.9} words={[[2.0, 'pour montrer'], [2.05, 'UNE', YEL], [2.1, 'photo…']]} size={84} />
      <Sent top={300} t0={2.95} t1={5.2} words={[[2.98, 'et il commence'], [4.3, 'à faire défiler', RED]]} size={80} />
    </Scene>

    {/* CONSÉQUENCE */}
    <Scene t0={5.0} t1={10.65}>
      <Photo src="img_defile.png" t0={5} t1={10.7} dim={0.25} />
      <Sent top={290} t0={5.05} t1={8.6} words={[[5.08, 'Tes autres'], [5.44, 'photos,', RED]]} size={80} />
      <Sent top={390} t0={5.05} t1={8.6} words={[[6.16, 'tes'], [6.28, 'messages…', RED], [7.64, 'tout y passe']]} size={64} />
      <Pill t0={6.3} x={540} y={1050} size={44}><Img src={staticFile('speech_balloon_3d.png')} style={{width: 64, height: 64}} />Nouveau message de Léa</Pill>
      <Sent top={290} t0={8.7} t1={10.9} words={[[8.76, 'Et toi, tu n’oses pas'], [9.68, 'le reprendre', YEL]]} size={72} />
    </Scene>

    {/* DÉCLIC */}
    <Scene t0={10.7} t1={16.6}>
      <Glow x={540} y={1100} r={320} color="#3b2cff" />
      <Pill t0={10.76} x={540} y={300}><Img src={staticFile('key_3d.png')} style={{width: 60, height: 60}} />le réglage caché</Pill>
      <Sent top={420} t0={10.8} t1={14.0} words={[[11.16, 'Il bloque ton iPhone'], [13.06, 'sur une seule app', ELEC]]} size={62} />
      <Sent top={420} t0={14.0} t1={16.8} words={[[13.96, 'Rassure-toi :'], [15.88, 'moins d’une minute', GRN]]} size={62} />
      <AppGrid t0={11.4} />
    </Scene>

    {/* ÉTAPE 1 */}
    <Scene t0={16.85} t1={21.1}>
      <StepTag n={1} t0={16.9} />
      <Checklist cur={1} t0={17.0} />
      <Sent top={390} t0={17.6} t1={19.9} words={[[17.72, 'Ouvre'], [17.9, 'Réglages', ELEC], [18.6, 'puis'], [18.64, 'Accessibilité', ELEC]]} size={58} />
      <Sent top={390} t0={19.9} t1={21.3} words={[[19.94, 'Descends jusqu’à'], [20.52, 'Accès guidé', ELEC]]} size={58} />
      <ZoomPhone src={s1} t0={17.0} keys={[[17.4, 1.6, 300, R[1]], [18.4, 1.5, 300, A[1] - 150], [19.9, 1.7, 300, A[1]]]}>
        <HiBox sx={300} sy={R[1]} w={556} h={72} t0={17.6} t1={18.35} />
        <HiBox sx={300} sy={A[1]} w={556} h={72} t0={20.4} />
      </ZoomPhone>
    </Scene>

    {/* ÉTAPE 2 */}
    <Scene t0={21.35} t1={26.05}>
      <StepTag n={2} t0={21.42} />
      <Checklist cur={2} t0={21.5} />
      <Sent top={390} t0={21.9} t1={22.8} words={[[22.08, 'Active'], [22.26, 'Accès guidé', GRN]]} size={60} />
      <Sent top={390} t0={22.85} t1={24.0} words={[[22.86, 'puis'], [23.08, 'Réglages des codes', ELEC]]} size={58} />
      <Sent top={390} t0={24.02} t1={25.1} words={[[24.04, 'Choisis un'], [24.66, 'code', ELEC]]} size={60} />
      <Sent top={390} t0={25.12} t1={26.3} words={[[25.14, 'Garde-le'], [25.56, 'pour toi', YEL]]} size={64} />
      <ZoomPhone src={s2} t0={21.5} keys={[[21.6, 1.7, 400, AT[1] + 40], [22.85, 1.6, 300, AC[1]], [23.6, 1.6, 300, CD[1] + 60], [24.15, 1, 300, 650]]}>
        <HiBox sx={AT[0]} sy={AT[1]} w={100} h={60} t0={21.9} t1={22.8} />
        <HiBox sx={300} sy={AC[1]} w={556} h={72} t0={22.9} t1={23.55} />
        <HiBox sx={300} sy={CD[1]} w={556} h={72} t0={23.65} t1={24.15} />
      </ZoomPhone>
    </Scene>

    {/* ÉTAPE 3 */}
    <Scene t0={26.4} t1={36.1}>
      <StepTag n={3} t0={26.46} />
      <Checklist cur={3} t0={26.55} />
      <Sent top={390} t0={27.0} t1={30.2} words={[[28.56, 'Ouvre la'], [28.88, 'photo', ELEC], [29.06, 'à montrer']]} size={60} />
      <Sent top={390} t0={30.25} t1={32.5} words={[[30.38, 'Appuie'], [30.7, '3 fois', YEL], [31.62, 'sur le bouton du côté']]} size={52} />
      <Sent top={390} t0={32.55} t1={33.35} words={[[32.66, 'Touche'], [32.84, 'Démarrer', ELEC]]} size={64} />
      <Sent top={390} t0={33.4} t1={34.9} words={[[33.4, 'On peut'], [34.36, 'regarder…', GRN]]} size={64} />
      <Sent top={390} t0={34.92} t1={36.3} words={[[34.94, 'mais plus'], [35.44, 'sortir de l’app', RED]]} size={60} />
      <Phone src={s3} x={540} top={540} w={520} t0={26.6} float={t < 30 || t > 33.3}>
        <HiBox sx={DM[0]} sy={DM[1]} w={DM[2] + 20} h={64} t0={32.4} t1={33.3} />
      </Phone>
      <SideBtn x={804} y={800} taps={[30.7, 30.9, 31.1]} />
      <Stamp t0={35.4} text="IMPOSSIBLE DE SORTIR" color={RED} x={540} y={1180} size={46} />
    </Scene>

    {/* PARTAGE */}
    <Scene t0={36.6} t1={40.9}>
      <Photo src="img_enfant.png" t0={36.6} t1={41} dim={0.2} />
      <Sent top={290} t0={36.65} t1={41.2} words={[[36.68, 'Quelqu’un prête souvent']]} size={58} />
      <Sent top={370} t0={36.65} t1={41.2} words={[[37.96, 'son téléphone aux'], [38.58, 'enfants ?', YEL]]} size={58} />
      <Pill t0={39.14} x={540} y={1330} size={50}><Img src={staticFile('mobile_phone_with_arrow_3d.png')} style={{width: 70, height: 70}} />Envoie-lui cette vidéo</Pill>
    </Scene>

    {/* ÉTAPE 4 */}
    <Scene t0={41.35} t1={46.4}>
      <StepTag n={4} t0={41.42} />
      <Checklist cur={t < 46.1 ? 4 : 5} t0={41.5} />
      <Sent top={390} t0={41.9} t1={43.1} words={[[42.02, 'Quand on te le'], [42.34, 'rend', ELEC]]} size={62} />
      <Sent top={390} t0={43.12} t1={45.0} words={[[43.14, 'Appuie à nouveau'], [43.5, '3 fois', YEL]]} size={60} />
      <Sent top={390} t0={45.02} t1={46.6} words={[[45.08, 'et tape ton'], [45.34, 'code', ELEC]]} size={64} />
      <Phone src={s4} x={540} top={540} w={520} t0={41.5} float={false}>
        <HiBox sx={FN[0]} sy={FN[1]} w={FN[2] + 20} h={64} t0={45.9} t1={46.15} />
      </Phone>
      <SideBtn x={804} y={800} taps={[43.5, 43.7, 43.9]} />
      <Stamp t0={46.1} text="DÉBLOQUÉ !" color={GRN} x={540} y={1250} size={60} />
    </Scene>

    {/* BONUS */}
    <Scene t0={46.75} t1={51.9}>
      <Pill t0={46.82} x={540} y={300} size={46}><Img src={staticFile('check_mark_button_3d.png')} style={{width: 56, height: 56}} />Petit bonus</Pill>
      <Sent top={400} t0={47.6} t1={49.2} words={[[47.62, 'Dans'], [47.7, '« Réglages de session »', ELEC]]} size={52} />
      <Sent top={400} t0={49.2} t1={52.1} words={[[49.22, 'ajoute une'], [49.22, 'limite de temps', YEL]]} size={56} />
      <ZoomPhone src={s5} t0={46.9} keys={[[47.6, 1.5, 450, SR[1]], [48.0, 1.5, 300, OT[1] + 40]]}>
        <HiBox sx={SR[0]} sy={SR[1]} w={SR[2] + 10} h={66} t0={47.62} t1={47.95} />
        <HiBox sx={300} sy={OT[1]} w={556} h={72} t0={48.6} />
      </ZoomPhone>
    </Scene>

    {/* QUESTION */}
    <Scene t0={52.3} t1={55.9}>
      <Glow x={540} y={900} r={300} color="#3b2cff" />
      <Sent top={300} t0={52.3} t1={56.2} words={[[52.38, 'Et toi, tu prêtes'], [53.06, 'ton iPhone…']]} size={70} />
      <Pill t0={53.4} x={330} y={760} size={52} border={GRN}>facilement</Pill>
      <Pill t0={54.3} x={760} y={900} size={52} border={RED}>jamais !</Pill>
      <Icon src="speech_balloon_3d.png" t0={54.5} size={260} x={540} y={1130} />
      <Pill t0={54.84} x={540} y={1360} size={48} border={YEL}>Dis-le en commentaire</Pill>
    </Scene>

    <EndScreen t0={56.15} t1={58.5} tEnd={60.6} tAbonne={58.6} tPour={59.02} tImmergee={59.86} />
    <Finish total={61.6} />
  </AbsoluteFill>;
};
