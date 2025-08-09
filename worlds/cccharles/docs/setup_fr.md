# Guide d'Installation du MultiWorld Choo-Choo Charles
Cette page est un guide simplifié de la [page du Mod Randomiseur Multiworld de Choo-Choo Charles](https://github.com/lgbarrere/CCCharles-Random?tab=readme-ov-file#cccharles-random).

## Exigences et Logiciels Nécessaires
* Un ordinateur utilisant Windows (le Mod n'est pas utilisable sous Linux ou Mac)
* [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
* Une copie légale du jeu original Choo-Choo Charles (peut être trouvé sur [Steam](https://store.steampowered.com/app/1766740/ChooChoo_Charles/)

## Installation du Mod pour jouer
Pour installer le Mod, ouvrir la [page du Mod Randomiseur Multiworld de Choo-Choo Charles](https://github.com/lgbarrere/CCCharles-Random) et suivre les étapes ci-dessous.

### Préparation du Jeu
Les sorties de ce jeu ne sont actuellement pas officielles. Cependant, le Mod peut être installé et joué en suivant ces instructions :
1. Cliquer sur le bouton vert "<> Code"
2. Cliquer "Download ZIP" et désarchiver l'archive téléchargée ou cloner ce projet
3. Depuis ce dossier, dans **Release/**, copier le dossier **Obscure/** dans **\<DossierDuJeu\>** (où se situent le dossier **Obscure/** et **Obscure.exe**)
4. Lancer le jeu, si "OFFLINE" est marqué dans le coin en haut à droite de l'écran, le Mod est actif

Le contenu du dossier **Release/** peut être placé manuellement tant que les chemins des fichiers sont respectés.

### Créer un Fichier de Configuration (.yaml)
L'objectif d'un fichier YAML est décrit dans le [Guide d'Installation Basique du Multiworld](https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-game) (en anglais).

La [page d'Options Joueur](/games/Choo-Choo%20Charles/player-options) permet de configurer des options personnelles et exporter un fichier de configuration YAML.

## Rejoindre une Partie MultiWorld
Avant de jouer, il est fortement recommandé de consulter la section **[Problèmes Connus](setup_fr#probl%C3%A8mes-connus)**.
* La console du jeu doit être ouverte pour taper des commandes Archipelago, appuyer sur la touche "F10" ou "`" (ou "~") en querty (touche "²" en azerty)
* Taper ``/connect <IP> <NomDuJoueur>`` avec \<IP\> et \<NomDuJoueur\> trouvés sur la page web d'hébergement Archipelago sous la forme ``archipelago.gg:XXXXX`` et ``CCCharles``
* La déconnexion est automatique à la fermeture du jeu mais peut être faite manuellement avec ``/disconnect``

## Héberger une partie MultiWorld ou un Seul Joueur
Voir la section **[Préparation du Jeu](setup_fr#pr%C3%A9paration-du-jeu)** pour télécharger le dossier **Release/**.

Dans cette section, **Archipelago/** fait référence au chemin d'accès où [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) est installé localement.

Suivre ces étapes pour héberger une session multijoueur à distance ou locale pour un seul joueur :
1. Double-cliquer sur **cccharles.apworld** dans **Release/** pour installer automatiquement la logique de randomisation du monde
2. Copier **CCCharles.yaml** depuis **Release/** vers **Archipelago/Players/** avec le YAML de chaque joueur à héberger
3. Exécuter le lanceur Archipelago et cliquer sur "Generate" pour configurer une partie avec le YAML dans **Archipelago/output/**
4. Pour une session multijoueur, aller à la [page Archipelago HOST GAME](https://archipelago.gg/uploads)
5. Cliquer sur "Upload File" et selectionner le **AP_\<seed\>.zip** généré dans **Archipelago/output/**
6. Envoyer la page de la partie générée à chaque joueur

Pour une session locale à un seul joueur, cliquer sur "Host" dans le lanceur Archipelago en utilisant **AP_\<seed\>.zip** généré dans **Archipelago/output/**

## Problèmes Connus
### Problèmes majeurs
* Si le joueur reçoit la **Box of Rockets**, le bunker de la région **Training Explosive** sera ouvert une fois la zone chargée. Il peut être possible de casser l'état de la mission si le joueur interagit avec des éléments dans un ordre inattendu.

### Problèmes mineurs
* La version actuelle de l'analyseur de commandes n'accepte pas des commandes de la console dont le nom du joueur contient des espaces. Il est recommandé d'utiliser des soulignés "_" à la place, par exemple : CCCharles_Player_1.
* Parfois, la réception d'un objet ou l'envoie d'un emplacement peut échouer (cas rares). Recharger le jeu est supposé faire réapparaître tous les objets au sol et relancer une nouvelle partie récupère tous les objets débloqués sur Archipelago, ceci peut être utilisé comme solution de contournement.
* Quand un oeuf est reçu, si le joueur va vers l'une des trois sorties de mines avant de parler au PNJ qui en donne la clef d'entrée, le joueur ne sera plus capable d'interagir avec le PNJ. Il faut s'assurer de leur parler avant de s'approcher de leur mine respective. Recommencer une nouvelle partie si cela se produit.
