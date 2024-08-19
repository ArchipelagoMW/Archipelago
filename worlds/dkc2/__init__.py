import dataclasses
import os
import typing
import math
import settings
import hashlib
import threading
import pkgutil

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from Options import PerGameCommonOptions
from worlds.AutoWorld import World, WebWorld
from .Items import DKC2Item, ItemData, item_table, junk_table, item_groups
from .Locations import DKC2Location, setup_locations, all_locations, location_groups
from .Regions import create_regions, connect_regions
from .Names import ItemName, LocationName, EventName
from .Options import DKC2Options, LogicDifficulty, StartingKong
from .Client import DKC2SNIClient
from .Levels import generate_level_list, location_id_to_level_id
from .Rules import DKC2StrictRules, DKC2NormalRules, DKC2ExpertRules
from .Rom import patch_rom, DKC2ProcedurePatch, HASH_US, HASH_US_REV_1

class DKC2Settings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Mega Man X US ROM"""
        description = "Donkey Kong Country 2 (USA) ROM File"
        copy_to = "Donkey Kong Country 2 - Diddy's Kong Quest (USA).sfc"
        md5s = [HASH_US, HASH_US_REV_1]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class DKC2Web(WebWorld):
    theme = "grass"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Donkey Kong Country 2 - Diddy's Kong Quest with Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["lx5"]
    )

    tutorials = [setup_en]


class DKC2World(World):
    """
    Donkey Kong Country 2 WIP
    """
    game = "Donkey Kong Country 2"
    web = DKC2Web()

    settings: typing.ClassVar[DKC2Settings]
    
    options_dataclass = DKC2Options
    options: DKC2Options
    
    required_client_version = (0, 5, 0)

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations
    item_name_groups = item_groups
    location_name_groups = location_groups
    hint_blacklist = {
    }

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        location_table = setup_locations(self)
        create_regions(self.multiworld, self.player, self, location_table)

        itempool: typing.List[DKC2Item] = []
        
        connect_regions(self)
        
        total_required_locations = 192

        # Set starting kong
        if self.options.starting_kong == StartingKong.option_diddy:
            self.multiworld.push_precollected(self.create_item(ItemName.diddy))
        elif self.options.starting_kong == StartingKong.option_dixie:
            self.multiworld.push_precollected(self.create_item(ItemName.dixie))
        elif self.options.starting_kong == StartingKong.option_both:
            self.multiworld.push_precollected(self.create_item(ItemName.diddy))
            self.multiworld.push_precollected(self.create_item(ItemName.dixie))

        self.multiworld.push_precollected(self.create_item(ItemName.gangplank_galleon))

        # Add progression items
        itempool += [self.create_item(ItemName.crocodile_cauldron)]
        itempool += [self.create_item(ItemName.krem_quay)]
        itempool += [self.create_item(ItemName.krazy_kremland)]
        itempool += [self.create_item(ItemName.gloomy_gulch)]
        itempool += [self.create_item(ItemName.krools_keep)]
        itempool += [self.create_item(ItemName.the_flying_krock)]

        itempool += [self.create_item(ItemName.diddy)]
        itempool += [self.create_item(ItemName.dixie)]
        itempool += [self.create_item(ItemName.carry)]
        itempool += [self.create_item(ItemName.climb)]
        itempool += [self.create_item(ItemName.cling)]
        itempool += [self.create_item(ItemName.cartwheel)]
        itempool += [self.create_item(ItemName.swim)]
        itempool += [self.create_item(ItemName.team_attack)]
        itempool += [self.create_item(ItemName.helicopter_spin)]

        itempool += [self.create_item(ItemName.rambi)]
        itempool += [self.create_item(ItemName.squawks)]
        itempool += [self.create_item(ItemName.enguarde)]
        itempool += [self.create_item(ItemName.squitter)]
        itempool += [self.create_item(ItemName.rattly)]
        itempool += [self.create_item(ItemName.clapper)]
        itempool += [self.create_item(ItemName.glimmer)]

        itempool += [self.create_item(ItemName.barrel_kannons)]
        itempool += [self.create_item(ItemName.barrel_exclamation)]
        itempool += [self.create_item(ItemName.barrel_kong)]
        itempool += [self.create_item(ItemName.barrel_warp)]
        itempool += [self.create_item(ItemName.barrel_control)]
        
        itempool += [self.create_item(ItemName.skull_kart)]

        # Add junk items into the pool
        junk_count = total_required_locations - len(itempool)

        junk_weights = []
        junk_weights += ([ItemName.red_balloon] * 40)
        junk_weights += ([ItemName.banana_coin] * 20)

        junk_pool = []
        for i in range(junk_count):
            junk_item = self.random.choice(junk_weights)
            junk_pool.append(self.create_item(junk_item))

        itempool += junk_pool

        # Set victory item
        self.multiworld.get_location(LocationName.k_rool_duel_clear, self.player).place_locked_item(self.create_item(ItemName.victory))

        # Finish
        self.multiworld.itempool += itempool


    def create_item(self, name: str, force_classification=False) -> Item:
        data = item_table[name]

        if force_classification:
            classification = force_classification
        elif data.progression:
            classification = ItemClassification.progression
        elif data.trap:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler
        
        created_item = DKC2Item(name, classification, data.code, self.player)

        return created_item


    def set_rules(self):
        logic = self.options.logic_difficulty
        if logic == LogicDifficulty.option_easy:
            DKC2StrictRules(self).set_dkc2_rules()
        elif logic == LogicDifficulty.option_normal:
            DKC2StrictRules(self).set_dkc2_rules()
        elif logic == LogicDifficulty.option_hard:
            DKC2StrictRules(self).set_dkc2_rules()
        else:
            raise ValueError(f"Somehow you have a logic option that's currently invalid."
                             f" {logic} for {self.multiworld.get_player_name(self.player)}")


    def fill_slot_data(self):
        slot_data = {}
        return slot_data


    def generate_early(self):
        self.level_connections = dict()
        self.boss_connections = dict()
        self.rom_connections = dict()
        generate_level_list(self)


    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        pass


    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        pass


    def get_filler_item_name(self) -> str:
        return self.random.choice(list(junk_table.keys()))


    def generate_output(self, output_directory: str):
        try:
            patch = DKC2ProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch.write_file("dkc2_basepatch.bsdiff4", pkgutil.get_data(__name__, "data/dkc2_basepatch.bsdiff4"))
            patch_rom(self, patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected


    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
