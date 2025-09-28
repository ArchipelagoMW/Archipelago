from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import *

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


class EventLocations(str, Enum):
    GANON_DEFEATED = "Ganon Defeated",


def set_region_rules(world: "SohWorld") -> None:
    player = world.player
    
    # TODO: Temporary to test generation
    connect_regions(Regions.KOKIRI_FOREST.value, world, [
        [Regions.GANONS_ARENA.value, lambda state: True]
    ])
    connect_regions(Regions.GANONS_ARENA.value, world, [
        [Regions.KOKIRI_FOREST.value, lambda state: True]
    ])
    add_events(Regions.GANONS_ARENA.value, world, [
        [EventLocations.GANON_DEFEATED.value, Events.GAME_COMPLETED.value, lambda state: 
         (can_use(Items.LIGHT_ARROW.value, state, world) and can_use(Items.MASTER_SWORD.value, state, world) and world.options.triforce_hunt == 0) or 
         has_item(Events.GAME_COMPLETED.value, state, world)]
    ])
