# Adding Games

Adding a new game to Archipelago has two major parts:

* Game Modification to communicate with Archipelago server (hereafter referred to as "client")
* Archipelago Generation and Server integration plugin (hereafter referred to as "world")

This document will attempt to illustrate the bare minimum requirements and expectations of both parts of a new world
integration. As game modification wildly varies by system and engine, and has no bearing on the Archipelago protocol,
it will not be detailed here.

## Client

The client is an intermediary program between the game and the Archipelago server. This can either be a direct
modification to the game, an external program, or both. This can be implemented in nearly any modern language, but it
must fulfill a few requirements in order to function as expected. The specific requirements the game client must follow
to behave as expected are:

* Handle both secure and unsecure websocket connections
* Detect and react when a location has been "checked" by the player by sending a network packet to the server
* Receive and parse network packets when the player receives an item from the server, and reward it to the player on
demand
  * **Any** of your items can be received any number of times, up to and far surpassing those that the game might
normally expect from features such as starting inventory, item link replacement, or item cheating
  * Players and the admin can cheat items to the player at any time with a server command, and these items may not have
a player or location attributed to them
* Be able to change the port for saved connection info
  * Rooms hosted on the website attempt to reserve their port, but since there are a limited number of ports, this
privilege can be lost, requiring the room to be moved to a new port
* Reconnect if the connection is unstable and lost while playing
* Keep an index for items received in order to resync. The ItemsReceived Packets are a single list with guaranteed 
order.
* Receive items that were sent to the player while they were not connected to the server
  * The player being able to complete checks while offline and sending them when reconnecting is a good bonus, but not 
strictly required
* Send a status update packet alerting the server that the player has completed their goal

Libraries for most modern languages and the spec for various packets can be found in the
[network protocol](/docs/network%20protocol.md) API reference document.

## World

The world is your game integration for the Archipelago generator, webhost, and multiworld server. It contains all the
information necessary for creating the items and locations to be randomized, the logic for item placement, the 
datapackage information so other game clients can recognize your game data, and documentation. Your world must be
written as a Python package to be loaded by Archipelago. This is currently done by creating a fork of the Archipelago
repository and creating a new world package in `/worlds/`. A bare minimum world implementation must satisfy the 
following requirements:

* A folder within `/worlds/` that contains an `__init__.py`
* A `World` subclass where you create your world and define all of its rules
* A unique game name
* For webhost documentation and behaviors, a `WebWorld` subclass that must be instantiated in the `World` class 
definition
  * The game_info doc must follow the format `{language_code}_{game_name}.md`
* A mapping for items and locations defining their names and ids for clients to be able to identify them. These are 
`item_name_to_id` and `location_name_to_id`, respectively.
* Create an item when `create_item` is called both by your code and externally
* An `options_dataclass` defining the options players have available to them
* A `Region` for your player with the name "Menu" to start from
* Create a non-zero number of locations and add them to your regions
* Create a non-zero number of items **equal** to the number of locations and add them to the multiworld itempool
* All items submitted to the multiworld itempool must not be manually placed by the World. If you need to place specific 
items, there are multiple ways to do so, but they should not be added to the multiworld itempool.

Notable caveats:
* The "Menu" region will always be considered the "start" for the player
* The "Menu" region is *always* considered accessible; i.e. the player is expected to always be able to return to the
start of the game from anywhere
* When submitting regions or items to the multiworld (multiworld.regions and multiworld.itempool respectively), use 
`append`, `extend`, or `+=`. **Do not use `=`**
* Regions are simply containers for locations that share similar access rules. They do not have to map to 
concrete, physical areas within your game and can be more abstract like tech trees or a questline.

The base World class can be found in [AutoWorld](/worlds/AutoWorld.py). Methods available for your world to call during
generation can be found in [BaseClasses](/BaseClasses.py) and [Fill](/Fill.py). Some examples and documentation 
regarding the API can be found in the [world api doc](/docs/world%20api.md).
Before publishing, make sure to also check out [world maintainer.md](/docs/world%20maintainer.md).
