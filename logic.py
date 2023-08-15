from worlds.AutoWorld import LogicMixin

from .items import filter_item_names
from .types import ItemType, Passage

class WL4Logic(LogicMixin):
    def wl4_has_full_jewels(self, player: int, passage: Passage, count: int):
        return all(map(lambda piece: self.has(piece, player, count),
                       filter_item_names(type=ItemType.JEWEL, passage=passage)))
