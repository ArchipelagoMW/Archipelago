class Wargroove2LogicFilter:
    items: [str]

    def __init__(self, items: [str]):
        self.items = items

    def has(self, item: str, player: int) -> bool:
        return item in self.items

    def has_all(self, items: [str], player: int) -> bool:
        for item in items:
            if item not in self.items:
                return False
        return True

    def has_any(self, items: [str], player: int) -> bool:
        for item in items:
            if item in self.items:
                return True
        return False

    def can_reach(self, region, kind, player: int) -> bool:
        return True
