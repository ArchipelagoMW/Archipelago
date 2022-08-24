import os
import typing
# import math
import threading

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import CV64Item, ItemData, item_table, junk_table
from .Locations import CV64Location, all_locations, setup_locations
from .Options import cv64_options
from .Regions import create_regions, connect_regions
from .Levels import level_list
from .Rules import set_rules
from .Names import ItemName, LocationName
from ..AutoWorld import WebWorld, World
from .Rom import LocalRom, patch_rom, get_base_rom_path, CV64DeltaPatch
# import math


class CV64Web(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Castlevania 64 randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Liquid Cat"]
    )

    tutorials = "Insert setup webpage here"


class CV64World(World):
    """
    Castlevania for the Nintendo 64 is the first 3D game in the franchise. As either whip-wielding Belmont descendant
    Reinhardt Schneider or powerful sorceress Carrie Fernandez, brave many terrifying traps and foes as you make your
    way to Dracula's chamber and stop his rule of terror.
    """
    game: str = "Castlevania 64"
    option_definitions = cv64_options
    topology_present = False
    data_version = 0
    # hint_blacklist = {}
    remote_items = False

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    active_level_list: typing.List[str]
    web = CV64Web()

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, world):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def _get_slot_data(self):
        return {
            "death_link": self.world.death_link[self.player].value,
            "active_levels": self.active_level_list,
        }

    def _create_items(self, name: str):
        data = item_table[name]
        return [self.create_item(name)] * data.quantity

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in cv64_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def generate_basic(self):
        itempool: typing.List[CV64Item] = []

        # Levels
        total_required_locations = 28

        # number_of_specials = 0
        self.world.get_location(LocationName.the_end, self.player).place_locked_item(self.create_item(ItemName.victory))

        itempool += [self.create_item(ItemName.special_one)] * 1
        itempool += [self.create_item(ItemName.roast_beef)] * 4
        itempool += [self.create_item(ItemName.powerup)] * 1
        itempool += [self.create_item(ItemName.sun_card)] * 3
        itempool += [self.create_item(ItemName.moon_card)] * 3
        itempool += [self.create_item(ItemName.left_tower_key)] * 1

        total_junk_count = total_required_locations - len(itempool)

        junk_pool = []
        for item_name in self.world.random.choices(list(junk_table.keys()), k=total_junk_count):
            junk_pool += [self.create_item(item_name)]

        itempool += junk_pool

        self.active_level_list = level_list.copy()

        if self.world.stage_shuffle[self.player]:
            self.world.random.shuffle(self.active_level_list)

        connect_regions(self.world, self.player, self.active_level_list)

        self.world.itempool += itempool

    def generate_output(self, output_directory: str):
        try:
            world = self.world
            player = self.player

            rom = LocalRom(get_base_rom_path())
            patch_rom(self.world, rom, self.player, self.active_level_list)

            outfilepname = f'_P{player}'
            outfilepname += f"_{world.player_name[player].replace(' ', '_')}" \
                if world.player_name[player] != 'Player%d' % player else ''

            rompath = os.path.join(output_directory, f'AP_{world.seed_name}{outfilepname}.sfc')
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = CV64DeltaPatch(os.path.splitext(rompath)[0]+CV64DeltaPatch.patch_file_ending, player=player,
                                   player_name=world.player_name[player], patched_path=rompath)
            patch.write()
        except:
            raise
        finally:
            if os.path.exists(rompath):
                os.unlink(rompath)
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.world.player_name[self.player]]

    def create_regions(self):
        location_table = setup_locations(self.world, self.player)
        create_regions(self.world, self.player, location_table)

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = CV64Item(name, classification, data.code, self.player)

        return created_item

    def set_rules(self):
        set_rules(self.world, self.player)
