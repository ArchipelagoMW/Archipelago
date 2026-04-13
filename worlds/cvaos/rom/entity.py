"""
AoS ROM entity structure using bytemaker for type-safe serialization.
"""
from __future__ import annotations

from dataclasses import dataclass

from bytemaker.bittypes import SInt16, UInt8, UInt16
from bytemaker.conversions.aggregate_types import from_bytes_aggregate, to_bytes_aggregate


GBA_ROM_BASE = 0x08000000
ENTITY_SIZE = 12


@dataclass
class AoSPickupEntity:
    """
    12-byte AoS Pickup entity as stored in ROM.

    Offset  Size  Field
    0x00    2     x           Position
    0x02    2     y           Position
    0x04    1     entity_id   Per-room unique ID
    0x05    1     type        Entity type (4=PICKUP, 5=HARD_PICKUP)
    0x06    1     subtype     Item category (1=money, 2=consumable, 3=weapon,
                               4=armor, 6=ability soul, 7=guardian soul, 8=enchant soul)
    0x07    1     unknown     Always 0x00
    0x08    2     var_a       flag_offset — per-location save flag. Unchanged when shuffling items.
    0x0A    2     var_b       item_offset — index of item within its subtype category
    """

    x: SInt16
    y: SInt16
    entity_id: UInt8
    type: UInt8
    subtype: UInt8
    unknown: UInt8
    var_a: UInt16
    var_b: UInt16

    def to_bytes(self) -> bytes:
        return to_bytes_aggregate(self, endianness="little")

    @classmethod
    def from_bytes(cls, data: bytes) -> AoSPickupEntity:
        return from_bytes_aggregate(data, cls, endianness="little")
