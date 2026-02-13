from enum import Enum


class LineType(Enum):
    BLANK = 0
    BLUE = 1
    RED = 2
    WHITE1 = 3
    WHITE2 = 4
    COPYRIGHT1 = 5
    COPYRIGHT2 = 6
    COPYRIGHT3 = 7
    COPYRIGHT4 = 8
    END = 9


LINE_TYPE_VALS = {
    LineType.BLANK: 0x5,
    LineType.BLUE: 0x0,
    LineType.RED: 0x1,
    LineType.WHITE1: 0x3,
    LineType.WHITE2: 0x2,
    LineType.COPYRIGHT1: 0xA,
    LineType.COPYRIGHT2: 0xB,
    LineType.COPYRIGHT3: 0xC,
    LineType.COPYRIGHT4: 0xD,
    LineType.END: 0x6,
}

LINE_TYPE_HEIGHTS = {
    LineType.BLANK: 1,
    LineType.BLUE: 1,
    LineType.RED: 1,
    LineType.WHITE1: 1,
    LineType.WHITE2: 2,
    LineType.COPYRIGHT1: 1,
    LineType.COPYRIGHT2: 1,
    LineType.COPYRIGHT3: 1,
    LineType.COPYRIGHT4: 1,
    LineType.END: 0,
}

TEXT_LINE_TYPES = {LineType.BLUE, LineType.RED, LineType.WHITE1, LineType.WHITE2}
