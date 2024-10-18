import json


class Balance:

    def __init__(self, ancientCoins: int = 0, dabloons: int = 0, gold: int = 0):
        self.ancient_coins = ancientCoins
        self.dabloons = dabloons
        self.gold = gold

    def __sub__(self, other):
        ac = self.ancient_coins - other.ancient_coins
        db = self.dabloons - other.dabloons
        g = self.gold - other.gold
        return Balance(ac, db, g)

    def __add__(self, other):
        ac = self.ancient_coins + other.ancient_coins
        db = self.dabloons + other.dabloons
        g = self.gold + other.gold
        return Balance(ac, db, g)

    def isInDebt(self) -> bool:
        if self.ancient_coins < 0 or self.dabloons < 0 or self.gold < 0:
            return True
        return False

    def displayString(self) -> str:
        return "Gold: {} Dabloons: {} AncientCoins: {}".format(self.gold, self.dabloons, self.ancient_coins)


def fromJson(js: json) -> Balance:
    return Balance(js["ancientCoins"], js["doubloons"], js["gold"])
