# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing

from ..generic.Rules import add_rule, forbid_item

from .Regions import meritous_regions, connect_regions


def check_endgame(state, player):
    for check in ["Meridian", "Ataraxia", "Merodach"]:
        if not state.can_reach(check, "Location", player):
            return False
    return True


def set_rules(world, player):
    connect_regions(world, player, "Menu", "Meridian",
                    lambda state: state.has("PSI Key 1", player))
    connect_regions(world, player, "Menu", "Ataraxia",
                    lambda state: state.has("PSI Key 2", player))
    connect_regions(world, player, "Menu", "Merodach",
                    lambda state: state.has("PSI Key 3", player))
    connect_regions(world, player, "Menu", "Endgame",
                    lambda state: check_endgame(state, player))

    connect_regions(world, player, "Endgame", "Final Boss",
                    lambda state: state.has("Cursed Seal", player))
    connect_regions(world, player, "Endgame", "True Final Boss",
                    lambda state: state.has("Agate Knife", player) and state.has("Cursed Seal", player))

    forbid_item(world.get_location("Meridian", player), "PSI Key 1", player)
    forbid_item(world.get_location("Ataraxia", player), "PSI Key 2", player)
    forbid_item(world.get_location("Merodach", player), "PSI Key 3", player)
