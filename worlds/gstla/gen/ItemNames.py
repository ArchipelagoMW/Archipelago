from typing import Dict
from .InternalItemNames import InternalItemName, item_id_by_py_name


class ItemName(InternalItemName):
    pass

item_id_by_name: Dict[str, int] = {
    getattr(ItemName, key): value
    for key, value in item_id_by_py_name.items()
}
# Special case for empty item
item_id_by_name["Empty"] = 0

name_by_item_id: Dict[int, str] = {
    value: key for key, value in item_id_by_name.items()
}
