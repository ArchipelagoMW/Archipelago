"""
Aria of Sorrow live-memory map (EWRAM) for the BizHawk client.

All offsets here are **EWRAM-domain offsets** — the GBA address minus the EWRAM
base ``0x02000000`` — which is the form BizHawk's ``"EWRAM"`` memory domain expects
(the same convention the cvhodis client uses). The full GBA address is shown in a
comment beside each constant.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

# --- Memory/BizHawk address-section names ---
EWRAM = "EWRAM"

EWRAM_BASE = 0x02000000


# --- Game state / "safe to act" gating ---
GAME_STATE = 0x00010      # 0x02000010 u8
MENU_STATE = 0x00064      # 0x02000064 u8


class GameState(IntEnum):
    KONAMI_LOGO = 0x00
    TITLE = 0x01
    GAME_START = 0x02
    INGAME = 0x04
    GAME_OVER = 0x05
    CREDITS = 0x06


MENU_STATE_NORMAL = 0x01            # in-room, not transitioning/paused/shopping
MENU_STATE_ROOM_TRANSITION = 0x03
MENU_STATE_PAUSE = 0x06
MENU_STATE_SHOP = 0x09


# --- Location detection: collected-pickup save flags ---
PICKUP_FLAGS = 0x00360             # 0x02000360, 20 bytes / 160 bits
PICKUP_FLAGS_LEN = 0x14


# --- Progress / goal flags ---
EVENT_FLAGS = 0x0033C              # 0x0200033C - For Phase 6 (autotracking)
BOSS_FLAGS = 0x0037E               # 0x0200037E u16
GLOBAL_FLAGS = 0x0042C             # 0x0200042C u32
CURRENT_AREA = 0x0009E             # 0x0200009E u8 - For Phase 6 (area-aware DeathLink)
CURRENT_ROOM = 0x0009F             # 0x0200009F u8
CURRENT_SAVE_SLOT = 0x00428        # 0x02000428 u8

BOSS_FLAG_GRAHAM = 0x0001          # bad-ending final boss
BOSS_FLAG_DEATH = 0x0002
BOSS_FLAG_CHAOS = 0x0080           # true-ending final boss, fallback if global doesn't work
GLOBAL_FLAG_GOOD_ENDING = 0x00004000


# --- Player inventory / stats block ---
EQUIPPED_WEAPON = 0x13268          # 0x02013268 u8
EQUIPPED_RED_SOUL = 0x13269        # ...
EQUIPPED_BLUE_SOUL = 0x1326A       # ...
EQUIPPED_YELLOW_SOUL = 0x1326B     # ...
EQUIPPED_ARMOR = 0x1326C           # ...
EQUIPPED_ACCESSORY = 0x1326D       # ...
CURRENT_HP = 0x1327A               # 0x0201327A s16
CURRENT_MP = 0x1327C               # 0x0201327C s16
MAX_HP = 0x1327E                   # 0x0201327E u16
MAX_MP = 0x13280                   # 0x02013280 u16
CURRENT_GOLD = 0x13290             # 0x02013290 u32

AP_RECEIVED_COUNT = 0x1328A        # 0x0201328A u16 (pad_1328A: verified-dead, saved, zeroed-on-new-game)


@dataclass(frozen=True)
class InventoryArray:
    """
    One of AoS's owned-item count arrays. Each slot holds the quantity owned.

    Byte arrays store one count per byte. Soul arrays nibble-pack two souls per
    byte (low nibble = even index, high nibble = odd). ``base`` points at the
    primary list. Souls also have an unused secondary list, which we ignore.
    """

    name: str
    base: int
    length: int          # number of items the array can address
    nibble_packed: bool


# Keyed by item_info category string (worlds/cvaos/data/item_info) so callers can
# route a received item straight from its item_info.

# Layout: (category, base offset, number of items, nibble-packed)
INVENTORY: dict[str, InventoryArray] = {
    "consumable":   InventoryArray("consumable",   0x13294, 0x20, False),
    "weapon":       InventoryArray("weapon",       0x132B4, 0x3B, False),
    "armor":        InventoryArray("armor",        0x132EF, 0x19, False),
    "accessory":    InventoryArray("accessory",    0x13308, 0x14, False),
    "red_soul":     InventoryArray("red_soul",     0x1331C, 56,   True),
    "blue_soul":    InventoryArray("blue_soul",    0x13354, 26,   True),
    "yellow_soul":  InventoryArray("yellow_soul",  0x1336E, 36,   True),
    "ability_soul": InventoryArray("ability_soul", 0x13392, 6,    True),
}
# Money (subtype 1) is not an inventory array — it adds to CURRENT_GOLD.
