# Guide de mise en place de l'Archipelago de The Wind Waker

Bienvenue dans l'Archipelago The Wind Waker ! 
Ce guide vous aidera à mettre en place le randomiser et à jouer à votre premier multiworld.
Si vous jouez à The Wind Waker, vous devez suivre quelques étapes simple pour commencer.

## Requis

Vous aurez besoin des choses suivantes pour être capable de jouer à The Wind Waker:
*  L'[émulateur Dolphin](https://dolphin-emu.org/download/). **Nous recommendons d'utiliser la dernière version
  sortie.**
    * Les utilisateurs Linux peuvent utiliser le paquet flatpak
    [disponible sur Flathub](https://flathub.org/apps/org.DolphinEmu.dolphin-emu).
* La dernière version du [Randomiser The Wind Waker pour
  Archipelago](https://github.com/tanjo3/wwrando/releases?q=tag%3Aap_2).
    * Veuillez noter que cette version est **différente** de celui utilisé pour le randomiser standard. Cette version
      est spécifique à Archipelago.
* Une ISO du jeu Zelda The Wind Waker (version Nord Américaine), probablement nommé "Legend of Zelda, The - The Wind
  Waker (USA).iso".

De manière optionnelle, vous pouvez également télécharger:
* Le [tracker pour Wind Waker](https://github.com/Mysteryem/ww-poptracker/releases/latest) avec
  [PopTracker](https://github.com/black-sliver/PopTracker/releases), qui en est la dépendance.
* Des [modèles de personnages personnalisés pour Wind
  Waker](https://github.com/Sage-of-Mirrors/Custom-Wind-Waker-Player-Models) afin de personnaliser votre personnage en
  jeu.


## Mise en place d'un YAML

Tous les joueurs jouant à The Wind Waker doivent donner un YAML comportant les paramètres de leur monde
à l'hôte de la salle.
Vous pouvez aller sur la [page d'options The Wind Waker](/games/The%20Wind%20Waker/player-options)
pour générer un YAML avec vos options désirés. 
Seulement les localisations catégorisées sous les options activés
sous "Progression Locations" seront randomisés dans votre monde.
Une fois que vous êtes heureux avec vos paramètres, 
donnez votre fichier YAML à l'hôte de la salle et procéder à la prochaine étape.

## Connexion à une salle

L'hôte du multiworld vous donnera un lien pour télécharger votre fichier APTWW
ou un zip contenant les fichiers de tout le monde.
Le fichier APTWW doit être nommé `P#_<nom>_XXXXX.aptww`, où `#` est l'identifiant du joueur,
`<nom>` est votre nom de joueur, et `XXXXX` est l'identifiant de la salle.
L'hôte doit également vous donner le nom de la salle du serveur avec le numéro de port.

Une fois que vous êtes prêt, suivez ces étapes pour vous connecter à la salle:
1. Lancer le build AP du Randomiser. Si c'est la première fois que vous ouvrez le randomiser,
   vous aurez besoin d'indiquer le chemin vers votre ISO de The Wind Waker et le dossier de sortie pour l'ISO randomisé.
   Ceux-ci seront sauvegardé pour la prochaine fois que vous ouvrez le programme.
2. Modifier n'importe quel cosmétique comme vous le voulez avec les ajustements désirés 
   ainsi que la personnalisation de votre personnage desiré.
3. Pour le fichier APTWW, naviguer et localiser le chemin du fichier.
4. Appuyer sur `Randomize` en bas à droite. 
   Cela va randomiser et mettre l'ISO dans le dossier de sortie que vous avez renseigné.
   Le fichier sera nommé `TWW AP_YYYYY_P# (<nom>).iso`, où `YYYYY` est le numéro de votre seed,
   `#` est l'identifiant de votre joueur, et `<nom>` est le nom de votre joueur (nom de slot). 
   Veuillez vérifier que ces valeurs sont correctes pour votre multiworld.
5. Ouvrez Dolphin et utilisez le pour ouvrir l'iso randomisé.
6. Lancer `ArchipelagoLauncher.exe` (sans le `.exe` sur Linux) et choisissez `The Wind Waker Client`,
   Cela va lancer le client texte.
7. Si Dolphin n'est pas encore ouvert, ou que vous n'avez pas encore commencé de nouveau fichier,
   vous serez demandé à le faire.
    * Une fois que vous avez ouvert votre ISO dans Dolphin, le client doit dire "Dolphin connected successfully.".
8. Connectez-vous à la salle entrant le nom du serveur et son numéro de port en haut et cliquer sur `Connect`.
   Pour ceux qui hébergent sur le site web, cela sera `archipelago.gg:<port>`, où `<port>` est le numéro de port.
   Si un jeu est hébergé à partir de `ArchipelagoServer.exe` (sans le `.exe` sur Linux),
   le numéro de port par défaut est `38281` mais il peut être changé dans le `host.yaml`.
9. Si tu as ouvert ton ISO correspondant au multiworld auquel tu es connecté,
   ça doit authentifier ton nom de slot automatiquement quand tu commences une nouveau fichier de sauvegarde.

## Résolutions de problèmes
* Vérifier que vous utilisez la même version d'Archipelago que celui qui a généré le multiworld.
* Vérifier que `tww.apworld` n'est pas dans votre dossier d'installation Archipelago dans le dossier `custom_worlds`.
* Vérifier que vous utiliser la bonne version du build du randomiser que vous utilisez pour la version d'Archipelago.
  * Le build doit donner un message d'erreur vous dirigeant vers la bonne version. 
    Vous pouvez aussi consulter les notes de version des builds AP de TWW
    [ici](https://github.com/tanjo3/wwrando/releases?q=tag%3Aap_2),
    afin de voir avec quelles versions d'Archipelago chaque build est compatible avec.
* Ne pas lancer le Launcher d'Archipelago ou Dolphin en tant qu'Administrateur sur Windows.
* Si vous rencontrez des problèmes avec l'authentification, 
  vérifier que la ROM randomisé est ouverte dans Dolphin et correspond au multiworld auquel vous vous connectez.
* Vérifier que vous n'utilisez aucune triche Dolphin ou que des codes de triches sont activés. 
  Certains codes peut interférer de manière imprévue avec l'émulation et 
  rendre la résolution des problèmes compliquées.
* Vérifier que `Modifier la taille de la mémoire émulée` dans Dolphin 
  (situé sous `Options` > `Configuration` > `Avancé`) est **désactivé**.
* Si le client ne peut pas se connecter à Dolphin, Vérifier que Dolphin est situé sur le même disque qu'Archipelago.
  D'après certaines informations, avoir Dolphin sur un disque dur externe cause des problèmes de connexion.
* Vérifier que la `Région de remplacement` dans Dolphin (situé sous `Options` > `Configuration` > `Général`)
  est mise à `NTSC-U`.
* Si vous lancez un menu de démarrage de Gamecube personnalisé,
  vous aurez besoin de le passer en allant dans `Options` > `Configuration` > `GameCube`
  et cocher `Passer le Menu Principal`.
