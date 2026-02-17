"""worlds/kirbyam/locations.py

Kirby & The Amazing Mirror location definitions.

This module is intentionally "Kirby-first": AP location IDs come directly from
worlds/kirbyam/data.py (which loads worlds/kirbyam/data/locations.json).

At this stage, we only model AP-facing IDs. If/when ROM/RAM pointers are needed
for BizHawk or patching, add explicit fields (e.g., rom_address/ram_address) to
LocationData in data.py and thread them through here.
"""

from __future__ import annotations

from typing import Dict, Optional

from BaseClasses import Location, Region

from .data import data


class KirbyAmLocation(Location):
    game: str = "Kirby & The Amazing Mirror"

    # Convenience fields used by KirbyAmWorld.create_items()
    key: str | None
    default_item_code: int | None

    def __init__(
        self,
        player: int,
        name: str,
        address: int | None,
        parent: Region | None = None,
        *,
        key: str | None = None,
        default_item_code: int | None = None,
    ) -> None:
        super().__init__(player, name, address, parent)
        self.key = key
        self.default_item_code = default_item_code


def create_location_label_to_id_map() -> dict[str, int]:
    """Map human-readable location labels -> AP location id."""
    label_to_id_map: dict[str, int] = {}
    for loc in data.locations.values():
        label_to_id_map[loc.label] = loc.location_id
    return label_to_id_map
