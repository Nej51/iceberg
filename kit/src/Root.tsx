import React from 'react'; import {Composition} from 'remotion';
import {Video} from './Video';
import {Video as Teaser, TEASER_TOTAL} from './teaser';
import {Test, TEST_TOTAL} from './test_outils';
import data from './data.json';
import {Video as Secours2, S2_TOTAL} from './au_secours2';
import {Video as Muet, MUET_TOTAL} from './au_secours_muet';
import {Video as Haptic, HT_TOTAL} from './haptic';
// durée = longueur de la voix (secondes) écrite dans data.json par le script d'écrans : "duree"
const D: any = data;
export const Root: React.FC = () => <>
  <Composition id="Video" component={Video} width={1080} height={1920} fps={30} durationInFrames={Math.ceil((D.duree || 75.9) * 30)} />
  <Composition id="Teaser" component={Teaser} width={1080} height={1920} fps={30} durationInFrames={Math.ceil(TEASER_TOTAL * 30)} />
  <Composition id="Test" component={Test} width={1080} height={1920} fps={30} durationInFrames={Math.ceil(TEST_TOTAL * 30)} />
  <Composition id="Muet" component={Muet} width={1080} height={1920} fps={30} durationInFrames={Math.ceil(MUET_TOTAL * 30)} />
  <Composition id="Secours2" component={Secours2} width={1080} height={1920} fps={30} durationInFrames={Math.ceil(S2_TOTAL * 30)} />
  <Composition id="Haptic" component={Haptic} width={1080} height={1920} fps={30} durationInFrames={Math.ceil(HT_TOTAL * 30)} />
</>;
