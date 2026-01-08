from typing import Iterable, Optional

from .area_rando_types import AreaDoor
from .connection_data import area_doors
from .loadout import Loadout
from .location_data import Location
from .logic_area import area_logic
from .logic_locations import location_logic


def update_area_logic(loadout: Loadout, excluded_door: Optional[AreaDoor] = None) -> None:
    stuck = False  # check if loadout keeps increasing
    door_pairs = loadout.game.door_pairs
    while not stuck:
        prev_loadout = loadout.copy()
        for paths in area_logic.values():
            for path, access in paths.items():
                origin, destination = path
                if area_doors[destination] not in loadout:
                    other = door_pairs.other(area_doors[destination])
                    if area_doors[destination] == excluded_door or other == excluded_door:
                        continue
                    if other in loadout:
                        loadout.append(area_doors[destination])
                    elif (area_doors[origin] in loadout) and access(loadout):
                        loadout.append(area_doors[destination])
                        loadout.append(other)
        if loadout == prev_loadout:
            stuck = True


def updateLogic(unusedLocations: Iterable[Location],
                loadout: Loadout,
                excluded_door: Optional[AreaDoor] = None) -> Iterable[Location]:
    update_area_logic(loadout, excluded_door)
    # print("Updating logic...")
    for thisLoc in unusedLocations:
        thisLoc['inlogic'] = location_logic[thisLoc['fullitemname']](loadout)

    return unusedLocations
