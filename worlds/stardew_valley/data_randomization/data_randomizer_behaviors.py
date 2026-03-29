from numbers import Number
from random import Random
from typing import Any, Hashable, Iterable

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
    if len(existing_values) < 2:
        return randomize(existing_values, random)
    if all(isinstance(val, Number) for val in existing_values.values()):
        return range_randomize_numeric(existing_values, random)
    if all(isinstance(val, Iterable) for val in existing_values.values()):
        return range_randomize_iterable(existing_values, random)


def range_randomize_numeric(existing_values: dict[Any, Number], random: Random) -> dict[Any, Any]:
    keys = sorted([key for key in existing_values.keys()])
    values = sorted({val for val in existing_values.values()})

    if len(values) < 2:
        return randomize(existing_values, random)

    # TODO: Handle floats because this shit doesn't work
    # max_decimals = max(len(str(val - (val // 1))) - 2 for val in values)
    round_digits = 1
    while any(val != round(val, round_digits) for val in values):
        round_digits += 1
    round_digits -= 1

    range_start = values[0]
    range_end = values[-1]

    new_values = dict()
    for i in range(len(keys)):
        # if max_decimals == 0:
        random_value = random.randrange(range_start, range_end)
        random_value = round(random_value, -round_digits)
        # else:
        #     random_value = random.random()
        #     random_value = round(random_value, max_decimals)
        new_values[keys[i]] = random_value

    return new_values


def range_randomize_iterable(existing_values: dict[Any, Iterable], random: Random) -> dict[Any, Any]:
    keys = sorted([key for key in existing_values.keys()])
    values = sorted({val for val in existing_values.values()})
    value_for_type = values[0]

    if len(values) < 2:
        return randomize(existing_values, random)

    value_sizes = [len(val) for val in values]
    smallest_value_size = min(value_sizes)
    biggest_value_size = max(value_sizes)

    possible_entries = sorted({entry for sublist in values for entry in sublist})

    if len(possible_entries) < 1:
        return randomize(existing_values, random)

    new_values = dict()
    for i in range(len(keys)):
        size_value = random.randrange(smallest_value_size, biggest_value_size+1)
        entries = random.sample(possible_entries, k=size_value)
        entries = sorted(entries)
        if isinstance(value_for_type, frozenset):
            new_value = frozenset(entries)
        elif isinstance(value_for_type, set):
            new_value = set(entries)
        elif isinstance(value_for_type, list):
            new_value = list(entries)
        elif isinstance(value_for_type, tuple):
            new_value = tuple(entries)
        else:
            new_value = tuple(entries)
        new_values[keys[i]] = new_value

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