import os
import unittest
from argparse import Namespace
from contextlib import contextmanager
from typing import Dict, ClassVar, Iterable, Hashable, Tuple, Optional, List, Union, Any

from BaseClasses import MultiWorld, CollectionState, get_seed, Location
from Options import VerifyKeys
from Utils import cache_argsless
from test.bases import WorldTestBase
from test.general import gen_steps, setup_solo_multiworld as setup_base_solo_multiworld
from worlds.AutoWorld import call_all
from .assertion import RuleAssertMixin
from .. import StardewValleyWorld, options
from ..mods.mod_data import all_mods
from ..options import StardewValleyOptions, StardewValleyOption

DEFAULT_TEST_SEED = get_seed()


# TODO is this caching really changing anything?
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
    option_dict = default_options().copy()
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
    return {
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
        options.Mods.internal_name: frozenset(),
    }


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
    min_max_options = minimal_locations_maximal_items().copy()
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
    return {
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


@cache_argsless
def allsanity_options_with_mods():
    allsanity = allsanity_options_without_mods().copy()
    allsanity.update({options.Mods.internal_name: all_mods})
    return allsanity


class SVTestCase(unittest.TestCase):
    # Set False to not skip some 'extra' tests
    skip_base_tests: bool = True
    # Set False to run tests that take long
    skip_long_tests: bool = True

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        base_tests_key = "base"
        if base_tests_key in os.environ:
            cls.skip_base_tests = not bool(os.environ[base_tests_key])
        long_tests_key = "long"
        if long_tests_key in os.environ:
            cls.skip_long_tests = not bool(os.environ[long_tests_key])

    @contextmanager
    def solo_world_sub_test(self, msg: Optional[str] = None,
                            /,
                            world_options: Optional[Dict[Union[str, StardewValleyOption], Any]] = None,
                            *,
                            seed=DEFAULT_TEST_SEED,
                            world_caching=True,
                            dirty_state=False,
                            **kwargs) -> Tuple[MultiWorld, StardewValleyWorld]:
        if msg is not None:
            msg += " "
        else:
            msg = ""
        msg += f"[Seed = {seed}]"

        with self.subTest(msg, **kwargs):
            if world_caching:
                multi_world = setup_solo_multiworld(world_options, seed)
                if dirty_state:
                    original_state = multi_world.state.copy()
            else:
                multi_world = setup_solo_multiworld(world_options, seed, _cache={})

            yield multi_world, multi_world.worlds[1]

            if world_caching and dirty_state:
                multi_world.state = original_state


class SVTestBase(RuleAssertMixin, WorldTestBase, SVTestCase):
    game = "Stardew Valley"
    world: StardewValleyWorld
    player: ClassVar[int] = 1

    seed = DEFAULT_TEST_SEED

    options = get_minsanity_options()

    def world_setup(self, *args, **kwargs):
        self.options = parse_class_option_keys(self.options)

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

    def get_real_locations(self) -> List[Location]:
        return [location for location in self.multiworld.get_locations(self.player) if not location.event]

    def get_real_location_names(self) -> List[str]:
        return [location.name for location in self.multiworld.get_locations(self.player) if not location.event]


pre_generated_worlds = {}


# Mostly a copy of test.general.setup_solo_multiworld, I just don't want to change the core.
def setup_solo_multiworld(test_options: Optional[Dict[Union[str, StardewValleyOption], str]] = None,
                          seed=DEFAULT_TEST_SEED,
                          _cache: Dict[Hashable, MultiWorld] = {},  # noqa
                          _steps=gen_steps) -> MultiWorld:
    test_options = parse_class_option_keys(test_options)

    # Yes I reuse the worlds generated between tests, its speeds the execution by a couple seconds
    should_cache = "start_inventory" not in test_options
    frozen_options = frozenset({})
    if should_cache:
        frozen_options = frozenset(test_options.items()).union({seed})
        if frozen_options in _cache:
            cached_multi_world = _cache[frozen_options]
            print(f"Using cached solo multi world [Seed = {cached_multi_world.seed}]")
            return cached_multi_world

    multiworld = setup_base_solo_multiworld(StardewValleyWorld, (), seed=seed)
    # print(f"Seed: {multiworld.seed}") # Uncomment to print the seed for every test

    args = Namespace()
    for name, option in StardewValleyWorld.options_dataclass.type_hints.items():
        value = option.from_any(test_options.get(name, option.default))

        if issubclass(option, VerifyKeys):
            # Values should already be verified, but just in case...
            option.verify_keys(value.value)

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


def parse_class_option_keys(test_options: dict) -> dict:
    """ Now the option class is allowed as key. """
    parsed_options = {}

    if test_options:
        for option, value in test_options.items():
            if hasattr(option, "internal_name"):
                assert option.internal_name not in test_options, "Defined two times by class and internal_name"
                parsed_options[option.internal_name] = value
            else:
                assert option in StardewValleyOptions.type_hints, \
                    f"All keys of world_options must be a possible Stardew Valley option, {option} is not."
                parsed_options[option] = value

    return parsed_options


def complete_options_with_default(options_to_complete=None) -> StardewValleyOptions:
    if options_to_complete is None:
        options_to_complete = {}

    for name, option in StardewValleyOptions.type_hints.items():
        options_to_complete[name] = option.from_any(options_to_complete.get(name, option.default))

    return StardewValleyOptions(**options_to_complete)


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
