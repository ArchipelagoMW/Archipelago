from typing import TYPE_CHECKING

from ..Enums import *
from ..LogicHelpers import *

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


class EventLocations(str, Enum):
    ROOT_AMMO_DROP = "Root Ammo Drop"
    ROOT_TIME_TRAVEL = "Root Time Travel"
    ROOT_SHIELD = "Root Shield"
    TRIFORCE_HUNT_COMPLETION = "Triforce Hunt Completion"


def set_region_rules(world: "SohWorld") -> None:
    player = world.player

    ## Root
    # Events
    add_events(Regions.KOKIRI_FOREST, world, [
        (EventLocations.ROOT_AMMO_DROP, Events.AMMO_CAN_DROP, lambda s, r, w: True), # Not sure why but ship has this set to true immediately, so this mirrors that.
        (EventLocations.ROOT_TIME_TRAVEL, Events.TIME_TRAVEL, lambda s, r, w: has_item(Events.CLEARED_DEKU_TREE, s, w)), # temp
        (EventLocations.ROOT_SHIELD, Events.CAN_BUY_DEKU_SHIELD, lambda s, r, w: True), # Temp
        (EventLocations.TRIFORCE_HUNT_COMPLETION, Events.GAME_COMPLETED,  lambda s, r, w:
         (world.options.triforce_hunt == 1 and 
         has_item(Items.TRIFORCE_PIECE, s, w, w.options.triforce_hunt_required_pieces.value)) or 
         has_item(Events.GAME_COMPLETED, s, w))
    ])

    connect_regions(Regions.TEMPLE_OF_TIME, world, [
        (Regions.KOKIRI_FOREST, lambda s, r, w: True)
    ])

    # Locations
    add_locations(Regions.ROOT, world, [
        (Locations.LINKS_POCKET, lambda s, r, w: True)
    ])
    # Connections
    connect_regions(Regions.ROOT, world, [
        (Regions.ROOT_EXITS, lambda s, r, w: is_child(s, r, w) or has_item(Events.TIME_TRAVEL, s, w))
    ])
    
    ## Root Exits
    # Connections
    connect_regions(Regions.ROOT_EXITS, world, [
        (Regions.CHILD_SPAWN, lambda s, r, w: is_child(s, r, w)), # TODO: Implement starting age
        (Regions.ADULT_SPAWN, lambda s, r, w: is_adult(s, r, w)), # TODO: Implement starting age
        (Regions.MINUET_OF_FOREST_WARP, lambda s, r, w: True),
        (Regions.BOLERO_OF_FIRE_WARP, lambda s, r, w: True),
        (Regions.SERENADE_OF_WATER_WARP, lambda s, r, w: True),
        (Regions.NOCTURNE_OF_SHADOW_WARP, lambda s, r, w: True),
        (Regions.REQUIEM_OF_SPIRIT_WARP, lambda s, r, w: True),
        (Regions.PRELUDE_OF_LIGHT_WARP, lambda s, r, w: True),
    ])

    ## Child Spawn
    # Connections
    connect_regions(Regions.CHILD_SPAWN, world, [
        (Regions.KF_LINKS_HOUSE, lambda s, r, w: True)
    ])

    ## Adult Spawn
    # Connections
    connect_regions(Regions.ADULT_SPAWN, world, [
        (Regions.TEMPLE_OF_TIME, lambda s, r, w: True)
    ])

    ## Minuet of Forest Warp
    # Connections
    connect_regions(Regions.MINUET_OF_FOREST_WARP, world, [
        (Regions.SACRED_FOREST_MEADOW, lambda s, r, w: can_use(Items.MINUET_OF_FOREST, s, w))
    ])

    ## Bolero of Fire Warp
    # Connections
    connect_regions(Regions.BOLERO_OF_FIRE_WARP, world, [
        (Regions.DMC_CENTRAL_LOCAL, lambda s, r, w: can_use(Items.BOLERO_OF_FIRE, s, w))
    ])

    ## Serenade of Water Warp
    # Connections
    connect_regions(Regions.SERENADE_OF_WATER_WARP, world, [
        (Regions.LAKE_HYLIA, lambda s, r, w: can_use(Items.SERENADE_OF_WATER, s, w))
    ])

    ## Requiem of Spirit Warp
    # Connections
    connect_regions(Regions.REQUIEM_OF_SPIRIT_WARP, world, [
        (Regions.DESERT_COLOSSUS, lambda s, r, w: can_use(Items.REQUIEM_OF_SPIRIT, s, w))
    ])

    ## Nocturne of Shadow Warp
    # Connections
    connect_regions(Regions.NOCTURNE_OF_SHADOW_WARP, world, [
        (Regions.GRAVEYARD_WARP_PAD_REGION, lambda s, r, w: can_use(Items.NOCTURNE_OF_SHADOW, s, w))
    ])
    
    ## Prelude of Light Warp
    # Connections
    connect_regions(Regions.PRELUDE_OF_LIGHT_WARP, world, [
        (Regions.TEMPLE_OF_TIME, lambda s, r, w: can_use(Items.PRELUDE_OF_LIGHT, s, w))
    ])
