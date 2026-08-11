import typing
import threading
from typing import List, Set, Dict

from BaseClasses import Item, MultiWorld, Location, Tutorial
from Fill import fill_restrictive
from worlds.AutoWorld import World, WebWorld
import settings
from .Items import get_item_names_per_category, item_table
from .Locations import get_locations
from .Regions import init_areas, connect_area_exits
from .Options import EBOptions, eb_option_groups
from .setup_game import setup_gamevars, place_static_items
from .modules.enemy_data import initialize_enemies
from .modules.flavor_data import create_flavors
from .game_data.local_data import item_id_table, world_version
from .modules.hint_data import setup_hints
from .game_data.text_data import spoiler_psi, spoiler_starts, spoiler_badges
from .Client import EarthBoundClient
from .Rules import set_location_rules
from .Rom import patch_rom, EBProcPatch, valid_hashes
from .game_data.static_location_data import location_ids, location_groups
from .modules.equipamizer import EBArmor, EBWeapon
from .modules.boss_shuffle import BossData, SlotInfo
from worlds.generic.Rules import add_item_rule
from .generator_main import (EBItem, generate_early, create_regions, fill_slot_data,
                             modify_multidata, generate_output, create_items, get_filler_item_name, set_rules,
                             write_spoiler_header, extend_hint_information, create_item)


class EBSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the EarthBound US ROM"""
        description = "EarthBound ROM File"
        copy_to = "EarthBound.sfc"
        md5s = valid_hashes

    rom_file: RomFile = RomFile(RomFile.copy_to)


class EBWeb(WebWorld):
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the EarthBound randomizer"
        "and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    tutorials = [setup_en]

    option_groups = eb_option_groups
    # option_presets = eb_option_presets


class EarthBoundWorld(World):
    """EarthBound is a contemporary-themed JRPG. Take four psychically-endowed children
       across the world in search of 8 Melodies to defeat Giygas, the cosmic evil."""
    
    game = "EarthBound"
    option_definitions = EBOptions
    data_version = 1
    required_client_version = (0, 5, 0) 

    item_name_to_id = {item: data.code for item, data in item_table.items() if data.code}
    disable_ut = True
    location_name_to_id = location_ids
    item_name_groups = get_item_names_per_category()
    location_name_groups = location_groups

    web = EBWeb()
    settings: typing.ClassVar[EBSettings]
    # topology_present = True

    options_dataclass = EBOptions
    options: EBOptions

    locked_locations: List[str]
    location_cache: List[Location]

    generate_early = generate_early
    create_items = create_items
    create_item = create_item
    create_regions = create_regions
    fill_slot_data = fill_slot_data
    modify_multidata = modify_multidata
    generate_output = generate_output
    get_filler_item_name = get_filler_item_name
    set_rules = set_rules
    write_spoiler_header = write_spoiler_header
    extend_hint_information = extend_hint_information

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

        self.locked_locations = []
        self.location_cache = []
        self.event_count = 8
        self.progressive_filler_bats: int = 0
        self.progressive_filler_pans: int = 0
        self.progressive_filler_guns: int = 0
        self.progressive_filler_bracelets: int = 0
        self.progressive_filler_other: int = 0
        self.world_version: str = world_version
        self.armor_list = Dict[str, EBArmor]
        self.weapon_list = Dict[str, EBWeapon]
        self.boss_slots = Dict[str, SlotInfo]
        self.boss_info = Dict[str, BossData]
        self.starting_character: str | None = None
        self.locals = []
        self.rom_name = None
        self.starting_area_teleport = None
        self.common_gear = []
        self.uncommon_gear = []
        self.rare_gear = []
        self.get_all_spheres = threading.Event()
        self.boss_list: List[str] = []
        self.starting_region = str
        self.start_location = int
        self.dungeon_connections: dict[str, str] = {}
        self.has_generated_output: bool = False
        self.hint_man_hints: list[tuple[int | str, player]] = []

        self.common_items = [
            "Cookie",
            "Bag of Fries",
            "Teddy Bear",
            "Hamburger",
            "Boiled Egg",
            "Fresh Egg",
            "Picnic Lunch",
            "Croissant",
            "Bread Roll",
            "Can of Fruit Juice",
            "Royal Iced Tea",
            "Protein Drink",
            "Bottle of Water",
            "Cold Remedy",
            "Vial of Serum",
            "Ketchup Packet",
            "Sugar Packet",
            "Tin of Cocoa",
            "Carton of Cream",
            "Sprig of Parsley",
            "Jar of Hot Sauce",
            "Salt Packet",
            "Wet Towel",
            "Refreshing Herb",
            "Ruler",
            "Protractor",
            "Insecticide Spray",
            "Rust Promoter",
            "Stag Beetle",
            "Toothbrush",
            "Handbag Strap",
            "Chick",
            "Chicken",
            "Trout Yogurt",
            "Banana",
            "Calorie Stick",
            "Gelato de Resort",
            "Snake",
            "Cup of Noodles",
            "Cup of Coffee",
            "Double Burger",
            "Bean Croquette",
            "Molokheiya Soup",
            "Plain Roll",
            "Magic Tart",
            "PSI Caramel",
            "Popsicle",
            "Bottle Rocket"
        ]

        self.common_gear = [
            "Yo-yo",
            "Slingshot",
            "Travel Charm",
            "Great Charm",
            "Ribbon",
            "Red Ribbon"
        ]

        self.uncommon_items = [
            "Pasta di Summers",
            "Pizza",
            "Chef's Special",
            "Super Plush Bear",
            "Jar of Delisauce",
            "Secret Herb",
            "Xterminator Spray",
            "Snake Bag",
            "Bomb",
            "Rust Promoter DX",
            "Pair of Dirty Socks",
            "Mummy Wrap",
            "Pharaoh's Curse",
            "Sudden Guts Pill",
            "Picture Postcard",
            "Viper",
            "Repel Sandwich",
            "Lucky Sandwich",
            "Peanut Cheese Bar",
            "Bowl of Rice Gruel",
            "Kabob",
            "Plain Yogurt",
            "Beef Jerky",
            "Mammoth Burger",
            "Bottle of DXwater",
            "Magic Pudding",
            "Big Bottle Rocket",
            "Bazooka",
            "Meteornium"

        ]

        self.uncommon_gear = [
            "Trick Yo-yo",
            "Bionic Slingshot",
            "Crystal Charm",
            "Defense Ribbon",
            "Earth Pendant",
            "Flame Pendant",
            "Rain Pendant",
            "Night Pendant"
        ]

        self.rare_items = [
            "Large Pizza",
            "Magic Truffle",
            "Brain Food Lunch",
            "Rock Candy",
            "Kraken Soup",
            "IQ Capsule",
            "Guts Capsule",
            "Speed Capsule",
            "Vital Capsule",
            "Luck Capsule",
            "Horn of Life",
            "Multi Bottle Rocket",
            "Super Bomb",
            "Bag of Dragonite",
            "Meteotite",
            "Repel Superwich",
            "Piggy Jelly",
            "Spicy Jerky",
            "Luxury Jerky",
            "Cup of Lifenoodles"
        ]

        self.rare_gear = [
            "Combat Yo-yo",
            "Sword of Kings",
            "Sea Pendant",
            "Star Pendant",
            "Goddess Ribbon"
        ]

        self.money = [
            "$10",
            "$100",
            "$1000"
        ]

    def pre_fill(self) -> None:
        prefill_locations = []
        prefill_items = []

        if not self.options.character_shuffle:
            main_characters = ["Ness", "Paula", "Jeff", "Poo"]
            for character in main_characters:
                if character != self.starting_character:
                    prefill_items.append(self.create_item(character))

            prefill_items.extend([
                self.create_item("Flying Man"),
                self.create_item("Teddy Bear"),
                self.create_item("Super Plush Bear")
            ])

            prefill_locations.extend([
                self.multiworld.get_location("Happy-Happy Village - Prisoner", self.player),
                self.multiworld.get_location("Threed - Zombie Prisoner", self.player),
                self.multiworld.get_location("Snow Wood - Bedroom", self.player),
                self.multiworld.get_location("Monotoli Building - Monotoli Character", self.player),
                self.multiworld.get_location("Dalaam - Throne Character", self.player),
                self.multiworld.get_location("Deep Darkness - Barf Character", self.player),
            ])
            self.random.shuffle(prefill_locations)
            add_item_rule(self.multiworld.get_location("Happy-Happy Village - Prisoner", self.player), lambda item: item.name in self.item_name_groups["Characters"])
            add_item_rule(self.multiworld.get_location("Threed - Zombie Prisoner", self.player), lambda item: item.name in self.item_name_groups["Characters"])
            add_item_rule(self.multiworld.get_location("Snow Wood - Bedroom", self.player), lambda item: item.name in self.item_name_groups["Characters"])
            add_item_rule(self.multiworld.get_location("Monotoli Building - Monotoli Character", self.player), lambda item: item.name in self.item_name_groups["Characters"])
            add_item_rule(self.multiworld.get_location("Dalaam - Throne Character", self.player), lambda item: item.name in self.item_name_groups["Characters"])
            add_item_rule(self.multiworld.get_location("Deep Darkness - Barf Character", self.player), lambda item: item.name in self.item_name_groups["Characters"])

        fill_restrictive(self.multiworld, self.multiworld.get_all_state(False, collect_pre_fill_items=False), prefill_locations, prefill_items, True, True)
        setup_hints(self)

    def get_pre_fill_items(self) -> list[Item]:
        characters = ["Ness", "Paula", "Jeff", "Poo"]
        prefill_items = []
        for character in characters:
            if character != self.starting_character:
                prefill_items.append(self.create_item(f"{character}"))     
        return prefill_items

    @classmethod
    def stage_generate_output(cls, multiworld: MultiWorld, output_directory: str) -> None:
        try:
            multiworld.earthbound_locations_by_sphere = list(multiworld.get_spheres())
        except Exception:
            raise
        finally:
            for world in multiworld.get_game_worlds("EarthBound"):
                world.get_all_spheres.set()

    def create_item(self, name: str) -> EBItem:
        data = item_table[name]
        return EBItem(name, data.classification, data.code, self.player)

    def get_filler_item_name(self) -> str:  # Todo: make this suck less
        weights = {"rare": self.options.rare_filler_weight.value, "uncommon": self.options.uncommon_filler_weight.value, "common": self.options.common_filler_weight.value,
                   "rare_gear": int(self.options.rare_filler_weight.value * 0.5), "uncommon_gear": int(self.options.uncommon_filler_weight.value * 0.5),
                   "common_gear": int(self.options.common_filler_weight.value * 0.5), "money": self.options.money_weight.value}
        
        filler_type = self.random.choices(list(weights), weights=list(weights.values()), k=1)[0]
        weight_table = {
            "common": self.common_items,
            "common_gear": self.common_gear,
            "uncommon": self.uncommon_items,
            "uncommon_gear": self.uncommon_gear,
            "rare": self.rare_items,
            "rare_gear": self.rare_gear,
            "money": self.money
        }
        return self.random.choice(weight_table[filler_type])

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        excluded_items.add(self.starting_character)
        starting_area_to_teleport = ["Onett Teleport", "Onett Teleport", "Twoson Teleport", "Happy-Happy Village Teleport",
                                     "Threed Teleport", "Saturn Valley Teleport", "Fourside Teleport", "Winters Teleport",
                                     "Summers Teleport", "Dalaam Teleport", "Scaraba Teleport", "Deep Darkness Teleport",
                                     "Tenda Village Teleport", "Lost Underworld Teleport", "Magicant Teleport"]
        self.starting_area_teleport = starting_area_to_teleport[self.start_location]
        excluded_items.add(self.starting_area_teleport)
        if self.options.random_start_location:
            excluded_items.add(self.starting_teleport)

        if self.options.magicant_mode not in [0, 3]:
            excluded_items.add("Magicant Teleport")

        if not self.options.character_shuffle:
            excluded_items.add("Ness")
            excluded_items.add("Paula")
            excluded_items.add("Jeff")
            excluded_items.add("Poo")
            excluded_items.add("Flying Man")

        if self.options.progressive_weapons:
            excluded_items.add("Magicant Bat")
            excluded_items.add("Legendary Bat")
            excluded_items.add("Pop Gun")
            excluded_items.add("Stun Gun")
            excluded_items.add("Death Ray")
            excluded_items.add("Moon Beam Gun")

        if self.options.progressive_armor:
            excluded_items.add("Platinum Band")
            excluded_items.add("Diamond Band")
            excluded_items.add("Pixie's Bracelet")
            excluded_items.add("Cherub's Band")
            excluded_items.add("Goddess Band")
            excluded_items.add("Coin of Slumber")
            excluded_items.add("Souvenir Coin")
            excluded_items.add("Mr. Saturn Coin")

        if not self.options.no_free_sanctuaries:
            excluded_items.add("Tiny Key")
            excluded_items.add("Tenda Lavapants")

        return excluded_items

    def fill_item_pool(self, pool: List[Item]) -> None:
        item_to_counts = {
            "Progressive Bat": self.progressive_filler_bats,
            "Progressive Fry Pan": self.progressive_filler_pans,
            "Progressive Gun": self.progressive_filler_guns,
            "Progressive Bracelet": self.progressive_filler_bracelets,
            "Progressive Other": self.progressive_filler_other
        }

        max_filler_counts = {
            "Progressive Bat": 8,
            "Progressive Fry Pan": 9,
            "Progressive Gun": 6,
            "Progressive Bracelet": 6,
            "Progressive Other": 10
        }

        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool) - self.event_count):  # Change to fix event count
            item = self.set_classifications(self.get_filler_item_name())
            if item.name in ["Progressive Bat", "Progressive Fry Pan", "Progressive Other",
                             "Progressive Gun", "Progressive Bracelet"]:
                item_to_counts[item.name] += 1

                if item_to_counts[item.name] >= max_filler_counts[item.name]:
                    self.common_gear = [x for x in self.common_gear if x != item.name]
                    self.uncommon_gear = [x for x in self.uncommon_gear if x != item.name]
                    self.rare_gear = [x for x in self.rare_gear if x != item.name]
            pool.append(item)

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                for _ in range(data.amount):
                    item = self.set_classifications(name)
                    pool.append(item)
        
        if self.options.progressive_weapons:
            for i in range(2):
                pool.append(self.set_classifications("Progressive Bat"))
            for i in range(4):
                pool.append(self.set_classifications("Progressive Gun"))

        if self.options.progressive_armor:
            for i in range(5):
                pool.append(self.set_classifications("Progressive Bracelet"))
            for i in range(3):
                pool.append(self.set_classifications("Progressive Other"))

        return pool
