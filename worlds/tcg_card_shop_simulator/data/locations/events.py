from enum import IntEnum

from .. import GeneratedLocationData
from ..regions.regions import Regions
from ...constants import LOCATIONS_EVENTS_OFFSET


class EventFormat(IntEnum):
    STANDARD = 0
    PAUPER = 1
    FIRE_CUP = 2
    EARTH_CUP = 3
    WATER_CUP = 4
    WIND_CUP = 5
    FIRST_EDITION_VINTAGE = 6
    SILVER_BORDER = 7
    GOLD_BORDER = 8
    EX_BORDER = 9
    FULL_ART_BORDER = 10
    FOIL = 11
    NO_FORMAT = 12


FORMAT_NAMES: dict[EventFormat, str] = {
    EventFormat.STANDARD: "Standard",
    EventFormat.PAUPER: "Pauper",
    EventFormat.FIRE_CUP: "Fire Cup",
    EventFormat.EARTH_CUP: "Earth Cup",
    EventFormat.WATER_CUP: "Water Cup",
    EventFormat.WIND_CUP: "Wind Cup",
    EventFormat.FIRST_EDITION_VINTAGE: "First Edition Vintage",
    EventFormat.SILVER_BORDER: "Silver Border",
    EventFormat.GOLD_BORDER: "Gold Border",
    EventFormat.EX_BORDER: "EX Border",
    EventFormat.FULL_ART_BORDER: "Full Art Border",
    EventFormat.FOIL: "Foil",
    EventFormat.NO_FORMAT: "No Format",
}


def generate_event_locations(formats: list[EventFormat], games_per_format: int = 15) -> list[GeneratedLocationData]:
    if not 0 <= games_per_format < 1000:
        raise ValueError("Play Table Games out of range")
    return [
        GeneratedLocationData(
            name=(f"Play {n} Event Games" if tableFormat == EventFormat.NO_FORMAT
                  else f"Play {n} {FORMAT_NAMES[tableFormat]} Format Games"),
            location_id=(LOCATIONS_EVENTS_OFFSET + (tableFormat.value * 1000) + n),
            region=Regions.EVENTS,
        )
        for tableFormat in formats
        for n in range(1, games_per_format + 1)
    ]
