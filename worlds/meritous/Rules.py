# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from ..generic.Rules import forbid_item, exclusion_rules


def set_rules(world, player):
    # Prevent PSI keys from showing up in any boss' room
    # This is to prevent softlock from ending up having to fight a boss in the wrong boss room
    for boss in ["Meridian", "Ataraxia", "Merodach"]:
        for key in range(1, 4):
            forbid_item(world.get_location(boss, player), f"PSI Key {key}", player)

    # Prevent progression from showing up in last six checks per store
    # This is to prevent softlock from high prices or low chest drop
    default_exclude_locations = set()
    for store in ["Alpha Cache", "Beta Cache", "Gamma Cache", "Reward Chest"]:
        for check_number in range(19, 25):
            default_exclude_locations.add(f"{store} {check_number}")
    exclusion_rules(world, player, default_exclude_locations)
