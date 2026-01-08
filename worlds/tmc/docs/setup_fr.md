# The Minish Cap Setup Guide

## Logiciel requis

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- Une copie EU de The Legend of Zelda : The Minish Cap. La communauté Archipelago ne peut pas fournir ce logiciel.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 ou plus récent

## Logiciel en option

- [TMC AP Tracker par Deoxis](https://github.com/deoxis9001/tmcrando_maptracker_deoxis/releases/latest), à utiliser avec
[PopTracker](https://github.com/black-sliver/PopTracker/releases)

### Configuration de BizHawk

Une fois que vous avez installé BizHawk, ouvrez `EmuHawk.exe` et modifiez les paramètres suivants :

- Si vous utilisez BizHawk 2.7 ou 2.8, allez dans `Config > Customize`. Dans l'onglet Avancé, changez le noyau Lua de
`NLua+KopiLua` à `Lua+LuaInterface`, puis redémarrez EmuHawk. (Si vous utilisez BizHawk 2.9, vous pouvez sauter cette étape).
- Sous `Config > Customize`, cochez l'option « Run in background » pour éviter de vous déconnecter du client pendant que vous êtes en train de quitter EmuHawk.
lorsque vous êtes déconnecté d'EmuHawk.
- Ouvrez un fichier `.gba` dans EmuHawk et allez dans `Config > Controllers...` pour configurer vos entrées. Si vous ne pouvez pas cliquer sur
`Contrôleurs...`, chargez d'abord n'importe quel ROM `.gba`.
- Pensez à effacer les raccourcis clavier dans `Config > Hotkeys...` si vous n'avez pas l'intention de les utiliser. Sélectionnez le raccourci clavier et appuyez sur Esc pour l'effacer.

## Installing the apworld

Comment utiliser un fichier .apworld : 
Placez le fichier .apworld dans votre dossier Archipelago/custom_worlds, ou 
double-cliquez sur le fichier .apworld pour le faire automatiquement.
Utilisez ArchipelagoLauncher.exe pour ouvrir le lanceur, puis cliquez sur 
`Generate Template Options` pour créer des fichiers yamls pour
vos fichiers .apworld personnalisés.
Placez les fichiers yaml des joueurs souhaités dans le dossier Players et
personnalisez-les comme bon vous semble.
Utilisez ArchipelagoGenerate.exe pour générer le jeu.
Téléchargez le jeu généré (dans le dossier de `output`) sur le site Web à l'adresse
https://archipelago.gg/uploads et créez une nouvelle salle.
Pour plus d'informations, consultez le guide de configuration de chaque jeu 
(généralement disponible dans les épingles de la rubrique « future-game-design » du jeu ou sur GitHub).
Les fichiers de correctifs se trouvent dans le fichier compressé de
votre dossier de `output` plutôt que surla page de la salle.

## Générer et patcher un jeu

1. Créez votre fichier d'options (YAML). Vous pouvez en télécharger un depuis la page GitHub Releases ou créer le fichier YAML par défaut à partir de votre Launcher avec l'option « Generate Template Options ».
2. Suivez les instructions générales d'Archipelago pour [générer un jeu] (../../Archipelago/setup/en#generating-a-game).
Cela générera un fichier de sortie pour vous. Votre fichier patch aura l'extension `.aptmc`.
3. Ouvrez `ArchipelagoLauncher.exe`
4. Sélectionnez « Open Patch » sur le côté gauche et sélectionnez votre fichier patch.
5. S'il s'agit de votre premier patch, vous serez invité à localiser votre ROM vanilla.
6. Un fichier `.gba` patché sera créé au même endroit que le fichier patch.
7. Lors de votre première ouverture d'un patch avec BizHawk Client, il vous sera également demandé de localiser `EmuHawk.exe` dans votre installation BizHawk.
BizHawk.

Si vous jouez à un jeu solo et que vous ne vous souciez pas de l'autotracking ou des indices, vous pouvez vous arrêter ici, fermer le client et charger la ROM patchée dans n'importe quel émulateur.
et charger le patch de la ROM dans n'importe quel émulateur. Cependant, pour les mondes à plusieurs et les autres fonctions d'Archipelago, continuez ci-dessous en utilisant BizHawk comme émulateur.

## Connexion à un serveur

Par défaut, l'ouverture d'un fichier patch exécutera automatiquement les étapes 1 à 5 ci-dessous. Néanmoins, gardez-les en mémoire au cas où vous devriez fermer et rouvrir une fenêtre en cours de jeu pour une raison ou une autre.

1. The Minish Cap utilise le client BizHawk d'Archipelago. Si le client n'est pas encore ouvert depuis que vous avez patché votre jeu,
vous pouvez le rouvrir à partir du lanceur.
2. Assurez-vous qu'EmuHawk utilise la ROM patchée.
3. Dans EmuHawk, allez dans `Tools > Lua Console`. Cette fenêtre doit rester ouverte pendant le jeu.
4. Dans la fenêtre Lua Console, allez dans `Script > Open Script...`.
5. Naviguez jusqu'à votre dossier d'installation Archipelago et ouvrez `data/lua/connector_bizhawk_generic.lua`.
6. L'émulateur et le client finiront par se connecter l'un à l'autre. La fenêtre du client BizHawk devrait indiquer qu'il s'est connecté et qu'il a reconnu The Minish Cap.
s'est connecté et a reconnu The Minish Cap.
7. Pour connecter le client au serveur, entrez l'adresse et le port de votre salle (par exemple `archipelago.gg:38281`) dans le champ de texte supérieur du client et cliquez sur Connecter

Vous devriez maintenant être en mesure de recevoir et d'envoyer des éléments. Vous devrez suivre ces étapes chaque fois que vous voudrez vous reconnecter. Il n'y a aucun risque à progresser hors ligne.
Il est parfaitement sûr de progresser hors ligne ; tout sera resynchronisé lorsque vous vous reconnecterez.

## Suivi automatique

Le Minish Cap dispose d'un tracker de carte entièrement fonctionnel qui prend en charge l'auto-tracking

1. Téléchargez [The Minish Cap AP Tracker](https://github.com/deoxis9001/tmcrando_maptracker_deoxis/releases/latest) et
[PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Placez le pack du tracker dans packs/ dans votre installation de PopTracker.
3. Ouvrez PopTracker et chargez le pack Minish Cap Randomizer Map Tracker. Si vous utilisez le Map Tracker, assurez-vous de sélectionner la variante **AP**.
4. Pour l'autotracking, cliquez sur le symbole « AP » en haut.
5. Saisissez l'adresse du serveur Archipelago (celui auquel vous avez connecté votre client), le nom du slot et le mot de passe.
