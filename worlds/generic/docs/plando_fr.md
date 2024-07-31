# Guide Plando Archipelago

## Qu'est-ce que Plando ?

Le but des randomiseurs est de mélanger les objets dans un jeu pour offrir une nouvelle expérience. Plando prend ce concept
et le modifie en vous permettant de planifier certains aspects du jeu en plaçant des objets spécifiques à des emplacements précis,
des boss spécifiques dans des salles spécifiques, en éditant du texte pour certains PNJ/panneaux, voire même en imposant
certaines connexions de région. Chacune de ces options sera détaillée séparément en tant que `item plando`, `boss plando`,
`text plando` et `connection plando`. Chaque jeu dans Archipelago prend en charge l'item plando, mais les autres options de plando
ne sont prises en charge que par certains jeux. Actuellement, seul A Link to the Past prend en charge le text et le boss plando.
La prise en charge du connection plando peut varier.

### Activation de Plando

Sur le site web, Plando sera déjà activé. Si vous générez le jeu localement, les fonctionnalités de Plando doivent être activées (opt-in).

* Pour activer Plando, accédez à l'installation d'Archipelago (par défaut : `C:\ProgramData\Archipelago`), ouvrez `host.yaml`
avec un éditeur de texte et trouvez la clé `plando_options`. Les modules Plando disponibles peuvent être activés en les ajoutant
après cela, par exemple `plando_options: bosses, items, texts, connections`.
* Vous pouvez ajouter les modules Plando nécessaires pour vos paramètres à la section `requires` de votre fichier YAML.
Cela générera une erreur si les options nécessaires ne sont pas activées, pour vous assurer d'obtenir les résultats souhaités.
Entrez uniquement les modules Plando que vous utilisez, mais cela devrait ressembler à ceci :

```yaml
  requires: 
    version: current.version.number
    plando: bosses, items, texts, connections
``` 

## Item Plando
Item plando permet à un joueur de placer un objet à un emplacement spécifique ou à des emplacements spécifiques,
ou de placer plusieurs objets dans une liste d'emplacements spécifiques, que ce soit dans son propre jeu
ou dans le jeu d'un autre joueur.

* Les options pour item plando sont `from_pool`, `world`, `percentage`, `force`, `count`, et soit `item` et
  `location`, ou `items` et `locations`.
    * `from_pool` détermine si l'objet doit être pris *du* stock d'objets ou *ajouté* à celui-ci. Cela peut être true ou
      false et par défaut à true s'il est omis.
    * `world` est le monde cible pour placer l'objet.
        * Cela est ignoré s'il n'y a qu'un seul monde généré.
        * Peut être un nombre, un nom, true, false, null, ou une liste. false est la valeur par défaut.
            * Si un nombre est utilisé, cela cible cet emplacement ou le numéro de joueur dans le MultiWorld.
            * Si un nom est utilisé, cela ciblera un monde avec ce nom de joueur.
            * Si c'est true, cela sera un monde de n'importe quel joueur sauf le vôtre.
            * Si c'est false, cela ciblera votre propre monde.
            * Si c'est null, cela ciblera un monde aléatoire dans le MultiWorld.
            * Si une liste de noms est utilisée, cela ciblera les jeux avec les noms de joueurs spécifiés.
    * `force` détermine si le générateur échouera si l'objet ne peut pas être placé à l'emplacement. Cela peut être true, false,
      ou silencieux. Silencieux est la valeur par défaut.
        * Si true, l'objet doit être placé et le générateur générera une erreur s'il ne peut pas le faire.
        * Si false, le générateur générera un avertissement si le placement ne peut pas être effectué mais continuera à générer.
        * Si défini sur silencieux et le placement échoue, il sera ignoré complètement.
    * `percentage` est le pourcentage de chance que le bloc pertinent soit déclenché. Cela peut être n'importe quelle valeur de 0 à 100 et
      par défaut à 100 s'il est omis.
    * Placement unique : lorsque vous utilisez un bloc plando pour placer un seul objet à un emplacement unique.
        * `item` est l'objet que vous souhaitez placer et `location` est l'emplacement où le placer.
    * Placement multiple utilise un bloc plando pour placer plusieurs objets dans plusieurs emplacements jusqu'à ce que l'une des listes soit épuisée.
        * `items` définit les objets à utiliser, chacun avec un nombre pour la quantité. Utiliser `true` au lieu d'un nombre utilise autant d'exemplaires de cet objet que possible dans votre pool d'objets.
        * `locations` est une liste d'emplacements possibles où ces objets peuvent être placés.
            * Certains noms de groupes d'emplacements spéciaux peuvent être spécifiés :
                * `early_locations` ajoutera tous les emplacements de la sphère 1 (emplacements logiquement atteignables uniquement avec votre inventaire de départ)
                * `non_early_locations` ajoutera tous les emplacements au-delà de la sphère 1 (emplacements qui nécessitent de trouver au moins un objet avant de devenir logiquement atteignables)
        * En utilisant la méthode de placement multiple, les placements sont choisis de manière aléatoire.

    * `count` peut être utilisé pour définir le nombre maximum d'objets placés à partir du bloc. La valeur par défaut est 1 si `item` est utilisé et false si `items` est utilisé.
        * Si un nombre est utilisé, il essaiera de placer ce nombre d'objets.
        * Si défini sur false, il essaiera de placer autant d'objets que possible à partir du bloc.
        * Si `min` et `max` sont définis, il essaiera de placer un nombre d'objets entre ces deux nombres au hasard.


### Objets et Emplacements Disponibles

Une liste de tous les objets et emplacements disponibles se trouve dans le [datapackage du site web](/datapackage). Les objets et emplacements se trouvent dans les sections `"item_name_to_id"` et `"location_name_to_id"` du jeu. Vous n'avez pas besoin des guillemets, mais le nom doit être saisi de

 la même manière qu'il apparaît sur cette page et est sensible à la casse.

### Exemples

```yaml
plando_items:
  # example block 1 - Timespinner
  - item:
      Empire Orb: 1
      Radiant Orb: 1
    location: Starter Chest 1
    from_pool: true
    world: true
    percentage: 50

  # example block 2 - Ocarina of Time
  - items:
      Kokiri Sword: 1
      Biggoron Sword: 1
      Bow: 1
      Magic Meter: 1
      Progressive Strength Upgrade: 3
      Progressive Hookshot: 2
    locations:
      - Deku Tree Slingshot Chest
      - Dodongos Cavern Bomb Bag Chest
      - Jabu Jabus Belly Boomerang Chest
      - Bottom of the Well Lens of Truth Chest
      - Forest Temple Bow Chest
      - Fire Temple Megaton Hammer Chest
      - Water Temple Longshot Chest
      - Shadow Temple Hover Boots Chest
      - Spirit Temple Silver Gauntlets Chest
    world: false

  # example block 3 - Slay the Spire
  - items:
      Boss Relic: 3
    locations:
      - Boss Relic 1
      - Boss Relic 2
      - Boss Relic 3

  # example block 4 - Factorio
  - items:
      progressive-electric-energy-distribution: 2
      electric-energy-accumulators: 1
      progressive-turret: 2
    locations:
      - military
      - gun-turret
      - logistic-science-pack
      - steel-processing
    percentage: 80
    force: true

# example block 5 - Secret of Evermore
  - items:
      Levitate: 1
      Revealer: 1
      Energize: 1
    locations:
      - Master Sword Pedestal
      - Boss Relic 1
    world: true
    count: 2

# example block 6 - A Link to the Past
  - items:
      Progressive Sword: 4
    world:
      - BobsSlaytheSpire
      - BobsRogueLegacy
    count:
      min: 1
      max: 4
```
1. Ce bloc a une probabilité de 50% de se produire, et s'il se produit, il placera soit Empire Orb, soit Radiant Orb dans le Coffre de départ 1 d'un autre joueur et retirera l'objet choisi du stock d'objets.
2. Ce bloc sera toujours déclenché et placera les swords, bow, magic meter, strength upgrades, and hookshots dans les coffres majeurs de donjon du joueur.
3. Ce bloc sera toujours déclenché et verrouillera les boss relics sur les boss.
4. Ce bloc a une probabilité de 80% de se produire, et lorsqu'il se produit, il placera tous sauf 1 des objets de manière aléatoire parmi les quatre emplacements choisis ici.
5. Ce bloc sera toujours déclenché et tentera de placer au hasard 2 des objets Levitate, Revealer et Energize dans les Master Sword Pedestals ou un emplacement Boss Relic d'autres joueurs.
6. Ce bloc sera toujours déclenché et tentera de placer un nombre aléatoire, entre 1 et 4, progressive swords dans n'importe quel emplacement des jeux nommés BobsSlaytheSpire et BobsRogueLegacy.

## Boss Plando

Cette fonction est actuellement supportée uniquement par A Link to the Past et Kirby's Dream Land 3. Le boss plando permet à un joueur de placer un 
un boss donné dans une arène. 
Des informations plus spécifiques sur le Boss Plando de A Link to the Past est disponibles sur la page  [Le guide plando](/tutorial/A%20Link%20to%20the%20Past/plando/en#connections).

Le Boss plando prend en compte une liste d'instructions pour placer des boss, séparées par un point-virgule `;`.
Il existe trois types de placement : direct, complet et aléatoire.
* Le placement direct prend une arène et un boss, et place le boss dans cette arène.
  * `Palais de l'Est-Trinexx`
* Le placement complet prend un boss et le place dans autant d'arènes restantes que possible.
  * Roi Dedede
* Aléatoire remplit toutes les arènes restantes en utilisant l'option de shuffle du boss, typiquement à utiliser comme dernière instruction.
  * `full`

### Exemples

```yaml
A Link to the Past:
  boss_shuffle:
    # Basic boss shuffle, but prevent Trinexx from being outside Turtle Rock
    Turtle Rock-Trinexx;basic: 1
    # Place as many Arrghus as possible, then let the rest be random
    Arrghus;chaos: 1
    
Kirby's Dream Land 3:
  boss_shuffle:
    # Ensure Iceberg's boss will be King Dedede, but randomize the rest
    Iceberg-King Dedede;full: 1
    # Have all bosses be Whispy Woods
    Whispy Woods: 1
    # Ensure Ripple Field's boss is Pon & Con, but let the method others
    # are placed with be random
    Ripple Field-Pon & Con;random: 1
```

## Text Plando

Étant donné que cela est actuellement pris en charge uniquement par A Link to the Past,
au lieu de trouver une explication ici, veuillez vous référer au guide pertinent : [Guide Plando A Link to the Past](/tutorial/A%20Link%20to%20the%20Past/plando/en)

## Connections Plando

Cette fonctionnalité n'est actuellement prise en charge que par quelques jeux, dont A Link to the Past, Minecraft et Ocarina of Time.
Comme la façon dont ces jeux interagissent avec leurs connexions est différente, seules les bases sont expliquées ici.
Des informations plus spécifiques sur le Connections Plando de A Link to the Past est disponibles sur la page  [Le guide plando](/tutorial/A%20Link%20to%20the%20Past/plando/en#connections).
* Les options pour les connexions sont `percentage`, `entrance`, `exit` et `direction`. Chacune de ces options prend en charge des sous-poids.
* `percentage` est la probabilité de cette connexion de 0 à 100 et par défaut à 100.
* Chaque connexion a une `entrance` et une `exit`. Celles-ci peuvent être déliées comme dans le mélange d'entrées d'insanité d'A Link to the Past.
* `direction` peut être `both`, `entrance` ou `exit` et détermine dans quelle direction cette connexion fonctionnera.

[Connexions A Link to the Past](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/alttp/EntranceShuffle.py#L3852)

[Connexions Minecraft](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/minecraft/Regions.py#L62)

### Exemples

```yaml
plando_connections:
  # example block 1 - A Link to the Past
  - entrance: Cave Shop (Lake Hylia)
    exit: Cave 45
    direction: entrance
  - entrance: Cave 45
    exit: Cave Shop (Lake Hylia)
    direction: entrance
  - entrance: Agahnims Tower
    exit: Old Man Cave Exit (West)
    direction: exit

  # example block 2 - Minecraft
  - entrance: Overworld Structure 1
    exit: Nether Fortress
    direction: both
  - entrance: Overworld Structure 2
    exit: Village
    direction: both
```
1. Ces connexions sont désolidarisées, donc entrer dans le Lake Hylia Cave Shop vous mènera à l'intérieur
de la Cave 45, et lorsque vous quitterez l'intérieur, vous sortirez sur la corniche de la Cave 45.
Entrer dans l'entrée de la Cave 45 vous conduira ensuite au Lake Hylia Cave Shop.
Entrer dans l'entrée de la Old Man Cave et de la Agahnims Tower vous conduira tous deux à leurs emplacements normaux,
mais sortir de la Old Man Cave vous fera sortir à la Agahnims Tower.
2. Cela forcera une Nether Fortress et un Village à être les structures de l'Overworld pour votre jeu.
Notez que pour que le plan de connexion Minecraft fonctionne, le mélange des structures doit être activé.