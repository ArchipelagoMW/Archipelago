import os
import typing
import math
import threading
import pdb 

from typing import Dict, List, Set, Tuple, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from .Items import get_item_names_per_category, item_table, filler_items
from .Locations import get_locations, EventId
from .LogicMixin import LogicComplex
from .Options import is_option_enabled, get_option_value, yoshi_options
from .Regions import create_regions
from ..AutoWorld import World, WebWorld
from .Rom import LocalRom, patch_rom, get_base_rom_path, YIDeltaPatch
import Patch


class YIWeb(WebWorld):
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "test",
        "ill",
        "write",
        "this",
        "later"
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

    locked_locations: List[str]
    location_cache: List[Location]


    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

        self.locked_locations= []
        self.location_cache= []

    def create_item(self, name: str) -> Item:
        return create_item_with_correct_settings(self.world, self.player, name)

    def generate_early(self):
        # in generate_early the start_inventory isnt copied over to precollected_items yet, so we can still modify the options directly
        if self.world.start_inventory[self.player].value.pop('Middle Ring', 0) > 0:
            self.world.StartWithMidRings[self.player].value = self.world.StartWithMidRings[self.player].option_true


    def create_regions(self):
        create_regions(self.world, self.player, get_locations(self.world, self.player),
                        self.location_cache)



    def get_filler_item_name(self) -> str:
        return self.world.random.choice(filler_items)

    def set_rules(self):
        setup_events(self.player, self.locked_locations, self.location_cache)

        self.world.completion_condition[self.player] = lambda state: state.has('Saved Baby Luigi', self.player)

    def generate_basic(self):
        
        if self.world.castle_open_condition[self.player] == 1 or self.world.castle_clear_condition == 1:
            self.world.get_location("Salvo The Slime's Castle: Flag", self.player).place_locked_item(self.create_item("World Flag"))
            self.world.get_location("The Potted Ghost's Castle: Flag", self.player).place_locked_item(self.create_item("World Flag"))
            self.world.get_location("Naval Piranha's Castle: Flag", self.player).place_locked_item(self.create_item("World Flag"))
            self.world.get_location("Hookbill The Koopa's Castle: Flag", self.player).place_locked_item(self.create_item("World Flag"))
            self.world.get_location("Raphael The Raven's Castle: Flag", self.player).place_locked_item(self.create_item("World Flag"))


        excluded_items = get_excluded_items(self, self.world, self.player)

        pool = get_item_pool(self.world, self.player, excluded_items)

        fill_item_pool_with_dummy_items(self, self.world, self.player, self.locked_locations, self.location_cache, pool)

        self.world.itempool += pool

    def generate_output(self, output_directory: str):
        try:
            world = self.world
            player = self.player
            rom = LocalRom(get_base_rom_path())
            patch_rom(self.world, rom, self.player)



            outfilepname = f'_P{player}'
            outfilepname += f"_{world.player_name[player].replace(' ', '_')}" \
                if world.player_name[player] != 'Player%d' % player else ''

            rompath = os.path.join(output_directory, f'AP_{world.seed_name}{outfilepname}.sfc')
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = YIDeltaPatch(os.path.splitext(rompath)[0]+YIDeltaPatch.patch_file_ending, player=player,
                                  player_name=world.player_name[player], patched_path=rompath)
            patch.write()
        except:
            raise
        finally:
            if os.path.exists(rompath):
                os.unlink(rompath)
            self.rom_name_available_event.set() # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.world.player_name[self.player]]











def get_excluded_items(self: YIWorld, world: MultiWorld, player: int) -> Set[str]:
    excluded_items: Set[str] = set()

    if is_option_enabled(world, player, "start_with_middle_rings"):
        excluded_items.add('Middle Ring')

    if get_option_value(world, player, "extras_enabled") == False:
        excluded_items.add('Extra Panels')
        excluded_items.add('Extra 1'),
        excluded_items.add('Extra 2'),
        excluded_items.add('Extra 3'),
        excluded_items.add('Extra 4'),
        excluded_items.add('Extra 5'),
        excluded_items.add('Extra 6')
    else:    
        if get_option_value(world, player, "split_extra") == True:
            excluded_items.add('Extra Panels')
        else:
            excluded_items.add('Extra 1'),
            excluded_items.add('Extra 2'),
            excluded_items.add('Extra 3'),
            excluded_items.add('Extra 4'),
            excluded_items.add('Extra 5'),
            excluded_items.add('Extra 6')
        

    if get_option_value(world, player, "split_bonus") == True:
        excluded_items.add('Bonus Panels')
    else:
        excluded_items.add('Bonus 1'),
        excluded_items.add('Bonus 2'),
        excluded_items.add('Bonus 3'),
        excluded_items.add('Bonus 4'),
        excluded_items.add('Bonus 5'),
        excluded_items.add('Bonus 6'),

    if get_option_value(world, player, "starting_world") == 0:
        excluded_items.add('World 1 Gate')
    elif get_option_value(world, player, "starting_world") == 1:
        excluded_items.add('World 2 Gate')
    elif get_option_value(world, player, "starting_world") == 2:
        excluded_items.add('World 3 Gate')
    elif get_option_value(world, player, "starting_world") == 3:
        excluded_items.add('World 4 Gate')
    elif get_option_value(world, player, "starting_world") == 4:
        excluded_items.add('World 5 Gate')
    elif get_option_value(world, player, "starting_world") == 5:
        excluded_items.add('World 6 Gate')

    for item in world.precollected_items[player]:
        if item.name not in self.item_name_groups['UseItem']:
            excluded_items.add(item.name)

    return excluded_items


def fill_item_pool_with_dummy_items(self: YIWorld, world: MultiWorld, player: int, locked_locations: List[str],
                                    location_cache: List[Location], pool: List[Item]):
    for _ in range(len(location_cache) - len(locked_locations) - len(pool)):
        item = create_item_with_correct_settings(world, player, self.get_filler_item_name())
        pool.append(item)

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

    if (name == "Secret Lens" and get_option_value(world, player, "stage_logic") > 1 or get_option_value(world, player, "hidden_object_visibility") >= 2):
        item.classification = ItemClassification.filler


    return item
    
def setup_events(player: int, locked_locations: List[str], location_cache: List[Location]):
    for location in location_cache:
        if location.address == EventId:
            item = Item(location.name, ItemClassification.progression, EventId, player)

            locked_locations.append(location.name)

            location.place_locked_item(item)



