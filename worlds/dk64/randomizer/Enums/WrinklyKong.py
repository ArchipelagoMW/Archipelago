"""Hint enums for kong type and locations."""

from enum import IntEnum, auto


class WrinklyKong(IntEnum):
    """Kong for wrinkly to assign to.

    Args:
        IntEnum (int): Enum of the kong.
    """

    ftt = auto()
    dk = auto()
    diddy = auto()
    tiny = auto()
    lanky = auto()
    chunky = auto()


class WrinklyLocation(IntEnum):
    """Lobby location of the wrinkly hint.

    Args:
        IntEnum (int): Enum of the location.
    """

    ftt = auto()
    japes = auto()
    aztec = auto()
    factory = auto()
    galleon = auto()
    fungi = auto()
    caves = auto()
    castle = auto()
