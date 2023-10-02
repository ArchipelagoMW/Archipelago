import os
from argparse import Namespace
from typing import Dict, FrozenSet, Tuple, Any, ClassVar

from BaseClasses import MultiWorld
from test.TestBase import WorldTestBase
from test.general import gen_steps, setup_solo_multiworld as setup_base_solo_multiworld
from .. import StardewValleyWorld, options
from ..mods.mod_data import ModNames
from worlds.AutoWorld import call_all


class SVTestBase(WorldTestBase):
    game = "Stardew Valley"
    world: StardewValleyWorld
    player: ClassVar[int] = 1
    skip_long_tests: bool = True

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

    def minimal_locations_maximal_items(self):
        min_max_options = {
            options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized,
            options.Cropsanity.internal_name: options.Cropsanity.option_shuffled,
            options.BackpackProgression.internal_name: options.BackpackProgression.option_vanilla,
            options.ToolProgression.internal_name: options.ToolProgression.option_vanilla,
            options.SkillProgression.internal_name: options.SkillProgression.option_vanilla,
            options.BuildingProgression.internal_name: options.BuildingProgression.option_vanilla,
            options.ElevatorProgression.internal_name: options.ElevatorProgression.option_vanilla,
            options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_disabled,
            options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_disabled,
            options.HelpWantedLocations.internal_name: 0,
            options.Fishsanity.internal_name: options.Fishsanity.option_none,
            options.Museumsanity.internal_name: options.Museumsanity.option_none,
            options.Friendsanity.internal_name: options.Friendsanity.option_none,
            options.NumberOfMovementBuffs.internal_name: 12,
            options.NumberOfLuckBuffs.internal_name: 12,
        }
        return min_max_options

    def allsanity_options_without_mods(self):
        allsanity = {
            options.Goal.internal_name: options.Goal.option_perfection,
            options.BundleRandomization.internal_name: options.BundleRandomization.option_shuffled,
            options.BundlePrice.internal_name: options.BundlePrice.option_expensive,
            options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized,
            options.Cropsanity.internal_name: options.Cropsanity.option_shuffled,
            options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
            options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
            options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
            options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive,
            options.FestivalLocations.internal_name: options.FestivalLocations.option_hard,
            options.ElevatorProgression.internal_name: options.ElevatorProgression.option_progressive,
            options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_full_shuffling,
            options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
            options.HelpWantedLocations.internal_name: 56,
            options.Fishsanity.internal_name: options.Fishsanity.option_all,
            options.Museumsanity.internal_name: options.Museumsanity.option_all,
            options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
            options.FriendsanityHeartSize.internal_name: 1,
            options.NumberOfMovementBuffs.internal_name: 12,
            options.NumberOfLuckBuffs.internal_name: 12,
            options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false,
            options.TrapItems.internal_name: options.TrapItems.option_nightmare,
        }
        return allsanity

    def allsanity_options_with_mods(self):
        allsanity = {}
        allsanity.update(self.allsanity_options_without_mods())
        all_mods = (
            ModNames.deepwoods, ModNames.tractor, ModNames.big_backpack,
            ModNames.luck_skill, ModNames.magic, ModNames.socializing_skill, ModNames.archaeology,
            ModNames.cooking_skill, ModNames.binning_skill, ModNames.juna,
            ModNames.jasper, ModNames.alec, ModNames.yoba, ModNames.eugene,
            ModNames.wellwick, ModNames.ginger, ModNames.shiko, ModNames.delores,
            ModNames.ayeisha, ModNames.riley, ModNames.skull_cavern_elevator
        )
        allsanity.update({options.Mods.internal_name: all_mods})
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
    for name, option in StardewValleyWorld.option_definitions.items():
        value = option(test_options[name]) if name in test_options else option.from_any(option.default)
        setattr(args, name, {1: value})
    multiworld.set_options(args)
    for step in gen_steps:
        call_all(multiworld, step)

    _cache[frozen_options] = multiworld

    return multiworld
