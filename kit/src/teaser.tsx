import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, Sequence, Audio, staticFile} from 'remotion';
import {useT, sp, Sent, Background, Icon, Scene, Pill, Photo, Glow, fontCss, ELEC, YEL, CoverTitle} from './lib';
// Teaser TikTok « Ton iPhone cache tout ça » v2 : 3 astuces en plein écran + voix de Yanis, 22/11/2026.

// [fichier, seconde dans la vidéo d'origine, début ici, fin ici, ligne 1, ligne 2, temps des mots]
const CLIPS: [string, number, number, number, string, string, number, number][] = [
  ['double_capture', 15.2, 3.66, 7.82, 'Filme avec tes', '2 caméras en même temps', 4.26, 5.04],
  ['isolement-voix', 30.5, 7.82, 11.98, 'Efface les bruits', 'quand tu appelles', 8.26, 9.4],
  ['acces_guide', 31.5, 11.98, 16.3, 'Bloque ton iPhone', 'sur une seule app', 13.5, 14.2],
];
const TOTAL = 25.45;
const COVS = ['double_capture', 'isolement-voix', 'acces_guide', 'demarchage', 'illisible', 'clavier-cache'];

const FullClip: React.FC<{i: number}> = ({i}) => {
  const [f, from, a, b, l1, l2, w1, w2] = CLIPS[i];
  return <Scene t0={a} t1={b}>
    <Sequence from={Math.round(a * 30)} durationInFrames={Math.round((b - a + 0.4) * 30)} layout="none">
      <OffthreadVideo src={staticFile(`clips/${f}.mp4`)} startFrom={Math.round(from * 30)} muted style={{position: 'absolute', width: 1080, height: 1920, left: 0, top: 0}} />
    </Sequence>
    {/* cache le texte de la vidéo d'origine en haut */}
    <AbsoluteFill style={{background: 'linear-gradient(180deg, #05060f 0%, #05060f 27%, rgba(5,6,15,0.0) 33%, transparent 80%, rgba(18,10,46,0.6) 100%)'}} />
    <Pill t0={a + 0.05} x={540} y={270} size={40} border={ELEC}>astuce {i + 1}</Pill>
    <Sent top={350} t0={a} t1={b + 0.3} words={[[w1, l1]]} size={66} />
    <Sent top={440} t0={a} t1={b + 0.3} words={[[w2, l2, ELEC]]} size={i === 0 ? 56 : 62} />
  </Scene>;
};

export const Video: React.FC = () => {
  const t = useT();
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE + HOOK */}
    <Scene t0={0} t1={3.66}>
      <Photo src="img_concert.png" t0={0} t1={4.0} dim={0.25} />
      <CoverTitle line="TON IPHONE CACHE" keyword="TOUT ÇA" size={92} />
      <Sent top={280} t0={1.9} t1={3.9} words={[[1.9, 'Des réglages']]} size={60} />
      <Sent top={365} t0={1.9} t1={3.9} words={[[2.24, 'que presque personne', ELEC]]} size={56} />
      <Sent top={445} t0={1.9} t1={3.9} words={[[2.9, 'ne connaît', ELEC]]} size={56} />
    </Scene>

    {CLIPS.map((_, i) => <FullClip key={i} i={i} />)}

    {/* MES TUTOS : grille du profil */}
    <Scene t0={16.3} t1={19.4}>
      <Sent top={280} t0={16.34} t1={19.6} words={[[16.34, 'Tout ça'], [16.9, 'dans mes tutos', ELEC]]} size={64} />
      <Sent top={370} t0={16.34} t1={19.6} words={[[17.5, 'va les voir'], [18.1, 'sur mon compte', YEL]]} size={52} />
      {COVS.map((c, i) => { const k = sp(t, 16.5 + i * 0.12, 12); const x = 150 + (i % 3) * 270, y = 520 + Math.floor(i / 3) * 450;
        return <Img key={c} src={staticFile(`cov_${c}.png`)} style={{position: 'absolute', left: x, top: y + (1 - k) * 100, width: 240, height: 427, borderRadius: 24, objectFit: 'cover',
          border: '2px solid rgba(255,255,255,0.3)', boxShadow: '0 20px 50px rgba(0,0,0,0.6)', transform: `scale(${0.8 + 0.2 * k})`, opacity: Math.min(1, k * 1.5)}} />; })}
    </Scene>

    {/* PARTAGE */}
    <Scene t0={19.4} t1={22.0}>
      <Glow x={540} y={950} r={300} color="#4a2cff" />
      <Sent top={300} t0={19.4} t1={22.2} words={[[19.4, 'Tu connais quelqu’un']]} size={62} />
      <Sent top={390} t0={19.4} t1={22.2} words={[[20.2, 'qui a un iPhone ?', ELEC]]} size={66} />
      <Icon src="mobile_phone_with_arrow_3d.png" t0={20.3} size={360} x={540} y={880} />
      <Pill t0={20.94} x={540} y={1250} size={54} border={ELEC}>Envoie-lui cette vidéo</Pill>
    </Scene>

    {/* FIN */}
    <Scene t0={22.0} t1={TOTAL + 1}>
      <Glow x={540} y={760} r={340} color="#7a2cff" />
      <Sent top={300} t0={22.0} t1={TOTAL + 2} words={[[22.1, 'Abonne-toi', YEL]]} size={96} />
      {(() => { const k = sp(t, 22.1, 9); return <Img src={staticFile('logo.png')} style={{position: 'absolute', left: 240, top: 440 + 8 * Math.sin(t * 2.2), width: 600, height: 600, transform: `scale(${k}) rotate(${(1 - k) * -20}deg)`, filter: 'drop-shadow(0 0 40px rgba(110,80,255,0.7))'}} />; })()}
      <Sent top={1080} t0={22.0} t1={TOTAL + 2} words={[[22.66, 'pour découvrir la partie']]} size={58} />
      <Sent top={1155} t0={22.0} t1={TOTAL + 2} words={[[23.36, 'immergée', ELEC], [23.9, 'de ton iPhone']]} size={58} />
      <Pill t0={23.1} x={540} y={1340} size={46} border="#4fd7ff">@iphoneiceberg</Pill>
    </Scene>

    <div style={{position: 'absolute', left: 0, top: 0, height: 8, width: `${(t / TOTAL) * 100}%`, background: ELEC, boxShadow: `0 0 20px ${ELEC}`}} />
    <Audio src={staticFile('voice_teaser.wav')} />
    <Audio src={staticFile('sfx_teaser.wav')} />
  </AbsoluteFill>;
};
export const TEASER_TOTAL = TOTAL;
