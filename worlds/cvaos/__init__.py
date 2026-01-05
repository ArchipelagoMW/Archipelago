import typing
from BaseClasses import MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World
import settings
from worlds.cvaos.options import CVAOSOptions
from .constants import USA_ROM_HASH

class CVAOSSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Castlevania AoS USA rom"""
        copy_to = "Castlevania - Aria of Sorrow (USA).gba"
        description = "Castlevania AoS (US) ROM File"
        md5s = [hex(USA_ROM_HASH)[2:]]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class CVAOSWebWorld(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up CVAoS in Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["dem1995"]
    )

    tutorials = [setup_en]

    # option_groups = OPTION_GROUPS

class CVAOSWorld(World):
    pass

# class CVAOSWorld(World):
#     options_dataclass = CVAOSOptions
#     settings: typing.ClassVar[CVAOSSettings]
#     game = "Castlevania: Aria of Sorrow"
#     web = CVAOSWebWorld()
#     topology_present = True
#     all_item_and_group_names = frozenset()  # TODO
#     item_name_to_id =  # TODO
#     location_name_to_id =  # TODO
#     item_name_groups = {} # TODO
#     location_name_groups = {} # TODO
#     origin_region_name = "Menu"
#     web = CVAOSWebWorld()

#     def __init__(self, multiworld: "MultiWorld", player: int):
#         super().__init__(multiworld, player)