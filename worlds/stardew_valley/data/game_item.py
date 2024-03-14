from dataclasses import dataclass


@dataclass(frozen=True)
class GameItem:
    name: str
    item_id: int

    def __repr__(self):
        return f"{self.name} [{self.item_id}]"

    def __lt__(self, other):
        return self.name < other.name
