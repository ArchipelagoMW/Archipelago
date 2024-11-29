# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import BumpStikLocation, level1_locs, level2_locs, level3_locs, level4_locs, level5_locs, location_table


def _generate_entrances(player: int, entrance_list: [str], parent: Region):
    return [Entrance(player, entrance, parent) for entrance in entrance_list]


def create_regions(multiworld: MultiWorld, player: int):
    region_map = {
        "Menu": level1_locs + ["Bonus Booster 1"] + [f"Treasure Bumper {i + 1}" for i in range(8)],
        "Level 1": level2_locs + ["Bonus Booster 2"] + [f"Treasure Bumper {i + 9}" for i in range(8)],
        "Level 2": level3_locs + ["Bonus Booster 3"] + [f"Treasure Bumper {i + 17}" for i in range(8)],
        "Level 3": level4_locs + [f"Bonus Booster {i + 4}" for i in range(2)] +
                   [f"Treasure Bumper {i + 25}" for i in range(8)],
        "Level 4": level5_locs
    }

    entrance_map = {
        "Level 1": lambda state:
        state.has("Booster Bumper", player, 1) and state.has("Treasure Bumper", player, 8),
        "Level 2": lambda state:
        state.has("Booster Bumper", player, 2) and state.has("Treasure Bumper", player, 16),
        "Level 3": lambda state:
        state.has("Booster Bumper", player, 3) and state.has("Treasure Bumper", player, 24),
        "Level 4": lambda state:
        state.has("Booster Bumper", player, 5) and state.has("Treasure Bumper", player, 32)
    }

    for x, region_name in enumerate(region_map):
        region_list = region_map[region_name]
        region = Region(region_name, player, multiworld)
        for location_name in region_list:
            region.locations += [BumpStikLocation(
                player, location_name, location_table[location_name], region)]
        if x < 4:
            region.exits += _generate_entrances(player,
                                                [f"To Level {x + 1}"], region)

        multiworld.regions += [region]

    for entrance in entrance_map:
        connection = multiworld.get_entrance(f"To {entrance}", player)
        connection.access_rule = entrance_map[entrance]
        connection.connect(multiworld.get_region(entrance, player))
