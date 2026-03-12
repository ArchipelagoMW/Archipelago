from typing import Dict

from BaseClasses import MultiWorld, Region, Entrance

from . import Locations
from .Constants import *


region_dict: Dict[str, List[str]] = {
    REGION_MENU: [],
    REGION_CAVE: [
        LOCATION_CAVE_AMMO,
        LOCATION_CAVE_RELOAD,
        LOCATION_CAVE_HEALTH,
        LOCATION_CAVE_WEAPON,
        EP_LOCATION_CAVE_MINIBOSS,
        EP_LOCATION_CAVE_BOSS,
        EVENT_LOCATION_GUARD_GONE,
    ],
    REGION_VOLCANIC: [
        LOCATION_VOLCANIC_RELOAD,
        LOCATION_VOLCANIC_HEALTH,
        LOCATION_VOLCANIC_AMMO,
        LOCATION_VOLCANIC_WEAPON,
        EP_LOCATION_VOLCANIC_BOSS,
        EVENT_LOCATION_CLIFF_GONE,
    ],
    REGION_ARCTIC: [
        LOCATION_HUB_AMMO,  # this is in hub, but past the cave that leads to arctic
        LOCATION_ARCTIC_AMMO,
        LOCATION_ARCTIC_RELOAD,
        LOCATION_ARCTIC_HEALTH,
        LOCATION_ARCTIC_WEAPON,
        LOCATION_JACKET,
        EP_LOCATION_ARCTIC_BOSS,
        EVENT_LOCATION_ACE_GONE,
    ],
    REGION_HUB: [
        LOCATION_HUB_HEALTH,
        LOCATION_HUB_RELOAD,
        EP_LOCATION_HUB_CONSOLE,
        EP_LOCATION_HUB_NINJA_SCARE,
    ],
    REGION_SWAMP: [
        LOCATION_SWAMP_AMMO,
        LOCATION_SWAMP_HEALTH,
        LOCATION_SWAMP_RELOAD,
        LOCATION_SWAMP_SPECIAL,
        EP_LOCATION_SWAMP_BOSS,
        EVENT_LOCATION_SNAKE_GONE,
    ],
    REGION_ELECTRICAL: [
        EP_LOCATION_ELEVATOR_NINJA_FIGHT,
        LOCATION_ELECTRICAL_WEAPON,
        EP_LOCATION_ELECTRICAL_MINIBOSS,
        EP_LOCATION_ELECTRICAL_EXTRA,
        EVENT_LOCATION_POWER_ON,
    ],
    REGION_ELECTRICAL_POWERED: [
        LOCATION_ELECTRICAL_RELOAD,
        LOCATION_ELECTRICAL_HEALTH,
        LOCATION_ELECTRICAL_AMMO,
        EP_LOCATION_ELECTRICAL_BOSS,
        EP_LOCATION_ELECTRICAL_FINAL_BOSS,
        EVENT_LOCATION_VICTORY,
    ],
    REGION_BATTLE_LOG: [
        BL_LOCATION_CRAB,
        BL_LOCATION_TURRET,
        BL_LOCATION_GUARD,
        BL_LOCATION_BLUE_CRAB,
        BL_LOCATION_ROLLER,
        BL_LOCATION_BEETLE,
        BL_LOCATION_CAVE_MINIBOSS,
        BL_LOCATION_CAVE_BOSS,
        BL_LOCATION_GOLD_CRAB,
        BL_LOCATION_FLY,
        BL_LOCATION_HOPPER,
        BL_LOCATION_FIRE_GUARD,
        BL_LOCATION_VOLCANIC_BOSS,
        BL_LOCATION_BAT,
        BL_LOCATION_FLEA_EGG,
        BL_LOCATION_FLEA,
        BL_LOCATION_ARCTIC_BOSS,
        BL_LOCATION_MIDGE,
        BL_LOCATION_SWAMP_BOSS,
        BL_LOCATION_NINJA_FIGHT,
        BL_LOCATION_ELECTRICAL_MINIBOSS,
        BL_LOCATION_ELECTRICAL_BOSS,
        BL_LOCATION_ELECTRICAL_FINAL_BOSS,
        BL_LOCATION_ELECTRIC_ORB,
    ]
}


def set_region_locations(region: Region, location_names: List[str], is_pool_expanded: bool, has_battle_logs: bool):
    location_pool = {**Locations.location_dict_base, **Locations.location_dict_events}
    if is_pool_expanded:
        location_pool = {**Locations.location_dict_expanded, **Locations.location_dict_event_expanded}
    if has_battle_logs:
        location_pool.update(Locations.location_dict_battle_log)
    region.locations = [
        Locations.SavingPrincessLocation(
            region.player,
            name,
            Locations.location_dict[name].code,
            region
        ) for name in location_names if name in location_pool.keys()
    ]


def create_regions(multiworld: MultiWorld, player: int, is_pool_expanded: bool, has_battle_logs: bool):
    for region_name, location_names in region_dict.items():
        # battle log region only exists if battle log checks are on
        if not has_battle_logs and region_name == REGION_BATTLE_LOG:
            continue
        region = Region(region_name, player, multiworld)
        set_region_locations(region, location_names, is_pool_expanded, has_battle_logs)
        multiworld.regions.append(region)
    connect_regions(multiworld, player, has_battle_logs)


def connect_regions(multiworld: MultiWorld, player: int, has_battle_logs):
    # and add a connection from the menu to the hub region
    menu = multiworld.get_region(REGION_MENU, player)
    hub = multiworld.get_region(REGION_HUB, player)
    connection = Entrance(player, f"{REGION_HUB} entrance", menu)
    menu.exits.append(connection)
    connection.connect(hub)

    # now add an entrance from every other region to hub
    for region_name in region_dict.keys() - {REGION_MENU, REGION_HUB, REGION_ELECTRICAL_POWERED}:
        # battle log region only exists if battle log checks are on
        if not has_battle_logs and region_name == REGION_BATTLE_LOG:
            continue
        connection = Entrance(player, f"{region_name} entrance", hub)
        hub.exits.append(connection)
        connection.connect(multiworld.get_region(region_name, player))

    # and finally, the connection between the final region and its powered version
    electrical = multiworld.get_region(REGION_ELECTRICAL, player)
    connection = Entrance(player, f"{REGION_ELECTRICAL_POWERED} entrance", electrical)
    electrical.exits.append(connection)
    connection.connect(multiworld.get_region(REGION_ELECTRICAL_POWERED, player))
