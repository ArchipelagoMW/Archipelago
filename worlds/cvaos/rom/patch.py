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
from ..items import item_table
from .entity import GBA_ROM_BASE

if TYPE_CHECKING:
    from BaseClasses import Location
    from .. import CVAOSWorld

CVAOS_USA_HASH = "e7470df4d241f73060d14437011b90ce"

# Archipelago metadata written into clean ROM free space (CLIENT_PLAN sec. 4B/5c). These are
# *file offsets* — both APProcedurePatch tokens and the BizHawk ROM domain the client reads
# are file-offset based. The region at file 0x660000+ (GBA 0x08660000) is well clear of the
# last real data at 0x651163. ARCHIPELAGO_IDENTIFIER doubles as the client/patch compatibility
# gate; bump it whenever the patch/client contract changes.
ARCHIPELAGO_IDENTIFIER_START = 0x660000   # 13 bytes
ARCHIPELAGO_IDENTIFIER = "CVAOS_AP_V0.1"
AUTH_NUMBER_START = 0x660010              # 16 bytes


# Item encoding lookup: AP item *code* -> (type_num, subtype_num, item_offset). Keyed by the stable
# packed code (not the display name) so renaming AP items can never desync ROM item placement.

_item_encoding: Dict[int, tuple[int, int, int]] = {
    item_table[p.display_name].code: (p.type_num, p.subtype_num, p.item_offset)
    for p in pickup_infos
}


def get_item_encoding(item_code: int) -> tuple[int, int, int]:
    """Return (type_num, subtype_num, item_offset) for a CVAoS item by its packed AP code."""
    return _item_encoding[item_code]


# Placeholder appearance for locations holding another world's item. AoS must physically give the
# collector *something* when a pickup is collected, and the data has no "null item", so we use a
# Skull Key (PICKUP type 4, consumable subtype 2, item_offset 25): an item not available in the game
# (and therefore an item that is *not* a placed)
# pickup anywhere, so it reads as an obvious "this was someone else's item" token.\
# This is intentional: the AP location check is driven by the collected-pickup save flag (the client reads
# PICKUP_FLAGS), NOT by what the pickup grants, so the substitute never affects check-sending. The
# real behaviour -- grant nothing locally and show a "sent X to Player Y" multiworld textbox -- needs
# the Phase 6 Strategy B ASM hook (see ROADMAP). Keep type=4 so the entity still sets its save flag.
_AP_PLACEHOLDER = (4, 2, 25)  # Skull Key

# Location data lookup: Location number -> ROM bytes

def get_location_data(world: CVAOSWorld, active_locations: List[Location]) -> Dict[int, bytes]:
    """Build a dict of {rom_file_offset: bytes_to_write} for every location."""
    writes: Dict[int, bytes] = {}

    for loc in active_locations:
        rom_offset = loc.address - GBA_ROM_BASE

        if loc.item.player == world.player:
            type_num, subtype_num, item_offset = get_item_encoding(loc.item.code)
        else:
            type_num, subtype_num, item_offset = _AP_PLACEHOLDER

        # Write type + subtype at entity +0x05
        writes[rom_offset + 0x05] = bytes([type_num, subtype_num])
        # Write item_offset at entity +0x0A  (little-endian u16)
        writes[rom_offset + 0x0A] = item_offset.to_bytes(2, "little")

    return writes


# Patch classes

def get_base_rom_bytes() -> bytes:
    file_name = get_settings().cvaos_options.rom_file
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

    # AP metadata in ROM free space: the identifier the client validates, and the
    # slot auth it reads to connect.
    patch.write_token(APTokenTypes.WRITE, ARCHIPELAGO_IDENTIFIER_START,
                      ARCHIPELAGO_IDENTIFIER.encode("ascii"))
    patch.write_token(APTokenTypes.WRITE, AUTH_NUMBER_START, bytes(world.auth))

    patch.write_file("token_data.bin", patch.get_token_binary())
