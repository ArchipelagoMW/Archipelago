# Guide d'Installation de Inscryption Randomizer

## Logiciel Exigé

- [Inscryption](https://store.steampowered.com/app/1092790/Inscryption/)
- Pour une installation facile (recommandé):
  - [r2modman](https://inscryption.thunderstore.io/package/ebkr/r2modman/) OU [Thunderstore Mod Manager](https://www.overwolf.com/app/Thunderstore-Thunderstore_Mod_Manager)
- Pour une installation manuelle:
  - [BepInEx pack for Inscryption](https://inscryption.thunderstore.io/package/BepInEx/BepInExPack_Inscryption/)
  - [MonoMod Loader for Inscryption](https://inscryption.thunderstore.io/package/BepInEx/MonoMod_Loader_Inscryption/)
  - [Inscryption API](https://inscryption.thunderstore.io/package/API_dev/API/)
  - [ArchipelagoMod](https://inscryption.thunderstore.io/package/Ballin_Inc/ArchipelagoMod/)

## Installation
Avant de commencer le processus d'installation, voici ce que vous deviez savoir:
- Installez uniquement les mods mentionnés dans ce guide si vous souhaitez une expérience stable! Les autres mods n'ont PAS été testés avec ArchipelagoMod et peuvent provoquer des problèmes.
- ArchipelagoMod utilise son propre système de sauvegarde lorsque vous jouez, mais pour des raisons de sécurité, sauvegardez votre fichier de sauvegarde en accédant à votre répertoire d'installation Inscryption et copiez le fichier `SaveFile.gwsave` dans un autre dossier.
- Il est fortement recommandé d'utiliser un mod manager si vous souhaitez avoir un processus d'installation plus rapide et plus facile, mais si vous n'aimez pas installer de logiciels supplémentaires et que vous êtes à l'aise pour déplacer des fichiers, vous pouvez vous référer au guide de configuration manuelle.

### Installation facile (mod manager)
1. Téléchargez [r2modman](https://inscryption.thunderstore.io/package/ebkr/r2modman/) à l'aide du bouton `Manual Download`, puis installez-le à l'aide de l'exécutable contenu dans le zip téléchargé (vous pouvez également utiliser [Thunderstore Mod Manager](https://www.overwolf.com/app/Thunderstore-Thunderstore_Mod_Manager) qui fonctionne de la même manière, mais cela nécessite [Overwolf](https://www.overwolf.com/))
2. Ouvrez le mod manager et sélectionnez Inscryption dans l'écran de sélection de jeu.
3. Sélectionnez le profil par défaut ou créez-en un nouveau.
4. Ouvrez l'onglet `Online` à gauche, puis recherchez `ArchipelagoMod`.
5. Développez ArchipelagoMod et cliquez sur le bouton `Download` pour installer la dernière version disponible et toutes ses dépendances.
6. Cliquez sur `Start Modded` pour ouvrir le jeu avec les mods (une console devrait apparaître si tout a été fait correctement).

### Installation manuelle
1. Téléchargez les mods suivants en utilisant le bouton `Manual Download`:
   - [BepInEx pack for Inscryption](https://inscryption.thunderstore.io/package/BepInEx/BepInExPack_Inscryption/)
   - [ArchipelagoMod](https://inscryption.thunderstore.io/package/Ballin_Inc/ArchipelagoMod/)
2. Ouvrez votre dossier d'installation d'Inscryption. Sur Steam, vous pouvez le trouver facilement en faisant un clic droit sur le jeu et en cliquant sur `Gérer` > `Parcourir les fichiers locaux`.
3. Ouvrez le fichier zip du pack BepInEx, puis ouvrez le dossier `BepInExPack_Inscryption`.
4. Prenez tous les dossiers et fichiers situés dans le dossier `BepInExPack_Inscryption` et déposez-les dans votre dossier Inscryption.
5. Ouvrez le dossier `BepInEx` dans votre dossier Inscryption.
6. Ouvrez le fichier zip d'ArchipelagoMod.
7. Prenez et déposez le dossier `plugins` dans le dossier `BepInEx` pour fusionner avec le dossier `plugins` existant.
8. Ouvrez le jeu normalement pour jouer avec les mods (si BepInEx a été correctement installé, une console devrait apparaitre).

## Rejoindre un nouveau MultiWorld
1. Après avoir ouvert le jeu, vous devriez voir un nouveau menu pour parcourir et créer des fichiers de sauvegarde.
2. Cliquez sur le bouton `New Game`, puis écrivez un nom unique pour votre fichier de sauvegarde.
3. Sur l'écran suivant, saisissez les informations nécessaires pour vous connecter au serveur MultiWorld, puis appuyez sur le bouton `Connect`.
4. En cas de succès, l'état de connexion en haut à droite changera pour "Connected". Sinon, un message d'erreur rouge apparaîtra.
5. Après s'être connecté au server et avoir reçu les items, le menu du jeu apparaîtra.

## Poursuivre une session MultiWorld
1. Après avoir ouvert le jeu, vous devriez voir une liste de vos fichiers de sauvegarde et un bouton pour en ajouter un nouveau.
2. Choisissez le fichier de sauvegarde que vous souhaitez utiliser, puis cliquez sur son bouton `Play`.
3. Sur l'écran suivant, les champs de texte seront remplis avec les informations que vous avez écrites précédemment. Vous pouvez ajuster certains champs si nécessaire, puis appuyer sur le bouton `Connect`.
4. En cas de succès, l'état de connexion en haut à droite changera pour "Connected". Sinon, un message d'erreur rouge apparaîtra.
5. Après s'être connecté au server et avoir reçu les items, le menu du jeu apparaîtra.

## Dépannage
### Le jeu ouvre normalement sans nouveau menu.
Si le nouveau menu mentionné précédemment n'apparaît pas, c'est peut-être l'un des deux problèmes suivants:
 - Si aucune console n'apparait à l'ouverture du jeu, cela signifie que les mods ne se sont pas chargés correctement. Voici ce que vous pouvez essayer:
   - Si vous utilisez le mod manager, assurez-vous de l'ouvrir et d'appuyer sur `Start Modded`. Ouvrir le jeu normalement depuis Steam ne chargera aucun mod.
   - Vérifiez si le mod manager a correctement trouvé le répertoire du jeu. Dans le mod manager, cliquez sur `Settings` puis allez dans l'onglet `Locations`. Assurez-vous que le répertoire sous `Change Inscryption directory` est correct. Vous pouvez vérifier le répertoire correct si vous faites un clic droit sur le jeu Inscription sur Steam et cliquez sur `Gérer` > `Parcourir les fichiers locaux`. Si le répertoire est erroné, cliquez sur ce paramètre et modifiez le répertoire.
   - Si vous avez installé les mods manuellement, cela signifie généralement que BepInEx n'a pas été correctement installé. Assurez-vous de lire attentivement le guide d'installation.
   - S'il n'y a toujours pas de console lors de l'ouverture du jeu modifié, essayez de demander de l'aide sur [Archipelago Discord Server](https://discord.gg/8Z65BR2).
 - S'il y a une console, cela signifie que les mods ont été chargés, mais que ArchipelagoMod n'a pas été trouvé ou a eu des erreurs lors du chargement.
   - Regardez dans la console et assurez-vous que vous trouvez un message concernant le chargement d'ArchipelagoMod.
   - Si vous voyez du texte rouge, il y a eu une erreur. Signalez le problème dans [Archipelago Discord Server](https://discord.gg/8Z65BR2) ou dans notre [GitHub](https://github.com/DrBibop/Archipelago_Inscryption/issues).

### J'ai un autre problème.
Vous pouvez demander de l'aide sur [le serveur Discord d'Archipelago](https://discord.gg/8Z65BR2) ou, si vous pensez avoir trouvé un bug avec le mod, signalez-le dans notre [GitHub](https://github.com/DrBibop/Archipelago_Inscryption/issues).