# Archipelago Plando Guide

## What is Plando?

The purpose of randomizers is to randomize the items in a game to give a new experience. Plando takes this concept and
changes it up by allowing you to plan out certain aspects of the game by placing certain items in certain locations,
certain bosses in certain rooms, edit text for certain NPCs/signs, or even force certain region connections. Each of
these options are going to be detailed separately as `item plando`, `boss plando`, `text plando`,
and `connection plando`. Every game in Archipelago supports item plando but the other plando options are only supported
by certain games. Currently, only A Link to the Past supports text and boss plando. Support for connection plando may
vary.

### Enabling Plando

On the website, plando will already be enabled. If you will be generating the game locally, plando features must be
enabled (opt-in).

* To opt-in go to the Archipelago installation (default: `C:\ProgramData\Archipelago`), open `host.yaml` with a text
  editor and find the `plando_options` key. The available plando modules can be enabled by adding them after this such
  as
  `plando_options: bosses, items, texts, connections`.
* You can add the necessary plando modules for your settings to the `requires` section of your YAML. Doing so will throw an error if the options that you need to generate properly are not enabled to ensure you will get the results you desire. Only enter in the plando modules that you are using here but it should look like:

```yaml
requires: 
  version: current.version.number
  plando: bosses, items, texts, connections
``` 

## Item Plando
Item plando allows a player to place an item in a specific location or specific locations, or place multiple items into a
list of specific locations both in their own game or in another player's game.

* The options for item plando are `from_pool`, `world`, `percentage`, `force`, `count`, and either `item` and
  `location`, or `items` and `locations`.
    * `from_pool` determines if the item should be taken *from* the item pool or *added* to it. This can be true or
      false and defaults to true if omitted.
    * `world` is the target world to place the item in.
        * It gets ignored if only one world is generated.
        * Can be a number, name, true, false, null, or a list. False is the default.
            * If a number is used, it targets that slot or player number in the multiworld.
            * If a name is used, it will target the world with that player name.
            * If set to true, it will be any player's world besides your own.
            * If set to false, it will target your own world.
            * If set to null, it will target a random world in the multiworld.
            * If a list of names is used, it will target the games with the player names specified.
    * `force` determines whether the generator will fail if the item can't be placed in the location. Can be true, false,
      or silent. Silent is the default.
        * If set to true, the item must be placed and the generator will throw an error if it is unable to do so.
        * If set to false, the generator will log a warning if the placement can't be done but will still generate.
        * If set to silent and the placement fails, it will be ignored entirely.
    * `percentage` is the percentage chance for the relevant block to trigger. This can be any value from 0 to 100 and
      if omitted will default to 100.
    * Single Placement is when you use a plando block to place a single item at a single location.
        * `item` is the item you would like to place and `location` is the location to place it.
    * Multi Placement uses a plando block to place multiple items in multiple locations until either list is exhausted.
        * `items` defines the items to use, each with a number for the amount. Using `true` instead of a number uses however many of that item are in your item pool.
        * `locations` is a list of possible locations those items can be placed in.
            * Some special location group names can be specified:
                * `early_locations` will add all sphere 1 locations (locations logically reachable only with your starting inventory)
                * `non_early_locations` will add all locations beyond sphere 1 (locations that require finding at least one item before they become logically reachable)
        * Using the multi placement method, placements are picked randomly.

    * `count` can be used to set the maximum number of items placed from the block. The default is 1 if using `item` and False if using `items`
        * If a number is used, it will try to place this number of items.
        * If set to false, it will try to place as many items from the block as it can.
        * If `min` and `max` are defined, it will try to place a number of items between these two numbers at random.


### Available Items and Locations

A list of all available items and locations can be found in the [website's datapackage](/datapackage). The items and locations will be in the `"item_name_to_id"` and `"location_name_to_id"` sections of the relevant game. You do not need the quotes but the name must be entered in the same as it appears on that page and is case-sensitive.

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
1. This block has a 50% chance to occur, and if it does, it will place either the Empire Orb or Radiant Orb on another
player's Starter Chest 1 and removes the chosen item from the item pool.
2. This block will always trigger and will place the player's swords, bow, magic meter, strength upgrades, and hookshots
in their own dungeon major item chests.
3. This block will always trigger and will lock boss relics on the bosses.
4. This block has an 80% chance of occurring, and when it does, it will place all but 1 of the items randomly among the
four locations chosen here.
5. This block will always trigger and will attempt to place a random 2 of Levitate, Revealer and Energize into
other players' Master Sword Pedestals or Boss Relic 1 locations.
6. This block will always trigger and will attempt to place a random number, between 1 and 4, of progressive swords
into any locations within the game slots named BobsSlaytheSpire and BobsRogueLegacy.


## Boss Plando

This is currently only supported by A Link to the Past and Kirby's Dream Land 3. Boss plando allows a player to place a 
given boss within an arena. More specific information for boss plando in A Link to the Past can be found in 
its [plando guide](/tutorial/A%20Link%20to%20the%20Past/plando/en).

Boss plando takes in a list of instructions for placing bosses, separated by a semicolon `;`.
There are three types of placement: direct, full, and shuffle.
* Direct placement takes both an arena and a boss, and places the boss into that arena.
  * `Eastern Palace-Trinexx`
* Full placement will take a boss, and place it into as many remaining arenas as possible.
  * `King Dedede`
* Shuffle will fill any remaining arenas using a given boss shuffle option, typically to be used as the last instruction.
  * `full`

### Examples

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

As this is currently only supported by A Link to the Past, instead of finding an explanation here, please refer to the
relevant guide: [A Link to the Past Plando Guide](/tutorial/A%20Link%20to%20the%20Past/plando/en)

## Connection Plando

This is currently only supported by a few games, including A Link to the Past, Minecraft, and Ocarina of Time. As the way that these games interact with their
connections is different, only the basics are explained here. More specific information for connection plando in A Link to the Past can be found in 
its [plando guide](/tutorial/A%20Link%20to%20the%20Past/plando/en#connections).

* The options for connections are `percentage`, `entrance`, `exit`, and `direction`. Each of these options supports
  subweights.
* `percentage` is the percentage chance for this connection from 0 to 100 and defaults to 100.
* Every connection has an `entrance` and an `exit`. These can be unlinked like in A Link to the Past insanity entrance
  shuffle.
* `direction` can be `both`, `entrance`, or `exit` and determines in which direction this connection will operate. `direction` defaults to `both`.

[A Link to the Past connections](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/alttp/EntranceShuffle.py#L3852)

[Minecraft connections](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/minecraft/data/regions.json#L18****)

### Examples

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

1. These connections are decoupled, so going into the Lake Hylia Cave Shop will take you to the inside of Cave 45, and
   when you leave the interior, you will exit to the Cave 45 ledge. Going into the Cave 45 entrance will then take you to
   the Lake Hylia Cave Shop. Walking into the entrance for the Old Man Cave and Agahnim's Tower entrance will both take
   you to their locations as normal, but leaving Old Man Cave will exit at Agahnim's Tower.
2. This will force a Nether fortress and a village to be the Overworld structures for your game. Note that for the
   Minecraft connection plando to work structure shuffle must be enabled.
