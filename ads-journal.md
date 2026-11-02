# Journal media buying

Une entrée par changement : date, changement, raison, résultat attendu, résultat observé.
Tenu par la conversation « Media buying ». Relu avant chaque « point perf ».

---

## 2026-11-02 — Mise en place du dépôt

- **Changement :** création du dépôt partagé (`CLAUDE.md`, `campagne.md`, `creas/creas-index.md`, `ads-journal.md`).
- **Raison :** partager le contexte entre les conversations Créa et Media buying.
- **État des campagnes :** aucune campagne créée par cette conversation. Existant côté Meta : à auditer (étape 1).
- **En attente :** champs [X] de `CLAUDE.md`, URL des vidéos, connexion Adspirer.

## 2026-11-02 — Point d'étape (reprise dans une nouvelle conversation)

- **Fait :** démarrage terminé (résumé de l'offre, de la cible, des créas et des champs [X]) ; dépôt créé ; conversation Créa (session_01Ce2igHwq61LuWqDpyEBitL) sollicitée pour pousser sources + MP4 dans `creas/exports/` et mettre à jour `creas-index.md`.
- **Adspirer :** connecteur claude.ai « Adspirer Ads & Performance Marketing Agent » en cours de connexion par Kevin → la conversation media buying redémarre dans une nouvelle session (les connecteurs sont chargés au démarrage).
- **Reste à faire avant l'étape 1 :** réponses de Kevin aux questions [X] (budget mensuel et répartition CH / frontaliers, coût cible par lead qualifié et par RDV, joignabilité, ancienneté minimale et seuils de prime, nombre de leads pour trancher, CRM ou Sheet + délai de rappel, statut FINMA / LSFin + n°, URL politique de confidentialité et site, durée du RDV) ; URL publiques des vidéos.
- **Choix retenu :** le test phase 1 suit `CLAUDE.md` (Long contre AB-hookA), pas le document de campagne (A contre C).

## 2026-11-02 — Étape 0 : Adspirer connecté (même conversation, pas besoin d'en rouvrir une)

- **Connecteur :** « Adspirer Ads & Performance Marketing Agent », compte « Tellancia ».
- **Comptes connectés :** Meta Ads `2066124837429413` ; Google Ads `7671208058` ; ChatGPT Ads `adacct_6ae386b8ce5c8190a073ee7e50c4e8eb`.
- **Page Facebook :** « Mon Pilier 3.ch » (`1018016868067458`). **Aucun compte Instagram lié** à la Page.
- **Forfait Adspirer : gratuit, 15 appels/mois** (1 utilisé, remise à zéro le 02.12.2026). Les recherches d'outils et les schémas ne comptent pas.
- **Limites d'Adspirer constatées (schémas des outils) :**
  - pas de création de formulaire instantané (seulement lister les formulaires / lire les leads) → le formulaire se crée dans Meta, puis on passe son ID ;
  - pas d'outil de test A/B Meta → deux ensembles de publicités identiques hors créa ;
  - une seule vidéo par publicité (pas de 9:16 + 4:5 dans la même publicité via la personnalisation des placements) ;
  - catégories spéciales proposées : HOUSING, CREDIT, EMPLOYMENT, ISSUES_ELECTIONS_POLITICS ; la catégorie « Produits et services financiers » n'apparaît pas sous ce nom (à vérifier) ;
  - champ DSA (bénéficiaire / payeur) obligatoire pour les ensembles qui ciblent la France.
- **Vidéos :** dépôt rendu public ; URL raw GitHub vérifiées (HTTP 200, taille exacte) et notées dans `creas/creas-index.md`.
