import unittest
from typing import ClassVar

from test.param import classvar_matrix
from ..options.option_names import get_all_option_choices
from ...options import ExcludeGingerIsland, ArcadeMachineLocations, BackpackProgression, BackpackSize, \
    BundlePerRoom, BundlePrice, ElevatorProgression, FarmType, SeasonRandomization, FestivalLocations, Moviesanity, Museumsanity, ToolProgression
from ...test.assertion import WorldAssertMixin
from ...test.bases import SVTestCase, solo_multiworld, skip_long_tests

if skip_long_tests():
    raise unittest.SkipTest("Long tests disabled")

# These options affect logic, but are unrelated to any ginger island content, so pointless for this specific test class
extra_options_to_ignore = [ArcadeMachineLocations.internal_name, BackpackProgression.internal_name, BackpackSize.internal_name, BundlePerRoom.internal_name,
                           BundlePrice.internal_name, ElevatorProgression.internal_name, FarmType.internal_name, SeasonRandomization.internal_name,
                           FestivalLocations.internal_name, Moviesanity.internal_name, Museumsanity.internal_name, ToolProgression.internal_name]


@classvar_matrix(option_and_choice=get_all_option_choices(extra_options_to_ignore))
class TestGenerateAllOptionsWithExcludeGingerIsland(WorldAssertMixin, SVTestCase):
    option_and_choice: ClassVar[tuple[str, str]]

    def test_given_choice_when_generate_exclude_ginger_island_then_ginger_island_is_properly_excluded(self):
        option, option_choice = self.option_and_choice

        if option == ExcludeGingerIsland.internal_name:
            self.skipTest("ExcludeGingerIsland is forced to true")

        world_options = {
            ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
            option: option_choice
        }

        with solo_multiworld(world_options) as (multiworld, stardew_world):

            if stardew_world.options.exclude_ginger_island != ExcludeGingerIsland.option_true:
                self.skipTest("Some options, like goals, will force Ginger island back in the game. We want to skip testing those.")

            self.assert_basic_checks(multiworld)
            self.assert_no_ginger_island_content(multiworld)