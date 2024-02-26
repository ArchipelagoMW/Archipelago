import os
import unittest
from argparse import Namespace
from typing import Dict, FrozenSet, Tuple, Any, ClassVar

from BaseClasses import MultiWorld
from Utils import cache_argsless
from test.TestBase import WorldTestBase
from test.general import gen_steps, setup_solo_multiworld as setup_base_solo_multiworld
from .. import StardewValleyWorld
from ..mods.mod_data import ModNames
from worlds.AutoWorld import call_all
from ..options import Cropsanity, SkillProgression, SpecialOrderLocations, Friendsanity, NumberOfLuckBuffs, SeasonRandomization, ToolProgression, \
    ElevatorProgression, Museumsanity, BackpackProgression, BuildingProgression, ArcadeMachineLocations, HelpWantedLocations, Fishsanity, NumberOfMovementBuffs, \
    BundleRandomization, BundlePrice, FestivalLocations, FriendsanityHeartSize, ExcludeGingerIsland, TrapItems, Goal, Mods


class SVTestCase(unittest.TestCase):
    player: ClassVar[int] = 1
    """Set to False to not skip some 'extra' tests"""
    skip_extra_tests: bool = True
    """Set to False to run tests that take long"""
    skip_long_tests: bool = True


class SVTestBase(WorldTestBase, SVTestCase):
    game = "Stardew Valley"
    world: StardewValleyWorld

    def world_setup(self, *args, **kwargs):
        super().world_setup(*args, **kwargs)
        long_tests_key = "long"
        if long_tests_key in os.environ:
            self.skip_long_tests = not bool(os.environ[long_tests_key])
        if self.constructed:
            self.world = self.multiworld.worlds[self.player]  # noqa

    @property
    def run_default_tests(self) -> bool:
        # world_setup is overridden, so it'd always run default tests when importing SVTestBase
        is_not_stardew_test = type(self) is not SVTestBase
        should_run_default_tests = is_not_stardew_test and super().run_default_tests
        return should_run_default_tests


@cache_argsless
def minimal_locations_maximal_items():
    min_max_options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
        Cropsanity.internal_name: Cropsanity.option_enabled,
        BackpackProgression.internal_name: BackpackProgression.option_vanilla,
        ToolProgression.internal_name: ToolProgression.option_vanilla,
        SkillProgression.internal_name: SkillProgression.option_vanilla,
        BuildingProgression.internal_name: BuildingProgression.option_vanilla,
        ElevatorProgression.internal_name: ElevatorProgression.option_vanilla,
        ArcadeMachineLocations.internal_name: ArcadeMachineLocations.option_disabled,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_disabled,
        HelpWantedLocations.internal_name: 0,
        Fishsanity.internal_name: Fishsanity.option_none,
        Museumsanity.internal_name: Museumsanity.option_none,
        Friendsanity.internal_name: Friendsanity.option_none,
        NumberOfMovementBuffs.internal_name: 12,
        NumberOfLuckBuffs.internal_name: 12,
    }
    return min_max_options


@cache_argsless
def allsanity_options_without_mods():
    allsanity = {
        Goal.internal_name: Goal.option_perfection,
        BundleRandomization.internal_name: BundleRandomization.option_shuffled,
        BundlePrice.internal_name: BundlePrice.option_expensive,
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
        Cropsanity.internal_name: Cropsanity.option_enabled,
        BackpackProgression.internal_name: BackpackProgression.option_progressive,
        ToolProgression.internal_name: ToolProgression.option_progressive,
        SkillProgression.internal_name: SkillProgression.option_progressive,
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        FestivalLocations.internal_name: FestivalLocations.option_hard,
        ElevatorProgression.internal_name: ElevatorProgression.option_progressive,
        ArcadeMachineLocations.internal_name: ArcadeMachineLocations.option_full_shuffling,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi,
        HelpWantedLocations.internal_name: 56,
        Fishsanity.internal_name: Fishsanity.option_all,
        Museumsanity.internal_name: Museumsanity.option_all,
        Friendsanity.internal_name: Friendsanity.option_all_with_marriage,
        FriendsanityHeartSize.internal_name: 1,
        NumberOfMovementBuffs.internal_name: 12,
        NumberOfLuckBuffs.internal_name: 12,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        TrapItems.internal_name: TrapItems.option_nightmare,
    }
    return allsanity


@cache_argsless
def allsanity_options_with_mods():
    allsanity = {}
    allsanity.update(allsanity_options_without_mods())
    all_mods = (
        ModNames.deepwoods, ModNames.tractor, ModNames.big_backpack,
        ModNames.luck_skill, ModNames.magic, ModNames.socializing_skill, ModNames.archaeology,
        ModNames.cooking_skill, ModNames.binning_skill, ModNames.juna,
        ModNames.jasper, ModNames.alec, ModNames.yoba, ModNames.eugene,
        ModNames.wellwick, ModNames.ginger, ModNames.shiko, ModNames.delores,
        ModNames.ayeisha, ModNames.riley, ModNames.skull_cavern_elevator
    )
    allsanity.update({Mods.internal_name: all_mods})
    return allsanity


pre_generated_worlds = {}


# Mostly a copy of test.general.setup_solo_multiworld, I just don't want to change the core.
def setup_solo_multiworld(test_options=None, seed=None,
                          _cache: Dict[FrozenSet[Tuple[str, Any]], MultiWorld] = {}) -> MultiWorld:  # noqa
    if test_options is None:
        test_options = {}

    # Yes I reuse the worlds generated between tests, its speeds the execution by a couple seconds
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
    for step in gen_steps:
        call_all(multiworld, step)

    _cache[frozen_options] = multiworld

    return multiworld
