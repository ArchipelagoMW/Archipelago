import os
import typing
import threading

from typing import List, Set, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
import settings
from .Items import get_item_names_per_category, item_table, filler_items
from .Locations import get_locations
from .Regions import init_areas
from .Options import SAI2Options
from .setup_game import setup_gamevars
from .Client import SAI2SNIClient
from .Rules import set_location_rules
from .Rom import LocalRom, patch_rom, get_base_rom_path, SAI2ProcedurePatch, USHASH

class SAI2Settings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Super Adventure Island II US ROM"""
        description = "Super Adventure Island II ROM File"
        copy_to = "Super Adventure Island II (USA).sfc"
        md5s = [USHASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)

class SAI2Web(WebWorld):
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Super Adventure Island II randomizer"
        "and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    tutorials = [setup_en]

class SAI2World(World):
    """Yoshi's Island is a 2D platforming game.
        During a delivery, Bowser's evil ward, Kamek, attacked the stork, kidnapping Luigi and dropping Mario onto Yoshi's Island.
        As Yoshi, you must run, jump, and throw eggs to escort the baby Mario across the island to defeat Bowser and reunite the two brothers with their parents."""
    game = "Super Adventure Island II"
    option_definitions = SAI2Options
    data_version = 1
    required_client_version = (0, 3, 5)

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = {location.name: location.code for
                           location in get_locations(None)}
    item_name_groups = get_item_names_per_category()

    web = SAI2Web()
    settings: typing.ClassVar[SAI2Settings]
    #topology_present = True

    options_dataclass = SAI2Options
    options: SAI2Options

    locked_locations: List[str]
    location_cache: List[Location]
    placed_life_bottles = 0
    first_weapon_placed = False
    first_projectile_placed = False

    item_classifications = {"filler": ItemClassification.filler,
                            "useful": ItemClassification.useful,
                            "progression": ItemClassification.progression}

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

        self.locked_locations= []
        self.location_cache= []
        self.locked_items = 17


    #def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        #spoiler_handle.write(f"Burt The Bashful's Boss Door:      {self.starting_item}\n")

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        classification = self.item_classifications[data.classification]
        item = Item(name, classification, data.code, self.player)

        return item

    def create_regions(self):
        init_areas(self, get_locations(self))

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)

    def set_rules(self):
        set_location_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has('Tina', self.player)
        self.multiworld.get_location("Poka-Poka First Cave", self.player).place_locked_item(self.create_item("Light Switch"))
        self.multiworld.get_location("Hiya-Hiya Top Level", self.player).place_locked_item(self.create_item("Star Switch"))
        self.multiworld.get_location("Boa-Boa Hidden Wall", self.player).place_locked_item(self.create_item("Sun Switch"))
        self.multiworld.get_location("Puka-Puka Switch Room", self.player).place_locked_item(self.create_item("Aqua Switch"))
        self.multiworld.get_location("Sala-Sala Switch Room", self.player).place_locked_item(self.create_item("Moon Switch"))
        self.multiworld.get_location("Puka-Puka Water Control", self.player).place_locked_item(self.create_item("Puka-Puka Drained"))
        self.multiworld.get_location("Phantom Defeat", self.player).place_locked_item(self.create_item("Tina"))

        self.multiworld.get_location("Boa-Hiya Shortcut Room", self.player).place_locked_item(self.create_item("Boa-Hiya Shortcut Open"))
        self.multiworld.get_location("Sala-Hiya Shortcut Room", self.player).place_locked_item(self.create_item("Sala-Hiya Shortcut Open"))
        self.multiworld.get_location("Sala-Puka Shortcut Room", self.player).place_locked_item(self.create_item("Sala-Puka Shortcut Open"))
        self.multiworld.get_location("Fuwa-Puka Shortcut Room", self.player).place_locked_item(self.create_item("Fuwa-Puka Shortcut Open"))
        self.multiworld.get_location("Fuwa-Poka Shortcut Room", self.player).place_locked_item(self.create_item("Fuwa-Poka Shortcut Open"))

        self.multiworld.get_location("Light Gate", self.player).place_locked_item(self.create_item("Light Gate Lowered"))
        self.multiworld.get_location("Sun Gate", self.player).place_locked_item(self.create_item("Sun Gate Lowered"))
        self.multiworld.get_location("Star Gate", self.player).place_locked_item(self.create_item("Star Gate Lowered"))
        self.multiworld.get_location("Aqua Gate", self.player).place_locked_item(self.create_item("Aqua Gate Lowered"))
        self.multiworld.get_location("Moon Gate", self.player).place_locked_item(self.create_item("Moon Gate Lowered"))

        if self.options.shuffle_skills != 2:
            self.multiworld.get_location("100 Coin Shop", self.player).place_locked_item(self.create_item(self.locked_skills[0]))
            self.multiworld.get_location("300 Coin Shop", self.player).place_locked_item(self.create_item(self.locked_skills[1]))
            self.multiworld.get_location("500 Coin Shop", self.player).place_locked_item(self.create_item(self.locked_skills[2]))

        if self.options.casino_checks == 0:
            self.multiworld.get_location("Casino 500 Coin Purchase", self.player).place_locked_item(self.create_item("Life Bottle"))
            self.multiworld.get_location("Casino 1000 Coin Purchase", self.player).place_locked_item(self.create_item("Boomerang"))
            self.multiworld.get_location("Casino 2000 Coin Purchase", self.player).place_locked_item(self.create_item("Light Shield"))
            self.multiworld.get_location("Casino 3000 Coin Purchase", self.player).place_locked_item(self.create_item("Light Armor"))
            self.multiworld.get_location("Casino 5000 Coin Purchase", self.player).place_locked_item(self.create_item("Light Sword"))
        else:
            self.multiworld.itempool.append(self.create_item('Life Bottle'))
            self.multiworld.itempool.append(self.create_item('Boomerang'))
            self.multiworld.itempool.append(self.create_item('Light Shield'))
            self.multiworld.itempool.append(self.create_item('Light Sword'))
            self.multiworld.itempool.append(self.create_item('Light Armor'))


    def generate_early(self):
        self.locals = []
        setup_gamevars(self)
        if self.options.world_state != 1:
            self.multiworld.push_precollected(self.create_item(self.starting_item))
        if self.options.extra_health == 1:
            for _ in range(2):
                self.multiworld.push_precollected(self.create_item("Life Bottle"))

        if self.light_gate == 1:
            self.multiworld.push_precollected(self.create_item("Light Gate Lowered"))

        if self.sun_gate == 1:
            self.multiworld.push_precollected(self.create_item("Sun Gate Lowered"))

        if self.star_gate == 1:
            self.multiworld.push_precollected(self.create_item("Star Gate Lowered"))

        if self.aqua_gate == 1:
            self.multiworld.push_precollected(self.create_item("Aqua Gate Lowered"))

        if self.moon_gate == 1:
            self.multiworld.push_precollected(self.create_item("Moon Gate Lowered"))



    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        if self.options.boss_spells == 1:
            excluded_items.add('Light Spell')
            excluded_items.add('Star Spell')
            excluded_items.add('Sun Spell')
            excluded_items.add('Aqua Spell')
            excluded_items.add('Moon Spell')
        
        if self.options.shuffle_skills != 2:
            excluded_items.add("Shove")
            excluded_items.add("Down Jab")
            excluded_items.add("Up Jab")

        return excluded_items

    def get_dynamic_classes(self, player: int, name: str) -> Item:
        data = item_table[name]
        classification = self.item_classifications[data.classification]
        item = Item(name, classification, data.code, player)
        weapons = ["Ice Sword", "Thunder Sword", "Crystal Sword", "Light Sword", "Dagger", "Fireballs", "Silver Sword", "Fire Sword", "Power Sword"]
        projectiles = ["Ax", "Boomerang"]

        if not self.options.casino_checks:
            weapons.remove("Light Sword")

        if not item.advancement:
            return item

        if name in weapons:
            if self.first_weapon_placed == True:
                if name not in ["Silver Sword", "Power Sword", "Fire Sword"]:
                    item.classification = ItemClassification.useful
            else:
                self.first_weapon_placed = True

        if name in projectiles:
            if self.first_projectile_placed == True:
                item.classification = ItemClassification.useful
            else:
                self.first_projectile_placed = True

        if name == "Life Bottle":
            item.classification = ItemClassification.useful

        if name == ("Light Sword" or "Boomerang") and self.options.casino_checks != 1:
            item.classification = ItemClassification.useful
        
        if name == "Light Stone" and self.light_gate == 1:
            item.classification = ItemClassification.filler

        if name == "Sun Stone" and self.sun_gate == 1:
            item.classification = ItemClassification.filler

        if name == "Star Stone" and self.star_gate == 1:
            item.classification = ItemClassification.filler

        if name == "Aqua Stone" and self.aqua_gate == 1:
            item.classification = ItemClassification.filler
        
        if name == "Moon Stone" and self.moon_gate == 1:
            item.classification = ItemClassification.filler

        return item

    def generate_filler(self, multiworld: MultiWorld, player: int,
                                        pool: List[Item]):
                                        
        for _ in range(len(multiworld.get_unfilled_locations(player)) - len(pool) - self.locked_items): #- number of event items
            item = self.get_dynamic_classes(player, self.get_filler_item_name())
            pool.append(item)

    def get_item_pool(self, player: int, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                for _ in range(data.amount):
                    item = self.get_dynamic_classes(player, name)
                    pool.append(item)

        return pool



    def create_items(self):
        if self.options.casino_checks == 0:
            self.locked_items += 5
        
        if self.options.shuffle_skills !=2:
            self.locked_items += 3

        if self.options.boss_spells == 1:
            self.locked_items += 5
        excluded_items = self.get_excluded_items()

        pool = self.get_item_pool(self.player, excluded_items)

        self.generate_filler(self.multiworld, self.player, pool)

        self.multiworld.itempool += pool

    def generate_output(self, output_directory: str):
        try:
            world = self.multiworld
            player = self.player
            patch = SAI2ProcedurePatch()
            patch_rom(self, patch, self.player, self.multiworld)

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
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    #def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):