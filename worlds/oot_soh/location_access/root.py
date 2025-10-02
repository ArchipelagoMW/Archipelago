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
        (EventLocations.ROOT_AMMO_DROP, Events.AMMO_CAN_DROP, lambda bundle: True), # Not sure why but ship has this set to true immediately, so this mirrors that.
        (EventLocations.ROOT_TIME_TRAVEL, Events.TIME_TRAVEL, lambda bundle: has_item(Events.CLEARED_DEKU_TREE, bundle)), # temp
        (EventLocations.ROOT_SHIELD, Events.CAN_BUY_DEKU_SHIELD, lambda bundle: True), # Temp
        (EventLocations.TRIFORCE_HUNT_COMPLETION, Events.GAME_COMPLETED,  lambda bundle:
         (world.options.triforce_hunt == 1 and 
         has_item(Items.TRIFORCE_PIECE, bundle, world.options.triforce_hunt_required_pieces.value)) or 
         has_item(Events.GAME_COMPLETED, bundle))
    ])

    connect_regions(Regions.TEMPLE_OF_TIME, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True)
    ])

    # Locations
    add_locations(Regions.ROOT, world, [
        (Locations.LINKS_POCKET, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.ROOT, world, [
        (Regions.ROOT_EXITS, lambda bundle: starting_age(bundle) or has_item(Events.TIME_TRAVEL, bundle))
    ])
    
    ## Root Exits
    # Connections
    connect_regions(Regions.ROOT_EXITS, world, [
        (Regions.CHILD_SPAWN, lambda bundle: is_child(bundle)),
        (Regions.ADULT_SPAWN, lambda bundle: is_adult(bundle)),
        (Regions.MINUET_OF_FOREST_WARP, lambda bundle: True),
        (Regions.BOLERO_OF_FIRE_WARP, lambda bundle: True),
        (Regions.SERENADE_OF_WATER_WARP, lambda bundle: True),
        (Regions.NOCTURNE_OF_SHADOW_WARP, lambda bundle: True),
        (Regions.REQUIEM_OF_SPIRIT_WARP, lambda bundle: True),
        (Regions.PRELUDE_OF_LIGHT_WARP, lambda bundle: True),
    ])

    ## Child Spawn
    # Connections
    connect_regions(Regions.CHILD_SPAWN, world, [
        (Regions.KF_LINKS_HOUSE, lambda bundle: True)
    ])

    ## Adult Spawn
    # Connections
    connect_regions(Regions.ADULT_SPAWN, world, [
        (Regions.TEMPLE_OF_TIME, lambda bundle: True)
    ])

    ## Minuet of Forest Warp
    # Connections
    connect_regions(Regions.MINUET_OF_FOREST_WARP, world, [
        (Regions.SACRED_FOREST_MEADOW, lambda bundle: can_use(Items.MINUET_OF_FOREST, bundle))
    ])

    ## Bolero of Fire Warp
    # Connections
    connect_regions(Regions.BOLERO_OF_FIRE_WARP, world, [
        (Regions.DMC_CENTRAL_LOCAL, lambda bundle: can_use(Items.BOLERO_OF_FIRE, bundle))
    ])

    ## Serenade of Water Warp
    # Connections
    connect_regions(Regions.SERENADE_OF_WATER_WARP, world, [
        (Regions.LAKE_HYLIA, lambda bundle: can_use(Items.SERENADE_OF_WATER, bundle))
    ])

    ## Requiem of Spirit Warp
    # Connections
    connect_regions(Regions.REQUIEM_OF_SPIRIT_WARP, world, [
        (Regions.DESERT_COLOSSUS, lambda bundle: can_use(Items.REQUIEM_OF_SPIRIT, bundle))
    ])

    ## Nocturne of Shadow Warp
    # Connections
    connect_regions(Regions.NOCTURNE_OF_SHADOW_WARP, world, [
        (Regions.GRAVEYARD_WARP_PAD_REGION, lambda bundle: can_use(Items.NOCTURNE_OF_SHADOW, bundle))
    ])
    
    ## Prelude of Light Warp
    # Connections
    connect_regions(Regions.PRELUDE_OF_LIGHT_WARP, world, [
        (Regions.TEMPLE_OF_TIME, lambda bundle: can_use(Items.PRELUDE_OF_LIGHT, bundle))
    ])
