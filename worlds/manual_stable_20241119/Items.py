from BaseClasses import Item
from .Data import item_table
from .Game import filler_item_name, starting_index


######################
# Generate item lookups
######################

item_id_to_name: dict[int, str] = {}
item_name_to_item: dict[str, dict] = {}
item_name_groups: dict[str, str] = {}
advancement_item_names: set[str] = set()
lastItemId = -1

count = starting_index

# add the filler item to the list of items for lookup
if filler_item_name:
    item_table.append({
        "name": filler_item_name
    })

# add sequential generated ids to the lists
for key, val in enumerate(item_table):
    if "id" in item_table[key]:
        item_id = item_table[key]["id"]
        if item_id >= count:
            count = item_id
        else:
            raise ValueError(f"{item_table[key]['name']} has an invalid ID. ID must be at least {count + 1}")

    item_table[key]["id"] = count
    item_table[key]["progression"] = val["progression"] if "progression" in val else False
    count += 1

for item in item_table:
    item_name = item["name"]
    item_id_to_name[item["id"]] = item_name
    item_name_to_item[item_name] = item

    if item["id"] is not None:
        lastItemId = max(lastItemId, item["id"])

    for c in item.get("category", []):
        if c not in item_name_groups:
            item_name_groups[c] = []
        item_name_groups[c].append(item_name)

    for v in item.get("value", {}).keys():
        group_name = f"has_{v.lower().strip()}_value"
        if group_name not in item_name_groups:
            item_name_groups[group_name] = []
        item_name_groups[group_name].append(item_name)

item_id_to_name[None] = "__Victory__"
item_name_to_id = {name: id for id, name in item_id_to_name.items()}


######################
# Item classes
######################


class ManualItem(Item):
    game = "Manual"
