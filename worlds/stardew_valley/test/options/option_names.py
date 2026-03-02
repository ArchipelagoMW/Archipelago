import random
from typing import Iterable

from Options import NamedRange, Option, Range
from ... import StardewValleyWorld
from ...options import StardewValleyOption

options_to_exclude = {"profit_margin", "starting_money",
                      "multiple_day_sleep_enabled", "multiple_day_sleep_cost",
                      "experience_multiplier", "friendship_multiplier", "debris_multiplier",
                      "quick_start", "gifting",
                      "movement_buff_number", "enabled_filler_buffs", "trap_difficulty", "trap_distribution",
                      "bundle_plando", "trap_items",
                      "progression_balancing", "accessibility",
                      "start_inventory", "local_items", "non_local_items", "exclude_locations", "priority_locations",
                      "start_hints", "start_location_hints", "item_links", "plando_items",
                      "death_link",
                      "jojapocalypse", "joja_start_price", "joja_end_price", "joja_pricing_pattern", "joja_purchases_for_membership", "joja_are_you_sure"}

for option in options_to_exclude:
    assert option in StardewValleyWorld.options_dataclass.type_hints.keys(), f"Excluding an option that doesn't exist: {option}"

options_to_include: list[type[StardewValleyOption | Option]] = [
    option
    for option_name, option in StardewValleyWorld.options_dataclass.type_hints.items()
    if option_name not in options_to_exclude
]


def get_option_choices(option: type[Option]) -> dict[str, int]:
    if issubclass(option, NamedRange):
        return option.special_range_names
    if issubclass(option, Range):
        range_size = option.range_end - option.range_start
        max_steps = 10
        step = max(1, range_size // max_steps)
        return {f"{val}": val for val in range(option.range_start, option.range_end + 1, step)}
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


all_option_choices = []
for option in options_to_include:
    if option.options:
        option_choices = get_option_choices(option)
        for choice_name, choice_value in option_choices.items():
            if option.default != choice_value:
                all_option_choices.append((option.internal_name, choice_name))

assert all_option_choices


def get_all_option_choices(extra_ignored: Iterable[str] = None):
    if extra_ignored is None:
        return all_option_choices
    return [option_choice for option_choice in all_option_choices if option_choice[0] not in extra_ignored]
