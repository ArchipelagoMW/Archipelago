import unittest
from itertools import combinations

from BaseClasses import get_seed
from .option_names import all_option_choices
from .. import SVTestCase, solo_multiworld
from ..assertion.world_assert import WorldAssertMixin
from ... import options
from ...mods.mod_data import ModNames


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
            options.Goal.internal_name: options.Goal.option_master_angler,
            options.QuestLocations.internal_name: -1,
            options.Fishsanity.internal_name: options.Fishsanity.option_all,
            options.Mods.internal_name: frozenset({ModNames.sve}),
        }
        for i in range(1):
            seed = get_seed()
            with self.subTest(f"Seed: {seed}"):
                print(f"Seed: {seed}")
                with solo_multiworld(option_dict, seed=seed) as (multiworld, _):
                    self.assert_basic_checks(multiworld)
