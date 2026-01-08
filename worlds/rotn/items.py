from typing import NamedTuple, Optional, List
from BaseClasses import Item, ItemClassification

class SongData(NamedTuple):
    code: Optional[int]
    song_name: str
    DLC: str
    diff_easy: int
    diff_medium: int
    diff_hard: int
    diff_impossible: int
    type: str = "Rift"

class ExtraSongData(NamedTuple):
    code: Optional[int]
    DLC: str
    diff: int

class RotNSongItem(Item):
    game: str = "Rift of the Necrodancer"

    def __init__(self, name: str, player: int, data: SongData) -> None:
        super().__init__(name, ItemClassification.progression, data.code, player)

class RotNFixedItem(Item):
    game: str = "Rift of the Necrodancer"

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int) -> None:
        super().__init__(name, classification, code, player)