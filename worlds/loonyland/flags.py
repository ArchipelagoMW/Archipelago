from enum import Flag, auto


class LLFlags(Flag):
    NONE = 0
    PWR = auto()
    PWR_BIG = auto()
    PWR_MAX = auto()
    OP = auto()

    TORCH = auto()

    DOLL = auto()
    LONG = auto()
    LONG_VANILLA_BADGES = auto()
    MULTISAVE = auto()
    POSTGAME = auto()
    VANILLA_POSTGAME = auto()

    MODE = auto()
    REMIX = auto()
