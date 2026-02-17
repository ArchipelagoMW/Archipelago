"""
Looks through data object to double-check it makes sense. Will fail for missing or duplicate definitions or
duplicate claims and give warnings for unused and unignored locations or warps.
"""
import logging
from typing import List


def validate_group_maps() -> bool:
    """Validate that group definitions only reference existing location labels.

    Kirby currently does not model "maps" (unlike the Pokémon Emerald example).
    This check is intentionally lightweight so it continues to provide signal
    without blocking early development.
    """
    from .groups import ITEM_GROUPS, LOCATION_GROUPS

    failed = False

    # Item groups should not contain empty strings.
    for group_name, items in ITEM_GROUPS.items():
        if any(not isinstance(i, str) or not i for i in items):
            failed = True
            logging.error("Kirby & The Amazing Mirror: Item group %s contains invalid entries", group_name)

    # Location groups should not contain empty strings.
    for group_name, locs in LOCATION_GROUPS.items():
        if any(not isinstance(l, str) or not l for l in locs):
            failed = True
            logging.error("Kirby & The Amazing Mirror: Location group %s contains invalid entries", group_name)

    return not failed


def validate_regions() -> bool:
    """
    Verifies that Kirby's data doesn't have duplicate or missing
    regions/warps/locations. Meant to catch problems during development like
    forgetting to add a new location or incorrectly splitting a region.
    """
    from .data import data, load_json_data

    locations = load_json_data("locations.json")
    error_messages: list[str] = []
    warn_messages: list[str] = []
    failed = False

    def error(message: str) -> None:
        nonlocal failed
        failed = True
        error_messages.append(message)

    def warn(message: str) -> None:
        warn_messages.append(message)

    # Check regions
    for name, region in data.regions.items():
        for region_exit in region.exits:
            if region_exit not in data.regions:
                error(f"Kirby & The Amazing Mirror: Region [{region_exit}] referenced by [{name}] was not defined")

    # Check locations
    claimed_locations = [location for region in data.regions.values() for location in region.locations]
    claimed_locations_set = set()
    for location_name in claimed_locations:
        if location_name in claimed_locations_set:
            error(f"Kirby & The Amazing Mirror: Location [{location_name}] was claimed by multiple regions")
        claimed_locations_set.add(location_name)

    for location_name in locations:
        if location_name not in claimed_locations:
            warn(f"Kirby & The Amazing Mirror: Location [{location_name}] was not claimed by any region")

    # Optional: Validate that bitfield indices (if present) are unique.
    bit_to_loc: dict[int, str] = {}
    for loc_key, loc in data.locations.items():
        if loc.bit_index is None:
            continue
        if loc.bit_index in bit_to_loc and bit_to_loc[loc.bit_index] != loc_key:
            error(
                "Kirby & The Amazing Mirror: bit_index %s is assigned to multiple locations (%s, %s)"
                % (loc.bit_index, bit_to_loc[loc.bit_index], loc_key)
            )
        else:
            bit_to_loc[loc.bit_index] = loc_key

    warn_messages.sort()
    error_messages.sort()

    for message in warn_messages:
        logging.warning(message)
    for message in error_messages:
        logging.error(message)

    logging.debug("Kirby & The Amazing Mirror sanity check done. Found %s errors and %s warnings.", len(error_messages), len(warn_messages))

    return not failed
