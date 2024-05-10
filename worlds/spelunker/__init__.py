import base64
import os
import typing
import threading

from typing import List, Set, TextIO, Dict
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
import settings
from .Items import get_item_names_per_category, item_table, filler_items, useful_items
from .Locations import get_locations
from .Regions import init_areas
from .Options import SpelunkerOptions
from .Client import SpelunkerClient
from .Rules import set_rules
from .Rom import LocalRom, patch_rom, get_base_rom_path, SpelunkerProcPatch, USHASH


class SpelunkerSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Spelunker NES ROM"""
        description = "Spelunker ROM File"
        copy_to = "Spelunker.nes"
        md5s = [USHASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class SpelunkerWeb(WebWorld):
    theme = "dirt"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Spelunker randomizer and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    tutorials = [setup_en]


class SpelunkerWorld(World):
    """
    Spelunker is a 2D platformer for the NES.
    Explore the cavernous depths, collecting treasure along the way and seeking the mythical Pyramid of Gold.
    Also, you'll probably die a lot.
    """
    game = "Spelunker"
    option_definitions = SpelunkerOptions
    required_client_version = (0, 4, 6)

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = {location.name: location.code for location in get_locations(None)}
    item_name_groups = get_item_names_per_category()

    web = SpelunkerWeb()
    settings: typing.ClassVar[SpelunkerSettings]
    # topology_present = True

    options_dataclass = SpelunkerOptions
    options: SpelunkerOptions

    locked_locations: List[str]
    rom_name: bytearray

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)
        self.locked_locations = []

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return Item(name, data.classification, data.code, self.player)

    def create_regions(self) -> None:
        init_areas(self, get_locations(self))

    def get_filler_item_name(self) -> str:
        if self.random.randint(0, 100) <= 10:
            return self.random.choice(useful_items)
        else:
            return self.random.choice(filler_items)

    def set_rules(self) -> None:
        set_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Golden Pyramid", self.player)
        self.get_location("Golden Pyramid").place_locked_item(self.create_item("Golden Pyramid"))

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        return excluded_items

    def create_item_with_correct_settings(self, name: str) -> Item:
        data = item_table[name]
        item = Item(name, data.classification, data.code, self.player)
        return item

    def generate_filler(self, pool: List[Item]) -> None:
        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool) - 1):
            item = self.create_item_with_correct_settings(self.get_filler_item_name())
            pool.append(item)

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                for _ in range(data.amount):
                    item = self.create_item_with_correct_settings(name)
                    pool.append(item)

        return pool

    def create_items(self) -> None:
        pool = self.get_item_pool(self.get_excluded_items())

        self.generate_filler(pool)

        self.multiworld.itempool += pool

    def generate_output(self, output_directory: str):
        try:
            world = self.multiworld
            player = self.player
            patch = SpelunkerProcPatch()
            patch_rom(self, patch, self.player, self.multiworld)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: dict) -> None:
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
