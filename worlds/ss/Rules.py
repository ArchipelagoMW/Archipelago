from collections.abc import Callable
from typing import TYPE_CHECKING

from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import set_rule

from .Locations import LOCATION_TABLE
from .logic.Logic import ALL_REQUIREMENTS
from .logic.LogicParser import parse_expression

if TYPE_CHECKING:
    from . import SSWorld


class SSLogic(LogicMixin):
    """
    Handles special logic in Skyward Sword.

    Methods in this class are to be prefixed with "_ss"
    These can be called in requirements by cutting off the "_ss"
    EXAMPLE: _ss_sword_requirement_met(self, player)  ->  _sword_requirement_met
    Options can be called in requirements by using "_option_{}"
    EXAMPLE: _ss_option_no_triforce  ->  option_no_triforce
    For more examples, see /logic/requirements/Faron.py @ Sealed Grounds - Sealed Temple
    """

    multiworld: MultiWorld

    def _ss_sword_requirement_met(self, player: int) -> bool:
        return (
            (
                self.has("Progressive Sword", player, 2)
                and self.multiworld.worlds[player].options.got_sword_requirement
                == "goddess_sword"
            )
            or (
                self.has("Progressive Sword", player, 3)
                and self.multiworld.worlds[player].options.got_sword_requirement
                == "goddess_longsword"
            )
            or (
                self.has("Progressive Sword", player, 4)
                and self.multiworld.worlds[player].options.got_sword_requirement
                == "goddess_white_sword"
            )
            or (
                self.has("Progressive Sword", player, 5)
                and self.multiworld.worlds[player].options.got_sword_requirement
                == "master_sword"
            )
            or (
                self.has("Progressive Sword", player, 6)
                and self.multiworld.worlds[player].options.got_sword_requirement
                == "true_master_sword"
            )
        )

    def _ss_can_beat_required_dungeons(self, player: int) -> bool:
        req_dungeon_checks = self.multiworld.worlds[
            player
        ].dungeons.required_dungeon_checks
        return all(self.can_reach_location(loc, player) for loc in req_dungeon_checks)
    
    def _ss_option_unrequired_dungeons(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.got_dungeon_requirement == "unrequired"

    def _ss_option_upgraded_skyward_strike(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.upgraded_skyward_strike

    def _ss_option_thunderhead_ballad(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.open_thunderhead == "ballad"

    def _ss_option_thunderhead_open(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.open_thunderhead == "open"

    def _ss_option_no_triforce(self, player: int) -> bool:
        return not self.multiworld.worlds[player].options.triforce_required

    def _ss_option_lake_floria_open(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.open_lake_floria == "open"

    def _ss_option_lake_floria_yerbal(self, player: int) -> bool:
        return (
            self.multiworld.worlds[player].options.open_lake_floria == "talk_to_yerbal"
        )

    def _ss_option_damage_multiplier_under_12(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.damage_multiplier < 12

    def _ss_option_lmf_open(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.open_lmf == "open"

    def _ss_option_lmf_main_node(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.open_lmf == "main_node"

    def _ss_option_shopsanity(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.shopsanity

    def _ss_option_gondo_upgrades(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.gondo_upgrades


def set_rules(world: "SSWorld") -> None:
    """
    Defines logic for locations.
    """

    for loc in world.multiworld.get_locations(world.player):
        check_name = " - ".join(loc.name.split(" - ")[1:])
        if loc.parent_region.name == "Batreaux's House":
            rule = world.batreaux_requirements[check_name]
        else:
            rule = ALL_REQUIREMENTS[loc.parent_region.name]["locations"][check_name]
            if loc.name not in LOCATION_TABLE.keys():
                raise Exception(f"Tried to set logic for unknown location: {loc.name}")
        if loc.name in world.progress_locations:
            set_rule(loc, eval(f"lambda state, player=world.player: {parse_expression(rule)}"))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
