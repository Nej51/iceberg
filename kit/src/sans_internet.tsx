import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {useT, sp, lin, Sent, Background, Glass, Icon, Scene, Phone, ZoomPhone, StepTag, HiBox, Stamp, Pill, Photo, Waves, pick, fontCss, ELEC, RED, GRN, YEL, CoverTitle, EndScreen, Finish} from './lib';
// Vidéo « 3 applis sans internet » (BitChat, Organic Maps, Kiwix), 23/11/2026.

const APPS = ['ic_bitchat.png', 'ic_organic.png', 'ic_kiwix.png'];
// checklist à gauche avec l'icône de chaque appli
const AppList: React.FC<{cur: number; t0: number}> = ({cur, t0}) => {
  const t = useT();
  return <div style={{position: 'absolute', left: 52, top: 660, display: 'flex', flexDirection: 'column', gap: 34}}>
    {APPS.map((src, i) => { const n = i + 1; const k = sp(t, t0 + i * 0.08, 12); const done = n < cur, on = n === cur; const p = 0.5 + 0.5 * Math.sin(t * 6);
      return <div key={n} style={{width: 92, height: 92, borderRadius: 26, position: 'relative', transform: `scale(${k})`, opacity: on || done ? 1 : 0.4,
        boxShadow: on ? `0 0 ${20 + 20 * p}px ${ELEC}` : done ? `0 0 20px ${GRN}` : 'none', border: `4px solid ${on ? ELEC : done ? GRN : 'rgba(255,255,255,0.25)'}`}}>
        <Img src={staticFile(src)} style={{width: '100%', height: '100%', borderRadius: 22}} />
        {done && <div style={{position: 'absolute', right: -14, bottom: -14, width: 44, height: 44, borderRadius: 22, background: GRN, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <svg width="28" height="28" viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6.5" stroke="#fff" strokeWidth="3.6" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg></div>}
      </div>; })}
  </div>;
};
// icône d'appli qui arrive avec un ressort (dans une carte en verre)
const AppCard: React.FC<{src: string; t0: number; x: number; y: number; s: number; check?: number}> = ({src, t0, x, y, s, check}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 11);
  return <div style={{position: 'absolute', left: x - s / 2, top: y - s / 2 + 8 * Math.sin(t * 2 + x), width: s, height: s, transform: `scale(${k}) rotate(${(1 - k) * -20}deg)`}}>
    <Img src={staticFile(src)} style={{width: s, height: s, borderRadius: s * 0.23, boxShadow: '0 25px 50px rgba(0,0,0,0.6), 0 0 40px rgba(47,91,255,0.5)', border: '3px solid rgba(255,255,255,0.3)'}} />
    {check !== undefined && t >= check && <div style={{position: 'absolute', right: -20, bottom: -20, width: s * 0.36, height: s * 0.36, borderRadius: '50%', background: GRN, boxShadow: `0 0 30px ${GRN}`, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${sp(t, check, 10)})`}}>
      <svg width={s * 0.24} height={s * 0.24} viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6.5" stroke="#fff" strokeWidth="3.6" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg></div>}
  </div>;
};
// mot géant lettre par lettre
const BigLetters: React.FC<{t0: number; t1: number; text: string; color: string; y: number; size?: number}> = ({t0, t1, text, color, y, size = 230}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const z = 1 + 0.06 * sp(t, t0 + text.length * 0.07 + 0.2, 12);
  return <div style={{position: 'absolute', top: y, left: 0, width: 1080, textAlign: 'center', transform: `scale(${z})`}}>
    {text.split('').map((c, i) => { const k = sp(t, t0 + i * 0.07, 9);
      return <span key={i} style={{display: 'inline-block', fontFamily: 'Pop', fontWeight: 700, fontSize: size, color, textShadow: `0 10px 40px rgba(0,0,0,0.7), 0 0 50px ${color}88`,
        transform: `translateY(${(1 - k) * -400}px)`, opacity: Math.min(1, k * 2)}}>{c}</span>; })}
  </div>;
};
// réseau de téléphones BitChat : nœuds + liens qui s'allument
const Node: React.FC<{x: number; y: number; t0: number}> = ({x, y, t0}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 11);
  return <Glass style={{left: x - 80, top: y - 80, width: 160, height: 160, borderRadius: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${k})`}}>
    <Img src={staticFile('ic_bitchat.png')} style={{width: 100, height: 100, borderRadius: 24}} /></Glass>;
};
const Link: React.FC<{a: [number, number]; b: [number, number]; t0: number}> = ({a, b, t0}) => {
  const t = useT(); if (t < t0) return null; const k = lin(t, t0, t0 + 0.5); const L = Math.hypot(b[0] - a[0], b[1] - a[1]); const ang = Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI;
  const dot = ((t - t0) * 0.8) % 1;
  return <div style={{position: 'absolute', left: a[0], top: a[1] - 4, width: L * k, height: 8, borderRadius: 4, background: ELEC, boxShadow: `0 0 24px ${ELEC}`, transformOrigin: '0 50%', transform: `rotate(${ang}deg)`}}>
    {k >= 1 && <div style={{position: 'absolute', left: dot * L - 12, top: -8, width: 24, height: 24, borderRadius: 12, background: '#fff', boxShadow: '0 0 20px #fff'}} />}</div>;
};
// carte « téléchargement impossible »
const NoDl: React.FC<{t0: number}> = ({t0}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12); const sh = Math.sin(t * 40) * 6 * (1 - lin(t, t0 + 0.4, t0 + 1.0));
  return <Glass style={{left: 140, top: 760, width: 800, height: 300, transform: `scale(${k}) translateX(${sh}px)`, display: 'flex', alignItems: 'center', gap: 40, padding: '0 50px', boxSizing: 'border-box', border: `3px solid ${RED}`, boxShadow: `0 0 40px ${RED}66`}}>
    <svg width="150" height="150" viewBox="0 0 24 24"><path d="M12 3v12M7 10l5 5 5-5M5 20h14" stroke="#fff" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" /><path d="M3 3l18 18" stroke={RED} strokeWidth="2.6" strokeLinecap="round" /></svg>
    <div><div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 54, color: '#fff', lineHeight: 1.1}}>Téléchargement</div>
      <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 54, color: RED, lineHeight: 1.1}}>impossible</div></div>
  </Glass>;
};

export const Video: React.FC = () => {
  const t = useT();
  const s1 = pick(t, [[0, 'si_bc_store.png'], [8.6, 'si_bc_chat.png']]);
  const s2 = pick(t, [[0, 'si_om_store.png'], [16.0, 'si_om_dl.png'], [17.3, 'si_om_dl_ok.png'], [17.84, 'si_om_map.png']]);
  const s3 = pick(t, [[0, 'si_kx_store.png'], [23.0, 'si_kx_lib.png'], [26.0, 'si_kx_art.png']]);
  const cur = t < 14.45 ? 1 : t < 21.2 ? 2 : t < 27.2 ? 3 : 4;
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE + HOOK */}
    <Scene t0={0} t1={6.45}>
      <Photo src="img_panne.png" t0={0} t1={6.75} dim={0.3} />
      <Sent top={290} t0={2.0} t1={6.6} words={[[2.0, 'Internet'], [2.2, 'et réseau'], [2.32, 'en panne ?', RED]]} size={66} />
      <Sent top={470} t0={2.74} t1={6.6} words={[[2.84, '3 applis', ELEC], [3.62, 'te sauvent', GRN]]} size={66} />
      <AppCard src="ic_bitchat.png" t0={2.84} x={270} y={1280} s={190} />
      <AppCard src="ic_organic.png" t0={3.1} x={540} y={1280} s={190} />
      <AppCard src="ic_kiwix.png" t0={3.36} x={810} y={1280} s={190} />
      <Pill t0={4.72} x={540} y={1460} size={44} border={ELEC}>à installer dès ce soir</Pill>
      <CoverTitle line="3 APPLIS SANS" keyword="INTERNET" />
    </Scene>

    {/* ÉTAPES : liste des 3 applis à gauche */}
    <Scene t0={6.45} t1={27.2}><AppList cur={cur} t0={6.5} /></Scene>

    {/* ÉTAPE 1 : BitChat */}
    <Scene t0={6.45} t1={10.7}>
      <StepTag n={1} t0={6.5} />
      <Sent top={400} t0={6.74} t1={7.7} words={[[6.74, 'BitChat', ELEC]]} size={70} />
      <Sent top={400} t0={7.72} t1={10.9} words={[[7.72, 'Des messages'], [8.84, 'sans réseau', GRN]]} size={60} />
      <Sent top={475} t0={9.4} t1={10.9} words={[[9.5, 'ni internet', GRN]]} size={60} />
      <ZoomPhone src={s1} t0={6.55} keys={[[6.6, 1, 300, 650], [7.1, 1.6, 230, 280], [8.6, 1, 300, 650]]}>
        <HiBox sx={307} sy={329} w={170} h={62} t0={7.5} t1={8.6} />
        <HiBox sx={300} sy={500} w={560} h={330} t0={9.0} t1={10.7} />
      </ZoomPhone>
    </Scene>
    <Scene t0={10.7} t1={14.45}>
      <Photo src="img_bt.png" t0={10.7} t1={14.75} dim={0.25} />
      <Sent top={290} t0={10.74} t1={14.6} words={[[11.12, 'Par le'], [11.54, 'Bluetooth', ELEC]]} size={74} />
      <Sent top={385} t0={10.74} t1={14.6} words={[[12.14, 'de téléphone'], [12.48, 'en téléphone']]} size={58} />
      <Pill t0={13.24} x={540} y={1440} size={44} border={ELEC}>avec les gens autour de toi</Pill>
    </Scene>

    {/* ÉTAPE 2 : Organic Maps */}
    <Scene t0={14.45} t1={21.2}>
      <StepTag n={2} t0={14.52} />
      <Sent top={400} t0={15.12} t1={16.0} words={[[15.12, 'Organic Maps', GRN]]} size={70} />
      <Sent top={400} t0={16.0} t1={17.84} words={[[16.06, 'Télécharge'], [17.0, 'ta région', ELEC]]} size={62} />
      <Sent top={475} t0={16.4} t1={17.84} words={[[16.46, 'à l’avance', YEL]]} size={56} />
      <Sent top={400} t0={17.84} t1={21.3} words={[[18.42, 'Carte,'], [18.96, 'recherche'], [19.58, 'et GPS', ELEC]]} size={58} />
      <Sent top={475} t0={20.2} t1={21.3} words={[[20.28, 'sans connexion', GRN]]} size={58} />
      <ZoomPhone src={s2} t0={14.55} keys={[[14.6, 1, 300, 650], [15.2, 1.6, 230, 280], [16.0, 1.35, 300, 560], [17.84, 1, 300, 650], [18.8, 1.5, 300, 160], [19.5, 1.4, 300, 760], [20.6, 1, 300, 650]]}>
        <HiBox sx={307} sy={329} w={170} h={62} t0={15.4} t1={16.0} />
        <HiBox sx={300} sy={567} w={560} h={82} t0={16.9} t1={17.84} />
        <HiBox sx={300} sy={103} w={560} h={70} t0={18.96} t1={19.5} />
        <HiBox sx={300} sy={760} w={150} h={150} t0={19.58} t1={20.6} />
      </ZoomPhone>
    </Scene>

    {/* ÉTAPE 3 : Kiwix */}
    <Scene t0={21.2} t1={27.2}>
      <StepTag n={3} t0={21.26} />
      <Sent top={400} t0={21.9} t1={23.0} words={[[22.0, 'Kiwix', ELEC]]} size={70} />
      <Sent top={400} t0={23.0} t1={26.0} words={[[23.24, 'Télécharge'], [23.64, 'Wikipédia', ELEC]]} size={62} />
      <Sent top={475} t0={24.1} t1={26.0} words={[[24.18, 'en entier'], [24.62, 'ou plus léger', YEL]]} size={52} />
      <Sent top={400} t0={26.0} t1={27.4} words={[[26.06, 'Lis'], [26.32, 'hors ligne', GRN]]} size={66} />
      <ZoomPhone src={s3} t0={21.3} keys={[[21.35, 1, 300, 650], [22.2, 1.6, 230, 280], [23.0, 1.3, 300, 480], [26.0, 1, 300, 650]]}>
        <HiBox sx={307} sy={329} w={170} h={62} t0={22.3} t1={23.0} />
        <HiBox sx={300} sy={320} w={560} h={116} t0={24.0} t1={24.62} />
        <HiBox sx={300} sy={440} w={560} h={116} t0={24.62} t1={25.28} />
        <HiBox sx={300} sy={560} w={560} h={116} t0={25.28} t1={26.0} />
      </ZoomPhone>
    </Scene>

    {/* ET VOILÀ */}
    <Scene t0={27.2} t1={29.45}>
      <Sent top={300} t0={27.3} t1={29.6} words={[[27.66, 'Ton iPhone'], [28.24, 'reste utile', GRN]]} size={72} />
      <AppCard src="ic_bitchat.png" t0={27.5} x={240} y={850} s={220} check={27.9} />
      <AppCard src="ic_organic.png" t0={27.65} x={540} y={850} s={220} check={28.05} />
      <AppCard src="ic_kiwix.png" t0={27.8} x={840} y={850} s={220} check={28.2} />
      <Stamp t0={27.3} text="ET VOILÀ !" color={GRN} x={540} y={1250} size={64} rot={-6} />
    </Scene>

    {/* COMMENT ÇA MARCHE */}
    <Scene t0={29.45} t1={34.5}>
      <Photo src="img_rando.png" t0={29.45} t1={34.8} dim={0.2} />
      <Sent top={290} t0={29.5} t1={31.0} words={[[29.5, 'Comment'], [29.92, 'ça marche ?', YEL]]} size={74} />
      <Sent top={290} t0={31.02} t1={34.6} words={[[31.16, 'Le GPS capte'], [32.4, 'les satellites', ELEC]]} size={62} />
      <Sent top={380} t0={32.9} t1={34.6} words={[[33.0, 'pas besoin'], [33.32, 'd’internet', GRN]]} size={62} />
      <Icon src="satellite_3d.png" t0={32.0} size={220} x={800} y={600} />
    </Scene>
    <Scene t0={34.5} t1={38.6}>
      <Sent top={290} t0={34.6} t1={38.8} words={[[35.0, 'Ce qui manque :'], [36.08, 'la carte', YEL]]} size={66} />
      <Phone src="si_om_map.png" x={540} top={470} w={430} t0={34.6} />
      <Stamp t0={37.62} text="DÉJÀ DANS TON IPHONE" color={GRN} x={540} y={1380} size={50} rot={-5} />
    </Scene>

    {/* PIÈGE */}
    <Scene t0={38.6} t1={44.9}>
      <Sent top={280} t0={38.76} t1={40.5} words={[[38.76, 'Attention,'], [39.4, 'un piège', RED]]} size={74} />
      <Sent top={280} t0={40.5} t1={45.1} words={[[40.54, 'Tout se prépare'], [41.12, 'avant', YEL]]} size={66} />
      <BigLetters t0={41.12} t1={42.4} text="AVANT" color={YEL} y={750} />
      <Sent top={370} t0={42.4} t1={45.1} words={[[42.4, 'Une fois coupé…', RED]]} size={58} />
      <NoDl t0={42.72} />
      <Stamp t0={43.84} text="TROP TARD" color={RED} x={540} y={1250} size={64} rot={-6} />
    </Scene>

    {/* LIMITES DE BITCHAT */}
    <Scene t0={44.9} t1={52.2}>
      <Sent top={280} t0={45.24} t1={52.4} words={[[45.42, 'BitChat parle'], [46.06, 'qu’à BitChat', ELEC]]} size={62} />
      <Waves cx={250} cy={820} t0={47.74} color={ELEC} r0={90} />
      <Link a={[250, 820]} b={[540, 960]} t0={48.2} />
      <Link a={[540, 960]} b={[830, 1100]} t0={49.56} />
      <Node x={250} y={820} t0={46.78} />
      <Node x={540} y={960} t0={48.2} />
      <Node x={830} y={1100} t0={49.56} />
      <Pill t0={48.2} x={540} y={600} size={42}>quelques dizaines de mètres</Pill>
      <Pill t0={49.56} x={560} y={1260} size={40} border={ELEC}>+ loin grâce aux relais</Pill>
      <Stamp t0={51.02} text="N’APPELLE PAS LES SECOURS" color={RED} x={540} y={1410} size={44} rot={-5} />
    </Scene>

    {/* PARTAGE */}
    <Scene t0={52.2} t1={58.3}>
      <Photo src="img_bt.png" t0={52.2} t1={58.6} dim={0.25} />
      <Sent top={290} t0={52.32} t1={58.5} words={[[52.32, 'Bon réflexe :', GRN]]} size={70} />
      <Sent top={385} t0={52.9} t1={58.5} words={[[53.0, 'installe-la'], [53.62, 'chez tes proches', ELEC]]} size={58} />
      <Pill t0={54.78} x={540} y={1400} size={46} border={ELEC}>Envoie-leur cette vidéo</Pill>
    </Scene>

    <EndScreen t0={58.3} t1={60.58} tEnd={63.04} tAbonne={60.84} tPour={61.3} tImmergee={62.14} />
    <Finish total={64.23} />
  </AbsoluteFill>;
};
