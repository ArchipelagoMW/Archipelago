# Guide de configuration pour Ocarina of Time Archipelago

## Important

Comme nous utilisons BizHawk, ce guide s'applique uniquement aux systèmes Windows et Linux.

## Logiciel requis

- BizHawk : [Sorties BizHawk de TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
   - Les versions 2.3.1 et ultérieures sont prises en charge. La version 2.10 est recommandée pour des raisons de stabilité.
   - Des instructions d'installation détaillées pour BizHawk peuvent être trouvées sur le lien ci-dessus.
   - Les utilisateurs Windows doivent d'abord exécuter le programme d'installation des prérequis, qui peut également être trouvé sur le lien ci-dessus.
- Le client Archipelago intégré, qui peut être installé [ici](https://github.com/ArchipelagoMW/Archipelago/releases)
   (sélectionnez « Ocarina of Time Client » lors de l'installation).
- Un fichier ROM v1.0 US d'Ocarina of Time.

## Configuration de BizHawk

Une fois BizHawk installé, ouvrez EmuHawk et modifiez les paramètres suivants :

- (≤ 2,8) Allez dans Config > Personnaliser. Passez à l'onglet Avancé, puis faites passer le Lua Core de "NLua+KopiLua" à
   "Lua+LuaInterface". Puis redémarrez EmuHawk. Ceci est nécessaire pour que le script Lua fonctionne correctement.
   **REMARQUE : Même si « Lua+LuaInterface » est déjà sélectionné, basculez entre les deux options et resélectionnez-la. Nouvelles installations**
   **des versions plus récentes d'EmuHawk ont tendance à afficher "Lua+LuaInterface" comme option sélectionnée par défaut mais ce pendant refait l'épate juste au dessus par précautions**
- Sous Config > Personnaliser > Avancé, assurez-vous que la case AutoSaveRAM est cochée et cliquez sur le bouton 5s.
   Cela réduit la possibilité de perdre des données de sauvegarde en cas de crash de l'émulateur.
- Sous Config > Personnaliser, cochez les cases « Exécuter en arrière-plan » et « Accepter la saisie en arrière-plan ». Cela vous permettra continuez à jouer en arrière-plan, même si une autre fenêtre est sélectionnée.
- Sous Config > Hotkeys, de nombreux raccourcis clavier sont répertoriés, dont beaucoup sont liés aux touches communes du clavier. Vous voudrez probablement pour désactiver la plupart d'entre eux, ce que vous pouvez faire rapidement en utilisant « Esc ».
- Si vous jouez avec une manette, lorsque vous associez des commandes, désactivez "P1 A Up", "P1 A Down", "P1 A Left" et "P1 A Right".
   car ceux-ci interfèrent avec la visée s’ils sont liés. Définissez plutôt l'entrée directionnelle à l'aide de l'onglet Analogique.
- Sous N64, activez "Utiliser le connecteur d'extension". Ceci est nécessaire pour que les états de sauvegarde fonctionnent.
   (Le menu N64 n'apparaît qu'après le chargement d'une ROM.)

Il est fortement recommandé d'associer les extensions de rom N64 (\*.n64, \*.z64) à l'EmuHawk que nous venons d'installer.
Pour ce faire, vous devez simplement rechercher n'importe quelle rom N64 que vous possédez, faire un clic droit et sélectionner "Ouvrir avec...", déplier la liste qui apparaît et sélectionnez l'option du bas "Rechercher une autre application", puis accédez au dossier BizHawk et sélectionnez EmuHawk.exe.

Un guide de configuration BizHawk alternatif ainsi que divers conseils de dépannage sont disponibles
[ici](https://wiki.ootrandomizer.com/index.php?title=Bizhawk).

## Créer un fichier de configuration (.yaml)

### Qu'est-ce qu'un fichier de configuration et pourquoi en ai-je besoin ?

Consultez le guide sur la configuration d'un YAML de base lors de la configuration de l'archipel.
guide : [Guide de configuration de base de Multiworld](/tutorial/Archipelago/setup/en)

### Où puis-je obtenir un fichier de configuration (.yaml) ?

La page Paramètres du lecteur sur le site Web vous permet de configurer vos paramètres personnels et d'exporter un fichier de configuration depuis eux. Page des paramètres du joueur : [Page des paramètres du joueur d'Ocarina of Time](/games/Ocarina%20of%20Time/player-options)

### Vérification de votre fichier de configuration

Si vous souhaitez valider votre fichier de configuration pour vous assurer qu'il fonctionne, vous pouvez le faire sur la page YAML Validator. 
YAML page du validateur : [page de validation YAML](/mysterycheck)

## Rejoindre un jeu multimonde

### Obtenez votre fichier OOT modifié

Lorsque vous rejoignez un jeu multimonde, il vous sera demandé de fournir votre fichier YAML à celui qui l'héberge. Une fois cela fait, l'hébergeur vous fournira soit un lien pour télécharger votre fichier de données, soit un fichier zip contenant les données de chacun des dossiers. Votre fichier de données doit avoir une extension « .apz5 ».

Double-cliquez sur votre fichier « .apz5 » pour démarrer votre client et démarrer le processus de correctif ROM. Une fois le processus terminé (cela peut prendre un certain temps), le client et l'émulateur seront automatiquement démarrés (si vous avez associé l'extension à l'émulateur comme recommandé).

### Connectez-vous au multiserveur

Une fois le client et l'émulateur démarrés, vous devez les connecter. Accédez à votre dossier d'installation Archipelago, puis vers `data/lua`, et faites glisser et déposez le script `connector_oot.lua` sur la fenêtre principale d'EmuHawk. (Vous pourrez plutôt ouvrir depuis la console Lua manuellement, cliquez sur `Script` 〉 `Open Script` et accédez à `connector_oot.lua` avec le sélecteur de fichiers.)

Pour connecter le client au multiserveur, mettez simplement `<adresse>:<port>` dans le champ de texte en haut et appuyez sur Entrée (si le serveur utilise un mot de passe, tapez dans le champ de texte inférieur `/connect <adresse>:<port> [mot de passe]`)

Vous êtes maintenant prêt à commencer votre aventure dans Hyrule.
