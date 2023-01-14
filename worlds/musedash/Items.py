from typing import Dict, NamedTuple, Optional, Union
from BaseClasses import Item, ItemClassification

"""
The data for each song. Contains the value of each difficulty to make filtering per-difficulty easier.
Note: -1 means difficulty missing. -2 means "?" difficulty
"""
class SongData(NamedTuple):
    code: Optional[int]
    default_song: bool
    streamer_mode: bool
    easy: str = Optional[int]
    hard: int = Optional[int]
    master: int = Optional[int]
    secret: int = Optional[int] #Note: Secret diffs can be Harder, but it can also just be "different". (See Heracles and Super Battleworm Insomniac for "different")

"""
The data for each album.
"""
class AlbumData(NamedTuple):
    code: Optional[int]

class MuseDashItem(Item):
    game: str = "Muse Dash"

    def __init__(self, name: str, player: int, data: Union[SongData, AlbumData]) -> None:
        super().__init__(name, ItemClassification.progression, data.code, player) #Todo: Should these be skip balancing?

class MuseDashFixedItem(Item):
    game: str = "Muse Dash"
    def __init__(self, name: str, classification: ItemClassification, player: int, code: Optional[int]) -> None:
        super().__init__(name, classification, code, player)
