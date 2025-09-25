from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule
from worlds.oot_soh.Regions import double_link_regions
from worlds.oot_soh.Items import SohItem
from worlds.oot_soh.Locations import SohLocation, SohLocationData
from worlds.oot_soh.Enums import *
from worlds.oot_soh.LogicHelpers import (can_use)

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


events: dict[str, SohLocationData] = {
    
}

def create_regions_and_rules(world: "SohWorld") -> None:
    for event_name, data in events.items():
        region = world.get_region(data.region)
        region.add_event(event_name, data.event_item, location_type=SohLocation, item_type=SohItem)

    set_rules(world)


## REGIONS

def set_rules(world: "SohWorld") -> None:
    player = world.player

    ## Root
    # Locations
    set_rule(world.get_location(Locations.LINKS_POCKET.value),
             rule=lambda state: True)
    # Connections
    world.get_region(Regions.ROOT.value).connect(
        world.get_region(Regions.ROOT_EXITS.value),
        rule=lambda state: True)
    
    ## Root Exits
    # Locations
    # NONE
    # Connections
    world.get_region(Regions.ROOT_EXITS.value).connect(
        world.get_region(Regions.CHILD_SPAWN.value),
        rule=lambda state: True) # TODO: Implement starting age
    world.get_region(Regions.ROOT_EXITS.value).connect(
        world.get_region(Regions.ADULT_SPAWN.value),
        rule=lambda state: False) # TODO: Implement starting age
    world.get_region(Regions.ROOT_EXITS.value).connect(
        world.get_region(Regions.MINUET_OF_FOREST_WARP.value))
    world.get_region(Regions.ROOT_EXITS.value).connect(
        world.get_region(Regions.BOLERO_OF_FIRE_WARP.value))
    world.get_region(Regions.ROOT_EXITS.value).connect(
        world.get_region(Regions.SERENADE_OF_WATER_WARP.value))
    world.get_region(Regions.ROOT_EXITS.value).connect(
        world.get_region(Regions.NOCTURNE_OF_SHADOW_WARP.value))
    world.get_region(Regions.ROOT_EXITS.value).connect(
        world.get_region(Regions.REQUIEM_OF_SPIRIT_WARP.value))
    world.get_region(Regions.ROOT_EXITS.value).connect(
        world.get_region(Regions.PRELUDE_OF_LIGHT_WARP.value))

    ## Child Spawn
    # Locations
    # NONE
    # Connections
    world.get_region(Regions.CHILD_SPAWN.value).connect(
        world.get_region(Regions.KF_LINKS_HOUSE.value))

    ## Adult Spawn
    # Locations
    # NONE
    # Connections
    world.get_region(Regions.ADULT_SPAWN.value).connect(
        world.get_region(Regions.TEMPLE_OF_TIME.value))

    ## Minuet of Forest Warp
    # Locations
    # NONE
    # Connections
    world.get_region(Regions.MINUET_OF_FOREST_WARP.value).connect(
        world.get_region(Regions.SACRED_FOREST_MEADOW.value),
        rule=lambda state: can_use(Items.MINUET_OF_FOREST.value, state, world))

    ## Bolero of Fire Warp
    # Locations
    # NONE
    # Connections
    world.get_region(Regions.BOLERO_OF_FIRE_WARP.value).connect(
        world.get_region(Regions.DMC_CENTRAL_LOCAL.value),
        rule=lambda state: can_use(Items.BOLERO_OF_FIRE.value, state, world))

    ## Serenade of Water Warp
    # Locations
    # NONE
    # Connections
    world.get_region(Regions.SERENADE_OF_WATER_WARP.value).connect(
        world.get_region(Regions.LAKE_HYLIA.value),
        rule=lambda state: can_use(Items.SERENADE_OF_WATER.value, state, world))

    ## Requiem of Spirit Warp
    # Locations
    # NONE
    # Connections
    world.get_region(Regions.REQUIEM_OF_SPIRIT_WARP.value).connect(
        world.get_region(Regions.DESERT_COLOSSUS.value),
        rule=lambda state: can_use(Items.REQUIEM_OF_SPIRIT.value, state, world))

    ## Nocturne of Shadow Warp
    # Locations
    # NONE
    # Connections
    world.get_region(Regions.NOCTURNE_OF_SHADOW_WARP.value).connect(
        world.get_region(Regions.GRAVEYARD_WARP_PAD_REGION.value),
        rule=lambda state: can_use(Items.NOCTURNE_OF_SHADOW.value, state, world))

    ## Prelude of Light Warp
    # Locations
    # NONE
    # Connections
    world.get_region(Regions.PRELUDE_OF_LIGHT_WARP.value).connect(
        world.get_region(Regions.TEMPLE_OF_TIME.value),
        rule=lambda state: can_use(Items.PRELUDE_OF_LIGHT.value, state, world))
