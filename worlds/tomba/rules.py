from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

from . import constants

if TYPE_CHECKING:
    from .world import TombaWorld

HAS_KEY = Has("Key")  # Hmm, what could this be? A little foreshadowing perhaps? :) You'll find out if you keep reading!


def set_all_rules(world: TombaWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: TombaWorld) -> None:
    pass

def set_all_location_rules(world: TombaWorld) -> None:
    can_dissipate_fog: Rule = Has(constants.FURIOUS_TORNADO)

    fog = world.get_location(constants.VILLAGE_OF_ALL_BEGINNINGS_FOG)
    world.set_rule(fog, can_dissipate_fog)


def set_completion_condition(world: TombaWorld) -> None:
    world.set_completion_rule(Has(constants.VICTORY))