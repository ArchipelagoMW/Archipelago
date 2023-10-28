from typing import Dict
import random

from BaseClasses import MultiWorld
from Options import SpecialRange, Range
from .option_names import options_to_include
from .. import setup_solo_multiworld, SVTestCase
from ..checks.goal_checks import assert_perfection_world_is_valid, assert_goal_world_is_valid
from ..checks.option_checks import assert_can_reach_island_if_should, assert_cropsanity_same_number_items_and_locations, \
    assert_festivals_give_access_to_deluxe_scarecrow
from ..checks.world_checks import assert_same_number_items_locations, assert_victory_exists


def get_option_choices(option) -> Dict[str, int]:
    if issubclass(option, SpecialRange):
        return option.special_range_names
    if issubclass(option, Range):
        return {f"{val}": val for val in range(option.range_start, option.range_end + 1)}
    elif option.options:
        return option.options
    return {}


def generate_random_multiworld(world_id: int):
    world_options = generate_random_world_options(world_id)
    multiworld = setup_solo_multiworld(world_options, seed=world_id)
    return multiworld


def generate_random_world_options(world_id: int) -> Dict[str, int]:
    num_options = len(options_to_include)
    world_options = dict()
    rng = random.Random(world_id)
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


def generate_many_worlds(number_worlds: int, start_index: int) -> Dict[int, MultiWorld]:
    num_steps = get_number_log_steps(number_worlds)
    log_step = number_worlds / num_steps
    multiworlds = dict()
    print(f"Generating {number_worlds} Solo Multiworlds [Start Seed: {start_index}] for Stardew Valley...")
    for world_number in range(0, number_worlds + 1):
        world_id = world_number + start_index
        multiworld = generate_random_multiworld(world_id)
        multiworlds[world_id] = multiworld
        if world_number > 0 and world_number % log_step == 0:
            print(f"Generated {world_number}/{number_worlds} worlds [{(world_number * 100) // number_worlds}%]")
    print(f"Finished generating {number_worlds} Solo Multiworlds for Stardew Valley")
    return multiworlds


def check_every_multiworld_is_valid(tester: SVTestCase, multiworlds: Dict[int, MultiWorld]):
    for multiworld_id in multiworlds:
        multiworld = multiworlds[multiworld_id]
        with tester.subTest(f"Checking validity of world {multiworld_id}"):
            check_multiworld_is_valid(tester, multiworld_id, multiworld)


def check_multiworld_is_valid(tester: SVTestCase, multiworld_id: int, multiworld: MultiWorld):
    assert_victory_exists(tester, multiworld)
    assert_same_number_items_locations(tester, multiworld)
    assert_goal_world_is_valid(tester, multiworld)
    assert_can_reach_island_if_should(tester, multiworld)
    assert_cropsanity_same_number_items_and_locations(tester, multiworld)
    assert_festivals_give_access_to_deluxe_scarecrow(tester, multiworld)


class TestGenerateManyWorlds(SVTestCase):
    def test_generate_many_worlds_then_check_results(self):
        if self.skip_long_tests:
            return
        number_worlds = 1000
        start_index = random.Random().randint(0, 9999999999)
        multiworlds = generate_many_worlds(number_worlds, start_index)
        check_every_multiworld_is_valid(self, multiworlds)
