import settings
import typing
from .Items import item_table
from .Locations import get_location_datas
from .Options import CrystalProjectOptions, Toggle
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, ItemClassification

class CrystalProjectItem(Item):  # or from Items import MyGameItem
    game = "Crystal Project"  # name of the game/world this item is from


class CrystalProjectLocation(Location):  # or from Locations import MyGameLocation
    game = "Crystal Project"  # name of the game/world this location is in


#class CrystalProjectSettings(settings.Group):
    # class RomFile(settings.SNESRomPath):
    #     """Insert help text for host.yaml here."""

    # rom_file: RomFile = RomFile("MyGame.sfc")

class CrystalProjectWorld(World):
    """Insert description of the world/game here."""
    game = "Crystal Project"  # name of the game/world
    options_dataclass = CrystalProjectOptions  # options the player can set
    options: CrystalProjectOptions  # typing hints for option results
    #settings: typing.ClassVar[CrystalProjectSettings]  # will be automatically assigned from type hint
    topology_present = False  # show path to required location checks in spoiler

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    base_id = 0
    # instead of dynamic numbering, IDs could be part of data

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    # item_name_to_id = {name: id for
    #                    id, name in enumerate(mygame_items, base_id)}
    # location_name_to_id = {name: id for
    #                        id, name in enumerate(mygame_locations, base_id)}
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {location.name: location.code for location in get_location_datas(-1, None)}

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    item_name_groups = {
        "weapons": {"sword", "lance"},
    }