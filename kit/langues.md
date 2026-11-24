# Version française + version anglaise d'une même vidéo

La même vidéo peut sortir en FR et en EN sans tout refaire : seuls la voix, les textes à l'écran et les sous-titres changent.

## Étapes
1. Script FR validé par Nej → Claude écrit la version EN (adaptée, pas mot à mot ; mêmes étapes, mêmes noms de réglages en anglais, ex. « Réglages » → « Settings »).
2. Voix EN : Nej la fait gratuitement sur le site EditCaption (outil texte vers voix, voix anglaise) et l'envoie. Le connecteur coûte des crédits : à éviter.
3. Temps morts : `python3 scripts/tighten.py voix_en.mp3 public/voice.wav`
4. Sous-titres EN : `python3 scripts/sous_titres.py public/voice.wav en`
5. Textes à l'écran : dans la timeline, mettre les phrases dans un objet `TXT = {fr: {...}, en: {...}}` et choisir la langue avec une constante `LANG`. Les temps viennent de la transcription de chaque voix.
6. Écrans d'iPhone : redessiner en anglais (mêmes fonctions `scr_…`, libellés anglais).
7. Rendu séparé : `<nom>_fr.mp4` et `<nom>_en.mp4`.

Comptes EN : pas encore créés (Nej se concentre sur le FR pour l'instant).
