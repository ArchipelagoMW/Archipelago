# Guide d'installation du *StarCraft 2 Randomizer*

Ce guide contient les instructions pour installer et dépanner le client de *StarCraft 2 Archipelago*, ainsi que des 
indications pour obtenir un fichier de configuration de *StarCraft 2 Archipelago* et comment modifier ce dernier.

## Logiciels requis

- [*StarCraft 2*](https://starcraft2.com/en-us/)
   - Bien que *StarCraft 2 Archipelago* supporte les quatre campagnes, elles ne sont pas obligatoires pour jouer au 
   *randomizer*. 
   Si vous ne possédez pas certaines campagnes, il vous suffit de les exclure dans le fichier de configuration de 
   votre monde.
- [La version la plus récente d'Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)

## Comment est-ce que j'installe ce *randomizer*?

1. Installer *StarCraft 2* et Archipelago en suivant les instructions indiquées dans les liens précédents. Le client de 
*StarCraft 2 Archipelago* est téléchargé par le programme d'installation d'Archipelago.
   - Les utilisateurs de Linux devraient aussi suivre les instructions qui se retrouvent à la fin de cette page 
(["Exécuter sous Linux"](#exécuter-sous-linux)).
   - Notez que votre jeu *StarCraft 2* doit être en anglais pour fonctionner avec Archipelago.
2. Exécuter `ArchipelagoStarcraft2Client.exe`.
   - Uniquement pour cette étape, les utilisateurs de macOS devraient plutôt suivre les instructions qui se trouvent à 
["Exécuter sous macOS"](#exécuter-sous-macos).
3. Dans le client de *StarCraft 2 Archipelago*, écrire la commande `/download_data`. Cette commande va lancer 
l'installation des fichiers qui sont nécessaires pour jouer à *StarCraft 2 Archipelago*.

## Où est-ce que j'obtiens le fichier de configuration (i.e., le *yaml*) pour ce jeu?

Un fichier dans le format *yaml* est utilisé pour communiquer à Archipelago comment vous voulez que votre jeu soit 
*randomized*. 
Ce dernier est nécessaire même si vous voulez utiliser les options par défaut. 
L'approche usuelle pour générer un *multiworld* consiste à avoir un fichier *yaml* par monde.

Il y a trois approches pour obtenir un fichier *yaml* pour *StarCraft 2 Randomizer*:
* Vous pouvez aller à la page [*Player options*](/games/Starcraft%202/player-options) qui vous permet de définir vos 
choix via une interface graphique et ensuite télécharger le *yaml* correspondant à ces choix.
* Vous pouvez obtenir le modèle de base en le téléchargeant à la page 
[*Player options*](/games/Starcraft%202/player-options) ou en cliquant sur *Generate template* après avoir exécuté le 
*Launcher* d'Archipelago (i.e., `ArchipelagoLauncher.exe`). Ce modèle de base inclut une description pour chacune des 
options et vous n'avez qu'à modifier les options dans un éditeur de texte de votre choix.
* Vous pouvez demander à quelqu'un d'autre de partager un de ces fichiers *yaml* pour l'utiliser ou l'ajuster à vos 
préférences.

Prenez soin de vous rappeler du nom de joueur que vous avez inscrit dans la page à options ou dans le fichier *yaml* 
puisque vous en aurez besoin pour vous connecter à votre monde!

Si vous désirez des informations et/ou instructions générales sur l'utilisation d'un fichier *yaml* pour Archipelago, 
veuillez consulter [*Creating a YAML*](/tutorial/Archipelago/setup/en#creating-a-yaml).

### Questions récurrentes à propos du fichier *yaml*

#### Comment est-ce que je sais que mon *yaml* est bien défini?

La manière la plus simple de valider votre *yaml* est d'utiliser le 
[système de validation](/check) du site web.

Vous pouvez aussi le tester en tentant de générer un *multiworld* avec votre *yaml*.
Pour faire ça, sauvegardez votre *yaml* dans le dossier `Players/` de votre installation d'Archipelago et exécutez 
`ArchipelagoGenerate.exe`. 
Si votre *yaml* est bien défini, vous devriez voir un nouveau fichier, avec l'extension `.zip`, apparaître dans le 
dossier `output/` de votre installation d'Archipelago.
Il est recommandé de lancer `ArchipelagoGenerate.exe` via un terminal afin que vous puissiez voir les messages générés 
par le logiciel, ce qui va inclure toutes erreurs qui ont eu lieu et le nom de fichier généré.
Si vous n'appréciez pas le fait d'utiliser un terminal, vous pouvez aussi regarder le fichier *log* qui va être produit 
dans le dossier `logs/`.

#### À quoi sert l'option *Progression Balancing*?

Pour *StarCraft 2*, cette option ne fait pas grand-chose.
Il s'agit d'une option d'Archipelago permettant d'équilibrer la progression des mondes en interchangeant les *items* 
dans les *spheres*. 
Si le *Progression Balancing* d'un monde est plus grand que ceux des autres, les *items* de progression de ce monde ont 
plus de chance d'être obtenus tôt et vice-versa si sa valeur est plus petite que celle des autres mondes. 
Cependant, *StarCraft 2* est beaucoup plus permissif en termes d'*items* qui permettent de progresser, ce réglage à 
donc peu d'influence sur la progression dans *StarCraft 2*. 
Vu qu'il augmente le temps de génération d'un *MultiWorld*, nous recommandons de le désactiver, c-à-d le définir à 
zéro, pour *StarCraft 2*. 


#### Comment est-ce que je définis une liste d'*items*, e.g. pour l'option *excluded items*?

Vous pouvez lire sur la syntaxe des conteneurs dans le format *yaml* à la page 
[*YAML specification*](https://yaml.org/spec/1.2.2/#21-collections). 
Pour les listes, chaque *item* doit être sur sa propre ligne et doit être précédé par un trait d'union.

```yaml
excluded_items:
  - Battlecruiser
  - Drop-Pods (Kerrigan Ability)
```

Une liste vide est représentée par une paire de crochets: `[]`. 
Il s'agit de la valeur par défaut dans le modèle de base, ce qui devrait vous aider à apprendre à utiliser cette 
syntaxe.

#### Comment est-ce que je fais pour avoir des *items* dès le départ?

L'option *starting inventory* est un *map* et non une liste. 
Ainsi, elle permet de spécifier le nombre de chaque *item* avec lequel vous allez commencer.
Sa syntaxe consiste à indiquer le nom de l'*item*, suivi par un deux-points, puis par un espace et enfin par le nombre 
désiré de cet *item*.

```yaml
start_inventory:
  Micro-Filtering: 1
  Additional Starting Vespene: 5
```

Un *map* vide est représenté par une paire d'accolades: `{}`. 
Il s'agit de la valeur par défaut dans le modèle de base, ce qui devrait vous aider à apprendre à utiliser cette 
syntaxe.

#### Comment est-ce que je fais pour connaître le nom des *items* et des *locations* dans *StarCraft 2 Archipelago*? 

La page [*datapackage*](/datapackage) d'Archipelago liste l'ensemble des *items* et des *locations* de tous les jeux 
que le site web prend en charge actuellement, dont ceux de *StarCraft 2*.

Vous trouverez aussi la liste complète des *items* de *StarCraft 2 Archipelago* à la page 
[*Icon Repository*](https://matthewmarinets.github.io/ap_sc2_icons/). 
Notez que cette page contient diverses informations supplémentaires sur chacun des *items*.
Cependant, l'information présente dans cette dernière peut différer de celle du *datapackage* d'Archipelago 
puisqu'elle est générée, habituellement, à partir de la version en développement de *StarCraft 2 Archipelago* qui 
n'ont peut-être pas encore été inclus dans le site web d'Archipelago.

Pour ce qui concerne les *locations*, vous pouvez consulter tous les *locations* associés à une mission dans votre 
monde en plaçant votre curseur sur la case correspondante dans l'onglet *StarCraft 2 Launcher* du client.


## Comment est-ce que je peux joindre un *MultiWorld*?

1. Exécuter `ArchipelagoStarcraft2Client.exe`.
   - Uniquement pour cette étape, les utilisateurs de macOS devraient plutôt suivre les instructions à la page 
["Exécuter sous macOS"](#exécuter-sous-macos).
2. Entrer la commande `/connect [server ip]`.
   - Si le *MultiWorld* est hébergé via un siteweb, l'IP du server devrait être indiqué dans le haut de la page de 
votre *room*.
3. Inscrivez le nom de joueur spécifié dans votre *yaml* lorsque vous y êtes invité.
4. Si le serveur a un mot de passe, l'inscrire lorsque vous y êtes invité.
5. Une fois connecté, aller sur l'onglet *StarCraft 2 Launcher* dans le client. Dans cet onglet, vous devriez trouver 
toutes les missions de votre monde. Les missions qui ne sont pas disponibles présentement auront leur texte dans une 
nuance de gris. Vous n'avez qu'à cliquer une des missions qui est disponible pour la commencer!

## *StarCraft 2* ne démarre pas quand je tente de commencer une mission

Pour commencer, regarder le fichier *log* pour trouver le problème (ce dernier devrait être dans 
`[Archipelago Directory]/logs/SC2Client.txt`).
Si vous ne comprenez pas le problème avec le fichier *log*, visitez notre 
[*Discord*](https://discord.com/invite/8Z65BR2) pour demander de l'aide dans le forum *tech-support*.
Dans votre message, veuillez inclure une description détaillée de ce qui ne marche pas et ajouter en pièce jointe le 
fichier *log*.

## Mon profil de raccourcis clavier n'est pas disponibles quand je joue à *StarCraft 2 Archipelago*

Pour que votre profil de raccourcis clavier fonctionne dans Archipelago, vous devez copier votre fichier de raccourcis 
qui se trouve dans `Documents/StarCraft II/Accounts/######/Hotkeys` vers `Documents/StarCraft II/Hotkeys`.
Si le dossier n'existe pas, créez-le.

Pour que *StarCraft 2 Archipelago* utilise votre profil, suivez les étapes suivantes.
Lancez *StarCraft 2* via l'application *Battle.net*. 
Changez votre profil de raccourcis clavier pour le mode standard et acceptez, puis sélectionnez votre profil 
personnalisé et acceptez. 
Vous n'aurez besoin de faire ça qu'une seule fois.

## Exécuter sous macOS

Pour exécuter *StarCraft 2* via Archipelago sous macOS, vous devez exécuter le client à partir de la source  
comme indiqué ici: [*macOS Guide*](/tutorial/Archipelago/mac/en). 
Notez que pour lancer le client, vous devez exécuter la commande `python3 Starcraft2Client.py`.

## Exécuter sous Linux

Pour exécuter *StarCraft 2* via Archipelago sous Linux, vous allez devoir installer le jeu avec *Wine* et ensuite 
exécuter le client d'Archipelago pour Linux.

Confirmez que vous avez installé *StarCraft 2* via *Wine* et que vous avez suivi les 
[instructions d'installation](#comment-est-ce-que-j'installe-ce-randomizer?) pour ajouter les *Maps* et les *Data 
files* nécessairent pour *StarCraft 2 Archipelago* au bon endroit.
Vous n'avez pas besoin de copier les fichiers `.dll`.
Si vous avez des difficultés pour installer ou exécuter *StarCraft 2* sous Linux, il est recommandé d'utiliser le 
logiciel *Lutris*.

Copier ce qui suit dans un fichier avec l'extension `.sh`, en prenant soin de définir les variables **WINE** et 
**SC2PATH** avec les bons chemins et de définir **PATH_TO_ARCHIPELAGO** avec le chemin vers le dossier qui contient le 
*AppImage* si ce dernier n'est pas dans le même dossier que ce script.

```sh
# Permet au client de savoir que SC2 est exécuté via Wine
export SC2PF=WineLinux
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# À_CHANGER Remplacer le chemin avec celui qui correspond à la version de Wine utilisé pour exécuter SC2
export WINE="/usr/bin/wine"

# À_CHANGER Remplacer le chemin par celui qui indique où StarCraft II est installé
export SC2PATH="/home/user/Games/starcraft-ii/drive_c/Program Files (x86)/StarCraft II/"

# À_CHANGER Indiquer le dossier qui contient l'AppImage d'Archipelago
PATH_TO_ARCHIPELAGO=

# Obtiens la dernière version de l'AppImage de Archipelago dans le dossier PATH_TO_ARCHIPELAGO.
# Si PATH_TO_ARCHIPELAGO n'est pas défini, la valeur par défaut est le dossier qui contient ce script.
ARCHIPELAGO="$(ls ${PATH_TO_ARCHIPELAGO:-$(dirname $0)}/Archipelago_*.AppImage | sort -r | head -1)"

# Lance le client de Archipelago
$ARCHIPELAGO "Starcraft 2 Client"
```

Pour une installation via Lutris, vous pouvez exécuter `lutris -l` pour obtenir l'identifiant numérique de votre 
installation *StarCraft II* et ensuite exécuter la commande suivante, en remplacant **${ID}** pour cet identifiant 
numérique.

    lutris lutris:rungameid/${ID} --output-script sc2.sh

Cette commande va définir toutes les variables d'environnement nécessaires pour exécuter *StarCraft 2* dans un script, 
incluant le chemin vers l'exécutable *Wine* que Lutris utilise.
Après ça, vous pouvez enlever la ligne qui permet de démarrer *Battle.Net* et copier le code décrit plus haut dans le 
script produit.

