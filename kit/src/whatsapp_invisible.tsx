import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {useT, sp, lin, Sent, Background, Glass, Icon, Scene, Phone, ZoomPhone, StepTag, HiBox, Stamp, Pill, Photo, pick, fontCss, ELEC, RED, GRN, YEL, CoverTitle, EndScreen, Finish} from './lib';
import data from './data.json';
// Vidéo « Conversation WhatsApp invisible » (code secret), 23/11/2026. 1re vidéo sans « Je sais pas si tu le sais ».
const D: any = data;
const WG = '#25D366';

const List3: React.FC<{cur: number; t0: number}> = ({cur, t0}) => {
  const t = useT();
  return <div style={{position: 'absolute', left: 52, top: 640, display: 'flex', flexDirection: 'column', gap: 34}}>
    {[1, 2, 3].map((n, i) => { const k = sp(t, t0 + i * 0.08, 12); const done = n < cur, on = n === cur; const p = 0.5 + 0.5 * Math.sin(t * 6);
      return <div key={n} style={{width: 78, height: 78, borderRadius: 26, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${k})`,
        background: done ? GRN : on ? ELEC : 'rgba(255,255,255,0.08)', border: on || done ? 'none' : '2px solid rgba(255,255,255,0.25)',
        boxShadow: on ? `0 0 ${20 + 20 * p}px ${ELEC}` : done ? `0 0 20px ${GRN}` : 'none', fontFamily: 'Pop', fontWeight: 700, fontSize: 42, color: '#fff'}}>
        {done ? <svg width="40" height="40" viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6.5" stroke="#fff" strokeWidth="3.4" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg> : n}</div>; })}
  </div>;
};
// carte code : 1234 barré, puis un mot
const CodeCard: React.FC<{t0: number; y: number; text: string; bad?: number; good?: number}> = ({t0, y, text, bad, good}) => {
  const t = useT(); if (t < t0) return null; const k = sp(t, t0, 12); const isBad = bad !== undefined && t >= bad; const isGood = good !== undefined && t >= good;
  const sh = isBad ? Math.sin(t * 40) * 8 * (1 - lin(t, bad!, bad! + 0.5)) : 0; const c = isBad ? RED : isGood ? GRN : 'rgba(255,255,255,0.3)';
  return <Glass style={{left: 190, top: y, width: 700, height: 190, transform: `scale(${k}) translateX(${sh}px)`, display: 'flex', alignItems: 'center', justifyContent: 'center', border: `3px solid ${c}`, boxShadow: isBad || isGood ? `0 0 40px ${c}88` : undefined}}>
    <span style={{fontFamily: 'Pop', fontWeight: 700, fontSize: 110, color: '#fff', letterSpacing: 12, position: 'relative'}}>{text}
      {isBad && <div style={{position: 'absolute', left: -20, right: -20, top: '50%', height: 12, borderRadius: 6, background: RED, transform: `rotate(-8deg) scaleX(${sp(t, bad!, 12)})`, boxShadow: `0 0 20px ${RED}`}} />}</span>
  </Glass>;
};
// notification iOS en verre
const Notif: React.FC<{t0: number; y: number; title: string; body: string; blur?: number; t1?: number}> = ({t0, y, title, body, blur, t1 = 999}) => {
  const t = useT(); if (t < t0 || t > t1) return null; const k = sp(t, t0, 11); const b = blur !== undefined ? lin(t, blur, blur + 0.5) : 0;
  return <Glass style={{left: 110, top: y, width: 860, height: 170, borderRadius: 44, transform: `translateY(${(1 - k) * -260}px)`, opacity: Math.min(1, k * 1.5), display: 'flex', alignItems: 'center', gap: 28, padding: '0 34px', boxSizing: 'border-box'}}>
    <div style={{width: 96, height: 96, borderRadius: 24, background: WG, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
      <svg width="58" height="58" viewBox="0 0 24 24"><path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3z" fill="#fff" /></svg></div>
    <div style={{filter: `blur(${b * 14}px)`, opacity: 1 - b * 0.6}}><div style={{fontFamily: 'Int', fontWeight: 700, fontSize: 40, color: '#fff'}}>{title}</div>
      <div style={{fontFamily: 'Int', fontWeight: 600, fontSize: 34, color: 'rgba(230,235,255,0.85)', whiteSpace: 'nowrap'}}>{body}</div></div>
  </Glass>;
};

export const Video: React.FC = () => {
  const t = useT();
  const s1 = pick(t, [[0, 'w_list0.png'], [11.0, 'w_menu.png'], [13.6, 'w_list.png'], [17.0, 'w_locked.png'], [19.9, 'w_params.png'], [21.3, 'w_params_on.png'], [22.0, 'w_sheet.png'], [22.9, 'w_code.png']]);
  const s2 = pick(t, [[0, 'w_hidden.png'], [27.2, 'w_search0.png'], [28.0, 'w_search.png']]);
  const cur = t < 13.86 ? 1 : t < 19.86 ? 2 : t < 23.4 ? 3 : 4;
  return <AbsoluteFill style={{background: '#05060f'}}>
    <style>{fontCss}</style>
    <Background />

    {/* COUVERTURE + ACCROCHE */}
    <Scene t0={0} t1={8.6}>
      <Photo src="img_cadenas.png" t0={0} t1={8.9} dim={0.25} />
      <Sent top={290} t0={2.0} t1={8.8} words={[[2.0, 'Une conversation'], [2.06, 'invisible', ELEC]]} size={62} />
      <Sent top={375} t0={3.1} t1={8.8} words={[[3.32, 'qui n’apparaît'], [3.72, 'nulle part', YEL]]} size={58} />
      <Pill t0={4.9} x={540} y={1300} size={44} border={WG}>sauf avec ton code secret</Pill>
      <Pill t0={6.6} x={540} y={1420} size={40} border={ELEC}>3 étapes</Pill>
      <CoverTitle line="RENDS TA CONVERSATION WHATSAPP" keyword="INVISIBLE" size={88} />
      {t < 2.0 && <Img src={staticFile('logo_wa.png')} style={{position: 'absolute', left: 540 - 130, top: 470 + 6 * Math.sin(t * 3), width: 260, height: 260, objectFit: 'contain', opacity: 1 - lin(t, 1.6, 2.0), filter: `drop-shadow(0 0 40px rgba(37,211,102,0.8)) blur(${lin(t, 1.6, 2.0) * 20}px)`}} />}
    </Scene>

    {/* ÉTAPES */}
    <Scene t0={8.6} t1={23.8}>
      <List3 cur={cur} t0={8.7} />
      <StepTag n={cur > 3 ? 3 : cur} t0={8.76} />
      <Sent top={385} t0={9.64} t1={12.3} words={[[9.64, 'Appui long', ELEC]]} size={60} />
      <Sent top={465} t0={9.64} t1={12.3} words={[[10.9, 'sur la conversation']]} size={56} />
      <Sent top={385} t0={12.38} t1={13.8} words={[[12.38, 'puis'], [12.92, '« Verrouiller »', ELEC]]} size={60} />
      <Sent top={385} t0={14.6} t1={18.2} words={[[14.6, 'Tout en haut, ouvre']]} size={60} />
      <Sent top={465} t0={17.06} t1={18.2} words={[[17.06, '« Discussions verrouillées »', ELEC]]} size={52} />
      <Sent top={385} t0={18.28} t1={19.86} words={[[18.28, 'puis'], [18.76, '« Paramètres »', ELEC]]} size={60} />
      <Sent top={385} t0={20.72} t1={23.9} words={[[20.72, 'Active'], [21.26, '« Masquer »', ELEC]]} size={60} />
      <Sent top={465} t0={22.58} t1={23.9} words={[[22.58, 'et crée'], [22.9, 'ton code secret', GRN]]} size={56} />
      <ZoomPhone src={s1} t0={8.8} keys={[[8.85, 1, 300, 650], [9.6, 1.45, 300, 656], [11.0, 1.35, 230, 760], [13.86, 1.45, 280, 420], [17.0, 1.45, 420, 160], [19.9, 1.5, 320, 260], [22.0, 1, 300, 650], [22.9, 1.45, 300, 380]]}>
        <HiBox sx={D.row_Sarah[0]} sy={D.row_Sarah[1]} w={580} h={92} t0={9.64} t1={11.0} />
        <HiBox sx={D.m_lock[0]} sy={D.m_lock[1]} w={390} h={64} t0={12.38} t1={13.6} />
        <HiBox sx={D.folder[0]} sy={D.folder[1]} w={540} h={58} t0={15.1} t1={17.0} />
        <HiBox sx={D.params_btn[0]} sy={D.params_btn[1]} w={150} h={60} t0={18.44} t1={19.9} />
        <HiBox sx={D.toggle[0]} sy={D.toggle[1]} w={90} h={56} t0={20.72} t1={21.4} />
        <HiBox sx={D.create[0]} sy={D.create[1]} w={560} h={72} t0={22.05} t1={22.9} />
        <HiBox sx={D.code_field[0]} sy={D.code_field[1]} w={570} h={76} t0={22.95} t1={23.8} />
      </ZoomPhone>
    </Scene>

    {/* ET VOILÀ : DOSSIER DISPARU */}
    <Scene t0={23.8} t1={26.2}>
      <Sent top={290} t0={23.98} t1={26.4} words={[[24.62, 'Le dossier a'], [25.02, 'disparu', YEL]]} size={72} />
      <Phone src="w_hidden.png" x={540} top={470} w={420} t0={23.85} />
      <Stamp t0={24.0} text="ET VOILÀ !" color={GRN} x={540} y={1380} size={64} rot={-6} />
    </Scene>

    {/* RETROUVER AVEC LE CODE */}
    <Scene t0={26.2} t1={29.2}>
      <Sent top={290} t0={26.28} t1={29.4} words={[[26.56, 'Pour le retrouver,']]} size={58} />
      <Sent top={370} t0={26.28} t1={29.4} words={[[27.22, 'tape ton code', ELEC]]} size={58} />
      <Sent top={450} t0={28.02} t1={29.4} words={[[28.02, 'dans la recherche', GRN]]} size={54} />
      <ZoomPhone src={s2} t0={26.25} keys={[[26.3, 1, 300, 650], [26.9, 1.6, 300, 300]]}>
        <HiBox sx={D.search[0]} sy={D.search[1]} w={570} h={56} t0={27.0} t1={28.4} />
        <HiBox sx={D.found[0]} sy={D.found[1]} w={576} h={84} t0={28.5} t1={29.2} />
      </ZoomPhone>
    </Scene>

    {/* CONSEIL : UN MOT PLUTÔT QUE 1234 */}
    <Scene t0={29.2} t1={37.0}>
      <Sent top={280} t0={29.2} t1={37.2} words={[[29.2, 'Un conseil', YEL]]} size={74} />
      <Sent top={380} t0={30.36} t1={37.2} words={[[30.36, 'choisis'], [30.8, 'un mot', GRN], [31.18, 'pas 1234', RED]]} size={56} />
      <CodeCard t0={30.9} y={560} text="1234" bad={31.38} />
      <CodeCard t0={33.1} y={830} text="soleil" good={35.44} />
      <Icon src="sun_3d.png" t0={34.8} size={170} x={880} y={820} />
      <Pill t0={33.9} x={540} y={1120} size={42}>lettres, chiffres, emojis…</Pill>
      <Sent top={1220} t0={35.44} t1={37.2} words={[[35.44, 'Personne n’aura l’idée', GRN]]} size={52} />
    </Scene>

    {/* PIÈGE */}
    <Scene t0={37.0} t1={44.9}>
      <Photo src="img_coffre.png" t0={37.0} t1={45.2} dim={0.4} />
      <Sent top={280} t0={37.14} t1={45.1} words={[[37.14, 'Attention,'], [38.22, 'un piège', RED]]} size={72} />
      <Sent top={375} t0={38.88} t1={45.1} words={[[38.88, 'Code oublié ='], [41.48, 'messages effacés', RED]]} size={54} />
      <Stamp t0={41.5} text="TOUT EST EFFACÉ" color={RED} x={540} y={1250} size={58} rot={-6} />
      <Pill t0={43.14} x={540} y={1420} size={44} border={YEL}>Note-le dans un endroit sûr</Pill>
    </Scene>

    {/* BONNE NOUVELLE : NOTIFICATIONS */}
    <Scene t0={44.9} t1={51.4}>
      <Sent top={280} t0={45.08} t1={51.6} words={[[45.08, 'Bonne nouvelle', GRN]]} size={72} />
      <Sent top={375} t0={45.76} t1={51.6} words={[[45.84, 'personne'], [46.68, 'n’est prévenu', YEL]]} size={56} />
      <Notif t0={45.9} y={600} title="Sarah" body="Tu as vu la surprise ?" blur={47.3} t1={47.9} />
      <Notif t0={47.9} y={600} title="WhatsApp" body="1 nouveau message" />
      <Sent top={860} t0={50.12} t1={51.6} words={[[50.12, 'sans le nom'], [50.58, 'ni le texte', ELEC]]} size={56} />
      <Stamp t0={50.86} text="DISCRET" color={ELEC} x={540} y={1180} size={60} rot={-6} />
    </Scene>

    {/* PARTAGE + QUESTION */}
    <Scene t0={51.4} t1={56.9}>
      <Photo src="img_bulle.png" t0={51.4} t1={57.2} dim={0.3} />
      <Sent top={290} t0={51.56} t1={54.7} words={[[51.84, 'Quelqu’un tient'], [52.64, 'à sa vie privée ?', ELEC]]} size={56} />
      <Pill t0={53.54} x={540} y={1400} size={46} border={ELEC}>Envoie-lui cette vidéo</Pill>
      <Sent top={290} t0={54.82} t1={57.1} words={[[54.82, 'Tu cacherais'], [55.72, 'quelle conversation ?', YEL]]} size={56} />
    </Scene>

    <EndScreen t0={56.9} t1={59.4} tEnd={62.0} tAbonne={59.88} tPour={60.28} tImmergee={61.14} />
    <Finish total={63.17} />
  </AbsoluteFill>;
};
