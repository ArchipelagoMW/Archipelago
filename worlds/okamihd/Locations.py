from BaseClasses import Region, Location, ItemClassification
from .Enums.LocationType import LocationType
from .Rules import apply_event_or_location_rules
from .Types import LocData, OkamiLocation, OkamiItem, resolve_option_callable, EventData
from typing import TYPE_CHECKING
from .RegionsData import okami_locations, okami_events, okami_shop_locations

if TYPE_CHECKING:
    from . import OkamiWorld


def get_location_names():
    # ALL Locations are in this table, even events and shops
    location_names = {}
    for region_key, region_locations in okami_locations.items():
        for location_name, location_data in region_locations.items():
            location_names[location_name] = location_data.id
    for region_key, region_events in okami_events.items():
        for event_name, event_data in region_events.items():
            location_names[event_name] = event_data.id
    # Include all possible shop locations (they're conditionally created based on options)
    for region_key, region_shop_locations in okami_shop_locations.items():
        for location_name, location_data in region_shop_locations.items():
            location_names[location_name] = location_data.id
    return location_names


def create_region_locations(reg: Region, world: "OkamiWorld"):
    if reg.name in okami_locations:
        for (location_name, location_data) in okami_locations[reg.name].items():
            # if location_data.praise_sanity  <= world.options.PraiseSanity:
            create_location(location_name, location_data, reg, world)

    # Create shop locations if RandomizeShops is enabled
    if world.options.RandomizeShops and reg.name in okami_shop_locations:
        shop_slots = world.options.ShopSlots.value
        created_count = 0
        for (location_name, location_data) in okami_shop_locations[reg.name].items():
            if location_data.type == LocationType.SHOP and created_count < shop_slots:
                create_location(location_name, location_data, reg, world)
                created_count += 1


def create_location(location_name: str, location_data: EventData | LocData, reg: Region, world: "OkamiWorld"):
    location = OkamiLocation(world.player, location_name, location_data.id, reg)
    # Set location
    progress_type = resolve_option_callable(location_data.progress_type, world)
    location.progress_type = progress_type
    apply_event_or_location_rules(location, location_name, location_data, world)
    reg.locations.append(location)
    return location


def create_region_events(reg: Region, world: "OkamiWorld"):
    if reg.name in okami_events:
        for (event_name, event_data) in okami_events[reg.name].items():

            precollected_item_event_state = resolve_option_callable(event_data.precollected, world)

            is_event_item_state = resolve_option_callable(event_data.is_event_item, world)

            if not precollected_item_event_state and not is_event_item_state:
                # It's a true event, we need to create it as such.
                event_location = create_event(event_name,
                                              event_data.event_item_name if event_data.event_item_name else event_name,
                                              None, reg, event_data,
                                              world)

            elif is_event_item_state:
                create_location(event_name, event_data, reg, world)


def create_event(location_name: str, item_name: str, code: int | None, region: Region, data: LocData,
                 world: "OkamiWorld") -> Location:
    event = OkamiLocation(world.player, location_name, None, region)
    event.show_in_spoiler = False
    apply_event_or_location_rules(event, location_name, data, world)
    region.locations.append(event)
    event.place_locked_item(OkamiItem(item_name, ItemClassification.progression, code, world.player))
    return event


# Remember to update me when adding locations that aren't always randomized.
def get_total_locations(world: "OkamiWorld") -> int:
    location_count = 0
    for _, region_locations in okami_locations.items():
        location_count += len(region_locations)
    for region_key, region_events in okami_events.items():
        for _, event_data in region_events.items():
            if resolve_option_callable(event_data.is_event_item, world):
                location_count += 1
    # Count shop locations if RandomizeShops is enabled
    if world.options.RandomizeShops:
        shop_slots = world.options.ShopSlots.value
        num_shops = len(okami_shop_locations)  # Number of regions with shops
        location_count += num_shops * shop_slots
    return location_count



