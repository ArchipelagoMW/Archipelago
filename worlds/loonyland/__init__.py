# world/Loonyland/__init__.py

import settings
import typing
from .options import LoonylandOptions  
from .items import Loonyland_items, item_frequencies, LoonylandItem
from .locations import Loonyland_locations, LoonylandLocation
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, RegionType, ItemClassification


class MyGameSettings(settings.Group):


class MyGameWorld(World):
    """Insert description of the world/game here."""
    game = "Loonyland"  
    options_dataclass = LoonylandOptions  # options the player can set
    options: LoonylandOptions  # typing hints for option results
    settings: typing.ClassVar[MyGameSettings]  # will be automatically assigned from type hint
    topology_present = True  # show path to required location checks in spoiler

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    base_id = 2876900
    # instead of dynamic numbering, IDs could be part of data

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: id for
                       id, name in enumerate(mygame_items, base_id)}
    location_name_to_id = {name: id for
                           id, name in enumerate(mygame_locations, base_id)}
