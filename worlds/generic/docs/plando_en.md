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

For a basic understanding of YAML files, refer to 
[YAML Formatting](/tutorial/Archipelago/advanced_settings/en#yaml-formatting) 
in Advanced Settings.

## Item Plando

Item Plando allows a player to place an item in a specific location or locations, or place multiple items into a list 
of specific locations in their own game and/or in another player's game.

To add item plando to your player yaml, you add them under the `plando_items` block. You should start with `item` if you 
want to do Single Placement, or `items` if you want to do Multi Placement. A list of items can still be defined under 
`item` but only one of them will be chosen at random to be used.

After you define `item/items`, you would define `location` or `locations`, depending on if you want to fill one 
location or many. Note that both `location` and `locations` are optional. A list of locations can still be defined under 
`location` but only one of them will be chosen at random to be used.

You may do any combination of `item/items` and `location/locations` in a plando block, but the block only places items 
in locations **until the shorter of the two lists is used up.**

Once you are satisfied with your first block, you may continue to define ones under the same `plando_items` parent.
Each block can have several different options to tailor it the way you like.

* The `items` section defines the items to use. Each item name can be followed by a colon and a value.
    * A numerical value indicates the amount of that item.
    * A `true` value uses all copies of that item that are in your item pool.

* The `item` section defines a list of items to use, from which one will be chosen at random. Each item name can be 
    followed by a colon and a value. The value indicates the weight of that item being chosen.

* The `locations` section defines possible locations those items can be placed in. Two special location groups exist:
    * `early_locations` will add all sphere 1 locations (locations logically reachable only with your starting 
      inventory).
    * `non_early_locations` will add all locations beyond sphere 1 (locations that require finding at least one item 
      before they become logically reachable).

* `from_pool` determines if the item should be taken *from* the item pool or *created* from scratch.
    * `false`: Create a new item with the same name (the world will determine its properties e.g. classification).
    * `true`: Take the existing item, if it exists, from the item pool. If it does not exist, one will be created from 
      scratch. **(Default)**

* `world` is the target world to place the item in. It gets ignored if only one world is generated.
    * **A number:** Use this slot or player number in the multiworld.
    * **A name:** Use the world with that player name.
    * **A list of names:** Use the worlds with the player names specified.
    * `true`: Locations will be in any player's world besides your own.
    * `false`: Locations will be in your own world. **(Default)**
    * `null`: Locations will be in a random world in the multiworld.

* `force` determines whether the generator will fail if the plando block cannot be fulfilled.
    * `true`: The generator will throw an error if it is unable to place an item.
    * `false`: The generator will log a warning if it is unable to place an item, but it will still generate.
    * `silent`: If the placement fails, it will be ignored entirely. **(Default)**

* `percentage` is the percentage chance for the block to trigger. This can be any integer from 0 to 100. 
    **(Default: 100)**

* `count` sets the number of items placed from the list.
    * **Default: 1 if using `item` or `location`, and `false` otherwise.**
    * **A number:** It will place this number of items.
    * `false`: It will place as many items from the list as it can.
    * **If `min` is defined,** it will place at least `min` many items (can be combined with `max`).
    * **If `max` is defined,** it will place at most `max` many items (can be combined with `min`).

### Available Items and Locations

A list of all available items and locations can be found in the [website's datapackage](/datapackage). The items and 
locations will be in the `"item_name_to_id"` and `"location_name_to_id"` sections of the relevant game. Names are 
case-sensitive. You can also use item groups and location groups that are defined in the datapackage.

## Item Plando Examples
```yaml
 plando_items:
    # Example block - Pokémon Red and Blue
    - items:
        Potion: 3
      locations:
        - "Route 1 - Free Sample Man" 
        - "Mt Moon 1F - West Item"
        - "Mt Moon 1F - South Item"
```
This block will lock 3 Potion items on the Route 1 Pokémart employee and 2 Mt Moon items. Note these are all 
Potions in the vanilla game. The world value has not been specified, so these locations must be in this player's own 
world by default.

```yaml
  plando_items:
  # Example block - A Link to the Past
    - items:
        Progressive Sword: 4
      world:
        - BobsWitness
        - BobsRogueLegacy
      count:
        min: 1
        max: 4
```
This block will attempt to place a random number, between 1 and 4, of Progressive Swords into any locations within the 
game slots named "BobsWitness" and "BobsRogueLegacy."

```yaml
  plando_items:
  # Example block - Secret of Evermore
    - items:
        Levitate: 1
        Revealer: 1
        Energize: 1
      locations:
        - Master Sword Pedestal
        - Desert Discard
      world: true
      count: 2
```
This block will choose 2 from the Levitate, Revealer, and Energize items at random and attempt to put them into the 
locations named "Master Sword Pedestal" and "Desert Discard". Because the world value is `true`, these locations 
must be in other players' worlds.

```yaml
  plando_items:
    # Example block - Timespinner
    - item:
        Empire Orb: 1
        Radiant Orb: 3
      location: Starter Chest 1
      from_pool: false
      world: true
      percentage: 50
```
This block will place a single item, either the Empire Orb or Radiant Orb, on the location "Starter Chest 1". There is
a 25% chance it is Empire Orb, and 75% chance it is Radiant Orb (1 to 3 odds). The world value is `true`, so this 
location must be in another player's world. Because the from_pool value is `false`, a copy of these items is added to 
these locations, while the originals remain in the item pool to be shuffled. Unlike the previous examples, which will 
always trigger, this block only has a 50% chance to trigger.

```yaml
  plando_items:
    # Example block - Factorio
    - items:
        progressive-electric-energy-distribution: 2
        electric-energy-accumulators: 1
        progressive-turret: 2
      locations:
        - AP-1-001
        - AP-1-002
        - AP-1-003
        - AP-1-004
      percentage: 80
      force: true
      from_pool: true
      world: false
```
This block lists 5 items but only 4 locations, so it will place all but 1 of the items randomly among the locations 
chosen here. This block has an 80% chance of occurring. Because force is `true`, the Generator will fail if it cannot
place one of the selected items (not including the fifth item). From_pool and World have been set to their default
values here, but they can be omitted and have the same result: items will be removed from the pool, and the locations
are in this player's own world.

**NOTE:** Factorio's locations are dynamically generated, so the locations listed above may not exist in your game,
they are here for demonstration only.

```yaml
  plando_items:
    # Example block - Ocarina of Time
    - items:
        Biggoron Sword: 1
        Bow: 1
        Magic Meter: 1
        Progressive Strength Upgrade: 3
        Progressive Hookshot: 2
      locations:
        - Dodongos Cavern Bomb Bag Chest
        - Jabu Jabus Belly Boomerang Chest
        - Bottom of the Well Lens of Truth Chest
        - Forest Temple Bow Chest
        - Fire Temple Megaton Hammer Chest
        - Water Temple Longshot Chest
        - Shadow Temple Hover Boots Chest
        - Spirit Temple Silver Gauntlets Chest
      from_pool: false
      
    - item: Kokiri Sword
      location: Deku Tree Slingshot Chest
      from_pool: false
```
The first block will place the player's Biggoron Sword, Bow, Magic Meter, strength upgrades, and hookshots in the 
dungeon major item chests. Because the from_pool value is `false`, a copy of these items is added to these locations, 
while the originals remain in the item pool to be shuffled. The second block will place the Kokiri Sword in the Deku 
Tree Slingshot Chest, again not from the pool.

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

This is currently only supported by a few games, including A Link to the Past and Ocarina of Time. As the way that these games interact with their
connections is different, only the basics are explained here. More specific information for connection plando in A Link to the Past can be found in 
its [plando guide](/tutorial/A%20Link%20to%20the%20Past/plando/en#connections).

* The options for connections are `percentage`, `entrance`, `exit`, and `direction`. Each of these options supports
  subweights.
* `percentage` is the percentage chance for this connection from 0 to 100 and defaults to 100.
* Every connection has an `entrance` and an `exit`. These can be unlinked like in A Link to the Past insanity entrance
  shuffle.
* `direction` can be `both`, `entrance`, or `exit` and determines in which direction this connection will operate. `direction` defaults to `both`.

[A Link to the Past connections](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/alttp/EntranceShuffle.py#L3852)


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

```

1. These connections are decoupled, so going into the Lake Hylia Cave Shop will take you to the inside of Cave 45, and
   when you leave the interior, you will exit to the Cave 45 ledge. Going into the Cave 45 entrance will then take you to
   the Lake Hylia Cave Shop. Walking into the entrance for the Old Man Cave and Agahnim's Tower entrance will both take
   you to their locations as normal, but leaving Old Man Cave will exit at Agahnim's Tower.
