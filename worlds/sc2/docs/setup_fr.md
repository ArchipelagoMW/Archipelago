# Guide d'installation de *StarCraft 2 Randomizer*

Ce guide contient les instructions pour installer et dépanner le client de *StarCraft 2 Archipelago*, ainsi que des indications pour obtenir un fichier de configuration de *Starcraft 2 Archipelago* et comment modifier ce dernier.

## Logiciels requis

- [*StarCraft 2*](https://starcraft2.com/en-us/)
- [La version la plus récente d'Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)

## Comment est-ce que j'installe ce *randomizer*?

1. Installer *StarCraft 2* et Archipelago en suivant les instructions indiquées dans les liens précédents. Le client de *StarCraft 2 Archipelago* est téléchargé par le programme d'installation d'Archipelago.
   - Les utilisateurs de Linux devrait aussi suivre les instructions qui se retrouvent à la fin de cette page 
     (["Éxécuter sous Linux"](#éxécuter-sous-linux)).
2. Éxécuter `ArchipelagoStarcraft2Client.exe`.
   - Uniquement pour cette étape, les utilisateurs de macOS devraient plutôt suivre les instructions qui se trouvent à ["Éxécuter sous macOS"](#éxécuter-sous-macos).
3. Dans le client de *StarCraft 2 Archipelago*, écrire la commande `/download_data`. Cette commande va lancer l'installation des *Maps* et des *Data files* qui sont nécessairent pour jouer à *StarCraft 2 Archipelago*.

## Où est-ce que j'obtiens le fichier de configuration (i.e., le *yaml*) pour ce jeu?

Un fichier dans le format *yaml* est utilisé pour communiquer à Archipelago comment est-ce que vous voulez que votre jeu soit *randomized*. 
Ce dernier est nécesaire même si vous voulez utiliser les options par défaut. 
L'approche usuel pour générer un *multiworld* consiste à avoir un fichier *yaml* par monde.

Il y a trois approches pour obtenir un fichier *yaml* pour *StarCraft 2 Randomizer*:
* Vous pouvez aller à la page [*Player options*](/games/Starcraft%202/player-options) qui vous permet de définir vos choix via une interface graphique et ensuite télécharger le *yaml* correspondant à ces choix.
* Vous pouvez obtenir le modèle de base en le téléchargant de la page [*Player options*](/games/Starcraft%202/player-options) ou en cliquant sur *Generate template* après avoir éxécuté le *Launcher* d'archipelago (i.e., `ArchipelagoLauncher.exe`). Ce modèle de base inclut une desciption pour chacun des options et vous n'avez qu'à modifier les options dans un éditeur de texte de votre choix.
* Vous pouvez demander à quelqu'un d'autres de partager un de ces fichiers *yaml* pour l'utiliser ou l'ajuster à vos préférences.

Prennez soin de vous rappeller du nom de joueur que vous avez inscrit dans la page à options ou dans le fichier *yaml* puisque vous en aurez besoin pour vous connecter à votre monde!

Notez que la page *Player options* ne permet pas de définir certaines des options avancées, e.g., l'exclusion de certaines unitées ou de leur *upgrade*. 
Utilisez la page [*Weighted Options*](/weighted-options) pour avoir accès à ces dernières.

Si vous désirez des informations et/ou instructions générale sur l'utilisation d'un fichier *yaml* pour Archipelago, veuilliez consutler [*Creating a YAML*](/tutorial/Archipelago/setup/en#creating-a-yaml).

### Questions récurrentes à propos du fichier yaml
#### Comment est-ce que je sais que mon *yaml* est bien définit?

La manière la plus simple de valider est d'essayer. 
Sauvegarder votre *yaml* dans le dossier `Players/` de votre installation d'Archipelago et éxécuter `ArchipelagoGenerate.exe`. 
Si votre *yaml* est bien définit, vous devriez voir un nouveau fichier, avec l'extension `.zip`, apparaître dans le dossier `output/` de votre installation d'Archipelago.
Il est recommandé de lancer `ArchipelagoGenerate.exe` via un terminal afin que vous puissiez voir les messages générés par le logiciel, ce qui va inclure toutes erreurs qui a eu lieu et le nom de fichier généré.
Si vous n'appréciez pas le fait d'utiliser un terminal, vous pouvez aussi regarder le fichier *log* qui va être produit dans le dossier `logs/`.

#### À quoi sert l'option *Progression Balancing*?

Pour un monde *Starcraft 2* seule, cette option ne fait rien. 
Il s'agit d'une option d'Archipelago qui permet de balancer la progression d'un monde relativement aux autres mondes en interchangent les *items* de progression dans les *sphères*.
Si le *Progression Balancing* d'un monde est plus grand que ceux des autres, les *items* de progression de ce monde ont plus de chance d'être obtenus tôt et vice-versa si sa valeur est plus petite que celle des autres mondes.
Cependant, *Starcraft 2* est beaucoup plus permissif en termes d'*items* qui sont nécessaire pour progresser.
Pour cette raison, cet ajustement a souvent peu d'influence sur la capacité de progresser dans un monde de *StarCraft 2*. 
Notez que l'utilisation de cette option, i.e. au moins un monde avec une valeur différente de *Progression Balancing*, augmente le temps de génération d'un *MultiWorld*, alors certains recommandent de ne pas toucher à cette option.

#### Comment est-ce que je définie une liste d'*items*, e.g. pour l'option *excluded items*?

Vous pouvez lire sur la syntaxe des conteneurs dans le format *yaml* à la page [*YAML specification*](https://yaml.org/spec/1.2.2/#21-collections). 
Pour les listes, chaque *item* doit être sur sa propre ligne et doit être précédé par un trait d'union.

```yaml
excluded_items:
  - Battlecruiser
  - Drop-Pods (Kerrigan Tier 7)
```

Une liste vide est représentée par une paire de crochet: `[]`. 
Il s'agît de la valeur par défaut dans le modèle de base, ce qui devrait vous aider à apprendre à utiliser cette syntaxe.

#### Comment est-ce que je fais pour avoir des *items* dès le départ?

L'option *starting inventory* est un *map* et non une liste. 
Ainsi, elle permet de spécifier le nombre de chaque *item* avec lequel vous allez commencer.
Sa syntaxe consiste à indiquer le nom de l'*item*, suivit par un deux points, puis par un espace et enfin par le nombre désiré de cette *item*.

```yaml
start_inventory:
  Micro-Filtering: 1
  Additional Starting Vespene: 5
```

Un *map* vide est représenté par une paire d'accolade: `{}`. 
Il s'agît de la valeur par défaut dans le modèle de base, ce qui devrait vous aider à apprendre à utiliser cette syntaxe.

#### Comment est-ce que je fais pour connaître le nom des *items* dans *StarCraft 2 Archipelago*? 

Vous trouverez la liste complète des *items* de *StarCraft 2 Archipelago* à la page [*Icon Repository*](https://matthewmarinets.github.io/ap_sc2_icons/).

## Comment est-ce que je peux joindre un *MultiWorld*?

1. Éxécuter `ArchipelagoStarcraft2Client.exe`.
   - Uniquement pour cette étape, les utilisateurs de macOS devraient plutôt suivre les instructions à la page ["Éxécuter sous macOS"](#éxécuter-sous-macos).
2. Entrer la commande `/connect [server ip]`.
   - Si le *MultiWorld* est hébergé via un siteweb, l'IP du server devrait être indiqué dans le haut de la page de votre *room*.
3. Inscrivez le nom de joueur spécifié dans votre *yaml* lorsque vous y êtes invité.
4. Si le serveur a un mot de passe, l'inscrire lorsque vous y êtes invité.
5. Une fois connecté, changer l'onglet *StarCraft 2 Launcher* dans le client. Dans cet onglet, vous devriez trouver toutes les missions de votre monde. Les missions qui ne sont pas disponible présentement auront leur texte dans une tonte de gris. Vous n'avez qu'à cliquer une des missions qui est disponible pour la commencer!

## *StarCraft 2* ne démarre pas quand je tente de commencer une mission

Pour commencer, regarder le fichier *log* pour trouver le problème (ce dernier devrait être dans `[Archipelago Directory]/logs/SC2Client.txt`).
Si vous ne comprennez pas le problème avec le fichier *log*, visitez notre [*Discord*](https://discord.com/invite/8Z65BR2) pour demander de l'aide dans le forum *tech-support*.
Dans votre message, veuillez inclure une description détaillé de ce qui ne marche pas et ajouter en pièce jointe le fichier *log*.

## Éxécuter sous macOS

Pour éxécuter *StarCraft 2* via Archipelago sous macOS, vous devez éxécuter le client à partir de la source tel qu'indiqué ici: [*macOS Guide*](/tutorial/Archipelago/mac/en). 
Notez que pour lancer le client, vous devez éxécuter la commande `python3 Starcraft2Client.py`.

## Éxécuter sous Linux

Pour éxécuter *StarCraft 2* via Archipelago sous Linux, vous allez devoir installer le jeu avec *Wine* et ensuite éxécuter le client d'Archipelago pour Linux.

Confirmez que vous avez installé *StarCraft 2* via *Wine* et que vous avez suivi les 
[instructions d'installation](#comment-est-ce-que-j'installe-ce-randomizer?) pour ajouter les *Maps* et et les *Data files* nécessairent pour *StarCraft 2 Archipelago* au bon endroit.
Vous n'avez pas besoin de copier les fichiers `.dll`.
Si vous avez des difficultés pour installer ou éxécuter *StarCraft 2* sous Linux, il est recommandé d'utiliser le logiciel *Lutris*.

Copier ce qui suit dans un fichier avec l'extension `.sh`, en prennant soin de définir les variables **WINE** et **SC2PATH** avec les bons chemins et de définir **PATH_TO_ARCHIPELAGO** avec le chemin vers le dossier qui contient le *AppImage* si ce dernier n'est pas dans le même dossier que ce script.

```sh
# Permet au client de savoir que SC2 est éxécuté via Wine
export SC2PF=WineLinux
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# À_CHANGER Remplacer le chemin avec celui qui correspond à la version de Wine utilisé pour éxécuter SC2
export WINE="/usr/bin/wine"

# À_CHANGER Remplacer le chemin par celui qui indique où StarCraft II est installé
export SC2PATH="/home/user/Games/starcraft-ii/drive_c/Program Files (x86)/StarCraft II/"

# À_CHANGER Indiquer le dossier qui contient l'AppImage d'Archipelago
PATH_TO_ARCHIPELAGO=

# Obtiens la dernière version de l'AppImage de Archipelago dans le dossier PATH_TO_ARCHIPELAGO.
# Si PATH_TO_ARCHIPELAGO n'est pas défénit, la valeur par défaut est le dossier qui contient ce script.
ARCHIPELAGO="$(ls ${PATH_TO_ARCHIPELAGO:-$(dirname $0)}/Archipelago_*.AppImage | sort -r | head -1)"

# Lance le client de Archipelago
$ARCHIPELAGO Starcraft2Client
```

Pour une installation via Lutris, vous pouvez éxécuter `lutris -l` pour obtenir l'identifiant numérique de votre installation *StarCraft II* et ensuite éxécuter la commande suivante, en remplacant **${ID}** pour cette identifiant numérique.

    lutris lutris:rungameid/${ID} --output-script sc2.sh

Cette commande va définir toutes les variables d'environnement nécessaires pour éxécuter *StarCraft 2* dans un script, incluant le chemin vert l'éxécutable *Wine* que Lutris utilise.
Après ça, vous pouvez enlever la ligne qui permet de démarer *Battle.Net* et copier le code décrit plus haut dans le script existant.

