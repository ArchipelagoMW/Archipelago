from dataclasses import dataclass


@dataclass(frozen=True)
class GameItem:
    name: str
    item_id: int

    def __repr__(self):
        return f"{self.name} [{self.item_id}]"


@dataclass(frozen=True)
class FishItem(GameItem):
    locations: frozenset[str]
    seasons: frozenset[str]
    difficulty: int

    def __repr__(self):
        return f"{self.name} [{self.item_id}] (Locations: {self.locations} |" \
               f" Seasons: {self.seasons} |" \
               f" Difficulty: {self.difficulty}) "
