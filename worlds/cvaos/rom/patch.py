"""
ROM patching for Castlevania: Aria of Sorrow.
"""
from __future__ import annotations

import os
from typing import TYPE_CHECKING, Dict, List

from BaseClasses import ItemClassification
from settings import get_settings
from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes

from ..data.pickup_info import rows as pickup_infos
from .entity import GBA_ROM_BASE

if TYPE_CHECKING:
    from BaseClasses import Location
    from .. import CVAOSWorld

CVAOS_USA_HASH = "e7470df4d241f73060d14437011b90ce"


# Item encoding lookup:  identifier_key -> (type_num, subtype_num, item_offset)

_item_encoding: Dict[str, tuple[int, int, int]] = {
    p.identifier_key: (p.type_num, p.subtype_num, p.item_offset)
    for p in pickup_infos
}


def get_item_encoding(item_name: str) -> tuple[int, int, int]:
    """Return (type_num, subtype_num, item_offset) for a CVAoS item name."""
    return _item_encoding[item_name]


# Placeholder appearance for items belonging to other games.
# Uses consumable subtype (2) with Potion appearance (item_offset 0).
_AP_PLACEHOLDER = (4, 2, 0)

# Location data lookup: Location number -> ROM bytes

def get_location_data(world: CVAOSWorld, active_locations: List[Location]) -> Dict[int, bytes]:
    """Build a dict of {rom_file_offset: bytes_to_write} for every location."""
    writes: Dict[int, bytes] = {}

    for loc in active_locations:
        rom_offset = loc.address - GBA_ROM_BASE

        if loc.item.game == world.game:
            type_num, subtype_num, item_offset = get_item_encoding(loc.item.name)
        else:
            type_num, subtype_num, item_offset = _AP_PLACEHOLDER

        # Write type + subtype at entity +0x05
        writes[rom_offset + 0x05] = bytes([type_num, subtype_num])
        # Write item_offset at entity +0x0A  (little-endian u16)
        writes[rom_offset + 0x0A] = item_offset.to_bytes(2, "little")

    return writes


# Patch classes

def get_base_rom_bytes() -> bytes:
    file_name = get_settings().cvaos_settings.rom_file
    with open(file_name, "rb") as fh:
        return fh.read()


class CVAOSPatchExtension(APPatchExtension):
    game = "Castlevania - Aria of Sorrow"


class CVAOSProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [CVAOS_USA_HASH]
    patch_file_ending: str = ".apcvaos"
    result_file_ending: str = ".gba"
    game = "Castlevania - Aria of Sorrow"

    procedure = [
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def patch_rom(world: CVAOSWorld, patch: CVAOSProcedurePatch, offset_data: Dict[int, bytes]) -> None:
    """Write all item placement tokens into the patch."""
    for offset, data in offset_data.items():
        patch.write_token(APTokenTypes.WRITE, offset, data)

    patch.write_file("token_data.bin", patch.get_token_binary())
