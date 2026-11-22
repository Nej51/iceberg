import React from 'react';
import {AbsoluteFill} from 'remotion';
import {useT, sp, lin, Sent, Background, Glass, Scene, Phone, ZoomPhone, StepTag, Checklist, HiBox, Stamp, Photo, Glow, Waves, pick, fontCss, ELEC, RED, GRN, CoverTitle, EndScreen, Finish} from './lib';
// Vidéo « Au secours » (raccourci d'urgence fait par l'IA), refaite le 22/11/2026 avec la voix d'origine de Nej.

// mot géant : lettres qui tombent une par une
const Giant: React.FC<{t0: number; t1: number; text: string; color: string; size?: number; top?: number}> = ({t0, t1, text, color, size = 280, top = 760}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const z = 1 + 0.06 * sp(t, t0 + text.length * 0.09 + 0.25, 10);
  return <div style={{position: 'absolute', top, left: 0, width: 1080, textAlign: 'center', transform: `scale(${z})`}}>
    {text.split('').map((c, i) => { const k = sp(t, t0 + i * 0.09, 9);
      return <span key={i} style={{display: 'inline-block', fontFamily: 'Pop', fontWeight: 700, fontSize: size, color, lineHeight: 1, textShadow: `0 10px 40px rgba(0,0,0,0.7), 0 0 60px ${color}`,
        transform: `translateY(${(1 - k) * -700}px)`, opacity: Math.min(1, k * 2)}}>{c}</span>; })}</div>;
};
// carte en verre avec interrupteurs iPhone qui passent au vert un par un
const Switches: React.FC<{t0: number; rows: [number, string, string][]}> = ({t0, rows}) => {
  const t = useT(); const k = sp(t, t0, 13);
  return <Glass style={{left: 90, top: 560, width: 900, height: rows.length * 150 + 30, transform: `scale(${k})`, opacity: Math.min(1, k * 1.5)}}>
    {rows.map(([a, l, s], i) => { const on = sp(t, a, 12); const g = t >= a ? 1 + 0.04 * Math.max(0, 1 - (t - a) / 0.4) : 1;
      return <div key={i} style={{position: 'absolute', left: 50, top: 30 + i * 150, width: 800, height: 130, display: 'flex', alignItems: 'center', transform: `scale(${g})`,
        borderBottom: i < rows.length - 1 ? '1.5px solid rgba(255,255,255,0.15)' : 'none'}}>
        <div style={{flex: 1}}><div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 50, color: '#fff', whiteSpace: 'nowrap'}}>{l}</div>
          <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 34, color: t >= a ? GRN : 'rgba(200,210,255,0.5)', whiteSpace: 'nowrap'}}>{s}</div></div>
        <div style={{width: 150, height: 86, borderRadius: 43, background: `rgba(${Math.round(120 - 68 * on)},${Math.round(120 + 79 * on)},${Math.round(130 - 41 * on)},1)`, position: 'relative', boxShadow: on > 0.5 ? `0 0 30px ${GRN}` : 'none'}}>
          <div style={{position: 'absolute', top: 6, left: 6 + 64 * on, width: 74, height: 74, borderRadius: 37, background: '#fff', boxShadow: '0 4px 10px rgba(0,0,0,0.3)'}} /></div>
      </div>; })}
  </Glass>;
};

export const Video: React.FC = () => {
  const t = useT();
  const scr = pick(t, [[16.6, 'as_reg.png'], [20.0, 'as_fid0.png'], [22.1, 'as_fid1.png'], [25.0, 'as_all.png'], [27.6, 'as_new0.png'], [31.26, 'as_new1.png'], [32.32, 'as_new2.png'], [33.5, 'as_new3.png'],
    [34.46, 'as_new4.png'], [35.86, 'as_new5.png'], [37.3, 'as_new6.png'], [39.68, 'as_new7.png'], [43.0, 'as_sc.png'], [46.8, 'as_name.png'], [48.6, 'as_sc2.png'], [49.3, 'as_ask.png']]);
  const cur = t < 25.0 ? 1 : t < 27.6 ? 2 : t < 45.9 ? 3 : t < 52.2 ? 4 : 5;
  const ex: [number, string][] = [[30.36, 'Par exemple…'], [32.32, 'Lampe torche'], [33.5, 'Volume à fond'], [34.46, 'Économie d’énergie'], [35.86, 'Position à Maman et Papa'], [37.72, '« Urgence, j’ai besoin d’aide »'], [39.68, 'Le 112 ou Maman ?']];
  const exi = ex.filter(([a]) => t >= a).length - 1;
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE + ACCROCHE : la scène de l'escalier */}
    <Scene t0={0} t1={9.5}>
      <Photo src="img_escalier.png" t0={0} t1={9.8} dim={0.15} />
      <Waves cx={150} cy={1325} t0={5.9} color={ELEC} r0={30} />
      <Sent top={290} t0={2.0} t1={4.45} words={[[2.0, 'Ton iPhone'], [2.08, 'appelle à l’aide', ELEC]]} size={60} />
      <Sent top={400} t0={2.44} t1={4.45} words={[[2.44, 'à ta place,'], [3.06, 'même hors de portée']]} size={52} />
      <Sent top={290} t0={4.54} t1={8.6} words={[[4.54, 'Tu glisses'], [4.88, 'dans l’escalier']]} size={60} />
      <Sent top={400} t0={5.88} t1={8.6} words={[[5.88, 'ton iPhone finit'], [6.74, 'sous le meuble', RED]]} size={52} />
      <Sent top={290} t0={8.7} t1={9.5} words={[[8.7, 'Mais tu peux'], [9.14, 'parler.', ELEC]]} size={80} />
      <CoverTitle line="TON IPHONE APPELLE À" keyword="L’AIDE" />
    </Scene>

    {/* « Dis Siri, au secours » */}
    <Scene t0={9.5} t1={13.45}>
      <Glow x={540} y={1000} r={360} color="#7a2cff" />
      <Sent top={290} t0={9.88} t1={11.8} words={[[9.88, '« Dis Siri,'], [10.66, 'au secours »', ELEC]]} size={84} />
      <Sent top={290} t0={11.88} t1={13.45} words={[[11.88, 'Ton iPhone'], [12.8, 's’occupe de tout', GRN]]} size={72} />
      <Phone src={t < 11.88 ? 'as_siri.png' : 'as_done.png'} x={540} top={520} w={440} t0={9.55} />
    </Scene>

    {/* l'IA le fabrique */}
    <Scene t0={13.45} t1={16.7}>
      <Glow x={540} y={900} r={400} color={ELEC} />
      <Sent top={330} t0={13.68} t1={16.7} words={[[13.68, 'Le mieux ?']]} size={80} />
      <Giant t0={14.4} t1={16.7} text="L’IA" color={ELEC} />
      <Sent top={1130} t0={14.88} t1={16.7} words={[[14.88, 'de ton iPhone'], [15.7, 'le fabrique pour toi', ELEC]]} size={58} />
    </Scene>

    {/* ÉTAPES */}
    <Scene t0={16.7} t1={52.3}>
      <StepTag n={1} t0={16.8} />
      {t >= 25.08 && <StepTag n={2} t0={25.08} />}
      {t >= 27.7 && <StepTag n={3} t0={27.7} />}
      {t >= 45.96 && <StepTag n={4} t0={45.96} />}
      <Checklist cur={cur} t0={16.9} />
      <ZoomPhone src={scr} t0={16.75} keys={[[16.7, 1, 300, 650], [18.6, 1.7, 300, 890], [20.0, 1, 300, 650], [21.1, 1.75, 300, 587], [23.5, 1, 300, 650], [26.6, 1.8, 470, 200], [27.6, 1.75, 300, 470],
        [42.6, 1, 300, 650], [46.7, 1.8, 300, 200], [48.5, 1, 300, 650], [49.6, 1.5, 300, 730]]}>
        <HiBox sx={300} sy={890} w={556} h={62} t0={18.7} t1={20.0} />
        <HiBox sx={300} sy={587} w={556} h={62} t0={21.2} t1={23.5} />
        <HiBox sx={556} sy={108} w={70} h={70} t0={26.9} t1={27.6} />
        <HiBox sx={522} sy={792} w={62} h={62} t0={42.82} t1={43.0} />
        <HiBox sx={300} sy={110} w={300} h={56} t0={46.9} t1={48.5} />
        <HiBox sx={300} sy={685} w={460} h={80} t0={50.28} t1={52.3} />
      </ZoomPhone>
      {/* étape 1 */}
      <Sent top={385} t0={17.6} t1={20.0} words={[[17.6, 'Va dans'], [17.94, 'Réglages', ELEC]]} />
      <Sent top={465} t0={18.7} t1={20.0} words={[[18.7, 'puis'], [18.8, 'Face ID et code', ELEC]]} />
      <Sent top={385} t0={20.08} t1={23.6} words={[[20.08, 'Vérifie que'], [21.2, 'Siri', ELEC], [21.48, 'est activé']]} />
      <Sent top={465} t0={22.36} t1={23.6} words={[[22.36, 'en mode verrouillé', ELEC]]} />
      {t < 25.0 && <Stamp t0={23.64} text="OBLIGATOIRE" color={RED} x={540} y={440} size={66} />}
      {/* étape 2 */}
      <Sent top={385} t0={25.74} t1={27.6} words={[[25.74, 'Ouvre'], [25.98, 'Raccourcis', ELEC]]} />
      <Sent top={465} t0={26.88} t1={27.6} words={[[26.88, 'et touche le'], [27.22, '+', ELEC]]} />
      {/* étape 3 */}
      <Sent top={385} t0={28.62} t1={30.3} words={[[28.62, 'Écris simplement']]} />
      <Sent top={465} t0={29.26} t1={30.3} words={[[29.26, 'ce que tu veux', ELEC]]} />
      {t >= 30.36 && t < 42.7 && <Sent key={exi} top={420} t0={ex[exi][0]} t1={exi < ex.length - 1 ? ex[exi + 1][0] : 42.7} words={[[ex[exi][0], ex[exi][1], exi ? ELEC : '#fff']]} size={exi === 5 ? 54 : 70} />}
      <Sent top={385} t0={42.82} t1={45.25} words={[[42.82, 'Valide', GRN]]} />
      <Sent top={465} t0={43.68} t1={45.25} words={[[43.68, 'et en quelques secondes…']]} size={58} />
      {t < 45.9 && <Stamp t0={45.3} text="C’EST PRÊT !" color={GRN} x={540} y={440} size={70} />}
      {/* étape 4 */}
      <Sent top={385} t0={46.82} t1={49.3} words={[[46.82, 'Touche son nom'], [47.28, 'en haut']]} />
      <Sent top={465} t0={47.94} t1={49.3} words={[[47.94, 'appelle-le'], [48.34, '« Au secours »', ELEC]]} size={58} />
      <Sent top={385} t0={49.36} t1={52.3} words={[[49.36, 'Teste-le une fois']]} />
      <Sent top={465} t0={50.28} t1={52.3} words={[[50.28, 'avec'], [50.7, 'Maman', GRN]]} />
      <Stamp t0={51.16} text="JAMAIS LE 112" color={RED} x={540} y={1380} size={60} rot={-5} />
    </Scene>

    {/* récap : interrupteurs */}
    <Scene t0={52.4} t1={58.1}>
      <Sent top={300} t0={52.5} t1={58.1} words={[[52.5, 'Et en cas de pépin :']]} size={68} />
      <Switches t0={52.6} rows={[[53.24, 'Lampe torche', 'pour qu’on te trouve'], [54.68, 'Volume à fond', 'pour entendre'], [55.94, 'Économie d’énergie', 'la batterie tient'], [57.18, 'Position partagée', 'ta famille sait où tu es']]} />
    </Scene>

    {/* partage */}
    <Scene t0={58.1} t1={60.6}>
      <Photo src="img_alerte.png" t0={58.1} t1={61} dim={0.2} />
      <Sent top={290} t0={58.16} t1={60.6} words={[[58.16, 'Envoie cette vidéo']]} size={76} />
      <Sent top={390} t0={59.4} t1={60.6} words={[[59.4, 'à quelqu’un'], [59.76, 'qui vit seul', ELEC]]} size={66} />
    </Scene>

    <EndScreen t0={999} t1={60.6} tEnd={63.6} tAbonne={60.9} tPour={61.52} tImmergee={62.58} handle="@iphoniceberg" />
    <Finish total={65.0} />
  </AbsoluteFill>;
};
