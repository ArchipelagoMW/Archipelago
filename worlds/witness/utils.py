import os
from Utils import cache_argsless
from itertools import accumulate
from typing import *
from fractions import Fraction


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


@cache_argsless
def get_disable_unrandomized_list():
    adjustment_file = "Disable_Unrandomized.txt"
    path = os.path.join(os.path.dirname(__file__), adjustment_file)

    with open(path) as f:
        return [line.strip() for line in f.readlines()]
