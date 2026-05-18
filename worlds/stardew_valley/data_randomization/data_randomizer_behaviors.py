import math
from numbers import Number
from random import Random
from typing import Any, Iterable

from ..options.options import DataRandomizationBehavior


def shuffle_data(existing_values: dict[Any, Any], random: Random, *args, **kwargs) -> dict[Any, Any]:
    keys = sorted([key for key in existing_values.keys()])
    values = sorted([val for val in existing_values.values()])

    random.shuffle(values)

    new_values = dict()
    for i in range(len(keys)):
        new_values[keys[i]] = values[i]

    return new_values


def weight_randomize(existing_values: dict[Any, Any], random: Random, *args, **kwargs) -> dict[Any, Any]:
    keys = sorted([key for key in existing_values.keys()])
    values = sorted([val for val in existing_values.values()])

    new_values = dict()
    for i in range(len(keys)):
        new_values[keys[i]] = random.choice(values)

    return new_values


def normal_randomize(existing_values: dict[Any, Any], random: Random, *args, **kwargs) -> dict[Any, Any]:
    if len(existing_values) < 2 or all(isinstance(val, bool) for val in existing_values.values()):
        return randomize(existing_values, random)
    if any(not isinstance(val, Number) for val in existing_values.values()):
        return randomize(existing_values, random)

    keys = sorted([key for key in existing_values.keys()])
    values = sorted([val for val in existing_values.values()])

    min_value = min(values) if len(args) < 1 else args[0]
    max_value = max(values) if len(args) < 2 else args[1]

    all_integer = all(isinstance(val, int) for val in values)

    # Log data before doing the math so big outliers don't dominate as much
    log_data = [math.log(x) for x in values]

    mean = sum(log_data) / len(log_data)
    variance = sum((x - mean) ** 2 for x in log_data) / len(log_data)
    standard_deviation = variance ** 0.5

    new_values = dict()
    for i in range(len(keys)):
        normal_random_value = normal_sample(random, mean, standard_deviation)
        restored_value = math.exp(normal_random_value)
        if restored_value > max_value or restored_value < min_value:
            normal_random_value = normal_sample(random, mean, standard_deviation)
            restored_value = math.exp(normal_random_value)
        if all_integer:
            restored_value = round(restored_value)
        new_values[keys[i]] = restored_value

    return new_values


def normal_sample(random: Random, mean: float = 0.0, standard_deviation: float = 1.0) -> float:
    # Box-Muller transform
    u1 = random.random()
    u2 = random.random()

    z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return mean + z0 * standard_deviation


def randomize(existing_values: dict[Any, Any], random: Random, *args, **kwargs) -> dict[Any, Any]:
    keys = sorted([key for key in existing_values.keys()])
    values = sorted({val for val in existing_values.values()})

    new_values = dict()
    for i in range(len(keys)):
        new_values[keys[i]] = random.choice(values)

    return new_values


def range_randomize(existing_values: dict[Any, Any], random: Random, *args, **kwargs) -> dict[Any, Any]:
    if len(existing_values) < 2 or all(isinstance(val, bool) for val in existing_values.values()):
        return randomize(existing_values, random, *args, **kwargs)
    if all(isinstance(val, Number) for val in existing_values.values()):
        return range_randomize_numeric(existing_values, random, *args, **kwargs)
    if all(isinstance(val, Iterable) and
           not isinstance(val, str) and
           is_all_same_type(val)
           for val in existing_values.values()):
        return range_randomize_iterable(existing_values, random, *args, **kwargs)
    return randomize(existing_values, random, *args, **kwargs)


def is_all_same_type(iterable_val: Iterable) -> bool:
    as_list = list(iterable_val)
    if len(as_list) <= 1:
        return True
    correct_type = type(as_list[0])
    all_correct_type = all(isinstance(val, correct_type) for val in as_list)
    return all_correct_type


def range_randomize_numeric(existing_values: dict[Any, Number], random: Random, *args, **kwargs) -> dict[Any, Any]:
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

    range_start = values[0] if len(args) < 1 else args[0]
    range_end = values[-1] if len(args) < 2 else args[1]

    new_values = dict()
    for i in range(len(keys)):
        # if max_decimals == 0:
        random_value = random.randrange(range_start, range_end + 1)
        random_value = round(random_value, -round_digits)
        # else:
        #     random_value = random.random()
        #     random_value = round(random_value, max_decimals)
        new_values[keys[i]] = random_value

    return new_values


def range_randomize_iterable(existing_values: dict[Any, Iterable], random: Random, *args, **kwargs) -> dict[Any, Any]:
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
        size_value = random.randrange(smallest_value_size, biggest_value_size + 1)
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
    DataRandomizationBehavior.option_shuffled: shuffle_data,
    DataRandomizationBehavior.option_weighted_randomized: weight_randomize,
    DataRandomizationBehavior.option_normal_randomized: normal_randomize,
    DataRandomizationBehavior.option_randomized: randomize,
    DataRandomizationBehavior.option_range_randomized: range_randomize,
    # DataRandomizationBehavior.option_wild: randomize_wild,
}
