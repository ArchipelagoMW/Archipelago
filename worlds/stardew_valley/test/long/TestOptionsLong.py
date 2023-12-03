import unittest
from typing import Dict

from BaseClasses import MultiWorld
from Options import NamedRange
from .option_names import options_to_include
from worlds.stardew_valley.test.checks.world_checks import assert_can_win, assert_same_number_items_locations
from .. import setup_solo_multiworld, SVTestCase


def basic_checks(tester: unittest.TestCase, multiworld: MultiWorld):
    assert_can_win(tester, multiworld)
    assert_same_number_items_locations(tester, multiworld)


def get_option_choices(option) -> Dict[str, int]:
    if issubclass(option, NamedRange):
        return option.special_range_names
    elif option.options:
        return option.options
    return {}


class TestGenerateDynamicOptions(SVTestCase):
    def test_given_option_pair_when_generate_then_basic_checks(self):
        if self.skip_long_tests:
            return
        num_options = len(options_to_include)
        for option1_index in range(0, num_options):
            for option2_index in range(option1_index + 1, num_options):
                option1 = options_to_include[option1_index]
                option2 = options_to_include[option2_index]
                option1_choices = get_option_choices(option1)
                option2_choices = get_option_choices(option2)
                for key1 in option1_choices:
                    for key2 in option2_choices:
                        with self.subTest(f"{option1.internal_name}: {key1}, {option2.internal_name}: {key2}"):
                            choices = {option1.internal_name: option1_choices[key1],
                                       option2.internal_name: option2_choices[key2]}
                            multiworld = setup_solo_multiworld(choices)
                            basic_checks(self, multiworld)