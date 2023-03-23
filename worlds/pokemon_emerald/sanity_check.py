"""
Looks through data object to double-check it makes sense. Will fail for missing or duplicate definitions or
duplicate claims and give warnings for unused and unignored locations or warps.
"""
import logging
import os

from .data import load_json, data


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
    for name, region in data.regions.items():
        for region_exit in region.exits:
            if region_exit not in data.regions:
                _error(f"Region [{region_exit}] referenced by [{name}] was not defined")


def _check_warps():
    ignorable_warps = set(load_json(os.path.join(os.path.dirname(__file__), "data/ignorable_warps.json")))
    for warp_source, warp_dest in data.warp_map.items():
        if warp_source in ignorable_warps:
            continue

        if warp_dest is None:
            _error(f"Warp [{warp_source}] has no destination")
        elif not data.warps[warp_dest].connects_to(data.warps[warp_source]) and not data.warps[warp_source].is_one_way:
            _error(f"Warp [{warp_source}] appears to be a one-way warp but was not marked as one")


def _check_locations():
    ignorable_locations = load_json(os.path.join(os.path.dirname(__file__), "data/ignorable_locations.json"))
    claimed_locations = [location for region in data.regions.values() for location in region.locations]
    claimed_locations_set = set()
    for location_name in claimed_locations:
        if location_name in claimed_locations_set:
            _error(f"Location [{location_name}] was claimed by multiple regions")
        claimed_locations_set.add(location_name)

    for location_name in data.locations:
        if location_name not in claimed_locations and location_name not in ignorable_locations:
            _warn(f"Location [{location_name}] was not claimed by any region")


def _finish():
    _warn_messages.sort()
    _error_messages.sort()
    for message in _warn_messages:
        logging.warning(message)
    for message in _error_messages:
        logging.error(message)
    logging.debug("Sanity check done. Found %s errors and %s warnings.", len(_error_messages), len(_warn_messages))
    return not _failed


def _error(message):
    global _failed
    _failed = True
    _error_messages.append(message)


def _warn(message):
    _warn_messages.append(message)
