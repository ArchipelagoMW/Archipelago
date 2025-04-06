import random
import unittest
from typing import Dict

from BaseClasses import MultiWorld, get_seed
from Options import NamedRange, Range
from .option_names import options_to_include
from .. import SVTestCase
from ..assertion import GoalAssertMixin, OptionAssertMixin, WorldAssertMixin


def get_option_choices(option) -> Dict[str, int]:
    if issubclass(option, NamedRange):
        return option.special_range_names
    if issubclass(option, Range):
        return {f"{val}": val for val in range(option.range_start, option.range_end + 1)}
    elif option.options:
        return option.options
    return {}


def generate_random_world_options(seed: int) -> Dict[str, int]:
    num_options = len(options_to_include)
    world_options = dict()
    rng = random.Random(seed)
    for option_index in range(0, num_options):
        option = options_to_include[option_index]
        option_choices = get_option_choices(option)
        if not option_choices:
            continue
        chosen_option_value = rng.choice(list(option_choices.values()))
        world_options[option.internal_name] = chosen_option_value
    return world_options


def get_number_log_steps(number_worlds: int) -> int:
    if number_worlds <= 10:
        return 2
    if number_worlds <= 100:
        return 5
    if number_worlds <= 500:
        return 10
    if number_worlds <= 1000:
        return 20
    if number_worlds <= 5000:
        return 25
    if number_worlds <= 10000:
        return 50
    return 100


class TestGenerateManyWorlds(GoalAssertMixin, OptionAssertMixin, WorldAssertMixin, SVTestCase):
    def test_generate_many_worlds_then_check_results(self):
        if self.skip_long_tests:
            raise unittest.SkipTest("Long tests disabled")

        number_worlds = 10 if self.skip_long_tests else 1000
        seed = get_seed()
        self.generate_and_check_many_worlds(number_worlds, seed)

    def generate_and_check_many_worlds(self, number_worlds: int, seed: int):
        num_steps = get_number_log_steps(number_worlds)
        log_step = number_worlds / num_steps

        print(f"Generating {number_worlds} Solo Multiworlds [Start Seed: {seed}] for Stardew Valley...")
        for world_number in range(0, number_worlds + 1):

            world_seed = world_number + seed
            world_options = generate_random_world_options(world_seed)

            with self.solo_world_sub_test(f"Multiworld: {world_seed}", world_options, seed=world_seed, world_caching=False) as (multiworld, _):
                self.assert_multiworld_is_valid(multiworld)

            if world_number > 0 and world_number % log_step == 0:
                print(f"Generated and Verified {world_number}/{number_worlds} worlds [{(world_number * 100) // number_worlds}%]")

        print(f"Finished generating and verifying {number_worlds} Solo Multiworlds for Stardew Valley")

    def assert_multiworld_is_valid(self, multiworld: MultiWorld):
        self.assert_victory_exists(multiworld)
        self.assert_same_number_items_locations(multiworld)
        self.assert_goal_world_is_valid(multiworld)
        self.assert_can_reach_island_if_should(multiworld)
        self.assert_cropsanity_same_number_items_and_locations(multiworld)
        self.assert_festivals_give_access_to_deluxe_scarecrow(multiworld)
        self.assert_has_festival_recipes(multiworld)
