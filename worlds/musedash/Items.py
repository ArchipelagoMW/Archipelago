from typing import NamedTuple, Optional, Union
from BaseClasses import Item, ItemClassification


class SongData(NamedTuple):
    """Special data container to contain the metadata of each song to make filtering work."""

    code: Optional[int]
    album: str
    streamer_mode: bool
    easy: Optional[int]
    hard: Optional[int]
    master: Optional[int]


class AlbumData(NamedTuple):
    """Special data container to contain the metadata of each album to make filtering work. Currently not used."""

    code: Optional[int]


class MuseDashSongItem(Item):
    game: str = "Muse Dash"

    def __init__(self, name: str, player: int, data: Union[SongData, AlbumData]) -> None:
        super().__init__(name, ItemClassification.progression, data.code, player)


class MuseDashFixedItem(Item):
    game: str = "Muse Dash"

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int) -> None:
        super().__init__(name, classification, code, player)
