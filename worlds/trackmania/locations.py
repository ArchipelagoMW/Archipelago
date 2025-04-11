from typing import Dict
from BaseClasses import Region, Location
from .options import MapNumber

# The number of locations depeds on the number of maps and the target time
# Each map will have a check for each medal below the target time, and one extra check for meeting the target time

class TrackmaniaLocation(Location):  # or from Locations import MyGameLocation
    game = "Trackmania"  # name of the game/world this location is in

def BuildLocationDict() -> Dict[str, int]:
    trackmania_locations : Dict[str, int]
    startingId = 24001
    idOffset = 0
    for x in range(MapNumber.range_end):
        trackmania_locations["Map " + str(x+1) + " Bronze Medal"] = startingId + idOffset
        trackmania_locations["Map " + str(x+1) + " Silver Medal"] = startingId + idOffset + 1
        trackmania_locations["Map " + str(x+1) + " Gold Medal"]   = startingId + idOffset + 2
        trackmania_locations["Map " + str(x+1) + " Author Medal"] = startingId + idOffset + 3
        trackmania_locations["Map " + str(x+1) + " Completion"]   = startingId + idOffset + 4
        idOffset += 5

    return trackmania_locations

# def BuildLocationDict(mapNumber: int, targetTime: int) -> Dict[str, int]:
#     trackmania_locations : Dict[str, int]
#     startingId = 24001
#     idOffset = 0
#     for x in range(mapNumber):
#         trackmania_locations["Map " + str(x+1) + " Bronze Medal"] = startingId + idOffset
#         idOffset += 1
#         if targetTime >= 100:
#             trackmania_locations["Map " + str(x+1) + " Silver Medal"] = startingId + idOffset
#             idOffset += 1
#         if targetTime >= 200:
#             trackmania_locations["Map " + str(x+1) + " Gold Medal"] = startingId + idOffset
#             idOffset += 1
#         if targetTime >= 300:
#             trackmania_locations["Map " + str(x+1) + " Author Medal"] = startingId + idOffset
#             idOffset += 1
#         trackmania_locations["Map " + str(x+1) + " Completion"] = startingId + idOffset
#         idOffset += 1

#     return trackmania_locations

