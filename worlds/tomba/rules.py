from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import Has

from .constants import Events
from .locations import Cleared, LocationHandler

if TYPE_CHECKING:
    from .world import TombaWorld


def set_all_rules(world: TombaWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(_: TombaWorld) -> None:
    pass


def set_all_location_rules(world: TombaWorld) -> None:
    for location in LocationHandler.location_table:
        if location.rule is not None:
            world.set_rule(world.get_location(location.name), location.rule)


def set_completion_condition(world: TombaWorld) -> None:
    world.set_completion_rule(Has(Cleared(Events.INSIDE_THE_KOKKA_EGGS)))
