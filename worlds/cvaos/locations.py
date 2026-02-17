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
        location_name = pickup.identifier_key
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
