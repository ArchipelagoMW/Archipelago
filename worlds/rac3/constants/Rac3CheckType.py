from enum import Enum


class CHECKTYPE(Enum):
    """
    What memory size are we checking when reading memory:
    - BIT: a single bit, either 0 or 1
    - BYTE: 8 bits, 0x00 to 0xFF
    - SHORT: 16 bits, 2 bytes, 0x0000 to 0xFFFF
    - INT: 32 bits, 4 bytes, 0x00000000 to 0xFFFFFFFF
    What comparison is being done:
    - set or unset for individual bits
    - Equal, Not Equal, Greater Than, Less Than, Greater or Equal, Less than or Equal
    """
    BIT_SET = 0
    BIT_UNSET = 1
    BYTE_EQ = 2
    BYTE_NE = 3
    BYTE_GT = 4
    BYTE_LT = 5
    BYTE_GE = 6
    BYTE_LE = 7
    SHORT_EQ = 8
    SHORT_NE = 9
    SHORT_GT = 10
    SHORT_LT = 11
    SHORT_GE = 12
    SHORT_LE = 13
    INT_EQ = 14
    INT_NE = 15
    INT_GT = 16
    INT_LT = 17
    INT_GE = 18
    INT_LE = 19
