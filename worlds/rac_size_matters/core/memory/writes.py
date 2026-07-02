from __future__ import annotations

from ...interface import Pine
from ..armour import ArmourPiece
from ..states.game_state import GameState
from ..weapons import WeaponAddresses
from .singletons import (
    _ARMOUR_PIECES,
    _ARMOUR_SET_ORDER,
    _PIECE_TO_SLOTS,
    ARMOUR_ADDRESSES,
    GADGETS,
    PLAYER_ARMOUR_SLOTS,
    WEAPONS,
)


def zero_weapon(ipc: Pine, w: WeaponAddresses) -> None:
    ipc.write_int8(w.unlocked, 0)
    ipc.write_int8(w.mod_slot_one, 0)
    ipc.write_int8(w.mod_slot_two, 0)
    ipc.write_int8(w.mod_slot_three, 0)


def apply_tracked_armour(gs: GameState) -> None:
    for name, val in gs.tracked_armour.items():
        gs.ipc.write_int8(ARMOUR_ADDRESSES[name], val)


def apply_slots_from_armour(gs: GameState) -> None:
    slot_vals: dict[str, int] = dict.fromkeys(PLAYER_ARMOUR_SLOTS, 0)
    for set_idx, set_name in enumerate(_ARMOUR_SET_ORDER):
        val = gs.tracked_armour.get(set_name, 0)
        if not val:
            continue
        slot_value = set_idx + 1
        for piece in _ARMOUR_PIECES:
            if piece in ArmourPiece(val):
                for slot in _PIECE_TO_SLOTS[piece]:
                    slot_vals[slot] = slot_value
    for slot, v in slot_vals.items():
        gs.ipc.write_int8(PLAYER_ARMOUR_SLOTS[slot], v)


def apply_tracked_weapons(gs: GameState) -> None:
    for name, val in gs.tracked_weapons.items():
        if name in WEAPONS:
            gs.ipc.write_int8(WEAPONS[name].unlocked, val)
    for name, val in gs.tracked_gadgets.items():
        if name in GADGETS:
            gs.ipc.write_int8(GADGETS[name].unlocked, val)


def restore_tracked_weapon_state(gs: GameState) -> None:
    for w in WEAPONS.values():
        zero_weapon(gs.ipc, w)
    for g in GADGETS.values():
        gs.ipc.write_int8(g.unlocked, 0)
    for name, val in gs.tracked_weapons.items():
        if name in WEAPONS:
            gs.ipc.write_int8(WEAPONS[name].unlocked, val)
    for name, slots in gs.tracked_mods.items():
        if name in WEAPONS:
            for slot in slots:
                gs.ipc.write_int8(getattr(WEAPONS[name], f"mod_slot_{slot}"), 1)
    for name, val in gs.tracked_gadgets.items():
        if name in GADGETS:
            gs.ipc.write_int8(GADGETS[name].unlocked, val)
