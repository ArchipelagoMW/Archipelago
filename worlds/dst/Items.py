from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification as IC
from .Constants import DSTAP_ITEMS, ITEM_ID_OFFSET

class DSTItem(Item):
	 game = "Don't Starve Together"
	 
class DSTItemData(NamedTuple):
	code: Optional[int] = None
	type: IC = IC.filler
	tags: set[str] = set()

def generate_item_map() -> Dict[str, DSTItemData]:
	ret: Dict[str, DSTItemData] = {}
	for v in DSTAP_ITEMS:
		code:int = v[0] + ITEM_ID_OFFSET
		name:str = v[1]
		classification:IC = IC.filler
		tags: set[str] = set()
		match v[3]:
			case "progression": classification = IC.progression
			case "useful": classification = IC.useful
			case "trap": classification = IC.trap; tags.update(["filler", "trap", "regulartrap"])
			case "seasontrap": classification = IC.trap; tags.update(["filler", "trap", "seasontrap"])
			case "junk": tags.add("filler")

		ret.setdefault(name, DSTItemData(code, classification, tags))
	return ret

item_data_table: Dict[str, DSTItemData] = generate_item_map()
item_name_to_id = {name: data.code for name, data in item_data_table.items() if data.code is not None}