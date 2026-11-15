# Guide de configuration MultiWorld d'Aquaria

## Logiciels nécessaires

- Une copie du jeu Aquaria non modifiée (disponible sur la majorité des sites de ventes de jeux vidéos en ligne)
- Le client du Randomizer d'Aquaria [Aquaria randomizer](https://github.com/tioui/Aquaria_Randomizer/releases/latest)

## Logiciels optionnels

- De manière optionnelle, pour pouvoir envoyer des [commandes](/tutorial/Archipelago/commands/en) comme `!hint`: utilisez le client texte de [la version la plus récente d'Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
- [Aquaria AP Tracker](https://github.com/palex00/aquaria-ap-tracker/releases/latest), pour utiliser avec [PopTracker](https://github.com/black-sliver/PopTracker/releases/latest)

## Procédures d'installation et d'exécution

### Windows

En premier lieu, vous devriez effectuer une nouvelle copie du jeu d'Aquaria original à chaque fois que vous effectuez une
nouvelle partie. La première raison de cette copie est que le randomizer modifie des fichiers qui rendront possiblement
le jeu original non fonctionnel. La seconde raison d'effectuer cette copie est que les sauvegardes sont créées
directement dans le répertoire du jeu. Donc, la copie permet d'éviter de perdre vos sauvegardes du jeu d'origine ou
encore de charger une sauvegarde d'une ancienne partie de multiworld (ce qui pourrait avoir comme conséquence de briser
la logique du multiworld).

Désarchiver le randomizer d'Aquaria et copier tous les fichiers de l'archive dans le répertoire du jeu d'Aquaria. Le
fichier d'archive devrait contenir les fichiers suivants:
- aquaria_randomizer.exe
- OpenAL32.dll
- randomizer_files (directory)
- SDL2.dll
- usersettings.xml
- wrap_oal.dll
- cacert.pem

S'il y a des conflits entre les fichiers de l'archive zip et les fichiers du jeu original, vous devez utiliser
les fichiers contenus dans l'archive zip.

Il y a plusieurs manières de lancer le randomizer. Le plus simple consiste à utiliser le lanceur intégré en
exécutant simplement le fichier `aquaria_randomizer.exe`.

Il est également possible de lancer le randomizer en utilisant la ligne de commande (vous pouvez ouvrir une interface de
ligne de commande, entrez l'adresse `cmd` dans la barre d'adresse de l'explorateur de fichier de Windows). Voici
la ligne de commande à utiliser pour lancer le randomizer:

```bash
aquaria_randomizer.exe --name VotreNom --server leServeur:LePort
```

ou, si vous devez entrer un mot de passe:

```bash
aquaria_randomizer.exe --name VotreNom --server leServeur:LePort --password leMotDePasse
```

### Linux avec le fichier AppImage

Si vous utilisez le fichier AppImage, copiez le fichier dans le répertoire du jeu d'Aquaria. Ensuite, assurez-vous de
le mettre exécutable. Vous pouvez mettre le fichier exécutable avec la commande suivante:

```bash
chmod +x Aquaria_Randomizer-*.AppImage
```

ou bien en utilisant l'explorateur de fichier graphique de votre système (la permission d'exécution est
généralement dans les propriétés du fichier).

Pour lancer le randomizer en utilisant le lanceur intégré, seulement exécuter le fichier AppImage.

Vous pouvez également lancer le randomizer en spécifiant les informations de connexion dans les arguments de la ligne de commande:

```bash
./Aquaria_Randomizer-*.AppImage --name VotreNom --server LeServeur:LePort
```

Si vous devez entrer un mot de passe:

```bash
./Aquaria_Randomizer-*.AppImage --name VotreNom --server LeServeur:LePort --password LeMotDePasse
```

À noter que vous ne devez pas avoir plusieurs fichiers AppImage différents dans le même répertoire. Si cette situation
survient, le jeu sera lancé plusieurs fois.

### Linux avec le fichier tar

En premier lieu, assurez-vous de faire une copie du répertoire du jeu d'origine d'Aquaria. Les fichiers contenus
dans le randomizer auront comme impact de rendre le jeu d'origine non fonctionnel. Donc, effectuer la copie du jeu
avant de déposer le randomizer à l'intérieur permet de vous assurer de garder une version du jeu d'origine fonctionnel.

Désarchiver le fichier tar et copier tous les fichiers qu'il contient dans le répertoire du jeu d'origine d'Aquaria. Les
fichiers extraient du fichier tar devraient être les suivants:
- aquaria_randomizer
- randomizer_files (directory)
- usersettings.xml
- cacert.pem

S'il y a des conflits entre les fichiers de l'archive tar et les fichiers du jeu original, vous devez utiliser
les fichiers contenus dans l'archive tar.

Ensuite, vous devez installer manuellement les librairies dont dépend le jeu: liblua5, libogg, libvorbis, libopenal and
libsdl2. Vous pouvez utiliser le système de "package" de votre système pour les installer. Voici un exemple avec
Debian (et Ubuntu):

```bash
sudo apt install liblua5.1-0-dev libogg-dev libvorbis-dev libopenal-dev libsdl2-dev
```

Notez également que s'il y a des fichiers ".so" dans le répertoire d'Aquaria (`libgcc_s.so.1`, `libopenal.so.1`,
`libSDL-1.2.so.0` and `libstdc++.so.6`), vous devriez les retirer. Il s'agit de vieille version des librairies qui
ne sont plus fonctionnelles dans les systèmes modernes et qui pourrait empêcher le randomizer de fonctionner.

Pour lancer le randomizer en utilisant le lanceur intégré, seulement exécuter le fichier `aquaria_randomizer`.

Vous pouvez également lancer le randomizer en spécifiant les information de connexion dans les arguments de la
ligne de commande:

```bash
./aquaria_randomizer --name VotreNom --server LeServeur:LePort
```

Si vous devez entrer un mot de passe:

```bash
./aquaria_randomizer --name VotreNom --server LeServeur:LePort --password LeMotDePasse
```

Note: Si vous avez une erreur de permission lors de l'exécution du randomizer, vous pouvez utiliser cette commande
pour vous assurer que votre fichier est exécutable:

```bash
chmod +x aquaria_randomizer
```
### Steam Deck

Pour installer le randomizer sur la Steam Deck, seulement suivre la procédure pour les fichiers AppImage
indiquée précédemment.

### Aucun son sur Linux/Steam Deck

Si le jeu fonctionne sans problème, mais qu'il n'y a aucun son, c'est probablement parce que le jeu
n'arrive pas à utiliser le bon pilote de son. Généralement, le problème est réglé en ajoutant la
variable d'environnement `ALSOFT_DRIVERS=pulse`. Voici un exemple (peut varier en fonction de la manière
que le randomizer est lancé):

```bash
ALSOFT_DRIVERS=pulse ./Aquaria_Randomizer-*.AppImage --name VotreNom --server LeServeur:LePort
```

## Tracking automatique

Aquaria a un tracker complet qui supporte le tracking automatique.

1. Téléchargez [Aquaria AP Tracker](https://github.com/palex00/aquaria-ap-tracker/releases/latest) et [PopTracker](https://github.com/black-sliver/PopTracker/releases/latest).
2. Mettre le fichier compressé du tracker dans le sous-répertoire /packs/ du répertoire d'installation de PopTracker.
3. Lancez PopTracker, et ouvrez le pack d'Aquaria.
4. Pour activer le tracking automatique, cliquez sur le symbole "AP" dans le haut de la fenêtre.
5. Entrez l'adresse du serveur Archipelago (le serveur auquel vous avez connecté le client), le nom de votre slot, et le mot de passe (si un mot de passe est nécessaire).

Le logiciel vous indiquera si une mise à jour du pack est disponible.
