import os
import unittest
from argparse import Namespace
from typing import Dict, ClassVar, Iterable

from BaseClasses import MultiWorld, CollectionState
from Utils import cache_argsless
from test.bases import WorldTestBase
from test.general import gen_steps, setup_solo_multiworld as setup_base_solo_multiworld
from worlds.AutoWorld import call_all
from .assertion import RuleAssertMixin
from .. import StardewValleyWorld, options
from ..mods.mod_data import all_mods


@cache_argsless
def disable_5_x_x_options():
    return {
        options.Monstersanity.internal_name: options.Monstersanity.option_none,
        options.Shipsanity.internal_name: options.Shipsanity.option_none,
        options.Cooksanity.internal_name: options.Cooksanity.option_none,
        options.Chefsanity.internal_name: options.Chefsanity.option_none,
        options.Craftsanity.internal_name: options.Craftsanity.option_none
    }


@cache_argsless
def default_4_x_x_options():
    option_dict = default_options()
    option_dict.update(disable_5_x_x_options())
    option_dict.update({
        options.BundleRandomization.internal_name: options.BundleRandomization.option_shuffled,
    })
    return option_dict


@cache_argsless
def default_options():
    return {}


@cache_argsless
def get_minsanity_options():
    minsanity = {
        options.Goal.internal_name: options.Goal.option_bottom_of_the_mines,
        options.BundleRandomization.internal_name: options.BundleRandomization.option_vanilla,
        options.BundlePrice.internal_name: options.BundlePrice.option_very_cheap,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_disabled,
        options.Cropsanity.internal_name: options.Cropsanity.option_disabled,
        options.BackpackProgression.internal_name: options.BackpackProgression.option_vanilla,
        options.ToolProgression.internal_name: options.ToolProgression.option_vanilla,
        options.SkillProgression.internal_name: options.SkillProgression.option_vanilla,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_vanilla,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_disabled,
        options.ElevatorProgression.internal_name: options.ElevatorProgression.option_vanilla,
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_disabled,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_disabled,
        options.QuestLocations.internal_name: -1,
        options.Fishsanity.internal_name: options.Fishsanity.option_none,
        options.Museumsanity.internal_name: options.Museumsanity.option_none,
        options.Monstersanity.internal_name: options.Monstersanity.option_none,
        options.Shipsanity.internal_name: options.Shipsanity.option_none,
        options.Cooksanity.internal_name: options.Cooksanity.option_none,
        options.Chefsanity.internal_name: options.Chefsanity.option_none,
        options.Craftsanity.internal_name: options.Craftsanity.option_none,
        options.Friendsanity.internal_name: options.Friendsanity.option_none,
        options.FriendsanityHeartSize.internal_name: 8,
        options.NumberOfMovementBuffs.internal_name: 0,
        options.NumberOfLuckBuffs.internal_name: 0,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
        options.TrapItems.internal_name: options.TrapItems.option_no_traps,
        options.Mods.internal_name: (),
    }
    return minsanity


@cache_argsless
def minimal_locations_maximal_items():
    min_max_options = {
        options.Goal.internal_name: options.Goal.option_craft_master,
        options.BundleRandomization.internal_name: options.BundleRandomization.option_shuffled,
        options.BundlePrice.internal_name: options.BundlePrice.option_expensive,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized,
        options.Cropsanity.internal_name: options.Cropsanity.option_disabled,
        options.BackpackProgression.internal_name: options.BackpackProgression.option_vanilla,
        options.ToolProgression.internal_name: options.ToolProgression.option_vanilla,
        options.SkillProgression.internal_name: options.SkillProgression.option_vanilla,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_vanilla,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_disabled,
        options.ElevatorProgression.internal_name: options.ElevatorProgression.option_vanilla,
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_disabled,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_disabled,
        options.QuestLocations.internal_name: -1,
        options.Fishsanity.internal_name: options.Fishsanity.option_none,
        options.Museumsanity.internal_name: options.Museumsanity.option_none,
        options.Monstersanity.internal_name: options.Monstersanity.option_none,
        options.Shipsanity.internal_name: options.Shipsanity.option_none,
        options.Cooksanity.internal_name: options.Cooksanity.option_none,
        options.Chefsanity.internal_name: options.Chefsanity.option_none,
        options.Craftsanity.internal_name: options.Craftsanity.option_none,
        options.Friendsanity.internal_name: options.Friendsanity.option_none,
        options.FriendsanityHeartSize.internal_name: 8,
        options.NumberOfMovementBuffs.internal_name: 12,
        options.NumberOfLuckBuffs.internal_name: 12,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
        options.TrapItems.internal_name: options.TrapItems.option_nightmare,
        options.Mods.internal_name: (),
    }
    return min_max_options


@cache_argsless
def minimal_locations_maximal_items_with_island():
    min_max_options = minimal_locations_maximal_items()
    min_max_options.update({options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false})
    return min_max_options


@cache_argsless
def allsanity_4_x_x_options_without_mods():
    option_dict = {
        options.Goal.internal_name: options.Goal.option_perfection,
        options.BundleRandomization.internal_name: options.BundleRandomization.option_thematic,
        options.BundlePrice.internal_name: options.BundlePrice.option_expensive,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_hard,
        options.ElevatorProgression.internal_name: options.ElevatorProgression.option_progressive,
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_full_shuffling,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
        options.QuestLocations.internal_name: 56,
        options.Fishsanity.internal_name: options.Fishsanity.option_all,
        options.Museumsanity.internal_name: options.Museumsanity.option_all,
        options.Monstersanity.internal_name: options.Monstersanity.option_progressive_goals,
        options.Shipsanity.internal_name: options.Shipsanity.option_everything,
        options.Cooksanity.internal_name: options.Cooksanity.option_all,
        options.Chefsanity.internal_name: options.Chefsanity.option_all,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 1,
        options.NumberOfMovementBuffs.internal_name: 12,
        options.NumberOfLuckBuffs.internal_name: 12,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false,
        options.TrapItems.internal_name: options.TrapItems.option_nightmare,
    }
    option_dict.update(disable_5_x_x_options())
    return option_dict


@cache_argsless
def allsanity_options_without_mods():
    allsanity = {
        options.Goal.internal_name: options.Goal.option_perfection,
        options.BundleRandomization.internal_name: options.BundleRandomization.option_thematic,
        options.BundlePrice.internal_name: options.BundlePrice.option_expensive,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_hard,
        options.ElevatorProgression.internal_name: options.ElevatorProgression.option_progressive,
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_full_shuffling,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
        options.QuestLocations.internal_name: 56,
        options.Fishsanity.internal_name: options.Fishsanity.option_all,
        options.Museumsanity.internal_name: options.Museumsanity.option_all,
        options.Monstersanity.internal_name: options.Monstersanity.option_progressive_goals,
        options.Shipsanity.internal_name: options.Shipsanity.option_everything,
        options.Cooksanity.internal_name: options.Cooksanity.option_all,
        options.Chefsanity.internal_name: options.Chefsanity.option_all,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 1,
        options.NumberOfMovementBuffs.internal_name: 12,
        options.NumberOfLuckBuffs.internal_name: 12,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false,
        options.TrapItems.internal_name: options.TrapItems.option_nightmare,
    }
    return allsanity


@cache_argsless
def allsanity_options_with_mods():
    allsanity = {}
    allsanity.update(allsanity_options_without_mods())
    allsanity.update({options.Mods.internal_name: all_mods})
    return allsanity


class SVTestCase(unittest.TestCase):
    game = "Stardew Valley"
    world: StardewValleyWorld
    player: ClassVar[int] = 1
    # Set False to not skip some 'extra' tests
    skip_base_tests: bool = True
    # Set False to run tests that take long
    skip_long_tests: bool = True

    options = get_minsanity_options()

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        base_tests_key = "base"
        if base_tests_key in os.environ:
            cls.skip_base_tests = not bool(os.environ[base_tests_key])
        long_tests_key = "long"
        if long_tests_key in os.environ:
            cls.skip_long_tests = not bool(os.environ[long_tests_key])


class SVTestBase(RuleAssertMixin, WorldTestBase, SVTestCase):
    seed = None

    def world_setup(self, *args, **kwargs):
        super().world_setup(seed=self.seed)
        if self.constructed:
            self.world = self.multiworld.worlds[self.player]  # noqa

    @property
    def run_default_tests(self) -> bool:
        if self.skip_base_tests:
            return False
        # world_setup is overridden, so it'd always run default tests when importing SVTestBase
        is_not_stardew_test = type(self) is not SVTestBase
        should_run_default_tests = is_not_stardew_test and super().run_default_tests
        return should_run_default_tests

    def collect_lots_of_money(self):
        self.multiworld.state.collect(self.world.create_item("Shipping Bin"), event=False)
        for i in range(100):
            self.multiworld.state.collect(self.world.create_item("Stardrop"), event=False)

    def collect_all_the_money(self):
        self.multiworld.state.collect(self.world.create_item("Shipping Bin"), event=False)
        for i in range(1000):
            self.multiworld.state.collect(self.world.create_item("Stardrop"), event=False)


pre_generated_worlds = {}


# Mostly a copy of test.general.setup_solo_multiworld, I just don't want to change the core.
def setup_solo_multiworld(test_options=None, seed=None, _cache: Dict[str, MultiWorld] = {}, _steps=gen_steps) -> MultiWorld:  # noqa
    if test_options is None:
        test_options = {}

    # Yes I reuse the worlds generated between tests, its speeds the execution by a couple seconds
    should_cache = "start_inventory" not in test_options
    frozen_options = frozenset({})
    if should_cache:
        frozen_options = frozenset(test_options.items()).union({seed})
        if frozen_options in _cache:
            return _cache[frozen_options]

    multiworld = setup_base_solo_multiworld(StardewValleyWorld, ())
    multiworld.set_seed(seed)
    # print(f"Seed: {multiworld.seed}") # Uncomment to print the seed for every test
    args = Namespace()
    for name, option in StardewValleyWorld.options_dataclass.type_hints.items():
        value = option(test_options[name]) if name in test_options else option.from_any(option.default)
        setattr(args, name, {1: value})
    multiworld.set_options(args)
    if "start_inventory" in test_options:
        for item, amount in test_options["start_inventory"].items():
            for _ in range(amount):
                multiworld.push_precollected(multiworld.create_item(item, 1))
    for step in _steps:
        call_all(multiworld, step)

    if should_cache:
        _cache[frozen_options] = multiworld

    return multiworld


def setup_multiworld(test_options: Iterable[Dict[str, int]] = None, seed=None) -> MultiWorld:  # noqa
    if test_options is None:
        test_options = []

    multiworld = MultiWorld(len(test_options))
    multiworld.player_name = {}
    multiworld.set_seed(seed)
    multiworld.state = CollectionState(multiworld)
    for i in range(1, len(test_options) + 1):
        multiworld.game[i] = StardewValleyWorld.game
        multiworld.player_name.update({i: f"Tester{i}"})
    args = Namespace()
    for name, option in StardewValleyWorld.options_dataclass.type_hints.items():
        options = {}
        for i in range(1, len(test_options) + 1):
            player_options = test_options[i - 1]
            value = option(player_options[name]) if name in player_options else option.from_any(option.default)
            options.update({i: value})
        setattr(args, name, options)
    multiworld.set_options(args)

    for step in gen_steps:
        call_all(multiworld, step)

    return multiworld
