from random import random
from typing import Dict

from Options import NamedRange
from .option_names import options_to_include
from ..checks.world_checks import basic_checks
from .. import setup_solo_multiworld, SVTestCase, SVTestBase
from ... import Goal
from ...options import EntranceRandomization, SpecialOrderLocations, Monstersanity


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
                        seed = int(random() * pow(10, 18) - 1)
                        # seed = 738592514038774912
                        with self.subTest(f"{option1.internal_name}: {key1}, {option2.internal_name}: {key2} [SEED: {seed}]"):
                            choices = {option1.internal_name: option1_choices[key1],
                                       option2.internal_name: option2_choices[key2]}
                            multiworld = setup_solo_multiworld(choices, seed)
                            basic_checks(self, multiworld)


class TestDynamicOptionDebug(SVTestCase):

    def test_option_pair_debug(self):
        options = {
            SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi,
            Monstersanity.internal_name: Monstersanity.option_one_per_monster,
        }
        for i in range(1):
            # seed = int(random() * pow(10, 18) - 1)
            seed = 823942126251776128
            with self.subTest(f"Seed: {seed}"):
                print(f"Seed: {seed}")
                multiworld = setup_solo_multiworld(options, seed)
                basic_checks(self, multiworld)
