# Guide d'Installation du MultiWorld Choo-Choo Charles
Cette page est un guide simplifié de la [page du Mod Randomiseur Multiworld de Choo-Choo Charles](https://github.com/lgbarrere/CCCharles-Random?tab=readme-ov-file#cccharles-random).

## Exigences et Logiciels Nécessaires
* Un ordinateur utilisant Windows (le Mod n'est pas utilisable sous Linux ou Mac)
* [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
* Une copie légale du jeu original Choo-Choo Charles (peut être trouvé sur [Steam](https://store.steampowered.com/app/1766740/ChooChoo_Charles/)

## Installation du Mod pour jouer
### Téléchargement du Mod
Tous les fichiers nécessaires du Mod se trouvent dans les [Releases](https://github.com/lgbarrere/CCCharles-Random/releases).
Pour utiliser le Mod, télécharger et désarchiver **CCCharles_Random.zip** à un endroit sûr, puis suivre les instructions dans les sections suivantes de ce guide. Cette archive contient :
* Le dossier **Obscure/** qui charge le Mod lui-même, il lance le code qui gère tous les éléments randomisés
* Le fichier **cccharles.apworld** qui contient la logique de randomisation, utilisé par l'hôte pour générer une graine aléatoire avec les autres jeux

### Préparation du Jeu
Le Mod peut être installé et joué en suivant les étapes suivantes (voir la section [Téléchargement du Mod](setup_fr#téléchargement-du-mod) pour récupérer **CCCharles_Random.zip**) :
1. Copier le dossier **Obscure/** de **CCCharles_Random.zip** vers **\<GameFolder\>** (où se situent le dossier **Obscure/** et **Obscure.exe**)
2. Lancer le jeu, si "OFFLINE" est visible dans le coin en haut à droite de l'écran, le Mod est actif

### Créer un Fichier de Configuration (.yaml)
L'objectif d'un fichier YAML est décrit dans le [Guide d'Installation Basique du Multiworld](https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-game) (en anglais).

La [page d'Options Joueur](/games/Choo-Choo%20Charles/player-options) permet de configurer des options personnelles et exporter un fichier de configuration YAML.

## Rejoindre une Partie MultiWorld
Avant de jouer, il est fortement recommandé de consulter la section **[Problèmes Connus](setup_fr#probl%C3%A8mes-connus)**.
* La console du jeu doit être ouverte pour taper des commandes Archipelago, appuyer sur la touche "F10" ou "`" (ou "~") en querty (touche "²" en azerty)
* Taper ``/connect <IP> <NomDuJoueur>`` avec \<IP\> et \<NomDuJoueur\> trouvés sur la page web d'hébergement Archipelago sous la forme ``archipelago.gg:XXXXX`` et ``CCCharles``
* La déconnexion est automatique à la fermeture du jeu mais peut être faite manuellement avec ``/disconnect``

## Héberger une partie MultiWorld ou un Seul Joueur
Voir la section [Téléchargement du Mod](setup_fr#téléchargement-du-mod) pour récupérer le fichier **cccharles.apworld**.

Dans cette section, **Archipelago/** fait référence au chemin d'accès où [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) est installé localement.

Suivre ces étapes pour héberger une session multijoueur à distance ou locale pour un seul joueur :
1. Double-cliquer sur **cccharles.apworld** pour installer automatiquement la logique de randomisation du monde
2. Placer le **CCCharles.yaml** dans **Archipelago/Players/** avec le YAML de chaque joueur à héberger
3. Exécuter le lanceur Archipelago et cliquer sur "Generate" pour configurer une partie avec les YAML dans **Archipelago/output/**
4. Pour une session multijoueur, aller à la [page Archipelago HOST GAME](https://archipelago.gg/uploads)
5. Cliquer sur "Upload File" et selectionner le **AP_\<seed\>.zip** généré dans **Archipelago/output/**
6. Envoyer la page de la partie générée à chaque joueur

Pour une session locale à un seul joueur, cliquer sur "Host" dans le lanceur Archipelago en utilisant **AP_\<seed\>.zip** généré dans **Archipelago/output/**

## Problèmes Connus
### Problèmes majeurs
Aucun problème majeur trouvé.

### Problèmes mineurs
* La version actuelle de l'analyseur de commandes n'accepte pas des commandes de la console dont le nom du joueur contient des espaces. Il est recommandé d'utiliser des soulignés "_" à la place, par exemple : CCCharles_Player_1.
