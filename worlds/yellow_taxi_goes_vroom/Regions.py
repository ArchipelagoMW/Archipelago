from __future__ import annotations
from typing import Callable, Dict, List, NamedTuple, TYPE_CHECKING

from BaseClasses import CollectionState
from . import Locations

from .Names.RegionName import *
from .Names.ItemName import *
from .Names.EventName import *

if TYPE_CHECKING:
    from . import YTGVWorld

class YTGVRegionData(NamedTuple):
    exits: List[str] = []
    rules: Dict[str, Callable[[CollectionState], bool]] = {}

def create_region_data_table(world: YTGVWorld) -> Dict[str, YTGVRegionData]:
    return {
        MENU: YTGVRegionData(
            exits = [
                MORIOS_LAB,
            ],
            rules = {}
        ),
        LAW_FIRM: YTGVRegionData(
            exits = [
                GRANNYS_ISLAND,
            ],
            rules = {}
        ),
        MORIOS_LAB: YTGVRegionData(
            exits = [
                GRANNYS_ISLAND,
                MORIOS_ISLAND,
                BOMBEACH,
                ARCADE_PLAZA,
                PIZZA_TIME,
                TOSLA_SQUARE,
                MAURIZIOS_CITY,
                CRASH_TEST_INDUSTRIES,
                MORIOS_MIND,
                OBSERVING,
                ANTICIPATION,
            ],
            rules = {
                GRANNYS_ISLAND: lambda state: state.has(GEAR, world.player, 0),
                MORIOS_ISLAND: lambda state: state.has(GEAR, world.player, 3),
                BOMBEACH: lambda state: state.has(GEAR, world.player, 6),
                ARCADE_PLAZA: lambda state: state.has(GEAR, world.player, 18),
                PIZZA_TIME: lambda state: state.has(GEAR, world.player, 32),
                TOSLA_SQUARE: lambda state: state.has(GEAR, world.player, 50),
                MAURIZIOS_CITY: lambda state: state.has(GEAR, world.player, 65),
                CRASH_TEST_INDUSTRIES: lambda state: state.has(GEAR, world.player, 80),
                MORIOS_MIND: lambda state: state.has(GEAR, world.player, 0),
                OBSERVING: lambda state: state.has(GEAR, world.player, 0),
                ANTICIPATION: lambda state: state.has(GEAR, world.player, 130),
            }
        ),
        CRASH_AGAIN: YTGVRegionData(
            exits = [
                GRANNYS_ISLAND,
            ],
            rules = {}
        ),
        ICE_CREAM_TRUCK: YTGVRegionData(
            exits = [
                GRANNYS_ISLAND,
            ],
            rules = {}
        ),
        GRANNYS_ISLAND: YTGVRegionData(
            exits = [
                MORIOS_LAB,
                ICE_CREAM_TRUCK,
                LAW_FIRM,
                CRASH_AGAIN,
                PIZZA_OVEN,
                GYM_GEARS,
                FECAL_MATTERS,
                FLUSHED_AWAY,
                MOON, # accessible after beating Alien Mosk
                MOSKS_ROCKET, # accessable after beating Granny
            ],
            rules = {
                MOON: lambda state: state.has(TO_THE_MOON, world.player),
                MOSKS_ROCKET: lambda state: state.has(SHE_IS_FINE_NOW, world.player),
                # TODO: allow access to MOON after beating Alien Mosk
                # TODO: check other regions for conditions (FECAL_MATTERS, etc)
            }
        ),
        PIZZA_OVEN: YTGVRegionData(
            exits = [
                GRANNYS_ISLAND
            ],
            rules = {}
        ),
        PIZZA_OVEN_900_DEGREES: YTGVRegionData(
            exits = [
                PIZZA_TIME,
            ],
            rules = {}
        ),
        PIZZA_TIME: YTGVRegionData(
            exits = [
                MORIOS_LAB,
                PIZZA_OVEN_400_DEGREES,
                PIZZA_OVEN_600_DEGREES,
                PIZZA_OVEN_900_DEGREES,
            ],
            rules = {}
        ),
        PIZZA_OVEN_600_DEGREES: YTGVRegionData(
            exits = [
                PIZZA_TIME,
            ],
            rules = {}
        ),
        PIZZA_OVEN_400_DEGREES: YTGVRegionData(
            exits = [
                PIZZA_TIME,
            ],
            rules = {}
        ),
        BOMBEACH: YTGVRegionData(
            exits = [
                MORIOS_LAB,
                CAVE,
            ],
            rules = {}
        ),
        CAVE: YTGVRegionData(
            exits = [
                BOMBEACH,
            ],
            rules = {}
        ),
        TOSLA_OFFICES: YTGVRegionData(
            exits = [
                TOSLA_SQUARE,
            ],
            rules = {}
        ),
        TOSLA_SQUARE: YTGVRegionData(
            exits = [
                MORIOS_LAB,
                TOSLA_OFFICES,
            ],
            rules = {}
        ),
        GYM_GEARS: YTGVRegionData(
            exits = [
                GRANNYS_ISLAND,
            ],
            rules = {}
        ),
        FECAL_MATTERS: YTGVRegionData(
            exits = [
                GRANNYS_ISLAND,
            ],
            rules = {}
        ),
        FLUSHED_AWAY: YTGVRegionData(
            exits = [
                GRANNYS_ISLAND,
            ],
            rules = {}
        ),
        PURPLE_TUNNEL: YTGVRegionData(
            exits = [
                MAURIZIOS_CITY,
            ],
            rules = {}
        ),
        MAURIZIOS_CITY: YTGVRegionData(
            exits = [
                PURPLE_TUNNEL,
            ],
            rules = {}
        ),
        PIPE_ZONE: YTGVRegionData(
            exits = [
                CRASH_TEST_INDUSTRIES,
            ],
            rules = {}
        ),
        CRASH_TEST_INDUSTRIES: YTGVRegionData(
            exits = [
                MORIOS_LAB,
                PIPE_ZONE,
            ],
            rules = {}
        ),
        MORIOS_MIND: YTGVRegionData(
            exits = [
                MORIOS_LAB,
                DREAMING,
            ],
            rules = {}
        ),
        DREAMING: YTGVRegionData(
            exits = [
                MORIOS_MIND,
            ],
            rules = {}
        ),
        ROOFTOPS: YTGVRegionData(
            exits = [
                OBSERVING,
            ],
            rules = {}
        ),
        THE_GREEN_PLACE: YTGVRegionData(
            exits = [
                OBSERVING,
            ],
            rules = {}
        ),
        OBSERVING: YTGVRegionData(
            exits = [
                MORIOS_LAB,
                THE_GREEN_PLACE,
                ROOFTOPS,
            ],
            rules = {}
        ),
        ANTICIPATION: YTGVRegionData(
            exits = [
                MORIOS_LAB,
                TOSLA_HQ,
            ],
            rules = {}
        ),
        TOSLA_HQ: YTGVRegionData(
            exits = [
                MORIOS_LAB,
                MOON,
                # There is no direct way back to ANTICIPATION
            ],
            rules = {}
        ),
        SPACESHIP: YTGVRegionData(
            exits = [
                GRANNYS_ISLAND,
                # There is no direct way back to MOON
            ],
            rules = {}
        ),
        MOON: YTGVRegionData(
            exits = [
                GRANNYS_ISLAND,
            ],
            rules = {}
        ),
        FAR_FAR_AWAY: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        INFILTRATION: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        MID_AIR: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        EYE_SURGERY: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        CONVEYOR_BELTS: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        HEROIC_MOVES: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        SMELLY_SLIMES: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        COSTIPATION: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        PODIUM: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        STEALTHY: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        BUTTONS_SMASHING: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        PEPPERONI: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        BOMB_IT: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        WELCOMING_CLIMBS: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        LAB_MEMORIES: YTGVRegionData(
            exits = [
                MOSKS_ROCKET,
            ],
            rules = {}
        ),
        MOSKS_ROCKET: YTGVRegionData(
            exits = [
                GRANNYS_ISLAND,
                FAR_FAR_AWAY,
                INFILTRATION,
                MID_AIR,
                EYE_SURGERY,
                CONVEYOR_BELTS,
                HEROIC_MOVES,
                SMELLY_SLIMES,
                COSTIPATION,
                PODIUM,
                STEALTHY,
                PEPPERONI,
                BUTTONS_SMASHING,
                BOMB_IT,
                WELCOMING_CLIMBS,
                LAB_MEMORIES,
            ],
            rules = {}
        ),
        ARCADE_PLAZA: YTGVRegionData(
            exits = [
                MORIOS_LAB,
                ARCADE_PANIK,
            ],
            rules = {}
        ),
        ARCADE_PANIK: YTGVRegionData(
            exits = [
                MORIOS_LAB,
                FLIPPER,
            ],
            rules = {}
        ),
        FLIPPER: YTGVRegionData(
            exits = [
                ARCADE_PANIK,
            ],
            rules = {}
        ),
        MORIOS_HOME: YTGVRegionData(
            exits = [
                MORIOS_ISLAND,
                WEIRD_TUNNELS,
            ],
            rules = {}
        ),
        MORIOS_ISLAND: YTGVRegionData(
            exits = [
                MORIOS_LAB,
                MORIOS_HOME,
            ],
            rules = {}
        ),
        WEIRD_TUNNELS: YTGVRegionData(
            exits = [
                MORIOS_HOME,
            ],
            rules = {}
        )


        # MORIOS_LAB: YTGVRegionData(
        #     exits = [
        #         GRANNYS_ISLAND,
        #         TOSLA_HQ,
        #     ],
        #     rules = {
        #         TOSLA_HQ: lambda state: state.has(ItemName.GEAR, world.player, 2)
        #     },
        # ),
        # GRANNYS_ISLAND: YTGVRegionData([
        #     MORIOS_LAB,
        # ]),
        # TOSLA_HQ: YTGVRegionData([
        #     MORIOS_LAB,
        #     MOON,
        # ]),
        # MOON: YTGVRegionData([
        #     MORIOS_LAB
        # ])
    }

region_name_to_locations = {}

for location_name, location_data in Locations.location_data_table.items():
    locations = region_name_to_locations.setdefault(location_data.region, {})
    locations[location_name] = location_data.id

from pprint import pprint
print("##### DEBUG: region_name_to_locations:")
pprint(region_name_to_locations)