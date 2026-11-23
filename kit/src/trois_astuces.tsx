import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {useT, sp, lin, Sent, Background, Glass, Scene, Phone, ZoomPhone, StepTag, HiBox, Stamp, Pill, Photo, pick, fontCss, ELEC, RED, GRN, YEL, CoverTitle, EndScreen, Finish} from './lib';
import data from './data.json';
// Vidéo « 3 astuces cachées » (Envoyer plus tard, Pleine page, symbole °), 23/11/2026.
const D: any = data;

const Check: React.FC<{ok: boolean; s: number}> = ({ok, s}) => <div style={{width: s, height: s, borderRadius: s / 2, background: ok ? GRN : RED, boxShadow: `0 0 24px ${ok ? GRN : RED}`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
  <svg width={s * 0.6} height={s * 0.6} viewBox="0 0 24 24">{ok ? <path d="M4 12.5l5 5L20 6.5" stroke="#fff" strokeWidth="3.6" fill="none" strokeLinecap="round" strokeLinejoin="round" /> : <path d="M6 6l12 12M18 6L6 18" stroke="#fff" strokeWidth="3.6" strokeLinecap="round" />}</svg></div>;

// checklist 1-2-3 à gauche (étapes de l'astuce 1)
const List3: React.FC<{cur: number; t0: number}> = ({cur, t0}) => {
  const t = useT();
  return <div style={{position: 'absolute', left: 52, top: 640, display: 'flex', flexDirection: 'column', gap: 34}}>
    {[1, 2, 3].map((n, i) => { const k = sp(t, t0 + i * 0.08, 12); const done = n < cur, on = n === cur; const p = 0.5 + 0.5 * Math.sin(t * 6);
      return <div key={n} style={{width: 78, height: 78, borderRadius: 26, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${k})`,
        background: done ? GRN : on ? ELEC : 'rgba(255,255,255,0.08)', border: on || done ? 'none' : '2px solid rgba(255,255,255,0.25)',
        boxShadow: on ? `0 0 ${20 + 20 * p}px ${ELEC}` : done ? `0 0 20px ${GRN}` : 'none', fontFamily: 'Pop', fontWeight: 700, fontSize: 42, color: '#fff'}}>
        {done ? <svg width="40" height="40" viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6.5" stroke="#fff" strokeWidth="3.4" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg> : n}</div>; })}
  </div>;
};
// carte « astuce n »
const AstCard: React.FC<{n: number; label: string; sub: string; t0: number; y: number; on?: number}> = ({n, label, sub, t0, y, on}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12); const lit = on !== undefined && t >= on; const p = 0.5 + 0.5 * Math.sin(t * 5);
  return <Glass style={{left: 120, top: y, width: 840, height: 190, transform: `translateX(${(1 - k) * 300}px) scale(${lit ? 1.04 : 1})`, opacity: Math.min(1, k * 1.5), display: 'flex', alignItems: 'center', gap: 34, padding: '0 34px', boxSizing: 'border-box',
    border: lit ? `3px solid ${ELEC}` : undefined, boxShadow: lit ? `0 0 ${30 + 30 * p}px ${ELEC}aa` : undefined}}>
    <div style={{width: 110, height: 110, borderRadius: 32, background: ELEC, boxShadow: `0 0 30px ${ELEC}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Pop', fontWeight: 700, fontSize: 64, color: '#fff'}}>{n}</div>
    <div><div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 54, color: '#fff', whiteSpace: 'nowrap'}}>{label}</div>
      <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 32, color: 'rgba(210,220,255,0.85)', whiteSpace: 'nowrap'}}>{sub}</div></div>
  </Glass>;
};
const Cards: React.FC<{t0: number; on?: number}> = ({t0, on}) => <>
  <AstCard n={1} label="Envoyer plus tard" sub="Messages" t0={t0} y={620} on={on} />
  <AstCard n={2} label="Pleine page" sub="Capture d’écran" t0={t0 + 0.2} y={860} />
  <AstCard n={3} label="Le symbole °" sub="Clavier" t0={t0 + 0.4} y={1100} />
</>;
// grosse bulle iMessage / SMS
const BigBubble: React.FC<{t0: number; y: number; color: string; text: string; ok: boolean; tc: number}> = ({t0, y, color, text, ok, tc}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12); const sh = !ok && t > tc ? Math.sin(t * 40) * 8 * (1 - lin(t, tc, tc + 0.5)) : 0;
  return <div style={{position: 'absolute', left: 150, top: y, width: 780, display: 'flex', alignItems: 'center', gap: 30, transform: `scale(${k}) translateX(${sh}px)`, opacity: !ok && t > tc ? 0.75 : 1}}>
    <div style={{flex: 1, background: color, borderRadius: 50, padding: '30px 44px', fontFamily: 'Pop', fontWeight: 700, fontSize: 50, color: '#fff', boxShadow: `0 0 40px ${color}99`, whiteSpace: 'nowrap'}}>{text}</div>
    {t >= tc && <div style={{transform: `scale(${sp(t, tc, 10)})`}}><Check ok={ok} s={100} /></div>}
  </div>;
};
// carte en verre + chiffre qui grimpe (14 jours max)
const DaysCard: React.FC<{t0: number}> = ({t0}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12); const v = Math.round(14 * lin(t, t0 + 0.1, t0 + 0.9));
  return <Glass style={{left: 140, top: 1110, width: 800, height: 260, transform: `scale(${k})`, padding: '30px 50px', boxSizing: 'border-box'}}>
    <div style={{display: 'flex', alignItems: 'baseline', gap: 20}}><span style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 110, color: YEL, lineHeight: 1}}>{v}</span>
      <span style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 52, color: '#fff'}}>jours max</span></div>
    <div style={{marginTop: 30, height: 22, borderRadius: 11, background: 'rgba(255,255,255,0.12)'}}><div style={{width: `${(v / 14) * 100}%`, height: '100%', borderRadius: 11, background: YEL, boxShadow: `0 0 20px ${YEL}`}} /></div>
  </Glass>;
};
// pile de captures qui s'empilent
const ShotPile: React.FC<{t0: number}> = ({t0}) => {
  const t = useT(); if (t < t0) return null;
  return <>{Array.from({length: 10}).map((_, i) => { const a = t0 + i * 0.07; if (t < a) return null; const k = sp(t, a, 11); const r = ((i * 37) % 30) - 15;
    return <div key={i} style={{position: 'absolute', left: 540 - 130 + ((i * 53) % 160) - 80, top: 820 + ((i * 41) % 200), width: 260, height: 520, borderRadius: 26, overflow: 'hidden', border: '4px solid #fff',
      boxShadow: '0 20px 50px rgba(0,0,0,0.6)', transform: `rotate(${r}deg) scale(${k})`}}><Img src={staticFile('c_page.png')} style={{width: 260, height: 563}} /></div>; })}</>;
};
// liste des applis compatibles
const AppRows: React.FC<{rows: [number, string, boolean][]}> = ({rows}) => {
  const t = useT();
  return <Glass style={{left: 140, top: 560, width: 800, height: 760, padding: '40px 50px', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 34}}>
    {rows.map(([a, n, ok], i) => { const k = sp(t, a, 12); const on = t >= a;
      return <div key={i} style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: 140, padding: '0 34px', borderRadius: 36, background: on ? (ok ? 'rgba(52,199,89,0.16)' : 'rgba(255,69,58,0.18)') : 'rgba(255,255,255,0.06)', transform: `scale(${on ? 1 + 0.04 * (1 - k) : 1})`}}>
        <span style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 56, color: on ? '#fff' : 'rgba(255,255,255,0.35)'}}>{n}</span>
        {on && <div style={{transform: `scale(${k})`}}><Check ok={ok} s={86} /></div>}</div>; })}
  </Glass>;
};
// mot géant lettre par lettre
const BigLetters: React.FC<{t0: number; t1: number; text: string; color: string; y: number; size?: number}> = ({t0, t1, text, color, y, size = 300}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const z = 1 + 0.06 * sp(t, t0 + text.length * 0.08 + 0.2, 12);
  return <div style={{position: 'absolute', top: y, left: 0, width: 1080, textAlign: 'center', transform: `scale(${z})`}}>
    {text.split('').map((c, i) => { const k = sp(t, t0 + i * 0.08, 9);
      return <span key={i} style={{display: 'inline-block', fontFamily: 'Pop', fontWeight: 700, fontSize: size, color, textShadow: `0 10px 40px rgba(0,0,0,0.7), 0 0 50px ${color}88`, transform: `translateY(${(1 - k) * -400}px)`, opacity: Math.min(1, k * 2)}}>{c}</span>; })}
  </div>;
};
const Flash: React.FC<{t0: number}> = ({t0}) => { const t = useT(); if (t < t0 || t > t0 + 0.4) return null;
  return <AbsoluteFill style={{background: '#fff', opacity: 0.85 * (1 - lin(t, t0, t0 + 0.4))}} />; };

export const Video: React.FC = () => {
  const t = useT();
  const s1 = pick(t, [[0, 'm_conv.png'], [13.25, 'm_menu.png'], [15.9, 'm_picker.png'], [18.62, 'm_typed.png'], [19.6, 'm_sent.png']]);
  const s2 = pick(t, [[0, 'c_page.png'], [32.95, 'c_ecran.png'], [34.5, 'c_full.png']]);
  const s3 = pick(t, [[0, 'k_num.png'], [51.84, 'k_zero.png'], [54.58, 'k_deg.png'], [54.95, 'k_done.png']]);
  const cur = t < 14.54 ? 1 : t < 16.84 ? 2 : t < 19.6 ? 3 : 4;
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE + HOOK */}
    <Scene t0={0} t1={5.4}>
      <Photo src="img_gateau.png" t0={0} t1={5.7} dim={0.25} />
      <Sent top={290} t0={2.0} t1={5.6} words={[[2.0, 'Peur d’oublier']]} size={62} />
      <Sent top={370} t0={2.0} t1={5.6} words={[[2.1, 'un anniversaire ?', YEL]]} size={62} />
      <Sent top={470} t0={2.7} t1={5.6} words={[[2.8, 'Ton iPhone'], [3.26, 'l’envoie']]} size={62} />
      <Sent top={550} t0={2.7} t1={5.6} words={[[4.08, 'à ta place', ELEC]]} size={62} />
      <Pill t0={4.76} x={540} y={1430} size={44} border={ELEC}>à l’heure que tu veux</Pill>
      <CoverTitle line="3 ASTUCES" keyword="CACHÉES" after="DANS TON IPHONE" />
    </Scene>

    {/* LES 3 ASTUCES */}
    <Scene t0={5.4} t1={10.4}>
      <Sent top={300} t0={5.5} t1={10.6} words={[[6.7, '3 astuces', ELEC], [6.88, 'cachées']]} size={84} />
      <Cards t0={6.7} on={8.32} />
      <Sent top={1360} t0={8.32} t1={10.6} words={[[8.32, 'On commence ?', GRN]]} size={56} />
    </Scene>

    {/* ASTUCE 1 : ENVOYER PLUS TARD */}
    <Scene t0={10.4} t1={20.2}>
      <List3 cur={cur} t0={10.5} />
      <StepTag n={cur > 3 ? 3 : cur} t0={10.5} />
      <Sent top={385} t0={11.98} t1={14.5} words={[[11.98, 'Ouvre'], [12.14, 'la conversation']]} size={62} />
      <Sent top={465} t0={12.9} t1={14.5} words={[[12.9, 'puis touche'], [13.22, 'le +', ELEC]]} size={62} />
      <Sent top={385} t0={15.24} t1={16.8} words={[[15.24, 'Choisis']]} size={62} />
      <Sent top={465} t0={15.54} t1={16.8} words={[[15.54, '« Envoyer plus tard »', ELEC]]} size={62} />
      <Sent top={385} t0={17.74} t1={20.3} words={[[17.74, 'Règle le jour'], [18.26, 'et l’heure', YEL]]} size={62} />
      <Sent top={465} t0={18.62} t1={20.3} words={[[18.62, 'écris,'], [19.44, 'envoie', GRN]]} size={62} />
      <ZoomPhone src={s1} t0={10.5} keys={[[10.55, 1, 300, 650], [12.6, 1.8, 140, 790], [13.3, 1.45, 250, 640], [15.95, 1.35, 300, 960], [18.5, 1.6, 300, 790], [19.6, 1.5, 360, 620]]}>
        <HiBox sx={D.plus[0]} sy={D.plus[1]} w={72} h={72} t0={12.9} t1={13.25} />
        <HiBox sx={D.m_later[0]} sy={D.m_later[1]} w={440} h={78} t0={15.4} t1={15.9} />
        <HiBox sx={D.picker[0]} sy={D.picker[1]} w={560} h={64} t0={17.74} t1={18.6} />
        <HiBox sx={D.send[0]} sy={D.send[1]} w={58} h={58} t0={19.2} t1={19.6} />
      </ZoomPhone>
    </Scene>

    {/* ET VOILÀ */}
    <Scene t0={20.2} t1={23.7}>
      <Sent top={290} t0={20.3} t1={23.9} words={[[20.82, 'Il part'], [21.14, 'tout seul', GRN]]} size={72} />
      <Sent top={385} t0={21.72} t1={23.9} words={[[21.72, 'même'], [22.08, 'iPhone éteint', YEL]]} size={60} />
      <Phone src="m_sent.png" x={540} top={520} w={400} t0={20.25} />
      <Stamp t0={20.35} text="ET VOILÀ !" color={GRN} x={540} y={1380} size={64} rot={-6} />
    </Scene>

    {/* ATTENTION : BULLES BLEUES + 14 JOURS */}
    <Scene t0={23.7} t1={28.2}>
      <Sent top={290} t0={23.9} t1={28.4} words={[[23.9, 'Attention', RED]]} size={78} />
      <Sent top={395} t0={24.66} t1={28.4} words={[[24.66, 'seulement'], [25.24, 'les bulles bleues', ELEC]]} size={56} />
      <BigBubble t0={25.24} y={600} color="#0A84FF" text="Entre iPhone" ok tc={25.8} />
      <BigBubble t0={25.5} y={820} color="#30B94D" text="SMS (Android)" ok={false} tc={25.65} />
      <DaysCard t0={26.9} />
    </Scene>

    {/* ASTUCE 2 : PLEINE PAGE */}
    <Scene t0={28.2} t1={32.3}>
      <Photo src="img_recette.png" t0={28.2} t1={32.6} dim={0.3} />
      <Pill t0={28.32} x={540} y={250} size={42} border={ELEC}>Astuce 2</Pill>
      <Sent top={330} t0={29.58} t1={32.5} words={[[29.58, 'Garde une recette'], [30.38, 'en entier', ELEC]]} size={60} />
      <Sent top={425} t0={31.02} t1={32.5} words={[[31.02, 'pas besoin de'], [31.6, '10 captures', RED]]} size={56} />
      <ShotPile t0={31.6} />
    </Scene>
    <Scene t0={32.3} t1={37.3}>
      <Sent top={300} t0={32.5} t1={34.1} words={[[32.5, 'Une seule'], [32.72, 'capture', ELEC]]} size={66} />
      <Sent top={300} t0={34.1} t1={35.7} words={[[34.1, 'puis'], [34.2, '« Pleine page »', ELEC]]} size={62} />
      <Sent top={300} t0={35.7} t1={37.5} words={[[35.76, 'Toute la page'], [36.6, 'd’un coup', GRN]]} size={62} />
      <ZoomPhone src={s2} t0={32.35} keys={[[32.4, 1, 300, 650], [33.4, 1.7, 400, 260], [35.6, 1.35, 470, 640]]}>
        <HiBox sx={D.tab_full[0]} sy={D.tab_full[1]} w={270} h={58} t0={33.8} t1={34.6} />
        <HiBox sx={531} sy={780} w={86} h={960} t0={35.8} t1={37.3} />
      </ZoomPhone>
      <Flash t0={32.86} />
      <Stamp t0={36.6} text="1 SEULE CAPTURE" color={GRN} x={540} y={1400} size={56} rot={-5} />
    </Scene>

    {/* PIÈGE : SEULEMENT CERTAINES APPLIS */}
    <Scene t0={37.3} t1={43.6}>
      <Sent top={280} t0={37.46} t1={43.8} words={[[37.46, 'Le piège', RED]]} size={78} />
      <Sent top={385} t0={38.34} t1={43.8} words={[[38.34, 'pas dans'], [38.74, 'toutes les applis', YEL]]} size={56} />
      <AppRows rows={[[39.56, 'Safari', true], [40.24, 'Notes', true], [40.66, 'Mail', true], [41.58, 'Instagram', false]]} />
    </Scene>

    {/* PARTAGE */}
    <Scene t0={43.6} t1={47.4}>
      <Photo src="img_recette.png" t0={43.6} t1={47.7} dim={0.35} />
      <Sent top={290} t0={43.74} t1={47.6} words={[[44.68, '100 captures', RED], [45.42, 'de la même recette ?']]} size={58} />
      <Pill t0={46.16} x={540} y={1400} size={48} border={ELEC}>Envoie-lui cette vidéo</Pill>
    </Scene>

    {/* ASTUCE 3 : DEGRÉ */}
    <Scene t0={47.4} t1={50.0}>
      <Photo src="img_froid.png" t0={47.4} t1={50.3} dim={0.3} />
      <Pill t0={47.62} x={540} y={250} size={42} border={ELEC}>Astuce 3</Pill>
      <Sent top={330} t0={48.96} t1={50.2} words={[[48.96, 'Le petit rond'], [49.48, 'des degrés', ELEC]]} size={62} />
      <BigLetters t0={49.48} t1={50.2} text="3°" color="#fff" y={620} size={300} />
    </Scene>
    <Scene t0={50.0} t1={55.2}>
      <Sent top={300} t0={50.04} t1={51.3} words={[[50.04, 'Passe sur'], [50.4, 'les chiffres', ELEC]]} size={62} />
      <Sent top={300} t0={51.38} t1={53.2} words={[[51.38, 'Appui long'], [52.3, 'sur le 0', ELEC]]} size={62} />
      <Sent top={300} t0={53.26} t1={55.4} words={[[53.26, 'Le ° apparaît,'], [54.58, 'glisse', GRN]]} size={62} />
      <ZoomPhone src={s3} t0={50.05} keys={[[50.1, 1, 300, 650], [51.1, 1.7, 430, 880], [55.0, 1.5, 300, 840]]}>
        <HiBox sx={D.k0[0]} sy={D.k0[1]} w={62} h={84} t0={51.38} t1={51.84} />
        <HiBox sx={D.pop_deg[0]} sy={D.pop_deg[1]} w={70} h={100} t0={53.26} t1={54.95} />
      </ZoomPhone>
    </Scene>

    {/* QUESTION */}
    <Scene t0={55.2} t1={58.1}>
      <Sent top={300} t0={55.3} t1={58.3} words={[[55.3, 'Laquelle'], [55.84, 'tu ne connaissais pas ?', YEL]]} size={60} />
      <Cards t0={55.5} />
      <Pill t0={56.76} x={540} y={1420} size={44} border={ELEC}>Dis-le en commentaire</Pill>
    </Scene>

    <EndScreen t0={58.1} t1={60.55} tEnd={63.0} tAbonne={60.72} tPour={61.18} tImmergee={62.1} />
    <Finish total={64.41} />
  </AbsoluteFill>;
};
