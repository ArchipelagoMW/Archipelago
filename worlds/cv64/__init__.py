from typing import Dict, List
import os
import threading

from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from .Items import item_table, filler_items
from .Locations import get_locations, EventId
from .LogicMixin import CV64Logic
from .Options import is_option_enabled, get_option_value, cv64_options
from .Regions import create_regions
from .Rom import LocalRom, patch_rom, get_base_rom_path, CV64DeltaPatch
from ..AutoWorld import World, WebWorld


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
    game: str = "Castlevania"
    options = cv64_options
    topology_present = False
    data_version = 0
    # hint_blacklist = {LocationName.rocket_rush_flag}
    remote_items = False
    web = CV64Web()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {location.name: location.code for location in get_locations(None, None)}

    locked_locations: List[str]
    location_cache: List[Location]

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, world):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def create_regions(self):
        create_regions(self.world, self.player, get_locations(self.world, self.player),
                       self.location_cache)

    def create_item(self, name: str) -> Item:
        return create_item_with_correct_settings(self.world, self.player, name)

    def get_filler_item_name(self) -> str:
        return self.world.random.choice(filler_items)

    def set_rules(self):
        setup_events(self.player, self.locked_locations, self.location_cache)

        self.world.completion_condition[self.player] = lambda state: state.has('Youre Winner', self.player)

    def generate_basic(self):
        pool = get_item_pool(self.world, self.player)

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

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        for option_name in cv64_options:
            slot_data[option_name] = get_option_value(self.world, self.player, option_name)

        slot_data["PersonalItems"] = get_personal_items(self.player, self.location_cache)

        return slot_data


def get_item_pool(world: MultiWorld, player: int) -> List[Item]:
    pool: List[Item] = []

    for name, data in item_table.items():
        for _ in range(data.count):
            item = create_item_with_correct_settings(world, player, name)
            pool.append(item)

    return pool


def fill_item_pool_with_dummy_items(self: CV64World, world: MultiWorld, player: int, locked_locations: List[str],
                                    location_cache: List[Location], pool: List[Item]):
    for _ in range(len(location_cache) - len(locked_locations) - len(pool)):
        item = create_item_with_correct_settings(world, player, self.get_filler_item_name())
        pool.append(item)


def create_item_with_correct_settings(world: MultiWorld, player: int, name: str) -> Item:
    data = item_table[name]
    if data.progression:
        classification = ItemClassification.progression
    else:
        classification = ItemClassification.filler
    item = Item(name, classification, data.code, player)

    if not item.advancement:
        return item

    return item


def setup_events(player: int, locked_locations: List[str], location_cache: List[Location]):
    for location in location_cache:
        if location.address == EventId:
            item = Item(location.name, ItemClassification.progression, EventId, player)

            locked_locations.append(location.name)

            location.place_locked_item(item)


def get_personal_items(player: int, locations: List[Location]) -> Dict[int, int]:
    personal_items: Dict[int, int] = {}

    for location in locations:
        if location.address and location.item and location.item.code and location.item.player == player:
            personal_items[location.address] = location.item.code

    return personal_items
