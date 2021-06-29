from typing import Dict, Set

item_table = {}

lookup_id_to_name:Dict[int, str] = {data.id: item_name for item_name, data in item_table.items()}
lookup_type_to_names:Dict[str, Set[str]] = {}
for item, item_data in item_table.items():
    lookup_type_to_names.setdefault(item_data.type, set()).add(item)