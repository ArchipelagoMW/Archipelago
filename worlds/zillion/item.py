from typing import Dict
from BaseClasses import Item
from zilliandomizer.options import Chars
from zilliandomizer.logic_components.items import Item as ZzItem, id_to_item
from .config import base_id


item_id_to_zz_item: Dict[int, ZzItem] = {
    i + base_id: item
    for i, item in id_to_item.items()
}

item_name_to_id = {
    z.debug_name: i
    for i, z in item_id_to_zz_item.items()
}


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
