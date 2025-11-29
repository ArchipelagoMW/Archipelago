import random

from Options import NamedRange, Option, Range
from ... import StardewValleyWorld
from ...options import StardewValleyOption

options_to_exclude = {"profit_margin", "starting_money", "multiple_day_sleep_enabled", "multiple_day_sleep_cost",
                      "experience_multiplier", "friendship_multiplier", "debris_multiplier",
                      "quick_start", "gifting", "gift_tax",
                      "progression_balancing", "accessibility", "start_inventory", "start_hints", "death_link"}

options_to_include: list[type[StardewValleyOption | Option]] = [
    option
    for option_name, option in StardewValleyWorld.options_dataclass.type_hints.items()
    if option_name not in options_to_exclude
]


def get_option_choices(option: type[Option]) -> dict[str, int]:
    if issubclass(option, NamedRange):
        return option.special_range_names
    if issubclass(option, Range):
        return {f"{val}": val for val in range(option.range_start, option.range_end + 1)}
    elif option.options:
        return option.options
    return {}


def generate_random_world_options(seed: int) -> dict[str, int]:
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


all_option_choices = [
    (option.internal_name, value)
    for option in options_to_include
    if option.options
    for value in get_option_choices(option)
    if option.default != get_option_choices(option)[value]
]

assert all_option_choices
