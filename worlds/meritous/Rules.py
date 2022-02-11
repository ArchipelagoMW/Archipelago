# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing

from ..generic.Rules import forbid_item


def check_endgame(state, player):
    for check in ["Meridian", "Ataraxia", "Merodach"]:
        if not state.can_reach(check, "Location", player):
            return False
    return True


def set_rules(world, player):
    forbid_item(world.get_location("Meridian", player), "PSI Key 1", player)
    forbid_item(world.get_location("Ataraxia", player), "PSI Key 2", player)
    forbid_item(world.get_location("Merodach", player), "PSI Key 3", player)
