import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import data from './data.json';
import {useT, sp, lin, Word, Sent, Background, Glass, Icon, Scene, Phone, HiBox, ZoomPhone, Waves, StepTag, Checklist, Stamp, Pill, Photo, CallCard, Bubble, Sorter, Glow, pick, fontCss, ELEC, RED, GRN, YEL, ORG, TS, CoverTitle, EndScreen, Finish} from './lib';
const P: any = data;
// EXEMPLE : vidéo « Fini les appels de démarchage » (19/11/2026). Copier ce fichier et refaire la timeline.
const TB = P["tel:Blocage d'appels et identification"], TM = P["tel:Demander le motif de l'appel"], RA = P['reg:Apps'], AT = P['apps:Téléphone'], BT = P['bloc:tog'];

export const Video: React.FC = () => {
  const t = useT();
  const step2src = pick(t, [[0, 'reg.png'], [27.75, 'reg_hi.png'], [28.1, 'apps.png'], [28.55, 'apps_hi.png'], [28.95, 'tel.png'], [29.5, 'tel_hi_bloc.png'], [30.3, 'bloc_off.png'], [32.0, 'bloc_on.png']]);
  const step4src = pick(t, [[0, 'tel.png'], [40.4, 'tel_hi_motif.png'], [41.6, 'tel_motif.png']]);
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* ACCROCHE */}
    <Scene t0={0} t1={7.3}>
      <Photo src="img_table.png" t0={0} t1={7.3} dim={0.2} />
      <Waves cx={690} cy={1235} t0={0.2} color="#5b8cff" r0={90} />
      <CoverTitle line="FINI LES APPELS DE" keyword="DÉMARCHAGE" />
      <Sent top={300} t0={2.0} t1={4.1} words={[[2.0, 'Ton iPhone sonne'], [2.24, 'en plein'], [2.4, 'repas', YEL], [2.98, 'tu cours…']]} size={84} />
      <Sent top={300} t0={4.15} t1={7.3} words={[[4.15, "et c'est"], [4.4, 'encore'], [4.82, 'un démarcheur', RED]]} size={84} />
      <CallCard t0={4.5} y={640} title="Démarchage ?" sub="09 48 •• •• ••" color={RED} />
    </Scene>

    {/* CONSÉQUENCE */}
    <Scene t0={7.5} t1={11.95}>
      <Photo src="img_main.png" t0={7.5} t1={12} dim={0.3} />
      <Sent top={290} t0={7.5} t1={9.2} words={[[7.54, 'À force, tu ne'], [8.2, 'décroches'], [8.54, 'plus du tout', RED]]} size={78} />
      <Sent top={290} t0={9.22} t1={11.1} words={[[9.24, 'Et le jour où'], [9.74, "c'est le"], [9.94, 'livreur', ELEC], [10.36, 'ou le'], [10.6, 'médecin…', ELEC]]} size={78} />
      <Sent top={290} t0={11.12} t1={12.2} words={[[11.16, 'tu'], [11.24, 'rates', RED], [11.4, "l'appel."]]} size={96} />
      {t > 9.8 && t < 11.15 && <><Icon src="delivery_truck_3d.png" t0={9.94} size={230} x={330} y={900} /><Icon src="stethoscope_3d.png" t0={10.6} size={230} x={750} y={900} /></>}
      <Stamp t0={11.3} text="APPEL MANQUÉ" color={RED} x={540} y={900} />
    </Scene>

    {/* DÉCLIC */}
    <Scene t0={12.0} t1={15.75}>
      <Glow x={540} y={760} r={300} color="#3b2cff" />
      <Pill t0={12.1} x={540} y={300}><Img src={staticFile('key_3d.png')} style={{width: 60, height: 60}} />la solution</Pill>
      <Sent top={420} t0={12.1} t1={16} words={[[12.14, 'Rassure-toi :'], [12.82, '2 petits'], [13.38, 'réglages', ELEC]]} size={86} />
      <Sent top={640} t0={14.0} t1={16} words={[[14.04, 'ton iPhone fait le'], [14.76, 'tri', ELEC], [14.92, 'tout seul']]} size={64} />
      <Sorter t0={12.6} />
    </Scene>

    {/* ÉTAPE 1 */}
    <Scene t0={15.95} t1={21.45}>
      <StepTag n={1} t0={16.0} />
      <Checklist cur={1} t0={16.1} />
      <Sent top={390} t0={16.0} t1={18.95} words={[[16.1, 'Télécharge'], [16.5, 'Saracroche', YEL]]} size={68} />
      <Sent top={470} t0={16.0} t1={18.95} words={[[18.04, "sur l'App Store"]]} size={60} />
      <Sent top={390} t0={19.0} t1={21.5} words={[[19.04, 'Une appli'], [19.48, 'française,', ELEC]]} size={68} />
      <Sent top={470} t0={19.0} t1={21.5} words={[[20.1, 'gratuite', GRN], [20.46, 'et'], [20.78, 'sans pub', GRN]]} size={68} />
      <Phone src={t < 18.35 ? 'as_get.png' : 'as_open.png'} x={590} top={600} w={500} t0={16.1}>
        <HiBox sx={P['as:btn'][0]} sy={P['as:btn'][1]} w={180} h={66} t0={17.4} t1={18.6} />
      </Phone>
    </Scene>
    <Scene t0={21.5} t1={25.35}>
      <Photo src="img_bouclier.png" t0={21.5} t1={25.4} dim={0.15} />
      <Checklist cur={1} t0={21.5} />
      <Sent top={280} t0={21.5} t1={25.6} words={[[21.6, 'Elle bloque des'], [22.06, 'millions', YEL]]} size={64} />
      <Sent top={380} t0={21.5} t1={25.6} words={[[22.52, 'de numéros de démarchage']]} size={58} />
      <Sent top={460} t0={23.4} t1={25.6} words={[[23.5, 'avant même'], [23.98, 'que ça sonne', GRN]]} size={58} />
    </Scene>

    {/* ÉTAPE 2 */}
    <Scene t0={25.55} t1={33.5}>
      <StepTag n={2} t0={25.62} />
      <Checklist cur={t < 32.3 ? 2 : 3} t0={25.7} />
      <Sent top={390} t0={26.3} t1={28.5} words={[[26.42, 'Ouvre'], [26.76, 'Réglages', ELEC], [27.72, 'puis'], [27.8, 'Apps', ELEC]]} size={66} />
      <Sent top={390} t0={28.52} t1={29.4} words={[[28.56, 'puis'], [28.6, 'Téléphone', ELEC]]} size={66} />
      <Sent top={390} t0={29.42} t1={31.9} words={[[29.46, 'Touche'], [29.88, '« Blocage d’appels', ELEC]]} size={62} />
      <Sent top={470} t0={29.42} t1={31.9} words={[[30.3, 'et identification »', ELEC]]} size={62} />
      <Sent top={390} t0={31.92} t1={33.6} words={[[31.98, 'et active'], [32.46, 'Saracroche', GRN]]} size={68} />
      <ZoomPhone src={step2src} t0={25.7} keys={[[26.6, 1.6, 300, RA[1] - 120], [28.1, 1.5, 300, AT[1]], [28.95, 1.6, 300, TB[1] - 120], [30.3, 1.9, 380, BT[1] + 40]]}>
        <HiBox sx={300} sy={RA[1]} w={556} h={74} t0={27.1} t1={28.05} />
        <HiBox sx={300} sy={AT[1]} w={556} h={74} t0={28.3} t1={28.9} />
        <HiBox sx={300} sy={TB[1]} w={556} h={74} t0={29.3} t1={30.25} />
        <HiBox sx={BT[0]} sy={BT[1]} w={100} h={60} t0={31.0} t1={33.6} />
      </ZoomPhone>
    </Scene>

    {/* ÉTAPE 3 */}
    <Scene t0={33.8} t1={38.95}>
      <StepTag n={3} t0={33.86} />
      <Checklist cur={3} t0={33.9} />
      <Sent top={390} t0={34.5} t1={36.15} words={[[34.62, 'Sur la même page'], [35.38, 'Téléphone', ELEC]]} size={60} />
      <Sent top={390} t0={36.2} t1={39.2} words={[[36.24, "Descends jusqu'à"]]} size={60} />
      <Sent top={470} t0={36.2} t1={39.2} words={[[36.82, '« Filtrer les correspondants', ELEC], [37.56, 'inconnus »', ELEC]]} size={42} />
      <ZoomPhone src="tel.png" t0={33.9} keys={[[34.4, 1.5, 300, 1050], [35.6, 1.5, 300, 700], [36.6, 1.7, 300, 330]]}>
        <HiBox sx={300} sy={P['tel:hdr'][1]} w={540} h={44} t0={36.9} />
      </ZoomPhone>
    </Scene>

    {/* ÉTAPE 4 */}
    <Scene t0={39.1} t1={42.1}>
      <StepTag n={4} t0={39.22} />
      <Checklist cur={t < 41.6 ? 4 : 5} t0={39.3} />
      <Sent top={390} t0={39.9} t1={42.3} words={[[40.06, 'Choisis'], [40.46, '« Demander le', ELEC]]} size={56} />
      <Sent top={470} t0={39.9} t1={42.3} words={[[40.94, "motif de l'appel »", ELEC]]} size={56} />
      <ZoomPhone src={step4src} t0={39.3} keys={[[39.2, 1.7, 300, 330], [39.9, 1.7, 330, TM[1]]]}>
        <HiBox sx={300} sy={TM[1]} w={556} h={TM[2]} t0={40.1} />
      </ZoomPhone>
      <Stamp t0={41.7} text="C'EST FINI !" color={GRN} x={540} y={1420} size={62} />
    </Scene>

    {/* RÉSULTAT */}
    <Scene t0={42.15} t1={48.75}>
      <Glow x={540} y={900} r={320} color="#2a3cff" />
      <Sent top={280} t0={42.15} t1={44.4} words={[[42.18, 'Si un démarcheur'], [43.48, 'passe quand même…', RED]]} size={64} />
      <Sent top={280} t0={44.45} t1={48.9} words={[[44.48, 'ton iPhone lui demande'], [45.3, 'qui il est', ELEC]]} size={64} />
      <CallCard t0={42.9} y={480} title="Numéro inconnu" sub="Appel entrant" color={RED} icon="mobile_phone_3d.png" />
      <Bubble t0={45.1} y={740} right label="Ton iPhone" text="Bonjour, qui êtes-vous et pourquoi appelez-vous ?" />
      <Bubble t0={46.8} y={1010} label="L'appelant" text="« C'est pour votre pompe à chaleur… »" />
      <Pill t0={47.5} x={540} y={1360} size={46} border={RED}>Tu décides : <span style={{color: RED}}>tu ignores</span></Pill>
    </Scene>
    <Scene t0={48.8} t1={51.2}>
      <Glow x={540} y={900} r={320} color="#1f8a4a" />
      <Sent top={300} t0={48.8} t1={51.5} words={[[48.92, 'Tes'], [49.04, 'contacts,', GRN], [49.64, 'eux,']]} size={80} />
      <Sent top={400} t0={48.8} t1={51.5} words={[[50.18, 'sonnent normalement', GRN]]} size={66} />
      <Waves cx={540} cy={840} t0={49.6} color={GRN} r0={150} />
      <CallCard t0={49.5} y={745} title="Maman" sub="Appel entrant" color={GRN} />
    </Scene>

    {/* PARTAGE */}
    <Scene t0={51.35} t1={56.45}>
      <Glow x={540} y={950} r={300} color="#4a2cff" />
      <Sent top={290} t0={51.4} t1={56.6} words={[[51.44, 'Tu connais quelqu’un qui reçoit']]} size={56} />
      <Sent top={370} t0={51.4} t1={56.6} words={[[52.78, '3 appels', RED], [53.32, 'de démarchage'], [53.82, 'par jour ?']]} size={56} />
      {[0, 1, 2].map((i) => <Icon key={i} src="telephone_receiver_3d.png" t0={52.9 + i * 0.15} size={150} x={330 + i * 210} y={640} />)}
      <Icon src="mobile_phone_with_arrow_3d.png" t0={54.5} size={330} x={540} y={1000} />
      <Pill t0={54.6} x={540} y={1300} size={50}>Envoie-lui cette vidéo</Pill>
    </Scene>

    {/* ORANGE */}
    <Scene t0={56.7} t1={64.5}>
      <Pill t0={56.8} x={540} y={290} size={46}>Petite précision</Pill>
      <Sent top={390} t0={58.2} t1={64.8} words={[[58.32, "L'appli"], [59.3, 'Orange Téléphone', ORG]]} size={64} />
      {(() => { const k = sp(t, 59.3, 13); if (t < 59.3) return null; return <Glass style={{left: 160, top: 620, width: 760, height: 470, transform: `scale(${k})`, opacity: Math.min(1, k * 1.5)}}>
        <div style={{position: 'absolute', left: 50, top: 50, width: 120, height: 120, borderRadius: 30, background: 'linear-gradient(135deg,#ff9a2e,#ff6a00)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <div style={{width: 70, height: 70, borderRadius: 35, border: '7px solid #fff'}} /></div>
        <div style={{position: 'absolute', left: 200, top: 72, fontFamily: 'Pop', fontWeight: 700, fontSize: 46, color: '#fff'}}>Orange Téléphone</div>
        <div style={{position: 'absolute', left: 200, top: 132, fontFamily: 'Int', fontWeight: 600, fontSize: 30, color: 'rgba(220,225,255,0.75)'}}>écrit « Démarchage »… et ça sonne</div>
        <div style={{position: 'absolute', left: 50, right: 50, top: 250, height: 2, background: 'rgba(255,255,255,0.2)'}} />
        <div style={{position: 'absolute', left: 50, top: 300, fontFamily: 'Int', fontWeight: 700, fontSize: 40, color: '#fff'}}>Blocage automatique</div>
        <div style={{position: 'absolute', right: 50, top: 290, width: 120, height: 70, borderRadius: 35, background: 'rgba(120,120,128,0.5)'}}>
          <div style={{position: 'absolute', left: 6, top: 6, width: 58, height: 58, borderRadius: 29, background: '#fff'}} /></div>
      </Glass>; })()}
      <Sent top={1170} t0={60.4} t1={62.35} words={[[60.88, 'ne bloque plus'], [61.5, 'rien', RED], [61.72, 'toute seule']]} size={58} />
      <Sent top={1170} t0={62.4} t1={64.8} words={[[62.42, "sauf avec l'option"], [63.26, 'payante', ORG]]} size={58} />
      <Icon src="money_bag_3d.png" t0={63.3} size={200} x={860} y={640} />
      <Stamp t0={61.5} text="ÇA SONNE QUAND MÊME" color={RED} x={560} y={1060} size={44} />
    </Scene>

    {/* QUESTION */}
    <Scene t0={64.7} t1={69.0}>
      <Glow x={540} y={900} r={300} color="#3b2cff" />
      <Sent top={300} t0={64.8} t1={69.3} words={[[64.82, 'Et toi,'], [65.36, 'combien d’appels']]} size={62} />
      <Sent top={390} t0={64.8} t1={69.3} words={[[65.86, 'de démarchage'], [66.58, 'par'], [67.0, 'semaine ?', YEL]]} size={52} />
      <Icon src="speech_balloon_3d.png" t0={66.0} size={360} x={540} y={900} />
      <Pill t0={67.74} x={540} y={1240} size={50} border={YEL}>Dis-le en commentaire</Pill>
    </Scene>

    {/* FIN */}
    <EndScreen t0={69.2} t1={71.95} tEnd={74.6} tAbonne={72.02} tPour={72.56} tImmergee={73.56} />
    <Finish total={75.9} />
  </AbsoluteFill>;
};
