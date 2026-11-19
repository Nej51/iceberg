# Usage : python3 transcrire.py <audio_ou_video> [fr]
# Affiche chaque phrase avec l'heure de début de chaque mot (mot@secondes).
import sys, subprocess, numpy as np
from faster_whisper import WhisperModel
src=sys.argv[1]; lang=sys.argv[2] if len(sys.argv)>2 else None
raw=subprocess.run(['ffmpeg','-v','error','-i',src,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.float32)
m=WhisperModel('small',device='cpu',compute_type='int8')
segs,info=m.transcribe(a,language=lang,word_timestamps=True)
for s in segs:
    print(' '.join(f"{w.word.strip()}@{w.start:.2f}" for w in s.words), f"|fin {s.words[-1].end:.2f}")
