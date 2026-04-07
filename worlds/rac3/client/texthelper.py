"""This module contains functions for processing the message displayed when sending items"""

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification
from NetUtils import NetworkItem
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.messages.text_strings import RAC3TEXTFORMATSTRING

if TYPE_CHECKING:
    from worlds.rac3.client.client import Rac3Context


def colorize_item_name(item_name: str, item_flags: int) -> str:
    """Function to colorize the item name"""
    color = RAC3TEXTFORMATSTRING.WHITE  # Filler / Trap = White
    if item_flags & ItemClassification.progression:
        color = RAC3TEXTFORMATSTRING.MAGENTA  # Progression = Magenta
    elif item_flags & ItemClassification.useful:
        color = RAC3TEXTFORMATSTRING.BLUE  # Useful = Blue
    return f"{color}{item_name}{RAC3TEXTFORMATSTRING.NORMAL}"


def get_sent_item_message(ctx: "Rac3Context", net_item: NetworkItem, player_name_after: bool = False) -> str:
    """Returns the pop-up message to be displayed in game, given the item just collected"""
    item_name = colorize_item_name(ctx.item_names.lookup_in_slot(net_item.item, net_item.player), net_item.flags)
    location_name = ctx.location_names.lookup_in_slot(net_item.location, net_item.player)

    if ctx.slot == net_item.player:
        # Item is ours, no need to specify player name
        return f"Found {item_name} at {location_name}"
    # Item belongs to someone else, give their name
    player_name = ctx.player_names.get(net_item.player, "???")
    if player_name_after:
        return f"Sent {item_name} to {RAC3TEXTFORMATSTRING.GREEN}{player_name}"
    return f"Sent {player_name}'s {item_name}"

TEXT_BYTE_TO_EXPECTED_WIDTH = {
    0x00: 0,  # Null terminator
    0x01: 0,  # Newline
    0x02: 0,  # Carriage return
    0x03: 0,  # Tab
    0x04: 0,  # Backspace
    0x05: 0,  # Form feed
    0x06: 0,  # Vertical tab
    0x07: 0,  # Bell
    0x08: 0,  # Default Text Color Byte
    0x09: 0,  # Blue Color Byte
    0x0A: 0,  # Green Color Byte
    0x0B: 0,  # Magenta Color Byte
    0x0C: 0,  # White Color Byte
    0x0D: 0,  # Black Color Byte
    0x0E: 0,  # Unused Color Byte 1
    0x0F: 0,  # Unused Color Byte 2
    0x10: 32,  # Cross
    0x11: 32,  # Circle
    0x12: 32,  # Triangle
    0x13: 32,  # Square
    0x14: 32,  # L1
    0x15: 32,  # R1
    0x16: 32,  # L2
    0x17: 32,  # R2
    0x18: 32,  # L3
    0x19: 32,  # R3
    0x1A: 32,  # Select
    0x1B: 0,  # Nothing
    0x1C: 0,  # Nothing
    0x1D: 0,  # Nothing
    0x1E: 0,  # Nothing
    0x1F: 0,  # Nothing
    0x20: 4,  # Space
    0x21: 3,  # ! (thin)
    0x22: 6,  # "
    0x23: 8,  # #
    0x24: 8,  # $
    0x25: 9,  # %
    0x26: 9,  # &
    0x27: 4,  # ' (thin)
    0x28: 6,  # (
    0x29: 6,  # )
    0x2A: 7,  # *
    0x2B: 8,  # +
    0x2C: 3,  # , (thin)
    0x2D: 4,  # -
    0x2E: 3,  # . (thin)
    0x2F: 6,  # /
    0x30: 10,  # 0 (monospace)
    0x31: 10,  # 1 (monospace)
    0x32: 10,  # 2 (monospace)
    0x33: 10,  # 3 (monospace)
    0x34: 10,  # 4 (monospace)
    0x35: 10,  # 5 (monospace)
    0x36: 10,  # 6 (monospace)
    0x37: 10,  # 7 (monospace)
    0x38: 10,  # 8 (monospace)
    0x39: 10,  # 9 (monospace)
    0x3A: 3,  # : (thin)
    0x3B: 3,  # ; (thin)
    0x3C: 8,  # <
    0x3D: 8,  # =
    0x3E: 8,  # >
    0x3F: 8,  # ?
    0x40: 11,  # @ (wide)
    0x41: 11,  # A
    0x42: 9,  # B
    0x43: 9,  # C
    0x44: 10,  # D
    0x45: 8,  # E
    0x46: 8,  # F
    0x47: 10,  # G
    0x48: 9,  # H
    0x49: 3,  # I (thin)
    0x4A: 8,  # J
    0x4B: 10,  # K
    0x4C: 8,  # L
    0x4D: 12,  # M (wide)
    0x4E: 10,  # N
    0x4F: 10,  # O (wide)
    0x50: 9,  # P
    0x51: 11,  # Q (wide)
    0x52: 9,  # R
    0x53: 9,  # S
    0x54: 9,  # T
    0x55: 9,  # U
    0x56: 11,  # V
    0x57: 14,  # W (wide)
    0x58: 11,  # X
    0x59: 11,  # Y
    0x5A: 9,  # Z
    0x5B: 4,  # [
    0x5C: 6,  # \
    0x5D: 4,  # ]
    0x5E: 8,  # ^
    0x5F: 8,  # _
    0x60: 5,  # ` (thin)
    0x61: 8,  # a
    0x62: 8,  # b
    0x63: 8,  # c
    0x64: 8,  # d
    0x65: 8,  # e
    0x66: 6,  # f (thin)
    0x67: 8,  # g
    0x68: 8,  # h
    0x69: 3,  # i (thin)
    0x6A: 3,  # j (thin)
    0x6B: 8,  # k
    0x6C: 3,  # l (thin)
    0x6D: 12,  # m (wide)
    0x6E: 8,  # n
    0x6F: 8,  # o
    0x70: 8,  # p
    0x71: 8,  # q
    0x72: 7,  # r (thin)
    0x73: 8,  # s
    0x74: 7,  # t (thin)
    0x75: 8,  # u
    0x76: 8,  # v
    0x77: 12,  # w (wide)
    0x78: 8,  # x
    0x79: 8,  # y
    0x7A: 8,  # z
    0x7B: 4,  # {
    0x7C: 3,  # | (thin)
    0x7D: 4,  # }
    0x7E: 8,  # ~
    0x7F: 0,  # DEL
}

ITEM_TO_STRING_TABLE_INDEX_OFFSET: dict[str, int] = {
    RAC3ITEM.SHOCK_BLASTER: 0x0910,
    RAC3ITEM.NITRO_LAUNCHER: 0x0570,
    RAC3ITEM.PLASMA_WHIP: 0x09B0,
    RAC3ITEM.N60_STORM: 0x0520,
    RAC3ITEM.INFECTOR: 0x0960,
    RAC3ITEM.SUCK_CANNON: 0x08C0,
    RAC3ITEM.SPITTING_HYDRA: 0x0820,
    RAC3ITEM.AGENTS_OF_DOOM: 0x0870,
    RAC3ITEM.FLUX_RIFLE: 0x0A50,
    RAC3ITEM.LAVA_GUN: 0x02D0,
    RAC3ITEM.MINI_TURRET: 0x0330,
    RAC3ITEM.ANNIHILATOR: 0x0AA0,
    RAC3ITEM.HOLO_SHIELD: 0x07D0,
    RAC3ITEM.DISC_BLADE: 0x05C0,
    RAC3ITEM.RIFT_INDUCER: 0x0A00,
    RAC3ITEM.QWACK_O_RAY: 0x0730,
    RAC3ITEM.BOUNCER: 0x04C0,
    RAC3ITEM.PLASMA_COIL: 0x0390,
    RAC3ITEM.SHIELD_CHARGER: 0x03F0,
    RAC3ITEM.RY3N0: 0x0780,
    RAC3ITEM.MAGNAPLATE: 0x12B0,
    RAC3ITEM.ADAMANTINE: 0x12C0,
    RAC3ITEM.AEGIS: 0x12D0,
    RAC3ITEM.INFERNOX: 0x12E0,
}

ITEM_TO_ORIGINAL_STRING_POINTER_OFFSET: dict[str, int] = {
    RAC3ITEM.SHOCK_BLASTER: 0x07E0,
    RAC3ITEM.NITRO_LAUNCHER: 0x0442,
    RAC3ITEM.PLASMA_WHIP: 0x0868,
    RAC3ITEM.N60_STORM: 0x0403,
    RAC3ITEM.INFECTOR: 0x082E,
    RAC3ITEM.SUCK_CANNON: 0x0799,
    RAC3ITEM.SPITTING_HYDRA: 0x06F7,
    RAC3ITEM.AGENTS_OF_DOOM: 0x0744,
    RAC3ITEM.FLUX_RIFLE: 0x08F7,
    RAC3ITEM.ANNIHILATOR: 0x093B,
    RAC3ITEM.HOLO_SHIELD: 0x0691,
    RAC3ITEM.DISC_BLADE: 0x0495,
    RAC3ITEM.RIFT_INDUCER: 0x08AE,
    RAC3ITEM.QWACK_O_RAY: 0x061B,
    RAC3ITEM.LAVA_GUN: 0x01F8,
    RAC3ITEM.MINI_TURRET: 0x097E,
    RAC3ITEM.BOUNCER: 0x03BE,
    RAC3ITEM.PLASMA_COIL: 0x02C8,
    RAC3ITEM.SHIELD_CHARGER: 0x030F,
    RAC3ITEM.RY3N0: 0x0664,
    RAC3ITEM.MAGNAPLATE: 0x11DE,
    RAC3ITEM.ADAMANTINE: 0x11EF,
    RAC3ITEM.AEGIS: 0x1200,
    RAC3ITEM.INFERNOX: 0x1213,
}
