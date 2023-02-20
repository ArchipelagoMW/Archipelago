from dataclasses import dataclass
from typing import Tuple, FrozenSet


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


@dataclass(frozen=True)
class MuseumItem(GameItem):
    locations: FrozenSet[str]
    geodes: FrozenSet[str]
    monsters: FrozenSet[str]
    difficulty: float

    def __repr__(self):
        return f"{self.name} [{self.item_id}] (Locations: {self.locations} |" \
               f" Geodes: {self.geodes} |" \
               f" Monsters: {self.monsters}) "


@dataclass(frozen=True)
class Villager:
    name: str
    bachelor: bool
    locations: FrozenSet[str]
    birthday: str
    gifts: FrozenSet[str]
    available: bool

    def __repr__(self):
        return f"{self.name} [Bachelor: {self.bachelor}] [Available from start: {self.available}]" \
               f"(Locations: {self.locations} |" \
               f" Birthday: {self.birthday} |" \
               f" Gifts: {self.gifts}) "
