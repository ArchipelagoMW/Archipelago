# # Guide de configuration MultiWorld de DLCQuest

## Logiciels requis

- DLC Quest sur PC (Recommandé: [Version Steam](https://store.steampowered.com/app/230050/DLC_Quest/))
- [DLCQuestipelago](https://github.com/agilbert1412/DLCQuestipelago/releases)
- BepinEx (utilisé comme un modloader pour DLCQuest. La version du mod ci-dessus inclut BepInEx si vous choisissez la version d'installation complète)

## Logiciels optionnels
- [Archipelago] (https://github.com/ArchipelagoMW/Archipelago/releases)
    - (Uniquement pour le TextClient)

## Créer un fichier de configuration (.yaml)

### Qu'est-ce qu'un fichier YAML et pourquoi en ai-je besoin ?

Voir le guide d'Archipelago sur la mise en place d'un YAML de base : [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Où puis-je obtenir un fichier YAML ?

Vous pouvez personnaliser vos paramètres en visitant la [page des paramètres du joueur DLC Quest](/games/DLCQuest/player-options).

## Rejoindre une partie multi-monde

### Installer le mod

- Télécharger le [DLCQuestipelago mod release](https://github.com/agilbert1412/DLCQuestipelago/releases). Si c'est la première fois que vous installez le mod, ou si vous n'êtes pas à l'aise avec l'édition manuelle de fichiers, vous devriez choisir l'Installateur. Il se chargera de la plus grande partie du travail pour vous


- Extraire l'archive .zip à l'emplacement de votre choix


- Exécutez "DLCQuestipelagoInstaller.exe".

![image](https://i.imgur.com/2sPhMgs.png)
- Le programme d'installation devrait décrire ce qu'il fait à chaque étape, et vous demandera votre avis si nécessaire.
  - Il vous permettra de choisir l'emplacement d'installation de votre jeu moddé et vous proposera un emplacement par défaut
  - Il **essayera** de trouver votre jeu DLCQuest sur votre ordinateur et, en cas d'échec, vous demandera d'indiquer le chemin d'accès.
  - Il vous offrira la possibilité de créer un raccourci sur le bureau pour le lanceur moddé.

### Se connecter au MultiServer

- Localisez le fichier "ArchipelagoConnectionInfo.json", qui se situe dans le même emplacement que votre installation moddée. Vous pouvez éditer ce fichier avec n'importe quel éditeur de texte, et vous devez entrer l'adresse IP du serveur, le port et votre nom de joueur dans les champs appropriés.

- Exécutez BepInEx.NET.Framework.Launcher.exe. Si vous avez opté pour un raccourci sur le bureau, vous le trouverez avec une icône et un nom plus reconnaissable.
![image](https://i.imgur.com/ZUiFrhf.png)

- Votre jeu devrait se lancer en même temps qu'une console de modloader, qui contiendra des informations de débogage importantes si vous rencontrez des problèmes.
- Le jeu devrait se connecter automatiquement, et tenter de se reconnecter si votre internet ou le serveur se déconnecte, pendant que vous jouez.

### Interagir avec le MultiWorld depuis le jeu

Vous ne pouvez pas envoyer de commandes au serveur ou discuter avec les autres joueurs depuis DLC Quest, car le jeu ne dispose pas d'un moyen approprié pour saisir du texte.
Vous pouvez suivre l'activité du serveur dans votre console BepInEx, car les messages de chat d'Archipelago y seront affichés.
Vous devrez utiliser [Archipelago Text Client] (https://github.com/ArchipelagoMW/Archipelago/releases) si vous voulez envoyer des commandes.
