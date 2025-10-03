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
    connect_regions(Regions.KOKIRI_FOREST, world, [
        (Regions.GANONS_ARENA, lambda bundle: True)
    ])
    connect_regions(Regions.GANONS_ARENA, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True)
    ])
    add_events(Regions.GANONS_ARENA, world, [
        (EventLocations.GANON_DEFEATED, Events.GAME_COMPLETED, lambda bundle: 
         (can_use(Items.LIGHT_ARROW, bundle) and can_use(Items.MASTER_SWORD, bundle) and world.options.triforce_hunt == 0) or 
         has_item(Events.GAME_COMPLETED, bundle))
    ])
