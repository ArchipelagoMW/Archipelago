# Advanced Game Options Guide


The Archipelago system generates games using player configuration files as input. Generally these are going to be
YAML files and each player will have one of these containing their custom settings for the randomized game they want to play.
On the website when you customize your settings from one of the game player settings pages which you can reach from the
[supported games page](/games). Clicking on the export settings button at the bottom will provide you with a pre-filled out
YAML with your options. The player settings page also has an option to download a fully filled out yaml containing every
option with every available setting for the available options.

## YAML Formatting
YAML files are a format of <span data-tooltip="Allegedly.">human-readable</span> markup config files. The basic syntax
of a yaml file will have `root` and then different levels of `nested` text that the generator "reads" in order to determine
your settings. To nest text, the correct syntax is **two spaces over** from its root option. A YAML file can be edited
with whatever text editor you choose to use though I personally recommend that you use [Sublime Text](https://www.sublimetext.com/).
This program out of the box supports the correct formatting for the YAML file, so you will be able to tab and get proper
highlighting for any potential errors made while editing the file. If using any other text editor such as Notepad or
Notepad++ whenever you move to nest an option that it is done with two spaces and not tabs. 

Typical YAML format will look as follows:
```yaml
root_option:
  nested_option_one:
    option_one_setting_one: 1
    option_one_setting_two: 0
  nested_option_two:
    option_two_setting_one: 14
    option_two_setting_two: 43
```

In Archipelago YAML options are always written out in full lowercase with underscores separating any words. The numbers
following the colons here are weights. The generator will read the weight of every option the roll that option that many
times, the next option as many times as its numbered and so forth. For the above example `nested_option_one` will have
`option_one_setting_one` 1 time and `option_one_setting_two` 0 times so `option_one_setting_one` is guaranteed to occur.
For `nested_option_two`, `option_two_setting_one` will be rolled 14 times and `option_two_setting_two` will be rolled 43
times against each other. This means `option_two_setting_two` will be more likely to occur but it isn't guaranteed adding
more randomness and "mystery" to your settings. Every configurable setting supports weights.

### Root Options
Currently there are only a few options that are root options. Everything else should be nested within one of these root
options or in some cases nested within other nested options. The only options that should exist in root are `description`,
`name`, `game`, `requires`, `accessibility`, `progression_balancing`, `triggers`, and the name of the games you want 
settings for.
* `description` is ignored by the generator and is simply a good way for you to organize if you have multiple files using
this to detail the intention of the file.
* `name` is the player name you would like to use and is used for your slot data to connect with most games. This can also
be filled with multiple names each having a weight to it.
* `game` is where either your chosen game goes or if you would like can be filled with multiple games each with different
weights.
* `requires` details different requirements from the generator for the YAML to work as you expect it to. Generally this
is good for detailing the version of Archipelago this YAML was prepared for as if it is rolled on an older version may be
missing settings and as such will not work as expected. If any plando is used in the file then requiring it here to ensure
it will be used is good practice.
* `accessibility` determines the level of access to the game the generation will expect you to have in order to reach your
completion goal. This supports `items`, `locations`, and `none` and is set to `locations` by default.
  * `items` will guarantee you can acquire all items in your world but may not be able to access all locations. This mostly
comes into play if there is any entrance shuffle in the seed as locations without items in them can be placed in areas
that make them unreachable.
  * `none` will only guarantee that the seed is beatable. You will be guaranteed able to finish the seed logically but
may not be able to access all locations or acquire all items. A good example of this is having a big key in the big chest
in a dungeon in ALTTP making it impossible to get and finish the dungeon.
* `progression_balancing` is a system the Archipelago generator uses to try and reduce "BK mode" as much as possible. This
primarily involves moving necessary progression items into earlier logic spheres to make the games more accessible so that
players almost always have something to do. This can be turned `on` or `off` and is `on` by default.
* `triggers` is one of the more advanced options that allows you to create conditional adjustments. You can read more
about this [here](/tutorial/archipelago/triggers/en).

### Game Options

One of your root settings will be the name of the game you would like to populate with settings in the format
`GameName`. since it is possible to give a weight to any option it is possible to have one file that can generate a seed
for you where you don't know which game you'll play. For these cases you'll want to fill the game options for every game
that can be rolled by these settings. If a game can be rolled it **must** have a settings section even if it is empty.

#### Universal Game Options

Some options in Archipelago can be used by every game but must still be placed within the relevant game's section.
Currently, these options are `start_inventory`, `start_hints`, `local_items`, `non_local_items`, `start_location_hints`, 
`exclude_locations`, and various [plando options](/tutorial/archipelago/plando/en).
* `start_inventory` will give any items defined here to you at the beginning of your game. The format for this must be
the name as it appears in the game files and the amount you would like to start with. For example `Rupees(5): 6` which
will give you 30 rupees.
* `start_hints` gives you free server hints for the defined item/s at the beginning of the game allowing you to hint for
the location without using any hint points.
* `local_items` will force any items you want to be in your world instead of being in another world.
* `non_local_items` is the inverse of `local_items` forcing any items you want to be in another world and won't be located
in your own.
* `start_location_hints` allows you to define a location which you can then hint for to find out what item is located in
it to see how important the location is.
* `exclude_locations` lets you define any locations that you don't want to do and during generation will force a "junk"
item which isn't necessary for progression to go in these locations.

### Example

```yaml

description: An example using various advanced options
name: Example Player
game: A Link to the Past
requires: 
  version: 0.2.0
accessibility: none
progression_balancing: on
A Link to the Past:
  smallkey_shuffle:
    original_dungeon: 1
    any_world: 1
  start_inventory:
    Pegasus Boots: 1
    Bombs (3): 2
  start_hints:
    - Hammer
  local_items:
    - Bombos
    - Ether
    - Quake
  non_local_items:
    - Moon Pearl
  start_location_hints:
    - Spike Cave
  exclude_locations:
    - Cave 45
triggers:
  - option_category: A Link to the Past
    option_name: smallkey_shuffle
    option_result: any_world
    options:
      A Link to the Past:
        bigkey_shuffle: any_world
        map_shuffle: any_world
        compass_shuffle: any_world
```

#### This is a fully functional yaml file that will do all the following things:
* `description` gives us a general overview so if we pull up this file later we can understand the intent.
* `name` is `Example Player` and this will be used in the server console when sending and receiving items.
* `game` is set to `A Link to the Past` meaning that is what game we will play with this file.
* `requires` is set to require release version 0.2.0 or higher.
* `accesibility` is set to `none` which will set this seed to beatable only meaning some locations and items may be
completely inaccessible but the seed will still be completable.
* `progression_balancing` is set on meaning we will likely receive important items earlier increasing the chance of having
things to do.
* `A Link to the Past` defines a location for us to nest all the game options we would like to use for our game `A Link to the Past`.
* `smallkey_shuffle` is an option for A Link to the Past which determines how dungeon small keys are shuffled. In this example
we have a 1/2 chance for them to either be placed in their original dungeon and a 1/2 chance for them to be placed anywhere
amongst the multiworld.
* `start_inventory` defines an area for us to determine what items we would like to start the seed with. For this example
we have:
  * `Pegasus Boots: 1` which gives us 1 copy of the Pegasus Boots
  * `Bombs (3)` gives us 2 packs of 3 bombs or 6 total bombs
* `start_hints` gives us a starting hint for the hammer available at the beginning of the multiworld which we can use with no cost.
* `local_items` forces the `Bombos`, `Ether`, and `Quake` medallions to all be placed within our own world, meaning we
have to find it ourselves.
* `non_local_items` forces the `Moon Pearl` to be placed in someone else's world, meaning we won't be able to find it.
* `start_location_hints` gives us a starting hint for the `Spike Cave` location available at the beginning of the multiworld
that can be used for no cost.
* `exclude_locations` forces a not important item to be placed on the `Cave 45` location.
* `triggers` allows us to define a trigger such that if our `smallkey_shuffle` option happens to roll the `any_world`
result it will also ensure that `bigkey_shuffle`, `map_shuffle`, and `compass_shuffle` are also forced to the `any_world`
result.