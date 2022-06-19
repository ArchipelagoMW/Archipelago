from BaseClasses import Item
from zilliandomizer.options import Chars
from zilliandomizer.logic_components.items import Item as ZzItem

from .id_maps import item_id_to_zz_item


class ZillionItem(Item):
    game = "Zillion"
    zz_item: ZzItem

    def __init__(self, name: str, advancement: bool, code: int, player: int, start_char: Chars) -> None:
        super().__init__(name, advancement, code, player)
        self.zz_item = item_id_to_zz_item[code]
        self._hint_text = self.zz_item.name
        if self._hint_text == start_char:
            self._hint_text = "JJ"

        # TODO: unit test to make sure jj hint text gets changed
