import os
import typing
import math
import threading
import pdb

from typing import Dict, List, Set, Tuple, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from .Items import get_item_names_per_category, item_table, filler_items, trap_items
from .Locations import get_locations, EventId
from .LogicExtensions import YoshiLogic
from .Options import yoshi_options, get_option_value
from .Regions import create_regions
from ..AutoWorld import World, WebWorld
from .Client import YISNIClient
from .Rom import LocalRom, patch_rom, get_base_rom_path, YIDeltaPatch
import Patch

class YIWeb(WebWorld):
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Super Adventure Island 2 randomizer and connecting to an Archipelago server.",
        "English",
        "sai2_setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    tutorials = [setup_en]

class YIWorld(World):
    """Yoshi's Island is a 2D platforming game.
        During a delivery, Bowser's evil ward, Kamek, attacked the stork, kidnapping Luigi and dropping Mario onto Yoshi's Island.
        As Yoshi, you must run, jump, and throw eggs to escort the baby Mario across the island to defeat Bowser and reunite the two brothers with their parents."""
    game: str = "Yoshi's Island"
    option_definitions = yoshi_options
    topology_present = False
    data_version = 0
    required_client_version = (0, 3, 5)

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {location.name: location.code for location in get_locations(None, None)}
    item_name_groups = get_item_names_per_category()

    locked_locations: List[str]
    location_cache: List[Location]
    set_req_bosses: str

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

        self.locked_locations= []
        self.location_cache= []

    @classmethod
    def stage_assert_generate(cls, world):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def _get_slot_data(self):
        return {
            #"death_link": self.multiworld.death_link[self.player].value,
        }

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in yoshi_options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

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

        if not item.advancement:
            return item

        return item

    def create_regions(self):
        create_regions(self.multiworld, self.player, get_locations(self.multiworld, self.player),
                        self.location_cache)

    def get_filler_item_name(self) -> str:
        trap_chance: int = self.multiworld.trap_percent[self.player].value

        if self.multiworld.random.random() < (trap_chance / 100) and self.multiworld.traps_enabled[self.player].value == 1:
            return self.multiworld.random.choice(trap_items)
        else:
            return self.multiworld.random.choice(filler_items)

    def set_rules(self):
        setup_events(self.player, self.locked_locations, self.location_cache)

        self.multiworld.completion_condition[self.player] = lambda state: state.has('Saved Baby Luigi', self.player)

    def place_locked_item(self, excluded_items: Set[str], location: str, item: str) -> None:
        excluded_items.add(item)

        item = self.create_item(item)

        self.multiworld.get_location(location, self.player).place_locked_item(item)

    def generate_early(self):
        var_boss(self, self.multiworld, self.player)


    def generate_basic(self):

        self.multiworld.get_location("Burt The Bashful Defeated", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Salvo The Slime Defeated", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Bigger Boo Defeated", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Roger The Ghost Defeated", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Prince Froggy Defeated", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Naval Piranha Defeated", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Marching Milde Defeated", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Hookbill The Koopa Defeated", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Sluggy The Unshaven Defeated", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Raphael The Raven Defeated", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Tap-Tap The Red Nose Defeated", self.player).place_locked_item(self.create_item("Boss Clear"))

        excluded_items = get_excluded_items(self, self.multiworld, self.player)

        pool = get_item_pool(self.multiworld, self.player, excluded_items)

        fill_item_pool_with_dummy_items(self, self.multiworld, self.player, self.locked_locations, self.location_cache, pool)

        self.multiworld.itempool += pool

    def generate_output(self, output_directory: str):

        rompath = ""  # if variable is not declared finally clause may fail
        try:
            world = self.multiworld
            player = self.player
            rom = LocalRom(get_base_rom_path())
            patch_rom(self.multiworld, rom, self.player)

            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = YIDeltaPatch(os.path.splitext(rompath)[0]+YIDeltaPatch.patch_file_ending, player=player,
                                  player_name=world.player_name[player], patched_path=rompath)
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

def get_excluded_items(self: YIWorld, world: MultiWorld, player: int) -> Set[str]:
    excluded_items: Set[str] = set()
    
    if self.multiworld.starting_world[self.player] == 0:
        excluded_items.add('World 1 Gate')
    if self.multiworld.starting_world[self.player] == 1:
        excluded_items.add('World 2 Gate')
    if self.multiworld.starting_world[self.player] == 2:
        excluded_items.add('World 3 Gate')
    if self.multiworld.starting_world[self.player] == 3:
        excluded_items.add('World 4 Gate')
    if self.multiworld.starting_world[self.player] == 4:
        excluded_items.add('World 5 Gate')
    if self.multiworld.starting_world[self.player] == 5:
        excluded_items.add('World 6 Gate')

    if self.multiworld.shuffle_midrings[self.player] == 0:
        excluded_items.add('Middle Ring')

    if self.multiworld.add_secretlens[self.player] == 0:
        excluded_items.add('Secret Lens')

    if self.multiworld.extras_enabled[self.player] == 0:
        excluded_items.add('Extra Panels')
        excluded_items.add('Extra 1')
        excluded_items.add('Extra 2')
        excluded_items.add('Extra 3')
        excluded_items.add('Extra 4')
        excluded_items.add('Extra 5')
        excluded_items.add('Extra 6')

    if self.multiworld.split_extras[self.player] == 1:
        excluded_items.add('Extra Panels')
    else:
        excluded_items.add('Extra 1')
        excluded_items.add('Extra 2')
        excluded_items.add('Extra 3')
        excluded_items.add('Extra 4')
        excluded_items.add('Extra 5')
        excluded_items.add('Extra 6')

    if self.multiworld.split_bonus[self.player] == 1:
        excluded_items.add('Bonus Panels')
    else:
        excluded_items.add('Bonus 1')
        excluded_items.add('Bonus 2')
        excluded_items.add('Bonus 3')
        excluded_items.add('Bonus 4')
        excluded_items.add('Bonus 5')
        excluded_items.add('Bonus 6')

    return excluded_items

def fill_item_pool_with_dummy_items(self: YIWorld, world: MultiWorld, player: int, locked_locations: List[str],
                                    location_cache: List[Location], pool: List[Item]):
    for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)):
        item = create_item_with_correct_settings(world, player, self.get_filler_item_name())
        pool.append(item)

def var_boss(self, world: MultiWorld, player: int):
    world.castle_bosses = world.castle_open_condition[player].value
    world.bowser_bosses = world.castle_clear_condition[player].value
    if world.starting_lives[player] > 255:
        world.lives_high = world.starting_lives[player].value >> 8
        world.lives_low = (world.starting_lives[player].value - world.lives_high) - ((255 * world.lives_high))
    else:
        world.lives_high = 0x00
        world.lives_low = world.starting_lives[player].value

    world.level_colors = []
    world.color_order = []
    for i in range(72):
            world.level_colors.append(world.random.randint(0,7))
    if world.yoshi_colors[player].value == 3:
        singularity_color = world.random.randint(0,7)
        for i in range(len(world.level_colors)):
                    world.level_colors[i] = singularity_color
    elif world.yoshi_colors[player].value == 1:
        world.leader_color = world.random.randint(0,7)
        for i in range(7):
            world.color_order.append(world.random.randint(0,7))


    bonus_valid = [0x00, 0x02, 0x04, 0x06, 0x08, 0x0A]

    world.world_bonus = []
    for i in range(12):
        world.world_bonus.append(world.random.choice(bonus_valid))


def get_item_pool(world: MultiWorld, player: int, excluded_items: Set[str]) -> List[Item]:
    pool: List[Item] = []

    for name, data in item_table.items():
        if name not in excluded_items:
            for _ in range(data.count):
                item = create_item_with_correct_settings(world, player, name)
                pool.append(item)

    return pool

def create_item_with_correct_settings(world: MultiWorld, player: int, name: str) -> Item:
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

    if (name == 'Car Morph' and get_option_value(world, player, "stage_logic") != 0):
        item.classification = ItemClassification.filler

    if (name == 'Secret Lens' and (get_option_value(world, player, "hidden_object_visibility") >= 2 or get_option_value(world, player, "stage_logic") != 0)):
        item.classification = ItemClassification.useful

    if (name in ["Bonus 1", "Bonus 2", "Bonus 3", "Bonus 4", "Bonus 5", "Bonus 6", "Bonus Panels"] and get_option_value(world, player, "minigame_checks") <= 2):
        item.classification = ItemClassification.useful

    if (name in ["Bonus 1", "Bonus 3", "Bonus 4", 'Bonus Panels'] and get_option_value(world, player, "item_logic") == 1):
        item.classification = ItemClassification.progression

    return item

def setup_events(player: int, locked_locations: List[str], location_cache: List[Location]):
    for location in location_cache:
        if location.address == EventId:
            item = Item(location.name, ItemClassification.progression, EventId, player)

            locked_locations.append(location.name)

            location.place_locked_item(item)