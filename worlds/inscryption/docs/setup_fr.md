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
Avant de commencé le processus d'installation, voici ce que vous devriez savoir:
- Installé seulement les mods mentionnés dans ce guide si vous souhaité une installation facile et rapide! Aucun autre mod à été testé avec ArchipelagoMod et il pourrait provoquer des problèmes.
- ArchipelagoMod créera un fichier de sauvegarde séparé lorsque vous jouez, mais pour des raisons de sécurité, sauvegardez votre fichier de sauvegarde en accédant à votre répertoire d'installation Inscryption et copiez le fichier "SaveFile.gwsave" dans un autre dossier.
- Il est fortement recommandé d'utiliser un mod manager si vous souhaitez avoir un processus d'installation plus rapide et plus facile, mais si vous n'aimez pas installer de logiciels supplémentaires et que vous êtes à l'aise pour déplacer des fichiers, vous pouvez vous référer au guide de configuration manuelle.

### Installation facile (mod manager)
1. Téléchargez [r2modman](https://inscryption.thunderstore.io/package/ebkr/r2modman/) à l'aide du bouton "Manual Download", puis installez-le à l'aide de l'exécutable contenu dans le zip téléchargé (vous pouvez également utiliser [Thunderstore Mod Manager ](https://www.overwolf.com/app/Thunderstore-Thunderstore_Mod_Manager) qui est exactement le même, mais cela nécessite [Overwolf](https://www.overwolf.com/))
2. Ouvrez le mod manager et sélectionnez Inscryption dans l'écran de sélection de jeu.
3. Sélectionnez le profil par défaut ou créez-en un nouveau.
4. Ouvrez l'onglet "Online" à gauche, puis recherchez "ArchipelagoMod".
5. Développez ArchipelagoMod et cliquez sur le bouton "Download" pour installer la dernière version disponible et toutes ses dépendances.
6. Cliquez sur "Start Modded" pour ouvrir le jeu avec les mods (une console devrait apparaitre si tout a été fait correctement).

### Installation manuelle
1. Téléchargez les mods suivants en utilisant le bouton "Manual Download" :
   - [BepInEx pack for Inscryption](https://inscryption.thunderstore.io/package/BepInEx/BepInExPack_Inscryption/)
   - [ArchipelagoMod](https://inscryption.thunderstore.io/package/Ballin_Inc/ArchipelagoMod/)
2. Ouvrez votre répertoire d'installation d'enregistrement. Sur Steam, vous pouvez le trouver facilement en faisant un clic droit sur le jeu et en cliquant sur "Gérer" > "Parcourir les fichiers locaux".
3. Ouvrez le fichier zip du pack BepInEx, puis ouvrez le dossier "BepInExPack_Inscryption".
4. Prenez tous les dossiers et fichiers situés dans le dossier "BepInExPack_Inscryption" et déposez-les dans votre répertoire Inscryption.
5. Ouvrez le dossier "BepInEx" dans votre répertoire Inscryption.
6. Ouvrez le fichier zip d'ArchipelagoMod.
7. Prenez et déposez le dossier "plugins" dans le dossier "BepInEx" pour fusionner avec le dossier "plugins" existant.
8. Ouvrez le jeu normalement pour jouer avec les mods (si BepInEx a été correctement installé, une console devrait apparaitre).

## Rejoindre un nouveau MultiWorld
1. Assurez-vous d'avoir une nouvelle sauvegarde à chaque fois que vous démarrez un nouveau MultiWorld! Si ce n'est pas votre premier MultiWorld avec Inscryption, appuyez quatre fois sur le bouton "Réinitialiser les données de sauvegarde" dans les paramètres. Cela devrait vous ramener à la cinématique de départ.
2. Dans le menu principal du jeu, ouvrez le menu des paramètres.
3. Si tout a été installé correctement, vous devriez voir un quatrième onglet avec le logo d'Archipelago.
4. Ouvrez le quatrième onglet et remplissez les zones de texte avec les informations du serveur MultiWorld (si le serveur est hébergé sur le site Web, laissez le nom d'hôte comme "archipelago.gg").
5. Cliquez sur le bouton "connect". En cas de succès, le statut en haut à droite devrait écrire "connected". Sinon, un message d'erreur rouge devrait apparaître.
6. Revenez au menu principal et démarrez le jeu.

## Poursuivre une session MultiWorld
Sauf si le nom d'hôte ou le port a changé, vous n'avez pas besoin de revenir aux paramètres lorsque vous rouvrez le jeu. La sélection de l'option "Continuer" devrait automatiquement vous connecter au serveur. Tout ce que vous écrivez dans les paramètres est enregistré pour toutes les sessions futures.

## Dépannage
### Il n'y a pas de quatrième onglet dans les paramètres.
S'il n'y a pas de quatrième onglet, c'est peut être l'un des deux problèmes suivants:
 - Si aucune console n'apparait pas à l'ouverture du jeu, cela signifie que les mods ne se sont pas chargés correctement. Voici ce que vous pouvez essayer:
   - Si vous utilisez le mod manager, assurez-vous de l'ouvrir et d'appuyer sur "Start Modded". Ouvrir le jeu normalement depuis Steam ne chargera aucun mod.
   - Vérifiez si le mod manager a correctement trouvé le chemin du jeu. Dans le mod manager, cliquez sur "Settings" puis allez dans l'onglet "Locations". Assurez-vous que le chemin répertorié sous "Change Inscryption directory" est correct. Vous pouvez vérifier le chemin correct si vous faites un clic droit sur le jeu Inscription sur Steam et cliquez sur "Gérer" > "Parcourir les fichiers locaux". Si le chemin est erroné, cliquez sur ce paramètre et modifiez le chemin.
   - Si vous avez installé les mods manuellement, cela signifie généralement que BepInEx n'a pas été correctement installé. Assurez-vous de lire attentivement le guide d'installation.
   - S'il n'y a toujours pas de console lors de l'ouverture du jeu modifié, essayez de demander de l'aide sur [Archipelago Discord Server](https://discord.gg/8Z65BR2).
 - S'il y a une console, cela signifie que les mods ont été chargés mais que ArchipelagoMod n'a pas été trouvé ou a eu des erreurs lors du chargement.
   - Regardez dans la console et assurez-vous que vous trouver un message concernant le chargement d'ArchipelagoMod.
   - Si vous voyez du texte rouge, il y a eu une erreur. Signalez le problème dans [Archipelago Discord Server](https://discord.gg/8Z65BR2) ou créez un issue dans notre [GitHub](https://github.com/DrBibop/Archipelago_Inscryption/issues).

### J'ai un autre problème.
Vous pouvez demander de l'aide sur [le serveur Discord d'Archipelago](https://discord.gg/8Z65BR2) ou, si vous pensez avoir trouvé un problème avec le mod, créez un issue dans notre [GitHub](https://github.com/DrBibop/Archipelago_Inscryption/issues).