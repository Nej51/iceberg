import React from 'react'; import {Composition} from 'remotion';
import {Video} from './Video';
import data from './data.json';
// durée = longueur de la voix (secondes) écrite dans data.json par le script d'écrans : "duree"
const D: any = data;
export const Root: React.FC = () => <Composition id="Video" component={Video} width={1080} height={1920} fps={30} durationInFrames={Math.ceil((D.duree || 75.9) * 30)} />;
