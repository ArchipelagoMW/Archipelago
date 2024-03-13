import unittest
from itertools import combinations

from .option_names import all_option_choices
from .. import setup_solo_multiworld, SVTestCase
from ..assertion.world_assert import WorldAssertMixin
from ... import options


class TestGenerateDynamicOptions(WorldAssertMixin, SVTestCase):
    def test_given_option_pair_when_generate_then_basic_checks(self):
        if self.skip_long_tests:
            raise unittest.SkipTest("Long tests disabled")

        for (option1, option1_choice), (option2, option2_choice) in combinations(all_option_choices, 2):
            if option1 is option2:
                continue

            world_options = {
                option1: option1_choice,
                option2: option2_choice
            }

            with self.solo_world_sub_test(f"{option1.internal_name}: {option1_choice}, {option2.internal_name}: {option2_choice}",
                                          world_options,
                                          world_caching=False) \
                    as (multiworld, _):
                self.assert_basic_checks(multiworld)


class TestDynamicOptionDebug(WorldAssertMixin, SVTestCase):

    def test_option_pair_debug(self):
        option_dict = {
            options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
            options.Monstersanity.internal_name: options.Monstersanity.option_one_per_monster,
        }
        for i in range(1):
            # seed = int(random() * pow(10, 18) - 1)
            seed = 823942126251776128
            with self.subTest(f"Seed: {seed}"):
                print(f"Seed: {seed}")
                multiworld = setup_solo_multiworld(option_dict, seed)
                self.assert_basic_checks(multiworld)
