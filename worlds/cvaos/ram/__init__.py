"""
Live-memory (EWRAM) access for the Aria of Sorrow BizHawk client.

- ``addresses`` — the AoS EWRAM map (constants, ``GameState``, the ``INVENTORY``
  table). Pure data; importable without BizHawk.
- ``AoSRAM`` — async typed get/set helpers over those addresses for one BizHawk
  connection.
- ``PlayerVitals`` / ``EquippedGear`` — bytemaker structs for the contiguous
  regions ``AoSRAM.get_vitals`` / ``get_equipped_gear`` read.

See ``worlds/cvaos/CLIENT_PLAN.md`` (secs. 3c, 5b, 5d) for where these come from.
"""
from . import addresses
from .accessors import AoSRAM
from .addresses import INVENTORY, GameState, InventoryArray
from .structures import EquippedGear, PlayerVitals

__all__ = [
    "addresses",
    "AoSRAM",
    "INVENTORY",
    "InventoryArray",
    "GameState",
    "PlayerVitals",
    "EquippedGear",
]
