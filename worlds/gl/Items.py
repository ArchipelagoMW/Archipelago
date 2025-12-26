from collections.abc import Mapping
from types import MappingProxyType
from typing import Final, List

from BaseClasses import Item, ItemClassification
from worlds.gl.Data import item_classifications, portals, obelisks


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
item_table: Final[Mapping[str, ItemData]] = MappingProxyType({item.item_name: item for item in item_list})
items_by_id: Final[Mapping[int, ItemData]] = MappingProxyType({item.id: item for item in item_list})

gauntlet_item_name_groups = {
    "Runestone": [f"Runestone {i}" for i in range(1, 14)],
    "Portal": portals.keys(),
    "Obelisk": obelisks,
}
