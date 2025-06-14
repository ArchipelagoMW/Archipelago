import unittest
from itertools import combinations
from typing import ClassVar

from BaseClasses import get_seed
from test.param import classvar_matrix
from ..assertion.world_assert import WorldAssertMixin
from ..bases import skip_long_tests, SVTestCase, solo_multiworld
from ..options.option_names import all_option_choices
from ... import options


@unittest.skip
class TestDynamicOptionDebug(WorldAssertMixin, SVTestCase):

    def test_option_pair_debug(self):
        option_dict = {
            options.Goal.internal_name: options.Goal.option_cryptic_note,
            options.EntranceRandomization.internal_name: options.EntranceRandomization.option_buildings,
        }
        for i in range(1):
            seed = get_seed(76312028554502615508)
            with self.subTest(f"Seed: {seed}"):
                print(f"Seed: {seed}")
                with solo_multiworld(option_dict, seed=seed) as (multiworld, _):
                    self.assert_basic_checks(multiworld)


if skip_long_tests():
    raise unittest.SkipTest("Long tests disabled")


@classvar_matrix(options_and_choices=combinations(all_option_choices, 2))
class TestGenerateDynamicOptions(WorldAssertMixin, SVTestCase):
    options_and_choices: ClassVar[tuple[tuple[str, str], tuple[str, str]]]

    def test_given_option_pair_when_generate_then_basic_checks(self):
        (option1, option1_choice), (option2, option2_choice) = self.options_and_choices

        world_options = {
            option1: option1_choice,
            option2: option2_choice
        }

        with solo_multiworld(world_options, world_caching=False) as (multiworld, _):
            self.assert_basic_checks(multiworld)
