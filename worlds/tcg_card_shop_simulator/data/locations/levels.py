from .. import GeneratedLocationData
from ..regions.regions import get_level_region
from ...constants import LOCATIONS_LEVELS_OFFSET

def generate_level_locations(first_level: int = 2, last_level: int = 100
) -> list[GeneratedLocationData]:
    if first_level <= 1 or last_level < first_level or last_level > 100:
        raise ValueError("invalid level interval")
    return [
        GeneratedLocationData(
            name=f"Level {level}",
            location_id=(LOCATIONS_LEVELS_OFFSET + level),
            region=get_level_region(level),
        )
        for level in range(first_level, last_level + 1)
    ]
