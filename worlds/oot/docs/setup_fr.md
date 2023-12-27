# Guide d'installation Archipelago pour Ocarina of Time 

## Important

Comme nous utilisons BizHawk, ce guide ne s'applique qu'aux systèmes Windows et Linux.

## Logiciel requis

- BizHawk : [BizHawk sort de TASVideos] (https://tasvideos.org/BizHawk/ReleaseHistory)
   - Les versions 2.3.1 et ultérieures sont prises en charge. La version 2.7 est recommandée pour la stabilité.
   - Des instructions d'installation détaillées pour BizHawk peuvent être trouvées sur le lien ci-dessus.
   - Les utilisateurs Windows doivent d'abord exécuter le programme d'installation prereq, qui peut également être trouvé sur le lien ci-dessus.
- Le client Archipelago intégré, qui peut être installé [ici](https://github.com/ArchipelagoMW/Archipelago/releases)
   (sélectionnez `Ocarina of Time Client` lors de l'installation).
- Une ROM Ocarina of Time v1.0.

## Configuration de BizHawk

Une fois BizHawk installé, ouvrez BizHawk et modifiez les paramètres suivants :

- Allez dans Config > Personnaliser. Basculez vers l'onglet Avancé, puis basculez le Lua Core de "NLua+KopiLua" vers
   "Interface Lua+Lua". Redémarrez ensuite BizHawk. Ceci est nécessaire pour que le script Lua fonctionne correctement.
   **REMARQUE : Même si "Lua+LuaInterface" est déjà sélectionné, basculez entre les deux options et resélectionnez-le. Nouvelles installations**
   ** des versions plus récentes de BizHawk ont tendance à afficher "Lua+LuaInterface" comme option sélectionnée par défaut mais se chargent toujours **
   **"NLua+KopiLua" jusqu'à ce que cette étape soit terminée.**
- Sous Config > Personnaliser > Avancé, assurez-vous que la case pour AutoSaveRAM est cochée et cliquez sur le bouton 5s.
   Cela réduit la possibilité de perdre des données de sauvegarde en cas de plantage de l'émulateur.
- Sous Config > Personnaliser, cochez les cases "Exécuter en arrière-plan" et "Accepter la saisie en arrière-plan". Cela vous permettra de
   continuer à jouer en arrière-plan, même si une autre fenêtre est sélectionnée.
- Sous Config> Raccourcis clavier, de nombreux raccourcis clavier sont répertoriés, dont beaucoup sont liés aux touches communes du clavier. Vous voudrez probablement
   désactiver la plupart d'entre eux, ce que vous pouvez faire rapidement en utilisant `Esc`.
- Si vous jouez avec une manette, lorsque vous liez les commandes, désactivez "P1 A Up", "P1 A Down", "P1 A Left" et "P1 A Right"
   car ceux-ci interfèrent avec la visée s'ils sont liés. Définissez l'entrée directionnelle à l'aide de l'onglet Analogique à la place.
- Sous N64, activez "Utiliser l'emplacement d'extension". Ceci est nécessaire pour que les sauvegardes fonctionnent.
   (Le menu N64 n'apparaît qu'après le chargement d'une ROM.)

Il est fortement recommandé d'associer les extensions de rom N64 (\*.n64, \*.z64) au BizHawk que nous venons d'installer.
Pour ce faire, nous devons simplement rechercher n'importe quelle rom N64 que nous possédons, faire un clic droit et sélectionner "Ouvrir avec ...", dépliez
la liste qui apparaît et sélectionnez l'option du bas "Rechercher une autre application", puis naviguez jusqu'au dossier BizHawk
et sélectionnez EmuHawk.exe.

Un guide de configuration BizHawk alternatif ainsi que divers conseils de dépannage peuvent être trouvés
[ici](https://wiki.ootrandomizer.com/index.php?title=Bizhawk).

## Configuration de votre fichier YAML

### Qu'est-ce qu'un fichier YAML et pourquoi en ai-je besoin ?

Votre fichier YAML contient un ensemble d'options de configuration qui fournissent au générateur des informations sur la façon dont il doit
générer votre jeu. Chaque joueur d'un multimonde fournira son propre fichier YAML. Cette configuration permet à chaque joueur de profiter
d'une expérience personnalisée à leur goût, et différents joueurs dans le même multimonde peuvent tous avoir des options différentes.

### Où puis-je obtenir un fichier YAML ?

Un yaml OoT de base ressemblera à ceci. Il y a beaucoup d'options cosmétiques qui ont été supprimées pour le plaisir de ce
tutoriel, si vous voulez voir une liste complète, téléchargez Archipelago depuis
la [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases) et recherchez l'exemple de fichier dans
le dossier "Lecteurs".

``` yaml
description: Modèle par défaut d'Ocarina of Time # Utilisé pour décrire votre yaml. Utile si vous avez plusieurs fichiers
# Votre nom dans le jeu. Les espaces seront remplacés par des underscores et il y a une limite de 16 caractères
name: VotreNom
game:
  Ocarina of Time: 1
requires:
  version: 0.1.7 # Version d'Archipelago requise pour que ce yaml fonctionne comme prévu.
# Options partagées prises en charge par tous les jeux :
accessibility:
  items: 0 # Garantit que vous pourrez acquérir tous les articles, mais vous ne pourrez peut-être pas accéder à tous les emplacements
  locations: 50 # Garantit que vous pourrez accéder à tous les emplacements, et donc à tous les articles
  none: 0 # Garantit seulement que le jeu est battable. Vous ne pourrez peut-être pas accéder à tous les emplacements ou acquérir tous les objets
progression_balancing: # Un système pour réduire le BK, comme dans les périodes où vous ne pouvez rien faire, en déplaçant vos éléments dans une sphère d'accès antérieure
  0: 0 # Choisissez un nombre inférieur si cela ne vous dérange pas d'avoir un multimonde plus long, ou si vous pouvez glitch / faire du hors logique.
  25: 0
  50: 50 # Faites en sorte que vous ayez probablement des choses à faire.
  99: 0 # Obtenez les éléments importants tôt et restez en tête de la progression.
Ocarina of Time:
  logic_rules: # définit la logique utilisée pour le générateur.
    glitchless: 50
    glitched: 0
    no_logic: 0
  logic_no_night_tokens_without_suns_song: # Les skulltulas nocturnes nécessiteront logiquement le Chant du soleil.
    false: 50
    true: 0
  open_forest: # Définissez l'état de la forêt de Kokiri et du chemin vers l'arbre Mojo.
    open: 50
    closed_deku: 0
    closed: 0
  open_kakariko: # Définit l'état de la porte du village de Kakariko.
    open: 50
    zelda: 0
    closed: 0
  open_door_of_time: # Ouvre la Porte du Temps par défaut, sans le Chant du Temps.
    false: 0
    true: 50
  zora_fountain: # Définit l'état du roi Zora, bloquant le chemin vers la fontaine de Zora.
    open: 0
    adult: 0
    closed: 50
  gerudo_fortress: # Définit les conditions d'accès à la forteresse Gerudo.
    normal: 0
    fast: 50
    open: 0
  bridge: # Définit les exigences pour le pont arc-en-ciel.
    open: 0
    vanilla: 0
    stones: 0
    medallions: 50
    dungeons: 0
    tokens: 0
  trials: # Définit le nombre d'épreuves requises dans le Château de Ganon.
    # vous pouvez ajouter des valeurs supplémentaires entre minimum et maximum
    0: 50 # valeur minimale
    6: 0 # valeur maximale
    random: 0
    random-low: 0
    random-higt: 0
  starting_age: # Choisissez l'âge auquel Link commencera.
    child: 50
    adult: 0
  triforce_hunt: # Rassemblez des morceaux de la Triforce dispersés dans le monde entier pour terminer le jeu.
    false: 50
    true: 0
  triforce_goal: # Nombre de pièces Triforce nécessaires pour terminer le jeu. Nombre total placé déterminé par le paramètre Item Pool.
    # vous pouvez ajouter des valeurs supplémentaires entre minimum et maximum
    1: 0 # valeur minimale
    50: 0 # valeur maximale
    random: 0
    random-low: 0
    random-higt: 0
    20: 50
  bombchus_in_logic: # Les Bombchus sont correctement pris en compte dans la logique. Le premier pack trouvé aura 20 chus ; Kokiri Shop et Bazaar vendent des recharges ; bombchus ouvre Bombchu Bowling.
    false: 50
    true: 0
  bridge_stones: # Définissez le nombre de pierres spirituelles requises pour le pont arc-en-ciel.
    # vous pouvez ajouter des valeurs supplémentaires entre minimum et maximum
    0: 0 # valeur minimale
    3: 50 # valeur maximale
    random: 0
    random-low: 0
    random-high: 0
  bridge_medallions: # Définissez le nombre de médaillons requis pour le pont arc-en-ciel.
    # vous pouvez ajouter des valeurs supplémentaires entre minimum et maximum
    0: 0 # valeur minimale
    6: 50 # valeur maximale
    random: 0
    random-low: 0
    random-high: 0
  bridge_rewards: # Définissez le nombre de récompenses de donjon requises pour le pont arc-en-ciel.
    # vous pouvez ajouter des valeurs supplémentaires entre minimum et maximum
    0: 0 # valeur minimale
    9: 50 # valeur maximale
    random: 0
    random-low: 0
    random-high: 0
  bridge_tokens: # Définissez le nombre de jetons Gold Skulltula requis pour le pont arc-en-ciel.
    # vous pouvez ajouter des valeurs supplémentaires entre minimum et maximum
    0: 0 # valeur minimale
    100: 50 # valeur maximale
    random: 0
    random-low: 0
    random-high: 0
  shuffle_mapcompass: # Contrôle où mélanger les cartes et boussoles des donjons.
    remove: 0
    startwith: 50
    vanilla: 0
    dungeon: 0
    overworld: 0
    any_dungeon: 0
    keysanity: 0
  shuffle_smallkeys: # Contrôle où mélanger les petites clés de donjon.
    remove: 0
    vanilla: 0
    dungeon: 50
    overworld: 0
    any_dungeon: 0
    keysanity: 0
  shuffle_hideoutkeys: # Contrôle où mélanger les petites clés de la Forteresse Gerudo.
    vanilla: 50
    overworld: 0
    any_dungeon: 0
    keysanity: 0
  shuffle_bosskeys: # Contrôle où mélanger les clés du boss, à l'exception de la clé du boss du château de Ganon.
    remove: 0
    vanilla: 0
    dungeon: 50
    overworld: 0
    any_dungeon: 0
    keysanity: 0
  shuffle_ganon_bosskey: # Contrôle où mélanger la clé du patron du château de Ganon.
    remove: 50
    vanilla: 0
    dungeon: 0
    overworld: 0
    any_dungeon: 0
    keysanity: 0
    on_lacs: 0
  enhance_map_compass: # La carte indique si un donjon est vanille ou MQ. La boussole indique quelle est la récompense du donjon.
    false: 50
    true: 0
  lacs_condition: # Définissez les exigences pour la cinématique de la Flèche lumineuse dans le Temple du temps.
    vanilla: 50
    stones: 0
    medallions: 0
    dungeons: 0
    tokens: 0
  lacs_stones: # Définissez le nombre de pierres spirituelles requises pour le LACS.
     # vous pouvez ajouter des valeurs supplémentaires entre minimum et maximum
     0: 0 # valeur minimale
     3: 50 # valeur maximale
    random: 0
    random-low: 0
    random-high: 0
  lacs_medallions: # Définissez le nombre de médaillons requis pour LACS.
    # vous pouvez ajouter des valeurs supplémentaires entre minimum et maximum
    0: 0 # valeur minimale
    6: 50 # valeur maximale
    random: 0
    random-low: 0
    random-high: 0
  lacs_rewards: # Définissez le nombre de récompenses de donjon requises pour LACS.
    # vous pouvez ajouter des valeurs supplémentaires entre minimum et maximum
    0: 0 # valeur minimale
    9: 50 # valeur maximale
    random: 0
    random-low: 0
    random-high: 0
  lacs_tokens: # Définissez le nombre de jetons Gold Skulltula requis pour le LACS.
     # vous pouvez ajouter des valeurs supplémentaires entre minimum et maximum
     0: 0 # valeur minimale
     100: 50 # valeur maximale
    random: 0
    random-low: 0
    random-high: 0
  shuffle_song_items: # Définit où les chansons peuvent apparaître.
    song: 50
    dungeon: 0
    any: 0
  shopsanity: # Randomise le contenu de la boutique. Réglez sur "off" pour ne pas mélanger les magasins ; "0" mélange les magasins mais ne n'autorise pas les articles multimonde dans les magasins.
    0: 0
    1: 0
    2: 0
    3: 0
    4: 0
    random_value: 0
    off: 50
  tokensanity : # les récompenses en jetons des Skulltulas dorées sont mélangées dans la réserve.
    off: 50
    dungeons: 0
    overworld: 0
    all: 0
  shuffle_scrubs: # Mélangez les articles vendus par Business Scrubs et fixez les prix.
    off: 50
    low: 0
    regular: 0
    random_prices: 0
  shuffle_cows: # les vaches donnent des objets lorsque la chanson d'Epona est jouée.
    false: 50
    true: 0
  shuffle_kokiri_sword: # Mélangez l'épée Kokiri dans la réserve d'objets.
    false: 50
    true: 0
  shuffle_ocarinas: # Mélangez l'Ocarina des fées et l'Ocarina du temps dans la réserve d'objets.
    false: 50
    true: 0
  shuffle_weird_egg: # Mélangez l'œuf bizarre de Malon au château d'Hyrule.
    false: 50
    true: 0
  shuffle_gerudo_card: # Mélangez la carte de membre Gerudo dans la réserve d'objets.
    false: 50
    true: 0
  shuffle_beans: # Ajoute un paquet de 10 haricots au pool d'objets et change le vendeur de haricots pour qu'il vende un objet pour 60 roupies.
    false: 50
    true: 0
  shuffle_medigoron_carpet_salesman: # Mélangez les objets vendus par Medigoron et le vendeur de tapis Haunted Wasteland.
    false: 50
    true: 0
  skip_child_zelda: # le jeu commence avec la lettre de Zelda, l'objet de la berceuse de Zelda et les événements pertinents déjà terminés.
    false: 50
    true: 0
  no_escape_sequence: # Ignore la séquence d'effondrement de la tour entre les combats de Ganondorf et de Ganon.
    false: 50
    true: 0
  no_guard_stealth: # Le vide sanitaire du château d'Hyrule passe directement à Zelda.
    false: 50
    true: 0
  no_epona_race: # Epona peut toujours être invoquée avec Epona's Song.
    false: 50
    true: 0
  skip_some_minigame_phases: # Dampe Race et Horseback Archery donnent les deux récompenses si la deuxième condition est remplie lors de la première tentative.
    false: 50
    true: 0
   complete_mask_quest: # Tous les masques sont immédiatement disponibles à l'emprunt dans la boutique Happy Mask.
    false: 50
    true: 0
  useful_cutscenes: # Réactive la cinématique Poe dans le Temple de la forêt, Darunia dans le Temple du feu et l'introduction de Twinrova. Surtout utile pour les pépins.
    false: 50
    true: 0
  fast_chests: # Toutes les animations des coffres sont rapides. Si désactivé, les éléments principaux ont une animation lente.
    false: 50
    true: 0
  free_scarecrow: # Sortir l'ocarina près d'un point d'épouvantail fait apparaître Pierre sans avoir besoin de la chanson.
    false: 50
    true: 0
  fast_bunny_hood: # Bunny Hood vous permet de vous déplacer 1,5 fois plus vite comme dans Majora's Mask.
    false: 50
    true: 0
  chicken_count: # Contrôle le nombre de Cuccos pour qu'Anju donne un objet en tant qu'enfant.
    \# vous pouvez ajouter des valeurs supplémentaires entre le minimum et le maximum
    0: 0 # valeur minimale
    7: 50 # valeur maximale
    random: 0
    random-low: 0
    random-high: 0
  hints: # les pierres à potins peuvent donner des indices sur l'emplacement des objets.
    none: 0
    mask: 0
    agony: 0
    always: 50
  hint_dist: # Choisissez la distribution d'astuces à utiliser. Affecte la fréquence des indices forts, quels éléments sont toujours indiqués, etc.
    balanced: 50
    ddr: 0
    league: 0
    mw2: 0
    scrubs: 0
    strong: 0
    tournament: 0
    useless: 0
    very_strong: 0
  text_shuffle: # Randomise le texte dans le jeu pour un effet comique.
    none: 50
    except_hints: 0
    complete: 0
  damage_multiplier: # contrôle la quantité de dégâts subis par Link.
    half: 0
    normal: 50
    double: 0
    quadruple: 0
    ohko: 0
  no_collectible_hearts: # les cœurs ne tomberont pas des ennemis ou des objets.
    false: 50
    true: 0
  starting_tod: # Changer l'heure de début de la journée.
    default: 50
    sunrise: 0
    morning: 0
    noon: 0
    afternoon: 0
    sunset: 0
    evening: 0
    midnight: 0
    witching_hour: 0
  start_with_consumables: # Démarrez le jeu avec des Deku Sticks et des Deku Nuts pleins.
    false: 50
    true: 0
  start_with_rupees: # Commencez avec un portefeuille plein. Les mises à niveau de portefeuille rempliront également votre portefeuille.
    false: 50
    true: 0
  item_pool_value: # modifie le nombre d'objets disponibles dans le jeu.
    plentiful: 0
    balanced: 50
    scarce: 0
    minimal: 0
  junk_ice_traps: # Ajoute des pièges à glace au pool d'objets.
    off: 0
    normal: 50
    on: 0
    mayhem: 0
    onslaught: 0
  ice_trap_appearance: # modifie l'apparence des pièges à glace en tant qu'éléments autonomes.
    major_only: 50
    junk_only: 0
    anything: 0
  logic_earliest_adult_trade: # premier élément pouvant apparaître dans la séquence d'échange pour adultes.
    pocket_egg: 0
    pocket_cucco: 0
    cojiro: 0
    odd_mushroom: 0
    poachers_saw: 0
    broken_sword: 0
    prescription: 50
    eyeball_frog: 0
    eyedrops: 0
    claim_check: 0
  logic_latest_adult_trade: # Dernier élément pouvant apparaître dans la séquence d'échange pour adultes.
    pocket_egg: 0
    pocket_cucco: 0
    cojiro: 0
    odd_mushroom: 0
    poachers_saw: 0
    broken_sword: 0
    prescription: 0
    eyeball_frog: 0
    eyedrops: 0
    claim_check: 50

```

## Rejoindre une partie MultiWorld

### Obtenez votre fichier de correctif OOT

Lorsque vous rejoignez un jeu multimonde, il vous sera demandé de fournir votre fichier YAML à l'hébergeur. Une fois que c'est Fini,
l'hébergeur vous fournira soit un lien pour télécharger votre fichier de données, soit un fichier zip contenant les données de chacun
des dossiers. Votre fichier de données doit avoir une extension `.apz5`.

Double-cliquez sur votre fichier `.apz5` pour démarrer votre client et démarrer le processus de patch ROM. Une fois le processus terminé
(cela peut prendre un certain temps), le client et l'émulateur seront lancés automatiquement (si vous avez associé l'extension
à l'émulateur comme recommandé).

### Connectez-vous au multiserveur

Une fois le client et l'émulateur démarrés, vous devez les connecter. Dans l'émulateur, cliquez sur "Outils"
menu et sélectionnez "Console Lua". Cliquez sur le bouton du dossier ou appuyez sur Ctrl+O pour ouvrir un script Lua.

Accédez à votre dossier d'installation Archipelago et ouvrez `data/lua/connector_oot.lua`.

Pour connecter le client au multiserveur, mettez simplement `<adresse>:<port>` dans le champ de texte en haut et appuyez sur Entrée (si le
le serveur utilise un mot de passe, saisissez dans le champ de texte inférieur `/connect <adresse>:<port> [mot de passe]`)

Vous êtes maintenant prêt à commencer votre aventure à Hyrule.
