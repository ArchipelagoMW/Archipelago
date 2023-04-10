from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class GameItem:
    name: str
    item_id: int

    def __repr__(self):
        return f"{self.name} [{self.item_id}]"

    def __lt__(self, other):
        return self.name < other.name


@dataclass(frozen=True)
class FishItem(GameItem):
    locations: Tuple[str]
    seasons: Tuple[str]
    difficulty: int

    def __repr__(self):
        return f"{self.name} [{self.item_id}] (Locations: {self.locations} |" \
               f" Seasons: {self.seasons} |" \
               f" Difficulty: {self.difficulty}) "
