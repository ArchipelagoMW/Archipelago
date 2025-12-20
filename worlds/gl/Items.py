from collections.abc import Mapping
from types import MappingProxyType
from typing import Final, NamedTuple, List, Dict

from BaseClasses import Item, ItemClassification
from worlds.gl.Data import item_classifications


class ItemData:
    id: int
    item_name: str
    progression: ItemClassification
    rom_id: int
    frequency: int

    def __init__(self, id: int | None, item_name: str, progression: str, rom_id: str = "0x0", frequency: int = 1):
        self.id = id
        self.item_name = item_name
        self.progression = item_classifications[progression]
        self.rom_id = int(rom_id, 16)
        self.frequency = frequency



class GLItem(Item):
    game: str = "Gauntlet Legends"

def import_items() -> List[ItemData]:
    import json
    import pkgutil

    return json.loads(pkgutil.get_data(__name__, "json/items.json").decode("utf-8"), object_hook=lambda d: ItemData(**d))

item_list: List[ItemData] = import_items()
item_table: Dict[str, ItemData] = {item.item_name: item for item in item_list}
items_by_id: Dict[int, ItemData] = {item.id: item for item in item_list}
