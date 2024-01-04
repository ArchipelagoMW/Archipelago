from typing import Set

from worlds.AutoWorld import LogicMixin


class YuGiOh06Logic(LogicMixin):
    def yugioh06_difficulty(self, player, amount: int):
        return self.has_group("Core Booster", player, amount)

    def yugioh06_has_individual(self, items: list[str], player: int):
        amount = 0
        for item in items:
            if self.has(item, player):
                amount += 1
        return amount

