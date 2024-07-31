# Guide avancé YAML

Ce guide couvre des options plus avancées disponibles dans les fichiers YAML.
Il est destiné à l'utilisateur qui prévoit de modifier manuellement son fichier YAML.
La lecture de ce guide devrait prendre environ 10 minutes.

Si vous souhaitez générer un YAML de base entièrement jouable sans éditer de fichier, visitez la page des paramètres du jeu que vous prévoyez de jouer
La page des paramètres pondérés peut également gérer la plupart des paramètres avancés discutés ici.

La page des paramètres se trouve sur la page des jeux, il vous suffit de cliquer sur le lien "Settings Page" sous le nom du jeu que vous souhaitez.
* Page des jeux pris en charge: [Liste des jeux Archipelago](/games)
* Page des paramètres pondérés: [Paramètres pondérés d'Archipelago](/weighted-settings)

En cliquant sur le bouton "Export Settings" en bas à gauche, vous obtiendrez un fichier YAML pré-rempli avec vos options.
La page des paramètres des joueurs propose également un lien pour télécharger un fichier modèle complet pour ce jeu,
contenant toutes les options possibles pour le jeu, y compris celles qui ne s'affichent pas correctement sur le site.

## Aperçu YAML

Le système Archipelago génère des jeux à l'aide de fichiers de configuration des joueurs en tant qu'entrée. Ceux-ci seront
des fichiers YAML et chaque monde en aura un contenant ses paramètres personnalisés pour le jeu que ce monde jouera.

## Formatage YAML

Les fichiers YAML sont un format de fichiers de configuration lisible par un humain. La syntaxe de base d'un fichier YAML aura un nœud `racine` et ensuite différents niveaux de nœuds `imbriqués` que le générateur lira pour déterminer vos paramètres.

Pour imbriquer du texte, la syntaxe correcte consiste à indenter de **deux espaces** à partir du parent.
Un fichier YAML peut être édité avec n'importe quel éditeur de texte que vous choisissez, bien que je recommande 
personnellement l'utilisation de Sublime Text.
Site: [Site SublimeText](https://www.sublimetext.com)

Ce programme prend en charge le formatage correct du fichier YAML par défaut, vous pourrez donc utiliser la touche Tab
et obtenir une mise en surbrillance correcte pour d'éventuelles erreurs commises lors de l'édition du fichier.
Si vous utilisez un autre éditeur de texte, assurez-vous que votre indentation est correcte avec deux espaces.

Un fichier YAML typique ressemblera à ceci:

```yaml
option_racine:
  option_imbriquee_un:
    parametre_un_option_un: 1
    parametre_un_option_deux: 0
  option_imbriquee_deux:
    parametre_deux_option_un: 14
    parametre_deux_option_deux: 43
```

Dans Archipelago, les options YAML sont toujours écrites en minuscules avec des tirets bas séparant les mots.
Les nombres suivant les `:` ici sont des poids. Le générateur lira le poids de chaque option, puis lancera
cette option autant de fois que son nombre, l'option suivante autant de fois que son nombre, et ainsi de suite.

Pour l'exemple ci-dessus, `option_imbriquee_un` aura `parametre_un_option_un` une fois et `parametre_un_option_deux` zéro fois,
donc `parametre_un_option_un` est garanti de se produire.

Pour `option_imbriquee_deux`, `parametre_deux_option_un` sera lancé 14 fois et `parametre_deux_option_deux` sera lancé 43 fois les uns contre les autres.
Cela signifie que `parametre_deux_option_deux` sera plus susceptible de se produire, mais ce n'est pas garanti, ajoutant plus de hasard et
de "mystère" à vos paramètres. Chaque paramètre configurable prend en charge les poids.

## Options racines

Actuellement, il n'y a que quelques options qui sont des options racines. Tout le reste devrait être imbriqué dans l'une de ces options racines ou,
dans certains cas, imbriqué dans d'autres options imbriquées. Les seules options qui devraient exister en racine sont
`description`, `name`, `game`, `requires`, et le nom des jeux pour lesquels vous voulez des paramètres.

* `description` est ignorée par le générateur et sert simplement à organiser si vous avez plusieurs fichiers utilisant
  cela pour détailler l'intention du fichier.

* `name` est le nom du joueur que vous souhaitez utiliser et est utilisé pour que vos données de slot se connectent
  avec la plupart des jeux. Cela peut également être rempli avec plusieurs noms ayant chacun un poids.
  Les noms peuvent également contenir certains mots-clés, entourés d'accolades, qui seront remplacés lors de la génération
  par un nombre:
  
  * `{player}` sera remplacé par le numéro de slot du joueur.
  * `{PLAYER}` sera remplacé par le numéro de slot du joueur si ce numéro de slot est supérieur à 1, sinon vide.
  * `{number}` sera remplacé par la valeur du compteur du nom.
  * `{NUMBER}` sera remplacé par la valeur du compteur du nom si la valeur du compteur est supérieure à 1, sinon vide.
  
* `game` est l'endroit où va être le nom de votre jeu choisi, soit, si vous le souhaitez,
  peut être rempli avec plusieurs jeux, chacun ayant des poids différents.

* `requires` détaille différentes exigences du générateur pour que le YAML fonctionne comme vous vous y attendez.
Généralement, cela est utile pour détailler la version d'Archipelago pour laquelle ce YAML a été préparé,
car si elle est lancée sur une version plus ancienne, des paramètres peuvent être manquants et il ne fonctionnera pas comme prévu.
Si un plan est utilisé dans le fichier, le spécifier ici pour s'assurer qu'il sera utilisé est une bonne pratique.

## Options de jeu

L'un de vos paramètres racines sera le nom du jeu pour lequel vous souhaitez remplir des paramètres. Comme il est possible
de donner un poids à n'importe quelle option, il est possible d'avoir un fichier qui peut générer une partie pour vous
où vous ne savez pas quel jeu vous allez jouer. Pour ces cas, vous voudrez remplir les options de jeu pour chaque jeu
qui peut être généré par ces paramètres, même si un jeu peut être généré, il **doit** avoir une section de paramètres
même si elle est vide.

### Options universelles du jeu

Certaines options dans Archipelago peuvent être utilisées par chaque jeu mais doivent toujours être placées
dans la section du jeu concerné.

Actuellement, ces options sont `accessibility`, `progression_balancing`, `triggers`, `local_items`, `non_local_items`, `start_inventory`,
`start_hints`, `start_location_hints`, `exclude_locations`, `priority_locations`, `item_links`, et diverses options plando.

Consultez le guide plando pour plus d'informations sur les options plando. Guide plando: [Guide Archipelago Plando](/tutorial/Archipelago/plando/fr)

* `accessibility` détermine le niveau d'accès au jeu que la génération s'attend à ce que vous ayez pour atteindre votre objectif de complétion.
  Cela prend en charge `items`, `locations`, et `minimal` et est réglé par défaut sur `locations`.
  * `locations` garantira que toutes les emplacements soient accessibles dans votre monde.
  * `items` garantira que vous pouvez acquérir tous les objets logiquement pertinents dans votre monde. Certains objets, tels que des clés, peuvent être auto-verrouillants.
  * `minimal` garantira seulement que la partie est battable. Vous aurez la garantie de pouvoir terminer logiquement la partie, mais vous ne pourrez peut-être pas accéder à tous les emplacements ou acquérir tous les objets. Un bon exemple de cela est d'avoir une grosse clé dans le grand coffre d'un donjon dans ALTTP, ce qui le rend impossible à obtenir et à terminer le donjon.
* `progression_balancing` est un système que le générateur Archipelago utilise pour essayer de réduire autant que possible le mode ["BK"](glossaire/en/#burger-king-/-bk-mode) (mode "Burger King").
  Cela implique principalement de déplacer les objets de progression nécessaires dans des sphères logiques antérieures pour rendre les jeux plus accessibles afin que les joueurs aient presque toujours quelque chose à faire. Cela peut être dans une plage de 0 à 99 et est de 50 par défaut. Ce nombre représente un pourcentage du joueur progressant le plus loin.
  * Par exemple : avec la valeur par défaut de 50%, si le joueur le plus avancé peut accéder à 40% de ses objets, le randomiseur essaie de vous permettre d'accéder à au moins 20% de vos objets. 50% de 40% est 20%.
  * Notez qu'il n'est pas toujours garanti qu'il pourra vous amener jusqu'à ce seuil.
* `triggers` est l'une des options les plus avancées qui vous permet de créer des ajustements conditionnels.
  Vous pouvez lire plus de détails dans le guide des déclencheurs. Guide des déclencheurs: [Guide Archipelago Triggers](/tutorial/Archipelago/triggers/fr)
* `local_items` forcera tous les objets que vous voulez dans votre monde au lieu d'être dans un autre monde.
* `non_local_items` est l'inverse de `local_items`, forçant tous les objets que vous voulez dans un autre monde au lieu du vôtre.
* `start_inventory` donnera les objets définis ici au début de votre jeu. Le format doit être le nom tel qu'il apparaît dans les fichiers du jeu
  et la quantité avec laquelle vous souhaitez commencer. Par exemple `Rupees(5): 6` vous donnera 30 rubis.
* `start_hints` vous donne des indices de serveur gratuits pour les objets définis au début du jeu, vous permettant
  de trouver l'emplacement sans utiliser de points d'indice.
* `start_location_hints` est la même que `start_hints` mais pour les emplacements, vous permettant d'obtenir des indices
  sur l'objet qui s'y trouve sans utiliser de points d'indice.
* `exclude_locations` vous permet de définir des emplacements que vous ne voulez pas faire et lors de la génération,
  cela forcera un objet "junk" qui n'est pas nécessaire pour la progression à aller à ces emplacements.
* `priority_locations` est l'inverse de `exclude_locations`, forçant un objet de progression dans les emplacements définis.
* `item_links` permet aux joueurs de lier leurs objets dans un groupe avec le même nom de lien d'objet et de jeu.
  Les objets déclarés dans `item_pool` sont combinés et lorsque un objet est trouvé pour le groupe, tous les joueurs du groupe
  le reçoivent. Les liens d'objets peuvent également avoir des objets locaux et non locaux, forçant les objets à être placés dans
  les mondes du groupe ou dans des mondes extérieurs au groupe. Si les joueurs ont une quantité variable d'un objet spécifique
  dans le lien, la quantité la plus basse des joueurs sera la quantité mise dans le groupe.

### Nombres aléatoires

Les options prenant le choix d'un nombre peuvent également utiliser diverses options `random` pour choisir un nombre au hasard.

- `random` choisira un nombre autorisé pour le paramètre au hasard.
- `random-low` choisira un nombre autorisé pour le paramètre au hasard, mais sera pondéré vers les nombres plus bas.
- `random-middle` choisira un nombre autorisé pour le paramètre au hasard, mais sera pondéré vers le milieu de la plage.
- `random-high` choisira un nombre autorisé pour le paramètre au hasard, mais sera pondéré vers les nombres plus élevés.
- `random-range-#-#` choisira un nombre au hasard entre les nombres spécifiés. Par exemple, `random-range-40-60` choisira un nombre entre 40 et 60.
- `random-range-low-#-#`, `random-range-middle-#-#`, et `random-range-high-#-#` choisiront un nombre au hasard parmi les nombres spécifiés, mais avec les pondérations spécifiées.

### Exemple


```yaml

description: An example using various advanced options
name: Example Player
game: 
  A Link to the Past: 10
  Timespinner: 10
requires: 
  version: 0.4.1
A Link to the Past:
  accessibility: minimal
  progression_balancing: 50
  smallkey_shuffle:
    original_dungeon: 1
    any_world: 1
  crystals_needed_for_gt:
    random-low: 1
  crystals_needed_for_ganon:
    random-range-high-1-7: 1
  local_items:
    - Bombos
    - Ether
    - Quake
  non_local_items:
    - Moon Pearl
  start_inventory:
    Pegasus Boots: 1
    Bombs (3): 2
  start_hints:
    - Hammer
  start_location_hints:
    - Spike Cave
  exclude_locations:
    - Cave 45
  priority_locations:
    - Link's House
  item_links:
    - name: rods
      item_pool:
        - Fire Rod
        - Ice Rod
      replacement_item: "Rupee (1)"
      link_replacement: true
  triggers:
    - option_category: A Link to the Past
      option_name: smallkey_shuffle
      option_result: any_world
      options:
        A Link to the Past:
          bigkey_shuffle: any_world
          map_shuffle: any_world
          compass_shuffle: any_world
Timespinner:
  accessibility: minimal
  progression_balancing: 50
  item_links: # Share part of your item pool with other players.
    - name: TSAll
      item_pool: 
        - Everything
      local_items:
        - Twin Pyramid Key
        - Timespinner Wheel
      replacement_item: null
```
#### Ceci est un fichier YAML entièrement fonctionnel qui accomplira toutes les tâches suivantes :

* `description` nous donne une vue d'ensemble générale afin que, si nous consultons ce fichier plus tard, nous puissions comprendre l'intention.
* `name` est `Nom du joueur` et cela sera utilisé dans la console du serveur lors de l'envoi et de la réception d'objets.
* `game` a une chance égale d'être soit `A Link to the Past` ou `Timespinner` avec une chance de 10/20 pour chacun.
  Cela est dû au poids de chaque jeu, qui est de 10, et le total de tous les poids est de 20.
* `requires` est défini sur la version requise 0.3.2 ou supérieure.
* `accessibility` pour les deux jeux est définie sur `minimal`, ce qui rendra cette partie faisable uniquement,
  certaines localités et objets pouvant être complètement inaccessibles mais la partie restera réalisable.
* `progression_balancing` pour les deux jeux est fixé à 50, la valeur par défaut, ce qui signifie que nous recevrons probablement
  des objets importants plus tôt, augmentant la chance d'avoir des choses à faire.
* `A Link to the Past` définit un emplacement pour imbriquer toutes les options de jeu que nous souhaitons
  utiliser pour notre jeu `A Link to the Past`.
* `smallkey_shuffle` est une option pour A Link to the Past qui détermine comment les petites clés de donjon sont mélangées.
  Dans cet exemple, il y a une chance de 1/2 pour qu'elles soient placées dans leur donjon d'origine et une chance de 1/2
  pour qu'elles soient placées n'importe où parmi les mondes multiples.
* `crystals_needed_for_gt` détermine le nombre de cristaux nécessaires pour entrer dans l'entrée de la Tour de Ganon.
  Dans cet exemple, un nombre aléatoire sera choisi dans la plage autorisée pour ce paramètre (0 à 7), mais sera pondéré
  en faveur d'un nombre plus bas.
* `crystals_needed_for_ganon` détermine le nombre de cristaux nécessaires pour vaincre Ganon.
  Dans cet exemple, un nombre entre 1 et 7 sera choisi au hasard, pondéré en faveur d'un nombre élevé.
* `local_items` force les médailles `Bombos`, `Ether` et `Quake` à être toutes placées dans notre propre monde,
  ce qui signifie que nous devons les trouver nous-mêmes.
* `non_local_items` force la `Moon Pearl` à être placée dans le monde de quelqu'un d'autre,
  ce qui signifie que nous ne pourrons pas la trouver.
* `start_inventory` définit une zone pour déterminer quels objets nous aimerions commencer avec. Pour cet exemple, nous avons :
  * `Pegasus Boots: 1` qui nous donne 1 exemplaire des Pegasus Boots
  * `Bombs (3): 2` nous donne 2 paquets de 3 bombes, soit 6 bombes au total
* `start_hints` nous donne un indice de départ pour le marteau disponible au début du monde multiple que nous pouvons utiliser sans coût.
* `start_location_hints` nous donne un indice de départ pour l'emplacement `Spike Cave` disponible au début du MultiWorld
  qui peut être utilisé sans coût.
* `exclude_locations` force un objet non important à être placé dans l'emplacement `Cave 45`.
* `priority_locations` force un objet de progression à être placé dans l'emplacement `Link's House`.
* `item_links`
  * Pour `A Link to the Past`, tous les joueurs du groupe d'objets `rods` partageront leurs baguettes de feu et de glace,
  et les objets du joueur seront remplacés par des rubis uniques. Le rubis sera également partagé entre ces joueurs.
  * Pour `Timespinner`, tous les joueurs du groupe d'objets `TSAll` partageront l'ensemble de leurs objets,
    et la `Twin Pyramid Key` et `Timespinner Wheel` seront forcées parmi les mondes de ceux du groupe.
	L'objet de remplacement `null` permettra, au lieu de forcer un objet spécifique choisi, au générateur de choisir
	au hasard un objet de comblement pour remplacer les objets du joueur.
* `triggers` nous permet de définir un déclencheur de telle sorte que si notre option `smallkey_shuffle` doit donner le résultat
  `any_world`, cela garantira également que `bigkey_shuffle`, `map_shuffle` et `compass_shuffle` sont également forcés vers
  le résultat `any_world`. Plus d'informations sur les déclencheurs peuvent être trouvées dans le [guide des déclencheurs](/tutorial/Archipelago/triggers/fr).

## Génération de plusieurs mondes

Les fichiers YAML peuvent être configurés pour générer plusieurs mondes en utilisant un seul fichier. Cela est principalement utile
si vous jouez à un monde multiple asynchrone (abrégé en async) et que vous souhaitez soumettre plusieurs mondes car ils peuvent
être condensés en un seul fichier, éliminant ainsi le besoin de gérer des fichiers séparés si vous choisissez de le faire.

Par mesure de précaution, avant de soumettre un fichier YAML multi-jeux comme celui-ci dans un monde multiple synchrone/sync,
veuillez confirmer que les autres joueurs du monde multiple sont d'accord avec ce que vous soumettez, et soyez raisonnablement
raisonnable concernant la soumission. (c'est-à-dire que plusieurs jeux longs (SMZ3, OoT, HK, etc.) pour un jeu prévu pour <2 heures
ne sont probablement pas considérés comme raisonnables, mais soumettre un ChecksFinder aux côtés d'un autre jeu ou soumettre
plusieurs runs de Slay the Spire est probablement acceptable)

Pour configurer votre fichier pour générer plusieurs mondes, utilisez 3 tirets `---` sur une ligne vide pour séparer la fin d'un monde
et le début d'un autre monde.

### Example

```yaml
description: Example of generating multiple worlds. World 1 of 3
name: Mario
game: Super Mario 64
requires:
  version: 0.3.2
Super Mario 64:
  progression_balancing: 50
  accessibilty: items
  EnableCoinStars: false
  StrictCapRequirements: true
  StrictCannonRequirements: true
  StarsToFinish: 70
  AmountOfStars: 70
  DeathLink: true
  BuddyChecks: true
  AreaRandomizer: true
  ProgressiveKeys:
    true: 1
    false: 1

---

description: Example of generating multiple worlds. World 2 of 3
name: Minecraft
game: Minecraft
Minecraft:
  progression_balancing: 50
  accessibilty: items
  advancement_goal: 40
  combat_difficulty: hard
  include_hard_advancements: false
  include_unreasonable_advancements: false
  include_postgame_advancements: false
  shuffle_structures: true
  structure_compasses: true
  send_defeated_mobs: true
  bee_traps: 15
  egg_shards_required: 7
  egg_shards_available: 10
  required_bosses:
    none: 0
    ender_dragon: 1
    wither: 0
    both: 0

---

description: Example of generating multiple worlds. World 3 of 3
name: ExampleFinder
game: ChecksFinder

ChecksFinder: 
  progression_balancing: 50
  accessibilty: items
```

L'exemple ci-dessus générera 3 mondes - un Super Mario 64, un Minecraft et un ChecksFinder. 

