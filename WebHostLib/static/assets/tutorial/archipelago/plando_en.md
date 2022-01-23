# Archipelago Plando Guide

## What is Plando?

The purposes of randomizers is to randomize the items in a game to give a new experience. Plando takes this concept and
changes it up by allowing you to plan out certain aspects of the game by placing certain items in certain locations,
certain bosses in certain rooms, edit text for certain NPCs/signs, or even force certain region connections. Each of
these options are going to be detailed separately as `item plando`, `boss plando`, `text plando`,
and `connection plando`. Every game in archipelago supports item plando but the other plando options are only supported
by certain games. Currently, Minecraft and LTTP both support connection plando, but only LTTP supports text and boss
plando.

### Enabling Plando

On the website plando will already be enabled. If you will be generating the game locally plando features must be
enabled (opt-in).

* To opt-in go to the archipelago installation (default: `C:\ProgramData\Archipelago`), open the host.yaml with a text
  editor and find the `plando_options` key. The available plando modules can be enabled by adding them after this such
  as
  `plando_options: bosses, items, texts, connections`.
* If you are not the one doing the generation or even if you are you can add to the `requires` section of your yaml so
  that it will throw an error if the options that you need to generate properly are not enabled to ensure you will get
  the results you desire. Only enter in the plando modules that you are using here but it should look like:

```yaml
  requires: 
    version: current.version.number
    plando: bosses, items, texts, connections
``` 

## Item Plando
Item plando allows a player to place an item in a specific location or specific locations, place multiple items into a
list of specific locations both in their own game or in another player's game.

* The options for item plando are `from_pool`, `world`, `percentage`, `force`, `count`, and either item and location, or items
  and locations.
    * `from_pool` determines if the item should be taken *from* the item pool or *added* to it. This can be true or
      false and defaults to true if omitted.
    * `world` is the target world to place the item in.
        * It gets ignored if only one world is generated.
        * Can be a number, name, true, false, null, or a list. False is the default.
            * If a number is used it targets that slot or player number in the multiworld.
            * If a name is used it will target the world with that player name.
            * If set to true it will be any player's world besides your own.
            * If set to false it will target your own world.
            * If set to null it will target a random world in the multiworld.
            * If a list of names is used, it will target the games with the player names specified.
    * `force` determines whether the generator will fail if the item can't be placed in the location can be true, false,
      or silent. Silent is the default.
        * If set to true the item must be placed and the generator will throw an error if it is unable to do so.
        * If set to false the generator will log a warning if the placement can't be done but will still generate.
        * If set to silent and the placement fails it will be ignored entirely.
    * `percentage` is the percentage chance for the relevant block to trigger. This can be any value from 0 to 100 and
      if omitted will default to 100.
    * Single Placement is when you use a plando block to place a single item at a single location.
        * `item` is the item you would like to place and `location` is the location to place it.
    * Multi Placement uses a plando block to place multiple items in multiple locations until either list is exhausted.
        * `items` defines the items to use and a number letting you place multiple of it. You can use true instead of a number to have it use however many of that item are in your item pool.
        * `locations` is a list of possible locations those items can be placed in.
        * Using the multi placement method, placements are picked randomly.
        * Instead of a number, you can use true 
    * `count` can be used to set the maximum number of items placed from the block. The default is 1 if using `item` and False if using `items`
        * If a number is used it will try to place this number of items.
        * If set to false it will try to place as many items from the block as it can.
        * If `min` and `max` are defined, it will try to place a number of items between these two numbers at random


### Available Items

* [A Link to the Past](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/alttp/Items.py#L52)
* [Factorio Non-Progressive](https://wiki.factorio.com/Technologies) Note that these use the *internal names*. For
  example, `advanced-electronics`
* [Factorio Progressive](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/factorio/Technologies.py#L374)
* [Final Fantasy 1](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/ff1/data/items.json)
* [Minecraft](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/minecraft/Items.py#L14)
* [Ocarina of Time](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/oot/Items.py#L61)
* [Risk of Rain 2](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/ror2/Items.py#L8)
* [Rogue Legacy](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/rogue-legacy/Names/ItemName.py)
* [Slay the Spire](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/spire/Items.py#L13)
* [Subnautica](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/subnautica/items.json)
* [Super Metroid](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/sm/variaRandomizer/rando/Items.py#L37) Look for "Name="
* [Timespinner](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/timespinner/Items.py#L11)

### Available Locations

* [A Link to the Past](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/alttp/Regions.py#L429)
* [Factorio](https://wiki.factorio.com/Technologies) Same as items
* [Final Fantasy 1](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/ff1/data/locations.json)
* [Minecraft](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/minecraft/Locations.py#L18)
* [Ocarina of Time](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/oot/LocationList.py#L38)
* [Risk of Rain 2](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/ror2/Locations.py#L17) This is a
  special case. The locations are "ItemPickup[number]" up to the maximum set in the yaml.
* [Rogue Legacy](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/rogue-legacy/Names/LocationName.py)
* [Slay the Spire](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/spire/Locations.py)
* [Subnautica](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/subnautica/locations.json)
* [Super Metroid](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/sm/variaRandomizer/graph/location.py#L132)
* [Timespinner](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/timespinner/Locations.py#L13)

A list of all available items and locations can also be found in the [server's datapackage](/api/datapackage).

### Examples

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
1. This block has a 50% chance to occur, and if it does will place either the Empire Orb or Radiant Orb on another player's
Starter Chest 1 and removes the chosen item from the item pool.
2. This block will always trigger and will place the player's swords, bow, magic meter, strength upgrades, and hookshots
in their own dungeon major item chests.
3. This block will always trigger and will lock boss relics on the bosses.
4. This block has an 80% chance of occurring and when it does will place all but 1 of the items randomly among the four
locations chosen here.
5. This block will always trigger and will attempt to place a random 2 of Levitate, Revealer and Energize into
other players' Master Sword Pedestals or Boss Relic 1 locations.
6. This block will always trigger and will attempt to place a random number, between 1 and 4, of progressive swords
into any locations within the game slots named BobsSlaytheSpire and BobsRogueLegacy


## Boss Plando

As this is currently only supported by A Link to the Past instead of explaining here please refer to the
[relevant guide](/tutorial/zelda3/plando/en)

## Text Plando

As this is currently only supported by A Link to the Past instead of explaining here please refer to the
[relevant guide](/tutorial/zelda3/plando/en)

## Connections Plando

This is currently only supported by Minecraft and A Link to the Past. As the way that these games interact with their
connections is different I will only explain the basics here while more specifics for Link to the Past connection plando
can be found in its plando guide.

* The options for connections are `percentage`, `entrance`, `exit`, and `direction`. Each of these options support
  subweights.
* `percentage` is the percentage chance for this connection from 0 to 100 and defaults to 100.
* Every connection has an `entrance` and an `exit`. These can be unlinked like in A Link to the Past insanity entrance
  shuffle.
* `direction` can be `both`, `entrance`, or `exit` and determines in which direction this connection will operate.

[Link to the Past connections](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/alttp/EntranceShuffle.py#L3852)

[Minecraft connections](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/minecraft/Regions.py#L62)

### Examples

```yaml
plando_connections:
  # example block 1 - Link to the Past
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

1. These connections are decoupled so going into the lake hylia cave shop will take you to the inside of cave 45 and
   when you leave the interior you will exit to the cave 45 ledge. Going into the cave 45 entrance will then take you to
   the lake hylia cave shop. Walking into the entrance for the old man cave and Agahnim's Tower entrance will both take
   you to their locations as normal but leaving old man cave will exit at Agahnim's Tower.
2. This will force a nether fortress and a village to be the overworld structures for your game. Note that for the
   Minecraft connection plando to work structure shuffle must be enabled.
