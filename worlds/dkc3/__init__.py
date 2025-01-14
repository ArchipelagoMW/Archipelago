import dataclasses
import math
import os
import threading
import typing

import settings
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
from .Client import DKC3SNIClient
from .Items import DKC3Item, ItemData, item_table, inventory_table, junk_table
from .Levels import level_list
from .Locations import DKC3Location, all_locations, setup_locations
from .Names import ItemName, LocationName
from .Options import DKC3Options, dkc3_option_groups
from .Regions import create_regions, connect_regions
from .Rom import LocalRom, patch_rom, get_base_rom_path, DKC3DeltaPatch
from .Rules import set_rules


class DK3Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the DKC3 US rom"""
        copy_to = "Donkey Kong Country 3 - Dixie Kong's Double Trouble! (USA) (En,Fr).sfc"
        description = "DKC3 (US) ROM File"
        md5s = [DKC3DeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class DKC3Web(WebWorld):
    theme = "jungle"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Donkey Kong Country 3 randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["PoryGone"]
    )

    tutorials = [setup_en]

    option_groups = dkc3_option_groups


class DKC3World(World):
    """
    Donkey Kong Country 3 is an action platforming game.
    Play as Dixie Kong and her baby cousin Kiddy as they try to solve the
    mystery of why Donkey Kong and Diddy disappeared while on vacation.
    """
    game: str = "Donkey Kong Country 3"
    settings: typing.ClassVar[DK3Settings]

    options_dataclass = DKC3Options
    options: DKC3Options

    topology_present = False
    #hint_blacklist = {LocationName.rocket_rush_flag}

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    active_level_list: typing.List[str]
    web = DKC3Web()
    
    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def _get_slot_data(self):
        return {
            #"death_link": self.options.death_link.value,
            "active_levels": self.active_level_list,
        }

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in (attr.name for attr in dataclasses.fields(DKC3Options)
                            if attr not in dataclasses.fields(PerGameCommonOptions)):
            option = getattr(self.options, option_name)
            slot_data[option_name] = option.value

        return slot_data

    def create_regions(self):
        location_table = setup_locations(self)
        create_regions(self, location_table)

        # Not generate basic
        self.topology_present = self.options.level_shuffle.value
        itempool: typing.List[DKC3Item] = []

        # Levels
        total_required_locations = 159

        number_of_banana_birds = 0
        # Rocket Rush Cog
        total_required_locations -= 1
        number_of_cogs = 4
        self.multiworld.get_location(LocationName.rocket_rush_flag, self.player).place_locked_item(self.create_item(ItemName.krematoa_cog))
        number_of_bosses = 8
        if self.options.goal == "knautilus":
            self.multiworld.get_location(LocationName.kastle_kaos, self.player).place_locked_item(self.create_item(ItemName.victory))
            number_of_bosses = 7
        else:
            self.multiworld.get_location(LocationName.banana_bird_mother, self.player).place_locked_item(self.create_item(ItemName.victory))
            number_of_banana_birds = self.options.number_of_banana_birds

        # Bosses
        total_required_locations += number_of_bosses

        # Secret Caves
        total_required_locations += 13

        if self.options.kongsanity:
            total_required_locations += 39

        ## Brothers Bear
        if False:#self.options.include_trade_sequence:
            total_required_locations += 10

        number_of_bonus_coins = (self.options.krematoa_bonus_coin_cost * 5)
        number_of_bonus_coins += math.ceil((85 - number_of_bonus_coins) * self.options.percentage_of_extra_bonus_coins / 100)

        itempool += [self.create_item(ItemName.bonus_coin) for _ in range(number_of_bonus_coins)]
        itempool += [self.create_item(ItemName.dk_coin) for _ in range(41)]
        itempool += [self.create_item(ItemName.banana_bird) for _ in range(number_of_banana_birds)]
        itempool += [self.create_item(ItemName.krematoa_cog) for _ in range(number_of_cogs)]
        itempool += [self.create_item(ItemName.progressive_boat) for _ in range(3)]

        total_junk_count = total_required_locations - len(itempool)

        junk_pool = []
        for item_name in self.multiworld.random.choices(list(junk_table.keys()), k=total_junk_count):
            junk_pool.append(self.create_item(item_name))

        itempool += junk_pool

        self.active_level_list = level_list.copy()

        if self.options.level_shuffle:
            self.random.shuffle(self.active_level_list)

        connect_regions(self, self.active_level_list)

        self.multiworld.itempool += itempool

    def generate_output(self, output_directory: str):
        try:
            rom = LocalRom(get_base_rom_path())
            patch_rom(self, rom, self.active_level_list)

            self.active_level_list.append(LocationName.rocket_rush_region)

            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = DKC3DeltaPatch(os.path.splitext(rompath)[0]+DKC3DeltaPatch.patch_file_ending, player=self.player,
                                   player_name=self.multiworld.player_name[self.player], patched_path=rompath)
            patch.write()
        except:
            raise
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

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        if self.topology_present:
            world_names = [
            LocationName.lake_orangatanga_region,
            LocationName.kremwood_forest_region,
            LocationName.cotton_top_cove_region,
            LocationName.mekanos_region,
            LocationName.k3_region,
            LocationName.razor_ridge_region,
            LocationName.kaos_kore_region,
            LocationName.krematoa_region,
            ]
            er_hint_data = {}
            for world_index in range(len(world_names)):
                for level_index in range(5):
                    level_id: int = world_index * 5 + level_index

                    if level_id >= len(self.active_level_list):
                        break

                    level_region = self.multiworld.get_region(self.active_level_list[level_id], self.player)
                    for location in level_region.locations:
                        er_hint_data[location.address] = world_names[world_index]

            hint_data[self.player] = er_hint_data

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = DKC3Item(name, classification, data.code, self.player)

        return created_item

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(list(junk_table.keys()))

    def set_rules(self):
        set_rules(self)
