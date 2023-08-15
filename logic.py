from worlds.AutoWorld import LogicMixin

from .names import JewelPieces

class WL4Logic(LogicMixin):
    def wl4_has_full_jewels(self, player: int, jewel: JewelPieces, count: int):
        return all(self.has(piece, player, count) for piece in jewel)
