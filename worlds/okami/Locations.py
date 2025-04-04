from BaseClasses import Region, Location, ItemClassification
from .Rules import apply_event_or_location_rules
from .Types import LocData, BrushTechniques, OkamiLocation, OkamiItem
from typing import Dict, TYPE_CHECKING
from .RegionsData import r100,r122

if TYPE_CHECKING:
    from . import OkamiWorld

def create_region_locations(reg:Region, world:"OkamiWorld"):
    if reg.name in okami_locations:
        for (location_name, location_data) in okami_locations[reg.name].items():
            location = OkamiLocation(world.player, location_name, location_data.id, reg)
            apply_event_or_location_rules(location, location_name, location_data, world)
            reg.locations.append(location)

def create_region_events(reg:Region, world:"OkamiWorld"):
    if reg.name in okami_events:
        for (event_name,event_data) in okami_events[reg.name].items():
            event_location = create_event(event_name, event_name, reg,world)
            event_location.show_in_spoiler =False

def create_event(name: str, item_name: str, region: Region,data:LocData ,world: "OkamiWorld") -> Location:
    event = OkamiLocation(world.player, name, None, region)
    apply_event_or_location_rules(event,name,data,world)
    region.locations.append(event)
    event.place_locked_item(OkamiItem(item_name, ItemClassification.progression, None, world.player))
    return event



def get_total_locations(world: "OkamiWorld") -> int:
    total = 0
    return total


def is_location_valid(world: "OkamiWorld", location: str) -> bool:
    #used to mark locations as invalid when they're not in the seed bc of settings
    #data = location_table.get(location) or event_locs.get(location)

    return True

okami_locations={
    **r100.locations,
    **r122.locations
}

okami_events={
    **r100.events,
    **r122.events
}

