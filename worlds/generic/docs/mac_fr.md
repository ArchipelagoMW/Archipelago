#Guide pour exécuter Archipelago à partir du code source sur macOS
Archipelago n'a pas de version compilée sur macOS. Cependant, il est possible de l'exécuter à partir du code source sur macOS. Ce guide suppose que vous avez une certaine expérience de l'exécution de logiciels à partir du terminal.
## Les logiciels prérequis
Voici une liste des logiciels à installer et du code source à télécharger.
1. Python 3.9 "universal2" ou plus récent à partir de la [page de téléchargement Python pour macOS] (https://www.python.org/downloads/macos/).
   **Python 3.11 n'est pas encore supporté**.
2. Xcode depuis le [macOS App Store](https://apps.apple.com/us/app/xcode/id497799835).
3. Le code source à partir de la [page des versions d'Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).
4. Le contenu ayant darwin dans le nom à partir de la [SNI Github releases page](https://github.com/alttpo/sni/releases).
5. Si vous souhaitez générer des graines enémisées pour ALTTP localement (pas sur le site web), vous pouvez avoir besoin de l'EnemizerCLI à partir de sa [page de publication Github](https://github.com/Ijwu/Enemizer/releases).
6. Un émulateur de votre choix pour les jeux qui nécessitent un émulateur. Pour les jeux SNES, je recommande RetroArch, entièrement parce qu'il a été le plus facile à installer sur macOS. Il peut être téléchargé sur la [page de téléchargement de RetroArch](https://www.retroarch.com/?page=platforms)
## Extraction du répertoire Archipelago
1. Double-cliquer sur le fichier zip du code source d'Archipelago pour extraire les fichiers dans un répertoire Archipelago.
2. Déplacez ce répertoire Archipelago hors de votre répertoire de téléchargements.
3. Ouvrir le terminal et naviguer jusqu'au répertoire Archipelago.
## Mise en place d'un environnement virtuel
Il est généralement recommandé d'utiliser un environnement virtuel pour exécuter des logiciels basés sur Python afin d'éviter la contamination qui peut endommager certains logiciels. Si Archipelago est le seul logiciel que vous utilisez et qui s'exécute à partir du code source python, il n'est pas nécessaire d'utiliser un environnement virtuel. 
1. Ouvrir le terminal et naviguer jusqu'au répertoire Archipelago. Il est également possible de faire un clic droit sur le dossier Archipelago dans le Finder et de sélectionner "New Terminal at Folder" (Nouveau terminal dans le dossier).
2. Exécutez la commande `python3 -m venv venv` pour créer un environnement virtuel. L'exécution de cette commande créera un nouveau répertoire au chemin spécifié, assurez-vous donc que ce chemin est clair pour qu'un nouveau répertoire soit créé.
3. Exécutez la commande `source venv/bin/activate` pour activer l'environnement virtuel.
4. Si vous souhaitez quitter l'environnement virtuel, exécutez la commande `deactivate`.
## Etapes d'exécution des clients 
1. Si votre jeu n'a pas de fichier patch, lancez la commande `python3 SNIClient.py`, en changeant le nom du fichier par celui du client que vous voulez lancer.
2. Si votre jeu a un fichier patch, déplacez la rom de base dans le répertoire Archipelago et lancez la commande `python3 SNIClient.py 'patchfile'` avec l'extension du fichier patch (apsm, aplttp, apsmz3, etc.) incluse et en changeant le nom du fichier par le fichier du client que vous voulez lancer.
3. Votre client devrait maintenant fonctionner et la ROM devrait être créée (le cas échéant).
## Etapes supplémentaires pour les jeux SNES
1. Si vous utilisez RetroArch, les instructions pour configurer votre émulateur [ici dans le guide de configuration de Link to the Past] (https://archipelago.gg/tutorial/A%20Link%20to%20the%20Past/multiworld/fr) fonctionnent également sur la version macOS de RetroArch.
2. Double-cliquez sur le téléchargement SNI tar.gz pour extraire les fichiers dans un répertoire SNI. Si ce n'est pas déjà fait, renommez ce répertoire en SNI pour faciliter certaines étapes.
3. Déplacer le répertoire SNI hors du répertoire des téléchargements, de préférence dans le répertoire Archipelago créé plus tôt.
4. Si le répertoire SNI est correctement nommé et déplacé dans le répertoire Archipel, il devrait s'exécuter automatiquement avec le client SNI. Si ce n'est pas le cas, ouvrez le répertoire SNI et exécutez manuellement le fichier exécutable SNI.
5. Si vous utilisez EnemizerCLI, extrayez le répertoire téléchargé et renommez-le en EnemizerCLI.
6. Déplacer le répertoire EnemizerCLI dans le répertoire Archipelago pour que Generate.py puisse en profiter. 
7. Maintenant pour SNI, le client et l'émulateur, vous êtes prêt à commencer.
