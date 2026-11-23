import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {useT, sp, lin, Sent, Background, Glass, Icon, Scene, Phone, ZoomPhone, StepTag, Checklist, HiBox, Stamp, Pill, Glow, pick, fontCss, ELEC, RED, GRN, YEL, CoverTitle, EndScreen, Finish} from './lib';
// Vidéo « Relooke ton écran verrouillé » (iOS 27 : heure en petit, lecteur, Étendre, Image Playground), 23/11/2026.

// image qui apparaît en fondu par-dessus l'écran du téléphone (reçoit scale du Phone)
const FadeImg: React.FC<{src: string; a: number; b: number; scale?: number}> = ({src, a, b}) => {
  const t = useT(); const o = lin(t, a, b); if (o <= 0) return null;
  return <Img src={staticFile(src)} style={{position: 'absolute', left: 0, top: 0, width: '100%', height: '100%', opacity: o}} />;
};
// doigt qui glisse (coordonnées écran 600x1300)
const Swipe: React.FC<{x0: number; x1: number; y: number; t0: number; t1: number; scale?: number}> = ({x0, x1, y, t0, t1, scale = 1}) => {
  const t = useT(); if (t < t0 - 0.2 || t > t1 + 0.25) return null; const k = lin(t, t0, t1); const x = x0 + (x1 - x0) * (1 - Math.pow(1 - k, 2)); const r = 40 * scale;
  const o = Math.min(lin(t, t0 - 0.2, t0), 1 - lin(t, t1, t1 + 0.25));
  return <div style={{position: 'absolute', left: x * scale - r, top: y * scale - r, width: 2 * r, height: 2 * r, borderRadius: '50%', background: 'rgba(255,255,255,0.6)', border: `${3 * scale}px solid #fff`, boxShadow: '0 0 30px rgba(47,91,255,0.9)', opacity: o}} />;
};
// deux doigts qui pincent
const Pinch: React.FC<{cx: number; cy: number; t0: number; t1: number; scale?: number}> = ({cx, cy, t0, t1, scale = 1}) => {
  const t = useT(); if (t < t0 - 0.2 || t > t1 + 0.25) return null; const k = lin(t, t0, t1); const d = 190 - 110 * k; const r = 38 * scale;
  const o = Math.min(lin(t, t0 - 0.2, t0), 1 - lin(t, t1, t1 + 0.25));
  return <>{[-1, 1].map((s) => <div key={s} style={{position: 'absolute', left: (cx + s * d * 0.7) * scale - r, top: (cy + s * d) * scale - r, width: 2 * r, height: 2 * r, borderRadius: '50%', background: 'rgba(255,255,255,0.6)', border: `${3 * scale}px solid #fff`, boxShadow: '0 0 30px rgba(47,91,255,0.9)', opacity: o}} />)}</>;
};
// « Étendre » : l'image complète se dévoile depuis la bande de la photo
const Reveal: React.FC<{t0: number; t1: number; scale?: number}> = ({t0, t1}) => {
  const t = useT(); if (t < t0) return null; const k = lin(t, t0, t1); const e = 1 - Math.pow(1 - k, 3);
  const top = 36.15 * (1 - e), bot = 34.3 * (1 - e), side = 10 * (1 - e);
  const sh = 1 - lin(t, t1, t1 + 0.8);
  return <>
    <Img src={staticFile('ev_ext_done.png')} style={{position: 'absolute', left: 0, top: 0, width: '100%', height: '100%', clipPath: `inset(${top}% ${side}% ${bot}% ${side}%)`}} />
    <div style={{position: 'absolute', left: `${side}%`, right: `${side}%`, top: `${top}%`, bottom: `${bot}%`, border: '3px solid rgba(140,180,255,0.9)', boxShadow: '0 0 40px rgba(47,91,255,0.9), inset 0 0 40px rgba(140,120,255,0.6)', opacity: sh}} />
  </>;
};
// texte tapé dans le champ Image Playground
const Typed: React.FC<{text: string; t0: number; dt: number; scale?: number}> = ({text, t0, dt, scale = 1}) => {
  const t = useT(); if (t < t0) return null; const n = Math.min(text.length, Math.floor((t - t0) / dt) + 1);
  return <div style={{position: 'absolute', left: 32 * scale, top: 662 * scale, width: 536 * scale, height: 76 * scale, borderRadius: 38 * scale, background: '#3d3566', display: 'flex', alignItems: 'center', paddingLeft: 36 * scale, boxSizing: 'border-box',
    fontFamily: 'Int', fontWeight: 600, fontSize: 22 * scale, color: '#fff', whiteSpace: 'nowrap'}}>{text.slice(0, n)}<span style={{width: 3 * scale, height: 30 * scale, background: '#4f8cff', marginLeft: 3 * scale, opacity: Math.sin(t * 12) > 0 ? 1 : 0}} /></div>;
};
// petit téléphone avant/après avec étiquette
const Mini: React.FC<{src: string; x: number; t0: number; label: string; color: string}> = ({src, x, t0, label, color}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 13);
  return <>
    <Phone src={src} x={x} top={620} w={360} t0={t0} ph={x / 100} />
    <div style={{position: 'absolute', left: x - 130, top: 545, width: 260, textAlign: 'center', transform: `scale(${k})`}}>
      <span style={{display: 'inline-block', background: color, borderRadius: 30, padding: '6px 30px', fontFamily: 'Pop', fontWeight: 700, fontSize: 40, color: '#fff', boxShadow: `0 0 30px ${color}`}}>{label}</span></div>
  </>;
};

export const Video: React.FC = () => {
  const t = useT();
  const scr = pick(t, [[0, 'ev_big.png'], [9.5, 'ev_gal.png'], [11.4, 'ev_edit.png'], [12.2, 'ev_edit_sel.png'], [12.85, 'ev_panel.png'], [15.6, 'ev_panel_small.png'], [17.1, 'ev_small.png'],
    [19.36, 'ev_music.png'], [23.15, 'ev_music_swipe.png'], [23.45, 'ev_music_gone.png'], [23.75, 'ev_small.png'], [28.8, 'ev_music.png'], [30.05, 'ev_music_swipe.png'], [30.3, 'ev_music_gone.png'], [30.5, 'ev_small.png'],
    [30.74, 'ev_ext.png'], [40.08, 'ev_gal.png'], [41.3, 'ev_add.png'], [42.3, 'ev_ip.png'], [46.1, 'ev_ip_result.png']]);
  const cur = t < 19.36 ? 1 : t < 30.74 ? 2 : t < 40.08 ? 3 : t < 46.9 ? 4 : 5;
  const st = Math.min(cur, 4);
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE + ACCROCHE : écran en bazar -> écran propre */}
    <Scene t0={0} t1={6.0}>
      <Glow x={540} y={1050} r={360} color="#6a2cff" />
      <Phone src="ev_big_music.png" x={540} top={560 + 230 * (1 - lin(t, 1.6, 2.3))} w={450}>
        <FadeImg src="ev_small.png" a={2.86} b={3.3} />
      </Phone>
      {t >= 2.86 && t < 4.0 && <Stamp t0={2.86} text="PROPRE" color={GRN} x={540} y={1250} size={64} rot={-6} />}
      <Sent top={260} t0={2.0} t1={6.0} words={[[2.0, 'Rends ton écran'], [2.1, 'verrouillé', ELEC]]} size={56} />
      <Sent top={340} t0={2.0} t1={6.0} words={[[2.44, 'beaucoup plus'], [2.86, 'propre', GRN]]} size={56} />
      <Pill t0={4.3} x={540} y={480} size={44} border={ELEC}>4 réglages, quelques secondes</Pill>
      <CoverTitle line="RELOOKE TON ÉCRAN" keyword="VERROUILLÉ" />
    </Scene>

    {/* ÉTAPES 1 À 4 */}
    <Scene t0={6.0} t1={46.9}>
      <StepTag n={st} t0={[6.14, 19.36, 30.74, 40.08][st - 1]} />
      <Checklist cur={cur} t0={6.3} />
      {/* étape 1 */}
      <Sent top={390} t0={6.5} t1={8.6} words={[[6.6, 'L’heure cache'], [7.4, 'ta photo', RED]]} size={62} />
      <Sent top={390} t0={8.86} t1={10.5} words={[[8.86, 'Reste appuyé'], [9.6, 'sur ton écran', ELEC]]} size={58} />
      <Sent top={390} t0={10.6} t1={12.45} words={[[10.6, 'Touche'], [10.8, '« Personnaliser »', ELEC]]} size={56} />
      <Sent top={465} t0={11.7} t1={12.45} words={[[11.72, 'puis l’heure']]} size={50} />
      <Sent top={390} t0={12.5} t1={15.5} words={[[12.6, 'Dans le panneau,']]} size={56} />
      <Sent top={465} t0={12.5} t1={15.5} words={[[14.3, 'l’icône'], [14.7, 'en haut à droite', ELEC]]} size={50} />
      <Sent top={390} t0={15.64} t1={19.3} words={[[15.7, 'L’heure se range'], [16.3, 'en petit', GRN]]} size={58} />
      <Sent top={465} t0={17.9} t1={19.3} words={[[17.96, 'ta photo'], [18.3, 'prend toute la place', GRN]]} size={46} />
      {/* étape 2 */}
      <Sent top={390} t0={19.4} t1={22.8} words={[[19.9, 'Le lecteur'], [20.4, 'de musique', ELEC]]} size={62} />
      <Sent top={390} t0={22.85} t1={24.3} words={[[22.9, 'Glisse-le'], [23.5, 'vers la gauche', ELEC]]} size={58} />
      <Sent top={390} t0={24.35} t1={26.3} words={[[24.4, 'La musique'], [25.5, 'continue', GRN]]} size={60} />
      <Sent top={390} t0={26.38} t1={30.6} words={[[26.4, 'Piège :', RED], [27.6, 'pause puis relance']]} size={54} />
      <Sent top={465} t0={29.2} t1={30.6} words={[[29.3, 'glisse-le'], [29.9, 'à nouveau', GRN]]} size={50} />
      {/* étape 3 */}
      <Sent top={390} t0={30.8} t1={32.8} words={[[31.3, 'Photo'], [31.8, 'pas au bon format ?', RED]]} size={54} />
      <Sent top={390} t0={32.9} t1={35.9} words={[[33.7, 'Pince pour'], [34.4, 'dézoomer', ELEC]]} size={58} />
      <Sent top={465} t0={34.9} t1={35.9} words={[[35.0, 'puis'], [35.3, '« Étendre »', ELEC]]} size={54} />
      <Sent top={390} t0={35.96} t1={40.0} words={[[36.0, 'Ton iPhone'], [36.3, 'invente la suite', GRN]]} size={56} />
      {/* étape 4 */}
      <Sent top={390} t0={40.2} t1={42.3} words={[[40.7, 'Touche le +'], [41.5, 'puis'], [41.6, 'Image Playground', ELEC]]} size={46} />
      <Sent top={390} t0={42.4} t1={46.0} words={[[42.8, 'Décris le fond'], [43.6, 'dont tu rêves', ELEC]]} size={56} />
      <Sent top={390} t0={46.0} t1={46.9} words={[[46.0, 'Il le dessine'], [46.6, 'pour toi', GRN]]} size={56} />

      <ZoomPhone src={scr} t0={6.15} keys={[[6.2, 1, 300, 650], [10.3, 1.5, 380, 1100], [11.5, 1, 300, 650], [11.8, 1.5, 300, 320], [12.85, 1.1, 300, 900], [14.1, 1.9, 500, 860], [15.7, 1.7, 300, 220], [17.2, 1, 300, 650],
        [21.0, 1.35, 300, 950], [24.4, 1, 300, 650], [28.6, 1.35, 300, 950], [30.6, 1, 300, 650], [33.5, 1.25, 300, 700], [34.9, 1.7, 300, 1060], [35.9, 1, 300, 650],
        [40.4, 1.7, 450, 1110], [41.4, 1.6, 300, 330], [42.4, 1.3, 300, 680], [46.1, 1, 300, 650]]}>
        <HiBox sx={300} sy={1115} w={320} h={84} t0={10.6} t1={11.4} />
        <HiBox sx={300} sy={300} w={460} h={230} t0={11.8} t1={12.8} />
        <HiBox sx={520} sy={852} w={86} h={86} t0={14.3} t1={15.6} />
        <HiBox sx={300} sy={150} w={380} h={60} t0={16.3} t1={17.1} />
        <HiBox sx={300} sy={955} w={560} h={270} t0={21.9} t1={22.9} />
        <Swipe x0={470} x1={130} y={955} t0={22.9} t1={23.5} />
        <Swipe x0={470} x1={130} y={955} t0={29.95} t1={30.45} />
        <Pinch cx={300} cy={660} t0={33.8} t1={34.6} />
        <HiBox sx={300} sy={1052} w={230} h={84} t0={35.1} t1={35.96} />
        {t >= 30.74 && t < 40.08 && <Reveal t0={35.96} t1={37.6} />}
        <HiBox sx={512} sy={1115} w={90} h={90} t0={40.75} t1={41.3} />
        <HiBox sx={300} sy={300} w={120} h={170} t0={41.6} t1={42.3} />
        {t >= 42.3 && t < 46.1 && <Typed text="un coucher de soleil sur la mer" t0={44.6} dt={0.035} />}
        {t >= 42.3 && t < 46.1 && <HiBox sx={300} sy={700} w={556} h={92} t0={42.9} t1={46.1} />}
      </ZoomPhone>
      {t >= 28.82 && t < 29.9 && <Stamp t0={28.82} text="IL REVIENT" color={RED} x={540} y={1380} size={52} rot={-6} />}
      {t >= 24.4 && t < 26.3 && <Icon src="musical_notes_3d.png" t0={24.4} size={170} x={860} y={700} />}
      {t >= 38.0 && t < 40.0 && <>
        <Pill t0={38.1} x={230} y={1390} size={40}>le ciel</Pill>
        <Pill t0={38.6} x={520} y={1390} size={40}>le décor</Pill>
        <Pill t0={39.2} x={800} y={1390} size={40}>les bords</Pill>
      </>}
    </Scene>

    {/* ATTENTION : Apple Intelligence + limite */}
    <Scene t0={46.9} t1={55.4}>
      <Sent top={280} t0={47.2} t1={55.6} words={[[47.3, 'Attention', RED]]} size={84} />
      <Sent top={400} t0={47.9} t1={52.4} words={[[48.0, 'Étendre'], [48.4, '+'], [48.6, 'Image Playground', ELEC]]} size={50} />
      <Pill t0={49.4} x={540} y={560} size={44} border={ELEC}>demandent Apple Intelligence</Pill>
      {t < 52.4 && <Icon src="mobile_phone_3d.png" t0={50.4} size={300} x={540} y={850} />}
      <Sent top={1040} t0={50.6} t1={52.4} words={[[50.7, 'iPhone 15 Pro', YEL]]} size={84} />
      <Sent top={1150} t0={50.6} t1={52.4} words={[[51.5, 'ou plus récent']]} size={60} />
      <Sent top={420} t0={52.5} t1={55.6} words={[[52.6, '« Étendre »'], [53.2, 'limite par jour', RED]]} size={54} />
      {t >= 52.5 && <Glass style={{left: 190, top: 620, width: 700, height: 420, overflow: 'hidden', transform: `scale(${sp(t, 52.6, 13)})`}}>
        <Img src={staticFile('ev_wallA.png')} style={{position: 'absolute', left: 0, top: -380, width: 700, height: 1517}} />
        <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg,transparent 50%,rgba(5,6,20,0.7))'}} /></Glass>}
      <Sent top={1090} t0={53.9} t1={55.6} words={[[54.0, 'garde-la pour'], [54.7, 'tes plus belles photos', YEL]]} size={48} />
    </Scene>

    {/* PARTAGE : avant / après */}
    <Scene t0={55.4} t1={59.32}>
      <Sent top={270} t0={55.5} t1={59.5} words={[[55.5, 'Un écran'], [57.3, 'en bazar ?', RED]]} size={74} />
      <Mini src="ev_big_music.png" x={300} t0={55.7} label="avant" color={RED} />
      <Mini src="ev_ip_result.png" x={780} t0={56.3} label="après" color={GRN} />
      <Pill t0={58.06} x={540} y={420} size={46} border={ELEC}>Envoie-lui cette vidéo</Pill>
    </Scene>

    <EndScreen t0={59.32} t1={61.58} tEnd={63.98} tAbonne={61.86} tPour={62.28} tImmergee={63.16} />
    <Finish total={65.3} />
  </AbsoluteFill>;
};
