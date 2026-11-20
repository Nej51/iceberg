#!/bin/bash
# Mixe la signature musicale sous la voix (baisse quand Nej parle) et remplace le son d'une vidéo déjà rendue.
# Usage : scripts/mixer_musique.sh <musique.mp3> <video_sans_musique.mp4> <sortie.mp4> [niveau_dB, défaut -25]   (lancer depuis kit/, voice.wav et sfx.wav dans public/)
set -e
MUS="$1"; VID="$2"; OUT="$3"; LVL="${4:--25}"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VID")
M=$(ffmpeg -i "$MUS" -af volumedetect -f null - 2>&1 | grep mean_volume | sed 's/.*mean_volume: \(-*[0-9.]*\) dB/\1/')
G=$(python3 -c "print(round(($LVL)-($M),1))")   # musique ramenée à ~ -25 dB de moyenne (Nej : -32 trop bas, on l'entendait à peine)
ffmpeg -v error -y -stream_loop -1 -i "$MUS" -t "$DUR" -af "afade=t=in:d=0.6,afade=t=out:st=$(python3 -c "print($DUR-1.8)"):d=1.8" -ar 44100 -ac 2 /tmp/bed_mix.wav
ffmpeg -v error -y -i public/voice.wav -i public/sfx.wav -i /tmp/bed_mix.wav -filter_complex \
 "[2:a]volume=${G}dB[bed];[0:a]pan=stereo|c0=c0|c1=c0,asplit=2[v1][v2];[1:a]pan=stereo|c0=c0|c1=c0[ss];[bed][v2]sidechaincompress=threshold=0.05:ratio=2:attack=30:release=500[duck];[v1][ss][duck]amix=inputs=3:normalize=0[m];[m]alimiter=limit=0.95[out]" \
 -map "[out]" -ar 44100 /tmp/mix_final.wav
ffmpeg -v error -y -i "$VID" -i /tmp/mix_final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "ok $OUT (gain musique ${G} dB)"
