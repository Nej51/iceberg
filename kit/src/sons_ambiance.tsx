import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {useT, sp, lin, Sent, Background, Glass, Icon, Scene, Phone, ZoomPhone, StepTag, Checklist, HiBox, Stamp, Pill, Photo, Glow, Waves, pick, fontCss, ELEC, RED, GRN, YEL, CoverTitle, EndScreen, Finish} from './lib';
// Vidéo « Sons en arrière-plan + Musique d'ambiance », 22/11/2026.

const VsCard: React.FC<{t0: number; y: number; x: number; title: string; sub: string; color: string; icon: string}> = ({t0, y, x, title, sub, color, icon}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12);
  return <Glass style={{left: x, top: y, width: 400, height: 440, transform: `scale(${k})`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 14, border: `3px solid ${color}`, boxShadow: `0 0 40px ${color}66`, textAlign: 'center'}}>
    <Img src={staticFile(icon)} style={{width: 340, height: 230, objectFit: 'cover', borderRadius: 30, boxShadow: '0 16px 30px rgba(0,0,0,0.5)'}} />
    <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 44, color: '#fff', lineHeight: 1.1, padding: '0 20px'}}>{title}</div>
    <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 32, color}}>{sub}</div>
  </Glass>;
};
// gouttes de pluie lumineuses qui tombent doucement (ambiance)
const Rain: React.FC<{o?: number}> = ({o = 0.5}) => {
  const t = useT();
  return <>{Array.from({length: 40}).map((_, i) => { const x = (i * 137) % 1080; const sp_ = 500 + (i * 53) % 400; const y = ((t * sp_ + i * 211) % 2100) - 100;
    return <div key={i} style={{position: 'absolute', left: x, top: y, width: 3, height: 60, borderRadius: 2, background: 'linear-gradient(180deg,transparent,rgba(140,180,255,0.8))', opacity: o}} />; })}</>;
};

// une image plein cadre par mot : coupe sèche + zoom « punch » + petit flash
const Cuts: React.FC<{list: [number, string][]}> = ({list}) => {
  const t = useT(); let i = 0; for (let k = 0; k < list.length; k++) if (t >= list[k][0]) i = k;
  const [a, src] = list[i]; const k = sp(t, a, 18); const z = 1.18 - 0.1 * k + 0.02 * (t - a);
  const fl = i > 0 ? 1 - lin(t, a, a + 0.18) : 0; const dx = (i % 2 ? -1 : 1) * 20 * (t - a);
  return <AbsoluteFill style={{overflow: 'hidden'}}>
    <Img src={staticFile(src)} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${z}) translateX(${dx}px)`}} />
    <AbsoluteFill style={{background: 'rgba(5,6,20,0.18)'}} />
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(5,6,15,0.85) 0%, rgba(5,6,15,0.35) 26%, transparent 45%, transparent 78%, rgba(18,10,46,0.7) 100%)'}} />
    {fl > 0 && <AbsoluteFill style={{background: `rgba(255,255,255,${0.35 * fl})`}} />}
  </AbsoluteFill>;
};
const BigWord: React.FC<{t0: number; t1: number; text: string; color: string; size?: number}> = ({t0, t1, text, color, size = 150}) => {
  const t = useT(); if (t < t0 || t >= t1) return null; const k = sp(t, t0, 11);
  return <div style={{position: 'absolute', top: 300, left: 0, width: 1080, textAlign: 'center', padding: '0 60px', boxSizing: 'border-box', fontFamily: 'Pop', fontWeight: 700, fontSize: size, lineHeight: 1.05, color,
    textShadow: `0 8px 40px rgba(0,0,0,0.8), 0 0 40px ${color}88`, transform: `scale(${1.4 - 0.4 * k})`, filter: `blur(${(1 - Math.min(1, k)) * 14}px)`, opacity: Math.min(1, k * 1.6)}}>{text}</div>;
};
// vrai bouton du centre de contrôle (découpé dans nos écrans) qui rebondit puis s'allume quand on « appuie »
const Btn: React.FC<{src: string; t0: number; tOn: number; x: number; y: number; w: number; round?: boolean}> = ({src, t0, tOn, x, y, w, round}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 10); const on = t >= tOn; const press = on ? 1 - 0.08 * Math.max(0, 1 - (t - tOn) / 0.2) : 1;
  const h = round ? w : w * 0.96; const pls = 0.5 + 0.5 * Math.sin(t * 6);
  return <div style={{position: 'absolute', left: x - w / 2, top: y - h / 2, width: w, height: h, transform: `scale(${k * press}) rotate(${(1 - k) * -14}deg)`}}>
    <Img src={staticFile(`${src}_${on ? 'on' : 'off'}.png`)} style={{width: w, height: h, borderRadius: round ? '50%' : w * 0.2, boxShadow: on ? `0 0 ${50 + 30 * pls}px ${ELEC}, 0 30px 60px rgba(0,0,0,0.6)` : '0 30px 60px rgba(0,0,0,0.6)', border: '3px solid rgba(255,255,255,0.35)'}} />
    {t >= tOn - 0.3 && t < tOn + 0.5 && <div style={{position: 'absolute', left: w / 2 - 40, top: h / 2 - 40, width: 80, height: 80, borderRadius: '50%', background: 'rgba(255,255,255,0.6)', border: '4px solid #fff', boxShadow: `0 0 30px ${ELEC}`, opacity: 1 - lin(t, tOn + 0.2, tOn + 0.5)}} />}
  </div>;
};

export const Video: React.FC = () => {
  const t = useT();
  const scr = pick(t, [[0, 'sa_cc.png'], [16.92, 'sa_edit.png'], [20.1, 'sa_gal.png'], [21.0, 'sa_gal_sons.png'], [23.8, 'sa_gal_mus.png'], [28.8, 'sa_after.png'], [30.3, 'sa_after_repos.png'], [32.38, 'sa_menu.png'], [34.82, 'sa_list.png']]);
  const cur = t < 20.08 ? 1 : t < 22.9 ? 2 : t < 28.76 ? 3 : t < 37.4 ? 4 : 5;
  const st = Math.min(cur, 4);
  const scr2 = pick(t, [[50, 'sa_reg_on.png'], [57.86, 'sa_reg_off.png'], [62.2, 'sa_min_h.png']]);
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE + HOOK (dynamique : boutons + une image par mot) */}
    <Scene t0={0} t1={9.3}>
      <Cuts list={[[0, 'img_chambre.png'], [4.68, 'img_toit.png'], [5.26, 'img_feu.png'], [5.78, 'img_ocean.png'], [6.58, 'img_casque.png'], [7.66, 'img_feu.png'], [8.22, 'img_casque.png'], [8.88, 'img_chambre.png']]} />
      {t < 4.68 && <Waves cx={654} cy={1222} t0={0.2} color={ELEC} r0={60} />}
      {t < 4.68 && <Rain o={0.35} />}
      {t >= 2.0 && t < 4.68 && <>
        <Sent top={280} t0={2.0} t1={4.68} words={[[2.0, 'Ajoute'], [2.3, 'ces 2 boutons', ELEC]]} size={74} />
        <Btn src="btn_sons" t0={2.64} tOn={3.1} x={300} y={800} w={330} round />
        <Btn src="btn_repos" t0={2.92} tOn={3.5} x={780} y={800} w={420} />
      </>}
      <BigWord t0={4.68} t1={5.26} text="LA PLUIE" color="#7fb2ff" />
      <BigWord t0={5.26} t1={5.78} text="LE FEU" color="#FF8A00" />
      <BigWord t0={5.78} t1={6.58} text="L’OCÉAN" color="#4fd7ff" />
      <BigWord t0={6.58} t1={7.66} text="MUSIQUES D’AMBIANCE" color={ELEC} size={96} />
      <BigWord t0={7.66} t1={8.22} text="SE RELAXER" color="#ffffff" />
      <BigWord t0={8.22} t1={8.88} text="TRAVAILLER" color="#ffffff" />
      <BigWord t0={8.88} t1={9.6} text="S’ENDORMIR" color={YEL} />
      <CoverTitle line="TON IPHONE T’AIDE À" keyword="DORMIR" />
    </Scene>
    <Scene t0={9.3} t1={15.0}>
      <Photo src="img_chambre.png" t0={9.3} t1={15.3} dim={0.3} />
      <Sent top={290} t0={9.74} t1={15.2} words={[[9.74, 'Déjà dans'], [10.82, 'ton iPhone', ELEC]]} size={74} />
      <Stamp t0={12.42} text="GRATUIT" color={GRN} x={540} y={1180} size={80} rot={-6} />
      <Pill t0={13.04} x={540} y={1360} size={44} border={ELEC}>en quelques clics</Pill>
    </Scene>

    {/* ÉTAPES */}
    <Scene t0={15.0} t1={37.5}>
      <StepTag n={st} t0={[15.08, 20.08, 22.9, 28.76][st - 1]} />
      <Checklist cur={cur} t0={15.2} />
      <Sent top={400} t0={15.6} t1={16.9} words={[[15.66, 'Ouvre le'], [16.02, 'centre de contrôle', ELEC]]} size={50} />
      <Sent top={400} t0={16.9} t1={20.08} words={[[16.92, 'Reste appuyé'], [17.64, 'sur un espace vide']]} size={48} />
      <Sent top={470} t0={18.4} t1={20.08} words={[[18.46, 'puis'], [18.98, '« Ajouter une commande »', ELEC]]} size={46} />
      <Sent top={400} t0={20.4} t1={22.9} words={[[20.88, 'Cherche']]} size={52} />
      <Sent top={470} t0={20.4} t1={22.9} words={[[21.02, '« Sons en arrière-plan »', ELEC]]} size={52} />
      <Sent top={400} t0={23.6} t1={28.7} words={[[23.72, 'Cherche'], [23.86, '« Musique d’ambiance »', ELEC]]} size={46} />
      <Sent top={470} t0={24.8} t1={28.7} words={[[24.92, 'et ajoute'], [25.12, 'les 4', GRN]]} size={52} />
      <Sent top={400} t0={29.4} t1={31.3} words={[[29.5, 'Touche un bouton'], [30.22, 'pour lancer', GRN]]} size={50} />
      <Sent top={400} t0={31.38} t1={37.5} words={[[32.26, 'Reste appuyé'], [32.84, 'sur Sons', ELEC]]} size={52} />
      <Sent top={470} t0={33.8} t1={37.5} words={[[33.9, 'choisis'], [34.32, 'le volume'], [34.82, 'et le son', ELEC]]} size={50} />
      <ZoomPhone src={scr} t0={15.1} keys={[[15.2, 1, 300, 650], [17.6, 1.4, 300, 1000], [20.1, 1, 300, 650], [20.6, 1.7, 300, 300], [28.8, 1, 300, 650], [29.6, 1.5, 300, 470], [31.6, 1.6, 230, 700], [32.4, 1.3, 300, 620], [34.82, 1.25, 300, 700], [35.3, 1.5, 300, 1000]]}>
        <HiBox sx={300} sy={1090} w={420} h={90} t0={17.0} t1={18.9} />
        <HiBox sx={300} sy={1175} w={320} h={66} t0={18.98} t1={20.1} />
        <HiBox sx={300} sy={176} w={520} h={70} t0={20.9} t1={21.9} />
        <HiBox sx={120} sy={400} w={150} h={180} t0={21.9} t1={22.9} />
        <HiBox sx={506} sy={400} w={140} h={170} t0={25.84} t1={26.4} />
        <HiBox sx={95} sy={400} w={140} h={170} t0={26.46} t1={27.1} />
        <HiBox sx={369} sy={400} w={140} h={170} t0={27.2} t1={28.0} />
        <HiBox sx={232} sy={400} w={140} h={170} t0={28.06} t1={28.8} />
        <HiBox sx={431} sy={574} w={250} h={240} t0={29.84} t1={31.4} />
        <HiBox sx={108} sy={785} w={130} h={130} t0={32.0} t1={32.4} />
        <HiBox sx={300} sy={602} w={520} h={60} t0={34.3} t1={34.82} />
        <HiBox sx={300} sy={1104} w={440} h={56} t0={35.46} t1={36.3} />
        <HiBox sx={300} sy={422} w={440} h={56} t0={36.42} t1={36.9} />
        <HiBox sx={300} sy={670} w={440} h={56} t0={36.98} t1={37.5} />
      </ZoomPhone>
      {t > 30.4 && t < 31.4 && <Waves cx={540} cy={1000} t0={30.4} color={ELEC} r0={160} />}
    </Scene>

    {/* DIFFÉRENCE */}
    <Scene t0={37.5} t1={50.2}>
      {t < 39.5 && <Stamp t0={37.6} text="ET VOILÀ !" color={GRN} x={540} y={1450} size={56} rot={-6} />}
      <Sent top={280} t0={38.2} t1={50.4} words={[[38.2, 'Quelle'], [38.3, 'différence ?', YEL]]} size={72} />
      <VsCard t0={39.66} x={90} y={540} title="Sons en arrière-plan" sub="bruit continu" color={ELEC} icon="img_toit.png" />
      <VsCard t0={43.84} x={590} y={540} title="Musique d’ambiance" sub="vraies musiques" color={GRN} icon="img_casque.png" />
      <Sent top={380} t0={41.6} t1={43.8} words={[[41.78, 'cache la rue'], [42.98, 'et les voisins', ELEC]]} size={50} />
      <Pill t0={46.5} x={290} y={1100} size={42}>dormir</Pill>
      <Pill t0={47.06} x={540} y={1100} size={42}>détente</Pill>
      <Pill t0={47.78} x={800} y={1100} size={42}>concentration</Pill>
      <Stamp t0={48.6} text="SANS ABONNEMENT" color={ELEC} x={540} y={1280} size={52} rot={-5} />
    </Scene>

    {/* PIÈGE */}
    <Scene t0={50.2} t1={59.1}>
      <Sent top={270} t0={50.3} t1={59.3} words={[[50.32, 'Attention,'], [51.22, 'un piège', RED]]} size={66} />
      <Sent top={360} t0={53.7} t1={57.8} words={[[53.8, '« Ne plus lire les sons'], [54.74, 'en mode verrouillé »', RED]]} size={40} />
      <Sent top={360} t0={57.86} t1={59.3} words={[[57.86, 'Laisse-le'], [58.2, 'désactivé', GRN]]} size={56} />
      <ZoomPhone src={scr2} t0={50.4} keys={[[50.5, 1, 300, 650], [52.4, 1.6, 300, 960]]}>
        <HiBox sx={300} sy={997} w={560} h={92} t0={54.0} t1={59.2} />
      </ZoomPhone>
      <Stamp t0={56.38} text="TOUT S’ARRÊTE" color={RED} x={540} y={1400} size={50} rot={-6} />
    </Scene>

    {/* BONUS */}
    <Scene t0={59.1} t1={65.0}>
      <Sent top={270} t0={59.2} t1={65.2} words={[[59.22, 'Bonus :', GRN], [60.7, 'un minuteur', ELEC]]} size={64} />
      <Sent top={360} t0={62.0} t1={65.2} words={[[62.06, 'ça s’arrête'], [62.5, 'tout seul', GRN]]} size={52} />
      <ZoomPhone src={scr2} t0={59.15} keys={[[59.2, 1.6, 300, 960], [61.2, 1.5, 300, 860], [62.2, 1.5, 300, 360]]}>
        <HiBox sx={300} sy={895} w={560} h={70} t0={60.7} t1={62.2} />
        <HiBox sx={300} sy={295} w={560} h={60} t0={63.2} t1={64.0} />
        <HiBox sx={300} sy={361} w={560} h={60} t0={64.06} t1={65.2} />
      </ZoomPhone>
    </Scene>

    {/* PARTAGE + QUESTION */}
    <Scene t0={65.0} t1={70.3}>
      <Photo src="img_lit.png" t0={65.0} t1={70.6} dim={0.2} />
      <Sent top={290} t0={65.0} t1={67.4} words={[[65.0, 'Quelqu’un'], [65.68, 'dort mal ?', YEL]]} size={70} />
      <Pill t0={66.24} x={540} y={1130} size={48} border={ELEC}>Envoie-lui cette vidéo</Pill>
      <Sent top={290} t0={67.42} t1={70.5} words={[[67.42, 'Et toi ?']]} size={70} />
      <Pill t0={68.6} x={310} y={1300} size={48} border={ELEC}>la pluie</Pill>
      <Pill t0={69.4} x={780} y={1300} size={48} border="#4fd7ff">l’océan</Pill>
    </Scene>

    <EndScreen t0={70.3} t1={72.9} tEnd={75.0} tAbonne={72.94} tPour={73.34} tImmergee={74.16} />
    <Finish total={76.3} />
  </AbsoluteFill>;
};
