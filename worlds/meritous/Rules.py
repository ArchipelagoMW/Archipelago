# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing

from ..generic.Rules import forbid_item, exclusion_rules


def set_rules(world, player):
    # Prevent PSI keys from showing up in respective boss' room
    # Should be prevented by region generation but let's be sure
    forbid_item(world.get_location("Meridian", player), "PSI Key 1", player)
    forbid_item(world.get_location("Ataraxia", player), "PSI Key 2", player)
    forbid_item(world.get_location("Merodach", player), "PSI Key 3", player)

    # Prevent progression from showing up in last six checks per store
    # This is to prevent softlock from high prices or low chest drop
    default_exclude_locations = set()
    for store in ["Alpha Store", "Beta Store", "Gamma Store", "Reward Chest"]:
        for check_number in range(19, 25):
            default_exclude_locations.add(f"{store} {check_number}")
    exclusion_rules(world, player, default_exclude_locations)
