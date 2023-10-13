# world/khcom/__init__.py

import settings
import typing
from .Options import khcom_options  # the options we defined earlier
from .Items import KHCOMItem, item_table  # data used below to add items to the World
from .Locations import KHCOMAchievement, achievement_table  # same as above
from .Rules import set_rules
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, RegionType, ItemClassification




class KHCOMWorld(World):
    """Insert description of the world/game here."""
    game = "Kingdom Hearts Chain of Memories"  # name of the game/world
    options_dataclass = khcom_options  # options the player can set
    options: khcom_options  # typing hints for option results
    topology_present = True  # show path to required location checks in spoiler

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    base_id = 7474
    # Instead of dynamic numbering, IDs could be part of data.

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: id for
                       id, name in enumerate(item_table, base_id)}
    location_name_to_id = {name: id for
                           id, name in enumerate(mygame_locations, base_id)}