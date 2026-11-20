import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import data from './data.json';
import {useT, sp, lin, Sent, Background, Glass, Icon, Scene, HiBox, ZoomPhone, StepTag, Checklist, Stamp, Pill, Photo, Glow, pick, fontCss, ELEC, RED, GRN, YEL, CoverTitle, EndScreen, Finish} from './lib';
const P: any = data;
// Vidéo « Ton iPhone est illisible ? » (Liquid Glass, contraste, transparence), 20/11/2026.

// déclic : un texte flou qui devient net
const Sharpen: React.FC<{t0: number}> = ({t0}) => {
  const t = useT(); const k = sp(t, t0, 14); const b = 18 * (1 - lin(t, t0 + 1.2, t0 + 2.6));
  return <Glass style={{left: 140, top: 900, width: 800, height: 420, transform: `scale(${k})`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 18}}>
    <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 96, color: '#fff', filter: `blur(${b}px)`, opacity: 0.45 + 0.55 * (1 - b / 18)}}>Notification</div>
    <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 40, color: 'rgba(220,225,255,0.9)', filter: `blur(${b}px)`}}>Ton colis arrive demain</div>
  </Glass>;
};
const Compare: React.FC<{t0: number}> = ({t0}) => {
  const t = useT(); const k = sp(t, t0, 14);
  return <div style={{position: 'absolute', left: 120, top: 640, width: 840, transform: `scale(${k})`, opacity: Math.min(1, k * 1.5)}}>
    <Img src={staticFile('img_lg_compare.png')} style={{width: 840, borderRadius: 40, boxShadow: '0 30px 80px rgba(0,0,0,0.6)', border: '1.5px solid rgba(255,255,255,0.22)'}} />
    <div style={{position: 'absolute', left: 60, top: -30}}><Pill t0={t0 + 0.3} x={150} y={0} size={40} border={GRN}>Teinté</Pill></div>
    <div style={{position: 'absolute', left: 460, top: -30}}><Pill t0={t0 + 0.5} x={170} y={0} size={40} border={RED}>Transparent</Pill></div>
  </div>;
};

const RA = P['reg:Apparence'], RC = P['reg:Accessibilité'], LG = P['app:Liquid Glass'], SL = P['lg:slider'], TE = P['lg:teinte'];
const AF = P['acc:Affichage et taille du texte'], CT = P['aff:Augmenter le contraste:tog'], TT = P['aff:Réduire la transparence:tog'];

export const Video: React.FC = () => {
  const t = useT();
  const sl = Math.min(4, Math.max(0, Math.floor((t - 20.6) / 0.25)));
  const s1 = pick(t, [[0, 'lg_reg.png'], [17.9, 'lg_reg_hi_app.png'], [18.3, 'lg_app.png'], [19.2, 'lg_app_hi.png'], [19.6, `lg_slider${t >= 20.6 ? sl : 0}.png`]]);
  const s2 = pick(t, [[0, 'lg_reg.png'], [26.3, 'lg_reg_hi_acc.png'], [26.65, 'lg_acc.png'], [27.6, 'lg_acc_hi.png'], [28.1, 'lg_aff.png']]);
  const s3 = pick(t, [[0, 'lg_aff.png'], [30.5, 'lg_aff_hi_c.png'], [31.2, 'lg_aff_c.png']]);
  const s4 = pick(t, [[0, 'lg_aff_c.png'], [43.7, 'lg_aff_hi_t.png'], [44.25, 'lg_aff_ct.png']]);
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* ACCROCHE */}
    <Scene t0={0} t1={4.5}>
      <Photo src="img_lg2.png" t0={0} t1={4.6} dim={0.15} />
      <CoverTitle line="TON IPHONE EST" keyword="ILLISIBLE ?" />
      <Sent top={300} t0={2.0} t1={4.8} words={[[2.0, 'Le texte se'], [3.46, 'mélange', RED], [3.7, 'au fond']]} size={80} />
    </Scene>

    {/* CONSÉQUENCE */}
    <Scene t0={4.7} t1={12.2}>
      <Photo src="img_lg1.png" t0={4.7} t1={12.3} dim={0.25} />
      <Sent top={290} t0={4.8} t1={8.4} words={[[4.94, 'Tu plisses les'], [5.44, 'yeux', YEL]]} size={80} />
      <Sent top={390} t0={4.8} t1={8.4} words={[[5.84, 'luminosité à fond…'], [7.2, 'batterie vidée', RED]]} size={58} />
      <Sent top={290} t0={8.5} t1={12.4} words={[[8.56, 'Ce n’est pas ta'], [9.34, 'vue', YEL]]} size={80} />
      <Sent top={390} t0={8.5} t1={12.4} words={[[9.98, 'l’iPhone est devenu'], [11.4, 'transparent', ELEC]]} size={58} />
    </Scene>

    {/* DÉCLIC */}
    <Scene t0={12.3} t1={16.2}>
      <Glow x={540} y={1100} r={320} color="#3b2cff" />
      <Pill t0={12.4} x={540} y={300}><Img src={staticFile('key_3d.png')} style={{width: 60, height: 60}} />4 réglages cachés</Pill>
      <Sent top={420} t0={12.5} t1={16.4} words={[[12.54, 'Rassure-toi :'], [14.9, 'un écran'], [15.26, 'bien net', GRN]]} size={66} />
      <Sharpen t0={13.0} />
    </Scene>

    {/* ÉTAPE 1 */}
    <Scene t0={16.4} t1={22.2}>
      <StepTag n={1} t0={16.5} />
      <Checklist cur={1} t0={16.6} />
      <Sent top={390} t0={17.2} t1={18.95} words={[[17.36, 'Ouvre'], [17.6, 'Réglages', ELEC], [18.04, 'puis'], [18.34, 'Apparence', ELEC]]} size={60} />
      <Sent top={390} t0={19.0} t1={20.35} words={[[19.0, 'Touche'], [19.18, 'Liquid Glass', ELEC]]} size={64} />
      <Sent top={390} t0={20.4} t1={22.4} words={[[20.42, 'Glisse vers'], [21.64, 'Teinté', GRN]]} size={66} />
      <ZoomPhone src={s1} t0={16.6} keys={[[17.4, 1.6, 300, RA[1] + 100], [18.5, 1.5, 300, LG[1] - 100], [19.6, 1.7, 360, SL[1]]]}>
        <HiBox sx={300} sy={RA[1]} w={556} h={72} t0={17.7} t1={18.35} />
        <HiBox sx={300} sy={LG[1] - 30} w={556} h={72} t0={19.0} t1={19.6} />
        <HiBox sx={TE[0] + 20} sy={TE[1]} w={110} h={64} t0={20.4} />
      </ZoomPhone>
    </Scene>
    <Scene t0={22.25} t1={24.5}>
      <StepTag n={1} t0={16.5} />
      <Checklist cur={1} t0={16.6} />
      <Sent top={390} t0={22.25} t1={24.8} words={[[22.3, 'Menus plus'], [23.8, 'lisibles', GRN]]} size={66} />
      <Compare t0={22.3} />
    </Scene>

    {/* ÉTAPE 2 */}
    <Scene t0={24.85} t1={29.3}>
      <StepTag n={2} t0={24.94} />
      <Checklist cur={2} t0={25.0} />
      <Sent top={390} t0={25.6} t1={26.5} words={[[25.7, 'Reviens dans'], [26.0, 'Réglages', ELEC]]} size={62} />
      <Sent top={390} t0={26.55} t1={27.3} words={[[26.56, 'Ouvre'], [26.68, 'Accessibilité', ELEC]]} size={62} />
      <Sent top={390} t0={27.32} t1={29.5} words={[[27.32, 'puis'], [27.6, '« Affichage et taille', ELEC]]} size={54} />
      <Sent top={465} t0={27.32} t1={29.5} words={[[28.24, 'du texte »', ELEC]]} size={54} />
      <ZoomPhone src={s2} t0={25.0} keys={[[25.8, 1.6, 300, RC[1] + 120], [26.7, 1.6, 300, AF[1] + 100], [28.2, 1, 300, 650]]}>
        <HiBox sx={300} sy={RC[1]} w={556} h={72} t0={26.0} t1={26.65} />
        <HiBox sx={300} sy={AF[1]} w={556} h={72} t0={27.4} t1={28.1} />
      </ZoomPhone>
    </Scene>

    {/* ÉTAPE 3 */}
    <Scene t0={29.5} t1={36.8}>
      <StepTag n={3} t0={29.6} />
      <Checklist cur={3} t0={29.7} />
      <Sent top={390} t0={30.2} t1={32.3} words={[[30.42, 'Active'], [30.64, '« Augmenter le contraste »', ELEC]]} size={50} />
      <Sent top={390} t0={32.35} t1={34.3} words={[[32.4, 'Les textes'], [33.5, 'ressortent', GRN]]} size={64} />
      <Sent top={390} t0={34.35} t1={37.0} words={[[34.38, 'Vu par'], [35.08, 'des millions', YEL], [35.88, 'sur TikTok']]} size={58} />
      <ZoomPhone src={s3} t0={29.7} keys={[[30.2, 1.7, 360, CT[1]], [32.3, 1.2, 300, 520]]}>
        <HiBox sx={CT[0]} sy={CT[1]} w={100} h={60} t0={30.6} t1={32.3} />
      </ZoomPhone>
    </Scene>

    {/* PARTAGE */}
    <Scene t0={37.3} t1={41.7}>
      <Glow x={540} y={950} r={300} color="#4a2cff" />
      <Sent top={290} t0={37.35} t1={41.9} words={[[37.44, 'Quelqu’un ne voit'], [38.64, 'plus rien', RED]]} size={54} />
      <Sent top={385} t0={37.35} t1={41.9} words={[[39.1, 'sur son iPhone ?']]} size={54} />
      <Icon src="mobile_phone_with_arrow_3d.png" t0={39.9} size={330} x={540} y={950} />
      <Pill t0={40.0} x={540} y={1280} size={50}>Envoie-lui cette vidéo</Pill>
    </Scene>

    {/* ÉTAPE 4 */}
    <Scene t0={42.2} t1={49.1}>
      <StepTag n={4} t0={42.28} />
      <Checklist cur={t < 44.3 ? 4 : 5} t0={42.4} />
      <Sent top={390} t0={43.0} t1={45.3} words={[[43.7, 'Active'], [43.9, '« Réduire la transparence »', ELEC]]} size={48} />
      <Sent top={390} t0={45.4} t1={47.1} words={[[45.44, 'Les'], [45.72, 'flous', RED], [45.88, 'disparaissent']]} size={62} />
      <Sent top={390} t0={47.15} t1={49.3} words={[[47.18, 'Un écran'], [48.0, 'reposant', GRN]]} size={66} />
      <ZoomPhone src={s4} t0={42.4} keys={[[43.0, 1.7, 360, TT[1]], [45.3, 1.15, 300, 560]]}>
        <HiBox sx={TT[0]} sy={TT[1]} w={100} h={60} t0={43.7} t1={45.3} />
      </ZoomPhone>
      <Stamp t0={44.4} text="C'EST NET !" color={GRN} x={540} y={1380} size={60} />
    </Scene>

    {/* QUESTION */}
    <Scene t0={49.5} t1={52.9}>
      <Glow x={540} y={900} r={300} color="#3b2cff" />
      <Sent top={300} t0={49.5} t1={53.2} words={[[49.64, 'Et toi, tu préfères'], [50.32, 'ton iPhone…']]} size={68} />
      <Pill t0={50.62} x={330} y={760} size={52} border={ELEC}>transparent</Pill>
      <Pill t0={51.3} x={760} y={900} size={52} border={GRN}>bien net</Pill>
      <Icon src="speech_balloon_3d.png" t0={51.5} size={240} x={540} y={1130} />
      <Pill t0={51.88} x={540} y={1360} size={48} border={YEL}>Dis-le en commentaire</Pill>
    </Scene>

    <EndScreen t0={53.3} t1={55.8} tEnd={58.0} tAbonne={55.9} tPour={56.26} tImmergee={57.14} />
    <Finish total={60.65} />
  </AbsoluteFill>;
};
