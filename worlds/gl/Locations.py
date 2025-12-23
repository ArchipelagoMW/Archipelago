from typing import Final, List, Dict

from BaseClasses import Location


class LocationData:
    name: str = ""
    id: int = 0
    difficulty: int = 0
    tags: Final[tuple[str, ...]]

    def __init__(self, name, id, difficulty, tags=None):
        if tags is None:
            tags = []
        self.name = name
        self.id = id
        self.difficulty = difficulty
        self.tags = tags


class GLLocation(Location):
    game: str = "Gauntlet Legends"

def import_locations() -> List[LocationData]:
    import json
    import pkgutil

    return json.loads(pkgutil.get_data(__name__, "json/locations.json").decode("utf-8"), object_hook=lambda d: LocationData(**d))



def get_locations_by_tags(tags: str | List[str]) -> List[LocationData]:
    if isinstance(tags, str):
        tags = [tags]
    return [loc for loc in all_locations if any(tag in loc.tags for tag in tags)]


def get_locations_by_all_tags(tags: List[str]) -> List[LocationData]:
    if isinstance(tags, str):
        tags = [tags]
    return [loc for loc in all_locations if all(tag in loc.tags for tag in tags)]


def get_location_ids(locations: List[LocationData]) -> List[int]:
    return [loc.id for loc in locations if loc.id]


def get_location_names(locations: List[LocationData]) -> List[str]:
    return [loc.name for loc in locations if loc.name]

all_locations: List[LocationData] = import_locations()

location_table: Dict[str, int] = {locData.name: locData.id for locData in all_locations}

location_id_to_name: Dict[int, str] = {locData.id: locData.name for locData in all_locations if locData.id is not None}

locationName_to_data: Dict[str, LocationData] = {locData.name: locData for locData in all_locations}