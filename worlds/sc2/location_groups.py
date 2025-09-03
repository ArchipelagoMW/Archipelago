"""
Location group definitions
"""

from typing import Dict, Set, Iterable
from .locations import DEFAULT_LOCATION_LIST, LocationData
from .mission_tables import lookup_name_to_mission, MissionFlag

def get_location_groups() -> Dict[str, Set[str]]:
    result: Dict[str, Set[str]] = {}
    locations: Iterable[LocationData] = DEFAULT_LOCATION_LIST

    for location in locations:
        if location.code is None:
            # Beat events
            continue
        mission = lookup_name_to_mission.get(location.region)
        if mission is None:
            continue

        if (MissionFlag.HasRaceSwap|MissionFlag.RaceSwap) & mission.flags:
            # Location group including race-swapped variants of a location
            agnostic_location_name = (
                location.name
                .replace(' (Terran)', '')
                .replace(' (Protoss)', '')
                .replace(' (Zerg)', '')
            )
            result.setdefault(agnostic_location_name, set()).add(location.name)

            # Location group including all locations in all raceswaps
            result.setdefault(mission.mission_name[:mission.mission_name.find(' (')], set()).add(location.name)

        # Location group including all locations in a mission
        result.setdefault(mission.mission_name, set()).add(location.name)

        # Location group by location category
        result.setdefault(location.type.name.title(), set()).add(location.name)

    return result
