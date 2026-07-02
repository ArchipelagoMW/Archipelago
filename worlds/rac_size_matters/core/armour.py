from __future__ import annotations

from collections.abc import Callable
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum, IntFlag
from typing import NamedTuple

from ..constants import (
    Rac5ClankChallenges as RACSMCLANK,
    Rac5Locations,
    Rac5Planets,
    Rac5SkyboardChallenges as RACSMSKY,
    Rac5ArmourSet,
)
from ..interface_orchestrator.memory.accessor import MemoryAccessor
from ..interface_orchestrator.state.base_state import BaseState
from ..interface_orchestrator.storage.local import LocalStorage
from ..interface_orchestrator.structs.address_map import AddressMap
from .structs.pickups import ArmourSetCollectedStruct, ArmourStruct

# Armour address resolvers

class ArmourAddresses:
    """
    Armour Address Struct
    This is the layout of Armour in Static Memory
    Slot Offsets are the currently equiped armour pieces
    Set Offsets are the unlock addresses for the Armour
    We only need one read and one write to handle these addresses as they are next to eachother in memory
    """

    _SLOT_OFFSETS: dict[str, int] = {
        "chestplate":   0x00,
        "helmet":       0x01,
        "gloves_left":  0x02,
        "gloves_right": 0x03,
        "boots_left":   0x04,
        "boots_right":  0x05,
    }

    _SET_OFFSETS: dict[str, int] = {
        "wildfire":     0x06,
        "sludge":       0x07,
        "crystallix":   0x08,
        "electroshock": 0x09,
        "mega_bomb":    0x0A,
        "hyperborean":  0x0B,
        "chameleon":    0x0C,
    }

    def __init__(self, base: int) -> None:
        self.base = base
        for name, offset in {**self._SLOT_OFFSETS, **self._SET_OFFSETS}.items():
            setattr(self, name, base + offset)

    @property
    def slots(self) -> dict[str, int]:
        return {name: getattr(self, name) for name in self._SLOT_OFFSETS}

    @property
    def sets(self) -> dict[str, int]:
        return {name: getattr(self, name) for name in self._SET_OFFSETS}


class ArmourPiece(IntFlag):
    """
    Armour pieces are represented as bits in a byte, with the following mapping:
    - Bit 0 (0x01): Chestplate
    - Bit 1 (0x02): Helmet
    - Bit 2 (0x04): Gloves
    - Bit 4 (0x10): Boots (any value with bit 4 set is considered to have boots equipped)
    """
    NONE       = 0
    CHESTPLATE = 0x01
    HELMET     = 0x02
    GLOVES     = 0x04
    # Boots changes: it's any value with bit 4 set, because the game treats left and
    # right boots as one piece, so any value with bit 4 set is considered equipped.
    BOOTS      = 0x10
    ALL        = 0x17


@dataclass(frozen=True)
class PlayerArmour:
    """
    Wrapper for armour piece bitmask.
    This sets up named boolean properties for each piece and helper methods for working with the bitmask.
    """
    pieces: ArmourPiece

    @classmethod
    def from_value(cls, value: int) -> PlayerArmour:
        return cls(pieces=ArmourPiece(value))

    @property
    def chestplate(self) -> bool:
        return ArmourPiece.CHESTPLATE in self.pieces

    @property
    def helmet(self) -> bool:
        return ArmourPiece.HELMET in self.pieces

    @property
    def gloves(self) -> bool:
        return ArmourPiece.GLOVES in self.pieces

    @property
    def boots(self) -> bool:
        return ArmourPiece.BOOTS in self.pieces

    def has(self, piece: ArmourPiece) -> bool:
        return piece in self.pieces

    def with_piece(self, piece: ArmourPiece) -> PlayerArmour:
        return PlayerArmour(self.pieces | piece)

    def without_piece(self, piece: ArmourPiece) -> PlayerArmour:
        return PlayerArmour(self.pieces & ~piece)

    def to_value(self) -> int:
        return int(self.pieces)

    def __repr__(self) -> str:
        return f"PlayerArmour({self.pieces!r})"


# Armour pickups

class ArmourPickup(NamedTuple):
    """
    Data record for an armour pickup's information.
    This is used for monitoring and modifying armour pickups in the game.
    """
    set_key: str
    piece: ArmourPiece
    name: str
    planet: str


ARMOUR_PICKUPS: list[ArmourPickup] = [
    # Pokitaru
    ArmourPickup("wildfire", ArmourPiece.CHESTPLATE, Rac5Locations.POKITARU_CHESTPLATE, Rac5Planets.POKITARU),
    ArmourPickup("wildfire", ArmourPiece.GLOVES,     Rac5Locations.POKITARU_GLOVES,     Rac5Planets.POKITARU),
    # Ryllus
    ArmourPickup("sludge",   ArmourPiece.BOOTS,      Rac5Locations.RYLLUS_BOOTS,        Rac5Planets.RYLLUS),
    ArmourPickup("wildfire", ArmourPiece.HELMET,     Rac5Locations.RYLLUS_HELMET,       Rac5Planets.RYLLUS),
    # Kalidon
    ArmourPickup("sludge",   ArmourPiece.CHESTPLATE, Rac5Locations.KALIDON_CHESTPLATE,  Rac5Planets.KALIDON),
    ArmourPickup("wildfire", ArmourPiece.BOOTS,      Rac5Locations.KALIDON_BOOTS,       Rac5Planets.KALIDON),
    # Metalis
    # ArmourPickup("electroshock", ArmourPiece.GLOVES, Rac5Locations.METALIS_GLOVES,
    #              Rac5Planets.METALIS),  # currently unreachable
    # Dreamtime
    ArmourPickup("crystallix", ArmourPiece.CHESTPLATE, Rac5Locations.DREAMTIME_CHESTPLATE, Rac5Planets.DREAMTIME),
    # Outpost Omega
    ArmourPickup("crystallix", ArmourPiece.BOOTS,    Rac5Locations.OUTPOST_OMEGA_BOOTS, Rac5Planets.OUTPOST_OMEGA),
    # Challax
    # ArmourPickup("electroshock", ArmourPiece.CHESTPLATE, "Challax: Electroshock Chestplate",
    #              Rac5Planets.CHALLAX),  # not reachable
    ArmourPickup("electroshock", ArmourPiece.HELMET, Rac5Locations.CHALLAX_HELMET,      Rac5Planets.CHALLAX),
    # Dayni Moon
    ArmourPickup("mega_bomb", ArmourPiece.HELMET,    Rac5Locations.DAYNI_MOON_HELMET,   Rac5Planets.DAYNI_MOON),
    # Inside Clank
    ArmourPickup("mega_bomb", ArmourPiece.CHESTPLATE, Rac5Locations.INSIDE_CLANK_CHESTPLATE, Rac5Planets.INSIDE_CLANK),
]

ARMOUR_FLAG_TO_LOCATION: dict[tuple[str, ArmourPiece], str] = {
    (ap.set_key, ap.piece): ap.name
    for ap in ARMOUR_PICKUPS
}

CHALLENGE_LOCATION_TO_ARMOUR_FLAG: dict[str, tuple[str, ArmourPiece]] = {
    RACSMCLANK.METALIS_REVENGE:    ("crystallix",   ArmourPiece.HELMET),
    RACSMCLANK.METALIS_UBER:       ("crystallix",   ArmourPiece.GLOVES),
    RACSMCLANK.METALIS_NIGHT:      ("sludge",       ArmourPiece.GLOVES),
    RACSMCLANK.DAYNI_MOON_SHOWDOWN:("mega_bomb",    ArmourPiece.GLOVES),
    RACSMCLANK.DAYNI_MOON_INFINITE:("mega_bomb",    ArmourPiece.BOOTS),
    RACSMSKY.OUTPOST_OMEGA_VERTIGO:("electroshock", ArmourPiece.BOOTS),
}


# Armour set checks

class ArmourSets(IntEnum):
    """
    Enum representing different armour sets in the game.
    This is the value which is set in armour slots to represent what armour is currently equiped.
    """
    Wildfire     = 1
    Sludge       = 2
    Crystallix   = 3
    Electroshock = 4
    MegaBomb     = 5
    Hyperborean  = 6
    Chameleon    = 7


@dataclass(frozen=True)
class ArmourSetCheck:
    chestplate: int | None = None
    helmet:     int | None = None
    gloves:     int | None = None
    boots:      int | None = None

    def required_mask(self) -> int:
        mask = 0
        for val in {self.chestplate, self.helmet, self.gloves, self.boots} - {None}:
            mask |= 1 << (val - 1)
        return mask

    def matches(self, slot_values: dict[str, int]) -> bool:
        if self.chestplate is not None:
            if slot_values.get("chestplate", 0) != self.chestplate:
                return False
        if self.helmet is not None:
            if slot_values.get("helmet", 0) != self.helmet:
                return False
        if self.gloves is not None:
            if slot_values.get("gloves_left",  0) != self.gloves:
                return False
            if slot_values.get("gloves_right", 0) != self.gloves:
                return False
        if self.boots is not None:
            if slot_values.get("boots_left",  0) != self.boots:
                return False
            if slot_values.get("boots_right", 0) != self.boots:
                return False
        return True

ARMOUR_SET_CHECKS: dict[str, ArmourSetCheck] = {
    Rac5ArmourSet.WILDFIRE:      ArmourSetCheck(chestplate=ArmourSets.Wildfire,     helmet=ArmourSets.Wildfire,     gloves=ArmourSets.Wildfire,     boots=ArmourSets.Wildfire),
    Rac5ArmourSet.WILDBURST:     ArmourSetCheck(chestplate=ArmourSets.Wildfire,     helmet=ArmourSets.Sludge,       gloves=ArmourSets.Wildfire,     boots=ArmourSets.Wildfire),
    Rac5ArmourSet.SLUDGE_MK9:    ArmourSetCheck(chestplate=ArmourSets.Sludge,       helmet=ArmourSets.Sludge,       gloves=ArmourSets.Sludge,       boots=ArmourSets.Sludge),
    Rac5ArmourSet.CRYSTALLIX:    ArmourSetCheck(chestplate=ArmourSets.Crystallix,   helmet=ArmourSets.Crystallix,   gloves=ArmourSets.Crystallix,   boots=ArmourSets.Crystallix),
    Rac5ArmourSet.TRIPLE_WAVE:   ArmourSetCheck(chestplate=ArmourSets.Electroshock, helmet=ArmourSets.Wildfire,     gloves=ArmourSets.Sludge,       boots=ArmourSets.Electroshock),
    Rac5ArmourSet.SHOCK_CRYSTAL: ArmourSetCheck(chestplate=ArmourSets.Crystallix,   helmet=ArmourSets.Electroshock, gloves=ArmourSets.Crystallix,   boots=ArmourSets.Electroshock),
    Rac5ArmourSet.ELECTROSHOCK:  ArmourSetCheck(chestplate=ArmourSets.Electroshock, helmet=ArmourSets.Electroshock, gloves=ArmourSets.Electroshock, boots=ArmourSets.Electroshock),
    Rac5ArmourSet.MEGA_BOMB:     ArmourSetCheck(chestplate=ArmourSets.MegaBomb,     helmet=ArmourSets.MegaBomb,     gloves=ArmourSets.MegaBomb,     boots=ArmourSets.MegaBomb),
    Rac5ArmourSet.FIRE_BOMB:     ArmourSetCheck(chestplate=ArmourSets.MegaBomb,     helmet=ArmourSets.MegaBomb,     gloves=ArmourSets.Wildfire,     boots=ArmourSets.MegaBomb),
    Rac5ArmourSet.HYPERBOREAN:   ArmourSetCheck(chestplate=ArmourSets.Hyperborean,  helmet=ArmourSets.Hyperborean,  gloves=ArmourSets.Hyperborean,  boots=ArmourSets.Hyperborean),
    Rac5ArmourSet.ICE_II:        ArmourSetCheck(chestplate=ArmourSets.Hyperborean,  helmet=ArmourSets.Crystallix,   gloves=ArmourSets.Hyperborean,  boots=ArmourSets.Hyperborean),
    Rac5ArmourSet.CHAMELEON:     ArmourSetCheck(chestplate=ArmourSets.Chameleon,    helmet=ArmourSets.Chameleon,    gloves=ArmourSets.Chameleon,    boots=ArmourSets.Chameleon),
    Rac5ArmourSet.STALKER:       ArmourSetCheck(chestplate=ArmourSets.Chameleon,    helmet=ArmourSets.Wildfire,     gloves=ArmourSets.Sludge,       boots=ArmourSets.Chameleon),
}

_HYBRID_BYTE1_BITS: dict[str, int] = {
    Rac5ArmourSet.SHOCK_CRYSTAL: 0x01,
    Rac5ArmourSet.WILDBURST:     0x02,
    Rac5ArmourSet.TRIPLE_WAVE:   0x04,
    Rac5ArmourSet.ICE_II:        0x08,
    Rac5ArmourSet.STALKER:       0x10,
}

ARMOUR_SET_CHECK_MASKS: dict[str, int] = {
    name: (_HYBRID_BYTE1_BITS[name] << 8) if name in _HYBRID_BYTE1_BITS
          else check.required_mask()
    for name, check in ARMOUR_SET_CHECKS.items()
}


# Armour state (runtime)

class ArmourState(BaseState):

    def __init__(
        self,
        accessor: MemoryAccessor,
        addresses: AddressMap,
        storage: LocalStorage,
    ) -> None:
        super().__init__(accessor, addresses, storage)
        # Slot bytes store set indices (1-7), not ArmourPiece bitmask values — keep as int.
        self.equipped: dict[str, int]  = dict.fromkeys(ArmourStruct.SLOT_FIELDS, 0)
        # Stable snapshot — only updated by freeze_slots()/sync_slots()/sync().
        self._stable_slots: dict[str, int] = dict.fromkeys(ArmourStruct.SLOT_FIELDS, 0)
        self.on_slots_save: Callable[[dict[str, int]], None] = lambda _: None
        self.sets_unlocked: dict[str, bool]    = dict.fromkeys(ArmourStruct.SET_FIELDS, False)
        self.sets_bitmask: dict[str, int]      = dict.fromkeys(ArmourStruct.SET_FIELDS, 0)
        self.world_collected_armour: dict[str, int] = dict.fromkeys(ArmourStruct.SET_FIELDS, 0)
        self.ap_armour: dict[str, int]                 = dict.fromkeys(ArmourStruct.SET_FIELDS, 0)

    def load_slots(self, data: dict[str, int]) -> None:
        """Load saved slot values (e.g. from AP data storage)."""
        for name in ArmourStruct.SLOT_FIELDS:
            if name in data:
                val = int(data[name])
                self.equipped[name]      = val
                self._stable_slots[name] = val

    def push_slots_save(self) -> None:
        """Push the current equipped slots to AP data storage. Called
        explicitly (e.g. on pause-menu close) rather than on every
        poll-detected change, since that would echo back via set_notify and
        re-trigger restores."""
        self.on_slots_save(dict(self.equipped))

    def _register_handlers(self) -> None:
        self.accessor.on_struct_change(ArmourStruct, self._on_armour_change)

    def _unregister_handlers(self) -> None:
        self.accessor.remove_struct_handler(ArmourStruct, self._on_armour_change)

    def _on_armour_change(self, _address: int, new_bytes: bytes) -> None:
        instance = ArmourStruct.from_bytes(new_bytes)
        for name in ArmourStruct.SLOT_FIELDS:
            self.equipped[name] = getattr(instance, name)
        for name in ArmourStruct.SET_FIELDS:
            raw = getattr(instance, name)
            self.sets_bitmask[name]  = raw
            self.sets_unlocked[name] = bool(raw)

    def sync(self) -> None:
        instance = self.accessor.read_struct(ArmourStruct)
        for name in ArmourStruct.SLOT_FIELDS:
            raw = getattr(instance, name)
            self.equipped[name]      = raw
            self._stable_slots[name] = raw
        for name in ArmourStruct.SET_FIELDS:
            raw = getattr(instance, name)
            self.sets_bitmask[name]  = raw
            self.sets_unlocked[name] = bool(raw)

    def sync_bitmasks(self) -> None:
        """Read only the set bitmasks from memory without touching _stable_slots.

        Used in on_pickup_end so that the slot snapshot taken at pickup_start is
        preserved for restore_equipped_slots() after the detection window closes.
        """
        instance = self.accessor.read_struct(ArmourStruct)
        for name in ArmourStruct.SET_FIELDS:
            raw = getattr(instance, name)
            self.sets_bitmask[name]  = raw
            self.sets_unlocked[name] = bool(raw)

    def sync_slots(self) -> None:
        raw = self.accessor.read_raw(ArmourStruct.BASE_ADDRESS, len(ArmourStruct.SLOT_FIELDS))
        for i, name in enumerate(ArmourStruct.SLOT_FIELDS):
            self.equipped[name]      = raw[i]
            self._stable_slots[name] = raw[i]

    def freeze_slots(self) -> None:
        """Snapshot equipped into _stable_slots from the live dict, not from memory.

        Called on death so we capture the last known good state before the game
        clears armour memory as part of its death sequence.
        """
        for name in ArmourStruct.SLOT_FIELDS:
            self._stable_slots[name] = self.equipped[name]

    def restore_equipped_slots(self) -> None:
        """Write the stable slot snapshot back to memory without touching the set bytes."""
        slot_bytes = bytes(self._stable_slots[name] for name in ArmourStruct.SLOT_FIELDS)
        self.accessor.write_raw(ArmourStruct.BASE_ADDRESS, slot_bytes)

    def apply_world_armour(self) -> None:
        data = bytearray(ArmourStruct.size())
        for name in ArmourStruct.SLOT_FIELDS:
            offset = ArmourStruct.field_offset(name)
            data[offset] = self._stable_slots[name]
        for name in ArmourStruct.SET_FIELDS:
            offset = ArmourStruct.field_offset(name)
            data[offset] = self.world_collected_armour.get(name, 0)
        self.accessor.write_raw(ArmourStruct.BASE_ADDRESS, bytes(data))

    def apply_ap_armour(self) -> None:
        data = bytearray(ArmourStruct.size())
        for name in ArmourStruct.SLOT_FIELDS:
            offset = ArmourStruct.field_offset(name)
            data[offset] = self._stable_slots[name]
        for name in ArmourStruct.SET_FIELDS:
            offset = ArmourStruct.field_offset(name)
            data[offset] = self.ap_armour.get(name, 0)
        self.accessor.write_raw(ArmourStruct.BASE_ADDRESS, bytes(data))

    def clear_all_memory(self) -> None:
        self.accessor.write_raw(ArmourStruct.BASE_ADDRESS, bytes(ArmourStruct.size()))

    def add_world_armour_piece(self, set_name: str, piece: ArmourPiece) -> None:
        if set_name in self.world_collected_armour:
            self.world_collected_armour[set_name] |= int(piece)

    def add_ap_armour_piece(self, set_name: str, piece: ArmourPiece) -> None:
        if set_name in self.ap_armour:
            self.ap_armour[set_name] |= int(piece)

    def sync_from_ap(
        self,
        checked_locations: set[str],
        armour_item_pickups: set[tuple[str, ArmourPiece]] = frozenset(),
    ) -> None:
        _loc_to_flag: dict[str, tuple[str, ArmourPiece]] = {
            v: k for k, v in ARMOUR_FLAG_TO_LOCATION.items()
        }
        for key in ArmourStruct.SET_FIELDS:
            self.world_collected_armour[key] = 0
            self.ap_armour[key] = 0
        for loc_name in checked_locations:
            flag = _loc_to_flag.get(loc_name) or CHALLENGE_LOCATION_TO_ARMOUR_FLAG.get(loc_name)
            if flag:
                set_key, piece = flag
                self.world_collected_armour[set_key] |= int(piece)
        for flag in armour_item_pickups:
            if ARMOUR_FLAG_TO_LOCATION.get(flag):
                set_key, piece = flag
                self.ap_armour[set_key] |= int(piece)

    def __repr__(self) -> str:
        unlocked  = [n for n, v in self.sets_unlocked.items() if v]
        slots = {k: v for k, v in self.equipped.items() if v}
        return f"ArmourState(sets_unlocked={unlocked}, equipped_slots={slots})"


# Armour set collected state (runtime)

class ArmourSetCollectedState(BaseState):

    def __init__(
        self,
        accessor: MemoryAccessor,
        addresses: AddressMap,
        storage: LocalStorage,
    ) -> None:
        super().__init__(accessor, addresses, storage)
        self._prev:      int       = 0
        self._completed: set[str]  = set()
        self.on_location_check: Callable[[str], None] = lambda _: None

    def on_exit(self) -> None:
        self.on_location_check = lambda _: None

    def _register_handlers(self) -> None:
        self.accessor.on_struct_change(ArmourSetCollectedStruct, self._on_change)

    def _unregister_handlers(self) -> None:
        self.accessor.remove_struct_handler(ArmourSetCollectedStruct, self._on_change)

    def _on_change(self, _address: int, new_bytes: bytes) -> None:
        byte0 = new_bytes[0] if new_bytes else 0
        byte1 = new_bytes[1] if len(new_bytes) > 1 else 0
        current = byte0 | (byte1 << 8)
        if current == self._prev:
            return
        self._prev = current
        self._check(current)

    def _check(self, value: int) -> None:
        for name, mask in ARMOUR_SET_CHECK_MASKS.items():
            if name not in self._completed and (value & mask) == mask:
                self._completed.add(name)
                self.on_location_check(name)

    def sync(self) -> None:
        raw = self.accessor.read_raw(ArmourSetCollectedStruct.BASE_ADDRESS, 2)
        byte0 = raw[0] if raw else 0
        byte1 = raw[1] if len(raw) > 1 else 0
        self._prev = byte0 | (byte1 << 8)
        self._check(self._prev)

    def sync_from_ap(self, checked_locations: set[str]) -> None:
        self._completed.update(
            name for name in checked_locations if name in ARMOUR_SET_CHECK_MASKS
        )

    def __repr__(self) -> str:
        return f"ArmourSetCollectedState(prev=0x{self._prev:02X}, completed={len(self._completed)})"
