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
from worlds.AutoWorld import World, WebWorld
from .Client import YISNIClient
from .Rom import LocalRom, patch_rom, get_base_rom_path, YIDeltaPatch
import Patch

class YIWeb(WebWorld):
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Yoshi's Island randomizer and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
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
    location_name_to_id = {location.name: location.code for location in get_locations(None, None, None, None)}
    item_name_groups = get_item_names_per_category()

    web = YIWeb()

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
    luigi_pieces: int

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
        spoiler_handle.write(f"\nLevels:\n1-1: {self.level_location_list[0]}\n")
        spoiler_handle.write(f"1-2: {self.level_name_list[1]}\n")
        spoiler_handle.write(f"1-3: {self.level_name_list[2]}\n")
        spoiler_handle.write(f"1-4: {self.level_name_list[3]}\n")
        spoiler_handle.write(f"1-5: {self.level_name_list[4]}\n")
        spoiler_handle.write(f"1-6: {self.level_name_list[5]}\n")
        spoiler_handle.write(f"1-7: {self.level_name_list[6]}\n")
        spoiler_handle.write(f"1-8: {self.level_name_list[7]}\n")

        spoiler_handle.write(f"\n2-1: {self.level_name_list[8]}\n")
        spoiler_handle.write(f"2-2: {self.level_name_list[9]}\n")
        spoiler_handle.write(f"2-3: {self.level_name_list[10]}\n")
        spoiler_handle.write(f"2-4: {self.level_name_list[11]}\n")
        spoiler_handle.write(f"2-5: {self.level_name_list[12]}\n")
        spoiler_handle.write(f"2-6: {self.level_name_list[13]}\n")
        spoiler_handle.write(f"2-7: {self.level_name_list[14]}\n")
        spoiler_handle.write(f"2-8: {self.level_name_list[15]}\n")

        spoiler_handle.write(f"\n3-1: {self.level_name_list[16]}\n")
        spoiler_handle.write(f"3-2: {self.level_name_list[17]}\n")
        spoiler_handle.write(f"3-3: {self.level_name_list[18]}\n")
        spoiler_handle.write(f"3-4: {self.level_name_list[19]}\n")
        spoiler_handle.write(f"3-5: {self.level_name_list[20]}\n")
        spoiler_handle.write(f"3-6: {self.level_name_list[21]}\n")
        spoiler_handle.write(f"3-7: {self.level_name_list[22]}\n")
        spoiler_handle.write(f"3-8: {self.level_name_list[23]}\n")

        spoiler_handle.write(f"\n4-1: {self.level_name_list[24]}\n")
        spoiler_handle.write(f"4-2: {self.level_name_list[25]}\n")
        spoiler_handle.write(f"4-3: {self.level_name_list[26]}\n")
        spoiler_handle.write(f"4-4: {self.level_name_list[27]}\n")
        spoiler_handle.write(f"4-5: {self.level_name_list[28]}\n")
        spoiler_handle.write(f"4-6: {self.level_name_list[29]}\n")
        spoiler_handle.write(f"4-7: {self.level_name_list[30]}\n")
        spoiler_handle.write(f"4-8: {self.level_name_list[31]}\n")

        spoiler_handle.write(f"\n5-1: {self.level_name_list[32]}\n")
        spoiler_handle.write(f"5-2: {self.level_name_list[33]}\n")
        spoiler_handle.write(f"5-3: {self.level_name_list[34]}\n")
        spoiler_handle.write(f"5-4: {self.level_name_list[35]}\n")
        spoiler_handle.write(f"5-5: {self.level_name_list[36]}\n")
        spoiler_handle.write(f"5-6: {self.level_name_list[37]}\n")
        spoiler_handle.write(f"5-7: {self.level_name_list[38]}\n")
        spoiler_handle.write(f"5-8: {self.level_name_list[39]}\n")

        spoiler_handle.write(f"\n6-1: {self.level_name_list[40]}\n")
        spoiler_handle.write(f"6-2: {self.level_name_list[41]}\n")
        spoiler_handle.write(f"6-3: {self.level_name_list[42]}\n")
        spoiler_handle.write(f"6-4: {self.level_name_list[43]}\n")
        spoiler_handle.write(f"6-5: {self.level_name_list[44]}\n")
        spoiler_handle.write(f"6-6: {self.level_name_list[45]}\n")
        spoiler_handle.write(f"6-7: {self.level_name_list[46]}\n")
        spoiler_handle.write(f"6-8: King Bowser's Castle\n")

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
        create_regions(self.multiworld, self.player, get_locations(self.multiworld, self.player, self.boss_ap_loc, self.luigi_pieces),
                        self.location_cache, self, self.boss_ap_loc, self.level_location_list, self.luigi_pieces)

    def get_filler_item_name(self) -> str:
        trap_chance: int = self.multiworld.trap_percent[self.player].value

        if self.multiworld.random.random() < (trap_chance / 100) and self.multiworld.traps_enabled[self.player].value == 1:
            return self.multiworld.random.choice(trap_items)
        else:
            return self.multiworld.random.choice(filler_items)

    def set_rules(self):
        setup_events(self.player, self.locked_locations, self.location_cache)

        self.multiworld.completion_condition[self.player] = lambda state: state.has('Saved Baby Luigi', self.player)
        #else:
            #self.multiworld.completion_condition[self.player] = lambda state: state.has('Piece of Luigi', self.player, self.NumLuigiPieces)

    def place_locked_item(self, excluded_items: Set[str], location: str, item: str) -> None:
        excluded_items.add(item)

        item = self.create_item(item)

        self.multiworld.get_location(location, self.player).place_locked_item(item)

    def generate_early(self):
        var_boss(self, self.multiworld, self.player)


    def generate_basic(self):
        self.topology_present = self.multiworld.level_shuffle[self.player]

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

        if self.topology_present:
            er_hint_data = {}
            multidata['er_hint_data'][self.player] = er_hint_data

def get_excluded_items(self: YIWorld, multiworld: MultiWorld, player: int) -> Set[str]:
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

def fill_item_pool_with_dummy_items(self: YIWorld, multiworld: MultiWorld, player: int, locked_locations: List[str],
                                    location_cache: List[Location], pool: List[Item]):

    if self.playergoal == 1:
        for i in range(multiworld.luigi_pieces_in_pool[player].value):
            pool += [self.create_item('Piece of Luigi')]

    for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)):
        item = create_item_with_correct_settings(multiworld, player, self.get_filler_item_name())
        pool.append(item)

def var_boss(self: YIWorld, multiworld: MultiWorld, player: int):
    self.playergoal = multiworld.goal[player].value
    if multiworld.luigi_pieces_in_pool[player].value < multiworld.luigi_pieces_required[player].value:
        multiworld.luigi_pieces_in_pool[self.player].value = multiworld.random.randint(multiworld.luigi_pieces_required[self.player].value, 100)
    self.luigi_pieces = multiworld.luigi_pieces_required[player].value

    if multiworld.starting_lives[player] > 255:
        self.lives_high = multiworld.starting_lives[player].value >> 8
        self.lives_low = (multiworld.starting_lives[player].value - self.lives_high) - ((255 * self.lives_high))
    else:
        self.lives_high = 0x00
        self.lives_low = multiworld.starting_lives[player].value

    self.level_colors = []
    self.color_order = []
    for i in range(72):
            self.level_colors.append(multiworld.random.randint(0,7))
    if multiworld.yoshi_colors[player].value == 3:
        singularity_color = multiworld.yoshi_singularity_color[player].value
        for i in range(len(self.level_colors)):
                    self.level_colors[i] = singularity_color
    elif multiworld.yoshi_colors[player].value == 1:
        self.leader_color = multiworld.random.randint(0,7)
        for i in range(7):
            self.color_order.append(multiworld.random.randint(0,7))

    bonus_valid = [0x00, 0x02, 0x04, 0x06, 0x08, 0x0A]

    self.world_bonus = []
    for i in range(12):
        self.world_bonus.append(multiworld.random.choice(bonus_valid))

    safe_baby_sounds = [0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20,
    0x21, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F, 0x40,
    0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 
    0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x73, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E, 0x7F, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86,
    0x87, 0x88, 0x89, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F, 0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0x9B, 0x9C, 0x9D, 0x9E, 0x9F, 0xA0, 0xA1, 0xA2]

    if multiworld.baby_mario_sound[player] == 2:
        self.baby_mario_sfx = multiworld.random.choice(safe_baby_sounds)
    elif multiworld.baby_mario_sound == 1:
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

    if multiworld.boss_shuffle[player].value == 0:
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
    elif multiworld.boss_shuffle[player] == 1:
        for i in range(11):
            multiworld.random.shuffle(self.boss_list)
            self.boss_order = self.boss_list

    self.burt_pointers = [0x3D, 0x05, 0x63, 0x00]
    self.slime_pointers = [0x70, 0x04, 0x78, 0x00]
    self.boo_pointers = [0x74, 0xBB, 0x7A, 0x00]
    self.pot_pointers = [0xCF, 0x04, 0x4D, 0x00]
    self.frog_pointers = [0xBF, 0x12, 0x62, 0x04]
    self.plant_pointers = [0x7F, 0x0D, 0x42, 0x00]
    self.milde_pointers = [0x82, 0x06, 0x64, 0x00]
    self.koop_pointers = [0x86, 0x0D, 0x78, 0x00]
    self.slug_pointers = [0x8A, 0x09, 0x7A, 0x00]
    self.raph_pointers = [0xC4, 0x03, 0x4B, 0x05]
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
        9: self.raph_pointers,
        10: self.tap_pointers
    }

    boss_levels = [0x03, 0x07, 0x0F, 0x13, 0x1B, 0x1F, 0x27, 0x2B, 0x33, 0x37, 0x3F]

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

    boss_check_list = {
        "Burt The Bashful's Boss Room": "Burt The Bashful Defeated",
        "Salvo The Slime's Boss Room": "Salvo The Slime Defeated",
        "Bigger Boo's Boss Room": "Bigger Boo Defeated",
        "Roger The Ghost's Boss Room": "Roger The Ghost Defeated",
        "Prince Froggy's Boss Room": "Prince Froggy Defeated",
        "Naval Piranha's Boss Room": "Naval Piranha Defeated",
        "Marching Milde's Boss Room": "Marching Milde Defeated",
        "Hookbill The Koopa's Boss Room": "Hookbill The Koopa Defeated",
        "Sluggy The Unshaven's Boss Room": "Sluggy The Unshaven Defeated",
        "Raphael The Raven's Boss Room": "Raphael The Raven Defeated",
        "Tap-Tap The Red Nose's Boss Room": "Tap-Tap The Red Nose Defeated",
    }

    self.boss_room_id = [boss_room_idlist[roomnum] for roomnum in self.boss_order]
    self.tap_tap_room = boss_levels[self.boss_room_id.index(10)]
    self.boss_ap_loc = [boss_check_list[roomnum] for roomnum in self.boss_order]


    for i in range(4):
        self.boss_burt_data = (pointer_dict[self.boss_room_id[0]])

    for i in range(4):
        self.boss_slime_data = (pointer_dict[self.boss_room_id[1]])

    for i in range(4):
        self.boss_boo_data = (pointer_dict[self.boss_room_id[2]])

    for i in range(4):
        self.boss_pot_data = (pointer_dict[self.boss_room_id[3]])

    for i in range(4):
        self.boss_frog_data = (pointer_dict[self.boss_room_id[4]])

    for i in range(4):
        self.boss_plant_data = (pointer_dict[self.boss_room_id[5]])

    for i in range(4):
        self.boss_milde_data = (pointer_dict[self.boss_room_id[6]])

    for i in range(4):
        self.boss_koop_data = (pointer_dict[self.boss_room_id[7]])

    for i in range(4):
        self.boss_slug_data = (pointer_dict[self.boss_room_id[8]])

    for i in range(4):
        self.boss_raph_data = (pointer_dict[self.boss_room_id[9]])

    for i in range(4):
        self.boss_tap_data = (pointer_dict[self.boss_room_id[10]])

    
    self.global_level_list = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 
                              0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13,
                              0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F,
                              0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B,
                              0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
                              0x3C, 0x3D, 0x3E, 0x3F, 0x40, 0x41, 0x42]
    level_id_list = {
                    0x00: "Make Eggs, Throw Eggs",
                    0x01: "Watch Out Below!",
                    0x02: "The Cave Of Chomp Rock",
                    0x03: "Burt The Bashful's Fort",
                    0x04: "Hop! Hop! Donut Lifts",
                    0x05: "Shy-Guys On Stilts",
                    0x06: "Touch Fuzzy Get Dizzy",
                    0x07: "Salvo The Slime's Castle",
                    0x0C: "Visit Koopa And Para-Koopa",
                    0x0D: "The Baseball Boys",
                    0x0E: "What's Gusty Taste Like?",
                    0x0F: "Bigger Boo's Fort",
                    0x10: "Watch Out For Lakitu",
                    0x11: "The Cave Of The Mystery Maze",
                    0x12: "Lakitu's Wall",
                    0x13: "The Potted Ghost's Castle",
                    0x18: "Welcome To Monkey World!",
                    0x19: "Jungle Rhythm...",
                    0x1A: "Nep-Enuts' Domain",
                    0x1B: "Prince Froggy's Fort",
                    0x1C: "Jammin' Through The Trees",
                    0x1D: "The Cave Of Harry Hedgehog",
                    0x1E: "Monkeys' Favorite Lake",
                    0x1F: "Naval Piranha's Castle",
                    0x24: "GO! GO! MARIO!!",
                    0x25: "The Cave Of The Lakitus",
                    0x26: "Don't Look Back!",
                    0x27: "Marching Milde's Fort",
                    0x28: "Chomp Rock Zone",
                    0x29: "Lake Shore Paradise",
                    0x2A: "Ride Like The Wind",
                    0x2B: "Hookbill The Koopa's Castle",
                    0x30: "BLIZZARD!!!",
                    0x31: "Ride The Ski Lifts",
                    0x32: "Danger - Icy Conditions Ahead",
                    0x33: "Sluggy The Unshaven's Fort",
                    0x34: "Goonie Rides!",
                    0x35: "Welcome To Cloud World",
                    0x36: "Shifting Platforms Ahead",
                    0x37: "Raphael The Raven's Castle",
                    0x3C: "Scary Skeleton Goonies!",
                    0x3D: "The Cave Of The Bandits",
                    0x3E: "Beware The Spinning Logs",
                    0x3F: "Tap-Tap The Red Nose's Fort",
                    0x40: "The Very Loooooong Cave",
                    0x41: "The Deep, Underground Maze",
                    0x42: "KEEP MOVING!!!!"
                        }

    level_names = {
                    0x00: "Make Eggs, Throw Eggs",
                    0x01: "Watch Out Below!",
                    0x02: "The Cave Of Chomp Rock",
                    0x03: "Burt The Bashful's Fort",
                    0x04: "Hop! Hop! Donut Lifts",
                    0x05: "Shy-Guys On Stilts",
                    0x06: "Touch Fuzzy Get Dizzy",
                    0x07: "Salvo The Slime's Castle",
                    0x0C: "Visit Koopa And Para-Koopa",
                    0x0D: "The Baseball Boys",
                    0x0E: "What's Gusty Taste Like?",
                    0x0F: "Bigger Boo's Fort",
                    0x10: "Watch Out For Lakitu",
                    0x11: "The Cave Of The Mystery Maze",
                    0x12: "Lakitu's Wall",
                    0x13: "The Potted Ghost's Castle",
                    0x18: "Welcome To Monkey World!",
                    0x19: "Jungle Rhythm...",
                    0x1A: "Nep-Enuts' Domain",
                    0x1B: "Prince Froggy's Fort",
                    0x1C: "Jammin' Through The Trees",
                    0x1D: "The Cave Of Harry Hedgehog",
                    0x1E: "Monkeys' Favorite Lake",
                    0x1F: "Naval Piranha's Castle",
                    0x24: "GO! GO! MARIO!!",
                    0x25: "The Cave Of The Lakitus",
                    0x26: "Don't Look Back!",
                    0x27: "Marching Milde's Fort",
                    0x28: "Chomp Rock Zone",
                    0x29: "Lake Shore Paradise",
                    0x2A: "Ride Like The Wind",
                    0x2B: "Hookbill The Koopa's Castle",
                    0x30: "BLIZZARD!!!",
                    0x31: "Ride The Ski Lifts",
                    0x32: "Danger - Icy Conditions Ahead",
                    0x33: "Sluggy The Unshaven's Fort",
                    0x34: "Goonie Rides!",
                    0x35: "Welcome To Cloud World",
                    0x36: "Shifting Platforms Ahead",
                    0x37: "Raphael The Raven's Castle",
                    0x3C: "Scary Skeleton Goonies!",
                    0x3D: "The Cave Of The Bandits",
                    0x3E: "Beware The Spinning Logs",
                    0x3F: "Tap-Tap The Red Nose's Fort",
                    0x40: "The Very Loooooong Cave",
                    0x41: "The Deep, Underground Maze",
                    0x42: "KEEP MOVING!!!!"
                        }

    self.world_1_offsets = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00]
    self.world_2_offsets = [0x01, 0x01, 0x00, 0x00, 0x00, 0x00]
    self.world_3_offsets = [0x01, 0x01, 0x01, 0x00, 0x00, 0x00]
    self.world_4_offsets = [0x01, 0x01, 0x01, 0x01, 0x00, 0x00]
    self.world_5_offsets = [0x01, 0x01, 0x01, 0x01, 0x01, 0x00]
    self.easy_start_lv = [0x02, 0x04, 0x06, 0x0E, 0x10, 0x18, 0x1C, 0x28, 0x30, 0x31, 0x35, 0x36, 0x3E, 0x40, 0x42]
    self.norm_start_lv = [0x00, 0x01, 0x02, 0x04, 0x06, 0x0E, 0x10, 0x12, 0x18, 0x1A, 0x1C, 0x1E, 0x28, 0x30, 0x31, 0x34, 0x35, 0x36, 0x3D, 0x3E, 0x40, 0x42]
    self.hard_start_lv = [0x00, 0x01, 0x02, 0x04, 0x06, 0x0D, 0x0E, 0x10, 0x11, 0x12, 0x18, 0x1A, 0x1C, 0x1E, 0x24, 0x25, 0x26, 0x28, 0x29, 0x2B, 0x30, 0x31, 0x34, 0x35, 0x36, 0x3D, 0x3E, 0x40, 0x42]
    self.diff_index = [self.easy_start_lv, self.norm_start_lv, self.hard_start_lv]
    self.diff_level = self.diff_index[multiworld.stage_logic[player].value]
    self.boss_lv = [0x03, 0x07, 0x0F, 0x13, 0x1B, 0x1F, 0x27, 0x2B, 0x33, 0x37, 0x3F]
    self.world_start_lv = [0, 8, 16, 24, 32, 40]
    if multiworld.shuffle_midrings[player].value == 1:
        self.easy_start_lv.extend([0x1A, 0x24, 0x34])
        self.norm_start_lv.extend([0x24, 0x37, 0x3C])
        self.hard_start_lv.extend([0x1D, 0x3C])

    if multiworld.level_shuffle[player].value != 1:
        self.norm_start_lv.extend([0x37, 0x3C])
        self.hard_start_lv.extend([0x07, 0x1B, 0x1F, 0x2B, 0x33, 0x37])
        if multiworld.shuffle_midrings[player].value ==1:
            self.easy_start_lv.extend([0x1B])
            self.norm_start_lv.extend([0x1B, 0x2B, 0x37])

    self.starting_level = multiworld.random.choice(self.diff_level)
    self.starting_level_entrance = self.world_start_lv[multiworld.starting_world[player].value]
    if multiworld.level_shuffle[player].value != 0:
        self.global_level_list.remove(self.starting_level)
        multiworld.random.shuffle(self.global_level_list)
        if multiworld.level_shuffle[player].value == 1:
            for i in range(11):
                self.global_level_list = [item for item in self.global_level_list if item not in self.boss_lv]
            multiworld.random.shuffle(self.boss_lv)
            self.global_level_list.insert(3 - self.world_1_offsets[multiworld.starting_world[player].value], self.boss_lv[0]) #1 if starting world is 1, 0 otherwise
            self.global_level_list.insert(7 - self.world_1_offsets[multiworld.starting_world[player].value], self.boss_lv[1])
            self.global_level_list.insert(11 - self.world_2_offsets[multiworld.starting_world[player].value], self.boss_lv[2])
            self.global_level_list.insert(15 - self.world_2_offsets[multiworld.starting_world[player].value], self.boss_lv[3])
            self.global_level_list.insert(19 - self.world_3_offsets[multiworld.starting_world[player].value], self.boss_lv[4])
            self.global_level_list.insert(23 - self.world_3_offsets[multiworld.starting_world[player].value], self.boss_lv[5])
            self.global_level_list.insert(27 - self.world_4_offsets[multiworld.starting_world[player].value], self.boss_lv[6])
            self.global_level_list.insert(31 - self.world_4_offsets[multiworld.starting_world[player].value], self.boss_lv[7])
            self.global_level_list.insert(35 - self.world_5_offsets[multiworld.starting_world[player].value], self.boss_lv[8])
            self.global_level_list.insert(39 - self.world_5_offsets[multiworld.starting_world[player].value], self.boss_lv[9])
            self.global_level_list.insert(43 - 1, self.boss_lv[10])
        self.global_level_list.insert(self.starting_level_entrance, self.starting_level)
    self.level_location_list = [level_id_list[LevelID] for LevelID in self.global_level_list]
    self.level_name_list = [level_names[LevelID] for LevelID in self.global_level_list]

    level_panel_dict = {
                    0x00: [0x04, 0x04, 0x53],
                    0x01: [0x20, 0x04, 0x53],
                    0x02: [0x3C, 0x04, 0x53],
                    0x03: [0x58, 0x04, 0x53],
                    0x04: [0x74, 0x04, 0x53],
                    0x05: [0x90, 0x04, 0x53],
                    0x06: [0xAC, 0x04, 0x53],
                    0x07: [0xC8, 0x04, 0x53],
                    0x0C: [0x04, 0x24, 0x53],
                    0x0D: [0x20, 0x24, 0x53],
                    0x0E: [0x3C, 0x24, 0x53],
                    0x0F: [0x58, 0x24, 0x53],
                    0x10: [0x74, 0x24, 0x53],
                    0x11: [0x90, 0x24, 0x53],
                    0x12: [0xAC, 0x24, 0x53],
                    0x13: [0xC8, 0x24, 0x53],
                    0x18: [0x04, 0x44, 0x53],
                    0x19: [0x20, 0x44, 0x53],
                    0x1A: [0x3C, 0x44, 0x53],
                    0x1B: [0x58, 0x44, 0x53],
                    0x1C: [0x74, 0x44, 0x53],
                    0x1D: [0x90, 0x44, 0x53],
                    0x1E: [0xAC, 0x44, 0x53],
                    0x1F: [0xC8, 0x44, 0x53],
                    0x24: [0x04, 0x64, 0x53],
                    0x25: [0x20, 0x64, 0x53],
                    0x26: [0x3C, 0x64, 0x53],
                    0x27: [0x58, 0x64, 0x53],
                    0x28: [0x74, 0x64, 0x53],
                    0x29: [0x90, 0x64, 0x53],
                    0x2A: [0xAC, 0x64, 0x53],
                    0x2B: [0xC8, 0x64, 0x53],
                    0x30: [0x04, 0x04, 0x53],
                    0x31: [0x20, 0x04, 0x53],
                    0x32: [0x3C, 0x04, 0x53],
                    0x33: [0x58, 0x04, 0x53],
                    0x34: [0x74, 0x04, 0x53],
                    0x35: [0x90, 0x04, 0x53],
                    0x36: [0xAC, 0x04, 0x53],
                    0x37: [0xC8, 0x04, 0x53],
                    0x3C: [0x04, 0x24, 0x53],
                    0x3D: [0x20, 0x24, 0x53],
                    0x3E: [0x3C, 0x24, 0x53],
                    0x3F: [0x58, 0x24, 0x53],
                    0x40: [0x74, 0x24, 0x53],
                    0x41: [0x90, 0x24, 0x53],
                    0x42: [0xAC, 0x24, 0x53]
                        }
    self.panel_palette_1 = [0x00, 0x03, 0x04, 0x05, 0x0C, 0x10, 0x12, 0x13, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x24, 0x26, 0x27, 0x29, 0x2A, 0x2B, 0x30, 0x32, 0x34, 0x35, 0x37, 0x3C, 0x3D, 0x40, 0x41] #000C
    self.panel_palette_2 = [0x01, 0x02, 0x06, 0x07, 0x0D, 0x0E, 0x0F, 0x11, 0x18, 0x1E, 0x1F, 0x25, 0x28, 0x31, 0x33, 0x36, 0x3E, 0x3F, 0x42] #0010

    stage_number = 0
    world_number = 1
    for i in range(47):
        stage_number += 1
        if stage_number >= 9:
            world_number += 1
            stage_number = 1
        for j in range(3):
            setattr(self, f'_{world_number}{stage_number}StageGFX', level_panel_dict[self.global_level_list[i]])

    self.level_gfx_table = []
    self.palette_panel_list = []

    for i in range(47):
        if self.global_level_list[i] >=0x30:
            self.level_gfx_table.append(0x15)
        else:
            self.level_gfx_table.append(0x11)
        
        if self.global_level_list[i] in self.panel_palette_1:
            self.palette_panel_list.extend([0x00, 0x0C])
        elif self.global_level_list[i] in self.panel_palette_2:
            self.palette_panel_list.extend([0x00, 0x10])

    self.palette_panel_list[16:16] = [0x00, 0x0c, 0x00, 0x0c, 0x00, 0x18, 0x00, 0x18]
    self.palette_panel_list[40:40] = [0x00, 0x0c, 0x00, 0x0c, 0x00, 0x18, 0x00, 0x18]
    self.palette_panel_list[64:64] = [0x00, 0x0c, 0x00, 0x0c, 0x00, 0x18, 0x00, 0x18]
    self.palette_panel_list[88:88] = [0x00, 0x0c, 0x00, 0x0c, 0x00, 0x18, 0x00, 0x18]
    self.palette_panel_list[112:112] = [0x00, 0x0c, 0x00, 0x0c, 0x00, 0x18, 0x00, 0x18]

    self.level_gfx_table.insert(8, 0x15)
    self.level_gfx_table.insert(8, 0x15)
    self.level_gfx_table.insert(8, 0x15)
    self.level_gfx_table.insert(8, 0x11)

    self.level_gfx_table.insert(20, 0x15)
    self.level_gfx_table.insert(20, 0x15)
    self.level_gfx_table.insert(20, 0x15)
    self.level_gfx_table.insert(20, 0x11)

    self.level_gfx_table.insert(32, 0x15)
    self.level_gfx_table.insert(32, 0x15)
    self.level_gfx_table.insert(32, 0x15)
    self.level_gfx_table.insert(32, 0x11)

    self.level_gfx_table.insert(44, 0x15)
    self.level_gfx_table.insert(44, 0x15)
    self.level_gfx_table.insert(44, 0x15)
    self.level_gfx_table.insert(44, 0x11)

    self.level_gfx_table.insert(56, 0x15)
    self.level_gfx_table.insert(56, 0x15)
    self.level_gfx_table.insert(56, 0x15)
    self.level_gfx_table.insert(56, 0x15)
    
    
    #Need to make this more efficient. I need to find the values to insert for worlds 5 and 6 in the morning. Probably just 9 more, probably all 15. Also, maybe double check the level GFX?

    castle_door_dict = {
                    0: [0xB8, 0x05, 0x77, 0x00],
                    1: [0xB8, 0x05, 0x77, 0x00],
                    2: [0xC6, 0x07, 0x7A, 0x00],
                    3: [0xCD, 0x05, 0x5B, 0x00],
                    4: [0xD3, 0x00, 0x77, 0x06],
                    5: [0xB8, 0x05, 0x77, 0x00]
    }

    self.castle_door = castle_door_dict[multiworld.bowser_door_mode[player].value]
    

    





def get_item_pool(multiworld: MultiWorld, player: int, excluded_items: Set[str]) -> List[Item]:
    pool: List[Item] = []

    for name, data in item_table.items():
        if name not in excluded_items:
            for _ in range(data.count):
                item = create_item_with_correct_settings(multiworld, player, name)
                pool.append(item)

    return pool

def create_item_with_correct_settings(multiworld: MultiWorld, player: int, name: str) -> Item:
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

    if (name == 'Car Morph' and get_option_value(multiworld, player, "stage_logic") != 0):
        item.classification = ItemClassification.useful

    if (name == 'Secret Lens' and (get_option_value(multiworld, player, "hidden_object_visibility") >= 2 or get_option_value(multiworld, player, "stage_logic") != 0)):
        item.classification = ItemClassification.useful

    if (name in ["Bonus 1", "Bonus 2", "Bonus 3", "Bonus 4", "Bonus 5", "Bonus 6", "Bonus Panels"] and get_option_value(multiworld, player, "minigame_checks") <= 2):
        item.classification = ItemClassification.useful

    if (name in ["Bonus 1", "Bonus 3", "Bonus 4", 'Bonus Panels'] and get_option_value(multiworld, player, "item_logic") == 1):
        item.classification = ItemClassification.progression

    for i in range((multiworld.luigi_pieces_in_pool[player].value) - (multiworld.luigi_pieces_required[player].value)):
        if name == 'Piece of Luigi':
            item.classification = ItemClassification.Useful

    return item

def setup_events(player: int, locked_locations: List[str], location_cache: List[Location]):
    for location in location_cache:
        if location.address == EventId:
            item = Item(location.name, ItemClassification.progression, EventId, player)

            locked_locations.append(location.name)

            location.place_locked_item(item)