from typing import Dict, List, TypeVar

# TODO probably move to Locations

environment_vanilla_orderedstage_1_table: Dict[str, int] = {
    "Distant Roost":                            7,  # blackbeach
    "Distant Roost (2)":                        8,  # blackbeach2
    "Titanic Plains":                          15,  # golemplains
    "Titanic Plains (2)":                      16,  # golemplains2
}
environment_vanilla_orderedstage_2_table: Dict[str, int] = {
    "Abandoned Aqueduct":                      17,  # goolake
    "Wetland Aspect":                          12,  # foggyswamp
}
environment_vanilla_orderedstage_3_table: Dict[str, int] = {
    "Rallypoint Delta":                        13,  # frozenwall
    "Scorched Acres":                          47,  # wispgraveyard
}
environment_vanilla_orderedstage_4_table: Dict[str, int] = {
    "Abyssal Depths":                          10,  # dampcavesimple
    "Siren's Call":                            37,  # shipgraveyard
    "Sundered Grove":                          35,  # rootjungle
}
environment_vanilla_orderedstage_5_table: Dict[str, int] = {
    "Sky Meadow":                              38,  # skymeadow
}

environment_vanilla_hidden_realm_table: Dict[str, int] = {
    "Hidden Realm: Bulwark's Ambry":            5,  # artifactworld
    "Hidden Realm: Bazaar Between Time":        6,  # bazaar
    "Hidden Realm: Gilded Coast":              14,  # goldshores
    "Hidden Realm: A Moment, Whole":           27,  # limbo
    "Hidden Realm: A Moment, Fractured":       33,  # mysteryspace
}

environment_vanilla_special_table: Dict[str, int] = {
    "Void Fields":                              4,  # arena
    "Commencement":                            32,  # moon2
}

environment_sotv_orderedstage_1_table: Dict[str, int] = {
    "Siphoned Forest":                         39,  # snowyforest
}
environment_sotv_orderedstage_2_table: Dict[str, int] = {
    "Aphelian Sanctuary":                       3,  # ancientloft
}
environment_sotv_orderedstage_3_table: Dict[str, int] = {
    "Sulfur Pools":                            41,  # sulfurpools
}

environment_sotv_special_table: Dict[str, int] = {
    "Void Locus":                              46,  # voidstage
    "The Planetarium":                         45,  # voidraid
}

X = TypeVar("X")
Y = TypeVar("Y")


def compress_dict_list_horizontal(list_of_dict: List[Dict[X, Y]]) -> Dict[X, Y]:
    """Combine all dictionaries in a list together into one dictionary."""
    compressed: Dict[X, Y] = {}
    for individual in list_of_dict:
        compressed.update(individual)
    return compressed


def collapse_dict_list_vertical(list_of_dict_1: List[Dict[X, Y]], *args: List[Dict[X, Y]]) -> List[Dict[X, Y]]:
    """Combine all parallel dictionaries in lists together to make a new list of dictionaries of the same length."""
    # find the length of the longest list
    length = len(list_of_dict_1)
    for list_of_dict_n in args:
        length = max(length, len(list_of_dict_n))

    # create a combined list with a length the same as the longest list
    collapsed: List[Dict[X, Y]] = [{}] * length
    # The reason the list_of_dict_1 is not directly used to make collapsed is
    #   side effects can occur if all the dictionaries are not manually unioned.

    # merge contents from list_of_dict_1
    for i in range(len(list_of_dict_1)):
        collapsed[i] = {**collapsed[i], **list_of_dict_1[i]}

    # merge contents of remaining lists_of_dicts
    for list_of_dict_n in args:
        for i in range(len(list_of_dict_n)):
            collapsed[i] = {**collapsed[i], **list_of_dict_n[i]}

    return collapsed


# TODO potentially these should only be created when they are directly referenced
#  (unsure of the space/time cost of creating these initially)

environment_vanilla_orderedstages_table = \
    [environment_vanilla_orderedstage_1_table, environment_vanilla_orderedstage_2_table,
     environment_vanilla_orderedstage_3_table, environment_vanilla_orderedstage_4_table,
     environment_vanilla_orderedstage_5_table]
environment_vanilla_table = \
    {**compress_dict_list_horizontal(environment_vanilla_orderedstages_table),
     **environment_vanilla_hidden_realm_table, **environment_vanilla_special_table}

environment_sotv_orderedstages_table = \
    [environment_sotv_orderedstage_1_table, environment_sotv_orderedstage_2_table,
     environment_sotv_orderedstage_3_table]
environment_sotv_table = \
    {**compress_dict_list_horizontal(environment_sotv_orderedstages_table), **environment_sotv_special_table}

environment_non_orderedstages_table = \
    {**environment_vanilla_hidden_realm_table, **environment_vanilla_special_table, **environment_sotv_special_table}
environment_orderedstages_table = \
    collapse_dict_list_vertical(environment_vanilla_orderedstages_table, environment_sotv_orderedstages_table)
environment_all_table = {**environment_vanilla_table, **environment_sotv_table}


def shift_by_offset(dictionary: Dict[str, int], offset: int) -> Dict[str, int]:
    """Shift all indexes in a dictionary by an offset"""
    return {name: index+offset for name, index in dictionary.items()}
