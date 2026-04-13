from typing import ClassVar

from BaseClasses import MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World
import settings

from .constants import USA_ROM_HASH
from .items import CVAOSItem, item_name_to_id, create_item, create_itempool
from .locations import location_name_to_id
from .options import CVAOSOptions
from .regions import create_regions


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


class CVAOSWorld(World):
    """
    Castlevania: Aria of Sorrow is a 2003 action-adventure game developed by Konami
    for the Game Boy Advance. Play as Soma Cruz and explore Dracula's castle,
    collecting souls from defeated enemies to gain their abilities.
    """

    game = "Castlevania - Aria of Sorrow"
    web = CVAOSWebWorld()

    options_dataclass = CVAOSOptions
    options: CVAOSOptions
    settings: ClassVar[CVAOSSettings]

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    topology_present = True
    origin_region_name = "Menu"

    def create_regions(self) -> None:
        create_regions(self)

    def create_items(self) -> None:
        itempool = create_itempool(self)
        self.multiworld.itempool += itempool

    def create_item(self, name: str) -> CVAOSItem:
        return create_item(self, name)
