from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule
from worlds.oot_soh.Items import SohItem
from worlds.oot_soh.Locations import SohLocation, SohLocationData
from worlds.oot_soh.Enums import *
from worlds.oot_soh.LogicHelpers import (add_logic, connect_regions, can_use)

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
    add_logic(Locations.LINKS_POCKET.value, lambda state: True, world)
    # Connections
    connect_regions(Regions.ROOT.value, Regions.ROOT_EXITS.value, lambda state: True, world)
    
    ## Root Exits
    # Locations
    # NONE
    # Connections
    connect_regions(Regions.ROOT_EXITS.value, Regions.CHILD_SPAWN.value, lambda state: True, world) # TODO: Implement starting age
    connect_regions(Regions.ROOT_EXITS.value, Regions.ADULT_SPAWN.value, lambda state: False, world) # TODO: Implement starting age
    connect_regions(Regions.ROOT_EXITS.value, Regions.MINUET_OF_FOREST_WARP.value, lambda state: True, world)
    connect_regions(Regions.ROOT_EXITS.value, Regions.BOLERO_OF_FIRE_WARP.value, lambda state: True, world)
    connect_regions(Regions.ROOT_EXITS.value, Regions.SERENADE_OF_WATER_WARP.value, lambda state: True, world)
    connect_regions(Regions.ROOT_EXITS.value, Regions.NOCTURNE_OF_SHADOW_WARP.value, lambda state: True, world)
    connect_regions(Regions.ROOT_EXITS.value, Regions.REQUIEM_OF_SPIRIT_WARP.value, lambda state: True, world)
    connect_regions(Regions.ROOT_EXITS.value, Regions.PRELUDE_OF_LIGHT_WARP.value, lambda state: True, world)

    ## Child Spawn
    # Locations
    # NONE
    # Connections
    connect_regions(Regions.CHILD_SPAWN.value, Regions.KF_LINKS_HOUSE.value, lambda state: True, world)

    ## Adult Spawn
    # Locations
    # NONE
    # Connections
    connect_regions(Regions.ADULT_SPAWN.value, Regions.TEMPLE_OF_TIME.value, lambda state: True, world)

    ## Minuet of Forest Warp
    # Locations
    # NONE
    # Connections
    connect_regions(Regions.MINUET_OF_FOREST_WARP.value, Regions.SACRED_FOREST_MEADOW.value, 
                    lambda state: can_use(Items.MINUET_OF_FOREST.value, state, world), world)

    ## Bolero of Fire Warp
    # Locations
    # NONE
    # Connections
    connect_regions(Regions.BOLERO_OF_FIRE_WARP.value, Regions.DMC_CENTRAL_LOCAL.value, 
                    lambda state: can_use(Items.BOLERO_OF_FIRE.value, state, world), world)

    ## Serenade of Water Warp
    # Locations
    # NONE
    # Connections
    connect_regions(Regions.SERENADE_OF_WATER_WARP.value, Regions.LAKE_HYLIA.value, 
                    lambda state: can_use(Items.SERENADE_OF_WATER.value, state, world), world)

    ## Requiem of Spirit Warp
    # Locations
    # NONE
    # Connections
    connect_regions(Regions.REQUIEM_OF_SPIRIT_WARP.value, Regions.DESERT_COLOSSUS.value, 
                    lambda state: can_use(Items.REQUIEM_OF_SPIRIT.value, state, world), world)

    ## Nocturne of Shadow Warp
    # Locations
    # NONE
    # Connections
    connect_regions(Regions.NOCTURNE_OF_SHADOW_WARP.value, Regions.GRAVEYARD_WARP_PAD_REGION.value, 
                    lambda state: can_use(Items.NOCTURNE_OF_SHADOW.value, state, world), world)
    
    ## Prelude of Light Warp
    # Locations
    # NONE
    # Connections
    connect_regions(Regions.PRELUDE_OF_LIGHT_WARP.value, Regions.TEMPLE_OF_TIME.value, 
                    lambda state: can_use(Items.PRELUDE_OF_LIGHT.value, state, world), world)
