import logging
import typing

from BaseClasses import Tutorial, ItemClassification, MultiWorld
from Fill import fill_restrictive
from worlds.AutoWorld import World, WebWorld
from .Items import item_table, item_names, copy_ability_table, animal_friend_table, filler_item_weights, KDL3Item, \
    trap_item_table, copy_ability_access_table
from .Locations import location_table, KDL3Location, level_consumables, consumable_locations
from .Names.AnimalFriendSpawns import animal_friend_spawns
from .Names.EnemyAbilities import vanilla_enemies, enemy_mapping, enemy_restrictive
from .Regions import create_levels, default_levels
from .Options import kdl3_options
from .Names import LocationName
from .Rules import set_rules
from .Rom import KDL3DeltaPatch, get_base_rom_path, RomData, patch_rom, KDL3JHASH, KDL3UHASH
from .Client import KDL3SNIClient

from typing import Dict, TextIO, Optional, List
import os
import math
import threading
import base64
import settings
from worlds.LauncherComponents import components

logger = logging.getLogger("Kirby's Dream Land 3")


# SNIComponent = next(x for x in components if x.display_name == "SNI Client")
# SNIComponent.file_identifier.suffixes.append(".apkdl3")


class KDL3Settings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the KDL3 JP or EN rom"""
        description = "Kirby's Dream Land 3 ROM File"
        copy_to = "Kirby's Dream Land 3.sfc"
        md5s = [KDL3JHASH, KDL3UHASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class KDL3WebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [

        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Kirby's Dream Land 3 randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Silvris"]
        )
    ]


class KDL3World(World):
    """
    Join Kirby and his Animal Friends on an adventure to collect Heart Stars and drive Dark Matter away from Dream Land!
    """

    game = "Kirby's Dream Land 3"
    option_definitions = kdl3_options
    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = {location_table[location]: location for location in location_table}
    item_name_groups = item_names
    data_version = 1
    web = KDL3WebWorld()
    settings: typing.ClassVar[KDL3Settings]

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name = None
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)
        self.copy_abilities: Dict[str, str] = vanilla_enemies.copy()
        self.required_heart_stars: int = 0  # we fill this during create_items
        self.boss_requirements: Dict[int, int] = dict()
        self.player_levels = default_levels.copy()
        self.stage_shuffle_enabled = False
        self.boss_butch_bosses: List[Optional[bool]] = list()

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        rom_file: str = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(f"Could not find base ROM for {cls.game}: {rom_file}")

    create_regions = create_levels

    def create_item(self, name: str, force_non_progression=False) -> KDL3Item:
        item = item_table[name]
        classification = ItemClassification.filler
        if item.progression and not force_non_progression:
            classification = ItemClassification.progression_skip_balancing \
                if item.skip_balancing else ItemClassification.progression
        elif item.trap:
            classification = ItemClassification.trap
        return KDL3Item(name, classification, item.code, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(filler_item_weights.keys()),
                                   weights=list(filler_item_weights.values()))[0]

    def get_trap_item_name(self) -> str:
        return self.random.choices(["Gooey Bag", "Slowness", "Eject Ability"],
                                   weights=[self.multiworld.gooey_trap_weight[self.player],
                                            self.multiworld.slow_trap_weight[self.player],
                                            self.multiworld.ability_trap_weight[self.player]])[0]

    def pre_fill(self) -> None:
        if self.multiworld.copy_ability_randomization[self.player]:
            # randomize copy abilities
            valid_abilities = list(copy_ability_access_table.keys())
            enemies_to_set = list(self.copy_abilities.keys())
            # now for the edge cases
            for abilities, enemies in enemy_restrictive:
                available_enemies = list()
                for enemy in enemies:
                    if enemy not in enemies_to_set:
                        if self.copy_abilities[enemy] in abilities:
                            break
                    else:
                        available_enemies.append(enemy)
                else:
                    chosen_enemy = self.random.choice(available_enemies)
                    chosen_ability = self.random.choice(tuple(abilities))
                    self.copy_abilities[chosen_enemy] = chosen_ability
                    enemies_to_set.remove(chosen_enemy)
            # place remaining
            for enemy in enemies_to_set:
                self.copy_abilities[enemy] = self.random \
                    .choice(valid_abilities)

        for enemy in enemy_mapping:
            self.multiworld.get_location(enemy, self.player) \
                .place_locked_item(self.create_item(self.copy_abilities[enemy_mapping[enemy]]))
        # fill animals
        if self.multiworld.animal_randomization[self.player] != 0:
            spawns = [animal for animal in animal_friend_spawns.keys() if
                      animal not in ["Ripple Field 5 - Animal 2", "Sand Canyon 6 - Animal 1", "Iceberg 4 - Animal 1"]]
            self.multiworld.get_location("Iceberg 4 - Animal 1", self.player) \
                .place_locked_item(self.create_item("ChuChu Spawn"))
            # Not having ChuChu here makes the room impossible (since only she has vertical burning)
            self.multiworld.get_location("Ripple Field 5 - Animal 2", self.player) \
                .place_locked_item(self.create_item("Pitch Spawn"))
            guaranteed_animal = self.random.choice(["Kine Spawn", "Coo Spawn"])
            self.multiworld.get_location("Sand Canyon 6 - Animal 1", self.player) \
                .place_locked_item(self.create_item(guaranteed_animal))
            # Ripple Field 5 - Animal 2 needs to be Pitch to ensure accessibility on non-door rando
            if self.multiworld.animal_randomization[self.player] == 1:
                animal_pool = [animal_friend_spawns[spawn] for spawn in animal_friend_spawns
                               if spawn not in ["Ripple Field 5 - Animal 2", "Sand Canyon 6 - Animal 1",
                                                "Iceberg 4 - Animal 1"]]
            else:
                animal_base = ["Rick Spawn", "Kine Spawn", "Coo Spawn", "Nago Spawn", "ChuChu Spawn", "Pitch Spawn"]
                animal_pool = [self.random.choice(animal_base)
                               for _ in range(len(animal_friend_spawns) - 9)]
                # have to guarantee one of each animal
                animal_pool.extend(animal_base)
            if guaranteed_animal == "Kine Spawn":
                animal_pool.append("Coo Spawn")
            else:
                animal_pool.append("Kine Spawn")
            locations = [self.multiworld.get_location(spawn, self.player) for spawn in spawns]
            items = [self.create_item(animal) for animal in animal_pool]
            fill_restrictive(self.multiworld, self.multiworld.get_all_state(False), locations, items)
        else:
            animal_friends = animal_friend_spawns.copy()
            for animal in animal_friends:
                self.multiworld.get_location(animal, self.player) \
                    .place_locked_item(self.create_item(animal_friends[animal]))


    def create_items(self) -> None:
        itempool = []
        itempool.extend([self.create_item(name) for name in copy_ability_table])
        itempool.extend([self.create_item(name) for name in animal_friend_table])
        required_percentage = self.multiworld.heart_stars_required[self.player] / 100.0
        remaining_items = (len(location_table) if self.multiworld.consumables[self.player]
                           else len(location_table) - len(consumable_locations)) - len(itempool)
        total_heart_stars = self.multiworld.total_heart_stars[self.player]
        required_heart_stars = max(math.floor(total_heart_stars * required_percentage),
                                   5)  # ensure at least 1 heart star required
        filler_items = total_heart_stars - required_heart_stars
        filler_amount = math.floor(filler_items * (self.multiworld.filler_percentage[self.player] / 100.0))
        trap_amount = math.floor(filler_amount * (self.multiworld.trap_percentage[self.player] / 100.0))
        filler_amount -= trap_amount
        non_required_heart_stars = filler_items - filler_amount - trap_amount
        self.required_heart_stars = required_heart_stars
        # handle boss requirements here
        requirements = [required_heart_stars]
        quotient = required_heart_stars // 5  # since we set the last manually, we can afford imperfect rounding
        if self.multiworld.boss_requirement_random[self.player]:
            for i in range(1, 5):
                if self.multiworld.strict_bosses[self.player]:
                    max_stars = quotient * i
                else:
                    max_stars = required_heart_stars
                requirements.insert(i, self.random.randint(
                    min(1, max_stars), max_stars))
            if self.multiworld.strict_bosses[self.player]:
                requirements.sort()
            else:
                self.random.shuffle(requirements)
        else:
            for i in range(1, 5):
                requirements.insert(i - 1, quotient * i)
        self.boss_requirements = requirements
        itempool.extend([self.create_item("Heart Star") for _ in range(required_heart_stars)])
        itempool.extend([self.create_item(self.get_filler_item_name())
                         for _ in range(filler_amount + (remaining_items - total_heart_stars))])
        itempool.extend([self.create_item(self.get_trap_item_name())
                         for _ in range(trap_amount)])
        itempool.extend([self.create_item("Heart Star", True) for _ in range(non_required_heart_stars)])
        self.multiworld.itempool += itempool

        for level in self.player_levels:
            for stage in range(0, 6):
                self.multiworld.get_location(location_table[self.player_levels[level][stage]]
                                             .replace("Complete", "Stage Completion"), self.player) \
                    .place_locked_item(KDL3Item(
                    f"{LocationName.level_names_inverse[level]}"
                    f"{f' {stage + 1} ' if not self.multiworld.open_world[self.player] else ' '}- Stage Completion",
                    ItemClassification.progression, None, self.player))

    set_rules = set_rules

    def generate_basic(self) -> None:
        self.stage_shuffle_enabled = self.multiworld.stage_shuffle[self.player] > 0
        goal = self.multiworld.goal[self.player]
        goal_location = self.multiworld.get_location(LocationName.goals[goal], self.player)
        goal_location.place_locked_item(KDL3Item("Love-Love Rod", ItemClassification.progression, None, self.player))
        for level in range(1, 6):
            self.multiworld.get_location(f"Level {level} Boss", self.player) \
                .place_locked_item(
                KDL3Item(f"Level {level} Boss Purified", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Love-Love Rod", self.player)
        # this can technically be done at any point before generate_output
        self.boss_butch_bosses.extend([None for _ in range(6)])
        if self.multiworld.allow_bb[self.player]:
            for i in range(6):
                if self.multiworld.allow_bb[self.player] == 1:
                    self.boss_butch_bosses[i] = self.random.choice(
                        [True, False])
                else:
                    self.boss_butch_bosses[i] = True

    def generate_output(self, output_directory: str):
        rom_path = ""
        try:
            world = self.multiworld
            player = self.player

            rom = RomData(get_base_rom_path())
            patch_rom(self.multiworld, self.player, rom, self.required_heart_stars,
                      self.boss_requirements,
                      self.player_levels,
                      self.boss_butch_bosses,
                      self.copy_abilities,
                      self.random)

            rom_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")
            rom.write_to_file(rom_path)
            self.rom_name = rom.name

            patch = KDL3DeltaPatch(os.path.splitext(rom_path)[0] + KDL3DeltaPatch.patch_file_ending, player=player,
                                   player_name=world.player_name[player], patched_path=rom_path)
            patch.write()
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected
            if os.path.exists(rom_path):
                os.unlink(rom_path)

    def modify_multidata(self, multidata: dict):
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.stage_shuffle_enabled:
            spoiler_handle.write(f"\nLevel Layout ({self.multiworld.get_player_name(self.player)}):\n")
            for level in LocationName.level_names:
                for stage, i in zip(self.player_levels[LocationName.level_names[level]], range(1, 7)):
                    spoiler_handle.write(f"{level} {i}: {location_table[stage].replace(' - Complete', '')}\n")

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        if self.stage_shuffle_enabled:
            regions = {LocationName.level_names[level]: level for level in LocationName.level_names}
            level_hint_data = {}
            for level in self.player_levels:
                for i in range(len(self.player_levels[level]) - 1):
                    stage = self.player_levels[level][i]
                    level_hint_data[stage] = regions[level] + f" {i + 1}"
                    if stage & 0x200 == 0:
                        level_hint_data[stage + 0x100] = regions[level] + f" {i + 1}"
                    if self.multiworld.consumables[self.player] and stage & 0xFF in level_consumables:
                        for consumable in level_consumables[stage & 0xFF]:
                            level_hint_data[consumable + 0x770300] = regions[level] + f" {i + 1}"
            for i in range(5):
                level_hint_data[0x770200 + i] = regions[i + 1] + " Boss"
            hint_data[self.player] = level_hint_data
