from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from Fill import FillError, fill_restrictive

from .constants import TMCItem, TMCLocation
from .locations import location_groups
from .options import DHCAccess

if TYPE_CHECKING:
    from . import MinishCapWorld


ELEMENT_LOCATIONS = frozenset({TMCLocation.DEEPWOOD_PRIZE, TMCLocation.COF_PRIZE, TMCLocation.DROPLETS_PRIZE,
                               TMCLocation.PALACE_PRIZE, TMCLocation.FORTRESS_PRIZE, TMCLocation.CRYPT_PRIZE})

BANNED_KEY_LOCATIONS = frozenset({TMCLocation.CRENEL_MELARI_NPC})
"""
A set of locations that dungeon filling should never place dungeon items at.
"""

ELEMENTS = frozenset({TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.WIND_ELEMENT})
"""
The list of elements that need placing when shuffle_elements is either
own_dungeon or vanilla. Order must be preserved to ensure they place onto the
same location for vanilla placement
"""

KEYS = frozenset({TMCItem.BIG_KEY_DWS, TMCItem.SMALL_KEY_DWS,
                  TMCItem.BIG_KEY_COF, TMCItem.SMALL_KEY_COF,
                  TMCItem.BIG_KEY_FOW, TMCItem.SMALL_KEY_FOW,
                  TMCItem.SMALL_KEY_TOD, TMCItem.BIG_KEY_TOD,
                  TMCItem.SMALL_KEY_RC,
                  TMCItem.BIG_KEY_POW, TMCItem.SMALL_KEY_POW,
                  TMCItem.BIG_KEY_DHC, TMCItem.SMALL_KEY_DHC})
"""
A list of keys to place, excluding ToD Big Key since that needs manual placement
to change the access rules.
"""

MAPS_COMPASSES = frozenset({TMCItem.DUNGEON_MAP_DWS, TMCItem.DUNGEON_COMPASS_DWS,
                            TMCItem.DUNGEON_MAP_COF, TMCItem.DUNGEON_COMPASS_COF,
                            TMCItem.DUNGEON_MAP_FOW, TMCItem.DUNGEON_COMPASS_FOW,
                            TMCItem.DUNGEON_MAP_TOD, TMCItem.DUNGEON_COMPASS_TOD,
                            TMCItem.DUNGEON_MAP_POW, TMCItem.DUNGEON_COMPASS_POW,
                            TMCItem.DUNGEON_MAP_DHC, TMCItem.DUNGEON_COMPASS_DHC})


def fill_dungeons(world: "MinishCapWorld"):
    multiworld = world.multiworld

    # Initialize collection state to assume player has all items except pre_filled items
    base_state = CollectionState(multiworld)
    for item in world.item_pool:
        base_state.collect(item)

    # Big Key, Small Key, Maps & Compass Fill
    for stage in [KEYS, MAPS_COMPASSES]:
        # Randomize dungeon order but keep DHC last to ensure access conditions are met
        dungeon_fill_order = ["DWS", "CoF", "ToD", "FoW", "PoW", "RC"]
        world.random.shuffle(dungeon_fill_order)
        if world.options.dhc_access.value != DHCAccess.option_closed:
            dungeon_fill_order.append("DHC")
        for dungeon in dungeon_fill_order:
            fill_dungeon(world, dungeon, stage, base_state)


def fill_dungeon(world: "MinishCapWorld", dungeon: str, stage_items: frozenset[str], base_state: CollectionState):
    multiworld = world.multiworld
    world_locations = multiworld.get_unfilled_locations(world.player)
    pre_fill_items = world.get_pre_fill_items()

    # Grab items from pre_fill list and filter to what's part of this dungeon & stage
    fill_stage_items = [item for item in pre_fill_items if item.name in stage_items and dungeon in item.name]
    if not fill_stage_items:
        return

    # Get list of locations that we can place items, filtered for current dungeon group
    fill_locations = [loc for loc in world_locations
                      if loc.name in location_groups[dungeon] and loc.name not in BANNED_KEY_LOCATIONS]

    if len(fill_locations) < len(fill_stage_items):
        raise FillError(f"Not enough locations to pre_fill for slot '{world.player_name}', did plando or other "
                        f"worlds fill too many of our dungeon locations?")

    world.random.shuffle(fill_locations)
    world.random.shuffle(fill_stage_items)

    # Create a new collection state that collects all the already placed items
    dungeon_state = base_state.copy()
    dungeon_state.sweep_for_advancements(multiworld.get_locations(world.player))

    fill_restrictive(multiworld, dungeon_state, fill_locations, fill_stage_items, single_player_placement=True,
                     lock=True, allow_excluded=True, name=f"TMC Dungeon Fill: {dungeon}")
