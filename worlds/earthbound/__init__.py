import typing
import threading
from typing import List, Dict

from BaseClasses import MultiWorld, Location, Tutorial
from worlds.AutoWorld import World, WebWorld
import settings
from .Items import get_item_names_per_category, item_table
from .Options import EBOptions, eb_option_groups
from .game_data.local_data import item_id_table, world_version
from .Client import EarthBoundClient
from .Rom import valid_hashes
from .game_data.static_location_data import location_ids, location_groups
from .modules.equipamizer import EBArmor, EBWeapon
from .modules.boss_shuffle import BossData, SlotInfo
from .generator_main import (EBItem, generate_early, create_regions, fill_slot_data,
                             modify_multidata, generate_output, create_items, get_filler_item_name, set_rules,
                             write_spoiler_header, extend_hint_information, create_item, pre_fill)


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
    pre_fill = pre_fill

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
        self.local_world_version: str = world_version
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
        self.item_pool = []

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

    @classmethod
    def stage_generate_output(cls, multiworld: MultiWorld, output_directory: str) -> None:
        try:
            multiworld.earthbound_locations_by_sphere = list(multiworld.get_spheres())
        except Exception:
            raise
        finally:
            for world in multiworld.get_game_worlds("EarthBound"):
                world.get_all_spheres.set()
