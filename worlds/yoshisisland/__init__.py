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
    lives_high: int
    lives_low: int
    castle_bosses: int
    bowser_bosses: int
    baby_mario_sfx: int
    leader_color: int
    boss_order: list
    boss_burt: int

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

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"Burt The Bashful's Boss Door:      {self.boss_order[0]}\n")
        spoiler_handle.write(f"Salvo The Slime's Boss Door:       {self.boss_order[1]}\n")
        spoiler_handle.write(f"Bigger Boo's Boss Door:            {self.boss_order[2]}\n")
        spoiler_handle.write(f"Roger The Ghost's Boss Door:       {self.boss_order[3]}\n")
        spoiler_handle.write(f"Prince Froggy's Boss Door:         {self.boss_order[4]}\n")
        spoiler_handle.write(f"Naval Piranha's Boss Door:         {self.boss_order[5]}\n")
        spoiler_handle.write(f"Marching Milde's Boss Door:        {self.boss_order[6]}\n")
        spoiler_handle.write(f"Hookbill The Koopa's Boss Door:    {self.boss_order[7]}\n")
        spoiler_handle.write(f"Sluggy The Unshaven's Boss Door:   {self.boss_order[8]}\n")
        spoiler_handle.write(f"Raphael The Raven's Boss Door:     {self.boss_order[9]}\n")
        spoiler_handle.write(f"Tap-Tap The Red Nose's Boss Door:  {self.boss_order[10]}\n")

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
                        self.location_cache, self)

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
            patch_rom(self, rom, self.player, self.multiworld)

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

def var_boss(self: YIWorld, world: MultiWorld, player: int):
    if world.starting_lives[player] > 255:
        self.lives_high = world.starting_lives[player].value >> 8
        self.lives_low = (world.starting_lives[player].value - self.lives_high) - ((255 * self.lives_high))
    else:
        self.lives_high = 0x00
        self.lives_low = world.starting_lives[player].value

    self.level_colors = []
    self.color_order = []
    for i in range(72):
            self.level_colors.append(world.random.randint(0,7))
    if world.yoshi_colors[player].value == 3:
        singularity_color = world.yoshi_singularity_color[player].value
        for i in range(len(self.level_colors)):
                    self.level_colors[i] = singularity_color
    elif world.yoshi_colors[player].value == 1:
        self.leader_color = world.random.randint(0,7)
        for i in range(7):
            self.color_order.append(world.random.randint(0,7))

    bonus_valid = [0x00, 0x02, 0x04, 0x06, 0x08, 0x0A]

    self.world_bonus = []
    for i in range(12):
        self.world_bonus.append(world.random.choice(bonus_valid))

    safe_baby_sounds = [0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20,
    0x21, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F, 0x40,
    0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 
    0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x73, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E, 0x7F, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86,
    0x87, 0x88, 0x89, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F, 0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0x9B, 0x9C, 0x9D, 0x9E, 0x9F, 0xA0, 0xA1, 0xA2]

    if world.baby_mario_sound[player] == 2:
        self.baby_mario_sfx = world.random.choice(safe_baby_sounds)
    elif world.baby_mario_sound == 1:
        self.baby_mario_sfx = 0x42
    else:
        self.baby_mario_sfx = 0x44

    self.boss_list = ["Burt The Bashful's Boss Room", "Salvo The Slime's Boss Room",
                 "Bigger Boo's Boss Room", "Roger The Ghost's Boss Room",
                "Prince Froggy's Boss Room", "Naval Piranha's Boss Room",
                "Marching Milde's Boss Room", "Hookbill The Koopa's Boss Room",
                "Sluggy The Unshaven's Boss Room", "Raphael The Raven's Boss Room",
                "Tap-Tap The Red Nose's Boss Room"]

    self.boss_order = []

    if world.boss_shuffle[player].value == 0:
        self.boss_order.append("Burt The Bashful's Boss Room")
        self.boss_order.append("Salvo The Slime's Boss Room")
        self.boss_order.append("Bigger Boo's Boss Room")
        self.boss_order.append("Roger The Ghost's Boss Room")
        self.boss_order.append("Prince Froggy's Boss Room")
        self.boss_order.append("Naval Piranha's Boss Room")
        self.boss_order.append("Marching Milde's Boss Room")
        self.boss_order.append("Hookbill The Koopa's Boss Room")
        self.boss_order.append("Sluggy The Unshaven's Boss Room")
        self.boss_order.append("Raphael The Raven's Boss Room")
        self.boss_order.append("Tap-Tap The Red Nose's Boss Room")
    elif world.boss_shuffle[player] == 1:
        for i in range(11):
            world.random.shuffle(self.boss_list)
            self.boss_order = self.boss_list

    self.burt_pointers = [0x3D, 0x05, 0x63, 0x00]
    self.slime_pointers = [0x70, 0x04, 0x78, 0x00]
    self.boo_pointers = [0x74, 0xBB, 0x7A, 0x00]
    self.pot_pointers = [0xBE, 0x18, 0x4A, 0x00]
    self.frog_pointers = [0xBF, 0x12, 0x62, 0x04]
    self.plant_pointers = [0x7F, 0x0D, 0x42, 0x00]
    self.milde_pointers = [0x82, 0x06, 0x64, 0x00]
    self.koop_pointers = [0x86, 0x0D, 0x78, 0x00]
    self.slug_pointers = [0x8A, 0x09, 0x7A, 0x00]
    self.raph_points = [0xC4, 0x03, 0x4B, 0x05]
    self.tap_pointers = [0xCC, 0x49, 0x64, 0x02]

    pointer_dict = {
        0: self.burt_pointers,
        1: self.slime_pointers,
        2: self.boo_pointers,
        3: self.pot_pointers,
        4: self.frog_pointers,
        5: self.plant_pointers,
        6: self.milde_pointers,
        7: self.koop_pointers,
        8: self.slug_pointers,
        9: self.raph_points,
        10: self.tap_pointers
    }

    boss_room_idlist = {
        "Burt The Bashful's Boss Room": 0,
        "Salvo The Slime's Boss Room": 1,
        "Bigger Boo's Boss Room": 2,
        "Roger The Ghost's Boss Room": 3,
        "Prince Froggy's Boss Room": 4,
        "Naval Piranha's Boss Room": 5,
        "Marching Milde's Boss Room": 6,
        "Hookbill The Koopa's Boss Room": 7,
        "Sluggy The Unshaven's Boss Room": 8,
        "Raphael The Raven's Boss Room": 9,
        "Tap-Tap The Red Nose's Boss Room": 10,
    }


    for i in range(4):
        self.boss_burt_data = (pointer_dict[self.boss_order.index("Burt The Bashful's Boss Room")])

    for i in range(4):
        self.boss_slime_data = (pointer_dict[self.boss_order.index("Salvo The Slime's Boss Room")])

    for i in range(4):
        self.boss_boo_data = (pointer_dict[self.boss_order.index("Bigger Boo's Boss Room")])

    for i in range(4):
        self.boss_pot_data = (pointer_dict[self.boss_order.index("Roger The Ghost's Boss Room")])

    for i in range(4):
        self.boss_frog_data = (pointer_dict[self.boss_order.index("Prince Froggy's Boss Room")])

    for i in range(4):
        self.boss_plant_data = (pointer_dict[self.boss_order.index("Naval Piranha's Boss Room")])

    for i in range(4):
        self.boss_milde_data = (pointer_dict[self.boss_order.index("Marching Milde's Boss Room")])

    for i in range(4):
        self.boss_koop_data = (pointer_dict[self.boss_order.index("Hookbill The Koopa's Boss Room")])

    for i in range(4):
        self.boss_slug_data = (pointer_dict[self.boss_order.index("Sluggy The Unshaven's Boss Room")])

    for i in range(4):
        self.boss_raph_data = (pointer_dict[self.boss_order.index("Raphael The Raven's Boss Room")])

    for i in range(4):
        self.boss_tap_data = (pointer_dict[self.boss_order.index("Tap-Tap The Red Nose's Boss Room")])

    self.boss_room_id = [boss_room_idlist[roomnum] for roomnum in self.boss_order]



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