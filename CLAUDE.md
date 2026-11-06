# Projet : Ads « 3ème pilier A : de l'assurance à la banque »

Contexte partagé par toutes les conversations Claude du projet (création ads, media buying Adspirer, etc.).
Chaque conversation lit ce fichier en premier et respecte toutes ses règles.

---

## 1. Le client, l'offre et l'objectif business

- **Annonceur :** **Tellancia Sàrl** (nom légal, à utiliser comme bénéficiaire/payeur DSA pour la France), cabinet de courtage en assurance et libre passage, basé à Genève. Site : https://monpilier3.ch ; Page Facebook « Mon Pilier 3.ch ». Statut : [intermédiaire d'assurance inscrit au registre FINMA n° X / conseiller inscrit au registre LSFin n° X].
- **Modèle économique :** le cabinet perçoit des **commissions de gestion récurrentes** sur les capitaux de 3ème pilier A placés en banque. La valeur d'un client est donc proportionnelle au **capital transféré**.
- **Cible (angle actuel, exclusif) :** personnes qui ont un **3ème pilier A souscrit en assurance**, résidant en **Suisse romande** ou **frontaliers** (France voisine) travaillant en Suisse. On n'élargit pas à d'autres angles pour l'instant.
- **Offre :** **analyse gratuite par un expert** du contrat d'assurance existant. On ne pousse pas le transfert : on pose la question et on propose de faire le point.
- **Arguments :**
  - **frais plus bas** en banque ;
  - **versements flexibles** (pas de prime fixe obligatoire) ;
  - **attention**, toutes les situations sont différentes (valeur de rachat, couverture risque incluse, ancienneté du contrat), d'où l'intérêt d'une analyse par un expert.

## 2. KPI et qualification des leads

**Entonnoir suivi :** Lead → Lead qualifié → RDV tenu → Transfert signé → Capital transféré.

- **KPI principal :** coût d'acquisition par **CHF de capital transféré** (ou coût par transfert signé tant que le volume est faible).
- **KPI intermédiaires :** coût par lead qualifié ≤ **100 CHF au démarrage, objectif ~50 CHF ensuite** (décision de Kevin du 02.11.2026) ; coût par RDV tenu ≤ [X CHF] ; taux de joignabilité ≥ [X %].
- **On n'optimise jamais sur le coût par lead brut.**
- **Budget :** **3 050 CHF/mois maximum** sur Meta (50 CHF/jour Suisse romande + 50 CHF/jour frontaliers, décision de Kevin du 02.11.2026). Ne jamais le dépasser.

**Lead qualifié =** a un 3ème pilier A **en assurance** + joignable + accepte un RDV, avec en priorité :
- contrat souscrit depuis **plus de [5] ans** (les contrats récents ont souvent une valeur de rachat faible : transfert rarement dans l'intérêt du client, donc peu de conversions) ;
- valeur actuelle estimée ou prime annuelle élevée ([seuils à définir]).

**Formulaire retenu (décision de Kevin, 02.11.2026) :** priorité au **volume et à une friction minimale**. On utilise le formulaire Meta existant « Lead gen 3P banque 2 » (ID `1790789782189392`, confirmé) : où se trouve votre 3e pilier A / travaillez-vous en Suisse / qu'aimeriez-vous améliorer + nom, téléphone, e-mail. La qualification (ancienneté, prime, valeur de rachat) se fait **au téléphone**. Les questions ci-dessous restent la cible si la qualité des leads est insuffisante.

**Questions du formulaire « idéal » (si on doit filtrer davantage) :**
1. Votre 3ème pilier A est-il en assurance ? (Oui / Non / Je ne sais pas) → « Non » = disqualifié
2. Depuis quand ? (moins de 3 ans / 3 à 10 ans / plus de 10 ans)
3. Prime annuelle approximative (moins de 2 000 CHF / 2 000 à 5 000 / plus de 5 000)
4. Vous êtes : résident en Suisse (canton) / frontalier
5. Meilleur moment pour vous rappeler
+ prénom, téléphone, email, lien vers la politique de confidentialité [URL].

**Remontée des conversions :** chaque statut (lead qualifié, RDV tenu, transfert signé + capital) est renvoyé à Meta (API Conversions / conversions hors ligne) et à Google, pour que les algorithmes optimisent sur la qualité. Leads stockés dans [CRM / Google Sheet]. Rappel sous [X h].

## 3. Conformité (obligatoire pour toute annonce, page, formulaire ou texte)

1. Toujours écrire **« 3ème pilier A »**, à l'écran comme dans les textes. **Jamais « 3A ».**
2. **Aucun nom ni logo** de banque ou d'assureur. Pas de dénigrement des assureurs.
3. **Aucune promesse de rendement chiffré**, de gain garanti ou de « sans risque ».
4. **Pas de logo du cabinet** dans les vidéos : tout reste neutre.
5. **Ne jamais se présenter comme « neutre », « indépendant » ou « sans intérêt »** : le cabinet est rémunéré par des commissions sur les capitaux placés. « Analyse gratuite » est correct.
6. **Ne jamais inciter à résilier** un contrat d'assurance. Toujours renvoyer à l'analyse : une résiliation peut entraîner une perte (valeur de rachat) ou la fin d'une couverture décès / invalidité.
7. **Transparence sur la rémunération :** avant tout conseil, le client est informé par écrit des commissions perçues (obligation légale, art. 26 LSFin). Ce n'est pas à mettre dans la pub, mais c'est à intégrer dans le parcours de RDV.
8. **Frontaliers :** le traitement fiscal du 3ème pilier A dépend du canton et du statut (imposition à la source, quasi-résident). **Pas d'argument fiscal dans les textes d'annonce** (textes communs Suisse + frontaliers).
   - **Exception décidée par Kevin le 02.11.2026 :** les 4 vidéos existantes (A, C, Long, AB-hookA) gardent la phrase « même avantage fiscal » (voix off et sous-titres), y compris dans la campagne fusionnée qui touche aussi la zone frontalière. Raison : la cible principale est la Suisse, la zone large apporte du volume ; c'est une comparaison banque/assurance, pas une promesse chiffrée. Décision assumée par Kevin. Pour les **nouvelles** créas, rester prudent sur la fiscalité.
9. **Plateformes :**
   - Meta : **catégorie spéciale « Produits et services financiers » (FINANCIAL_PRODUCTS_SERVICES), pays CH + FR — confirmé par Kevin**, déjà appliquée sur la campagne existante « 3P banque ». Respecter les restrictions de ciblage (âge, genre, lookalikes limités).
   - Google : la vérification « services financiers » s'applique dans toute l'UE, donc en France. Vérifier aussi pour la Suisse. Si elle est requise, me dire quoi fournir AVANT de créer les campagnes.
   - ChatGPT Ads : déclarer la catégorie **assurance** (pas services financiers, sinon refus — info Kevin). Vérifier que la diffusion est possible en Suisse et en France avant de prévoir quoi que ce soit.
10. Ton **naturel, informatif, convivial, rassurant**. Rien qui « fasse IA ».
11. En cas de doute réglementaire : demander, ne pas deviner.

## 4. Direction artistique

- **Couleurs :** encre `#0B1426` (bleu nuit) ; crème `#F4F1EA` ; rouge `#E63312`.
- **Typographies :** **Inter Tight Black** pour les titres ; **Instrument Serif italique** pour les mots d'accent.
- **Formats :** **9:16** (1080×1920, Reels, Stories) et **4:5** (1080×1350, fil d'actualité).
- **Zones de sécurité Meta en 9:16 :** rien d'important dans les **250 px du haut** ni dans les **400 px du bas**.
- **Sous-titres :** incrustés et synchronisés mot à mot, avec certains mots en rouge.
- **Style motion :** « app UI » moderne (cartes, relevés, coches, curseurs).
- **Voix :** voix de femme, Gemini 3.1 Flash TTS (via FLORA), preset **Kore**, français, **plus grave**, **débit plus rapide**.
- **Musique :** piste 2 (minimale, ElevenLabs), baissée sous la voix, s'arrête sur le dernier plan.
- **Bruitages :** clics, pops et whoosh sur les animations et les transitions.
- **Femme face caméra (vidéos avatar) :**
  - toujours **la même femme** : élégante, professionnelle, « sexy » mais jamais vulgaire ;
  - tenue retenue : **haut anthracite/bleu foncé + jupe crayon camel ajustée** ;
  - décor : bureau premium à Genève, **vue sur le Jet d'eau ou le Salève**, doux et réaliste ;
  - **plans face caméra courts**, en alternance avec du motion.

## 5. Créas produites

Voir `creas/creas-index.md` (source de vérité : fichier, angle, hook, format, durée, statut).

| Fichier | Contenu | Durée |
|---|---|---|
| `3emePilierA_A_9x16` / `_4x5` | Version A, typographique / motion | court |
| `3emePilierA_C_9x16` / `_4x5` | Version C, motion « soft 3D » (piliers ioniques) | court |
| `3emePilierA_Long_9x16` / `_4x5` | Face caméra + motion, hook **« Votre 3ème pilier A, vous l'avez choisi… ou on vous l'a vendu ? »** | ~52 s |
| `3emePilierA_AB-hookA_9x16` / `_4x5` | Face caméra + motion, hook **« Votre 3ème pilier A est en assurance ? Et la banque ? »** | 46,5 s |

- Versions B et D (autres hooks) : écrites, pas produites.
- Les vidéos utilisées en pub doivent être accessibles via une URL (ex. stockage cloud) pour l'upload par Adspirer.

## 6. Media buying (conversation dédiée, via Adspirer)

- **Document de campagne de départ :** https://claude.ai/artifact/2LUPUYfda4wD7Rzff552yU
- **État au 06.11.2026 : phase 1 EN COURS.** Une seule campagne Meta active : `3PA_Romandie-Frontaliers_2026-11` (`120251865264400642`), 100 CHF/jour, catégorie services financiers (CH + FR), ensemble `Romandie-Frontaliers_creas` (5 cantons romands + Sion/Monthey + 9 villes frontalières françaises à 25 km), formulaire « Lead gen 3P banque 2 », 6 pubs en 9:16 (V1 vendu, V2 Et la banque ?, V3 motion A, V4 motion C, F1 et F2 visuels fixes), identité Instagram @monpilier3. Lancée le 02.11.2026 au soir. Détails et IDs : `ads-journal.md`.
- **Contraintes Meta apprises :** catégorie services financiers = rayon minimum 25 km autour d'une ville, aucune exclusion de lieux possible (d'où une seule campagne Suisse + frontaliers) ; le compte Instagram doit avoir fait le choix « gratuit avec publicités » (Espace Comptes → Préférences publicitaires) sinon toutes les pubs sont bloquées (erreur #3858231) ; Adspirer ne garde pas le formulaire quand une pub a 2 formats (4:5 + 9:16) → une pub = un format.
- **Phase 1 (Meta), version validée le 02.11.2026 : voir `plan-phase1.md`** (2 campagnes, 4 vidéos + 2 visuels fixes). Version d'origine : test A/B des hooks « vendu » (Long) contre « Et la banque ? » (AB-hookA). Même audience, même budget, même formulaire. Deux zones séparées : Suisse romande / frontaliers (France voisine), car les règles et les performances diffèrent.
- **Règle de décision du test :** minimum 7 jours ET 10 leads par pub ; on tranche sur le **coût par lead qualifié**, puis sur le coût par RDV dès qu'il y a assez de données.
- **Phase 2 (Google Search), après validation de la phase 1 :** intentions fortes, par ex. « transférer 3ème pilier assurance banque », « résilier 3ème pilier assurance », « valeur de rachat 3ème pilier », « 3ème pilier assurance ou banque ». Volumes et CPC réels via Keyword Planner. Mots-clés négatifs (emploi, définition, PDF, noms de marques…).
- **Phase 3 (ChatGPT Ads), optionnelle :** seulement si la diffusion est disponible sur nos zones.
- **Seuils d'arrêt :** couper une annonce si dépense > 2× le coût par lead qualifié cible sans lead qualifié (200 CHF au démarrage, 100 CHF quand la cible passera à 50 CHF), après 7 jours minimum.
- **Scaling :** +20 % de budget maximum à la fois, pas plus d'une fois tous les 3 jours par campagne.

## 7. Règles de sécurité (non négociables)

- Toute campagne, ensemble de publicités ou annonce est créé **EN PAUSE**.
- Aucune activation, hausse de budget ou suppression **sans mon accord explicite** dans le chat.
- Sur Meta, les modifications de campagnes actives s'appliquent immédiatement : annoncer chaque modification avant de la faire.
- Après chaque création ou modification : relire l'objet créé et me montrer un récapitulatif. Ne pas se fier à un « done ».
- Économiser les tool calls Adspirer : regrouper les lectures, ne pas relancer une requête dont on a déjà le résultat.
- Toute génération payante (FLORA) est chiffrée en USD et validée avant d'être lancée.
- **Clés et tokens :** jamais dans le chat ni dans un fichier du dépôt. Variables d'environnement uniquement.
- **Sécurité des comptes Meta :** faux e-mails « Meta » (droits d'auteur, compte restreint, « Soumettre un appel ») = hameçonnage. Vérifier l'expéditeur (vrais domaines : @facebookmail.com, @support.facebook.com, @meta.com) et ne jamais cliquer. Les vraies restrictions s'affichent uniquement dans business.facebook.com/business-support-home. Incident du 03.11.2026 : clic sur un faux e-mail, mot de passe changé, sessions fermées, double authentification active (Facebook : SMS/WhatsApp ; Instagram : application). Ne jamais communiquer un code reçu par SMS/WhatsApp.

## 8. Organisation du projet

Les conversations Claude Code cloud ne partagent pas leurs fichiers : **tout ce qui doit être partagé vit dans le dépôt git du projet** (https://github.com/kpaulin1995-code/cabinet-3pilierA-ads). Chaque conversation fait `git pull` au début et `git commit` + `git push` à la fin.

```
cabinet-3pilierA-ads/
├── CLAUDE.md              ← ce fichier
├── creas/
│   └── creas-index.md     ← liste des créas : fichier, URL, angle, hook, format, statut (à tester / en test / gagnante / coupée)
├── sources/               ← scripts de montage (build*.py, sfx*.py) ; les MP4 sont stockés hors git (trop lourds) avec leur URL dans creas-index.md
├── ads-journal.md         ← historique media buying : date, changement, raison, résultat attendu, résultat observé
├── plan-phase1.md         ← plan de la phase 1 Meta (validé)
├── campagne.md            ← copie du document de campagne de départ
└── organique/             ← (conversation Organique) calendrier éditorial, textes, visuels des publications
```

- **Conversation « Créa » :** produit les créas, met à jour `creas/creas-index.md`. Avant une nouvelle série, lit `ads-journal.md` pour partir des angles gagnants.
- **Conversation « Media buying » :** utilise Adspirer, tient `ads-journal.md`, relit le journal avant chaque « point perf ».
- **Conversation « Organique » :** publications non payantes sur la Page Facebook « Mon Pilier 3.ch » et Instagram @monpilier3. Règles de conformité (§3) et DA (§4) identiques aux pubs. Tient `organique/` (calendrier, textes, visuels). Avant une nouvelle série, lit `ads-journal.md` pour reprendre les angles qui marchent en pub, et peut réutiliser les créas de `creas/`. Ne touche jamais aux campagnes payantes ni aux réglages du compte publicitaire.

## 9. Outils et méthode (conversation création)

- **Montage :** HyperFrames (HTML → vidéo), `npx hyperframes@0.8.185 check / snapshot / render`.
- **Scripts Python :** `build.py` (version A) ; `build_soft.py` (version C) ; `build_long.py` + `sfx_long.py` (version longue) ; `build_ab.py` + `sfx_ab.py` (version A/B).
- **FLORA** (abonnement payant, recharge auto activée) : images Nano Banana Pro ; voix Gemini 3.1 Flash TTS ; vidéo lip-sync MiniMax H3 (environ 0,19 $/s en 1080p). Toujours demander le devis (`quote`) avant une génération vidéo.
- **Lip-sync, ce qu'on a appris :**
  - le modèle réécrit l'audio : clips en **muet**, on garde **la voix off d'origine** ;
  - pas de silence à la **fin** de l'audio envoyé (sinon répétitions, ralentis, mots inventés) : le silence se met **au début**, puis on le saute au montage ;
  - prompts **uniquement visuels** (sinon elle récite le prompt) ; ajouter « real-time natural speed, no slow motion » et « keep exact framing, no zoom » ;
  - vérifier la synchro par **corrélation de l'enveloppe audio** (Whisper est imprécis) ;
  - **couper chaque plan face caméra exactement à la fin de la phrase**.
- **Mix audio :** voix à -15 LUFS ; musique à -22 LUFS, baissée automatiquement sous la voix ; limiteur en sortie.

## 10. Prochaines étapes

- **Media buying :** ne rien modifier sur la campagne avant le 09.11.2026 (apprentissage Meta) ; « point perf » quotidien ; Kevin remonte la qualité des leads (qualifié / RDV / transfert / capital) ; remontée des conversions vers Meta à mettre en place ; tester le texte 2 et les versions 4:5 plus tard ; Google Search (phase 2) seulement quand Kevin le demande.
- **Création :** hooks B et D ; déclinaisons courtes (15 s) pour les Stories ; nouvelles créas sans argument fiscal (§3.8).
- **Organique :** à lancer dans une conversation dédiée (§8).
- **Champs encore vides :** statut réglementaire et n° d'inscription (§1), coût par RDV et taux de joignabilité (§2), ancienneté minimale et seuils de prime (§2), CRM ou Google Sheet et délai de rappel (§2).
