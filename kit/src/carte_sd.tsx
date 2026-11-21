import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {useT, sp, lin, Sent, Background, Glass, Icon, Scene, ZoomPhone, StepTag, Checklist, HiBox, Stamp, Pill, Photo, Glow, pick, fontCss, ELEC, RED, GRN, YEL, ORG, CoverTitle, EndScreen, Finish} from './lib';
// Vidéo « Vider l'iPhone sur une carte SD » (TikTok Shop lecteur de carte), 21/11/2026.

// carte en verre : icône 3D + titre + sous-titre
const InfoCard: React.FC<{t0: number; x: number; y: number; w?: number; icon: string; title: string; sub?: string; color?: string; badge?: boolean; tBadge?: number}> = ({t0, x, y, w = 380, icon, title, sub, color = '#fff', tBadge}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12); const b = tBadge !== undefined ? sp(t, tBadge, 9) : 0;
  return <Glass style={{left: x, top: y, width: w, height: 420, transform: `scale(${k})`, opacity: Math.min(1, k * 1.5), display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 14,
    border: b > 0.1 ? `3px solid ${RED}` : undefined, boxShadow: b > 0.1 ? `0 0 40px ${RED}66` : undefined}}>
    <div style={{position: 'relative', width: 180, height: 180}}>
      <Img src={staticFile(icon)} style={{width: 180, height: 180, filter: 'drop-shadow(0 16px 20px rgba(0,0,0,0.5))'}} />
      {tBadge !== undefined && t >= tBadge && <Img src={staticFile('prohibited_3d.png')} style={{position: 'absolute', right: -30, bottom: -20, width: 110, height: 110, transform: `scale(${b}) rotate(${(1 - b) * -30}deg)`}} />}
    </div>
    <div style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 46, color: '#fff', whiteSpace: 'nowrap'}}>{title}</div>
    {sub && <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 32, color, whiteSpace: 'nowrap'}}>{sub}</div>}
  </Glass>;
};

export const Video: React.FC = () => {
  const t = useT();
  const scr = pick(t, [[0, 'sd_photos.png'], [24.62, 'sd_share.png'], [26.38, 'sd_pick.png'], [28.62, 'sd_card.png'], [29.5, 'sd_files.png']]);
  const cur = t < 21.36 ? 1 : t < 26.38 ? 2 : t < 29.4 ? 3 : t < 34.6 ? 4 : 5;
  const st = Math.min(cur, 4);
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE + HOOK */}
    <Scene t0={0} t1={6.4}>
      <Photo src="img_plein.png" t0={0} t1={6.7} dim={0.2} />
      <CoverTitle line="TON IPHONE EST" keyword="PLEIN ?" />
      <Sent top={290} t0={2.0} t1={6.6} words={[[2.05, 'Vide tes photos'], [2.9, 'sur une carte SD', ELEC]]} size={62} />
      <Sent top={385} t0={4.4} t1={6.6} words={[[4.5, 'sans ordi,'], [5.5, 'sans payer iCloud', GRN]]} size={54} />
      <Pill t0={3.8} x={540} y={1400} size={52} border={ELEC}>en une minute</Pill>
    </Scene>

    {/* PRODUIT */}
    <Scene t0={6.4} t1={17.9}>
      <Photo src="img_lecteur.png" t0={6.4} t1={18.2} dim={0.22} />
      <Sent top={290} t0={6.44} t1={10.3} words={[[6.44, 'La solution :'], [7.44, 'un petit lecteur', ELEC]]} size={60} />
      <Sent top={385} t0={6.44} t1={10.3} words={[[8.54, 'qui se branche'], [9.22, 'sur ton iPhone']]} size={54} />
      <Sent top={290} t0={10.36} t1={12.5} words={[[10.36, 'Celui que'], [10.76, 'je te conseille']]} size={60} />
      <Sent top={385} t0={10.36} t1={12.5} words={[[11.38, 'est dans le'], [11.6, 'panier orange', ORG]]} size={58} />
      <Sent top={290} t0={12.54} t1={18.1} words={[[12.54, 'Les deux prises']]} size={62} />
      <Pill t0={13.16} x={330} y={520} size={50} border={ELEC}>Lightning</Pill>
      <Pill t0={13.9} x={750} y={520} size={50} border={ELEC}>USB-C</Pill>
      <Pill t0={15.36} x={540} y={660} size={48} border={GRN}>iPhone 6 à 18</Pill>
      <Pill t0={17.2} x={540} y={790} size={48} border={GRN}>+ iPad</Pill>
    </Scene>

    {/* ÉTAPES */}
    <Scene t0={17.9} t1={35.6}>
      {t < 21.36 && <Photo src="img_lecteur.png" t0={17.9} t1={21.6} dim={0.35} />}
      <StepTag n={st} t0={[17.98, 21.36, 26.38, 29.4][st - 1]} />
      <Checklist cur={cur} t0={18.1} />
      {/* étape 1 */}
      <Sent top={400} t0={18.7} t1={21.3} words={[[18.7, 'Glisse ta carte'], [19.26, 'dans le lecteur', ELEC]]} size={52} />
      <Sent top={470} t0={18.7} t1={21.3} words={[[19.96, 'et branche-le'], [20.36, 'sur ton iPhone']]} size={50} />
      {t >= 19.0 && t < 21.36 && <Icon src="electric_plug_3d.png" t0={20.16} size={200} x={830} y={880} />}
      {/* étape 2 */}
      <Sent top={400} t0={22.0} t1={25.1} words={[[22.08, 'Dans Photos,'], [22.74, 'sélectionne', ELEC]]} size={54} />
      <Sent top={470} t0={22.0} t1={25.1} words={[[23.26, 'puis touche'], [24.2, 'Partager', ELEC]]} size={52} />
      <Sent top={400} t0={25.18} t1={26.38} words={[[25.18, 'puis']]} size={54} />
      <Sent top={470} t0={25.18} t1={26.38} words={[[25.26, '« Enregistrer dans Fichiers »', ELEC]]} size={50} />
      {/* étape 3 */}
      <Sent top={400} t0={27.06} t1={29.4} words={[[27.06, 'Choisis'], [27.42, 'ta carte', ELEC]]} size={58} />
      <Sent top={470} t0={27.06} t1={29.4} words={[[28.44, 'puis touche'], [28.74, '« Enregistrer »', ELEC]]} size={52} />
      {/* étape 4 */}
      <Sent top={400} t0={30.54} t1={32.5} words={[[30.54, 'Vérifie dans'], [31.06, 'Fichiers', ELEC]]} size={58} />
      <Sent top={470} t0={30.54} t1={32.5} words={[[31.84, 'onglet'], [32.1, 'Parcourir', ELEC]]} size={52} />
      <Sent top={400} t0={32.58} t1={35.6} words={[[32.58, 'Tes photos'], [33.34, 'sont sur la carte', GRN]]} size={54} />
      <Sent top={470} t0={32.58} t1={35.6} words={[[34.3, 'supprime-les'], [34.9, 'de l’iPhone', RED]]} size={50} />
      {t >= 21.36 && <ZoomPhone src={scr} t0={21.4} keys={[[21.4, 1, 300, 650], [22.8, 1.25, 300, 520], [23.9, 1.9, 120, 1150], [24.62, 1, 300, 650], [25.1, 1.7, 470, 900],
          [26.38, 1, 300, 650], [27.3, 1.6, 300, 760], [28.62, 1.8, 440, 230], [29.5, 1, 300, 650], [31.9, 1.6, 400, 1120], [32.6, 1.35, 300, 600], [34.6, 1, 300, 650]]}>
        <HiBox sx={84} sy={1208} w={90} h={80} t0={24.0} t1={24.6} />
        <HiBox sx={505} sy={950} w={150} h={170} t0={25.3} t1={26.38} />
        <HiBox sx={300} sy={810} w={556} h={74} t0={27.54} t1={28.6} />
        <HiBox sx={495} sy={162} w={176} h={70} t0={28.74} t1={29.45} />
        <HiBox sx={490} sy={1205} w={150} h={76} t0={32.1} t1={32.58} />
        <HiBox sx={300} sy={600} w={570} h={520} t0={32.9} t1={34.6} />
      </ZoomPhone>}
      <Stamp t0={33.8} text="SUR LA CARTE !" color={GRN} x={700} y={1420} size={56} rot={-7} />
    </Scene>

    {/* RÉSULTAT + ANNONCE DES PIÈGES */}
    <Scene t0={35.6} t1={38.9}>
      <Glow x={540} y={900} r={320} color={t < 37.4 ? '#2c8a4a' : '#8a2c2c'} />
      {t < 37.4 ? <>
        <Sent top={290} t0={35.7} t1={37.4} words={[[35.72, 'Et voilà :', GRN], [36.28, 'des gigas']]} size={66} />
        <Sent top={385} t0={35.7} t1={37.4} words={[[36.64, 'libérés d’un coup', ELEC]]} size={60} />
        <Icon src="sparkles_3d.png" t0={36.0} size={360} x={540} y={900} />
        <Stamp t0={36.4} text="PLACE LIBÉRÉE !" color={GRN} x={540} y={1250} size={60} rot={-6} />
      </> : <>
        <Sent top={290} t0={37.46} t1={39.1} words={[[37.46, 'Attention :'], [38.16, '2 pièges', RED]]} size={74} />
        <Icon src="warning_3d.png" t0={37.6} size={380} x={540} y={900} />
      </>}
    </Scene>

    {/* PIÈGE 1 */}
    <Scene t0={38.9} t1={43.9}>
      <Pill t0={39.0} x={540} y={300} size={44} border={RED}>piège n°1</Pill>
      <Sent top={390} t0={39.06} t1={41.7} words={[[39.06, 'Les photos supprimées'], [39.86, 'restent 30 jours', RED]]} size={50} />
      <Sent top={390} t0={41.8} t1={44.1} words={[[41.8, 'Vide', GRN], [41.94, 'cet album,'], [42.64, 'sinon']]} size={58} />
      <Sent top={470} t0={41.8} t1={44.1} words={[[42.78, 'tu ne gagnes'], [43.2, 'aucune place', RED]]} size={52} />
      <InfoCard t0={39.4} x={110} y={640} icon="wastebasket_3d.png" title="Supprimés" sub="récemment" color="#cfd6ff" />
      <InfoCard t0={40.12} x={590} y={640} icon="hourglass_not_done_3d.png" title="30 jours" sub="encore là" color={RED} />
      <Stamp t0={41.8} text="VIDE-LE !" color={GRN} x={540} y={1180} size={60} rot={-6} />
    </Scene>

    {/* PIÈGE 2 */}
    <Scene t0={43.9} t1={49.0}>
      <Pill t0={44.0} x={540} y={300} size={44} border={RED}>piège n°2</Pill>
      <Sent top={390} t0={44.0} t1={45.45} words={[[44.0, 'Tu utilises'], [44.56, 'Photos iCloud ?', ELEC]]} size={56} />
      <Sent top={390} t0={45.5} t1={47.6} words={[[45.5, 'supprimé de l’iPhone']]} size={54} />
      <Sent top={470} t0={45.5} t1={47.6} words={[[46.56, '= supprimé d’iCloud', RED]]} size={54} />
      <Sent top={390} t0={47.66} t1={49.2} words={[[47.66, 'Garde bien'], [48.26, 'ta carte', GRN]]} size={62} />
      <InfoCard t0={44.6} x={110} y={640} icon="mobile_phone_3d.png" title="iPhone" tBadge={45.9} />
      <InfoCard t0={44.8} x={590} y={640} icon="cloud_3d.png" title="iCloud" tBadge={46.7} />
      <Pill t0={47.9} x={540} y={1200} size={50} border={GRN}><Img src={staticFile('card_file_box_3d.png')} style={{width: 64, height: 64}} />ta sauvegarde</Pill>
    </Scene>

    {/* PARTAGE */}
    <Scene t0={49.0} t1={52.5}>
      <Glow x={540} y={950} r={300} color="#4a2cff" />
      <Sent top={290} t0={49.1} t1={52.7} words={[[49.1, 'Quelqu’un a toujours'], [50.36, 'le message']]} size={46} />
      <Sent top={380} t0={49.1} t1={52.7} words={[[50.6, '« stockage plein » ?', RED]]} size={62} />
      <Icon src="mobile_phone_with_arrow_3d.png" t0={50.8} size={340} x={540} y={900} />
      <Pill t0={51.58} x={540} y={1250} size={50} border={ELEC}>Envoie-lui cette vidéo</Pill>
    </Scene>

    <EndScreen t0={52.5} t1={54.9} tEnd={57.2} tAbonne={55.1} tPour={55.46} tImmergee={56.34} />
    <Finish total={58.4} />
  </AbsoluteFill>;
};
