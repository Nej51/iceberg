# Vérification des infos (avant d'enregistrer la voix)

Pourquoi : une seule erreur dans une vidéo fait perdre la confiance (ex. « pas d'iPhone 19 » alors qu'un iPhone 19 simple est annoncé).

## Méthode (Claude, à chaque script)
1. Lister chaque affirmation du script (une ligne = une affirmation).
2. Pour chacune : une recherche web, une source fiable (Apple, Bloomberg, MacRumors, 9to5Mac, Numerama, iGeneration…).
3. Statut : ✅ vrai / ⚠️ rumeur (dire « serait », « pourrait ») / ❌ faux → corriger le script.
4. Noms des menus : vérifier le libellé FRANÇAIS exact et la version d'iOS (demander une capture à Nej si doute).
5. Donner le tableau à Nej en même temps que le script, en très court.

## Modèle de tableau
| Affirmation | Source | Statut |
|-------------|--------|--------|
| Écran courbé sur les 4 côtés (iPhone 20 Pro) | Bloomberg (Gurman) | ⚠️ rumeur |
| Pas d'iPhone 19 en 2027 | Bloomberg : iPhone 19 simple prévu | ❌ → dire « pas d'iPhone 19 Pro » |
