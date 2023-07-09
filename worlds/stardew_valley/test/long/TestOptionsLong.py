from typing import Dict

from BaseClasses import ItemClassification, MultiWorld
from Options import SpecialRange
from .. import setup_solo_multiworld, SVTestBase
from ... import StardewItem
from ...options import stardew_valley_option_classes


def assert_can_win(tester: SVTestBase, multiworld: MultiWorld):
    for item in multiworld.get_items():
        multiworld.state.collect(item)

    tester.assertTrue(multiworld.find_item("Victory", 1).can_reach(multiworld.state))


def basic_checks(tester: SVTestBase, multiworld: MultiWorld):
    tester.assertIn(StardewItem("Victory", ItemClassification.progression, None, 1), multiworld.get_items())
    assert_can_win(tester, multiworld)
    non_event_locations = [location for location in multiworld.get_locations() if not location.event]
    tester.assertEqual(len(multiworld.itempool), len(non_event_locations))


def get_option_choices(option) -> Dict[str, int]:
    if issubclass(option, SpecialRange):
        return option.special_range_names
    elif option.options:
        return option.options
    return {}


class TestGenerateDynamicOptions(SVTestBase):
    def test_given_option_pair_when_generate_then_basic_checks(self):
        if self.skip_long_tests:
            return
        options_to_exclude = ["starting_money", "multiple_day_sleep_enabled", "multiple_day_sleep_cost",
                              "experience_multiplier", "friendship_multiplier", "debris_multiplier",
                              "quick_start", "gifting", "gift_tax"]
        options_to_include = [option_to_include for option_to_include in stardew_valley_option_classes
                              if option_to_include.internal_name not in options_to_exclude]
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