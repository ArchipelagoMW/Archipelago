# Adding Games

Like all contributions to Archipelago, New Game implementations should follow the [Contributing](/docs/contributing.md)
guide.

Adding a new game to Archipelago has two major parts:

* Game Modification to communicate with Archipelago server (hereafter referred to as "client")
* Archipelago Generation and Server integration plugin (hereafter referred to as "world")

This document will attempt to illustrate the bare minimum requirements and expectations of both parts of a new world
integration. As game modification wildly varies by system and engine, and has no bearing on the Archipelago protocol,
it will not be detailed here.

## Client

The client is an intermediary program between the game and the Archipelago server. This can either be a direct
modification to the game, an external program, or both. This can be implemented in nearly any modern language, but it
must fulfill a few requirements in order to function as expected. Libraries for most modern languages and the spec for 
various packets can be found in the [network protocol](/docs/network%20protocol.md) API reference document.

### Hard Requirements

In order for the game client to behave as expected, it must be able to perform these functions:

* Handle both secure and unsecure websocket connections
* Reconnect if the connection is unstable and lost while playing
* Be able to change the port for saved connection info
  * Rooms hosted on the website attempt to reserve their port, but since there are a limited number of ports, this
    privilege can be lost, requiring the room to be moved to a new port
* Send a status update packet alerting the server that the player has completed their goal

Regarding items and locations, the game client must be able to handle these tasks:

#### Location Handling

Send a network packet to the server when it detects a location has been "checked" by the player in-game.

* If actions were taken in game that would usually trigger a location check, and those actions can only ever be taken 
  once, but the client was not connected when they happened: The client must send those location checks on connection 
  so that they are not permanently lost, e.g. by reading flags in the game state or save file.

#### Item Handling

Receive and parse network packets from the server when the player receives an item.

* It must reward items to the player on demand, as items can come from other players at any time.
* It must be able to reward copies of an item, up to and beyond the number the game normally expects. This may happen
  due to features such as starting inventory, item link replacement, admin commands, or item cheating. **Any** of 
  your items can be received **any** number of times.
* Admins and players may use server commands to create items without a player or location attributed to them. The
  client must be able to handle these items.
* It must keep an index for items received in order to resync. The ItemsReceived Packets are a single list with a
  guaranteed order.
* It must be able to receive items that were sent to the player while they were not connected to the server.

### Encouraged Features

These are "nice to have" features for a client, but they are not strictly required. It is encouraged to add them 
if possible.

* If your client appears in the Archipelago Launcher, you may define an icon for it that differentiates it from
  other clients. The icon size is 48x48 pixels, but smaller or larger images will scale to that size.

## World

The world is your game integration for the Archipelago generator, webhost, and multiworld server. It contains all the
information necessary for creating the items and locations to be randomized, the logic for item placement, the 
datapackage information so other game clients can recognize your game data, and documentation. Your world must be
written as a Python package to be loaded by Archipelago. This is currently done by creating a fork of the Archipelago
repository and creating a new world package in `/worlds/`. 

The base World class can be found in [AutoWorld](/worlds/AutoWorld.py). Methods available for your world to call 
during generation can be found in [BaseClasses](/BaseClasses.py) and [Fill](/Fill.py). Some examples and documentation 
regarding the API can be found in the [world api doc](/docs/world%20api.md). Before publishing, make sure to also 
check out [world maintainer.md](/docs/world%20maintainer.md).

### Hard Requirements

A bare minimum world implementation must satisfy the following requirements:

* It has a folder with the name of your game (or an abbreviation) under `/worlds/` 
* The `/worlds/{game}` folder contains an `__init__.py`
* Any subfolders within `/worlds/{game}` that contain `*.py` files also contain an `__init__.py` for frozen build 
  packaging
* The game folder has at least one game_info doc named with follow the format `{language_code}_{game_name}.md`
* The game folder has at least one setup doc
* There must be a `World` subclass in your game folder (typically in `/worlds/{game}/__init__.py`) where you create 
  your world and define all of its rules and features

Within the `World` subclass you should also have:

* A [unique game name](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/AutoWorld.py#L260)
* An [instance](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/AutoWorld.py#L295) of a `WebWorld` 
subclass for webhost documentation and behaviors
  * In your `WebWorld`, if you wrote a game_info doc in more than one language, override the list of 
    [game info languages](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/AutoWorld.py#L210) with the 
    ones you include.
  * In your `WebWorld`, override the list of 
    [tutorials](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/AutoWorld.py#L213) with each tutorial
    or setup doc you included in the game folder.
* A mapping for items and locations defining their names and ids for clients to be able to identify them. These are 
  `item_name_to_id` and `location_name_to_id`, respectively.
* An implementation of `create_item` that can create an item when called by either your code or by another process 
  within Archipelago
* At least one `Region` for your player to start from (i.e. the Origin Region)
  * The default name of this region is "Menu" but you may configure a different name with 
    [origin_region_name](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/AutoWorld.py#L298-L299)
* A non-zero number of locations, added to your regions
* A non-zero number of items **equal** to the number of locations, added to the multiworld itempool
  * In rare cases, there may be 0-location-0-item games, but this is extremely atypical.
* A set 
  [completion condition](https://github.com/ArchipelagoMW/Archipelago/blob/main/BaseClasses.py#L77) (aka "goal") for
  the player.
  * Use your player as the index (`multiworld.completion_condition[player]`) for your world's completion goal.

### Encouraged Features

These are "nice to have" features for a world, but they are not strictly required. It is encouraged to add them 
if possible.

* An implementation of
  [get_filler_item_name](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/AutoWorld.py#L473)
  * By default, this function chooses any item name from `item_name_to_id`, so you want to limit it to only the true
    filler items.
* An `options_dataclass` defining the options players have available to them
  * This should be accompanied by a type hint for `options` with the same class name
* A [bug report page](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/AutoWorld.py#L220)
* A list of [option groups](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/AutoWorld.py#L226) 
  for better organization on the webhost
* A dictionary of [options presets](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/AutoWorld.py#L223)
  for player convenience
* A dictionary of [item name groups](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/AutoWorld.py#L273)
  for player convenience
* A dictionary of 
  [location name groups](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/AutoWorld.py#L276)
  for player convenience
  * Other games may also benefit from your name group dictionaries for hints, features, etc.

### Discouraged or Prohibited Behavior

These are behaviors or implementations that are known to cause various issues. Some of these points have notable
workarounds or preferred methods which should be used instead:

* All items submitted to the multiworld itempool must not be manually placed by the World. 
  * If you need to place specific items, there are multiple ways to do so, but they should not be added to the 
    multiworld itempool.
* It is not allowed to use `eval` for most reasons, chiefly due to security concerns. 
* It is discouraged to use PyYAML (i.e. `yaml.load`) directly due to security concerns.
  * When possible, use `Utils.parse_yaml` instead, as this defaults to the safe loader and the faster C parser.
* When submitting regions or items to the multiworld (`multiworld.regions` and `multiworld.itempool` respectively), 
  do **not** use `=` as this will overwrite all elements for all games in the seed.
  * Instead, use `append`, `extend`, or `+=`.

### Notable Caveats

* The Origin Region will always be considered the "start" for the player
* The Origin Region is *always* considered accessible; i.e. the player is expected to always be able to return to the
start of the game from anywhere
* Regions are simply containers for locations that share similar access rules. They do not have to map to 
concrete, physical areas within your game and can be more abstract like tech trees or a questline.
