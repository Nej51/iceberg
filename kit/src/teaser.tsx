import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, Sequence, Audio, staticFile} from 'remotion';
import {useT, sp, lin, Sent, Background, Icon, Scene, Pill, Photo, Glow, fontCss, ELEC, YEL, CoverTitle} from './lib';
// Teaser TikTok « Ton iPhone cache tout ça » (15 s, sans voix, musique The Tech), 22/11/2026.

// [fichier, seconde de départ dans la vidéo d'origine, phrase, mot coloré]
const CLIPS: [string, number, string, string][] = [
  ['double_capture', 29.0, 'Filme avec tes', '2 caméras'],
  ['acces_guide', 34.0, 'Bloque ton iPhone', 'sur une seule app'],
  ['isolement-voix', 31.5, 'On n’entend plus', 'que ta voix'],
  ['clavier-cache', 28.6, 'Ton clavier grossit', 'en secret'],
  ['demarchage', 22.0, 'Bloque le', 'démarchage'],
  ['illisible', 21.6, 'Rends ton écran', 'lisible'],
];
const T0 = 1.6, D = 1.7, TSHARE = T0 + CLIPS.length * D, TEND = TSHARE + 2.3, TOTAL = TEND + 2.6;

const ClipCard: React.FC<{i: number}> = ({i}) => {
  const t = useT(); const a = T0 + i * D; const k = sp(t, a, 13);
  const [f, from, l1, l2] = CLIPS[i];
  return <Scene t0={a} t1={a + D - 0.15}>
    <Pill t0={a} x={540} y={270} size={40} border={ELEC}>{i + 1} / {CLIPS.length}</Pill>
    <Sent top={350} t0={a} t1={a + D + 0.2} words={[[a + 0.02, l1], [a + 0.2, l2, ELEC]]} size={i === 1 ? 54 : 62} />
    <div style={{position: 'absolute', left: 120, top: 520, width: 840, height: 900, borderRadius: 50, overflow: 'hidden', border: '2px solid rgba(255,255,255,0.3)',
      boxShadow: '0 40px 100px rgba(0,0,0,0.7), 0 0 60px rgba(47,91,255,0.35)', transform: `scale(${0.85 + 0.15 * k}) translateY(${(1 - k) * 80}px)`, opacity: Math.min(1, k * 1.6)}}>
      <Sequence from={Math.round(a * 30)} durationInFrames={Math.round((D + 0.3) * 30)} layout="none">
        <OffthreadVideo src={staticFile(`clips/${f}.mp4`)} startFrom={Math.round(from * 30)} muted
          style={{position: 'absolute', width: 1080, height: 1920, left: -120, top: -500}} />
      </Sequence>
    </div>
  </Scene>;
};

export const Video: React.FC = () => {
  const t = useT();
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE */}
    <Scene t0={0} t1={T0}>
      <Photo src="img_concert.png" t0={0} t1={T0 + 0.3} dim={0.25} />
      <CoverTitle line="TON IPHONE CACHE" keyword="TOUT ÇA" size={92} />
    </Scene>

    {CLIPS.map((_, i) => <ClipCard key={i} i={i} />)}

    {/* PARTAGE */}
    <Scene t0={TSHARE} t1={TEND}>
      <Glow x={540} y={950} r={300} color="#4a2cff" />
      <Sent top={300} t0={TSHARE} t1={TEND + 0.2} words={[[TSHARE + 0.05, 'Tu connais quelqu’un']]} size={62} />
      <Sent top={390} t0={TSHARE} t1={TEND + 0.2} words={[[TSHARE + 0.4, 'qui a un iPhone ?', ELEC]]} size={66} />
      <Icon src="mobile_phone_with_arrow_3d.png" t0={TSHARE + 0.5} size={360} x={540} y={880} />
      <Pill t0={TSHARE + 0.9} x={540} y={1250} size={54} border={ELEC}>Envoie-lui cette vidéo</Pill>
    </Scene>

    {/* FIN */}
    <Scene t0={TEND} t1={TOTAL + 1}>
      <Glow x={540} y={760} r={340} color="#7a2cff" />
      <Sent top={300} t0={TEND} t1={TOTAL + 2} words={[[TEND + 0.1, 'Abonne-toi', YEL]]} size={96} />
      {(() => { const k = sp(t, TEND + 0.05, 9); return <Img src={staticFile('logo.png')} style={{position: 'absolute', left: 240, top: 440 + 8 * Math.sin(t * 2.2), width: 600, height: 600, transform: `scale(${k}) rotate(${(1 - k) * -20}deg)`, filter: 'drop-shadow(0 0 40px rgba(110,80,255,0.7))'}} />; })()}
      <Sent top={1080} t0={TEND} t1={TOTAL + 2} words={[[TEND + 0.5, 'pour découvrir la partie']]} size={58} />
      <Sent top={1155} t0={TEND} t1={TOTAL + 2} words={[[TEND + 0.9, 'immergée', ELEC], [TEND + 1.1, 'de ton iPhone']]} size={58} />
      <Pill t0={TEND + 1.2} x={540} y={1340} size={46} border="#4fd7ff">@iphoneiceberg</Pill>
    </Scene>

    <div style={{position: 'absolute', left: 0, top: 0, height: 8, width: `${(t / TOTAL) * 100}%`, background: ELEC, boxShadow: `0 0 20px ${ELEC}`}} />
    <Audio src={staticFile('sfx_teaser.wav')} />
  </AbsoluteFill>;
};
export const TEASER_TOTAL = TOTAL;
