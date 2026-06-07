from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from .data import PickupInfo, pickup_info_collection

if TYPE_CHECKING:
    from . import CVAOSWorld

__all__ = [
    "CVAOSLocation",
    "location_name_to_id",
    "location_id_to_name",
    "flag_offset_to_location_id",
]


class CVAOSLocation(Location):
    """
    A location in Castlevania: Aria of Sorrow.
    Each location corresponds to a pickup in the game.
    """
    game: str = "Castlevania - Aria of Sorrow"


def _build_location_tables() -> tuple[dict[str, int], dict[int, str]]:
    """
    Build location name <-> ID mappings from pickup_info_collection.

    Location names use the format: "{simple_name}{specifier or ''}"
    Location IDs are based on ptr_address to ensure uniqueness.
    """
    name_to_id: dict[str, int] = {}
    id_to_name: dict[int, str] = {}

    for pickup in pickup_info_collection:
        location_name = pickup.display_name
        # Use ptr_address as the unique location ID
        location_id = pickup.ptr_address

        if location_name in name_to_id:
            raise ValueError(f"Duplicate location name: {location_name}")
        if location_id in id_to_name:
            raise ValueError(f"Duplicate location ID: {location_id:#x}")

        name_to_id[location_name] = location_id
        id_to_name[location_id] = location_name

    return name_to_id, id_to_name


location_name_to_id, location_id_to_name = _build_location_tables()


def _build_flag_offset_map() -> dict[int, int]:
    """
    Map each pickup's ``flag_offset`` (its bit index in the collected-pickup
    bitfield) to its AP location id (``ptr_address``). The client reads that
    bitfield and turns each set bit back into a location check. A given
    flag offset is unique over all pickups.
    """
    flag_to_id: dict[int, int] = {}
    for pickup in pickup_info_collection:
        if pickup.flag_offset <= 0:
            continue  # no tracked save flag
        if pickup.flag_offset in flag_to_id:
            raise ValueError(
                f"Duplicate pickup flag_offset {pickup.flag_offset} "
                f"({flag_to_id[pickup.flag_offset]:#x} vs {pickup.ptr_address:#x})")
        flag_to_id[pickup.flag_offset] = pickup.ptr_address
    return flag_to_id


flag_offset_to_location_id = _build_flag_offset_map()
