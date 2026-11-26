import React from 'react';
import {AbsoluteFill} from 'remotion';
import {useT, sp, lin, Scene, Phone, ZoomPhone, HiBox, pick, fontCss, ELEC, TS, CoverTitle, EndScreen, Finish, Caption, CapData, HookPunch} from './lib';
import cap from './st_s2.json';
// « Au secours » v2 (26/11/2026) : refaite de zéro (TikTok avait jugé la v1 « non originale »).
// Style sobre : fond noir, blanc + un seul bleu, écrans en mode sombre, voix Yanis, sous-titres mot à mot.
export const S2_TOTAL = 61.15;

// fond noir + une seule lueur bleue qui respire
const Night: React.FC = () => { const t = useT();
  return <AbsoluteFill style={{background: '#040406'}}>
    <div style={{position: 'absolute', left: 540 - 520, top: 1000 - 520 + 30 * Math.sin(t * 0.5), width: 1040, height: 1040, borderRadius: '50%', background: 'radial-gradient(circle, rgba(47,91,255,0.28), transparent 65%)', filter: 'blur(40px)'}} />
  </AbsoluteFill>; };

// en-tête sobre : petite ligne en capitales espacées + titre blanc (mot clé bleu)
const Head: React.FC<{t0: number; t1: number; tag: string; a: string; b?: string; c?: string}> = ({t0, t1, tag, a, b, c}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const k = sp(t, t0, 15); const o = lin(t, t1 - 0.25, t1);
  return <div style={{position: 'absolute', top: 250, left: 60, width: 860, textAlign: 'center', opacity: Math.min(1, k * 1.6) * (1 - o), transform: `translateY(${(1 - k) * 30}px)`}}>
    <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 32, letterSpacing: 9, color: ELEC}}>{tag}</div>
    <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 64, lineHeight: 1.12, color: '#fff', marginTop: 14, textShadow: TS}}>{a}{b && <span style={{color: ELEC}}>{b}</span>}{c}</div>
  </div>;
};

export const Video: React.FC = () => {
  const t = useT();
  const scr = pick(t, [[9.0, 's2_reg.png'], [11.5, 's2_fid0.png'], [13.76, 's2_fid1.png'], [17.0, 's2_all.png'], [19.3, 's2_menu.png'], [20.8, 's2_d0.png'],
    [24.02, 's2_d1.png'], [24.98, 's2_d2.png'], [26.2, 's2_d3.png'], [27.48, 's2_d4.png'], [28.74, 's2_d5.png'], [30.2, 's2_d6.png'], [32.6, 's2_load.png'], [33.3, 's2_sc.png'], [35.4, 's2_name.png']]);
  const hero = t < 4.0 ? 's2_siri.png' : 's2_done.png';
  const res = t < 39.5 ? 's2_siri.png' : 's2_done.png';
  return <AbsoluteFill style={{background: '#040406'}}>
    <style>{fontCss}</style>
    <Night />

    {/* COUVERTURE + ACCROCHE : l'iPhone verrouillé qui écoute « Dis Siri » puis qui a tout fait */}
    <Scene t0={0} t1={8.9}>
      <Phone src={hero} x={540} top={560} w={500} tilt={6} />
      <Head t0={4.04} t1={8.9} tag={t < 7.42 ? 'DEPUIS iOS 27' : 'EN 2 MINUTES'} a={t < 7.42 ? 'Ton iPhone ' : 'Voilà comment '} b={t < 7.42 ? 'prépare tout' : 'le régler'} />
      <HookPunch t1={3.95} top={250} size={92} words={[[2.2, 'Une seule'], [2.48, 'phrase'], [3.08, 'et tes proches'], [3.62, 'sont prévenus', ELEC]]} />
      {t < 2.0 && <AbsoluteFill style={{background: `rgba(0,0,0,${0.45 * (1 - lin(t, 1.6, 2.0))})`}} />}
      <CoverTitle line="SI TU TOMBES, DIS JUSTE" keyword="ÇA" size={96} />
    </Scene>

    {/* ÉTAPES : un seul iPhone, la caméra plonge sur chaque bouton */}
    <Scene t0={9.0} t1={36.2}>
      <Head t0={9.1} t1={17.0} tag="ÉTAPE 1" a="Face ID et code › " b="Siri" />
      <Head t0={17.0} t1={20.8} tag="ÉTAPE 2" a="Raccourcis › " b="Décrire" />
      <Head t0={20.8} t1={34.5} tag="ÉTAPE 3" a="Écris ce qu’il " b="doit faire" />
      <Head t0={34.5} t1={36.3} tag="ÉTAPE 4" a="Renomme-le " b="« Au secours »" />
      <ZoomPhone src={scr} t0={9.05} keys={[[9.0, 1, 300, 650], [10.2, 1.7, 300, 890], [11.5, 1.3, 300, 450], [12.6, 1.8, 300, 587], [14.5, 1, 300, 650],
        [17.6, 1.9, 520, 140], [19.3, 1.5, 300, 960], [20.8, 1.45, 300, 480], [32.0, 1.8, 480, 760], [32.6, 1, 300, 650], [34.9, 1.8, 300, 160], [36.0, 1, 300, 650]]}>
        <HiBox sx={300} sy={890} w={556} h={62} t0={10.4} t1={11.5} />
        <HiBox sx={300} sy={587} w={556} h={62} t0={12.9} t1={14.5} />
        <HiBox sx={550} sy={110} w={66} h={66} t0={18.62} t1={19.3} />
        <HiBox sx={300} sy={946} w={540} h={112} t0={19.6} t1={20.8} />
        <HiBox sx={522} sy={792} w={58} h={58} t0={32.22} t1={32.6} />
        <HiBox sx={300} sy={110} w={320} h={56} t0={35.0} t1={36.2} />
      </ZoomPhone>
    </Scene>

    {/* RÉSULTAT */}
    <Scene t0={36.3} t1={40.9}>
      <Head t0={36.36} t1={40.9} tag="ET VOILÀ" a="« Dis Siri, " b="au secours »" />
      <Phone src={res} x={540} top={560} w={460} t0={36.3} />
    </Scene>

    {/* LE PIÈGE : la permission */}
    <Scene t0={41.0} t1={51.7}>
      <Head t0={41.0} t1={51.7} tag="LE PIÈGE" a={t < 47.0 ? 'Il demande ' : 'Fais un essai '} b={t < 47.0 ? 'la permission' : 'maintenant'} />
      <ZoomPhone src={t < 42.5 ? 's2_lock.png' : 's2_allow.png'} t0={41.05} keys={[[41.0, 1, 300, 650], [43.4, 1.35, 300, 680], [50.2, 1.9, 300, 774]]}>
        <HiBox sx={300} sy={774} w={480} h={64} t0={50.5} t1={51.7} />
      </ZoomPhone>
    </Scene>

    {/* PARTAGE */}
    <Scene t0={51.76} t1={54.0}>
      <div style={{position: 'absolute', top: 640, left: 60, width: 960, textAlign: 'center', fontFamily: 'Pop', fontWeight: 700, fontSize: 86, lineHeight: 1.15, color: '#fff', textShadow: TS,
        transform: `scale(${0.9 + 0.1 * sp(t, 51.8, 13)})`, opacity: Math.min(1, sp(t, 51.8, 13) * 1.5)}}>
        Envoie-la à quelqu’un qui <span style={{color: ELEC}}>vit seul</span></div>
    </Scene>

    <Caption data={cap as CapData} from={4.0} until={53.95} top={1290} />
    <EndScreen t0={54.0} t1={56.4} tEnd={58.8} tAbonne={56.5} tPour={57.3} tImmergee={57.88} />
    <Finish total={S2_TOTAL} />
  </AbsoluteFill>;
};
