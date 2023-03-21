import logging
import os
from .Data import load_json, get_region_data, get_extracted_data
from .Warps import Warp, warps_connect_ltr, get_warp_map, get_warp_region_name


_error_messages = []
_warn_messages = []
_failed = False


def sanity_check():
    global _failed
    _failed = False

    _check_exits()
    _check_warps()
    _check_locations()

    return _finish()


def _check_exits():
    region_data = get_region_data()
    for name, region in region_data.items():
        for region_exit in region.exits:
            if region_exit not in region_data:
                _error(f"Region [{region_exit}] referenced by [{name}] was not defined")


def _check_warps():
    ignorable_warps = load_json(os.path.join(os.path.dirname(__file__), "data/ignorable_warps.json"))
    warp_map = get_warp_map()
    for warp_source, warp_dest in warp_map.items():
        can_ignore = False
        for ignorable_warp in ignorable_warps:
            if warp_source == ignorable_warp:
                can_ignore = True
        if can_ignore:
            continue

        if warp_dest is None:
            _error(f"Warp [{warp_source}] has no destination")
        elif not warps_connect_ltr(warp_dest, warp_source) and not Warp(warp_source).is_one_way:
            _error(f"Warp [{warp_source}] appears to be a one-way warp but was not marked as one")
        elif get_warp_region_name(warp_source) is None:
            _warn(f"Warp [{warp_source}] was not claimed by any region")


def _check_locations():
    extracted_data = get_extracted_data()
    ignorable_locations = load_json(os.path.join(os.path.dirname(__file__), "data/ignorable_locations.json"))
    claimed_locations = [location for region in get_region_data().values() for location in region.locations]
    claimed_location_map = {}
    for location_data in claimed_locations:
        if location_data.name in claimed_location_map:
            _error(f"Location [{location_data.name}] was claimed by multiple regions")
        claimed_location_map[location_data.name] = location_data

    for location_name in extracted_data["locations"]:
        if (not location_name in claimed_location_map and not location_name in ignorable_locations):
            _warn(f"Location [{location_name}] was not claimed by any region")


def _finish():
    global _error_messages
    global _warn_messages
    global _failed
    _warn_messages.sort()
    _error_messages.sort()
    for message in _warn_messages:
        logging.warning(message)
    for message in _error_messages:
        logging.error(message)
    logging.debug("Sanity check done. Found %s errors and %s warnings.", len(_error_messages), len(_warn_messages))
    return not _failed


def _error(message):
    global _error_messages
    global _failed
    _failed = True
    _error_messages.append(message)


def _warn(message):
    global _warn_messages
    _warn_messages.append(message)
