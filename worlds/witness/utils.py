import os
from Utils import cache_argsless
from itertools import accumulate
from typing import *
from fractions import Fraction


def best_junk_to_add_based_on_weights(weights: Dict[Any, Fraction], created_junk: Dict[Any, int]):
    min_error = ("", 2)

    for junk_name, instances in created_junk.items():
        new_dist = created_junk.copy()
        new_dist[junk_name] += 1
        new_dist_length = sum(new_dist.values())
        new_dist = {key: Fraction(value/1)/new_dist_length for key, value in new_dist.items()}

        errors = {key: abs(new_dist[key] - weights[key]) for key in created_junk.keys()}

        new_min_error = max(errors.values())

        if min_error[1] > new_min_error:
            min_error = (junk_name, new_min_error)

    return min_error[0]


def weighted_list(weights: Dict[Any, Fraction], length):
    """
    Example:
        weights = {A: 0.3, B: 0.3, C: 0.4}
        length = 10

        returns: [A, A, A, B, B, B, C, C, C, C]

    Makes sure to match length *exactly*, might approximate as a result
    """
    vals = accumulate(map(lambda x: x * length, weights.values()), lambda x, y: x + y)
    output_list = []
    for k, v in zip(weights.keys(), vals):
        while len(output_list) < v:
            output_list.append(k)
    return output_list


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
        "panels": set()
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


def get_adjustment_file(adjustment_file):
    path = os.path.join(os.path.dirname(__file__), adjustment_file)

    with open(path) as f:
        return [line.strip() for line in f.readlines()]


@cache_argsless
def get_disable_unrandomized_list():
    return get_adjustment_file("settings/Disable_Unrandomized.txt")


@cache_argsless
def get_early_utm_list():
    return get_adjustment_file("settings/Early_UTM.txt")


@cache_argsless
def get_symbol_shuffle_list():
    return get_adjustment_file("settings/Symbol_Shuffle.txt")


@cache_argsless
def get_door_panel_shuffle_list():
    return get_adjustment_file("settings/Door_Panel_Shuffle.txt")


@cache_argsless
def get_doors_simple_list():
    return get_adjustment_file("settings/Doors_Simple.txt")


@cache_argsless
def get_doors_complex_list():
    return get_adjustment_file("settings/Doors_Complex.txt")


@cache_argsless
def get_doors_max_list():
    return get_adjustment_file("settings/Doors_Max.txt")


@cache_argsless
def get_laser_shuffle():
    return get_adjustment_file("settings/Laser_Shuffle.txt")


@cache_argsless
def get_audio_logs():
    return get_adjustment_file("settings/Audio_Logs.txt")


@cache_argsless
def get_ep_all_individual():
    return get_adjustment_file("settings/EP_Shuffle/EP_All.txt")


@cache_argsless
def get_ep_obelisks():
    return get_adjustment_file("settings/EP_Shuffle/EP_Sides.txt")


@cache_argsless
def get_ep_easy():
    return get_adjustment_file("settings/EP_Shuffle/EP_Easy.txt")


@cache_argsless
def get_ep_no_eclipse():
    return get_adjustment_file("settings/EP_Shuffle/EP_NoEclipse.txt")


@cache_argsless
def get_ep_no_caves():
    return get_adjustment_file("settings/EP_Shuffle/EP_NoCavesEPs.txt")


@cache_argsless
def get_ep_no_mountain():
    return get_adjustment_file("settings/EP_Shuffle/EP_NoMountainEPs.txt")


@cache_argsless
def get_ep_no_videos():
    return get_adjustment_file("settings/EP_Shuffle/EP_Videos.txt")