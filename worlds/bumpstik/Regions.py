# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from BaseClasses import MultiWorld, Region, Entrance, RegionType
from .Locations import BumpStikLocation, location_table


def _generate_entrances(player: int, entrance_list: [str], parent: Region):
    return [Entrance(player, entrance, parent) for entrance in entrance_list]


def create_regions(world: MultiWorld, player: int):
    region_map = {
        "Menu": [
            "250 Points", "500 Points", "750 Points", "1000 Points", "Booster Bumper 1", "Booster Bumper 2",
            "Treasure Bumper 1", "Treasure Bumper 2"
            ],
        "Level 1": [
            "1250 Points", "1500 Points", "1750 Points", "2000 Points", "Combo Clear 4", "Chain x2",
            "Booster Bumper 3", "Treasure Bumper 3", "Treasure Bumper 4"
            ],
        "Level 2": [
            "2250 Points", "2500 Points", "2750 Points", "3000 Points", "Combo Clear 5", "All Clear",
            "Booster Bumper 4", "Treasure Bumper 5", "Treasure Bumper 6"
            ],
        "Level 3": [
            "3250 Points", "3500 Points", "3750 Points", "4000 Points", "Combo Clear 6", "Chain x3",
            "Booster Bumper 5", "Treasure Bumper 7", "Treasure Bumper 8"
            ],
        "Level 4": ["Cleared All Hazards"]
    }

    entrance_map = {
        "Level 1": lambda state:
            state.has_group("Board Size", player, 2) and state.has(
                "Booster Bumper", player, 1),
        "Level 2": lambda state:
            state.has_group("Board Size", player, 3) and state.has_group("Color", player, 1) and state.has(
                "Booster Bumper", player, 2),
        "Level 3": lambda state:
            state.has_group("Board Size", player, 4) and state.has_group("Color", player, 2) and state.has(
                "Booster Bumper", player, 3),
        "Level 4": lambda state:
            state.has_group("Board Size", player, 5) and state.has_group("Color", player, 3) and state.has(
                "Booster Bumper", player, 4)
    }

    for x, region_name in enumerate(region_map):
        region_list = region_map[region_name]
        region = Region(region_name, RegionType.Generic,
                        region_name, player, world)
        for location_name in region_list:
            region.locations += [BumpStikLocation(
                player, location_name, location_table[location_name], region)]
        if x < 4:
            region.exits += _generate_entrances(player,
                                                [f"To Level {x + 1}"], region)

        world.regions += [region]

    for entrance in entrance_map:
        connection = world.get_entrance(f"To {entrance}", player)
        connection.access_rule = entrance_map[entrance]
        connection.connect(world.get_region(entrance, player))
