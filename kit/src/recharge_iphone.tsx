import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {useT, sp, lin, Sent, Background, Glass, Icon, Scene, Phone, StepTag, HiBox, Stamp, Pill, Photo, Glow, fontCss, ELEC, RED, GRN, YEL, ORG, CoverTitle, EndScreen, Finish, W} from './lib';
// Vidéo « Recharger un iPhone avec un autre iPhone » (USB-C, iPhone 15+), 21/11/2026.
// Les temps sont ceux de la voix d'origine ; m() ajoute les pauses (0,42 s) et le bonus.
const CUTS = [5.45, 9.04, 11.0, 12.95, 17.05, 18.36, 19.38, 23.0, 24.3, 29.25, 31.88, 34.6, 39.0, 42.8, 45.48, 47.25, 49.4];
const P = 0.42, BON = 31.88, BLEN = 6.0, DUR = 70.47;
const m = (s: number) => s + P * CUTS.filter((c) => c < s).length + (s > BON ? BLEN + P : 0);
const bo = (s: number) => m(BON) + P + s; // temps dans le bonus
const MS: React.FC<{top: number; t0: number; t1: number; words: W[]; size?: number; b?: boolean}> = ({top, t0, t1, words, size, b}) => {
  const f = b ? bo : m;
  return <Sent top={top} t0={f(t0)} t1={f(t1)} words={words.map(([a, w, c]) => [f(a), w, c] as W)} size={size} />;
};

// câble USB-C (SVG) : chemin entre deux points, dessiné progressivement, avec des points d'énergie
const bez = (p: number[][], u: number) => { const q = 1 - u; return [0, 1].map((i) => q * q * q * p[0][i] + 3 * q * q * u * p[1][i] + 3 * q * u * u * p[2][i] + u * u * u * p[3][i]); };
const Cable: React.FC<{pts: number[][]; draw: number; flow?: number; dir?: 1 | -1; plugs?: boolean; color?: string}> = ({pts, draw, flow = -1, dir = 1, plugs = true, color = GRN}) => {
  const t = useT(); const d = `M${pts[0]} C${pts[1]} ${pts[2]} ${pts[3]}`;
  const dots = flow >= 0 && t > flow ? Array.from({length: 7}).map((_, i) => { let u = ((t - flow) * 0.45 + i / 7) % 1; if (dir < 0) u = 1 - u; return bez(pts, u); }) : [];
  const plug = (x: number, y: number, k: number) => <g opacity={k}><rect x={x - 22} y={y - 6} width={44} height={46} rx={10} fill="#f2f2f5" /><rect x={x - 13} y={y - 26} width={26} height={24} rx={7} fill="#b9bcc6" /><rect x={x - 7} y={y - 20} width={14} height={8} rx={3} fill="#555" /></g>;
  return <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
    <path d={d} stroke="#e9e9ee" strokeWidth={16} fill="none" strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - draw} style={{filter: 'drop-shadow(0 8px 14px rgba(0,0,0,0.5))'}} />
    {plugs && plug(pts[0][0], pts[0][1], Math.min(1, draw * 4))}{plugs && plug(pts[3][0], pts[3][1], draw > 0.98 ? 1 : 0)}
    {dots.map(([x, y], i) => <circle key={i} cx={x} cy={y} r={11} fill={color} style={{filter: `drop-shadow(0 0 12px ${color})`}} />)}
  </svg>;
};
const Badge: React.FC<{t0: number; x: number; y: number; text: string; color: string; label?: string}> = ({t0, x, y, text, color, label}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12);
  return <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${k})`, textAlign: 'center'}}>
    {label && <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 30, color: 'rgba(210,220,255,0.9)', marginBottom: 6, whiteSpace: 'nowrap'}}>{label}</div>}
    <div style={{background: color, borderRadius: 30, padding: '6px 26px', fontFamily: 'Pop', fontWeight: 700, fontSize: 46, color: '#fff', boxShadow: `0 0 30px ${color}`, whiteSpace: 'nowrap'}}>{text}</div></div>;
};
// carte téléphone (icône 3D + titre + pourcentage)
const PCard: React.FC<{t0: number; x: number; y: number; title: string; sub: string; color: string; icon?: string; tag?: string; tagT?: number}> = ({t0, x, y, title, sub, color, icon = 'mobile_phone_3d.png', tag, tagT = 999}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12);
  return <Glass style={{left: x, top: y, width: 380, height: 450, transform: `scale(${k})`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 12, border: `3px solid ${color}`, boxShadow: `0 0 40px ${color}55`}}>
    <Img src={staticFile(icon)} style={{width: 160, height: 160, filter: 'drop-shadow(0 16px 20px rgba(0,0,0,0.5))'}} />
    <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 42, color: '#fff', whiteSpace: 'nowrap'}}>{title}</div>
    <div style={{fontFamily: 'Int', fontWeight: 700, fontSize: 38, color}}>{sub}</div>
    {t >= tagT && <div style={{marginTop: 6, background: color, borderRadius: 24, padding: '4px 22px', fontFamily: 'Pop', fontWeight: 700, fontSize: 36, color: '#fff', transform: `scale(${sp(t, tagT, 11)})`, boxShadow: `0 0 26px ${color}`}}>{tag}</div>}
  </Glass>;
};
// batterie externe dessinée (lavande, anneau sans fil, dragonne rouge)
const PowerBank: React.FC<{t0: number; tPose: number}> = ({t0, tPose}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 13); const pk = sp(t, tPose, 12); const glow = t > tPose ? 0.5 + 0.5 * Math.sin(t * 4) : 0;
  return <div style={{position: 'absolute', left: 540 - 230, top: 640, width: 460, height: 780, transform: `scale(${k})`}}>
    <div style={{position: 'absolute', left: -70, top: 60, width: 120, height: 60, borderRadius: 30, border: '14px solid #ff4d3d', boxSizing: 'border-box'}} />
    <div style={{position: 'absolute', inset: 0, borderRadius: 90, background: 'linear-gradient(145deg,#b7c3f3,#8ea0e6 55%,#7486d6)', boxShadow: '0 50px 100px rgba(0,0,0,0.6), inset 0 3px 0 rgba(255,255,255,0.5)'}} />
    <div style={{position: 'absolute', left: 130, top: 380, width: 200, height: 200, borderRadius: '50%', border: '18px solid #e9ecf5', boxShadow: `0 0 ${30 + 40 * glow}px rgba(52,199,89,${0.3 + 0.6 * glow})`}} />
    <div style={{position: 'absolute', left: 175, top: 140, width: 110, height: 110, borderRadius: '50%', background: '#9fb0ee', boxShadow: 'inset 0 4px 10px rgba(0,0,0,0.2)'}} />
    {[0, 1, 2, 3].map((i) => <div key={i} style={{position: 'absolute', left: 175 + i * 32, top: 720, width: 14, height: 14, borderRadius: 7, background: '#7fd0ff', boxShadow: '0 0 12px #7fd0ff'}} />)}
    {t >= tPose - 0.6 && <div style={{position: 'absolute', left: 40, top: 40 - (1 - pk) * 500, opacity: Math.min(1, pk * 2)}}><Phone src="rc_lock_chg.png" x={190} top={20} w={330} float={false} /></div>}
  </div>;
};

export const Video: React.FC = () => {
  const t = useT();
  const chg = t >= m(16.14);
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE + HOOK */}
    <Scene t0={0} t1={m(5.45)}>
      <Photo src="img_rue.png" t0={0} t1={m(5.7)} dim={0.2} />
      <CoverTitle line="RECHARGE UN IPHONE AVEC" keyword="TON IPHONE" size={92} />
      <MS top={290} t0={2.0} t1={2.66} words={[[2.0, 'Presque'], [2.05, 'à plat ?', RED]]} size={80} />
      <MS top={290} t0={2.68} t1={5.6} words={[[2.68, 'Un iPhone 15'], [3.36, 'ou plus récent']]} size={62} />
      <MS top={385} t0={2.68} t1={5.6} words={[[4.06, 'peut te'], [4.3, 'recharger', GRN]]} size={72} />
      <Pill t0={m(4.84)} x={540} y={1330} size={54} border={GRN}>avec un simple câble</Pill>
    </Scene>

    {/* ÉTAPE 1 : le câble */}
    <Scene t0={m(5.45)} t1={m(9.04)}>
      <StepTag n={1} t0={m(5.54)} />
      <MS top={400} t0={5.5} t1={9.04} words={[[6.1, 'Prends un câble'], [6.58, 'USB-C', ELEC]]} size={62} />
      <MS top={485} t0={5.5} t1={9.04} words={[[7.02, 'des deux côtés', ELEC]]} size={58} />
      <Cable pts={[[260, 1000], [300, 1350], [780, 650], [820, 1000]]} draw={lin(t, m(6.3), m(7.2))} />
      <Pill t0={m(7.9)} x={540} y={1300} size={44}>celui de la boîte suffit</Pill>
    </Scene>

    {/* ÉTAPES 2 et 3 : on branche, on regarde */}
    <Scene t0={m(9.04)} t1={m(17.05)}>
      <StepTag n={t < m(11.36) ? 2 : 3} t0={t < m(11.36) ? m(9.12) : m(11.36)} />
      <MS top={400} t0={9.1} t1={11.0} words={[[9.86, 'Branche un bout']]} size={60} />
      <MS top={480} t0={9.1} t1={11.0} words={[[10.24, 'dans chaque iPhone', ELEC]]} size={58} />
      <MS top={400} t0={11.36} t1={12.95} words={[[12.08, 'Regarde'], [12.4, 'les deux écrans', ELEC]]} size={58} />
      <MS top={400} t0={13.08} t1={17.2} words={[[13.16, 'Le plus chargé'], [14.14, 'recharge', GRN]]} size={58} />
      <MS top={480} t0={13.08} t1={17.2} words={[[14.96, 'celui qui en a'], [15.44, 'le moins', RED]]} size={54} />
      <Phone src="rc_lock_ami.png" x={300} top={680} w={330} t0={m(9.2)} ph={0} />
      <Phone src={chg ? 'rc_lock_chg.png' : 'rc_lock_low.png'} x={780} top={680} w={330} t0={m(9.35)} ph={2}>
        <HiBox sx={300} sy={650} w={330} h={92} t0={m(16.2)} />
      </Phone>
      <Cable pts={[[300, 1370], [300, 1500], [780, 1500], [780, 1370]]} draw={lin(t, m(10.1), m(10.6))} flow={m(14.14)} plugs={false} />
      <Badge t0={m(13.3)} x={300} y={640} text="64 %" color={GRN} label="ton ami" />
      <Badge t0={m(13.9)} x={780} y={640} text={chg ? '3 %' : '2 %'} color={chg ? GRN : RED} label="toi" />
      {t > m(16.26) && <Icon src="high_voltage_3d.png" t0={m(16.26)} size={170} x={930} y={1250} />}
    </Scene>

    {/* RÉSULTAT */}
    <Scene t0={m(17.05)} t1={m(18.36)}>
      <Photo src="img_bar.png" t0={m(17.05)} t1={m(18.6)} dim={0.15} />
      <MS top={290} t0={17.1} t1={18.5} words={[[17.16, 'Et voilà,', GRN]]} size={80} />
      <MS top={400} t0={17.1} t1={18.5} words={[[17.62, 'soirée sauvée !']]} size={66} />
    </Scene>

    {/* COMMENT ÇA MARCHE */}
    <Scene t0={m(18.36)} t1={m(23.0)}>
      <Glow x={540} y={950} r={320} color="#3b2cff" />
      <Pill t0={m(18.38)} x={540} y={300} size={46}><Img src={staticFile('light_bulb_3d.png')} style={{width: 60, height: 60}} />Comment ça marche ?</Pill>
      <MS top={400} t0={19.4} t1={23.1} words={[[19.42, 'Les deux iPhone'], [19.98, 'se parlent', ELEC]]} size={58} />
      <MS top={480} t0={19.4} t1={23.1} words={[[20.88, 'et décident'], [21.6, 'qui donne', GRN], [22.34, 'qui reçoit', ELEC]]} size={50} />
      <PCard t0={m(19.5)} x={110} y={640} title="64 %" sub="plus de batterie" color={GRN} tag="DONNE" tagT={m(21.9)} />
      <PCard t0={m(19.7)} x={590} y={640} title="2 %" sub="moins de batterie" color={ELEC} tag="REÇOIT" tagT={m(22.54)} />
      <Icon src="speech_balloon_3d.png" t0={m(20.2)} size={150} x={540} y={600} />
      {t > m(21.9) && <Cable pts={[[300, 1100], [300, 1240], [780, 1240], [780, 1100]]} draw={1} flow={m(21.9)} plugs={false} />}
    </Scene>

    {/* PIÈGE LIGHTNING */}
    <Scene t0={m(23.0)} t1={m(29.25)}>
      <MS top={290} t0={23.05} t1={24.3} words={[[23.06, 'Attention,'], [23.74, 'un piège', RED]]} size={72} />
      <Icon src="warning_3d.png" t0={m(23.3)} size={300} x={540} y={900} float />
      <MS top={290} t0={24.4} t1={29.4} words={[[25.1, 'Un ancien iPhone'], [25.92, 'Lightning ?', YEL]]} size={56} />
      <MS top={380} t0={24.4} t1={29.4} words={[[26.92, 'Le récent'], [27.84, 'donne toujours', RED]]} size={56} />
      {t > m(24.35) && <>
        <PCard t0={m(25.0)} x={110} y={640} title="iPhone récent" sub="20 %" color={RED} tag="DONNE" tagT={m(27.84)} />
        <PCard t0={m(25.4)} x={590} y={640} title="Ancien iPhone" sub="80 %" color={YEL} tag="REÇOIT" tagT={m(28.24)} />
        {t > m(27.84) && <Cable pts={[[300, 1100], [300, 1240], [780, 1240], [780, 1100]]} draw={1} flow={m(27.84)} plugs={false} color={RED} />}
        <Pill t0={m(28.3)} x={540} y={1330} size={44} border={RED}>même s’il a moins de batterie</Pill>
      </>}
    </Scene>
    {/* LENT */}
    <Scene t0={m(29.25)} t1={m(31.88)}>
      <MS top={290} t0={29.3} t1={32.0} words={[[29.62, 'Ça charge'], [29.96, 'doucement', YEL]]} size={70} />
      <MS top={390} t0={29.3} t1={32.0} words={[[30.6, 'comme un vieux'], [31.18, 'petit chargeur']]} size={54} />
      <Icon src="turtle_3d.png" t0={m(29.96)} size={380} x={540} y={900} />
      <Pill t0={m(30.9)} x={540} y={1250} size={48} border={YEL}>environ 4,5 W</Pill>
    </Scene>

    {/* BONUS */}
    <Scene t0={m(31.88)} t1={bo(6.0) + 0.1}>
      <Glow x={540} y={950} r={300} color="#2c8a4a" />
      <MS b top={290} t0={0} t1={6.2} words={[[0.0, 'Petit bonus', GRN]]} size={76} />
      <MS b top={390} t0={0.8} t1={6.2} words={[[0.84, 'ça marche aussi avec']]} size={52} />
      <PCard t0={bo(1.62)} x={110} y={600} title="Écouteurs" sub="câble USB-C" color={ELEC} icon="headphone_3d.png" />
      <PCard t0={bo(2.34)} x={590} y={600} title="Montre" sub="son chargeur" color={ELEC} icon="watch_3d.png" />
      <Pill t0={bo(3.26)} x={540} y={1150} size={46}>avec le bon câble</Pill>
      <Pill t0={bo(5.04)} x={540} y={1290} size={46} border={GRN}>plus besoin de prise</Pill>
    </Scene>

    {/* PARTAGE */}
    <Scene t0={bo(6.0) + 0.1} t1={m(34.6)}>
      <Glow x={540} y={950} r={300} color="#4a2cff" />
      <MS top={290} t0={31.9} t1={34.8} words={[[32.16, 'Quelqu’un'], [32.82, 'toujours'], [32.98, 'à 2 % ?', RED]]} size={64} />
      <Icon src="mobile_phone_with_arrow_3d.png" t0={m(33.2)} size={340} x={540} y={880} />
      <Pill t0={m(33.52)} x={540} y={1230} size={50} border={ELEC}>Envoie-lui cette vidéo</Pill>
    </Scene>

    {/* PAS DE SANS-FIL */}
    <Scene t0={m(34.6)} t1={m(39.0)}>
      <Glow x={540} y={950} r={300} color="#8a2c3a" />
      <MS top={280} t0={34.7} t1={39.2} words={[[35.48, 'Contrairement à']]} size={50} />
      <MS top={355} t0={34.7} t1={39.2} words={[[35.92, 'certains Samsung']]} size={50} />
      <MS top={460} t0={34.7} t1={39.2} words={[[36.82, 'l’iPhone ne recharge pas']]} size={54} />
      <MS top={545} t0={34.7} t1={39.2} words={[[38.42, 'sans fil', RED]]} size={66} />
      <Icon src="mobile_phone_3d.png" t0={m(36.82)} size={300} x={380} y={900} float={false} />
      <Icon src="mobile_phone_3d.png" t0={m(37.1)} size={300} x={700} y={900} float={false} />
      <Icon src="prohibited_3d.png" t0={m(38.42)} size={260} x={540} y={900} />
    </Scene>

    {/* PRODUIT (version TikTok seulement : coupé pour Insta/YouTube) */}
    <Scene t0={m(39.0)} t1={m(42.8)}>
      <Photo src="img_batterie.png" t0={m(39.0)} t1={m(43.1)} dim={0.15} />
      <MS top={290} t0={39.1} t1={43.0} words={[[39.24, 'La solution :', GRN]]} size={66} />
      <MS top={385} t0={39.1} t1={43.0} words={[[40.44, 'une batterie'], [41.24, 'sans fil', ELEC], [41.8, '+ câble intégré']]} size={52} />
    </Scene>
    <Scene t0={m(42.8)} t1={m(47.25)}>
      <Glow x={540} y={1000} r={330} color="#5a3cff" />
      <MS top={290} t0={42.85} t1={47.4} words={[[42.92, 'Pose ton iPhone'], [43.54, 'dessus', ELEC]]} size={62} />
      <MS top={380} t0={42.85} t1={45.48} words={[[44.32, 'plus jamais'], [44.8, 'de câble oublié', GRN]]} size={52} />
      <MS top={380} t0={45.5} t1={47.4} words={[[45.94, 'Dispo dans le'], [46.6, 'panier orange', ORG]]} size={52} />
      <PowerBank t0={m(42.85)} tPose={m(43.3)} />
    </Scene>

    {/* QUESTION */}
    <Scene t0={m(47.25)} t1={m(49.4)}>
      <Glow x={540} y={950} r={300} color="#4a2cff" />
      <MS top={290} t0={47.3} t1={49.6} words={[[47.4, 'Et toi,'], [47.68, 'tu prêtes'], [47.9, 'ta batterie ?', YEL]]} size={60} />
      <Icon src="thinking_face_3d.png" t0={m(47.6)} size={300} x={540} y={850} />
      <Stamp t0={m(48.74)} text="OUI" color={GRN} x={330} y={1200} rot={-8} size={64} />
      <Stamp t0={m(49.02)} text="JAMAIS" color={RED} x={740} y={1200} rot={7} size={64} />
    </Scene>

    <EndScreen t0={m(49.4)} t1={m(52.0)} tEnd={DUR - 1.3} tAbonne={m(52.06)} tPour={m(52.48)} tImmergee={m(53.34)} />
    <Finish total={DUR} />
  </AbsoluteFill>;
};
