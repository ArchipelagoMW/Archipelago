from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule
from ..Items import SohItem
from ..Locations import SohLocation, SohLocationData
from ..Enums import *
from ..LogicHelpers import (add_locations, connect_regions, can_use)

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


events: dict[str, SohLocationData] = {
    
}

def create_regions_and_rules(world: "SohWorld") -> None:
    for event_name, data in events.items():
        region = world.get_region(data.region)
        region.add_event(event_name, data.event_item, location_type=SohLocation, item_type=SohItem)

    set_rules(world)


def set_rules(world: "SohWorld") -> None:
    player = world.player

    ## Root
    # Locations
    add_locations(Regions.ROOT.value, world, [
        [Locations.LINKS_POCKET.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.ROOT.value, world, [
        [Regions.ROOT_EXITS.value, lambda state: True]
    ])
    
    ## Root Exits
    # Connections
    connect_regions(Regions.ROOT_EXITS.value, world, [
        [Regions.CHILD_SPAWN.value, lambda state: True], # TODO: Implement starting age
        [Regions.ADULT_SPAWN.value, lambda state: False], # TODO: Implement starting age
        [Regions.MINUET_OF_FOREST_WARP.value, lambda state: True],
        [Regions.BOLERO_OF_FIRE_WARP.value, lambda state: True],
        [Regions.SERENADE_OF_WATER_WARP.value, lambda state: True],
        [Regions.NOCTURNE_OF_SHADOW_WARP.value, lambda state: True],
        [Regions.REQUIEM_OF_SPIRIT_WARP.value, lambda state: True],
        [Regions.PRELUDE_OF_LIGHT_WARP.value, lambda state: True],
    ])

    ## Child Spawn
    # Connections
    connect_regions(Regions.CHILD_SPAWN.value, world, [
        [Regions.KF_LINKS_HOUSE.value, lambda state: True]
    ])

    ## Adult Spawn
    # Connections
    connect_regions(Regions.ADULT_SPAWN.value, world, [
        [Regions.TEMPLE_OF_TIME.value, lambda state: True]
    ])

    ## Minuet of Forest Warp
    # Connections
    connect_regions(Regions.MINUET_OF_FOREST_WARP.value, world, [
        [Regions.SACRED_FOREST_MEADOW.value, lambda state: can_use(Items.MINUET_OF_FOREST.value, state, world)]
    ])

    ## Bolero of Fire Warp
    # Connections
    connect_regions(Regions.BOLERO_OF_FIRE_WARP.value, world, [
        [Regions.DMC_CENTRAL_LOCAL.value, lambda state: can_use(Items.BOLERO_OF_FIRE.value, state, world)]
    ])

    ## Serenade of Water Warp
    # Connections
    connect_regions(Regions.SERENADE_OF_WATER_WARP.value, world, [
        [Regions.LAKE_HYLIA.value, lambda state: can_use(Items.SERENADE_OF_WATER.value, state, world)]
    ])

    ## Requiem of Spirit Warp
    # Connections
    connect_regions(Regions.REQUIEM_OF_SPIRIT_WARP.value, world, [
        [Regions.DESERT_COLOSSUS.value, lambda state: can_use(Items.REQUIEM_OF_SPIRIT.value, state, world)]
    ])

    ## Nocturne of Shadow Warp
    # Connections
    connect_regions(Regions.NOCTURNE_OF_SHADOW_WARP.value, world, [
        [Regions.GRAVEYARD_WARP_PAD_REGION.value, lambda state: can_use(Items.NOCTURNE_OF_SHADOW.value, state, world)]
    ])
    
    ## Prelude of Light Warp
    # Connections
    connect_regions(Regions.PRELUDE_OF_LIGHT_WARP.value, world, [
        [Regions.TEMPLE_OF_TIME.value, lambda state: can_use(Items.PRELUDE_OF_LIGHT.value, state, world)]
    ])
