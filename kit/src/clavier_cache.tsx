import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import data from './data.json';
import {useT, sp, lin, Sent, Background, Glass, Icon, Scene, ZoomPhone, Stamp, Pill, Glow, pick, fontCss, ELEC, RED, GRN, YEL, CoverTitle, EndScreen, Finish} from './lib';
const P: any = data;
// Vidéo « Ton clavier te cache un secret » (zones de touche invisibles qui grossissent), 20/11/2026.

// ---------- clavier dessiné (unités : 950 px de large) ----------
const KW = 86, GAP = 10, KH = 120, RG = 18;
const ROWS: [string, number][] = [['AZERTYUIOP', 0], ['QSDFGHJKLM', 0], ['WXCVBN\'', 150]];
type WF = (ch: string) => number;
const rowY = (r: number) => r * (KH + RG);
const zonesOf = (row: string, x0: number, wf: WF) => {
  const c = row.split('').map((_, i) => x0 + i * (KW + GAP) + KW / 2); const w = row.split('').map(wf);
  const b: number[] = [];
  for (let i = 0; i < row.length - 1; i++) b.push(c[i] + (c[i + 1] - c[i]) * w[i] / (w[i] + w[i + 1]));
  return row.split('').map((ch, i) => ({ch, l: i === 0 ? c[0] - (KW / 2 + 5) * Math.min(1, w[0]) : b[i - 1], r: i === row.length - 1 ? c[i] + KW / 2 + 5 : b[i], w: w[i]}));
};
const KeyCaps: React.FC<{alpha?: number; hi?: string}> = ({alpha = 1, hi}) => <>
  {ROWS.map(([row, x0], r) => row.split('').map((ch, i) => <div key={ch} style={{position: 'absolute', left: x0 + i * (KW + GAP), top: rowY(r), width: KW, height: KH, borderRadius: 16,
    background: ch === hi ? '#d8dcff' : `rgba(92,92,98,${alpha})`, boxShadow: `0 4px 0 rgba(0,0,0,${0.5 * alpha})`, display: 'flex', alignItems: 'center', justifyContent: 'center',
    fontFamily: 'Int', fontWeight: 600, fontSize: 52, color: ch === hi ? '#111' : `rgba(255,255,255,${alpha})`}}>{ch}</div>))}
  <div style={{position: 'absolute', left: 0, top: rowY(2), width: 140, height: KH, borderRadius: 16, background: `rgba(58,58,62,${alpha})`}} />
  <div style={{position: 'absolute', left: 822, top: rowY(2), width: 128, height: KH, borderRadius: 16, background: `rgba(58,58,62,${alpha})`}} />
</>;
const Zones: React.FC<{wf: WF; labels?: boolean; hot?: string[]; pExtra?: number}> = ({wf, labels = true, hot = [], pExtra = 0}) => <>
  {ROWS.map(([row, x0], r) => zonesOf(row, x0, wf).map((z) => {
    const big = z.w > 1.3, small = z.w < 0.8 && z.ch === 'W'; const col = small ? '255,69,58' : '90,140,255';
    const ex = z.ch === 'P' ? pExtra : 0;
    return <div key={z.ch} style={{position: 'absolute', left: z.l + 3, top: rowY(r) - 6, width: Math.max(6, z.r - z.l - 6), height: KH + 12 + ex, borderRadius: 22,
      background: `rgba(${col},${big ? 0.62 : small ? 0.3 : 0.16})`, border: `3px solid rgba(${col},${big || small || hot.includes(z.ch) ? 1 : 0.6})`,
      boxShadow: big ? `0 0 50px rgba(${col},0.9), inset 0 0 30px rgba(${col},0.5)` : `0 0 14px rgba(${col},0.4)`, zIndex: big ? 2 : 1,
      display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Pop', fontWeight: 700, fontSize: big ? 70 : 40, color: `rgba(255,255,255,${labels ? 0.9 : 0})`}}>{labels ? z.ch : ''}</div>;
  }))}
</>;
const one: WF = () => 1;

// vue éclatée : ce que tu vois / ce que tu touches
const Exploded: React.FC<{t0: number}> = ({t0}) => {
  const t = useT(); const k = sp(t, t0, 15); const sep = 300 * sp(t, 7.0, 16); const wob = lin(t, 11.3, 11.9);
  const wf: WF = (ch) => 1 + 0.75 * wob * Math.sin(t * 3.2 + ch.charCodeAt(0) * 1.7);
  const layer = (y: number, ch: React.ReactNode) => <div style={{position: 'absolute', left: 0, top: y, width: 950, height: 3 * KH + 2 * RG, transform: 'rotateX(58deg) rotateZ(-8deg)', transformStyle: 'preserve-3d'}}>{ch}</div>;
  return <div style={{position: 'absolute', left: 65, top: 690, width: 950, height: 700, perspective: 1800, transform: `scale(${0.9 * k})`, transformOrigin: '475px 300px', opacity: Math.min(1, k * 1.5)}}>
    {layer(260 + sep * 0.5, <div style={{opacity: lin(t, 7.0, 7.6)}}><Zones wf={wf} /></div>)}
    {layer(260 - sep * 0.5, <KeyCaps />)}
  </div>;
};

// clavier à plat, zones par-dessus
const FlatKB: React.FC<{top: number; wf: WF; zones: number; touch?: [number, number, number]; pExtra?: number; hi?: string}> = ({top, wf, zones, touch, pExtra = 0, hi}) => {
  const t = useT(); const k = sp(t, 0, 14);
  return <div style={{position: 'absolute', left: 60, top, width: 950, height: 420, transform: 'scale(0.9)', transformOrigin: '0 0'}}>
    <Glass style={{left: -24, top: -24, width: 998, height: 3 * KH + 2 * RG + 48, borderRadius: 40}} />
    <KeyCaps alpha={1 - 0.55 * zones} hi={hi} />
    <div style={{opacity: zones}}><Zones wf={wf} pExtra={pExtra} labels={false} /></div>
    {touch && t >= touch[2] && (() => { const q = sp(t, touch[2], 10); const p = lin(t, touch[2], touch[2] + 0.6);
      return <>
        <div style={{position: 'absolute', left: touch[0] - 46, top: touch[1] - 46, width: 92, height: 92, borderRadius: '50%', background: 'rgba(255,255,255,0.6)', border: '4px solid #fff', boxShadow: `0 0 40px ${ELEC}`, transform: `scale(${0.6 + 0.4 * q})`, zIndex: 5}} />
        <div style={{position: 'absolute', left: touch[0] - 46 - 60 * p, top: touch[1] - 46 - 60 * p, width: 92 + 120 * p, height: 92 + 120 * p, borderRadius: '50%', border: '5px solid #fff', opacity: 1 - p, zIndex: 5}} />
      </>; })()}
  </div>;
};
// coordonnées utiles
const CX = (i: number) => i * (KW + GAP) + KW / 2;
const pWF = (gp: number, gw: number): WF => (ch) => ch === 'P' ? 1 + 3.5 * gp : ch === 'W' ? 1 - 0.65 * gw : ch === 'O' ? 1 - 0.5 * gp : ch === 'I' ? 1 - 0.3 * gp : 1;

// zones lumineuses sur l'écran dessiné (coordonnées 600x1300)
const ScreenZones: React.FC<{t0: number; scale?: number}> = ({t0, scale = 1}) => {
  const t = useT(); if (t < t0) return null; const k = lin(t, t0, t0 + 0.6);
  return <>{'azertyuiopqsdfghjklmwxcvbn'.split('').map((ch, i) => { const [x, y] = P['k:' + ch]; const f = 0.5 + 0.5 * Math.sin(t * 5 + i * 1.3);
    return <div key={ch} style={{position: 'absolute', left: (x - 29) * scale, top: (y - 42) * scale, width: 58 * scale, height: 84 * scale, borderRadius: 12 * scale,
      border: `${2.5 * scale}px solid rgba(90,140,255,${(0.4 + 0.6 * f) * k})`, background: `rgba(47,91,255,${0.45 * f * k})`, boxShadow: `0 0 ${18 * scale}px rgba(47,91,255,${0.8 * k})`}} />; })}</>;
};
const Cap: React.FC<{t0: number; x: number; y: number; ch: string; color?: string; size?: number}> = ({t0, x, y, ch, color, size = 170}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 10);
  return <Glass style={{left: x - size / 2, top: y - size / 2, width: size, height: size, borderRadius: size * 0.24, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${k}) translateY(${(1 - k) * 40}px)`,
    background: color ? color : undefined, boxShadow: color ? `0 0 60px ${color}` : undefined, fontFamily: 'Pop', fontWeight: 700, fontSize: size * 0.55, color: '#fff'}}>{ch}</Glass>;
};
const WordRow: React.FC<{t0: number; y: number; pre: string; post: string}> = ({t0, y, pre, post}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12);
  return <div style={{position: 'absolute', left: 0, width: 800, top: y, textAlign: 'center', fontFamily: 'Pop', fontWeight: 700, fontSize: 64, color: '#fff', transform: `translateX(${(1 - k) * 80}px)`, opacity: Math.min(1, k * 1.5)}}>
    {pre}<span style={{color: YEL, textShadow: `0 0 24px ${YEL}`}}>p</span>{post}</div>;
};
const TypeCard: React.FC<{t0: number; top: number; parts: [number, string, string?][]; label?: string}> = ({t0, top, parts, label}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 13); const blink = Math.floor(t * 2.5) % 2 === 0;
  return <Glass style={{left: 140, top, width: 800, height: 150, borderRadius: 75, display: 'flex', alignItems: 'center', padding: '0 50px', boxSizing: 'border-box', transform: `scale(${k})`}}>
    {label && <div style={{position: 'absolute', top: -46, left: 40, fontFamily: 'Int', fontWeight: 600, fontSize: 30, color: 'rgba(200,210,255,0.85)'}}>{label}</div>}
    {parts.filter(([a]) => t >= a).map(([a, s, c], i) => <span key={i} style={{fontFamily: 'Int', fontWeight: 600, fontSize: 64, color: c || '#fff', whiteSpace: 'pre', textShadow: c ? `0 0 24px ${c}` : undefined}}>{s}</span>)}
    <span style={{width: 5, height: 70, marginLeft: 4, background: ELEC, opacity: blink ? 1 : 0}} />
  </Glass>;
};

export const Video: React.FC = () => {
  const t = useT();
  const scr = pick(t, P.EV as [number, string][]);
  const gp = sp(t, 28.3, 13), gw = sp(t, 32.0, 13);
  const pBound = (() => { const z = zonesOf('AZERTYUIOP', 0, pWF(1, 1)); return z[9].l; })();
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* ACCROCHE */}
    <Scene t0={0} t1={5.9}>
      <ZoomPhone src="kc_0.png" t0={-1} keys={[[0, 1.3, 300, 1010]]}><ScreenZones t0={2.6} /></ZoomPhone>
      <CoverTitle line="TON CLAVIER TE" keyword="CACHE" after="UN SECRET" size={100} />
      <Sent top={300} t0={2.0} t1={5.15} words={[[2.0, 'Un truc que tu ne'], [3.0, 'vois jamais', ELEC]]} size={70} />
      <Sent top={395} t0={2.0} t1={5.15} words={[[4.1, 'et qui t’aide'], [4.46, 'à chaque message']]} size={54} />
      <Sent top={330} t0={5.2} t1={6.1} words={[[5.26, 'Regarde'], [5.54, 'bien', YEL]]} size={90} />
    </Scene>

    {/* DÉCLIC : deux claviers */}
    <Scene t0={5.95} t1={13.0}>
      <Glow x={540} y={1100} r={320} color="#3b2cff" />
      <Sent top={290} t0={6.0} t1={8.6} words={[[6.06, 'Les touches que'], [6.56, 'tu vois', ELEC]]} size={66} />
      <Sent top={380} t0={6.0} t1={8.6} words={[[7.04, 'ne sont pas celles'], [7.82, 'que tu touches', YEL]]} size={58} />
      <Sent top={290} t0={8.65} t1={11.2} words={[[8.68, 'Juste en dessous :'], [9.5, 'un 2e clavier']]} size={62} />
      <Sent top={380} t0={8.65} t1={11.2} words={[[10.28, 'invisible', ELEC]]} size={80} />
      <Sent top={290} t0={11.25} t1={13.2} words={[[11.4, 'Il change'], [11.94, 'de forme', YEL]]} size={70} />
      <Sent top={385} t0={11.25} t1={13.2} words={[[12.26, 'pendant que tu écris']]} size={56} />
      <Exploded t0={6.1} />
      <Pill t0={7.4} x={300} y={660} size={36} border="#ffffff">ce que tu vois</Pill>
      <Pill t0={7.9} x={540} y={1440} size={36} border={ELEC}>ce que tu touches</Pill>
    </Scene>

    {/* EXEMPLE */}
    <Scene t0={13.0} t1={19.75}>
      <Sent top={290} t0={13.05} t1={13.9} words={[[13.08, 'Un'], [13.26, 'exemple', YEL]]} size={80} />
      <Sent top={290} t0={13.9} t1={15.85} words={[[13.92, 'Léa te demande :']]} size={64} />
      <Sent top={380} t0={13.9} t1={15.85} words={[[14.98, '« On dîne ce soir ? »', ELEC]]} size={58} />
      <Sent top={290} t0={15.9} t1={17.4} words={[[15.96, 'Tu réponds…']]} size={64} />
      <Sent top={380} t0={15.9} t1={17.4} words={[[16.84, '« pas le tem… »', ELEC]]} size={62} />
      <Sent top={290} t0={17.44} t1={19.95} words={[[17.44, 'Ton iPhone'], [18.64, 'devine', ELEC]]} size={74} />
      <Sent top={390} t0={17.44} t1={19.95} words={[[18.84, 'déjà la suite']]} size={60} />
      <ZoomPhone src={scr} t0={13.05} keys={[[13.4, 1, 300, 650], [14.2, 1.6, 230, 640], [15.8, 1.35, 300, 900]]} />
      <Icon src="crystal_ball_3d.png" t0={18.6} size={230} x={830} y={1320} />
    </Scene>

    {/* LISTE DE MOTS */}
    <Scene t0={19.75} t1={26.65}>
      <Glow x={540} y={950} r={300} color="#3b2cff" />
      <Pill t0={19.85} x={540} y={300}><Img src={staticFile('keyboard_3d.png')} style={{width: 60, height: 60}} />sa liste de mots</Pill>
      <Sent top={390} t0={20.0} t1={22.5} words={[[21.16, 'après T, E, M…']]} size={66} />
      <Sent top={390} t0={22.55} t1={26.9} words={[[22.58, 'presque toujours…'], [24.42, 'le P', ELEC]]} size={66} />
      <Cap t0={21.28} x={330} y={640} ch="T" />
      <Cap t0={21.94} x={540} y={640} ch="E" />
      <Cap t0={22.22} x={750} y={640} ch="M" />
      <Glass style={{left: 140, top: 820, width: 800, height: 560, opacity: lin(t, 22.4, 22.8)}} />
      {t < 24.42 && t > 22.6 && <Cap t0={22.6} x={540} y={1100} ch="?" size={200} />}
      <div style={{position: 'absolute', left: 140, top: 0}}>
        <WordRow t0={24.92} y={880} pre="tem" post="s" />
        <WordRow t0={25.32} y={980} pre="tem" post="ête" />
        <WordRow t0={26.04} y={1080} pre="tem" post="érature" />
      </div>
      {t >= 24.42 && t < 24.95 && <Cap t0={24.42} x={540} y={1100} ch="P" color={ELEC} size={220} />}
      {t >= 24.92 && <div style={{position: 'absolute', left: 140, top: 1220, width: 800, textAlign: 'center', fontFamily: 'Int', fontWeight: 600, fontSize: 34, color: 'rgba(200,210,255,0.8)', opacity: lin(t, 25.0, 25.5)}}>la lettre suivante = presque toujours P</div>}
    </Scene>

    {/* LA ZONE DU P GROSSIT */}
    <Scene t0={26.65} t1={33.7}>
      <Sent top={290} t0={26.7} t1={28.7} words={[[26.78, 'Discrètement,'], [27.7, 'il agrandit']]} size={64} />
      <Sent top={385} t0={26.7} t1={28.7} words={[[28.3, 'la zone du P', ELEC]]} size={72} />
      <Sent top={290} t0={28.74} t1={29.95} words={[[28.74, 'Elle devient'], [29.38, 'énorme', YEL]]} size={72} />
      <Sent top={290} t0={30.0} t1={33.9} words={[[30.08, 'Les lettres'], [30.92, 'improbables']]} size={64} />
      <Sent top={385} t0={30.0} t1={33.9} words={[[31.76, 'comme le W,', RED], [32.68, 'rétrécissent']]} size={58} />
      <FlatKB top={720} wf={pWF(gp, gw)} zones={lin(t, 26.8, 27.5)} pExtra={110 * gp} />
      <Stamp t0={29.4} text="ÉNORME" color={ELEC} x={540} y={1250} size={60} rot={-6} />
    </Scene>

    {/* RÉSULTAT */}
    <Scene t0={33.7} t1={43.6}>
      <Sent top={290} t0={33.75} t1={36.0} words={[[33.96, 'Résultat :', YEL], [34.48, 'ton doigt tombe'], [35.42, 'à côté…']]} size={54} />
      <Sent top={290} t0={36.0} t1={38.45} words={[[36.0, 'entre le O et le P…']]} size={60} />
      <Sent top={380} t0={36.0} t1={38.45} words={[[37.18, 'c’est quand même'], [37.68, 'le P', GRN]]} size={60} />
      <Sent top={290} t0={38.5} t1={43.8} words={[[38.52, 'Tu crois taper'], [39.36, 'juste…']]} size={62} />
      <Sent top={380} t0={38.5} t1={43.8} words={[[39.98, 'mais ton iPhone'], [41.1, 'rattrape', ELEC], [41.56, 'tes erreurs']]} size={52} />
      <TypeCard t0={33.8} top={520} parts={[[0, 'pas le tem'], [37.68, 'p', GRN]]} />
      <FlatKB top={790} wf={pWF(1, 1)} zones={1} pExtra={110} touch={[(CX(8) + pBound) / 2 + 30, KH / 2, 36.4]} />
      <Pill t0={42.16} x={540} y={1330} size={40} border={YEL}>des centaines de fois par jour</Pill>
    </Scene>

    {/* PARI RATÉ */}
    <Scene t0={43.6} t1={49.85}>
      <Sent top={290} t0={43.7} t1={47.05} words={[[43.78, 'C’est pour ça qu’un'], [45.5, 'prénom original', YEL]]} size={54} />
      <Sent top={380} t0={43.7} t1={47.05} words={[[46.2, 'ou un mot rare…']]} size={54} />
      <Sent top={290} t0={47.1} t1={50.05} words={[[47.1, 'sort avec la'], [47.34, 'mauvaise lettre', RED]]} size={56} />
      <Sent top={380} t0={48.3} t1={50.05} words={[[48.34, 'Ton iPhone a'], [48.88, 'mal parié', RED]]} size={56} />
      <TypeCard t0={43.9} top={620} label="Tu voulais écrire" parts={[[43.9, 'Salut Yaël']]} />
      <TypeCard t0={46.4} top={860} label="Ce qui s’écrit" parts={[[46.6, 'Salut '], [47.4, 'T', RED], [47.4, 'aël']]} />
      <Icon src="game_die_3d.png" t0={48.4} size={260} x={540} y={1210} />
      <Stamp t0={49.3} text="PARI RATÉ" color={RED} x={540} y={1400} size={56} />
    </Scene>

    {/* DÉFI */}
    <Scene t0={49.85} t1={55.7}>
      <Glow x={540} y={950} r={300} color="#4a2cff" />
      <Sent top={290} t0={49.9} t1={55.9} words={[[49.98, 'Petit'], [50.16, 'défi', YEL]]} size={90} />
      <Sent top={410} t0={51.1} t1={55.9} words={[[51.14, 'tape « tempw »'], [52.5, 'du premier coup', ELEC]]} size={50} />
      <TypeCard t0={51.3} top={620} parts={[[51.6, 't'], [51.75, 'e'], [51.9, 'm'], [52.0, 'p'], [52.15, 'w', RED]]} />
      <Icon src="speech_balloon_3d.png" t0={53.9} size={260} x={540} y={1030} />
      <Pill t0={53.9} x={540} y={1260} size={50} border={YEL}>T’y arrives ?</Pill>
      <Pill t0={54.6} x={540} y={1380} size={44}>Dis-le en commentaire</Pill>
    </Scene>

    <EndScreen t0={55.75} t1={58.1} tEnd={60.7} tAbonne={58.5} tPour={58.96} tImmergee={59.86} />
    <Finish total={61.97} />
  </AbsoluteFill>;
};
