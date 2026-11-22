import React from 'react'; import {Composition} from 'remotion';
import {Video} from './Video';
import {Video as Teaser, TEASER_TOTAL} from './teaser';
import data from './data.json';
// durée = longueur de la voix (secondes) écrite dans data.json par le script d'écrans : "duree"
const D: any = data;
export const Root: React.FC = () => <>
  <Composition id="Video" component={Video} width={1080} height={1920} fps={30} durationInFrames={Math.ceil((D.duree || 75.9) * 30)} />
  <Composition id="Teaser" component={Teaser} width={1080} height={1920} fps={30} durationInFrames={Math.ceil(TEASER_TOTAL * 30)} />
</>;
