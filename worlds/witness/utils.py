from functools import lru_cache
from math import floor
from typing import List, Collection
from pkgutil import get_data


def build_weighted_int_list(inputs: Collection[float], total: int) -> List[int]:
    """
    Converts a list of floats to a list of ints of a given length, using the Largest Remainder Method.
    """

    # Scale the inputs to sum to the desired total.
    scale_factor: float = total / sum(inputs)
    scaled_input = [x * scale_factor for x in inputs]

    # Generate whole number counts, always rounding down.
    rounded_output: List[int] = [floor(x) for x in scaled_input]
    rounded_sum = sum(rounded_output)

    # If the output's total is insufficient, increment the value that has the largest remainder until we meet our goal.
    remainders: List[float] = [real - rounded for real, rounded in zip(scaled_input, rounded_output)]
    while rounded_sum < total:
        max_remainder = max(remainders)
        if max_remainder == 0:
            break

        # Consume the remainder and increment the total for the given target.
        max_remainder_index = remainders.index(max_remainder)
        remainders[max_remainder_index] = 0
        rounded_output[max_remainder_index] += 1
        rounded_sum += 1

    return rounded_output


def define_new_region(region_string):
    """
    Returns a region object by parsing a line in the logic file
    """

    region_string = region_string[:-1]
    line_split = region_string.split(" - ")

    region_name_full = line_split.pop(0)

    region_name_split = region_name_full.split(" (")

    region_name = region_name_split[0]
    region_name_simple = region_name_split[1][:-1]

    options = set()

    for _ in range(len(line_split) // 2):
        connected_region = line_split.pop(0)
        corresponding_lambda = line_split.pop(0)

        options.add(
            (connected_region, parse_lambda(corresponding_lambda))
        )

    region_obj = {
        "name": region_name,
        "shortName": region_name_simple,
        "panels": list()
    }
    return region_obj, options


def parse_lambda(lambda_string):
    """
    Turns a lambda String literal like this: a | b & c
    into a set of sets like this: {{a}, {b, c}}
    The lambda has to be in DNF.
    """
    if lambda_string == "True":
        return frozenset([frozenset()])
    split_ands = set(lambda_string.split(" | "))
    lambda_set = frozenset({frozenset(a.split(" & ")) for a in split_ands})

    return lambda_set


class lazy(object):
    def __init__(self, func, name=None):
        self.func = func
        self.name = name if name is not None else func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, instance, class_):
        if instance is None:
            res = self.func(class_)
            setattr(class_, self.name, res)
            return res
        res = self.func(instance)
        setattr(instance, self.name, res)
        return res


@lru_cache(maxsize=None)
def get_adjustment_file(adjustment_file):
    data = get_data(__name__, adjustment_file).decode('utf-8')
    return [line.strip() for line in data.split("\n")]


def get_disable_unrandomized_list():
    return get_adjustment_file("settings/Disable_Unrandomized.txt")


def get_early_utm_list():
    return get_adjustment_file("settings/Early_UTM.txt")


def get_symbol_shuffle_list():
    return get_adjustment_file("settings/Symbol_Shuffle.txt")


def get_door_panel_shuffle_list():
    return get_adjustment_file("settings/Door_Panel_Shuffle.txt")


def get_doors_simple_list():
    return get_adjustment_file("settings/Doors_Simple.txt")


def get_doors_complex_list():
    return get_adjustment_file("settings/Doors_Complex.txt")


def get_doors_max_list():
    return get_adjustment_file("settings/Doors_Max.txt")


def get_laser_shuffle():
    return get_adjustment_file("settings/Laser_Shuffle.txt")


def get_audio_logs():
    return get_adjustment_file("settings/Audio_Logs.txt")


def get_ep_all_individual():
    return get_adjustment_file("settings/EP_Shuffle/EP_All.txt")


def get_ep_obelisks():
    return get_adjustment_file("settings/EP_Shuffle/EP_Sides.txt")


def get_ep_easy():
    return get_adjustment_file("settings/EP_Shuffle/EP_Easy.txt")


def get_ep_no_eclipse():
    return get_adjustment_file("settings/EP_Shuffle/EP_NoEclipse.txt")


def get_ep_no_caves():
    return get_adjustment_file("settings/EP_Shuffle/EP_NoCavesEPs.txt")


def get_ep_no_mountain():
    return get_adjustment_file("settings/EP_Shuffle/EP_NoMountainEPs.txt")


def get_ep_no_videos():
    return get_adjustment_file("settings/EP_Shuffle/EP_Videos.txt")


def get_sigma_normal_logic():
    return get_adjustment_file("WitnessLogic.txt")


def get_sigma_expert_logic():
    return get_adjustment_file("WitnessLogicExpert.txt")


def get_vanilla_logic():
    return get_adjustment_file("WitnessLogicVanilla.txt")


def get_items():
    return get_adjustment_file("WitnessItems.txt")
