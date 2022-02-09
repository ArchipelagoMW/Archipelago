# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing
from ..generic.Rules import add_rule
from .Regions import meritous_regions, connect_regions


def check_endgame(state, player):
    for check in ["Meridian", "Ataraxia", "Merodach"]:
        if not state.can_reach(check, "Location", player):
            return False
    return True


def set_rules(world, player):
    connect_regions(world, player, "Menu",
                    "Chest rewards", lambda state: True)
    connect_regions(world, player, "Menu", "Meridian",
                    lambda state: state.has("PSI Key 1", player))
    connect_regions(world, player, "Menu", "Ataraxia",
                    lambda state: state.has("PSI Key 2", player))
    connect_regions(world, player, "Menu", "Merodach",
                    lambda state: state.has("PSI Key 3", player))
    connect_regions(world, player, "Menu", "Endgame",
                    lambda state: check_endgame(state, player))

    world.completion_condition[player] = lambda state: state.can_reach(
        "Endgame", "Region", player)
