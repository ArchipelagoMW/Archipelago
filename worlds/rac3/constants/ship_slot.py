"""This module contains constants used for tracking the currently available planets in the ship menu"""


class RAC3SHIPSLOT:
    """Each planet slot in the ship menu"""
    SLOT_0 = "Planet Slot 0x00"
    SLOT_1 = "Planet Slot 0x01"
    SLOT_2 = "Planet Slot 0x02"
    SLOT_3 = "Planet Slot 0x03"
    SLOT_4 = "Planet Slot 0x04"
    SLOT_5 = "Planet Slot 0x05"
    SLOT_6 = "Planet Slot 0x06"
    SLOT_7 = "Planet Slot 0x07"
    SLOT_8 = "Planet Slot 0x08"
    SLOT_9 = "Planet Slot 0x09"
    SLOT_A = "Planet Slot 0x0A"
    SLOT_B = "Planet Slot 0x0B"
    SLOT_C = "Planet Slot 0x0C"
    SLOT_D = "Planet Slot 0x0D"
    SLOT_E = "Planet Slot 0x0E"
    SLOT_F = "Planet Slot 0x0F"
    SLOT_10 = "Planet Slot 0x10"
    SLOT_11 = "Planet Slot 0x11"
    SLOT_12 = "Planet Slot 0x12"
    SLOT_13 = "Planet Slot 0x13"


SHIP_SLOTS: list[str] = [
    RAC3SHIPSLOT.SLOT_0,
    RAC3SHIPSLOT.SLOT_1,
    RAC3SHIPSLOT.SLOT_2,
    RAC3SHIPSLOT.SLOT_3,
    RAC3SHIPSLOT.SLOT_4,
    RAC3SHIPSLOT.SLOT_5,
    RAC3SHIPSLOT.SLOT_6,
    RAC3SHIPSLOT.SLOT_7,
    RAC3SHIPSLOT.SLOT_8,
    RAC3SHIPSLOT.SLOT_9,
    RAC3SHIPSLOT.SLOT_A,
    RAC3SHIPSLOT.SLOT_B,
    RAC3SHIPSLOT.SLOT_C,
    RAC3SHIPSLOT.SLOT_D,
    RAC3SHIPSLOT.SLOT_E,
    RAC3SHIPSLOT.SLOT_F,
    RAC3SHIPSLOT.SLOT_10,
    RAC3SHIPSLOT.SLOT_11,
    RAC3SHIPSLOT.SLOT_12,
    RAC3SHIPSLOT.SLOT_13,
]
SLOT_FROM_ID: dict[int, str] = {
    0x01: RAC3SHIPSLOT.SLOT_0,
    0x02: RAC3SHIPSLOT.SLOT_1,
    0x03: RAC3SHIPSLOT.SLOT_2,
    0x04: RAC3SHIPSLOT.SLOT_3,
    0x05: RAC3SHIPSLOT.SLOT_4,
    0x06: RAC3SHIPSLOT.SLOT_5,
    0x07: RAC3SHIPSLOT.SLOT_6,
    0x08: RAC3SHIPSLOT.SLOT_7,
    0x09: RAC3SHIPSLOT.SLOT_8,
    0x0A: RAC3SHIPSLOT.SLOT_9,
    0x0B: RAC3SHIPSLOT.SLOT_A,
    0x0C: RAC3SHIPSLOT.SLOT_B,
    0x0D: RAC3SHIPSLOT.SLOT_C,
    0x0E: RAC3SHIPSLOT.SLOT_D,
    0x0F: RAC3SHIPSLOT.SLOT_E,
    0x10: RAC3SHIPSLOT.SLOT_F,
    0x11: RAC3SHIPSLOT.SLOT_10,
    0x12: RAC3SHIPSLOT.SLOT_11,
    0x13: RAC3SHIPSLOT.SLOT_12,
    0x14: RAC3SHIPSLOT.SLOT_13,
}
