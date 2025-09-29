from typing import TYPE_CHECKING

from ..Enums import *
from ..LogicHelpers import *

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


class EventLocations(str, Enum):
    ROOT_AMMO_DROP = "Root Ammo Drop"
    ROOT_TIME_TRAVEL = "Root Time Travel"
    TRIFORCE_HUNT_COMPLETION = "Triforce Hunt Completion"


def set_region_rules(world: "SohWorld") -> None:
    player = world.player

    ## Root
    # Events
    add_events(Regions.KOKIRI_FOREST, world, [
        [EventLocations.ROOT_AMMO_DROP, Events.AMMO_CAN_DROP, lambda state: True], # Not sure why but ship has this set to true immediately, so this mirrors that.
        [EventLocations.ROOT_TIME_TRAVEL, Events.TIME_TRAVEL, lambda state: has_item(Events.CLEARED_DEKU_TREE, state, world)], # temp
        [EventLocations.TRIFORCE_HUNT_COMPLETION, Events.GAME_COMPLETED,  lambda state:
         (world.options.triforce_hunt == 1 and 
         has_item(Items.TRIFORCE_PIECE, state, world, world.options.triforce_hunt_required_pieces.value)) or 
         has_item(Events.GAME_COMPLETED, state, world)]
    ])

    connect_regions(Regions.TEMPLE_OF_TIME, world, [
        [Regions.KOKIRI_FOREST, lambda state: True]
    ])

    # Locations
    add_locations(Regions.ROOT, world, [
        [Locations.LINKS_POCKET, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.ROOT, world, [
        [Regions.ROOT_EXITS, lambda state: is_child(state, world, Regions.ROOT) or has_item(Events.TIME_TRAVEL, state, world)]
    ])
    
    ## Root Exits
    # Connections
    connect_regions(Regions.ROOT_EXITS, world, [
        [Regions.CHILD_SPAWN, lambda state: is_child(state, world, Regions.ROOT_EXITS)], # TODO: Implement starting age
        [Regions.ADULT_SPAWN, lambda state: is_adult(state, world, Regions.ROOT_EXITS)], # TODO: Implement starting age
        [Regions.MINUET_OF_FOREST_WARP, lambda state: True],
        [Regions.BOLERO_OF_FIRE_WARP, lambda state: True],
        [Regions.SERENADE_OF_WATER_WARP, lambda state: True],
        [Regions.NOCTURNE_OF_SHADOW_WARP, lambda state: True],
        [Regions.REQUIEM_OF_SPIRIT_WARP, lambda state: True],
        [Regions.PRELUDE_OF_LIGHT_WARP, lambda state: True],
    ])

    ## Child Spawn
    # Connections
    connect_regions(Regions.CHILD_SPAWN, world, [
        [Regions.KF_LINKS_HOUSE, lambda state: True]
    ])

    ## Adult Spawn
    # Connections
    connect_regions(Regions.ADULT_SPAWN, world, [
        [Regions.TEMPLE_OF_TIME, lambda state: True]
    ])

    ## Minuet of Forest Warp
    # Connections
    connect_regions(Regions.MINUET_OF_FOREST_WARP, world, [
        [Regions.SACRED_FOREST_MEADOW, lambda state: can_use(Items.MINUET_OF_FOREST, state, world)]
    ])

    ## Bolero of Fire Warp
    # Connections
    connect_regions(Regions.BOLERO_OF_FIRE_WARP, world, [
        [Regions.DMC_CENTRAL_LOCAL, lambda state: can_use(Items.BOLERO_OF_FIRE, state, world)]
    ])

    ## Serenade of Water Warp
    # Connections
    connect_regions(Regions.SERENADE_OF_WATER_WARP, world, [
        [Regions.LAKE_HYLIA, lambda state: can_use(Items.SERENADE_OF_WATER, state, world)]
    ])

    ## Requiem of Spirit Warp
    # Connections
    connect_regions(Regions.REQUIEM_OF_SPIRIT_WARP, world, [
        [Regions.DESERT_COLOSSUS, lambda state: can_use(Items.REQUIEM_OF_SPIRIT, state, world)]
    ])

    ## Nocturne of Shadow Warp
    # Connections
    connect_regions(Regions.NOCTURNE_OF_SHADOW_WARP, world, [
        [Regions.GRAVEYARD_WARP_PAD_REGION, lambda state: can_use(Items.NOCTURNE_OF_SHADOW, state, world)]
    ])
    
    ## Prelude of Light Warp
    # Connections
    connect_regions(Regions.PRELUDE_OF_LIGHT_WARP, world, [
        [Regions.TEMPLE_OF_TIME, lambda state: can_use(Items.PRELUDE_OF_LIGHT, state, world)]
    ])
