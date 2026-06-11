"""
bytemaker structs for contiguous Aria of Sorrow RAM regions.

Offsets live in ``addresses.py``. All values are little-endian.
"""
from __future__ import annotations

from dataclasses import dataclass

from .._bytemaker_compat import SInt16, UInt8, UInt16, from_bytes_aggregate, to_bytes_aggregate

# Byte sizes of each struct, for the read that precedes a parse.
VITALS_SIZE = 8
EQUIPPED_GEAR_SIZE = 6


@dataclass
class PlayerVitals:
    """
    HP/MP block at ``addresses.CURRENT_HP`` (0x0201327A).
    """

    current_hp: SInt16
    current_mp: SInt16
    max_hp: UInt16
    max_mp: UInt16

    def to_bytes(self) -> bytes:
        return to_bytes_aggregate(self, endianness="little")

    @classmethod
    def from_bytes(cls, data: bytes) -> PlayerVitals:
        return from_bytes_aggregate(data, cls, endianness="little")


@dataclass
class EquippedGear:
    """
    Currently-equipped item/soul indices at ``addresses.EQUIPPED_WEAPON``
    (0x02013268).
    """

    weapon: UInt8
    red_soul: UInt8
    blue_soul: UInt8
    yellow_soul: UInt8
    armor: UInt8
    accessory: UInt8

    def to_bytes(self) -> bytes:
        return to_bytes_aggregate(self, endianness="little")

    @classmethod
    def from_bytes(cls, data: bytes) -> EquippedGear:
        return from_bytes_aggregate(data, cls, endianness="little")
