import React from 'react';
import {AbsoluteFill, Img, staticFile, interpolate} from 'remotion';
import {useT, sp, lin, C, Sent, Background, Glass, Icon, Scene, Phone, ZoomPhone, StepTag, Checklist, HiBox, Stamp, Pill, Photo, Glow, pick, fontCss, ELEC, RED, GRN, YEL, CoverTitle, EndScreen, Finish} from './lib';
// Vidéo « Double capture : filmer avec les deux caméras » (iPhone 17+), 22/11/2026.

// petite fenêtre (caméra avant) qu'on fait glisser avec le doigt, dans l'écran 600x1300
const DragPip: React.FC<{scale?: number}> = ({scale = 1}) => {
  const t = useT();
  const k = interpolate(t, [29.2, 30.2, 30.6, 31.3], [0, 1, 1, 1], {...C, easing: (x) => x * x * (3 - 2 * x)});
  const x = 383 + (20 - 383) * k, y = 110 + 70 * Math.sin(k * Math.PI) * 0.6 + 40 * k;
  const press = t > 28.9 && t < 30.5;
  return <>
    <Img src={staticFile('dc_pip.png')} style={{position: 'absolute', left: x * scale, top: y * scale, width: 198 * scale, height: 265 * scale, transform: press ? 'scale(1.06)' : undefined, filter: press ? 'drop-shadow(0 0 18px rgba(47,91,255,0.9))' : undefined}} />
    {t > 28.7 && t < 30.9 && <div style={{position: 'absolute', left: (x + 99) * scale - 30 * scale, top: (y + 150) * scale - 30 * scale, width: 60 * scale, height: 60 * scale, borderRadius: '50%', background: 'rgba(255,255,255,0.55)', border: `${3 * scale}px solid #fff`, boxShadow: '0 0 30px rgba(47,91,255,0.9)'}} />}
  </>;
};

// carte image (plans de coupe en vignettes)
const ImgCard: React.FC<{src: string; t0: number; x: number; y: number; w: number; h: number; label: string; rot?: number}> = ({src, t0, x, y, w, h, label, rot = 0}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12);
  return <div style={{position: 'absolute', left: x, top: y + (1 - k) * 120 + 8 * Math.sin(t * 2 + x), width: w, transform: `rotate(${rot * k}deg) scale(${0.7 + 0.3 * k})`, opacity: Math.min(1, k * 1.5)}}>
    <div style={{width: w, height: h, borderRadius: 34, overflow: 'hidden', border: '2px solid rgba(255,255,255,0.3)', boxShadow: '0 30px 70px rgba(0,0,0,0.6)'}}>
      <Img src={staticFile(src)} style={{width: w, height: h, objectFit: 'cover'}} /></div>
    <div style={{textAlign: 'center', marginTop: 18, fontFamily: 'Pop', fontWeight: 700, fontSize: 40, color: '#fff', whiteSpace: 'nowrap'}}>{label}</div></div>;
};

// mini cadre vidéo (caméra arrière + fenêtre) pour le piège
const MiniFrame: React.FC<{t0: number; merged: number; x: number; y: number}> = ({t0, merged, x, y}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12);
  const off = (1 - merged) * 130;
  return <div style={{position: 'absolute', left: x, top: y, width: 330, height: 586, transform: `scale(${k})`}}>
    <div style={{position: 'absolute', inset: 0, borderRadius: 40, overflow: 'hidden', border: '2px solid rgba(255,255,255,0.35)', boxShadow: '0 30px 70px rgba(0,0,0,0.6)'}}>
      <Img src={staticFile('dc_rear.png')} style={{width: 330, height: 715, marginTop: -60}} /></div>
    <Img src={staticFile('dc_pip.png')} style={{position: 'absolute', left: 205 + off, top: 30 - off * 0.5, width: 108, height: 145, filter: `drop-shadow(0 10px 20px rgba(0,0,0,0.6))`}} />
  </div>;
};

// rangée de zoom 0,5 · 1× · 2 · 4 · 8 qui s'allume au rythme de la voix
const ZoomRow: React.FC<{t0: number; y: number}> = ({t0, y}) => {
  const t = useT(); const L = ['0,5', '1×', '2', '4', '8']; const T = [45.0, 45.3, 45.6, 45.9, 46.2];
  let on = 1; T.forEach((a, i) => { if (t >= a) on = i; });
  return <Glass style={{left: 120, top: y, width: 840, height: 150, borderRadius: 75, display: 'flex', alignItems: 'center', justifyContent: 'space-around', padding: '0 20px', boxSizing: 'border-box', transform: `scale(${sp(t, t0, 12)})`}}>
    {L.map((l, i) => <div key={i} style={{width: 110, height: 110, borderRadius: 55, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Pop', fontWeight: 700, fontSize: 40,
      background: i === on ? 'rgba(0,0,0,0.55)' : 'transparent', color: i === on ? YEL : '#fff', boxShadow: i === on ? `0 0 30px ${YEL}88` : 'none', transform: `scale(${i === on ? 1.15 : 1})`}}>{l}</div>)}
  </Glass>;
};

// HD 60 -> HD 30
const FpsCard: React.FC<{t0: number; tSwitch: number}> = ({t0, tSwitch}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12); const s = lin(t, tSwitch, tSwitch + 0.4);
  const n = Math.round(60 - 30 * s);
  return <Glass style={{left: 290, top: 700, width: 500, height: 420, transform: `scale(${k})`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
    <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 120, color: '#fff', lineHeight: 1}}>HD</div>
    <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 150, color: s > 0.5 ? YEL : '#fff', lineHeight: 1.1, textShadow: s > 0.5 ? `0 0 40px ${YEL}88` : 'none'}}>{n}</div>
    <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 34, color: 'rgba(210,215,255,0.85)'}}>images par seconde</div>
  </Glass>;
};

export const Video: React.FC = () => {
  const t = useT();
  const scr = pick(t, [[0, 'dc_photo.png'], [8.8, 'dc_video.png'], [12.9, 'dc_menu.png'], [15.0, 'dc_dual.png'], [21.0, 'dc_rec.png']]);
  const cur = t < 9.7 ? 1 : t < 13.3 ? 2 : t < 19.18 ? 3 : t < 22.0 ? 4 : 5;
  const st = Math.min(cur, 4);
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE + HOOK */}
    <Scene t0={0} t1={6.5}>
      <Photo src="img_concert.png" t0={0} t1={6.8} dim={0.15} />
      <CoverTitle line="FILME AVEC TES" keyword="DEUX CAMÉRAS" />
      <Sent top={280} t0={2.0} t1={6.7} words={[[2.0, 'Filme ce que tu vois'], [2.46, 'et ta tête', ELEC]]} size={52} />
      <Sent top={365} t0={2.0} t1={6.7} words={[[2.82, 'en même temps', ELEC]]} size={58} />
      <Pill t0={3.8} x={540} y={1380} size={46} border={ELEC}>ton iPhone sait le faire</Pill>
      <Pill t0={5.1} x={540} y={1500} size={42} border={YEL}>les 2 caméras d’un coup</Pill>
    </Scene>

    {/* ÉTAPES */}
    <Scene t0={6.5} t1={22.0}>
      <StepTag n={st} t0={[6.55, 9.7, 13.3, 19.18][st - 1]} />
      <Checklist cur={cur} t0={6.7} />
      {/* étape 1 */}
      <Sent top={385} t0={7.1} t1={9.6} words={[[7.16, 'Ouvre'], [7.42, 'l’Appareil photo', ELEC]]} size={58} />
      <Sent top={465} t0={7.1} t1={9.6} words={[[8.14, 'et passe en'], [8.56, 'mode Vidéo', YEL]]} size={54} />
      {/* étape 2 */}
      <Sent top={385} t0={10.3} t1={13.2} words={[[10.38, 'Touche le bouton'], [11.32, 'aux six points', ELEC]]} size={54} />
      <Sent top={465} t0={10.3} t1={13.2} words={[[11.86, 'en bas à droite']]} size={54} />
      {/* étape 3 */}
      <Sent top={385} t0={14.1} t1={15.6} words={[[14.2, 'Choisis'], [14.42, '« Double capture »', ELEC]]} size={56} />
      <Sent top={385} t0={15.66} t1={19.1} words={[[15.66, 'Ta tête apparaît'], [16.3, 'dans une fenêtre', ELEC]]} size={52} />
      <Sent top={465} t0={15.66} t1={19.1} words={[[17.24, 'par-dessus'], [17.8, 'la caméra arrière']]} size={50} />
      {/* étape 4 */}
      <Sent top={385} t0={19.9} t1={22.1} words={[[19.94, 'Appuie sur'], [20.22, 'le bouton rouge', RED]]} size={58} />
      <ZoomPhone src={scr} t0={6.6} keys={[[6.6, 1, 300, 650], [8.2, 1.7, 300, 1150], [9.7, 1, 300, 650], [10.6, 1.8, 470, 1090], [12.9, 1, 300, 760], [14.2, 1.6, 200, 780],
          [15.1, 1, 300, 650], [16.2, 1.6, 420, 300], [18.8, 1, 300, 650], [19.9, 1.6, 300, 1000], [21.3, 1, 300, 650]]}>
        <HiBox sx={300} sy={1218} w={130} h={56} t0={8.5} t1={9.7} />
        <HiBox sx={513} sy={1074} w={86} h={86} t0={11.3} t1={12.9} />
        <HiBox sx={128} sy={800} w={180} h={200} t0={14.3} t1={15.0} />
        <HiBox sx={482} sy={242} w={212} h={280} t0={16.3} t1={18.8} />
        <HiBox sx={300} sy={1074} w={130} h={130} t0={20.3} t1={21.0} />
      </ZoomPhone>
      <Stamp t0={21.2} text="C’EST PARTI !" color={RED} x={600} y={1400} size={56} rot={-7} />
    </Scene>

    {/* RÉSULTAT */}
    <Scene t0={22.0} t1={25.3}>
      <Photo src="img_gateau.png" t0={22.0} t1={25.6} dim={0.15} />
      <Sent top={280} t0={22.06} t1={25.5} words={[[22.06, 'Et voilà :', GRN], [22.58, 'en une seule prise']]} size={50} />
      <Sent top={365} t0={22.06} t1={25.5} words={[[23.62, 'la scène'], [23.96, '+ ta réaction', ELEC]]} size={60} />
    </Scene>
    <Scene t0={25.3} t1={28.3}>
      <Sent top={290} t0={25.4} t1={28.5} words={[[25.4, 'Parfait pour…']]} size={70} />
      <ImgCard src="img_gateau.png" t0={26.1} x={70} y={520} w={300} h={470} label="anniversaire" rot={-5} />
      <ImgCard src="img_concert.png" t0={26.9} x={390} y={560} w={300} h={470} label="concert" rot={2} />
      <ImgCard src="img_cuisine.png" t0={27.6} x={710} y={520} w={300} h={470} label="recette" rot={6} />
    </Scene>

    {/* DÉPLACER LA FENÊTRE */}
    <Scene t0={28.3} t1={31.0}>
      <Sent top={270} t0={28.38} t1={31.2} words={[[28.38, 'Déplace la fenêtre']]} size={56} />
      <Sent top={350} t0={28.38} t1={31.2} words={[[29.72, 'avec ton doigt', ELEC], [30.26, 'en filmant', YEL]]} size={52} />
      <Phone src="dc_rec_nopip.png" x={540} top={520} w={470} t0={28.4}><DragPip /></Phone>
    </Scene>

    {/* PIÈGE */}
    <Scene t0={31.0} t1={39.0}>
      <Pill t0={31.05} x={540} y={300} size={44} border={RED}>le piège</Pill>
      <Sent top={390} t0={32.1} t1={34.4} words={[[32.1, 'Tout est collé']]} size={56} />
      <Sent top={470} t0={32.1} t1={34.4} words={[[32.88, 'dans une seule vidéo', RED]]} size={52} />
      <Sent top={390} t0={34.5} t1={37.4} words={[[34.5, 'Fenêtre mal placée ?']]} size={56} />
      <Sent top={470} t0={34.5} t1={37.4} words={[[36.06, 'impossible de la bouger', RED]]} size={50} />
      <Sent top={390} t0={37.5} t1={39.2} words={[[37.5, 'ni de séparer']]} size={56} />
      <Sent top={470} t0={37.5} t1={39.2} words={[[37.98, 'les deux images', RED]]} size={52} />
      <MiniFrame t0={31.3} merged={lin(t, 32.5, 33.3)} x={375} y={640} />
      {t > 31.3 && t < 34.4 && <Icon src="film_frames_3d.png" t0={31.4} size={180} x={260} y={1180} />}
      {t >= 33.1 && <Icon src="locked_3d.png" t0={33.1} size={200} x={810} y={1180} />}
      {t >= 36.4 && <Icon src="prohibited_3d.png" t0={36.4} size={180} x={250} y={1180} />}
    </Scene>

    {/* 30 IMAGES / SECONDE */}
    <Scene t0={39.0} t1={43.1}>
      <Sent top={300} t0={39.0} t1={43.3} words={[[39.0, 'La vidéo passe'], [39.68, 'à 30 images/s', YEL]]} size={56} />
      <Sent top={385} t0={39.0} t1={43.3} words={[[40.9, 'au lieu de 60']]} size={52} />
      <FpsCard t0={39.3} tSwitch={39.86} />
      <Stamp t0={42.3} text="C’EST NORMAL" color={GRN} x={540} y={1260} size={56} rot={-6} />
    </Scene>

    {/* BONUS ZOOM */}
    <Scene t0={43.1} t1={47.1}>
      <Sent top={300} t0={43.16} t1={47.3} words={[[43.16, 'Bonne nouvelle :', GRN]]} size={66} />
      <Sent top={390} t0={43.16} t1={47.3} words={[[43.82, 'tu peux'], [44.3, 'zoomer en filmant', ELEC]]} size={56} />
      <div style={{position: 'absolute', left: 240, top: 560, width: 600, height: 640, borderRadius: 44, overflow: 'hidden', border: '2px solid rgba(255,255,255,0.3)', boxShadow: '0 30px 80px rgba(0,0,0,0.6)', opacity: lin(t, 43.3, 43.7)}}>
        <Img src={staticFile('dc_rear.png')} style={{width: 600, height: 1300, marginTop: -330, transform: `scale(${interpolate(t, [45.0, 45.3, 45.6, 45.9, 46.2], [0.8, 1, 1.4, 1.9, 2.6], C)})`, transformOrigin: '50% 48%'}} />
      </div>
      <ZoomRow t0={44.3} y={1250} />
    </Scene>

    {/* QUITTER */}
    <Scene t0={47.1} t1={51.2}>
      <Sent top={300} t0={47.1} t1={51.4} words={[[47.1, 'Pour revenir'], [47.6, 'à la normale', GRN]]} size={58} />
      <Sent top={385} t0={47.1} t1={51.4} words={[[48.7, 'touche cette icône']]} size={50} />
      <Sent top={460} t0={47.1} t1={51.4} words={[[50.1, 'à côté de HD', ELEC]]} size={48} />
      <ZoomPhone src={t < 50.6 ? 'dc_dual.png' : 'dc_video.png'} t0={47.2} keys={[[47.2, 1, 300, 650], [48.6, 1.9, 320, 260], [50.8, 1, 300, 650]]}>
        <HiBox sx={333} sy={131} w={70} h={62} t0={49.0} t1={50.6} />
      </ZoomPhone>
    </Scene>

    {/* MODÈLES */}
    <Scene t0={51.2} t1={53.2}>
      <Sent top={300} t0={51.28} t1={53.4} words={[[51.28, 'Ça marche'], [51.58, 'à partir de']]} size={62} />
      <Icon src="mobile_phone_3d.png" t0={51.5} size={380} x={540} y={850} />
      <Pill t0={52.14} x={540} y={1200} size={60} border={ELEC}>l’iPhone 17</Pill>
    </Scene>

    {/* PARTAGE */}
    <Scene t0={53.2} t1={58.5}>
      <Glow x={540} y={950} r={300} color="#4a2cff" />
      <Sent top={290} t0={53.28} t1={58.7} words={[[53.28, 'Quelqu’un filme'], [54.46, 'ses enfants']]} size={50} />
      <Sent top={375} t0={53.28} t1={58.7} words={[[54.96, 'sans jamais'], [55.54, 'être dedans ?', ELEC]]} size={54} />
      <Icon src="mobile_phone_with_arrow_3d.png" t0={55.5} size={340} x={540} y={880} />
      <Pill t0={56.98} x={540} y={1250} size={50} border={ELEC}>Envoie-lui cette vidéo</Pill>
    </Scene>

    <EndScreen t0={58.5} t1={60.7} tEnd={63.1} tAbonne={61.06} tPour={61.5} tImmergee={62.14} />
    <Finish total={64.43} />
  </AbsoluteFill>;
};
