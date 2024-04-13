from __future__ import annotations
from typing import TYPE_CHECKING

from .Names import LocationName, EventName

if TYPE_CHECKING:
    from . import YTGVWorld

def set_rules(world: YTGVWorld):
    multiworld = world.multiworld

    location_musk = multiworld.get_location(LocationName.MUSK, world.player)
    location_granny = multiworld.get_location(LocationName.GRANNY, world.player)

    event_to_the_moon = world.create_event(EventName.TO_THE_MOON)
    event_she_is_fine_now = world.create_event(EventName.SHE_IS_FINE_NOW)

    # Locked items
    location_musk.place_locked_item(event_to_the_moon)
    location_granny.place_locked_item(event_she_is_fine_now)


    # Completion condition
    world.multiworld.completion_condition[world.player] = lambda state: state.has(event_she_is_fine_now.name, world.player)