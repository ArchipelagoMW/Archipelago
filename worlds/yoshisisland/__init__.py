import base64
import os
import typing
import threading

from typing import List, Set, TextIO, Dict
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
import settings
from .Items import get_item_names_per_category, item_table, filler_items, trap_items
from .Locations import get_locations
from .Regions import init_areas
from .Options import YoshisIslandOptions, PlayerGoal, ObjectVis, StageLogic, MinigameChecks
from .setup_game import setup_gamevars
from .Client import YoshisIslandSNIClient
from .Rules import set_easy_rules, set_normal_rules, set_hard_rules
from .Rom import LocalRom, patch_rom, get_base_rom_path, YoshisIslandDeltaPatch, USHASH


class YoshisIslandSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Yoshi's Island 1.0 US rom"""
        description = "Yoshi's Island ROM File"
        copy_to = "Super Mario World 2 - Yoshi's Island (U).sfc"
        md5s = [USHASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class YoshisIslandWeb(WebWorld):
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


class YoshisIslandWorld(World):
    """
    Yoshi's Island is a 2D platforming game.
    During a delivery, Bowser's evil ward, Kamek, attacked the stork, kidnapping Luigi and dropping Mario onto Yoshi's Island.
    As Yoshi, you must run, jump, and throw eggs to escort the baby Mario across the island to defeat Bowser and reunite the two brothers with their parents.
    """
    game = "Yoshi's Island"
    option_definitions = YoshisIslandOptions
    required_client_version = (0, 4, 4)

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = {location.name: location.code for location in get_locations(None)}
    item_name_groups = get_item_names_per_category()

    web = YoshisIslandWeb()
    settings: typing.ClassVar[YoshisIslandSettings]
    # topology_present = True

    options_dataclass = YoshisIslandOptions
    options: YoshisIslandOptions

    locked_locations: List[str]
    set_req_bosses: str
    lives_high: int
    lives_low: int
    castle_bosses: int
    bowser_bosses: int
    baby_mario_sfx: int
    leader_color: int
    boss_order: list
    boss_burt: int
    luigi_count: int

    rom_name: bytearray

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)
        self.locked_locations = []

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def fill_slot_data(self) -> Dict[str, List[int]]:
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
        return Item(name, data.classification, data.code, self.player)

    def create_regions(self) -> None:
        init_areas(self, get_locations(self))

    def get_filler_item_name(self) -> str:
        trap_chance: int = self.options.trap_percent.value

        if self.random.random() < (trap_chance / 100) and self.options.traps_enabled:
            return self.random.choice(trap_items)
        else:
            return self.random.choice(filler_items)

    def set_rules(self) -> None:
        rules_per_difficulty = {
            0: set_easy_rules,
            1: set_normal_rules,
            2: set_hard_rules
        }

        rules_per_difficulty[self.options.stage_logic.value](self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Saved Baby Luigi", self.player)
        self.get_location("Burt The Bashful's Boss Room").place_locked_item(self.create_item("Boss Clear"))
        self.get_location("Salvo The Slime's Boss Room").place_locked_item(self.create_item("Boss Clear"))
        self.get_location("Bigger Boo's Boss Room", ).place_locked_item(self.create_item("Boss Clear"))
        self.get_location("Roger The Ghost's Boss Room").place_locked_item(self.create_item("Boss Clear"))
        self.get_location("Prince Froggy's Boss Room").place_locked_item(self.create_item("Boss Clear"))
        self.get_location("Naval Piranha's Boss Room").place_locked_item(self.create_item("Boss Clear"))
        self.get_location("Marching Milde's Boss Room").place_locked_item(self.create_item("Boss Clear"))
        self.get_location("Hookbill The Koopa's Boss Room").place_locked_item(self.create_item("Boss Clear"))
        self.get_location("Sluggy The Unshaven's Boss Room").place_locked_item(self.create_item("Boss Clear"))
        self.get_location("Raphael The Raven's Boss Room").place_locked_item(self.create_item("Boss Clear"))
        self.get_location("Tap-Tap The Red Nose's Boss Room").place_locked_item(self.create_item("Boss Clear"))

        if self.options.goal == PlayerGoal.option_luigi_hunt:
            self.get_location("Reconstituted Luigi").place_locked_item(self.create_item("Saved Baby Luigi"))
        else:
            self.get_location("King Bowser's Castle: Level Clear").place_locked_item(
                self.create_item("Saved Baby Luigi")
            )

        self.get_location("Touch Fuzzy Get Dizzy: Gather Coins").place_locked_item(
            self.create_item("Bandit Consumables")
        )
        self.get_location("The Cave Of the Mystery Maze: Seed Spitting Contest").place_locked_item(
            self.create_item("Bandit Watermelons")
        )
        self.get_location("Lakitu's Wall: Gather Coins").place_locked_item(self.create_item("Bandit Consumables"))
        self.get_location("Ride Like The Wind: Gather Coins").place_locked_item(self.create_item("Bandit Consumables"))

    def generate_early(self) -> None:
        setup_gamevars(self)

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()

        starting_gate = ["World 1 Gate", "World 2 Gate", "World 3 Gate",
                         "World 4 Gate", "World 5 Gate", "World 6 Gate"]

        excluded_items.add(starting_gate[self.options.starting_world])

        if not self.options.shuffle_midrings:
            excluded_items.add("Middle Ring")

        if not self.options.add_secretlens:
            excluded_items.add("Secret Lens")

        if not self.options.extras_enabled:
            excluded_items.add("Extra Panels")
            excluded_items.add("Extra 1")
            excluded_items.add("Extra 2")
            excluded_items.add("Extra 3")
            excluded_items.add("Extra 4")
            excluded_items.add("Extra 5")
            excluded_items.add("Extra 6")

        if self.options.split_extras:
            excluded_items.add("Extra Panels")
        else:
            excluded_items.add("Extra 1")
            excluded_items.add("Extra 2")
            excluded_items.add("Extra 3")
            excluded_items.add("Extra 4")
            excluded_items.add("Extra 5")
            excluded_items.add("Extra 6")

        if self.options.split_bonus:
            excluded_items.add("Bonus Panels")
        else:
            excluded_items.add("Bonus 1")
            excluded_items.add("Bonus 2")
            excluded_items.add("Bonus 3")
            excluded_items.add("Bonus 4")
            excluded_items.add("Bonus 5")
            excluded_items.add("Bonus 6")

        return excluded_items

    def create_item_with_correct_settings(self, name: str) -> Item:
        data = item_table[name]
        item = Item(name, data.classification, data.code, self.player)

        if not item.advancement:
            return item

        if name == "Car Morph" and self.options.stage_logic != StageLogic.option_strict:
            item.classification = ItemClassification.useful

        secret_lens_visibility_check = (
                self.options.hidden_object_visibility >= ObjectVis.option_clouds_only
                or self.options.stage_logic != StageLogic.option_strict
        )
        if name == "Secret Lens" and secret_lens_visibility_check:
            item.classification = ItemClassification.useful

        is_bonus_location = name in {"Bonus 1", "Bonus 2", "Bonus 3", "Bonus 4", "Bonus 5", "Bonus 6", "Bonus Panels"}
        bonus_games_disabled = (
            self.options.minigame_checks not in {MinigameChecks.option_bonus_games, MinigameChecks.option_both}
        )
        if is_bonus_location and bonus_games_disabled:
            item.classification = ItemClassification.useful

        if name in {"Bonus 1", "Bonus 3", "Bonus 4", "Bonus Panels"} and self.options.item_logic:
            item.classification = ItemClassification.progression

        if name == "Piece of Luigi" and self.options.goal == PlayerGoal.option_luigi_hunt:
            if self.luigi_count >= self.options.luigi_pieces_required:
                item.classification = ItemClassification.useful
            else:
                item.classification = ItemClassification.progression_skip_balancing
                self.luigi_count += 1

        return item

    def generate_filler(self, pool: List[Item]) -> None:
        if self.options.goal == PlayerGoal.option_luigi_hunt:
            for _ in range(self.options.luigi_pieces_in_pool.value):
                item = self.create_item_with_correct_settings("Piece of Luigi")
                pool.append(item)

        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool) - 16):
            item = self.create_item_with_correct_settings(self.get_filler_item_name())
            pool.append(item)

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                for _ in range(data.amount):
                    item = self.create_item_with_correct_settings(name)
                    pool.append(item)

        return pool

    def create_items(self) -> None:
        self.luigi_count = 0

        if self.options.minigame_checks in {MinigameChecks.option_bonus_games, MinigameChecks.option_both}:
            self.multiworld.get_location("Flip Cards", self.player).place_locked_item(
                self.create_item("Bonus Consumables"))
            self.multiworld.get_location("Drawing Lots", self.player).place_locked_item(
                self.create_item("Bonus Consumables"))
            self.multiworld.get_location("Match Cards", self.player).place_locked_item(
                self.create_item("Bonus Consumables"))

        pool = self.get_item_pool(self.get_excluded_items())

        self.generate_filler(pool)

        self.multiworld.itempool += pool

    def generate_output(self, output_directory: str) -> None:
        rompath = ""  # if variable is not declared finally clause may fail
        try:
            world = self.multiworld
            player = self.player
            rom = LocalRom(get_base_rom_path())
            patch_rom(self, rom, self.player)

            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = YoshisIslandDeltaPatch(os.path.splitext(rompath)[0] + YoshisIslandDeltaPatch.patch_file_ending,
                                           player=player, player_name=world.player_name[player], patched_path=rompath)
            patch.write()
        finally:
            self.rom_name_available_event.set()
            if os.path.exists(rompath):
                os.unlink(rompath)

    def modify_multidata(self, multidata: dict) -> None:
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]) -> None:
        world_names = [f"World {i}" for i in range(1, 7)]
        world_stages = [
            self.world_1_stages, self.world_2_stages, self.world_3_stages,
            self.world_4_stages, self.world_5_stages, self.world_6_stages
        ]

        stage_pos_data = {}
        for loc in self.multiworld.get_locations(self.player):
            if loc.address is None:
                continue

            level_id = getattr(loc, "level_id")
            for level, stages in zip(world_names, world_stages):
                if level_id in stages:
                    stage_pos_data[loc.address] = level
                    break

        hint_data[self.player] = stage_pos_data
