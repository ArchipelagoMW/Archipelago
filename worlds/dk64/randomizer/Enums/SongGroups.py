"""Enum for Song Groups."""

from enum import IntEnum, auto


class SongGroup(IntEnum):
    """Enum data for what group of song you are playing.

    Args:
            IntEnum (int): Enum of the song.
    """

    Fight = auto()
    LobbyShop = auto()
    Interiors = auto()
    Exteriors = auto()
    Minigames = auto()
    Happy = auto()
    Gloomy = auto()
    Calm = auto()
    Spawning = auto()
    Collection = auto()
