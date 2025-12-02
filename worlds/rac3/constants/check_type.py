from enum import IntFlag


class CHECKTYPE(IntFlag):
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
    BIT = 0b00000001
    BYTE = 0b00000010
    SHORT = 0b00000100
    INT = 0b00001000
    EQ = 0b00010000
    NEQ = 0b00100000
    GT = 0b01000000
    LT = 0b10000000
    GE = GT | EQ
    LE = LT | EQ

    BYTE_EQ = BYTE | EQ
    BYTE_NE = BYTE | NEQ
    BYTE_GT = BYTE | GT
    BYTE_LT = BYTE | LT
    BYTE_GE = BYTE | GE
    BYTE_LE = BYTE | LE
    SHORT_EQ = SHORT | EQ
    SHORT_NE = SHORT | NEQ
    SHORT_GT = SHORT | GT
    SHORT_LT = SHORT | LT
    SHORT_GE = SHORT | GE
    SHORT_LE = SHORT | LE
    INT_EQ = INT | EQ
    INT_NE = INT | NEQ
    INT_GT = INT | GT
    INT_LT = INT | LT
    INT_GE = INT | GE
    INT_LE = INT | LE

    SIZE = BIT | BYTE | SHORT | INT
    SIGN = EQ | NEQ | GT | LT
