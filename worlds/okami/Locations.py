from BaseClasses import Region, Location, ItemClassification
from .Rules import apply_event_or_location_rules
from .Types import LocData, BrushTechniques, OkamiLocation, OkamiItem
from typing import Dict, TYPE_CHECKING
from .RegionsData import r100, r122, r101, r102

if TYPE_CHECKING:
    from . import OkamiWorld


def get_location_names():
    location_names = {}
    for region_key, region_locations in okami_locations.items():
        for location_name, location_data in region_locations.items():
            location_names[location_name] = location_data.id

    return location_names


def create_region_locations(region_code: str, reg: Region, world: "OkamiWorld"):
    if region_code in okami_locations:
        for (location_name, location_data) in okami_locations[region_code].items():
            location = OkamiLocation(world.player, location_name, location_data.id, reg)
            apply_event_or_location_rules(location, location_name, location_data, world)
            reg.locations.append(location)
            print("Created Location " + location_name)


def create_region_events(region_code: str, reg: Region, world: "OkamiWorld"):
    if region_code in okami_events:
        for (event_name, event_data) in okami_events[region_code].items():
            event_location = create_event(event_name, event_name, reg, event_data, world)
            event_location.show_in_spoiler = False


def create_event(name: str, item_name: str, region: Region, data: LocData, world: "OkamiWorld") -> Location:
    event = OkamiLocation(world.player, name, None, region)
    apply_event_or_location_rules(event, name, data, world)
    region.locations.append(event)
    event.place_locked_item(OkamiItem(item_name, ItemClassification.progression, None, world.player))
    return event


def get_total_locations(world: "OkamiWorld") -> int:
    return len(get_location_names().keys())


def is_location_valid(world: "OkamiWorld", location: str) -> bool:
    # used to mark locations as invalid when they're not in the seed bc of settings
    # data = location_table.get(location) or event_locs.get(location)

    return True


okami_locations = {
    **r100.locations,
    **r122.locations,
    **r101.locations,
    **r102.locations
}

okami_events = {
    **r100.events,
    **r122.events,
    **r101.events,
    **r102.events
}
