import base64
import os
import typing
import threading
import pkgutil


from typing import List, Set, Dict, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from Options import OptionGroup
from Fill import fill_restrictive
import settings
from .Items import get_item_names_per_category, item_table
from .Locations import get_locations, static_locations
from .Regions import init_areas
from .Options import Z2Options, z2_option_groups
from .setup_game import setup_gamevars, place_static_items, add_keys
from .Client import Zelda2Client
from .Rules import set_location_rules, set_region_rules
from .Rom import patch_rom, get_base_rom_path, Z2ProcPatch
from .game_data import world_version
from worlds.generic.Rules import add_item_rule, forbid_items_for_player
from logging import warning


class Z2Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Zelda 2 US ROM"""
        description = "Zelda 2 ROM File"
        copy_to = "Zelda 2.nes"
        md5 = "764d36fa8a2450834da5e8194281035a"

    rom_file: RomFile = RomFile(RomFile.copy_to)


class Z2Web(WebWorld):
    theme = "grass"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Zelda 2 randomizer"
        "and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    tutorials = [setup_en]

    option_groups = z2_option_groups


class Z2World(World):
    """In the exciting sequel to Legend of Zelda, Link must find the Triforce of Courage in the Great Palace
       to awaken Zelda, cursed with a sleeping spell. Along the wy, he is being hunted by Ganon's followers,
       who seek to use his blood to revive their master."""
    
    game = "Zelda II: The Adventure of Link"
    option_definitions = Z2Options
    data_version = 1
    required_client_version = (0, 5, 0)

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = static_locations
    item_name_groups = get_item_names_per_category()

    web = Z2Web()
    settings: typing.ClassVar[Z2Settings]

    options_dataclass = Z2Options
    options: Z2Options

    locked_locations: List[str]
    location_cache: List[Location]

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

        self.locked_locations = []
        self.location_cache = []
        self.extra_items = []
        self.extra_count = 39
        self.world_version = world_version
        self.filler_items = ["50 Point P-Bag", "100 Point P-Bag", "200 Point P-Bag", "500 Point P-Bag",
                             "1-Up Doll", "Blue Magic Jar", "Red Magic Jar"]

    def generate_early(self):  # Todo: place locked items in generate_early
        if self.options.key_shuffle < 2:
            self.options.local_items.value.add("Parapa Palace Key")
            self.options.local_items.value.add("Midoro Palace Key")
            self.options.local_items.value.add("Island Palace Key")
            self.options.local_items.value.add("Maze Palace Key")
            self.options.local_items.value.add("Sea Palace Key")
            self.options.local_items.value.add("Three-Eye Rock Palace Key")

        if self.options.remove_magical_key and not self.options.key_shuffle:
            warning(f"Warning: {self.multiworld.get_player_name(self.player)} attempted to have Vanilla keys with no Magic Key. Magic Key will be added.")
            self.options.remove_magical_key.value = 0

        if self.options.remove_magical_key and self.options.key_shuffle:
            self.extra_count += 5

        setup_gamevars(self)
        add_keys(self)

    def create_regions(self) -> None:
        init_areas(self, get_locations(self))

    def create_items(self) -> None:
        pool = self.get_item_pool()
        pool += self.extra_items
        self.generate_filler(pool)

        self.multiworld.itempool += pool

    def set_rules(self) -> None:
        set_location_rules(self)
        set_region_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Triforce of Courage", self.player)

    def pre_fill(self) -> None:
        place_static_items(self)
        if self.options.spell_locations == 1:
            spells = [
                self.create_item("Shield Spell"),
                self.create_item("Jump Spell"),
                self.create_item("Life Spell"),
                self.create_item("Fairy Spell"),
                self.create_item("Fire Spell"),
                self.create_item("Reflect Spell"),
                self.create_item("Thunder Spell"),
                self.create_item("Spell Spell")
            ]

            old_men = [
                self.multiworld.get_location("Sage of Rauru", self.player),
                self.multiworld.get_location("Sage of Ruto", self.player),
                self.multiworld.get_location("Sage of Saria", self.player),
                self.multiworld.get_location("Sage of Mido", self.player),
                self.multiworld.get_location("Sage of Nabooru", self.player),
                self.multiworld.get_location("Sage of Darunia", self.player),
                self.multiworld.get_location("Sage of Kasuto", self.player),
                self.multiworld.get_location("Sage of New Kasuto", self.player),
            ]

            fill_restrictive(self.multiworld, self.multiworld.get_all_state(False), old_men, spells, True, True)

        if self.options.key_shuffle == 1:
            state = self.multiworld.get_all_state(False)
            parapa_palace_checks = [
                self.multiworld.get_location("Parapa Palace: Horsehead Drop", self.player),
                self.multiworld.get_location("Parapa Palace: Pedestal Item", self.player),
                self.multiworld.get_location("Parapa Palace: Crumbling Bridge", self.player),
                self.multiworld.get_location("Parapa Palace: Stairwell", self.player),
                self.multiworld.get_location("Parapa Palace: Guarded Item", self.player),
            ]

            midoro_palace_checks = [
                self.multiworld.get_location("Midoro Palace: B2F Hall", self.player),
                self.multiworld.get_location("Midoro Palace: Lava Blocks Item", self.player),
                self.multiworld.get_location("Midoro Palace: Floating Block Hall", self.player),
                self.multiworld.get_location("Midoro Palace: Falling Blocks Item", self.player),
                self.multiworld.get_location("Midoro Palace: Pedestal Item", self.player),
                self.multiworld.get_location("Midoro Palace: Guarded Item", self.player),
                self.multiworld.get_location("Midoro Palace: Crumbling Blocks", self.player),
                self.multiworld.get_location("Midoro Palace: Helmethead Drop", self.player),
            ]

            island_palace_checks = [
                self.multiworld.get_location("Island Palace: Buried Item Left", self.player),
                self.multiworld.get_location("Island Palace: Buried Item Right", self.player),
                self.multiworld.get_location("Island Palace: Outside", self.player),
                self.multiworld.get_location("Island Palace: Block Mountain", self.player),
                self.multiworld.get_location("Island Palace: Precarious Item", self.player),
                self.multiworld.get_location("Island Palace: Pedestal Item", self.player),
                self.multiworld.get_location("Island Palace: Pillar Item", self.player),
                self.multiworld.get_location("Island Palace: Guarded by Iron Knuckles", self.player),
                self.multiworld.get_location("Island Palace: Rebonack Drop", self.player),
            ]

            maze_palace_checks = [
                self.multiworld.get_location("Maze Palace: Nook Item", self.player),
                self.multiworld.get_location("Maze Palace: Sealed Item", self.player),
                self.multiworld.get_location("Maze Palace: Block Mountain Left", self.player),
                self.multiworld.get_location("Maze Palace: Block Mountain Right", self.player),
                self.multiworld.get_location("Maze Palace: West Hall of Fire", self.player),
                self.multiworld.get_location("Maze Palace: East Hall of Fire", self.player),
                self.multiworld.get_location("Maze Palace: Basement Hall of Fire", self.player),
                self.multiworld.get_location("Maze Palace: Block Mountain Basement", self.player),
                self.multiworld.get_location("Maze Palace: Pillar Item", self.player),
                self.multiworld.get_location("Maze Palace: Pedestal Item", self.player),
                self.multiworld.get_location("Maze Palace: Carock Drop", self.player),
            ]

            sea_palace_checks = [
                self.multiworld.get_location("Palace on the Sea: Ledge Item", self.player),
                self.multiworld.get_location("Palace on the Sea: Crumbling Bridge", self.player),
                self.multiworld.get_location("Palace on the Sea: Falling Blocks", self.player),
                self.multiworld.get_location("Palace on the Sea: Above Elevator", self.player),
                self.multiworld.get_location("Palace on the Sea: Block Alcove", self.player),
                self.multiworld.get_location("Palace on the Sea: Knuckle Alcove", self.player),
                self.multiworld.get_location("Palace on the Sea: Pedestal Item", self.player),
                self.multiworld.get_location("Palace on the Sea: Skeleton Key", self.player),
                self.multiworld.get_location("Palace on the Sea: West Wing", self.player),
                self.multiworld.get_location("Palace on the Sea: Block Line", self.player),
                self.multiworld.get_location("Palace on the Sea: West Knuckle Alcove", self.player),
                self.multiworld.get_location("Palace on the Sea: Gooma Drop", self.player),
            ]

            rock_palace_checks = [
                self.multiworld.get_location("Three-Eye Rock Palace: 1F Block Mountain", self.player),
                self.multiworld.get_location("Three-Eye Rock Palace: 1F Enclosed Item", self.player),
                self.multiworld.get_location("Three-Eye Rock Palace: Middle Pit", self.player),
                self.multiworld.get_location("Three-Eye Rock Palace: Bottom Pit", self.player),
                self.multiworld.get_location("Three-Eye Rock Palace: Block Stairs", self.player),
                self.multiworld.get_location("Three-Eye Rock Palace: Pit of Sadness", self.player),
                self.multiworld.get_location("Three-Eye Rock Palace: Return of Helmethead", self.player),
                self.multiworld.get_location("Three-Eye Rock Palace: Pedestal Item", self.player),
                self.multiworld.get_location("Three-Eye Rock Palace: Helmethead III: The Revengening", self.player),
                self.multiworld.get_location("Three-Eye Rock Palace: Basement Block Mountain", self.player),
                self.multiworld.get_location("Three-Eye Rock Palace: Pit Hall", self.player),
                self.multiworld.get_location("Three-Eye Rock Palace: Barba Drop", self.player),
            ]

            parapa_keys = [
                self.create_item("Parapa Palace Key"),
                self.create_item("Parapa Palace Key")
            ]

            midoro_keys = [
                self.create_item("Midoro Palace Key"),
                self.create_item("Midoro Palace Key"),
                self.create_item("Midoro Palace Key"),
                self.create_item("Midoro Palace Key")
            ]

            island_keys = [
                self.create_item("Island Palace Key"),
                self.create_item("Island Palace Key"),
                self.create_item("Island Palace Key"),
                self.create_item("Island Palace Key")
            ]

            maze_keys = [
                self.create_item("Maze Palace Key"),
                self.create_item("Maze Palace Key"),
                self.create_item("Maze Palace Key"),
                self.create_item("Maze Palace Key"),
                self.create_item("Maze Palace Key"),
                self.create_item("Maze Palace Key")
            ]

            sea_keys = [
                self.create_item("Sea Palace Key"),
                self.create_item("Sea Palace Key"),
                self.create_item("Sea Palace Key"),
                self.create_item("Sea Palace Key"),
                self.create_item("Sea Palace Key")
            ]

            rock_keys = [
                self.create_item("Three-Eye Rock Palace Key"),
                self.create_item("Three-Eye Rock Palace Key")
            ]

            if self.options.remove_magical_key:
                rock_keys.extend([
                    self.create_item("Three-Eye Rock Palace Key"),
                    self.create_item("Three-Eye Rock Palace Key"),
                    self.create_item("Three-Eye Rock Palace Key"),
                    self.create_item("Three-Eye Rock Palace Key"),
                    self.create_item("Three-Eye Rock Palace Key"),
                ])

            self.random.shuffle(parapa_palace_checks)
            self.random.shuffle(midoro_palace_checks)
            self.random.shuffle(island_palace_checks)
            self.random.shuffle(maze_palace_checks)
            self.random.shuffle(sea_palace_checks)
            self.random.shuffle(rock_palace_checks)

            dungeon_checks = [
                (parapa_palace_checks, parapa_keys),
                (midoro_palace_checks, midoro_keys),
                (island_palace_checks, island_keys),
                (maze_palace_checks, maze_keys),
                (sea_palace_checks, sea_keys),
                (rock_palace_checks, rock_keys)
            ]
            
            for checks, keys in dungeon_checks:
                fill_restrictive(self.multiworld, state, checks, keys, True, True)

    def generate_output(self, output_directory: str):
        try:
            patch = Z2ProcPatch(player=self.player, player_name=self.player_name)
            patch.write_file("z2_base.bsdiff4", pkgutil.get_data(__name__, "z2_base.bsdiff4"))
            patch_rom(self, patch, self.player)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def fill_slot_data(self) -> Dict[str, List[int]]:
        return {
            #"early_boulder": self.early_boulder,
            "candle_required": self.options.candle_required.value
        }

    def modify_multidata(self, multidata: dict) -> None:
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    # def write_spoiler_header(self, spoiler_handle: TextIO) -> None:

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return Item(name, data.classification, data.code, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(self.filler_items)

    def set_classifications(self, name: str) -> Item:
        data = item_table[name]
        item = Item(name, data.classification, data.code, self.player)
        if item.name == "Candle" and not self.options.candle_required:
            item.classification = ItemClassification.useful

        if item.name == "Cross" and not self.options.cross_required:
            item.classification = ItemClassification.useful

        return item

    def generate_filler(self, pool: List[Item]) -> None:
        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool) - self.extra_count):
            item = self.set_classifications(self.get_filler_item_name())
            pool.append(item)

    def get_item_pool(self) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            for _ in range(data.amount):
                item = self.set_classifications(name)
                pool.append(item)
        return pool
        