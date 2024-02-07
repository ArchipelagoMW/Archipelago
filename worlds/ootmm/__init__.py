import settings
import typing
from .options import OoTMMOptions  # the options we defined earlier
from .items import OoTMMItems  # data used below to add items to the World
from .locations import OoTMMLocations  # same as above
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, RegionType, ItemClassification




class OoTMMSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """Insert help text for host.yaml here."""

    rom_file: RomFile = RomFile("MyGame.sfc")


class OoTMMWorld(World):
    """man fight bigger hunky man (ganondorf) and save world oh and also mask man and gets transformed into a beast (not a furry one tho)."""
    game = "Ocarina of Time & Majora's Mask"  # name of the game/world
    options_dataclass = OoTMMOptions  # options the player can set
    options: OoTMMOptions  # typing hints for option results
    settings: typing.ClassVar[OoTMMSettings]  # will be automatically assigned from type hint
    topology_present = True  # show path to required location checks in spoiler

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    base_id = 3621000
    # instead of dynamic numbering, IDs could be part of data

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: id for
                       id, name in enumerate(OoTMMItems, base_id)}
    location_name_to_id = {name: id for
                           id, name in enumerate(OoTMMLocations, base_id)}

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    # item_name_groups = {
    #     "weapons": {"sword", "lance"},
    # }