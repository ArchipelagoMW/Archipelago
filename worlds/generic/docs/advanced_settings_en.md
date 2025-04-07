# Advanced YAML Guide
This guide covers more the more advanced options available in YAML files. This guide is intended for the user who plans
to edit their YAML file manually. This guide should take about 10 minutes to read.

If you would like to generate a basic, fully playable YAML without editing a file, then visit the options page for the
game you intend to play.

The options page can be found on the supported games page, just click the "Options Page" link under the name of the
game you would like.

* Supported games page: [Archipelago Games List](/games)

Clicking on the "Export Options" button at the bottom-left will provide you with a pre-filled YAML with your options.
The player options page also has a link to download a full template file for that game which will have every option
possible for the game including some that don't display correctly on the site.

## YAML Overview

The Archipelago system generates games using player configuration files as input. These are going to be YAML files and
each world will have one of these containing their custom options for the game that world will play.

## YAML Formatting

YAML files are a format of human-readable config files. The basic syntax of a yaml file will have a `root` node and then
different levels of `nested` nodes that the generator reads in order to determine your options.

To nest text, the correct syntax is to indent **two spaces over** from its root option. A YAML file can be edited with
whatever text editor you choose to use though I personally recommend that you use Sublime Text. Sublime text
website: [SublimeText Website](https://www.sublimetext.com)

This program out of the box supports the correct formatting for the YAML file, so you will be able to use the tab key
and get proper highlighting for any potential errors made while editing the file. If using any other text editor you
should ensure your indentation is done correctly with two spaces. After editing your YAML file, you can validate it at
the website's [validation page](/check).

A typical YAML file will look like:

```yaml
root_option:
  nested_option_one:
    option_one_setting_one: 1
    option_one_setting_two: 0
  nested_option_two:
    option_two_setting_one: 14
    option_two_setting_two: 43
```

In Archipelago, YAML options are always written out in full lowercase with underscores separating any words. The numbers
following the colons here are weights. The generator will read the weight of every option, then roll that option that
many times, the next option as many times as its numbered and so forth.

For the above example `nested_option_one` will have `option_one_setting_one` 1 time and `option_one_setting_two` 0 times
so `option_one_setting_one` is guaranteed to occur.

For `nested_option_two`, `option_two_setting_one` will be rolled 14 times and `option_two_setting_two` will be rolled 43
times against each other. This means `option_two_setting_two` will be more likely to occur, but it isn't guaranteed,
adding more randomness and "mystery" to your options. Every configurable setting supports weights.

## Root Options

Currently, there are only a few options that are root options. Everything else should be nested within one of these root
options or in some cases nested within other nested options. The only options that should exist in root
are `description`, `name`, `game`, `requires`, and the name of the games you want options for.

* `description` is ignored by the generator and is simply a good way for you to organize if you have multiple files
  using this to detail the intention of the file.

* `name` is the player name you would like to use and is used for your slot data to connect with most games. This can
  also be filled with multiple names each having a weight to it. Names can also contain certain keywords, surrounded by
  curly-braces, which will be replaced on generation with a number:
  
  * `{player}` will be replaced with the player's slot number.
  * `{PLAYER}` will be replaced with the player's slot number if that slot number is greater than 1, otherwise blank.
  * `{number}` will be replaced with the counter value of the name.
  * `{NUMBER}` will be replaced with the counter value of the name if the counter value is greater than 1, otherwise 
  blank.

* `game` is where either your chosen game goes or, if you would like, can be filled with multiple games each with
  different weights.

* `requires` details different requirements from the generator for the YAML to work as you expect it to. Generally this
  is good for detailing the version of Archipelago this YAML was prepared for. If it is rolled on an older version,
  options may be missing and as such it will not work as expected. If any plando is used in the file then requiring it
  here to ensure it will be used is good practice.

## Game Options

One of your root options will be the name of the game you would like to populate with options. Since it is possible to
give a weight to any option, it is possible to have one file that can generate a seed for you where you don't know which
game you'll play. For these cases you'll want to fill the game options for every game that can be rolled by these
settings. If a game can be rolled it **must** have an options section even if it is empty.

### Universal Game Options

Some options in Archipelago can be used by every game but must still be placed within the relevant game's section.

Currently, these options are `accessibility`, `progression_balancing`, `triggers`, `local_items`, `non_local_items`,
`start_inventory`, `start_hints`, `start_location_hints`, `exclude_locations`, `priority_locations`, `item_links`, and
various plando options.

See the plando guide for more info on plando options. Plando
guide: [Archipelago Plando Guide](/tutorial/Archipelago/plando/en)

* `accessibility` determines the level of access to the game the generation will expect you to have in order to reach
  your completion goal. This supports `full`, `items`, and `minimal` and is set to `full` by default.
    * `full` will guarantee all locations are accessible in your world.
    * `items` will guarantee you can acquire all logically relevant items in your world. Some items, such as keys, may
      be self-locking. This value only exists in and affects some worlds.
    * `minimal` will only guarantee that the seed is beatable. You will be guaranteed able to finish the seed logically
      but may not be able to access all locations or acquire all items. A good example of this is having a big key in
      the big chest in a dungeon in ALTTP making it impossible to get and finish the dungeon.
* `progression_balancing` is a system the Archipelago generator uses to try and reduce
  ["BK mode"](/glossary/en/#burger-king-/-bk-mode)
  as much as possible.
  This primarily involves moving necessary progression items into earlier logic spheres to make the games more
  accessible so that players almost always have something to do. This can be in a range from 0 to 99, and is 50 by
  default. This number represents a percentage of the furthest progressible player.
    * For example: With the default of 50%, if the furthest player can access 40% of their items, the randomizer tries
      to let you access at least 20% of your items. 50% of 40% is 20%.
    * Note that it is not always guaranteed that it will be able to bring you up to this threshold.
* `triggers` is one of the more advanced options that allows you to create conditional adjustments. You can read
  more triggers in the triggers guide. Triggers
  guide: [Archipelago Triggers Guide](/tutorial/Archipelago/triggers/en)
* `local_items` will force any items you want to be in your world instead of being in another world.
* `non_local_items` is the inverse of `local_items`, forcing any items you want to be in another world instead of
  your own.
* `start_inventory` will give any items defined here to you at the beginning of your game. The format for this must be
  the name as it appears in the game files and the amount you would like to start with. For example `Rupees(5): 6` which
  will give you 30 rupees.
* `start_hints` gives you free server hints for the defined items at the beginning of the game, allowing you to hint for
  the location without using any hint points.
* `start_location_hints` is the same as `start_hints` but for locations, allowing you to hint for the item contained
  there without using any hint points.
* `exclude_locations` lets you define any locations that you don't want to do and prevents items classified as
  "progression" or "useful" from being placed on them.
* `priority_locations` lets you define any locations that you want to do and forces a progression item into these
  locations.
* `item_links` allows players to link their items into a group with the same item link name and game. The items declared
  in `item_pool` get combined and when an item is found for the group, all players in the group receive it. Item links
  can also have local and non-local items, forcing the items to either be placed within the worlds of the group or in
  worlds outside the group. If players have a varying amount of a specific item in the link, the lowest amount from the
  players will be the amount put into the group.

### Random numbers

Options taking a choice of a number can also use a variety of `random` options to choose a number randomly.

* `random` will choose a number allowed for the setting at random
* `random-low` will choose a number allowed for the setting at random, but will be weighted towards lower numbers
* `random-middle` will choose a number allowed for the setting at random, but will be weighted towards the middle of the
  range
* `random-high` will choose a number allowed for the setting at random, but will be weighted towards higher numbers
* `random-range-#-#` will choose a number at random from between the specified numbers. For example `random-range-40-60`
  will choose a number between 40 and 60
* `random-range-low-#-#`, `random-range-middle-#-#`, and `random-range-high-#-#` will choose a number at random from the
  specified numbers, but with the specified weights

### Example

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

#### This is a fully functional yaml file that will do all the following things:

* `description` gives us a general overview so if we pull up this file later we can understand the intent.
* `name` is `Example Player` and this will be used in the server console when sending and receiving items.
* `game` has an equal chance of being either `A Link to the Past` or `Timespinner` with a 10/20 chance for each. This is
  because each game has a weight of 10 and the total of all weights is 20.
* `requires` is set to required release version 0.3.2 or higher.
* `accessibility` for both games is set to `minimal` which will set this seed to beatable only, so some locations and
  items may be completely inaccessible but the seed will still be completable.
* `progression_balancing` for both games is set to 50, the default value, meaning we will likely receive important items
  earlier, increasing the chance of having things to do.
* `A Link to the Past` defines a location for us to nest all the game options we would like to use for our
  game `A Link to the Past`.
* `smallkey_shuffle` is an option for A Link to the Past which determines how dungeon small keys are shuffled. In this
  example we have a 1/2 chance for them to either be placed in their original dungeon and a 1/2 chance for them to be
  placed anywhere amongst the multiworld.
* `crystals_needed_for_gt` determines the number of crystals required to enter the Ganon's Tower entrance. In this
  example a random number will be chosen from the allowed range for this setting (0 through 7) but will be weighted
  towards a lower number.
* `crystals_needed_for_ganon` determines the number of crystals required to beat Ganon. In this example a number between
  1 and 7 will be chosen at random, weighted towards a high number.
* `local_items` forces the `Bombos`, `Ether`, and `Quake` medallions to all be placed within our own world, meaning we
  have to find it ourselves.
* `non_local_items` forces the `Moon Pearl` to be placed in someone else's world, meaning we won't be able to find it.
* `start_inventory` defines an area for us to determine what items we would like to start the seed with. For this
  example we have:
  * `Pegasus Boots: 1` which gives us 1 copy of the Pegasus Boots
  * `Bombs (3): 2` gives us 2 packs of 3 bombs or 6 total bombs
* `start_hints` gives us a starting hint for the hammer available at the beginning of the multiworld which we can use
  with no cost.
* `start_location_hints` gives us a starting hint for the `Spike Cave` location available at the beginning of the
  multiworld that can be used for no cost.
* `exclude_locations` forces a not important item to be placed on the `Cave 45` location.
* `priority_locations` forces a progression item to be placed on the `Link's House` location.
* `item_links`
  * For `A Link to the Past` all players in the `rods` item link group will share their fire and ice rods and the player
    items will be replaced with single rupees. The rupee will also be shared among those players.
  * For `Timespinner` all players in the `TSAll` item link group will share their entire item pool and the `Twin Pyramid
    Key` and `Timespinner Wheel` will be forced among the worlds of those in the group. The `null` replacement item
    will, instead of forcing a specific chosen item, allow the generator to randomly pick a filler item to replace the
    player items.
* `triggers` allows us to define a trigger such that if our `smallkey_shuffle` option happens to roll the `any_world`
  result it will also ensure that `bigkey_shuffle`, `map_shuffle`, and `compass_shuffle` are also forced to the
  `any_world` result. More information on triggers can be found in the
  [triggers guide](/tutorial/Archipelago/triggers/en).


## Generating Multiple Worlds

YAML files can be configured to generate multiple worlds using only one file. This is mostly useful if you are playing
an asynchronous multiworld (shortened to async) and are wanting to submit multiple worlds as they can be condensed into
one file, removing the need to manage separate files if one chooses to do so.  

As a precautionary measure, before submitting a multi-game yaml like this one in a synchronous/sync multiworld, please
confirm that the other players in the multi are OK with what you are submitting, and please be fairly reasonable about
the submission. (i.e. Multiple long games (SMZ3, OoT, HK, etc.) for a game intended to be <2 hrs is not likely considered
reasonable, but submitting a ChecksFinder alongside another game OR submitting multiple Slay the Spire runs is likely
OK)

To configure your file to generate multiple worlds, use 3 dashes `---` on an empty line to separate the ending of one
world and the beginning of another world. You can also combine multiple files by uploading them to the
[validation page](/check).

### Example

```yaml
description: Example of generating multiple worlds. World 1 of 3
name: Mario
game: Super Mario 64
requires:
  version: 0.3.2
Super Mario 64:
  progression_balancing: 50
  accessibility: items
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
  accessibility: items
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
  accessibility: items
```

The above example will generate 3 worlds - one Super Mario 64, one Minecraft, and one ChecksFinder.
 

