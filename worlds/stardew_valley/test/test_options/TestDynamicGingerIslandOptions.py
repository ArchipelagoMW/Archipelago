from typing import ClassVar

from test.param import classvar_matrix
from ...options import ExcludeGingerIsland
from ...test.assertion import WorldAssertMixin
from ...test.bases import SVTestCase, solo_multiworld
from ...test.options.option_names import all_option_choices


@classvar_matrix(option_and_choice=all_option_choices)
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