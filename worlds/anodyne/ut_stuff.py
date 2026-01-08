import json
import os.path

from .Data.Events import all_events
from .Data.Locations import all_locations
from .Data.Regions import RegionEnum, all_areas, Nexus


def map_page_index(data: None | int):
    if not isinstance(data, int):
        return 0
    return {
        area['name']: index
        for index, area in enumerate(make_map())
    }[all_areas[data].area_name()]


def location_icon_coords(index: int | None, coords: dict[str, int]) -> tuple[int, int, str] | None:
    """Converts player coordinates provided by the game mod into image coordinates for the map page."""
    if index is None or not coords:
        return None

    return coords.get("X", 0) * 160 + 80, coords.get("Y", 0) * 160 + 80, f"images/icons/young_player.png"


UTTrackerData = {
    "map_page_folder": "tracker",
    "map_page_maps": "maps.json",
    "map_page_locations": "locations.json",
    "map_page_setting_key": "Slot:{player}:MapIndex",
    "map_page_index": map_page_index,
    "external_pack_key": "ut_tracker_path",
    "location_setting_key": "Slot:{player}:MapLocation",
    "location_icon_coords": location_icon_coords,
}

def make_map():
    return sorted([{
        "name": area.area_name(),
        "img": f"images/maps/{area.__name__.upper()}.png",
        "location_size": 20,
        "location_border_thickness": 1
    } for area in all_areas], key=lambda d: 0 if d["name"] == "Nexus" else 1)


def location_data():
    all_locs: dict[type[RegionEnum], dict[tuple[int, int], list[str]]] = {}

    for location in all_locations:
        all_locs.setdefault(location.region.__class__, {}).setdefault(location.tracker_loc, []).append(location.name)
        if location.region.__class__ is not Nexus:
            all_locs.setdefault(Nexus, {}).setdefault(location.region.nexus_ut_loc(), []).append(location.name)

    for event in all_events:
        all_locs.setdefault(event.region.__class__, {}).setdefault(event.tracker_loc, []).append(event.name)
        if event.region.__class__ is not Nexus:
            # Move event overviews a bit to the left in the nexus overview so they don't overlap
            loc = event.region.nexus_ut_loc()
            loc = (loc[0] - 25, loc[1])
            all_locs.setdefault(Nexus, {}).setdefault(loc, []).append(event.name)

    return [{
        "name": region.area_name(),
        "children": [
            {
                "name": region.area_name(),
                "map_locations": [{"map": region.area_name(), "x": map_loc[0], "y": map_loc[1]}],
                "sections": [{"name": name} for name in names]
            }
            for map_loc, names in map_locs.items()
        ]
    } for region, map_locs in all_locs.items()]


if '.apworld' not in os.path.abspath(__file__):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, 'tracker/maps.json'), 'w', encoding='utf-8') as f:
        json.dump(make_map(), f, ensure_ascii=True, indent=4)
    with open(os.path.join(base_dir, 'tracker/locations.json'), 'w', encoding='utf-8') as f:
        json.dump(location_data(), f, ensure_ascii=True, indent=4)
    del UTTrackerData["external_pack_key"]
