from worlds.AutoWorld import LogicMixin


class YuGiOh06Logic(LogicMixin):
    def yugioh06_difficulty(self, player, amount: int):
        return self.has_group("Core Booster", player, amount)
