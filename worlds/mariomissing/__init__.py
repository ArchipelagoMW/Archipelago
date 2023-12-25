import os
import typing
import threading
import dataclasses

from typing import Dict, List, Set, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from Options import PerGameCommonOptions
import Patch
import settings
from .Items import get_item_names_per_category, item_table, filler_items, artifacts
from .Locations import get_locations
from .Regions import create_regions
from .Options import MarioisMissingOptions
from .SetupGame import setup_gamevars
from .Client import MIMSNIClient
from .Rom import LocalRom, patch_rom, get_base_rom_path, MIMDeltaPatch, USHASH

class MiMSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Mario is Missing US ROM"""
        description = "Mario is Missing ROM File"
        copy_to = "Mario Is Missing! (USA).sfc"
        md5s = [USHASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)

class MiMWeb(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Mario is Missing randomizer"
        "and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    tutorials = [setup_en]

class MarioisMissingWorld(World):
    """Mario is Missing is a 2D edutainment game. As Luigi, save cities of the world from Bowser's terror while searching his castle for Mario."""
    game: str = "Mario is Missing"
    option_definitions = MarioisMissingOptions
    data_version = 1
    required_client_version = (0, 3, 5)

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = {location.name: location.code for location in get_locations(None, None, None)}
    item_name_groups = get_item_names_per_category()

    web = MiMWeb()
    settings: typing.ClassVar[MiMSettings]
    #topology_present = True

    options_dataclass = MarioisMissingOptions
    options: MarioisMissingOptions

    locked_locations: List[str]
    location_cache: List[Location]

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

        self.locked_locations= []
        self.location_cache= []

    @classmethod
    def stage_assert_generate(cls, multiworld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"Floor 1:      {self.city_list[0:5]}\n")
        spoiler_handle.write(f"Floor 2:      {self.city_list[5:10]}\n")
        spoiler_handle.write(f"Floor 3:      {self.city_list[10:15]}\n")

    def create_item(self, name: str) -> Item:
        data = item_table[name]

        if data.useful:
            classification = ItemClassification.useful
        elif data.progression:
            classification = ItemClassification.progression
        elif data.trap:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler

        item = Item(name, classification, data.code, self.player)

        return item

    def create_regions(self):
        create_regions(self.multiworld, self.player, get_locations(self.multiworld, self.player, self),
                        self.location_cache, self)

    def get_filler_item_name(self) -> str:
        if self.options.computer_sanity.value == 1:
            return self.random.choice(filler_items)
        else:
            return "Photograph"

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has('Mario', self.player)
        self.multiworld.get_location("Bowser", self.player).place_locked_item(self.create_item("Mario"))

        self.multiworld.get_location("Colosseum - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Trevi Fountain - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Sistine Chapel - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Cathedral of Notre Dame - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Arc de Triomphe - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Eiffel Tower - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Tower of London - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Westminster Abbey - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Big Ben - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Empire State Building - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Statue of Liberty - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Rockefeller Center - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Golden Gate Bridge - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Coit Tower - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Transamerica Pyramid - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Erechtheion Temple - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Hadrian's Arch - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Parthenon - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Bondi Beach - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Taronga Zoo - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Sydney Opera - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Great Buddha of Kamakura - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Sensoji Temple - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Kokugikan Arena - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Nairobi National Park - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Maasai Village - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("National Museum of Kenya - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Christ the Redeemer Statue - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Copacabana Beach - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Sugar Loaf Mountain - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Great Pyramid - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Mosque of Mohammed - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Sphinx - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Kremlin - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("St. Basil's Cathedral - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Bolshoi Ballet - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Temple of Heaven - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Great Wall of China - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Forbidden City - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Teatro Colon - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Gaucho Museum - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Obelisk Monument - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Angel of Independence - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("National Palace - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))
        self.multiworld.get_location("Fine Arts Palace - Return Artifact", self.player).place_locked_item(self.create_item("Artifact Secured"))

    def place_locked_item(self, excluded_items: Set[str], location: str, item: str) -> None:
        excluded_items.add(item)

        item = self.create_item(item)

        self.multiworld.get_location(location, self.player).place_locked_item(item)

    def generate_early(self):
        setup_gamevars(self)


    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        for item in self.multiworld.start_inventory[self.player]:
            if item in artifacts:
                excluded_items.add(item)

        return excluded_items

    def create_item_with_correct_settings(self, player: int, name: str) -> Item:
        data = item_table[name]
        if data.useful:
            classification = ItemClassification.useful
        elif data.progression:
            classification = ItemClassification.progression
        elif data.trap:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler
        item = Item(name, classification, data.code, player)

        if not item.advancement:
            return item

        return item

    def generate_filler(self, multiworld: MultiWorld, player: int,
                                        pool: List[Item]):

        for _ in range(len(multiworld.get_unfilled_locations(player)) - len(pool) - 46):
            item = self.create_item_with_correct_settings(player, self.get_filler_item_name())
            pool.append(item)

    def get_item_pool(self, player: int, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                for _ in range(data.amount):
                    item = self.create_item_with_correct_settings(player, name)
                    pool.append(item)

        return pool

    def create_items(self):
        excluded_items = self.get_excluded_items()

        pool = self.get_item_pool(self.player, excluded_items)

        self.generate_filler(self.multiworld, self.player, pool)

        self.multiworld.itempool += pool

    def generate_output(self, output_directory: str):

        rompath = ""  # if variable is not declared finally clause may fail
        try:
            world = self.multiworld
            player = self.player
            rom = LocalRom(get_base_rom_path())
            patch_rom(self, rom, self.player, self.multiworld)

            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = MIMDeltaPatch(os.path.splitext(rompath)[0]+MIMDeltaPatch.patch_file_ending, player=player,
                                  player_name=world.player_name[player], patched_path=rompath)
            patch.write()
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected
            if os.path.exists(rompath):
                os.unlink(rompath)

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
