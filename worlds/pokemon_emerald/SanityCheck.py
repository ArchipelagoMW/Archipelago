import logging
import os
from .Data import load_json, get_region_data
from .Warps import warps_connect_ltr, get_warp_map, get_warp_region_name


_dot_dir = os.path.dirname(__file__)
_error_messages = []
_warn_messages = []
_failed = False


def sanity_check():
    global _failed
    _failed = False

    region_data = get_region_data()

    _check_exits(region_data)
    _check_warps()
    # TODO: Check location claims

    if (_failed): return _finish()

    return _finish()


def _check_exits(regions):
    for name, region in regions.items():
        for exit in region.exits:
            if (not exit in regions):
                _error(f"Region [{exit}] referenced by [{name}] was not defined")


def _check_warps():
    ignorable_warps = load_json(os.path.join(os.path.dirname(__file__), "data/ignorable_warps.json"))
    warp_map = get_warp_map()
    for warp_source, warp_dest in warp_map.items():
        can_ignore = False
        for ignorable_warp in ignorable_warps:
            if (warp_source == ignorable_warp):
                can_ignore = True
        if (can_ignore): continue

        if (warp_dest == None):
            _error(f"Warp [{warp_source}] has no destination")
        elif (not warps_connect_ltr(warp_dest, warp_source)):
            _warn(f"Warp [{warp_source}] appears to be a one-way warp")
        elif (get_warp_region_name(warp_source) == None):
            _warn(f"Warp [{warp_source}] was not claimed by any region")


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
    logging.debug(f"Sanity check done. Found {len(_error_messages)} errors and {len(_warn_messages)} warnings.")
    return not _failed


def _error(message):
    global _error_messages
    global _failed
    _failed = True
    _error_messages.append(message)


def _warn(message):
    global _warn_messages
    _warn_messages.append(message)
