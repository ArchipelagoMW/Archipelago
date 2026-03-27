from numbers import Number
from random import Random
from typing import Any, Hashable

from ..options.options import DataRandomizationBehavior


def shuffle_data(existing_values: dict[Any, Any], random: Random) -> dict[Any, Any]:
    keys = sorted([key for key in existing_values.keys()])
    values = sorted([val for val in existing_values.values()])

    random.shuffle(values)

    new_values = dict()
    for i in range(len(keys)):
        new_values[keys[i]] = values[i]

    return new_values


def weight_randomize(existing_values: dict[Any, Any], random: Random) -> dict[Any, Any]:
    keys = sorted([key for key in existing_values.keys()])
    values = sorted([val for val in existing_values.values()])

    new_values = dict()
    for i in range(len(keys)):
        new_values[keys[i]] = random.choice(values)

    return new_values


def randomize(existing_values: dict[Any, Any], random: Random) -> dict[Any, Any]:
    if any(not isinstance(val, Hashable) for val in existing_values.values()):
        return randomize(existing_values, random)

    keys = sorted([key for key in existing_values.keys()])
    values = sorted({val for val in existing_values.values()})

    new_values = dict()
    for i in range(len(keys)):
        new_values[keys[i]] = random.choice(values)

    return new_values


def range_randomize(existing_values: dict[Any, Any], random: Random) -> dict[Any, Any]:
    if any(not isinstance(val, Number) for val in existing_values.values()):
        return randomize(existing_values, random)

    keys = sorted([key for key in existing_values.keys()])
    values = sorted({val for val in existing_values.values()})

    if len(values) < 2:
        return randomize(existing_values, random)

    max_decimals = max(len(str(val - (val % 1))) - 2 for val in values)
    round_digits = 1
    while any(val != round(val, round_digits) for val in values):
        round_digits += 1
    round_digits -= 1

    range_start = values[0]
    range_end = values[-1]

    new_values = dict()
    for i in range(len(keys)):
        if max_decimals == 0:
            random_value = random.randrange(range_start, range_end)
            random_value = round(random_value, -round_digits)
        else:
            random_value = random.random()
            random_value = round(random_value, max_decimals)
        new_values[keys[i]] = random_value

    return new_values


def randomize_wild(existing_values: dict[Any, Any], random: Random) -> dict[Any, Any]:
    raise "Randomize Wild is not implemented yet"


randomizers_per_behavior = {
    DataRandomizationBehavior.option_off: None,
    DataRandomizationBehavior.option_shuffle: shuffle_data,
    DataRandomizationBehavior.option_weighted_randomized: weight_randomize,
    DataRandomizationBehavior.option_randomized: randomize,
    DataRandomizationBehavior.option_range_randomized: range_randomize,
    DataRandomizationBehavior.option_wild: randomize_wild,
}