from typing import Dict, NamedTuple, Optional, Set

from BaseClasses import Item, ItemClassification as IC
from .Constants import DSTAP_ITEMS, ITEM_ID_OFFSET

class DSTItem(Item):
    game = "Don't Starve Together"

class DSTItemData(NamedTuple):
    code: Optional[int] = None
    type: IC = IC.filler
    tags: Set[str] = set()

def generate_item_map() -> Dict[str, DSTItemData]:
    ret: Dict[str, DSTItemData] = {}
    for v in DSTAP_ITEMS:
        code:int = v[0] + ITEM_ID_OFFSET
        name:str = v[1]
        tags: Set[str] = set(v[3])

        if "nonwinter" in tags:
            tags.update(["autumn", "spring", "summer"])
        if "nonspring" in tags:
            tags.update(["autumn", "winter", "summer"])
        if "nonsummer" in tags:
            tags.update(["autumn", "winter", "spring"])

        classification:IC = (
            IC.progression if "progression" in tags else
            IC.progression_skip_balancing if "progression_skip_balancing" in tags else
            IC.useful if "useful" in tags else
            IC.trap if "trap" in tags else
            IC.filler
        )
        ret.setdefault(name, DSTItemData(code, classification, tags))
    return ret

item_data_table: Dict[str, DSTItemData] = generate_item_map()
item_name_to_id = {name: data.code for name, data in item_data_table.items() if data.code is not None}