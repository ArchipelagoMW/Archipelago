import logging

from BaseClasses import Tutorial, ItemClassification, MultiWorld, CollectionState, Item
from Fill import fill_restrictive
from Options import PerGameCommonOptions
from worlds.AutoWorld import World, WebWorld
from .items import item_table, item_names, copy_ability_table, animal_friend_table, filler_item_weights, KDL3Item, \
    trap_item_table, copy_ability_access_table, star_item_weights, total_filler_weights, animal_friend_spawn_table,\
    lookup_item_to_id
from .locations import location_table, KDL3Location, level_consumables, consumable_locations, star_locations
from .names.animal_friend_spawns import animal_friend_spawns, problematic_sets
from .names.enemy_abilities import vanilla_enemies, enemy_mapping, enemy_restrictive
from .regions import create_levels, default_levels
from .options import KDL3Options, kdl3_option_groups
from .presets import kdl3_options_presets
from .names import location_name
from .room import KDL3Room
from .rules import set_rules
from .rom import KDL3ProcedurePatch, get_base_rom_path, patch_rom, KDL3JHASH, KDL3UHASH
from .client import KDL3SNIClient

from typing import Dict, TextIO, Optional, List, Any, Mapping, ClassVar, Type
import os
import math
import threading
import base64
import settings

logger = logging.getLogger("Kirby's Dream Land 3")


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
    options_presets = kdl3_options_presets
    option_groups = kdl3_option_groups


class KDL3World(World):
    """
    Join Kirby and his Animal Friends on an adventure to collect Heart Stars and drive Dark Matter away from Dream Land!
    """

    game = "Kirby's Dream Land 3"
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = KDL3Options
    options: KDL3Options
    item_name_to_id = lookup_item_to_id
    location_name_to_id = {location_table[location]: location for location in location_table}
    item_name_groups = item_names
    web = KDL3WebWorld()
    settings: ClassVar[KDL3Settings]

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name: bytes = bytes()
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)
        self.copy_abilities: Dict[str, str] = vanilla_enemies.copy()
        self.required_heart_stars: int = 0  # we fill this during create_items
        self.boss_requirements: List[int] = []
        self.player_levels = default_levels.copy()
        self.stage_shuffle_enabled = False
        self.boss_butch_bosses: List[Optional[bool]] = []
        self.rooms: List[KDL3Room] = []

    create_regions = create_levels

    def generate_early(self) -> None:
        if self.options.total_heart_stars != -1:
            logger.warning(f"Kirby's Dream Land 3 ({self.player_name}): Use of \"total_heart_stars\" is deprecated. "
                           f"Please use \"max_heart_stars\" instead.")
            self.options.max_heart_stars.value = self.options.total_heart_stars.value

    def create_item(self, name: str, force_non_progression: bool = False) -> KDL3Item:
        item = item_table[name]
        classification = ItemClassification.filler
        if item.progression and not force_non_progression:
            classification = ItemClassification.progression_skip_balancing \
                if item.skip_balancing else ItemClassification.progression
        elif item.trap:
            classification = ItemClassification.trap
        return KDL3Item(name, classification, item.code, self.player)

    def get_filler_item_name(self, include_stars: bool = True) -> str:
        if include_stars:
            return self.random.choices(list(total_filler_weights.keys()),
                                       weights=list(total_filler_weights.values()))[0]
        return self.random.choices(list(filler_item_weights.keys()),
                                   weights=list(filler_item_weights.values()))[0]

    def get_trap_item_name(self) -> str:
        return self.random.choices(["Gooey Bag", "Slowness", "Eject Ability"],
                                   weights=[self.options.gooey_trap_weight.value,
                                            self.options.slow_trap_weight.value,
                                            self.options.ability_trap_weight.value])[0]

    def get_restrictive_copy_ability_placement(self, copy_ability: str, enemies_to_set: List[str],
                                               level: int, stage: int) -> Optional[str]:
        valid_rooms = [room for room in self.rooms if (room.level < level)
                       or (room.level == level and room.stage < stage)]  # leave out the stage in question to avoid edge
        valid_enemies = set()
        for room in valid_rooms:
            valid_enemies.update(room.enemies)
        placed_enemies = [enemy for enemy in valid_enemies if enemy not in enemies_to_set]
        if any(self.copy_abilities[enemy] == copy_ability for enemy in placed_enemies):
            return None  # a valid enemy got placed by a more restrictive placement
        return self.random.choice(sorted([enemy for enemy in valid_enemies if enemy not in placed_enemies]))

    def get_pre_fill_items(self) -> List[Item]:
        return [self.create_item(item)
                for item in [*copy_ability_access_table.keys(), *animal_friend_spawn_table.keys()]]

    def pre_fill(self) -> None:
        if self.options.copy_ability_randomization:
            # randomize copy abilities
            valid_abilities = list(copy_ability_access_table.keys())
            enemies_to_set = list(self.copy_abilities.keys())
            unplaced_abilities = set(key for key in copy_ability_access_table.keys()
                                     if key not in ("No Ability", "Cutter Ability", "Burning Ability"))
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
                    chosen_ability = self.random.choice(abilities)
                    self.copy_abilities[chosen_enemy] = chosen_ability
                    enemies_to_set.remove(chosen_enemy)
                    unplaced_abilities.discard(chosen_ability)
            # two less restrictive ones, we need to ensure Cutter and Burning appear before their required stages
            sand_canyon_5 = self.get_region("Sand Canyon 5 - 9")
            # this is primarily for typing, but if this ever hits it's fine to crash
            assert isinstance(sand_canyon_5, KDL3Room)
            cutter_enemy = self.get_restrictive_copy_ability_placement("Cutter Ability", enemies_to_set,
                                                                       sand_canyon_5.level, sand_canyon_5.stage)
            if cutter_enemy:
                self.copy_abilities[cutter_enemy] = "Cutter Ability"
                enemies_to_set.remove(cutter_enemy)
            iceberg_4 = self.get_region("Iceberg 4 - 7")
            # this is primarily for typing, but if this ever hits it's fine to crash
            assert isinstance(iceberg_4, KDL3Room)
            burning_enemy = self.get_restrictive_copy_ability_placement("Burning Ability", enemies_to_set,
                                                                        iceberg_4.level, iceberg_4.stage)
            if burning_enemy:
                self.copy_abilities[burning_enemy] = "Burning Ability"
                enemies_to_set.remove(burning_enemy)
            # ensure we place one of every ability
            if unplaced_abilities and self.options.accessibility != self.options.accessibility.option_minimal:
                # failsafe, on non-minimal we need to guarantee every copy ability exists
                for ability in sorted(unplaced_abilities):
                    enemy = self.random.choice(enemies_to_set)
                    self.copy_abilities[enemy] = ability
                    enemies_to_set.remove(enemy)
            # place remaining
            for enemy in enemies_to_set:
                self.copy_abilities[enemy] = self.random.choice(valid_abilities)
        for enemy in enemy_mapping:
            self.multiworld.get_location(enemy, self.player) \
                .place_locked_item(self.create_item(self.copy_abilities[enemy_mapping[enemy]]))
        # fill animals
        if self.options.animal_randomization != 0:
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
            if self.options.animal_randomization == 1:
                animal_pool = [animal_friend_spawns[spawn] for spawn in animal_friend_spawns
                               if spawn not in ["Ripple Field 5 - Animal 2", "Sand Canyon 6 - Animal 1",
                                                "Iceberg 4 - Animal 1"]]
            else:
                animal_base = ["Rick Spawn", "Kine Spawn", "Coo Spawn", "Nago Spawn", "ChuChu Spawn", "Pitch Spawn"]
                animal_pool = [self.random.choice(animal_base)
                               for _ in range(len(animal_friend_spawns) - 10)]
                # have to guarantee one of each animal
                animal_pool.extend(animal_base)
            if guaranteed_animal == "Kine Spawn":
                animal_pool.append("Coo Spawn")
            else:
                animal_pool.append("Kine Spawn")
            locations = [self.multiworld.get_location(spawn, self.player) for spawn in spawns]
            items: List[Item] = [self.create_item(animal) for animal in animal_pool]
            allstate = CollectionState(self.multiworld)
            for item in [*copy_ability_table, *animal_friend_table, *["Heart Star" for _ in range(99)]]:
                self.collect(allstate, self.create_item(item))
            self.random.shuffle(locations)
            fill_restrictive(self.multiworld, allstate, locations, items, True, True)

            # Need to ensure all of these are unique items, and replace them if they aren't
            for spawns in problematic_sets:
                placed = [self.get_location(spawn).item for spawn in spawns]
                placed_names = set([item.name for item in placed])
                if len(placed_names) != len(placed):
                    # have a duplicate
                    animals = []
                    for spawn in spawns:
                        spawn_location = self.get_location(spawn)
                        if spawn_location.item.name not in animals:
                            animals.append(spawn_location.item.name)
                        else:
                            new_animal = self.random.choice([x for x in ["Rick Spawn", "Coo Spawn", "Kine Spawn",
                                                                         "ChuChu Spawn", "Nago Spawn", "Pitch Spawn"]
                                                             if x not in placed_names and x not in animals])
                            spawn_location.item = None
                            spawn_location.place_locked_item(self.create_item(new_animal))
                            animals.append(new_animal)
                            # logically, this should be sound pre-ER. May need to adjust around it with ER in the future
        else:
            animal_friends = animal_friend_spawns.copy()
            for animal in animal_friends:
                self.multiworld.get_location(animal, self.player) \
                    .place_locked_item(self.create_item(animal_friends[animal]))

    def create_items(self) -> None:
        itempool = []
        itempool.extend([self.create_item(name) for name in copy_ability_table])
        itempool.extend([self.create_item(name) for name in animal_friend_table])
        required_percentage = self.options.heart_stars_required / 100.0
        remaining_items = len(location_table) - len(itempool)
        if not self.options.consumables:
            remaining_items -= len(consumable_locations)
        if not self.options.starsanity:
            remaining_items -= len(star_locations)
        max_heart_stars = self.options.max_heart_stars.value
        if max_heart_stars > remaining_items:
            max_heart_stars = remaining_items
        # ensure at least 1 heart star required per world
        required_heart_stars = min(max(int(max_heart_stars * required_percentage), 5), 99)
        filler_items = remaining_items - required_heart_stars
        converted_heart_stars = math.floor((max_heart_stars - required_heart_stars) * (self.options.filler_percentage / 100.0))
        non_required_heart_stars = max_heart_stars - converted_heart_stars - required_heart_stars
        filler_items -= non_required_heart_stars
        trap_amount = math.floor(filler_items * (self.options.trap_percentage / 100.0))

        filler_items -= trap_amount
        self.required_heart_stars = required_heart_stars
        # handle boss requirements here
        requirements = [required_heart_stars]
        quotient = required_heart_stars // 5  # since we set the last manually, we can afford imperfect rounding
        if self.options.boss_requirement_random:
            for i in range(1, 5):
                if self.options.strict_bosses:
                    max_stars = quotient * i
                else:
                    max_stars = required_heart_stars
                requirements.insert(i, self.random.randint(
                    min(1, max_stars), max_stars))
            if self.options.strict_bosses:
                requirements.sort()
            else:
                self.random.shuffle(requirements)
        else:
            for i in range(1, 5):
                requirements.insert(i - 1, quotient * i)
        self.boss_requirements = requirements
        itempool.extend([self.create_item("Heart Star") for _ in range(required_heart_stars)])
        itempool.extend([self.create_item(self.get_filler_item_name(bool(self.options.starsanity.value)))
                         for _ in range(filler_items)])
        itempool.extend([self.create_item(self.get_trap_item_name())
                         for _ in range(trap_amount)])
        itempool.extend([self.create_item("Heart Star", True) for _ in range(non_required_heart_stars)])
        self.multiworld.itempool += itempool
        if self.options.open_world:
            for level in self.player_levels:
                for stage in range(0, 6):
                    self.multiworld.get_location(location_table[self.player_levels[level][stage]]
                                                 .replace("Complete", "Stage Completion"), self.player) \
                        .place_locked_item(KDL3Item(
                            f"{location_name.level_names_inverse[level]} - Stage Completion",
                            ItemClassification.progression, None, self.player))

    set_rules = set_rules

    def generate_basic(self) -> None:
        self.stage_shuffle_enabled = self.options.stage_shuffle > 0
        goal = self.options.goal.value
        goal_location = self.multiworld.get_location(location_name.goals[goal], self.player)
        goal_location.place_locked_item(KDL3Item("Love-Love Rod", ItemClassification.progression, None, self.player))
        for level in range(1, 6):
            self.multiworld.get_location(f"Level {level} Boss - Defeated", self.player) \
                .place_locked_item(
                KDL3Item(f"Level {level} Boss Defeated", ItemClassification.progression, None, self.player))
            self.multiworld.get_location(f"Level {level} Boss - Purified", self.player) \
                .place_locked_item(
                KDL3Item(f"Level {level} Boss Purified", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Love-Love Rod", self.player)
        # this can technically be done at any point before generate_output
        if self.options.allow_bb:
            if self.options.allow_bb == self.options.allow_bb.option_enforced:
                self.boss_butch_bosses = [True for _ in range(6)]
            else:
                self.boss_butch_bosses = [self.random.choice([True, False]) for _ in range(6)]
        else:
            self.boss_butch_bosses = [False for _ in range(6)]

    def generate_output(self, output_directory: str) -> None:
        try:
            patch = KDL3ProcedurePatch(player=self.player, player_name=self.player_name)
            patch_rom(self, patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        assert isinstance(self.rom_name, bytes)
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(self.rom_name).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def fill_slot_data(self) -> Mapping[str, Any]:
        # UT support
        return {"player_levels": self.player_levels}

    def interpret_slot_data(self, slot_data: Mapping[str, Any]):
        # UT support
        player_levels = {int(key): value for key, value in slot_data["player_levels"].items()}
        return {"player_levels": player_levels}

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.stage_shuffle_enabled:
            spoiler_handle.write(f"\nLevel Layout ({self.multiworld.get_player_name(self.player)}):\n")
            for level in location_name.level_names:
                for stage, i in zip(self.player_levels[location_name.level_names[level]], range(1, 7)):
                    spoiler_handle.write(f"{level} {i}: {location_table[stage].replace(' - Complete', '')}\n")
        if self.options.animal_randomization:
            spoiler_handle.write(f"\nAnimal Friends ({self.multiworld.get_player_name(self.player)}):\n")
            for lvl in self.player_levels:
                for stage in range(6):
                    rooms = [room for room in self.rooms if room.level == lvl and room.stage == stage]
                    animals = []
                    for room in rooms:
                        animals.extend([location.item.name.replace(" Spawn", "")
                                        for location in room.locations if "Animal" in location.name
                                        and location.item is not None])
                    spoiler_handle.write(f"{location_table[self.player_levels[lvl][stage]].replace(' - Complete','')}"
                                         f": {', '.join(animals)}\n")
        if self.options.copy_ability_randomization:
            spoiler_handle.write(f"\nCopy Abilities ({self.multiworld.get_player_name(self.player)}):\n")
            for enemy in self.copy_abilities:
                spoiler_handle.write(f"{enemy}: {self.copy_abilities[enemy].replace('No Ability', 'None').replace(' Ability', '')}\n")

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]) -> None:
        if self.stage_shuffle_enabled:
            regions = {location_name.level_names[level]: level for level in location_name.level_names}
            level_hint_data = {}
            for level in regions:
                for stage in range(7):
                    stage_name = self.multiworld.get_location(self.location_id_to_name[self.player_levels[level][stage]],
                                                              self.player).name.replace(" - Complete", "")
                    stage_regions = [room for room in self.rooms if stage_name in room.name]
                    for region in stage_regions:
                        for location in [location for location in list(region.get_locations()) if location.address]:
                            level_hint_data[location.address] = f"{regions[level]} {stage + 1 if stage < 6 else 'Boss'}"
            hint_data[self.player] = level_hint_data
