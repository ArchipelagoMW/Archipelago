from enum import IntEnum


class Area(IntEnum):
    BRINSTAR = 0
    KRAID = 1
    NORFAIR = 2
    RIDLEY = 3
    TOURIAN = 4
    CRATERIA = 5
    CHOZODIA = 6


class Event(IntEnum):
    ACID_WORM_KILLED = 0x1C
    KRAID_KILLED = 0x1E
    IMAGO_COCOON_KILLED = 0x22
    IMAGO_KILLED = 0x23
    RIDLEY_KILLED = 0x25
    MOTHER_BRAIN_KILLED = 0x27
    ESCAPED_ZEBES = 0x41
    MECHA_RIDLEY_KILLED = 0x4A
    ESCAPED_CHOZODIA = 0x4B
    DEOREM_KILLED = 0x4F
    RUINS_TEST_PASSED = 0x50
    METROID_DNA_ACQUIRED = 0x51

    def block_number(self) -> int:
        return self // 32

    def bit_number(self) -> int:
        return self & 31

    def bit_mask(self) -> int:
        return 1 << self.bit_number()


class ItemType(IntEnum):
    NONE = 0
    ENERGY_TANK = 1
    MISSILE_TANK = 2
    SUPER_MISSILE_TANK = 3
    POWER_BOMB_TANK = 4
    BEAM = 5
    MAJOR = 6
    CUSTOM = 7
    METROID_DNA = 8


PIXEL_SIZE = 4


RC_COUNT = 101
