import itertools
import typing
from pathlib import Path
from collections import Counter
from typing import Any, ClassVar, Dict, List, Optional
import settings

from BaseClasses import CollectionState, Item, ItemClassification, MultiWorld, Tutorial
from Fill import fill_restrictive
from worlds.AutoWorld import WebWorld, World

from .client import MZMClient
from .items import item_data_table, major_item_data_table, mzm_item_name_groups, MZMItem
from .locations import full_location_table, location_count, mzm_location_name_groups
from .options import FullyPoweredSuit, Goal, LayoutPatches, MZMOptions, MorphBallPlacement, SpringBall, mzm_option_groups, \
    CombatLogicDifficulty, GameDifficulty, WallJumps, LogicDifficulty, HazardRuns
from .patch import MZMProcedurePatch, write_json_data
from .patcher import MD5_US, MD5_US_VC
from .patcher.layout_patches import LAYOUT_PATCH_MAPPING
from .regions import create_regions_and_connections
from .rules import set_location_rules
from .tricks import tricks_normal, tricks_advanced, tricky_shinesparks, hazard_runs_normal, hazard_runs_minimal


class MZMSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Metroid: Zero Mission ROM."""
        description = "Metroid: Zero Mission (U) ROM file"
        copy_to = "Metroid - Zero Mission (USA).gba"
        md5s = [MD5_US, MD5_US_VC]

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching),
        Set it to true to have the operating system default program open the rom
        Alternatively, set it to a path to a program to open the .gba file with
        """
    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: typing.Union[RomStart, bool] = True

class MZMWeb(WebWorld):
    theme = "ice"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Metroid: Zero Mission for Archipelago on your computer.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["N/A"]
    )

    tutorials = [setup]
    option_groups = mzm_option_groups


class MZMWorld(World):
    """
    Metroid: Zero Mission is a retelling of the first Metroid on NES. Relive Samus' first adventure on planet Zebes with
    new areas, items, enemies, and story! Logic based on Metroid: Zero Mission Randomizer by Biosp4rk and Dragonfangs,
    used with permission.
    """
    game: str = "Metroid Zero Mission"
    options_dataclass = MZMOptions
    options: MZMOptions
    topology_present = True
    settings: ClassVar[MZMSettings]

    web = MZMWeb()

    required_client_version = (0, 6, 3)

    item_name_to_id = {name: data.code for name, data in item_data_table.items()}
    location_name_to_id = {name: data.code for name, data in full_location_table.items()}

    item_name_groups = mzm_item_name_groups
    location_name_groups = mzm_location_name_groups

    starting_items: list[MZMItem]
    locked_items: list[MZMItem]
    pre_fill_items: list[MZMItem]
    removed_items: list[MZMItem]

    enabled_layout_patches: list[str]
    trick_allow_list: list[str]

    junk_fill_items: list[str]
    junk_fill_cdf: list[int]

    def generate_early(self):
        self.starting_items = []
        self.locked_items = []
        self.pre_fill_items = []
        self.removed_items = []
        self.junk_fill_items = list(self.options.junk_fill_weights.value.keys())
        self.junk_fill_cdf = list(itertools.accumulate(self.options.junk_fill_weights.value.values()))

        if self.options.metroid_dna_available.value < self.options.metroid_dna_required.value:
            self.options.metroid_dna_available = self.options.metroid_dna_required

        if self.options.layout_patches.value == LayoutPatches.option_true:
            self.enabled_layout_patches = list(LAYOUT_PATCH_MAPPING.keys())
        elif self.options.layout_patches.value == LayoutPatches.option_choice:
            self.enabled_layout_patches = list(self.options.selected_patches.value)
        else:
            self.enabled_layout_patches = []

        if self.options.logic_difficulty.value == LogicDifficulty.option_normal:
            self.trick_allow_list = list(tricks_normal.keys())
        elif self.options.logic_difficulty.value == LogicDifficulty.option_advanced:
            self.trick_allow_list = list(tricks_normal.keys())
            self.trick_allow_list.extend(tricks_advanced.keys())
        else:
            self.trick_allow_list = []

        if self.options.hazard_runs == HazardRuns.option_normal:
            self.trick_allow_list.extend(hazard_runs_normal.keys())
        elif self.options.hazard_runs == HazardRuns.option_minimal:
            self.trick_allow_list.extend(hazard_runs_minimal.keys())

        if self.options.tricky_shinesparks.value:
            self.trick_allow_list.extend(tricky_shinesparks.keys())

        for allowed_trick in self.options.tricks_allowed.value:
            self.trick_allow_list.append(allowed_trick)
        for denied_trick in self.options.tricks_denied.value:
            # If a player has put the same trick in both allow and deny, the trick will not be used
            if denied_trick in self.trick_allow_list:
                self.trick_allow_list.remove(denied_trick)

        if "Morph Ball" in self.options.start_inventory_from_pool:
            self.options.morph_ball = MorphBallPlacement(MorphBallPlacement.option_normal)
        if self.options.morph_ball == MorphBallPlacement.option_early:
            self.pre_fill_items.append(self.create_item("Morph Ball"))

        if self.options.fully_powered_suit == FullyPoweredSuit.option_ruins_test:
            self.locked_items.append(self.create_item("Fully Powered Suit"))
        elif self.options.fully_powered_suit == FullyPoweredSuit.option_start_with:
            self.starting_items.append(self.create_item("Fully Powered Suit"))
        elif self.options.fully_powered_suit == FullyPoweredSuit.option_legacy_always_usable:
            self.starting_items.append(self.create_item("Fully Powered Suit"))
            self.locked_items.append(self.create_item("Nothing"))

        if (self.options.walljumps == WallJumps.option_enabled
                or self.options.walljumps == WallJumps.option_enabled_not_logical):
            self.starting_items.append(self.create_item("Wall Jump"))
        if self.options.walljumps == WallJumps.option_disabled:
            self.removed_items.append(self.create_item("Wall Jump"))

        if "Spring Ball" in self.options.start_inventory_from_pool:
            self.options.spring_ball = SpringBall(True)
        if not self.options.spring_ball.value:
            self.removed_items.append(self.create_item("Spring Ball"))
            if "Spring Ball" in self.options.start_inventory:
                self.options.spring_ball = SpringBall(True)

        for item in self.starting_items:
            self.push_precollected(item)

    def create_regions(self) -> None:
        create_regions_and_connections(self)

        self.place_event("Ziplines Activated", "Kraid Zipline Activator")
        self.place_event("Kraid Defeated", "Kraid")
        self.place_event("Ridley Defeated", "Ridley")
        self.place_event("Mother Brain Defeated", "Mother Brain")
        self.place_event("Chozo Ghost Defeated", "Chozo Ghost")
        self.place_event("Mecha Ridley Defeated", "Mecha Ridley")
        self.place_event("Mission Accomplished!", "Chozodia Space Pirate's Ship")

        ruins_test_reward = self.get_location("Chozodia Ruins Test Reward")
        if self.options.fully_powered_suit == FullyPoweredSuit.option_ruins_test:
            ruins_test_reward.address = None
            ruins_test_reward.place_locked_item(self.create_item("Fully Powered Suit"))
        elif self.options.fully_powered_suit == FullyPoweredSuit.option_legacy_always_usable:
            ruins_test_reward.address = None
            ruins_test_reward.place_locked_item(self.create_item("Nothing"))

    def create_items(self) -> None:
        item_pool: List[MZMItem] = []

        item_pool_size = location_count - len(self.locked_items) - len(self.pre_fill_items)

        removed_majors = set(item.name for item in
                                self.starting_items + self.locked_items + self.pre_fill_items + self.removed_items)
        for name in major_item_data_table:
            if name not in removed_majors:
                item_pool.append(self.create_item(name))

        if self.options.goal.value == Goal.option_metroid_dna:
            item_pool.extend(self.create_tanks("Metroid DNA", self.options.metroid_dna_available, progression_balancing_count=0))

        # TODO: factor in hazard runs when determining etank progression count
        item_pool.extend(self.create_tanks("Energy Tank", 12))  # All energy tanks progression

        # Set only the minimum required ammo to satisfy combat/traversal logic as Progression
        if self.options.game_difficulty == GameDifficulty.option_normal:
            item_pool.extend(self.create_tanks("Power Bomb Tank", 9, 2, 3))  # 4 progression + 6 useful power bombs out of 18
        else:  # For Hard mode
            item_pool.extend(self.create_tanks("Power Bomb Tank", 9, 4, 5))  # 4 progression + 5 useful power bombs out of 9

        if self.options.combat_logic_difficulty == CombatLogicDifficulty.option_relaxed:
            item_pool.extend(self.create_tanks("Super Missile Tank", 15, 4, 5))  # 8 progression + 10 useful supers out of 30
            item_pool.extend(self.create_missile_tanks(50, 10, 3))  # 50 progression missiles out of 250
        elif self.options.combat_logic_difficulty == CombatLogicDifficulty.option_normal:
            item_pool.extend(self.create_tanks("Super Missile Tank", 15, 3, 5))  # 6 progression + 10 useful supers out of 30
            item_pool.extend(self.create_missile_tanks(50, 8))  # 40 progression missiles out of 250
        elif self.options.combat_logic_difficulty == CombatLogicDifficulty.option_minimal:
            item_pool.extend(self.create_tanks("Super Missile Tank", 15, 1, 3))  # 1 progression + 6 useful supers out of 30
            item_pool.extend(self.create_missile_tanks(50, 3))  # 15 progression missiles out of 250

        if len(item_pool) > item_pool_size:
            item_pool = item_pool[:item_pool_size]  # Last items should always be filler missiles
        while len(item_pool) < item_pool_size:
            item_pool.append(self.create_filler())

        self.multiworld.itempool += item_pool

    def set_rules(self) -> None:
        set_location_rules(self, full_location_table)
        self.multiworld.completion_condition[self.player] = lambda state: (
            state.has("Mission Accomplished!", self.player))

    def get_pre_fill_items(self):
        return list(self.pre_fill_items)

    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld):
        # Early-fill morph in prefill so more locations can be considered 'early' in regular fill
        all_state = CollectionState(multiworld)
        morph_balls: list[Item] = []
        for world in multiworld.get_game_worlds(cls.game):
            for item in world.get_pre_fill_items():
                if item.name == "Morph Ball":
                    morph_balls.append(item)
                else:
                    world.collect(all_state, item)
        all_state.sweep_for_advancements()
        players = {item.player for item in morph_balls}
        for player in players:
            if all_state.has("Mission Accomplished!", player):
                all_state.remove(multiworld.worlds[player].create_item("Mission Accomplished!"))
        for player in players:
            items = [item for item in morph_balls if item.player == player]
            locations = [loc for loc in multiworld.get_locations(player) if loc.can_reach(all_state) and not loc.item]
            multiworld.random.shuffle(locations)
            fill_restrictive(multiworld, all_state, locations, items,
                             single_player_placement=True, lock=True, allow_partial=False, allow_excluded=True,
                             name='Metroid Zero Mission Early Morph Balls')

    def generate_output(self, output_directory: str):
        output_path = Path(output_directory)

        patch = MZMProcedurePatch(player=self.player, player_name=self.player_name)
        write_json_data(self, patch)

        output_filename = self.multiworld.get_out_file_name_base(self.player)
        patch.write(output_path / f"{output_filename}{patch.patch_file_ending}")

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "goal": self.options.goal.value,
            "metroid_dna_required": self.options.metroid_dna_required.value,
            "game_difficulty": self.options.game_difficulty.value,
            "unknown_items_usable": self.options.fully_powered_suit.to_slot_data(),
            "walljumps": self.options.walljumps.value,
            "spring_ball": self.options.spring_ball.value,
            "layout_patches": self.options.layout_patches.value,
            "selected_patches": self.enabled_layout_patches,
            "logic_difficulty": self.options.logic_difficulty.value,
            "combat_logic_difficulty": self.options.combat_logic_difficulty.value,
            "ibj_in_logic": self.options.ibj_in_logic.value,
            "hazard_runs": self.options.hazard_runs.value,
            "tricks_allowed": self.options.tricks_allowed.value,
            "tricks_denied": self.options.tricks_denied.value,
            "tricky_shinesparks": self.options.tricky_shinesparks.value,
            "death_link": self.options.death_link.value,
            "remote_items": self.options.remote_items.value,
            "chozodia_access": self.options.chozodia_access.value,
        }

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choices(self.junk_fill_items, cum_weights=self.junk_fill_cdf)[0]

    def create_item(self, name: str, force_classification: Optional[ItemClassification] = None) -> MZMItem:
        return MZMItem(name,
                       force_classification if force_classification is not None else item_data_table[name].progression,
                       self.item_name_to_id[name],
                       self.player)

    # Overridden so the extra minor items can be forced filler
    def create_filler(self) -> MZMItem:
        return self.create_item(self.get_filler_item_name(), ItemClassification.filler)

    def create_tanks(self, item_name: str, count: int,
                     progression_count: int | None = None, useful_count: int = 0,
                     progression_balancing_count: int | None = None, non_priority: bool = False):
        if progression_count is None:
            progression_count = count
        if progression_balancing_count is None:
            skip_balancing_count = 0
        else:
            skip_balancing_count = progression_count - progression_balancing_count
            progression_count = progression_balancing_count
        if useful_count is None:
            useful_count = 0

        if non_priority:
            for _ in range(progression_count):
                yield self.create_item(item_name, ItemClassification.progression_deprioritized)
            for _ in range(skip_balancing_count):
                yield self.create_item(item_name, ItemClassification.progression_deprioritized_skip_balancing)
        else:
            for _ in range(progression_count):
                yield self.create_item(item_name)
            for _ in range(skip_balancing_count):
                yield self.create_item(item_name, ItemClassification.progression_skip_balancing)
        for _ in range(useful_count):
            yield self.create_item(item_name, ItemClassification.useful)
        for _ in range(count - progression_count - skip_balancing_count - useful_count):
            yield self.create_item(item_name, ItemClassification.filler)

    def create_missile_tanks(self, count: int, progression_count: int, balance_count: int = 3):
        return self.create_tanks("Missile Tank", count, progression_count, 0, balance_count, True)

    def place_event(self, name: str, location_name: Optional[str] = None):
        if location_name is None:
            location_name = name
        item = MZMItem(name, ItemClassification.progression, None, self.player)
        location = self.multiworld.get_location(location_name, self.player)
        assert location.address is None
        location.place_locked_item(item)
        location.show_in_spoiler = True
