"""
Encoding and granting received items for the Aria of Sorrow BizHawk client.

Every cvaos AP item code is a packed integer. ``pack`` builds one at generation time
(worlds/cvaos/items.py); ``resolve`` unpacks a received code into a ``ReceiveAction``, and
``grant`` performs it through the RAM accessors. This module owns the wire encoding and is the
single place that knows how an incoming item becomes a game-state change.

Bit layout (MSB->LSB, 53 bits — AP requires ``0 < id < 2**53`` for JS clients):

    [52:49] category   (4)  TransferCategory; 0 reserved so every code is > 0
    [48]    set_flag   (1)  also set an EWRAM flag bit?
    [47:40] unused     (8)  reserved for growth
    [39:28] id/value  (12)  item -> item_info.item_number; money -> gold value
    [27:22] disambig   (6)  copy index — distinguishes multiple pickups of the same item so
                            their codes stay unique; ignored when granting
    [21:4]  flag off  (18)  EWRAM byte offset (when set_flag)
    [3:1]   flag bit   (3)  bit index 0-7 (when set_flag)
    [0]     flag value (1)  value to set that bit to (when set_flag)

Extending later: ``other_item`` already routes like ``pickup``; ``event``/``to_be_implemented``
are reserved (``grant`` logs + skips them). Maps will set their reveal flag via ``set_flag``
once the offsets are known (see the TODO in items.py).
"""
from __future__ import annotations

from enum import IntEnum
from typing import NamedTuple, TYPE_CHECKING

from .data.item_info import by_item_number as _by_item_number

if TYPE_CHECKING:
    from .ram import AoSRAM


class TransferCategory(IntEnum):
    # 0 is reserved (unused) so that category, sitting in the high bits, keeps every code > 0.
    PICKUP = 1             # id = item_info.item_number -> give_item
    OTHER_ITEM = 2         # id = item_info.item_number -> give_item (item with no ground pickup)
    MONEY = 3              # id = gold value -> add_gold
    EVENT = 4              # reserved
    TO_BE_IMPLEMENTED = 5  # reserved


# --- bit layout (shifts + masks) ---
_CATEGORY_SHIFT, _CATEGORY_MASK = 49, 0xF
_SET_FLAG_SHIFT = 48
_ID_SHIFT, _ID_MASK = 28, 0xFFF            # 12 bits
_DISAMBIG_SHIFT, _DISAMBIG_MASK = 22, 0x3F  # 6 bits
_FLAG_OFFSET_SHIFT, _FLAG_OFFSET_MASK = 4, 0x3FFFF  # 18 bits (256 KB EWRAM)
_FLAG_BIT_SHIFT, _FLAG_BIT_MASK = 1, 0x7    # 3 bits
_FLAG_VALUE_MASK = 0x1

ID_MAX = _ID_MASK            # 4095  — largest packable item_number / gold value
DISAMBIG_MAX = _DISAMBIG_MASK  # 63   — most copies of one item that can share an (id) space


def pack(category: TransferCategory, id_or_value: int, *, disambiguation: int = 0,
         set_flag: bool = False, flag_offset: int = 0, flag_bit: int = 0, flag_value: int = 0) -> int:
    """Build a packed AP item code, raising if any field overflows its width."""
    if not 0 <= id_or_value <= _ID_MASK:
        raise ValueError(f"id/value {id_or_value} does not fit in 12 bits")
    if not 0 <= disambiguation <= _DISAMBIG_MASK:
        raise ValueError(f"disambiguation {disambiguation} does not fit in 6 bits")
    if not 0 <= flag_offset <= _FLAG_OFFSET_MASK:
        raise ValueError(f"flag_offset {flag_offset:#x} does not fit in 18 bits")
    if not 0 <= flag_bit <= _FLAG_BIT_MASK:
        raise ValueError(f"flag_bit {flag_bit} does not fit in 3 bits")
    return (
        (int(category) << _CATEGORY_SHIFT)
        | (int(bool(set_flag)) << _SET_FLAG_SHIFT)
        | (id_or_value << _ID_SHIFT)
        | (disambiguation << _DISAMBIG_SHIFT)
        | (flag_offset << _FLAG_OFFSET_SHIFT)
        | (flag_bit << _FLAG_BIT_SHIFT)
        | (flag_value & _FLAG_VALUE_MASK)
    )


class ReceiveAction(NamedTuple):
    category: TransferCategory
    id_or_value: int    # item -> item_info.item_number; money -> gold value
    set_flag: bool
    flag_offset: int
    flag_bit: int
    flag_value: int


def resolve(code: int) -> "ReceiveAction | None":
    """Unpack a received AP code. Returns ``None`` for an undefined category (the caller should
    log + skip). The disambiguation field is intentionally dropped — it never affects the grant.
    """
    try:
        category = TransferCategory((code >> _CATEGORY_SHIFT) & _CATEGORY_MASK)
    except ValueError:
        return None
    return ReceiveAction(
        category=category,
        id_or_value=(code >> _ID_SHIFT) & _ID_MASK,
        set_flag=bool((code >> _SET_FLAG_SHIFT) & 1),
        flag_offset=(code >> _FLAG_OFFSET_SHIFT) & _FLAG_OFFSET_MASK,
        flag_bit=(code >> _FLAG_BIT_SHIFT) & _FLAG_BIT_MASK,
        flag_value=code & _FLAG_VALUE_MASK,
    )


async def grant(ram: "AoSRAM", action: ReceiveAction) -> bool:
    """Apply a resolved action through the RAM accessors. Returns ``False`` only if a guarded
    write lost a race, so the caller retries next tick without advancing the received-counter.
    """
    # ORDER MATTERS: run the idempotent op (set_flag_bit -- a no-op when the bit is already at the
    # target value) FIRST, and the non-idempotent transfer (give_item/add_gold, a real increment)
    # LAST, so on a retry only the last committed op can re-run. If the flag write loses its guarded
    # race we return before any transfer (clean retry); if the transfer loses its race, re-setting the
    # flag next tick is harmless. This preserves "at most one non-idempotent op per grant" and becomes
    # load-bearing once maps pack set_flag=1 (TODO in items.py) -- do not reorder back.
    if action.set_flag:
        if not await ram.set_flag_bit(action.flag_offset, action.flag_bit, action.flag_value):
            return False
    return await _grant_transfer(ram, action)


async def _grant_transfer(ram: "AoSRAM", action: ReceiveAction) -> bool:
    category = action.category
    if category == TransferCategory.MONEY:
        return await ram.add_gold(action.id_or_value)
    if category in (TransferCategory.PICKUP, TransferCategory.OTHER_ITEM):
        info = _by_item_number[action.id_or_value]
        return await ram.give_item(info.item_category, info.id)
    # EVENT / TO_BE_IMPLEMENTED: reserved, not yet grantable. Skip loudly (never silently).
    from CommonClient import logger
    logger.warning("CVAoS: received reserved category %s; skipping.", category.name)
    return True
