from BaseClasses import Item
from zilliandomizer.options import Chars
from zilliandomizer.logic_components.items import Item as ZzItem, items as zz_items, MAIN_ITEM
from .config import base_id


item_id_to_zz_item = {
    i: item
    for i, item in enumerate(zz_items + [MAIN_ITEM], base_id)
}

item_name_to_id = {
    z.debug_name: i
    for i, z in item_id_to_zz_item.items()
}

# TODO: make an AP unit test that verifies the static resources for these maps from zilliandomizer


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
