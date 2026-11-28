import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {useT, sp, lin, Scene, fontCss, ELEC, TS, Background, Photo, ZoomPhone, HiBox, CoverTitle, EndScreen, Finish, Caption, CapData, HookPunch, pick} from './lib';
import cap from './st_courses.json';
// Liste de courses papier -> Rappels rangée par rayon (28/11/2026), format COMPLICE (« Quoi ?! »)
export const CO_TOTAL = 61.09;

const Head: React.FC<{t0: number; t1: number; tag: string; a: string; b?: string; c?: string; size?: number}> = ({t0, t1, tag, a, b, c, size = 62}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const k = sp(t, t0, 15); const o = lin(t, t1 - 0.25, t1);
  return <div style={{position: 'absolute', top: 250, left: 60, width: 860, textAlign: 'center', opacity: Math.min(1, k * 1.6) * (1 - o), transform: `translateY(${(1 - k) * 30}px)`}}>
    <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 32, letterSpacing: 9, color: ELEC}}>{tag}</div>
    <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: size, lineHeight: 1.12, color: '#fff', marginTop: 14, textShadow: TS}}>{a}{b && <span style={{color: ELEC}}>{b}</span>}{c}</div>
  </div>;
};
const Big: React.FC<{t0: number; t1: number; top?: number; children: React.ReactNode; size?: number}> = ({t0, t1, top = 640, children, size = 86}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const k = sp(t, t0, 13); const o = lin(t, t1 - 0.25, t1);
  return <div style={{position: 'absolute', top, left: 60, width: 900, textAlign: 'center', fontFamily: 'Pop', fontWeight: 700, fontSize: size, lineHeight: 1.15, color: '#fff', textShadow: TS,
    transform: `scale(${0.9 + 0.1 * k})`, opacity: Math.min(1, k * 1.5) * (1 - o)}}>{children}</div>;
};
// notification iOS en verre qui tombe sur l'écran verrouillé (coordonnées écran 600x1300)
const Notif: React.FC<{t0: number; scale?: number}> = ({t0, scale = 1}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 11); const s = scale;
  return <div style={{position: 'absolute', left: 24 * s, top: (420 - (1 - k) * 380) * s, width: 552 * s, borderRadius: 34 * s, background: 'rgba(255,255,255,0.78)', backdropFilter: 'blur(20px)',
    boxShadow: `0 ${10 * s}px ${40 * s}px rgba(0,0,0,0.35)`, padding: `${22 * s}px ${24 * s}px`, boxSizing: 'border-box', display: 'flex', gap: 18 * s, alignItems: 'center', opacity: Math.min(1, k * 2)}}>
    <div style={{width: 70 * s, height: 70 * s, borderRadius: 16 * s, background: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
      <div style={{display: 'flex', flexDirection: 'column', gap: 6 * s}}>{['#FF9500', '#007AFF', '#FF3B30'].map((c) => <div key={c} style={{display: 'flex', gap: 5 * s, alignItems: 'center'}}><div style={{width: 10 * s, height: 10 * s, borderRadius: '50%', border: `${2.5 * s}px solid ${c}`}} /><div style={{width: 26 * s, height: 4 * s, borderRadius: 2, background: '#c7c7cc'}} /></div>)}</div></div>
    <div style={{fontFamily: 'Int'}}>
      <div style={{fontWeight: 700, fontSize: 26 * s, color: '#000'}}>Courses</div>
      <div style={{fontWeight: 600, fontSize: 24 * s, color: '#333'}}>« Lait » a été ajouté par Léa</div></div>
  </div>;
};

export const Video: React.FC = () => {
  const t = useT();
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE + ACCROCHE */}
    <Scene t0={0} t1={6.5}>
      <Photo src="c_photo.png" t0={0} t1={6.5} dim={0.35} />
      <HookPunch t1={6.4} top={250} size={86} words={[[2.6, 'Ta liste papier'], [3.9, 'rangée toute seule'], [5.0, 'par rayon', ELEC]]} />
      <CoverTitle line="TA LISTE DE COURSES" keyword="SE RANGE" after="TOUTE SEULE" size={88} />
    </Scene>

    {/* D'ABORD : Rappels > nouvelle liste > Type de liste : Courses */}
    <Scene t0={6.55} t1={14.85}>
      <Head t0={6.6} t1={10.85} tag="D’ABORD" a="Rappels › " b="Ajouter une liste" size={58} />
      <Head t0={10.9} t1={14.85} tag="LE RÉGLAGE QUI CHANGE TOUT" a="Type de liste : " b="Courses" />
      <ZoomPhone t0={6.6} src={pick(t, [[0, 'c_home.png'], [9.8, 'c_new0.png'], [11.3, 'c_new1.png'], [12.05, 'c_new2.png']])}
        keys={[[8.7, 1.7, 400, 180], [9.8, 1, 300, 650], [11.1, 1.55, 420, 650], [12.9, 1.3, 330, 520]]}>
        <HiBox sx={377} sy={127} w={86} h={78} t0={9.0} t1={9.8} />
        <HiBox sx={412} sy={712} w={318} h={80} t0={11.6} t1={12.05} />
        <HiBox sx={300} sy={545} w={540} h={90} t0={12.1} />
      </ZoomPhone>
    </Scene>

    {/* ENSUITE : appareil photo > texte en direct > Tout copier */}
    <Scene t0={14.9} t1={24.05}>
      <Head t0={14.95} t1={20.45} tag="ENSUITE" a="Vise ta liste avec " b="l’appareil photo" size={58} />
      <Head t0={20.5} t1={24.05} tag="TON IPHONE LIT TON ÉCRITURE" a="Touche " b="Tout copier" />
      <ZoomPhone t0={15.0} src={pick(t, [[0, 'c_cam0.png'], [18.3, 'c_cam1.png'], [20.75, 'c_cam2.png']])}
        keys={[[16.4, 1.35, 300, 480], [18.3, 1.7, 470, 820], [20.6, 1.6, 230, 800], [21.8, 1.35, 300, 480]]}>
        <HiBox sx={520} sy={900} w={86} h={86} t0={18.5} t1={20.75} />
        <HiBox sx={130} sy={900} w={216} h={68} t0={20.9} t1={21.8} />
      </ZoomPhone>
    </Scene>

    {/* À LA FIN : Nouveau rappel > Coller */}
    <Scene t0={24.1} t1={27.95}>
      <Head t0={24.15} t1={27.95} tag="À LA FIN" a="Nouveau rappel › " b="Coller" />
      <ZoomPhone t0={24.2} src={pick(t, [[0, 'c_list0.png'], [26.5, 'c_list1.png']])} keys={[[25.2, 1.7, 220, 300]]}>
        <HiBox sx={130} sy={366} w={160} h={64} t0={26.7} />
      </ZoomPhone>
    </Scene>

    {/* ET VOILÀ : rangé par rayon */}
    <Scene t0={28.0} t1={39.15}>
      <Head t0={28.05} t1={35.75} tag="ET VOILÀ" a="Tout se range " b="par rayon" />
      <Head t0={35.8} t1={39.15} tag="ET PLUS TARD ?" a="Il va dans " b="le bon rayon" />
      <ZoomPhone t0={28.1} src={pick(t, [[0, 'c_sorted.png'], [36.5, 'c_sorted2.png']])}
        keys={[[31.6, 1.45, 300, 390], [32.9, 1.45, 300, 620], [34.2, 1, 300, 650], [36.6, 1.5, 300, 680], [38.6, 1, 300, 650]]}>
        <HiBox sx={300} sy={360} w={560} h={220} t0={31.7} t1={32.95} />
        <HiBox sx={300} sy={604} w={560} h={220} t0={33.0} t1={34.3} />
        <HiBox sx={300} sy={742} w={560} h={56} t0={37.3} />
      </ZoomPhone>
    </Scene>

    {/* ATTENTION */}
    <Scene t0={39.2} t1={43.75}>
      <Head t0={39.25} t1={43.75} tag="ATTENTION" a="Écriture difficile ? " b="Vérifie avant" size={58} />
      <ZoomPhone t0={39.3} src="c_cam2.png" keys={[[39.6, 1.45, 300, 470]]} />
    </Scene>

    {/* BONUS : liste partagée */}
    <Scene t0={43.8} t1={50.05}>
      <Head t0={43.85} t1={50.05} tag="BONUS" a="Partage-la avec " b="ta famille" />
      <ZoomPhone t0={43.9} src="c_lock.png" keys={[[46.4, 1.3, 300, 560]]}>
        <Notif t0={46.8} scale={ZOOM_S} />
      </ZoomPhone>
    </Scene>

    {/* PARTAGE */}
    <Scene t0={50.1} t1={53.4}>
      <Big t0={50.15} t1={53.4} top={640}>Envoie-la à quelqu’un qui <span style={{color: ELEC}}>oublie</span> toujours la moitié des courses</Big>
    </Scene>
    {/* QUESTION FIN */}
    <Scene t0={53.45} t1={55.65}>
      <Big t0={53.5} t1={55.65} top={640} size={100}>T’en penses quoi ?</Big>
      <Big t0={54.5} t1={55.65} top={790} size={100}><span style={{color: ELEC}}>Tu connaissais ?</span></Big>
    </Scene>

    <Caption data={cap as CapData} from={2.0} until={55.65} top={1300} />
    <EndScreen t0={55.7} t1={57.95} tEnd={60.0} tAbonne={58.02} tPour={58.54} tImmergee={59.2} />
    <Finish total={CO_TOTAL} />
  </AbsoluteFill>;
};
const ZOOM_S = 1; // les enfants du Phone reçoivent l'échelle automatiquement
