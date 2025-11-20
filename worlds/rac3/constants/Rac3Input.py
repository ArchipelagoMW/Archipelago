from enum import IntFlag

class RAC3INPUT(IntFlag):
    SELECT = 0x0001
    L3 = 0x0002
    R3 = 0x0004
    START = 0x0008
    UP = 0x0010
    RIGHT = 0x0020
    DOWN = 0x0040
    LEFT = 0x0080
    L2 = 0x0100
    R2 = 0x0200
    L1 = 0x0400
    R1 = 0x0800
    TRIANGLE = 0x1000
    CIRCLE = 0x2000
    CROSS = 0x4000
    SQUARE = 0x8000