import os
import typing
import threading

from typing import List, Set, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
import settings
from .Items import get_item_names_per_category, item_table, filler_items, trap_items
from .Locations import get_locations
from .Regions import init_areas
from .Options import YoshisIslandOptions
from .setup_game import setup_gamevars
from .Client import YISNIClient
from .Rules import set_easy_rules, set_normal_rules, set_hard_rules
from .Rom import LocalRom, patch_rom, get_base_rom_path, YIDeltaPatch, USHASH

class YISettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Yoshi's Island 1.0 US rom"""
        description = "Yoshi's Island ROM File"
        copy_to = "Super Mario World 2 - Yoshi's Island (U).sfc"
        md5s = [USHASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)

class YIWeb(WebWorld):
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Yoshi's Island randomizer"
        "and connecting to an Archipelago server.",
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
    game = "Yoshi's Island"
    option_definitions = YoshisIslandOptions
    data_version = 1
    required_client_version = (0, 4, 4)

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = {location.name: location.code for
                           location in get_locations(None)}
    item_name_groups = get_item_names_per_category()

    web = YIWeb()
    settings: typing.ClassVar[YISettings]
    #topology_present = True

    options_dataclass = YoshisIslandOptions
    options: YoshisIslandOptions

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
    def stage_assert_generate(cls, multiworld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def fill_slot_data(self):
        return {
            "world_1": self.world_1_stages,
            "world_2": self.world_2_stages,
            "world_3": self.world_3_stages,
            "world_4": self.world_4_stages,
            "world_5": self.world_5_stages,
            "world_6": self.world_6_stages
        }

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
        spoiler_handle.write(f"\nLevels:\n1-1: {self.level_name_list[0]}\n")
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
        spoiler_handle.write("6-8: King Bowser's Castle")

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

        return item

    def create_regions(self):
        init_areas(self, get_locations(self))

    def get_filler_item_name(self) -> str:
        trap_chance: int = self.options.trap_percent.value

        if self.random.random() < (trap_chance / 100) and self.options.traps_enabled.value == 1:
            return self.random.choice(trap_items)
        else:
            return self.random.choice(filler_items)

    def set_rules(self):
        if self.options.stage_logic == 0:
            set_easy_rules(self)
        elif self.options.stage_logic == 1:
            set_normal_rules(self)
        else:
            set_hard_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has('Saved Baby Luigi', self.player)
        self.multiworld.get_location("Burt The Bashful's Boss Room", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Salvo The Slime's Boss Room", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Bigger Boo's Boss Room", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Roger The Ghost's Boss Room", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Prince Froggy's Boss Room", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Naval Piranha's Boss Room", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Marching Milde's Boss Room", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Hookbill The Koopa's Boss Room", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Sluggy The Unshaven's Boss Room", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Raphael The Raven's Boss Room", self.player).place_locked_item(self.create_item("Boss Clear"))
        self.multiworld.get_location("Tap-Tap The Red Nose's Boss Room", self.player).place_locked_item(self.create_item("Boss Clear"))

        if self.options.goal.value == 1:
            self.multiworld.get_location("Reconstituted Luigi", self.player).place_locked_item(self.create_item("Saved Baby Luigi"))
        else:
            self.multiworld.get_location("King Bowser's Castle: Level Clear", self.player).place_locked_item(self.create_item("Saved Baby Luigi"))

        self.multiworld.get_location("Touch Fuzzy Get Dizzy: Gather Coins", self.player).place_locked_item(self.create_item("Bandit Consumables"))
        self.multiworld.get_location("The Cave Of the Mystery Maze: Seed Spitting Contest", self.player).place_locked_item(self.create_item("Bandit Watermelons"))
        self.multiworld.get_location("Lakitu's Wall: Gather Coins", self.player).place_locked_item(self.create_item("Bandit Consumables"))
        self.multiworld.get_location("Ride Like The Wind: Gather Coins", self.player).place_locked_item(self.create_item("Bandit Consumables"))

    def place_locked_item(self, excluded_items: Set[str], location: str, item: str) -> None:
        excluded_items.add(item)

        item = self.create_item(item)

        self.multiworld.get_location(location, self.player).place_locked_item(item)

    def generate_early(self):
        setup_gamevars(self)


    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()

        starting_gate = ["World 1 Gate", "World 2 Gate", "World 3 Gate",
                         "World 4 Gate", "World 5 Gate", "World 6 Gate"]


        excluded_items.add(starting_gate[self.options.starting_world])

        if self.options.shuffle_midrings.value == 0:
            excluded_items.add('Middle Ring')

        if self.options.add_secretlens.value == 0:
            excluded_items.add('Secret Lens')

        if self.options.extras_enabled.value == 0:
            excluded_items.add('Extra Panels')
            excluded_items.add('Extra 1')
            excluded_items.add('Extra 2')
            excluded_items.add('Extra 3')
            excluded_items.add('Extra 4')
            excluded_items.add('Extra 5')
            excluded_items.add('Extra 6')

        if self.options.split_extras.value == 1:
            excluded_items.add('Extra Panels')
        else:
            excluded_items.add('Extra 1')
            excluded_items.add('Extra 2')
            excluded_items.add('Extra 3')
            excluded_items.add('Extra 4')
            excluded_items.add('Extra 5')
            excluded_items.add('Extra 6')

        if self.options.split_bonus.value == 1:
            excluded_items.add('Bonus Panels')
        else:
            excluded_items.add('Bonus 1')
            excluded_items.add('Bonus 2')
            excluded_items.add('Bonus 3')
            excluded_items.add('Bonus 4')
            excluded_items.add('Bonus 5')
            excluded_items.add('Bonus 6')

        return excluded_items

    def create_item_with_correct_settings(self, player: int, name: str) -> Item:
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

        if name == 'Car Morph' and self.options.stage_logic.value != 0:
            item.classification = ItemClassification.useful

        if name == 'Secret Lens' and (self.options.hidden_object_visibility.value >= 2 or self.options.stage_logic.value != 0):
            item.classification = ItemClassification.useful

        if name in ["Bonus 1", "Bonus 2", "Bonus 3", "Bonus 4", "Bonus 5", "Bonus 6", "Bonus Panels"] and self.options.minigame_checks.value <= 1:
            item.classification = ItemClassification.useful

        if name in ["Bonus 1", "Bonus 3", "Bonus 4", 'Bonus Panels'] and self.options.item_logic.value == 1:
            item.classification = ItemClassification.progression

        if name == 'Piece of Luigi' and self.options.goal.value != 0:
            if self.luigi_count >= self.options.luigi_pieces_required.value:
                item.classification = ItemClassification.useful
            else:
                item.classification = ItemClassification.progression_skip_balancing
                self.luigi_count += 1

        return item

    def generate_filler(self, multiworld: MultiWorld, player: int,
                                        pool: List[Item]):
        if self.playergoal == 1:
            for _ in range(self.options.luigi_pieces_in_pool.value):
                item = self.create_item_with_correct_settings(player, "Piece of Luigi")
                pool.append(item)

        for _ in range(len(multiworld.get_unfilled_locations(player)) - len(pool) - 16):
            item = self.create_item_with_correct_settings(player, self.get_filler_item_name())
            pool.append(item)

    def get_item_pool(self, player: int, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                for _ in range(data.amount):
                    item = self.create_item_with_correct_settings(player, name)
                    pool.append(item)

        return pool



    def create_items(self):
        self.luigi_count = 0

        if self.options.minigame_checks.value >= 2:
            self.multiworld.get_location("Flip Cards", self.player).place_locked_item(self.create_item("Bonus Consumables"))
            self.multiworld.get_location("Drawing Lots", self.player).place_locked_item(self.create_item("Bonus Consumables"))
            self.multiworld.get_location("Match Cards", self.player).place_locked_item(self.create_item("Bonus Consumables"))


        excluded_items = self.get_excluded_items()

        pool = self.get_item_pool(self.player, excluded_items)

        self.generate_filler(self.multiworld, self.player, pool)

        self.multiworld.itempool += pool

    def generate_output(self, output_directory: str):

        rompath = ""  # if variable is not declared finally clause may fail
        try:
            world = self.multiworld
            player = self.player
            rom = LocalRom(get_base_rom_path())
            patch_rom(self, rom, self.player, self.multiworld)

            rompath = os.path.join(output_directory,
                                   f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = YIDeltaPatch(os.path.splitext(rompath)[0]+YIDeltaPatch.patch_file_ending,
                                  player=player, player_name=world.player_name[player],
                                  patched_path=rompath)
            patch.write()
        finally:
            self.rom_name_available_event.set()
            if os.path.exists(rompath):
                os.unlink(rompath)

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        stage_pos_data = {}
        for loc in self.multiworld.get_locations(self.player):
            if loc.LevelID is not None and loc.address is not None:
                if loc.LevelID in self.world_1_stages:
                    stage_pos_data[loc.address] = "World 1"
                elif loc.LevelID in self.world_2_stages:
                    stage_pos_data[loc.address] = "World 2"
                if loc.LevelID in self.world_3_stages:
                    stage_pos_data[loc.address] = "World 3"
                if loc.LevelID in self.world_4_stages:
                    stage_pos_data[loc.address] = "World 4"
                if loc.LevelID in self.world_5_stages:
                    stage_pos_data[loc.address] = "World 5"
                if loc.LevelID in self.world_6_stages:
                    stage_pos_data[loc.address] = "World 6"
        hint_data[self.player] = stage_pos_data
