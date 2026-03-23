from datetime import date
from math import floor
from pkgutil import get_data
from random import Random
from typing import Collection, FrozenSet, Iterable, List, Optional, Set, Tuple, TypeVar

from .definition_classes import AreaDefinition, ConnectionDefinition, RegionDefinition, WitnessRule

T = TypeVar("T")


def cast_not_none(value: Optional[T]) -> T:
    assert value is not None
    return value


def weighted_sample(world_random: Random, population: List[T], weights: List[float], k: int) -> List[T]:
    positions = range(len(population))
    indices: List[int] = []
    while True:
        needed = k - len(indices)
        if not needed:
            break
        for i in world_random.choices(positions, weights, k=needed):
            if weights[i]:
                weights[i] = 0.0
                indices.append(i)
    return [population[i] for i in indices]


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


def define_new_region(region_string: str, area: AreaDefinition) -> Tuple[RegionDefinition, List[ConnectionDefinition]]:
    """
    Returns a region object by parsing a line in the logic file
    """

    region_string = region_string[:-1]
    line_split = region_string.split(" - ")

    region_name_full = line_split.pop(0)

    region_name_split = region_name_full.split(" (")

    region_name = region_name_split[0]
    region_name_simple = region_name_split[1][:-1]

    options = []

    for _ in range(len(line_split) // 2):
        connected_region = line_split.pop(0)
        traversal_rule_string = line_split.pop(0)

        options.append(ConnectionDefinition(connected_region, parse_witness_rule(traversal_rule_string)))

    region_obj = RegionDefinition(region_name, region_name_simple, area)

    return region_obj, options


def parse_witness_rule(rule_string: str) -> WitnessRule:
    """
    Turns a rule string literal like this: a | b & c
    into a set of sets (called "WitnessRule") like this: {{a}, {b, c}}
    The rule string has to be in DNF.
    """
    if rule_string == "True":
        return frozenset([frozenset()])
    split_ands = set(rule_string.split(" | "))
    return frozenset({frozenset(a.split(" & ")) for a in split_ands})


_adjustment_file_cache = {}


def get_adjustment_file(adjustment_file: str) -> List[str]:
    if adjustment_file not in _adjustment_file_cache:
        data = get_data(__name__, adjustment_file)
        if data is None:
            raise FileNotFoundError(f"Could not find {adjustment_file}")
        _adjustment_file_cache[adjustment_file] = [line.strip() for line in data.decode("utf-8").split("\n")]

    return _adjustment_file_cache[adjustment_file]


def get_disable_unrandomized_list() -> List[str]:
    return get_adjustment_file("settings/Exclusions/Disable_Unrandomized.txt")


def get_early_caves_list() -> List[str]:
    return get_adjustment_file("settings/Early_Caves.txt")


def get_early_caves_start_list() -> List[str]:
    return get_adjustment_file("settings/Early_Caves_Start.txt")


def get_symbol_shuffle_list() -> List[str]:
    return get_adjustment_file("settings/Symbol_Shuffle.txt")


def get_complex_doors() -> List[str]:
    return get_adjustment_file("settings/Door_Shuffle/Complex_Doors.txt")


def get_simple_doors() -> List[str]:
    return get_adjustment_file("settings/Door_Shuffle/Simple_Doors.txt")


def get_complex_door_panels() -> List[str]:
    return get_adjustment_file("settings/Door_Shuffle/Complex_Door_Panels.txt")


def get_complex_additional_panels() -> List[str]:
    return get_adjustment_file("settings/Door_Shuffle/Complex_Additional_Panels.txt")


def get_simple_panels() -> List[str]:
    return get_adjustment_file("settings/Door_Shuffle/Simple_Panels.txt")


def get_simple_additional_panels() -> List[str]:
    return get_adjustment_file("settings/Door_Shuffle/Simple_Additional_Panels.txt")


def get_boat() -> List[str]:
    return get_adjustment_file("settings/Door_Shuffle/Boat.txt")


def get_laser_shuffle() -> List[str]:
    return get_adjustment_file("settings/Laser_Shuffle.txt")


def get_audio_logs() -> List[str]:
    return get_adjustment_file("settings/Audio_Logs.txt")


def get_ep_all_individual() -> List[str]:
    return get_adjustment_file("settings/EP_Shuffle/EP_All.txt")


def get_ep_obelisks() -> List[str]:
    return get_adjustment_file("settings/EP_Shuffle/EP_Sides.txt")


def get_obelisk_keys() -> List[str]:
    return get_adjustment_file("settings/Door_Shuffle/Obelisk_Keys.txt")


def get_ep_easy() -> List[str]:
    return get_adjustment_file("settings/EP_Shuffle/EP_Easy.txt")


def get_ep_no_eclipse() -> List[str]:
    return get_adjustment_file("settings/EP_Shuffle/EP_NoEclipse.txt")


def get_vault_exclusion_list() -> List[str]:
    return get_adjustment_file("settings/Exclusions/Vaults.txt")


def get_discard_exclusion_list() -> List[str]:
    return get_adjustment_file("settings/Exclusions/Discards.txt")


def get_caves_except_path_to_challenge_exclusion_list() -> List[str]:
    return get_adjustment_file("settings/Exclusions/Caves_Except_Path_To_Challenge.txt")


def get_entity_hunt() -> List[str]:
    return get_adjustment_file("settings/Entity_Hunt.txt")


def get_sigma_normal_logic() -> List[str]:
    return get_adjustment_file("WitnessLogic.txt")


def get_sigma_expert_logic() -> List[str]:
    return get_adjustment_file("WitnessLogicExpert.txt")


def get_umbra_variety_logic() -> List[str]:
    return get_adjustment_file("WitnessLogicVariety.txt")


def get_vanilla_logic() -> List[str]:
    return get_adjustment_file("WitnessLogicVanilla.txt")


def get_items() -> List[str]:
    return get_adjustment_file("WitnessItems.txt")


def optimize_witness_rule(witness_rule: WitnessRule) -> WitnessRule:
    """Removes any redundant terms from a logical formula in disjunctive normal form.
    This means removing any terms that are a superset of any other term get removed.
    This is possible because of the boolean absorption law: a | (a & b) = a"""
    to_remove = set()

    for option1 in witness_rule:
        for option2 in witness_rule:
            if option2 < option1:
                to_remove.add(option1)

    return witness_rule - to_remove


def logical_and_witness_rules(witness_rules: Iterable[WitnessRule]) -> WitnessRule:
    """
    performs the "and" operator on a list of logical formula in disjunctive normal form, represented as a set of sets.
    A logical formula might look like this: {{a, b}, {c, d}}, which would mean "a & b | c & d".
    These can be easily and-ed by just using the boolean distributive law: (a | b) & c = a & c | a & b.
    """
    current_overall_requirement: FrozenSet[FrozenSet[str]] = frozenset({frozenset()})

    for next_dnf_requirement in witness_rules:
        new_requirement: Set[FrozenSet[str]] = set()

        for option1 in current_overall_requirement:
            for option2 in next_dnf_requirement:
                new_requirement.add(option1 | option2)

        current_overall_requirement = frozenset(new_requirement)

    return optimize_witness_rule(current_overall_requirement)


def logical_or_witness_rules(witness_rules: Iterable[WitnessRule]) -> WitnessRule:
    return optimize_witness_rule(frozenset.union(*witness_rules))


def is_easter_time() -> bool:
    # dateutils would have been nice here, because it has an easter() function.
    # But adding it as a requirement seems heavier than necessary.
    # Thus, we just take a range from the earliest to latest possible easter dates.

    today = date.today()

    if today < date(2025, 3, 31): # Don't go live early if 0.6.0 RC3 happens, with a little leeway
        return False

    earliest_easter_day = date(today.year, 3, 20)  # Earliest possible is 3/22 + 2 day buffer for Good Friday
    last_easter_day = date(today.year, 4, 26)  # Latest possible is 4/25 + 1 day buffer for Easter Monday

    return earliest_easter_day <= today <= last_easter_day
