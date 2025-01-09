from typing import Set


class Wargroove2LogicFilter:
    items: set[str]

    def __init__(self, items: Set[str]):
        self.items = items

    def has(self, item: str, player: int) -> bool:
        return item in self.items

    def has_all(self, items: Set[str], player: int) -> bool:
        for item in items:
            if item not in self.items:
                return False
        return True

    def has_any(self, items: Set[str], player: int) -> bool:
        for item in items:
            if item in self.items:
                return True
        return False
