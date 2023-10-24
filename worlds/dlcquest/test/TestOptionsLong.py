from typing import Dict

from BaseClasses import MultiWorld
from Options import SpecialRange
from .option_names import options_to_include
from .checks.world_checks import assert_can_win, assert_same_number_items_locations
from . import DLCQuestTestBase, setup_dlc_quest_solo_multiworld
from ... import AutoWorldRegister


def basic_checks(tester: DLCQuestTestBase, multiworld: MultiWorld):
    assert_can_win(tester, multiworld)
    assert_same_number_items_locations(tester, multiworld)


def get_option_choices(option) -> Dict[str, int]:
    if issubclass(option, SpecialRange):
        return option.special_range_names
    elif option.options:
        return option.options
    return {}


class TestGenerateDynamicOptions(DLCQuestTestBase):
    def test_given_option_pair_when_generate_then_basic_checks(self):
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
                            multiworld = setup_dlc_quest_solo_multiworld(choices)
                            basic_checks(self, multiworld)

    def test_given_option_truple_when_generate_then_basic_checks(self):
        num_options = len(options_to_include)
        for option1_index in range(0, num_options):
            for option2_index in range(option1_index + 1, num_options):
                for option3_index in range(option2_index + 1, num_options):
                    option1 = options_to_include[option1_index]
                    option2 = options_to_include[option2_index]
                    option3 = options_to_include[option3_index]
                    option1_choices = get_option_choices(option1)
                    option2_choices = get_option_choices(option2)
                    option3_choices = get_option_choices(option3)
                    for key1 in option1_choices:
                        for key2 in option2_choices:
                            for key3 in option3_choices:
                                with self.subTest(f"{option1.internal_name}: {key1}, {option2.internal_name}: {key2}, {option3.internal_name}: {key3}"):
                                    choices = {option1.internal_name: option1_choices[key1],
                                               option2.internal_name: option2_choices[key2],
                                               option3.internal_name: option3_choices[key3]}
                                    multiworld = setup_dlc_quest_solo_multiworld(choices)
                                    basic_checks(self, multiworld)

    def test_given_option_quartet_when_generate_then_basic_checks(self):
        num_options = len(options_to_include)
        for option1_index in range(0, num_options):
            for option2_index in range(option1_index + 1, num_options):
                for option3_index in range(option2_index + 1, num_options):
                    for option4_index in range(option3_index + 1, num_options):
                        option1 = options_to_include[option1_index]
                        option2 = options_to_include[option2_index]
                        option3 = options_to_include[option3_index]
                        option4 = options_to_include[option4_index]
                        option1_choices = get_option_choices(option1)
                        option2_choices = get_option_choices(option2)
                        option3_choices = get_option_choices(option3)
                        option4_choices = get_option_choices(option4)
                        for key1 in option1_choices:
                            for key2 in option2_choices:
                                for key3 in option3_choices:
                                    for key4 in option4_choices:
                                        with self.subTest(
                                                f"{option1.internal_name}: {key1}, {option2.internal_name}: {key2}, {option3.internal_name}: {key3}, {option4.internal_name}: {key4}"):
                                            choices = {option1.internal_name: option1_choices[key1],
                                                       option2.internal_name: option2_choices[key2],
                                                       option3.internal_name: option3_choices[key3],
                                                       option4.internal_name: option4_choices[key4]}
                                            multiworld = setup_dlc_quest_solo_multiworld(choices)
                                            basic_checks(self, multiworld)
