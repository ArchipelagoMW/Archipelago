import os
import threading
import typing

import settings
from BaseClasses import Tutorial, ItemClassification
from .Options import GLOptions
from worlds.AutoWorld import WebWorld, World
from .Locations import all_locations, location_table
from .Items import GLItem, itemList, item_table, item_frequencies
from .Regions import create_regions, connect_regions
from .Rom import Rom, GLProcedurePatch, write_files
from .Rules import set_rules
from ..LauncherComponents import components, Component, launch_subprocess, Type, SuffixIdentifier


def launch_client(*args):
    from .GauntletLegendsClient import launch
    launch_subprocess(launch, name="GLClient")


components.append(Component("Gauntlet Legends Client", "GLClient", func=launch_client,
                            component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apgl")))


class GauntletLegendsWebWorld(WebWorld):
    settings_page = "games/gl/info/en"
    theme = 'partyTime'
    tutorials = [
        Tutorial(
            tutorial_name='Setup Guide',
            description='A guide to playing Gauntlet Legends',
            language='English',
            file_name='setup_en.md',
            link='setup/en',
            authors=['jamesbrq']
        )
    ]


class GLSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the GL US rom"""
        copy_to = "Gauntlet Legends (U) [!].z64"
        description = "Gauntlet Legends ROM File"

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = False


class GauntletLegendsWorld(World):
    """
    Gauntlet Legends
    """
    game = "Gauntlet Legends"
    web = GauntletLegendsWebWorld()
    data_version = 1
    options_dataclass = GLOptions
    options: GLOptions
    settings: typing.ClassVar[GLSettings]
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}
    required_client_version = (0, 4, 4)
    crc32: str = None
    shard_values: typing.List[bytes] = [[0x2B, 0x3], [0x2B, 0x1], [0x2B, 0x4], [0x2B, 0x2]]
    output_complete: threading.Event = threading.Event()

    excluded_locations = []

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)
        item = self.create_item("Key")
        self.multiworld.get_location("Valley of Fire - Key 1", self.player).place_locked_item(item)
        self.multiworld.get_location("Valley of Fire - Key 5", self.player).place_locked_item(item)

    def fill_slot_data(self) -> dict:
        return {
            "player": self.player,
            "scale": 0,
            "shards": self.shard_values
        }


    def create_items(self) -> None:
        # First add in all progression and useful items
        required_items = []
        precollected = [item for item in itemList if item in self.multiworld.precollected_items[self.player]]
        for item in itemList:
            if item.progression != ItemClassification.filler and item.progression != ItemClassification.skip_balancing and item not in precollected:
                freq = item_frequencies.get(item.itemName, 1)
                if freq is None:
                    freq = 1
                required_items += [item.itemName for _ in range(freq)]

        for itemName in required_items:
            self.multiworld.itempool.append(self.create_item(itemName))

        # Then, get a random amount of fillers until we have as many items as we have locations
        filler_items = []
        for item in itemList:
            if item.progression == ItemClassification.filler:
                freq = item_frequencies.get(item.itemName)
                if freq is None:
                    freq = 1
                filler_items += [item.itemName for _ in range(freq)]

        remaining = len(all_locations) - len(required_items) - 2
        for i in range(remaining):
            filler_item_name = self.multiworld.random.choice(filler_items)
            item = self.create_item(filler_item_name)
            self.multiworld.itempool.append(item)
            filler_items.remove(filler_item_name)

    def set_rules(self) -> None:
        set_rules(self, self.excluded_locations)
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.can_reach("Gates of the Underworld", "Region", self.player)

    def create_item(self, name: str) -> GLItem:
        item = item_table[name]
        return GLItem(item.itemName, item.progression, item.code, self.player)

    def generate_output(self, output_directory: str) -> None:
        patch = GLProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        write_files(self, patch)
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)
