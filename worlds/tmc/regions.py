import typing

from .constants import ALL_EVENTS, ALL_REGIONS, MinishCapLocation, MinishCapRegion, TMCEvent, TMCRegion, TMCTricks
from .locations import all_locations

if typing.TYPE_CHECKING:
    from . import MinishCapWorld


def excluded_locations_by_region(region: str, disabled_locations: set[str]):
    return (loc for loc in all_locations if loc.region == region and loc.id not in disabled_locations)


def create_regions(world: "MinishCapWorld", disabled_locations: set[str], disabled_dungeons: set[str]):
    menu_region = MinishCapRegion("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    for region_key in ALL_REGIONS:
        create_region(world, region_key, excluded_locations_by_region(region_key, disabled_locations))

    dungeon_clears = {
        TMCRegion.DUNGEON_DWS_CLEAR: ("DWS", TMCEvent.CLEAR_DWS),
        TMCRegion.DUNGEON_COF_CLEAR: ("CoF", TMCEvent.CLEAR_COF),
        TMCRegion.DUNGEON_FOW_CLEAR: ("FoW", TMCEvent.CLEAR_FOW),
        TMCRegion.DUNGEON_TOD_CLEAR: ("ToD", TMCEvent.CLEAR_TOD),
        TMCRegion.DUNGEON_RC_CLEAR: ("RC", TMCEvent.CLEAR_RC),
        TMCRegion.DUNGEON_POW_CLEAR: ("PoW", TMCEvent.CLEAR_POW),
    }

    for clear, (dungeon, event) in dungeon_clears.items():
        # If the entire dungeon has been excluded, don't add the dungeon clear so players aren't expected to beat it
        if dungeon in disabled_dungeons:
            continue
        register_event(world, clear, event)

    # General Events
    for (region, event) in ALL_EVENTS:
        register_event(world, region, event)

    if TMCTricks.POT_PUZZLE in world.options.tricks.value:
        register_event(world, TMCRegion.DUNGEON_POW_IN_3F_SWITCH, TMCEvent.POW_1ST_HALF_3F_ITEM_DROP)


def register_event(world: "MinishCapWorld", region: str, event: str):
    reg = world.get_region(region)
    loc = MinishCapLocation(world.player, event, None, reg)
    loc.place_locked_item(world.create_event(event))
    reg.locations.append(loc)


def create_region(world: "MinishCapWorld", name, locations):
    ret = MinishCapRegion(name, world.player, world.multiworld)
    for location in locations:
        if location.name in world.disabled_locations:
            continue
        loc = MinishCapLocation(world.player, location.name, location.id, ret)
        ret.locations.append(loc)
    world.multiworld.regions.append(ret)
