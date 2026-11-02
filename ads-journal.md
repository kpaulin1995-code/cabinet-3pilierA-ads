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

## 2026-11-02 — Étape 1 (audit, lecture seule) : premiers constats

- **Campagne existante :** « 3P banque » (`120251826305830642`), **ACTIVE** depuis le 31.10.2026, créée par Kevin hors de cette conversation. Prospects, CBO 25 CHF/jour, catégorie spéciale FINANCIAL_PRODUCTS_SERVICES (FR, CH). 1 ensemble « Transfert 3A Banque » : Bâle +30 km, Genève +45 km, Lausanne +30 km, Neuchâtel +30 km, 25–65 ans, Advantage+ Audience. 1 publicité « HOOK C » (1 texte, 3 titres, 2 descriptions).
- **Résultats à vie (au 02.11) :** 78,34 CHF dépensés, 910 impressions, 607 personnes atteintes, 9 clics, CTR 0,99 %, CPC 8,70 CHF. Leads : 1 sur le formulaire « Lead gen 3P banque 2 » (Adspirer compte 0 conversion sur 90 jours, données de la veille).
- **Formulaires de la Page :** « Lead gen 3P banque 2 » `1790789782189392` (1 lead) ; « Analyse gratuite de votre 3ème pilier A » `2079258669399367` (3 leads) ; « 3e pilier ouvert avant 2017 ? (v1) » `2644410509293100` (0 lead).
- **Pixel Meta :** aucun sur le compte publicitaire.
- **Décisions de Kevin :** formulaire simple existant (volume, peu de friction) ; Meta = services financiers ; ChatGPT Ads = catégorie assurance. Reportées dans `CLAUDE.md`.
- **Points à trancher :** Bâle est germanophone (hors cible) ; Genève +45 km mélange Suisse et frontaliers dans un même ensemble ; que faire de « 3P banque » au lancement de la phase 1 (pause ou maintien) ; la catégorie FINANCIAL_PRODUCTS_SERVICES n'est pas dans la liste d'Adspirer à la création → piste : dupliquer « 3P banque » (garde la catégorie) puis modifier.
- **Quota Adspirer :** 6 / 15 appels utilisés.

## 2026-11-02 — Décisions de Kevin pour la phase 1 (plan en préparation)

- **Formulaire :** « Lead gen 3P banque 2 » (`1790789782189392`) confirmé.
- **« 3P banque » :** mise en pause au lancement de la phase 1 (accord de Kevin ; pas avant).
- **Périmètre élargi :** au lieu du seul test Long contre AB-hookA, on teste plus de contenus : Long (« vendu »), AB-hookA (« Et la banque ? »), motion A, motion C, plus des **visuels fixes** (à produire par la conversation Créa).
- **Structure :** **2 campagnes** séparées : Suisse romande (résidents francophones) et frontaliers.
- **Budget :** recommandation demandée (voir réponse du 02.11 : ~75 CHF/jour, ~2 300 CHF/mois), en attente de validation.
- **Outils Adspirer utiles trouvés :** `duplicate_meta_campaign` (garde catégorie spéciale + formulaire) ; `add_meta_ad` accepte `placement_specific_videos` (feed + stories/reels dans une même publicité) et `story_image_url` pour les visuels fixes.

## 2026-11-02 — Plan phase 1 rédigé (en attente de validation)

- **Budget validé par Kevin :** 50 CHF/jour par campagne (Suisse romande + frontaliers), soit ~3 040 CHF/mois. Reporté dans `CLAUDE.md`.
- **Infos :** nom légal Tellancia Sàrl (DSA) ; site https://monpilier3.ch.
- **Plan :** `plan-phase1.md` (structure, ciblage, contenus, textes, règles de décision, points bloquants).
- **Créa :** demande de devis envoyée pour 2 visuels fixes (4:5 + 9:16), aucune génération payante sans accord de Kevin.

## 2026-11-02 — Plan phase 1 validé

- **Validé par Kevin :** `plan-phase1.md` (structure, ciblage, textes). Instagram relié, formulaire et lien de confidentialité OK.
- **Coût par lead qualifié :** 100 CHF au démarrage, objectif ~50 CHF ensuite. Seuil de coupe 200 CHF sans lead qualifié. Reporté dans `CLAUDE.md`.
- **Visuels fixes :** version gratuite validée (images clés existantes), production en cours côté Créa. Vérification de la fin des plans de « vendu » demandée.
- **Reste bloquant avant création :** forfait Adspirer (Kevin s'en occupe) ; fin des plans de V1 « vendu ».

## 2026-11-02 — Étape 3 (création, tout en pause) : campagnes et ciblage CH

- **Adspirer :** forfait Plus (150 appels/mois) activé par Kevin.
- **Créé (PAUSE) :** duplication de « 3P banque » (aucune pub copiée, catégorie FINANCIAL_PRODUCTS_SERVICES FR+CH conservée, formulaire non encore attaché — il le sera avec les pubs) :
  - `3PA_CH-Romande_2026-11` (`120251865264400642`), CBO **50 CHF/jour**, ensemble `CH-Romande_large` (`120251865264420642`) : cantons GE, VD, NE, JU, FR + Sion et Monthey (+25 km), 25–65 ans, Facebook/Instagram/Messenger, langue Français (tout) envoyée (à vérifier dans le gestionnaire), Advantage+ Audience activé (hérité).
  - `3PA_Frontaliers_2026-11` (`120251865273950642`), CBO **50 CHF/jour**, ensemble `Transfert 3A Banque` (`120251865273970642`) **pas encore modifié** (ciblage hérité de « 3P banque », dont Bâle).
- **Contraintes Meta (catégorie services financiers) découvertes :** rayon minimum autour d'une ville (15 km refusé, 25 km accepté) ; **exclusion de lieux interdite** → impossible d'exclure la Suisse de la campagne frontaliers. Décision demandée à Kevin.
- **Instagram :** Adspirer ne voit encore aucun compte Instagram lié ou autorisé sur le compte publicitaire.
- **Pubs :** pas encore créées (attente : Instagram visible, fin des plans de « vendu », visuels fixes).

## 2026-11-02 — Fusion en une seule campagne (accord de Kevin : « ok fusion »)

- **Raison :** catégorie services financiers = pas d'exclusion de lieux + rayon minimum 25 km → chevauchement inévitable entre 2 campagnes (Genève dans les cercles des villes françaises), donc données faussées.
- **Fait (relu après modification) :** `3PA_Romandie-Frontaliers_2026-11` (`120251865264400642`) PAUSE, 100 CHF/jour, catégorie FINANCIAL_PRODUCTS_SERVICES FR+CH ; ensemble `Romandie-Frontaliers_large` : 5 cantons + Sion/Monthey + 9 villes françaises à 25 km, 25–65 ans, FB/IG/Messenger. `3PA_Frontaliers_2026-11` archivée.
- **Non visible dans la relecture Adspirer (à vérifier dans le gestionnaire) :** langue Français (tout), DSA Tellancia Sàrl.
- **Textes :** communs, sans argument fiscal (voir `plan-phase1.md` §5).
- **Résultat attendu :** pas de chevauchement ; lecture Suisse / France par le découpage par pays et la question du formulaire.
- **Reste avant les pubs :** Instagram attribué au compte publicitaire (Kevin) ; fin des plans de « vendu » (Créa) ; visuels fixes (Créa).

## 2026-11-02 — Livraison Créa et point de conformité vidéos

- **Visuels fixes (0 $) :** `creas/exports/visuels/3emePilierA_V1-banque_{4x5,9x16}.png`, `3emePilierA_V2-vendu_{4x5,9x16}.png` — dimensions et URL raw vérifiées (HTTP 200). Contrôle visuel : conformes (« 3ème pilier A », pas de marque, pas de chiffre, rien de fiscal). Remarques : V2 = chemisier crème (DA : haut anthracite/bleu foncé) ; V1 = vue fenêtre surexposée, Jet d'eau peu visible.
- **Vidéo Long :** fin du plan 2 corrigée par la Créa (visage masqué à 21,15 s, voix finie à 21,13 s), nouveaux MP4 aux mêmes URL. Plus bloquant.
- **⚠️ Conformité :** les 4 vidéos disent « même avantage fiscal » (Long et C : « Même avantages fiscales », faute d'accord) en voix off et sous-titres. La campagne fusionnée vise aussi les frontaliers → contraire à `CLAUDE.md` §3.8. Décision demandée à Kevin : variantes sans la phrase (quelques centimes FLORA + rendu) et/ou lancement avec les visuels fixes seuls.

## 2026-11-02 — Décisions de Kevin : vidéos telles quelles, visuels à retoucher

- **Vidéos :** option C, les 4 vidéos restent avec « même avantage fiscal » (décision assumée par Kevin, exception notée dans `CLAUDE.md` §3.8). Textes d'annonce toujours sans argument fiscal.
- **Visuels fixes :** retouches demandées à la Créa (tenue DA sur « vendu », vue lisible sur « Et la banque ? »), gratuit en priorité, plafond FLORA 0,72 $ accepté par Kevin.
- **Instagram :** Kevin guidé pour attribuer le compte Instagram au compte publicitaire.

## 2026-11-02 — Création des pubs : blocages techniques

- **Instagram :** @monpilier3 (`17841457576459624`) autorisé sur le compte publicitaire et relié à la Page (vérifié via Adspirer).
- **Vidéos « vendu » téléversées dans la bibliothèque Meta** (l'appel a expiré après l'envoi) : 4:5 = `2123172968307143`, 9:16 = `2576681176130074` (identifiées par la taille des miniatures). Réutilisables sans renvoi.
- **Blocage 1 :** l'ensemble copié `Romandie-Frontaliers_large` (`120251865264420642`) est un ensemble **contenu dynamique** (hérité de « 3P banque ») → 1 seule pub possible. Il faut un nouvel ensemble classique.
- **Blocage 2 :** Meta refuse plusieurs textes/titres dans une pub qui a une vidéo par format (4:5 + 9:16) → 1 texte + 1 titre par pub (texte 1 / titre 1), le texte 2 sera testé plus tard.
- **Blocage 3 :** création du nouvel ensemble refusée « Aucun annonceur indiqué » (DSA) malgré `dsa_beneficiary` envoyé (« Tellancia Sàrl » puis « Tellancia Sarl ») → Adspirer ne semble pas le transmettre à la création. Solution demandée à Kevin : définir le bénéficiaire/payeur par défaut dans les paramètres du compte publicitaire Meta.
- **Rien n'a été créé à cette étape** (aucune pub, aucun nouvel ensemble). Campagne toujours en pause.

## 2026-11-02 — DSA réglé, nouveau blocage Instagram

- **DSA :** Kevin a défini le bénéficiaire/payeur par défaut → plus d'erreur « Aucun annonceur indiqué ».
- **Blocage :** Meta refuse la pub : « Le ou la propriétaire de @monpilier3 doit se connecter à Instagram et choisir d'utiliser les produits Meta gratuitement ou de s'abonner » (choix publicitaire européen, code 3858231). Action de Kevin dans l'app Instagram.
- **Vérifié :** rien n'a été créé (toujours 1 ensemble, 0 pub). Campagne en pause.

## 2026-11-02 — Étape 3 terminée : 6 pubs créées (campagne en pause)

- **Identité Instagram :** option A validée par Kevin → pubs créées **sans** compte @monpilier3 (diffusion Instagram au nom de la Page, comme « 3P banque »). Aucun impact sur la diffusion. Kevin pourra faire le choix « gratuit avec publicités » sur @monpilier3 plus tard.
- **Nouvel ensemble classique** `Romandie-Frontaliers_creas` (`120251865837390642`), même ciblage que `Romandie-Frontaliers_large` (5 cantons + Sion/Monthey + 9 villes FR à 25 km, 25–65 ans, FB/IG/Messenger), langue Français (tout), Advantage+ Audience désactivé, formulaire `1790789782189392`, DSA Tellancia Sàrl (défaut du compte).
- **Ancien ensemble** `Romandie-Frontaliers_large` (`120251865264420642`, contenu dynamique) : vide, en pause. À archiver (accord de Kevin à demander).
- **Formats :** 9:16 uniquement (Adspirer perd le formulaire quand une pub a 2 formats). Kevin ajoutera les 4:5 dans le gestionnaire.
- **Textes :** texte 1 + titre 1 + description + « En savoir plus » sur les 6 pubs (Meta refuse plusieurs textes avec la personnalisation par placement ; on a gardé la même règle partout pour comparer les créas à égalité).
- **Pubs (relues) :**
  - V1_Long_vendu `120251865837880642` (vidéo `2576681176130074`)
  - V2_AB-hookA_banque `120251865862330642`
  - V3_motion_A `120251865873810642`
  - V4_motion_C `120251865900470642`
  - F1_visuel_banque `120251865912770642` (image `269d862a68da8782ad0717b7b6b1b59f`)
  - F2_visuel_vendu `120251865917200642` (image `df765327f7dc06dda72e1bf5e2fe4ce7`)
  - Statut : en examen Meta ; campagne PAUSE, rien ne diffuse.
- **Point d'attention :** les options « Advantage+ Creative » diffèrent entre pubs (V1–V3 : 1 option désactivée ; V4, F1, F2 : 83 désactivées). À harmoniser dans le gestionnaire si on veut une comparaison stricte.
- **Au « lance » :** activer campagne + ensemble `_creas` + 6 pubs ; mettre « 3P banque » en pause.

## 2026-11-02 — Nettoyage du compte (demande de Kevin)

- **Supprimé :** ensemble vide `Romandie-Frontaliers_large` (`120251865264420642`, ancien ensemble à contenu dynamique, 0 pub).
- **Non supprimé (refusé par Kevin au moment de l'appel) :** campagne vide `3PA_Frontaliers_2026-11` (`120251865273950642`), qui reste **archivée** (masquée de la liste des campagnes, ne diffuse pas).
- **Vérifié après nettoyage :** `3PA_Romandie-Frontaliers_2026-11` intacte, en pause, 1 ensemble `Romandie-Frontaliers_creas`, 6 pubs (en examen Meta). Options Advantage+ Creative désormais identiques sur les 6 pubs (1 option désactivée chacune).
- **Compte Meta à ce jour :** 2 campagnes visibles : `3PA_Romandie-Frontaliers_2026-11` (pause) et « 3P banque » (active, à mettre en pause au lancement).

## 2026-11-02 — Instagram dissocié du compte publicitaire

- **Problème :** erreur Meta #3858231 sur les pubs (choix « gratuit avec publicités » non fait sur @monpilier3), Meta associant automatiquement @monpilier3.
- **Action de Kevin :** @monpilier3 dissocié du compte publicitaire Tellancia (lien avec la Page conservé).
- **Vérifié :** Adspirer ne voit plus aucun compte Instagram sur le compte publicitaire. Les 6 pubs sont passées de « en examen » à **PAUSED** (examen terminé, aucun refus affiché). Campagne et ensemble en pause.
- **À confirmer par Kevin dans le gestionnaire :** l'erreur #3858231 a disparu ; sinon recréer la pub concernée.
