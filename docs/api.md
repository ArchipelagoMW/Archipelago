# Archipelago API

This document tries to explain some internals required to implement a game for
Archipelago's generation and server. Once a seed is generated, a client or mod is 
required to send and receive items between the game and server.

Client implementation is out of scope of this document. Please refer to an
existing game that provides a similar API to yours or read the
[network protocol.md](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/network%20protocol.md)

Archipelago will be abbreviated as "AP" from now on.


## Language

AP uses python3 for generation, server and web host. The seed generation will be
written in python3, the client that connects to the server to sync items can be
in any language that allows using websockets.


## Coding style

AP follows all the PEPs. When in doubt use an IDE with coding style
linter, for example PyCharm Community Edition.


## Docstrings

Docstrings are strings attached to an object in Python that describe what the
object is supposed to be. Certain docstrings will be picked up and used by AP.
They are assigned by writing a string without any assignment right below a
definition. The string must be a triple-quoted string.
Example:
```python
class MyGameWorld(World):
    """This is the description of My Game that will be displayed on the AP
       website."""
```


## Definitions

### World Class

A `World` class is the class with all the specifics of a certain game to be
included. It will be instantiated for each player that rolls a seed for that
game.

### MultiWorld Object

The `MultiWorld` object references the whole multiworld (all items and locations
for all players) and is accessible through `self.world` inside a `World` object.

### Player

The player is just an integer in AP and is accessible through `self.player`
inside a World object.

### Player Options

Players provide customized settings for their World in the form of yamls.
Those are accessible through `self.world.<option_name>[self.player]`. A dict
of valid options has to be provided in `self.options`. Options are automatically
added to the `World` object for easy access.

### World Options

Any AP installation can provide settings for a world, for example a ROM file,
accessible through `Utils.get_options()['<world>_options']['<option>']`.

Users can set those in their `host.yaml` file.

### Locations

Locations are places where items can be located in your game. This may be chests
or boss drops for RPG-like games but could also be progress in a research tree.

Each location has a `name` and an `id` (a.k.a. "code" or "address"), is placed in a
Region and has access rules.
The name needs to be unique in each game, the ID needs to be unique across all
games and is best in the same range as the item IDs.

Special locations with ID `None` can hold events.

### Items

Items are all things that can "drop" for your game. This may be RPG items like
weapons, could as well be technologies you normally research in a research tree.

Each item has a name and an ID (also "code"), an `advancement` flag and will
be assigned to a location when rolling a seed. Advancement items will be
assigned to locations with higher priority and moved around to meet defined
rules and `progression_balancing`.

Special items with ID `None` can mark events (read below).

### Events

Events will mark some progress. You define an event location, an
event item, strap some rules to the location (i.e. hold certain
items) and manually place the event item at the event location.

Events can be used to either simplify the logic or to get better spoiler logs.
Events will show up in the spoiler playthrough but they do not represent actual
items or locations within the game.

There is one special case for events: Victory. To get the win condition to show
up in the spoiler log, you create an event item and place it at an event
location with the `access_rules` for game completion. Once that's done, the
world's win condition can be as simple as checking for that item.

By convention the victory event is called `"Victory"`. It can be placed at one
or more event locations based on player options.

### Regions

Regions are logical groups of locations that share some common access rules. If
location logic is written from scratch, using regions greatly simplifies the
definition and allow to somewhat easily implement things like entrance
randomizer in logic.

Regions have a list called `exits` which are `Entrance` objects representing transitions to other regions.

There has to be one special region "Menu" from which the logic unfolds. AP
assumes that a player will always be able to return to the "Menu" region by
resetting the game ("Save and quit").

### Entrances

An `Entrance` connects to a region, is assigned to region's exits and has rules
to define if it and thus the connected region is accessible.
They can be static (regular logic) or be defined/connected during generation
(entrance randomizer).

### Access Rules

An access rule is a function that returns `True` or `False` for a `Location` or `Entrance` based
on the the current `state` (items that can be collected).

### Item Rules

An item rule is a function that returns `True` or `False` for a `Location` based
on a single item. It can be used to reject placement of an item there.

### Plando

Plando allows a player to place certain items in certain locations through their
player options. While specifics are not covered here, plando is automatically
possible by providing a complete world with a working create_item method.


## Implementation

### Your World

Your world lives in `world/[world_name]/__init__.py` and is a class that
inherits from `..AutoWorld.World`. The generation progress will automatically
pick it up.

### Requirements

If your world needs specific python packages, they can be listed in
`world/[world_name]/requirements.txt`.
See [pip documentation](https://pip.pypa.io/en/stable/cli/pip_install/#requirements-file-format)

### Relative Imports

AP will only import the `__init__.py`. Depending on code size it makes sense to
use multiple files and use relative imports to access them.

e.g. `from .Options import mygame_options` from your `__init__.py` will load
`world/[world_name]/Options.py` and make its `mygame_options` accesible.

When imported names pile up it may be easier to use `from . import Options`
and access the variable as `Options.mygame_options`.

### Your Item Type

Each world uses its own subclass of `BaseClasses.Item`. The constuctor can be
overridden to attach additional data to it, e.g. "price in shop".
Since the constructor is only ever called from your code, you can add whatever
arguments you like to the constructor.

In its simplest form we only set the game name and use the default constuctor
```python
from BaseClasses import Item

class MyGameItem(Item):
    game: str = "My Game"
```
By convention this class definition will either be placed in your `__init__.py`
or your `Items.py`. For a more elaborate example see `worlds/oot/Items.py`.

### Your location type

The same we have done for items above, we will do for locations
```python
from BasClasses import Location

class MyGameLocation(Location):
    game: str = "My Game"
```
in your `__init__.py` or your `Locations.py`.

**FIXME**: Is setting Location.event actually required? Minecraft and OoT
do that. Factorio does not. What's the goal of doing that? When factorio places
a locked item this will do Location.event = item.advancement.

### Options

By convention options are defined in `Options.py` and will be used when parsing
the players' yaml files.

Each option has its own class, inherits from a base option type, has a docstring 
to describe it and a `displayname` property for display on the website.

The actual name as used in the yaml is defined in a dict[str, Option], that is
assigned to the world.

Common option types are `Toggle`, `DefaultOnToggle`, `Choice`, `Range`. For more see
`Options.py` in AP's base directory.

#### Toggle, DefaultOnToggle

Those don't need any additional properties defined. After parsing the option,
its `value` will either be True or False.

#### Range

Define properties `range_start`, `range_end` and `default`. Ranges will be
displayed as sliders on the website and can be set to random in the yaml.

#### Choice

Choices are like toggles, but have more options than just True and False.
Define a property `option_<name> = <number>` per selectable value and
`default = <number>` to set the default selection. Aliases can be set by
defining a property `alias_<name> = <same number>`.

One special case where aliases are required is when option name is `yes`, `no`,
`on` or `off` because they parse to `True` or `False`:
```python
option_off = 0
option_on = 1
option_some = 2
alias_false = 0
alias_true = 1
default = 0
```

#### Sample
```python
# Options.py

from Options import Toggle, Range, Choice
import typing

class Difficulty(Choice):
    """Sets overall game difficulty."""
    displayname = "Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    alias_beginner = 0  # same as easy
    alias_expert = 2  # same as hard
    default = 1  # default to normal

class FinalBossHP(Range):
    """Sets the HP of the final boss"""
    displayname = "Final Boss HP"
    range_start = 100
    range_end = 10000
    default = 2000

class FixXYZGlitch(Toggle):
    """Fixes ABC when you do XYZ"""
    displayname = "Fix XYZ Glitch"

# By convention we call the options dict variable `<world>_options`.
mygame_options: typing.Dict[str, type(Option)] = {
    "difficulty": Difficulty,
    "final_boss_hp": FinalBossHP,
    "fix_xyz_glitch": FixXYZGlitch
}
```
```python
# __init__.py

from ..AutoWorld import World
from .Options import mygame_options  # import the options dict

class MyGameWorld(World):
    #...
    options = mygame_options  # assign the options dict to the world
    #...
```
    
### Local or Remote

A world with `remote_items` set to `True` gets all items items from the server
and no item from the local game. So for an RPG opening a chest would not add
any item to your inventory, instead the server will send you what was in that
chest. The advantage is that a generic mod can be used that does not need to
know anything about the seed.

A world with `remote_items` set to `False` will locally reward its local items.
For console games this can remove delay and make script/animation/dialog flow
more natural. These games typically have been edited to 'bake in' the items.

### A World Class Skeleton

```python
# world/mygame/__init__.py

from .Options import mygame_options  # the options we defined earlier
from .Items import mygame_items  # data used below to add items to the World
from .Locations import mygame_locations  # same as above
from ..AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item
from Utils import get_options, output_path

class MyGameItem(Item):  # or from Items import MyGameItem
    game = "My Game"  # name of the game/world this item is from

class MyGameLocation(Location):  # or from Locations import MyGameLocation
    game = "My Game"  # name of the game/world this location is in

class MyGameWorld(World):
    """Insert description of the world/game here."""
    game: str = "My Game"  # name of the game/world
    options = mygame_options  # options the player can set
    topology_present: bool = True  # show path to victory in spoiler
    remote_items: bool = False  # True if all items come from the server

    # ID of first item and location, can be hard-coded but code may be easier
    # to read with this as a propery
    start_id = 1234

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: id for
                       id, name in enumerate(mygame_items, start_id)}
    location_name_to_id = {name: id for
                           id, name in enumerate(mygame_locations, start_id)}
```

### Generation

The world has to provide the following things for generation

* the properties mentioned above 
* additions to the item pool
* additions to the regions list: at least one called "Menu"
* locations placed inside those regions
* a `def create_item(self, item: str) -> MyGameItem` for plando/manual placing
* a `def generate_output(self, output_directory: str)` that creates the output
  if there is output to be generated (i.e. `remote_items = False`). When this is
  called, `self.world.get_locations()` has all locations for all players, with
  properties `item` pointing to the item and `player` identifying the player.
  `self.world.get_filled_locations(self.player)` will filter for this world.
  `item.player` can be used to see if it's a local item.

In addition the following methods can be implemented

* `def generate_early(self)`
  called per player before any items or locations are created. You can set
  properties on your world here. Already has access to player options and RNG.
* `def create_regions(self)`
  called to place player's regions into the MultiWorld's regions list. If it's
  hard to separate, this can be done during `generate_early` or `basic` as well.
* `def create_items(self)`
  called to place player's items into the MultiWorld's itempool.
* `def set_rules(self)`
  called to set access and item rules on locations and entrances.
* `def generate_basic(self)`
  called after the previous steps. Some placement and player specific
  randomizations can be done here. After this step all regions and items have
  to be in the MultiWorld's regions and itempool.
* `pre_fill`, `fill_hook` and `post_fill` are called to modify item placement
  before, during and after the regular fill process, before `generate_output`.
* `fill_slot_data` and `modify_multidata` can be used to modify the data that
  will be used by the server to host the MultiWorld.
* `def get_required_client_version(self)`
  can return a tuple of 3 ints to make sure the client is compatible to this
  world (e.g. item IDs) when connecting.

#### generate_early

```python
def generate_early(self):
    # read player settings to world instance
    self.final_boss_hp = self.world.final_boss_hp[self.player].value
```

#### create_item

```python
# we need a way to know if an item provides progress in the game ("key item")
# this can be part of the items definition, or depend on recipe randomization
from .Items import is_pregression  # this is just a dummy

def create_item(self, item: str):
    # This is called when AP wants to create an item by name (for plando) or
    # when you call it from your own code.
    return MyGameItem(item, is_progression(item), self.item_name_to_id[item],
                      self.player)

def create_event(self, event: str):
    # while we are at it, we can also add a helper to create events
    return MyGameItem(event, True, None, self.player)
```

#### create_items

```python
def create_items(self):
    # Add items to the Multiworld.
    # If there are two of the same item, the item has to be twice in the pool.
    # Which items are added to the pool may depend on player settings,
    # e.g. custom win condition like triforce hunt.
    for item in mygame_items:
        self.world.itempool += self.create_item(item)
```
**FIXME**: item groups? is that a generic thing?

#### create_regions

```python
def create_regions(self):
    # Add regions to the multiworld. "Menu" is the required starting point.
    # Arguments to Region() are name, type, human_readable_name, player, world
    r = Region("Menu", None, "Menu", self.player, self.world)
    # Set Region.exits to a list of entrances that are reachable from region
    r.exits = [Entrance(self.player, "New game", r)]  # or use r.exits.append
    # Append region to MultiWorld's regions
    self.world.regions.append(r)  # or use += [r...]
    
    r = Region("Main Area", None, "Main Area", self.player, self.world)
    # Add main area's locations to main area (all but final boss)
    r.locations = [MyGameLocation(self.player, location.name,
                   self.location_name_to_id[location.name], r)]
    r.exits = [Entrance(self.player, "Boss Door", r)]
    self.world.regions.append(r)
    
    r = Region("Boss Room", None, "Boss Room", self.player, self.world)
    # add event to Boss Room
    r.locations = [MyGameLocation(self.player, "Final Boss", None, r)]
    self.world.regions.append(r)
    
    # If entrances are not randomized, they should be connected here, otherwise
    # they can also be connected at a later stage.
    self.world.get_entrance("New Game", self.player)\
        .connect(self.world.get_region("Main Area", self.player))
    self.world.get_entrance("Boss Door", self.player)\
        .connect(self.world.get_region("Boss Room", self.player))
    
    # If setting location access rules from data is easier here, set_rules can
    # possibly omitted.
```

#### generate_basic

```python
def generate_basic(self):
    # place "Victory" at "Final Boss" and set collection as win condition
    self.world.get_location("Final Boss", self.player)\
        .place_locked_item(self.create_event("Victory"))
    self.world.completion_condition[self.player] = \
        lambda state: state.has("Victory", self.player)

    # place item Herb into location Chest1 for some reason
    item = self.create_item("Herb")
    self.world.get_location("Chest1", self.player).place_locked_item(item)
    # in most cases it's better to do this at the same time the itempool is
    # filled to avoid accidental duplicates:
    # manually placed and still in the itempool
```

### Setting Rules

```python
from ..generic.Rules import add_rule, set_rule, forbid_item
from Items import get_item_type

def set_rules(self):
    # For some worlds this step can be omitted if either a Logic mixin 
    # (see below) is used, it's easier to apply the rules from data during
    # location generation or everything is in generate_basic

    # set a simple rule for an region
    set_rule(self.world.get_entrance("Boss Door", self.player),
             lambda state: state.has("Boss Key", self.player))
    # combine rules to require two items
    add_rule(self.world.get_location("Chest2", self.player),
             lambda state: state.has("Sword", self.player))
    add_rule(self.world.get_location("Chest2", self.player),
             lambda state: state.has("Shield", self.player))
    # or simply combine yourself
    set_rule(self.world.get_location("Chest2", self.player),
             lambda state: state.has("Sword", self.player) and
                           state.has("Shield", self.player))
    # require two of an item
    set_rule(self.world.get_location("Chest3", self.player),
             lambda state: state.has("Key", self.player, 2))
    # set_rule is likely to be a bit faster than add_rule
    # state also has .item_count() for items and .has_any(), .has_all() for sets

    # FIXME: has_group, count_group ?

    # disallow placing a specific local item at a specific location
    forbid_item(self.world.get_location("Chest4", self.player), "Sword")
    # disallow placing items with a specific property
    add_item_rule(self.world.get_location("Chest5", self.player),
                  lambda item: get_item_type(item) == "weapon")
    # get_item_type needs to take player/world into account
    # if MyGameItem has a type property, a more direct implementation would be
    add_item_rule(self.world.get_location("Chest5", self.player),
                  lambda item: item.player != self.player or\
                               item.my_type == "weapon")
    # location.item_rule = ... is likely to be a bit faster
```

### Logic Mixin

While lambdas and events could do pretty much anything, by convention we
implement more complex logic in Logic mixins, even if there is no need to add
properties to the `BaseClasses.CollectionState` state object.

Wenn importing a file that defines a class that inherits from
`..AutoWorld.LogicMixin` the state object's class is automatically extended by
the mixin's members. By convention those are prefixed with `_world_`.

Typical uses are defining methods that are used instead of `state.has`
in lambdas, e.g.`state._mygame_has(custom, world, player)` or recurring checks
like `state._mygame_can_do_something(world, player)` to simplify lambdas.

More advanced uses could be to add additional variables to the state object,
override `World.collect(self, state, item)` and `remove(self, state, item)`
to update the state object, and check those added variables in added methods.
Please do this with caution and only when neccessary.

#### Sample

```python
# Logic.py

from ..AutoWorld import LogicMixin

class MyGameLogic(LogicMixin):
    def _mygame_has_key(self, world: MultiWorld, player: int):
        # Arguments above are free to choose
        # it may make sense to use World as argument instead of MultiWorld
        return self.has('key', player)  # or whatever
```
```python
# __init__.py

from ..generic.Rules import set_rule
import .Logic  # apply the mixin by importing its file

class MyGameWorld(World):
    # ...
    def set_rules(self):
        set_rule(self.world.get_location("A Door", self.player),
                 lamda state: state._myworld_has_key(self.world, self.player))
```

### Generate Output

```python
from .Mod import generate_mod

def generate_output(self, output_directory: str):
    # How to generate the mod or ROM highly depends on the game
    # if the mod is written in Lua, Jinja can be used to fill a template
    # if the mod reads a json file, `json.dump()` can be used to generate that
    # code below is a dummy
    data = {
        "seed": self.world.seed_name,  # to verify the server's multiworld
        "slot": self.world.player_name[self.player],  # to connect to server
        "items": {location.name: location.item.name
                  if location.item.player == self.player else "Remote"
                  for location in self.world.get_filled_locations(self.player)},
        "final_boss_hp": self.final_boss_hp,
        # store option name "easy", "normal" or "hard" for difficuly
        "difficulty": self.world.difficulty[self.player].current_key,
        # store option value True or False for fixing a glitch
        "fix_xyz_glitch": self.world.fix_xyz_glitch[self.player].value
    }
    # point to a ROM specified by the installation
    src = Utils.get_options()["mygame_options"]["rom_file"]
    # or point to worlds/mygame/data/mod_template
    src = os.path.join(os.path.dirname(__file__), "data", "mod_template")
    # generate output path
    mod_name = f"AP-{self.world.seed_name}-P{self.player}-{self.world.player_name[self.player]}"
    out_file = os.path.join(output_directory, mod_name + ".zip")
    # generate the file
    generate_mod(src, out_file, data)
```

